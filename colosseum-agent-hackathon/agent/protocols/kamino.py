"""Kamino Lending Protocol Adapter for Solana"""
import struct
from typing import Optional
import httpx
import structlog

from .base import (
    ProtocolAdapter, PositionData, CollateralPosition,
    DebtPosition, Protocol, RiskLevel,
)

logger = structlog.get_logger()

# Kamino Lending program ID
KAMINO_LENDING_PROGRAM = "KLend2g3cP87ber41GRRLYPqxQ1p57Y5MR8D68Lds"

# Known token mints (devnet/mainnet)
TOKEN_INFO = {
    "So11111111111111111111111111111111111111112": {"symbol": "SOL", "decimals": 9},
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": {"symbol": "USDC", "decimals": 6},
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": {"symbol": "USDT", "decimals": 6},
    "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So": {"symbol": "mSOL", "decimals": 9},
    "7dHbWXmci3dT8UFYWYZweBLXgycu7Y3iL6trKn1Y7ARj": {"symbol": "stSOL", "decimals": 9},
}


class KaminoAdapter(ProtocolAdapter):
    """Adapter for Kamino Lending (KLend) protocol on Solana"""

    def __init__(self, rpc_url: str, helius_api_key: Optional[str] = None):
        self.rpc_url = rpc_url
        self.helius_api_key = helius_api_key
        self.client = httpx.AsyncClient(timeout=30)

    async def get_protocol_name(self) -> str:
        return "Kamino Lending"

    async def get_positions(self, wallet_address: str) -> list[PositionData]:
        """Fetch all Kamino lending positions for a wallet"""
        positions = []

        try:
            # Query Kamino obligation accounts owned by this wallet
            obligations = await self._get_obligation_accounts(wallet_address)

            for obligation in obligations:
                position = await self._parse_obligation(wallet_address, obligation)
                if position and position.total_debt_usd > 0:
                    positions.append(position)

        except Exception as e:
            logger.error("kamino_fetch_error", wallet=wallet_address, error=str(e))

        return positions

    async def get_health_factor(self, obligation_key: str) -> float:
        """Get health factor for a specific Kamino obligation"""
        try:
            account_data = await self._get_account_data(obligation_key)
            if account_data:
                return self._calculate_health_factor(account_data)
        except Exception as e:
            logger.error("kamino_health_error", obligation=obligation_key, error=str(e))
        return 0.0

    async def _get_obligation_accounts(self, wallet_address: str) -> list[dict]:
        """Query Kamino obligation accounts for a wallet using getProgramAccounts"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getProgramAccounts",
            "params": [
                KAMINO_LENDING_PROGRAM,
                {
                    "encoding": "base64",
                    "filters": [
                        {"dataSize": 1300},  # Obligation account size
                        {
                            "memcmp": {
                                "offset": 8,  # Owner field offset
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
            "params": [
                account_key,
                {"encoding": "base64"},
            ],
        }

        response = await self.client.post(self.rpc_url, json=payload)
        result = response.json()

        if result.get("result", {}).get("value"):
            import base64
            data = result["result"]["value"]["data"][0]
            return base64.b64decode(data)
        return None

    async def _parse_obligation(
        self, wallet_address: str, obligation_account: dict
    ) -> Optional[PositionData]:
        """Parse a Kamino obligation account into PositionData"""
        try:
            import base64
            pubkey = obligation_account["pubkey"]
            data = base64.b64decode(obligation_account["account"]["data"][0])

            # Parse obligation data structure
            # Kamino obligation layout (simplified):
            # [8 bytes discriminator][32 bytes owner][32 bytes lending_market]
            # [deposits...][borrows...]
            
            total_collateral = 0.0
            total_debt = 0.0
            collaterals = []
            debts = []

            # Parse deposit reserves (collateral)
            # Each deposit: [32 bytes reserve][8 bytes deposited_amount][8 bytes market_value]
            num_deposits = struct.unpack_from("<B", data, 72)[0] if len(data) > 72 else 0
            offset = 73

            for i in range(min(num_deposits, 8)):
                if offset + 48 > len(data):
                    break
                reserve_key = base64.b64encode(data[offset:offset + 32]).decode()
                deposited = struct.unpack_from("<Q", data, offset + 32)[0]
                market_value = struct.unpack_from("<Q", data, offset + 40)[0]

                value_usd = market_value / 1e6  # 6 decimal USD
                total_collateral += value_usd

                collaterals.append(CollateralPosition(
                    mint=reserve_key[:8] + "...",
                    symbol=f"COLLATERAL_{i}",
                    amount=deposited / 1e9,
                    value_usd=value_usd,
                    ltv=0.75,  # Default LTV
                    liquidation_threshold=0.85,
                ))
                offset += 48

            # Parse borrow reserves (debt)
            num_borrows = struct.unpack_from("<B", data, offset)[0] if offset < len(data) else 0
            offset += 1

            for i in range(min(num_borrows, 8)):
                if offset + 48 > len(data):
                    break
                reserve_key = base64.b64encode(data[offset:offset + 32]).decode()
                borrowed = struct.unpack_from("<Q", data, offset + 32)[0]
                market_value = struct.unpack_from("<Q", data, offset + 40)[0]

                value_usd = market_value / 1e6
                total_debt += value_usd

                debts.append(DebtPosition(
                    mint=reserve_key[:8] + "...",
                    symbol=f"DEBT_{i}",
                    amount=borrowed / 1e9,
                    value_usd=value_usd,
                    borrow_rate_apy=0.05,
                ))
                offset += 48

            # Calculate health factor
            health_factor = (
                total_collateral * 0.85 / total_debt
                if total_debt > 0
                else float("inf")
            )

            risk_level = self.classify_risk(health_factor)

            return PositionData(
                protocol=Protocol.KAMINO,
                owner=wallet_address,
                obligation_key=pubkey,
                health_factor=health_factor,
                total_collateral_usd=total_collateral,
                total_debt_usd=total_debt,
                net_value_usd=total_collateral - total_debt,
                risk_level=risk_level,
                collaterals=collaterals,
                debts=debts,
            )

        except Exception as e:
            logger.error("kamino_parse_error", error=str(e))
            return None

    def _calculate_health_factor(self, account_data: bytes) -> float:
        """Calculate health factor from raw obligation data"""
        try:
            # Simplified: extract total collateral and debt values
            if len(account_data) < 120:
                return 0.0

            # These offsets are simplified — real implementation would use
            # the full Kamino IDL for precise deserialization
            total_collateral = struct.unpack_from("<Q", account_data, 80)[0] / 1e6
            total_debt = struct.unpack_from("<Q", account_data, 96)[0] / 1e6

            if total_debt == 0:
                return float("inf")

            return (total_collateral * 0.85) / total_debt

        except Exception:
            return 0.0

    async def close(self):
        await self.client.aclose()
