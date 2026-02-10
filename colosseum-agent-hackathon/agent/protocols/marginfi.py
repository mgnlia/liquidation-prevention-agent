"""MarginFi Protocol Adapter for Solana"""
import struct
from typing import Optional
import httpx
import structlog

from .base import (
    ProtocolAdapter, PositionData, CollateralPosition,
    DebtPosition, Protocol, RiskLevel,
)

logger = structlog.get_logger()

MARGINFI_PROGRAM = "MFv2hWf31Z9kbCa1snEPYctwafyhdJnV4QSdzCrRKg"


class MarginFiAdapter(ProtocolAdapter):
    """Adapter for MarginFi lending protocol on Solana"""

    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url
        self.client = httpx.AsyncClient(timeout=30)

    async def get_protocol_name(self) -> str:
        return "MarginFi"

    async def get_positions(self, wallet_address: str) -> list[PositionData]:
        """Fetch all MarginFi margin accounts for a wallet"""
        positions = []

        try:
            # Query MarginFi marginfi_account accounts
            margin_accounts = await self._get_margin_accounts(wallet_address)

            for account in margin_accounts:
                position = await self._parse_margin_account(wallet_address, account)
                if position and position.total_debt_usd > 0:
                    positions.append(position)

        except Exception as e:
            logger.error("marginfi_fetch_error", wallet=wallet_address, error=str(e))

        return positions

    async def get_health_factor(self, obligation_key: str) -> float:
        """Get health factor for a MarginFi margin account"""
        try:
            account_data = await self._get_account_data(obligation_key)
            if account_data:
                return self._calculate_health_factor(account_data)
        except Exception as e:
            logger.error("marginfi_health_error", account=obligation_key, error=str(e))
        return 0.0

    async def _get_margin_accounts(self, wallet_address: str) -> list[dict]:
        """Query MarginFi margin accounts using getProgramAccounts"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getProgramAccounts",
            "params": [
                MARGINFI_PROGRAM,
                {
                    "encoding": "base64",
                    "filters": [
                        # MarginFi account discriminator + authority filter
                        {
                            "memcmp": {
                                "offset": 40,  # Authority offset in MarginFi account
                                "bytes": wallet_address,
                            }
                        },
                    ],
                },
            ],
        }

        response = await self.client.post(self.rpc_url, json=payload)
        result = response.json()

        if "result" in result:
            return result["result"]
        return []

    async def _get_account_data(self, account_key: str) -> Optional[bytes]:
        """Fetch raw account data"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getAccountInfo",
            "params": [account_key, {"encoding": "base64"}],
        }

        response = await self.client.post(self.rpc_url, json=payload)
        result = response.json()

        if result.get("result", {}).get("value"):
            import base64
            return base64.b64decode(result["result"]["value"]["data"][0])
        return None

    async def _parse_margin_account(
        self, wallet_address: str, account: dict
    ) -> Optional[PositionData]:
        """Parse a MarginFi margin account into PositionData"""
        try:
            import base64
            pubkey = account["pubkey"]
            data = base64.b64decode(account["account"]["data"][0])

            # MarginFi account layout (simplified):
            # [8 discriminator][32 group][32 authority][lending_account...]
            # lending_account has balances array with active flag, bank_pk, asset/liability shares

            total_collateral = 0.0
            total_debt = 0.0
            collaterals = []
            debts = []

            # Parse active balances
            # Each balance: [1 active][32 bank_pk][16 asset_shares][16 liability_shares]
            balance_offset = 72  # After discriminator + group + authority
            num_balances = min(16, (len(data) - balance_offset) // 65)

            for i in range(num_balances):
                offset = balance_offset + (i * 65)
                if offset + 65 > len(data):
                    break

                active = data[offset]
                if not active:
                    continue

                bank_pk = data[offset + 1:offset + 33]
                # Asset shares (u128, but we read as two u64s)
                asset_lo = struct.unpack_from("<Q", data, offset + 33)[0]
                asset_hi = struct.unpack_from("<Q", data, offset + 41)[0]
                # Liability shares
                liability_lo = struct.unpack_from("<Q", data, offset + 49)[0]
                liability_hi = struct.unpack_from("<Q", data, offset + 57)[0]

                asset_value = (asset_hi * (2**64) + asset_lo) / 1e15  # Approximate USD
                liability_value = (liability_hi * (2**64) + liability_lo) / 1e15

                if asset_value > 0.01:
                    total_collateral += asset_value
                    collaterals.append(CollateralPosition(
                        mint=bank_pk[:8].hex(),
                        symbol=f"ASSET_{i}",
                        amount=asset_value,
                        value_usd=asset_value,
                        ltv=0.80,
                        liquidation_threshold=0.85,
                    ))

                if liability_value > 0.01:
                    total_debt += liability_value
                    debts.append(DebtPosition(
                        mint=bank_pk[:8].hex(),
                        symbol=f"DEBT_{i}",
                        amount=liability_value,
                        value_usd=liability_value,
                        borrow_rate_apy=0.06,
                    ))

            health_factor = (
                total_collateral * 0.85 / total_debt
                if total_debt > 0
                else float("inf")
            )

            return PositionData(
                protocol=Protocol.MARGINFI,
                owner=wallet_address,
                obligation_key=pubkey,
                health_factor=health_factor,
                total_collateral_usd=total_collateral,
                total_debt_usd=total_debt,
                net_value_usd=total_collateral - total_debt,
                risk_level=self.classify_risk(health_factor),
                collaterals=collaterals,
                debts=debts,
            )

        except Exception as e:
            logger.error("marginfi_parse_error", error=str(e))
            return None

    def _calculate_health_factor(self, account_data: bytes) -> float:
        """Calculate health factor from raw margin account data"""
        try:
            if len(account_data) < 140:
                return 0.0

            total_assets = 0.0
            total_liabilities = 0.0
            balance_offset = 72

            for i in range(16):
                offset = balance_offset + (i * 65)
                if offset + 65 > len(account_data):
                    break
                if not account_data[offset]:
                    continue

                asset_lo = struct.unpack_from("<Q", account_data, offset + 33)[0]
                liability_lo = struct.unpack_from("<Q", account_data, offset + 49)[0]

                total_assets += asset_lo / 1e15
                total_liabilities += liability_lo / 1e15

            if total_liabilities == 0:
                return float("inf")

            return (total_assets * 0.85) / total_liabilities

        except Exception:
            return 0.0

    async def close(self):
        await self.client.aclose()
