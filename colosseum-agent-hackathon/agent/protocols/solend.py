"""Solend Protocol Adapter for Solana"""
import struct
from typing import Optional
import httpx
import structlog

from .base import (
    ProtocolAdapter, PositionData, CollateralPosition,
    DebtPosition, Protocol, RiskLevel,
)

logger = structlog.get_logger()

SOLEND_PROGRAM = "So1endDq2YkqhipRh3WViPa8hFMqRV1JimkXg5H2RGD"


class SolendAdapter(ProtocolAdapter):
    """Adapter for Solend V2 lending protocol on Solana"""

    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url
        self.client = httpx.AsyncClient(timeout=30)

    async def get_protocol_name(self) -> str:
        return "Solend"

    async def get_positions(self, wallet_address: str) -> list[PositionData]:
        """Fetch all Solend obligations for a wallet"""
        positions = []

        try:
            obligations = await self._get_obligations(wallet_address)
            for obligation in obligations:
                position = await self._parse_obligation(wallet_address, obligation)
                if position and position.total_debt_usd > 0:
                    positions.append(position)
        except Exception as e:
            logger.error("solend_fetch_error", wallet=wallet_address, error=str(e))

        return positions

    async def get_health_factor(self, obligation_key: str) -> float:
        """Get health factor for a Solend obligation"""
        try:
            data = await self._get_account_data(obligation_key)
            if data:
                return self._calculate_health_factor(data)
        except Exception as e:
            logger.error("solend_health_error", obligation=obligation_key, error=str(e))
        return 0.0

    async def _get_obligations(self, wallet_address: str) -> list[dict]:
        """Query Solend obligation accounts"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getProgramAccounts",
            "params": [
                SOLEND_PROGRAM,
                {
                    "encoding": "base64",
                    "filters": [
                        {"dataSize": 916},  # Solend obligation size
                        {
                            "memcmp": {
                                "offset": 2,  # Owner offset
                                "bytes": wallet_address,
                            }
                        },
                    ],
                },
            ],
        }

        response = await self.client.post(self.rpc_url, json=payload)
        result = response.json()
        return result.get("result", [])

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

    async def _parse_obligation(
        self, wallet_address: str, account: dict
    ) -> Optional[PositionData]:
        """Parse Solend obligation into PositionData"""
        try:
            import base64
            pubkey = account["pubkey"]
            data = base64.b64decode(account["account"]["data"][0])

            # Solend obligation layout:
            # [1 version][1 last_update_slot...][32 lending_market][32 owner]
            # [u128 deposited_value][u128 borrowed_value][u128 allowed_borrow_value]
            # [u128 unhealthy_borrow_value]
            # [deposits_count][deposits...][borrows_count][borrows...]

            total_collateral = 0.0
            total_debt = 0.0
            collaterals = []
            debts = []

            # Parse deposited_value (u128 at offset ~66)
            offset = 66
            if len(data) >= offset + 16:
                deposited_lo = struct.unpack_from("<Q", data, offset)[0]
                deposited_hi = struct.unpack_from("<Q", data, offset + 8)[0]
                total_collateral = (deposited_hi * (2**64) + deposited_lo) / 1e18

            # Parse borrowed_value (u128)
            offset += 16
            if len(data) >= offset + 16:
                borrowed_lo = struct.unpack_from("<Q", data, offset)[0]
                borrowed_hi = struct.unpack_from("<Q", data, offset + 8)[0]
                total_debt = (borrowed_hi * (2**64) + borrowed_lo) / 1e18

            # Parse individual deposits
            deposits_offset = 130  # Approximate
            if len(data) > deposits_offset:
                num_deposits = data[deposits_offset]
                dep_offset = deposits_offset + 1

                for i in range(min(num_deposits, 10)):
                    if dep_offset + 56 > len(data):
                        break
                    reserve_key = data[dep_offset:dep_offset + 32]
                    deposited_amount = struct.unpack_from("<Q", dep_offset + 32, data)[0] if dep_offset + 40 <= len(data) else 0
                    value = struct.unpack_from("<Q", data, dep_offset + 40)[0] / 1e6 if dep_offset + 48 <= len(data) else 0

                    if value > 0:
                        collaterals.append(CollateralPosition(
                            mint=reserve_key[:4].hex(),
                            symbol=f"COL_{i}",
                            amount=deposited_amount / 1e9,
                            value_usd=value,
                            ltv=0.75,
                            liquidation_threshold=0.85,
                        ))
                    dep_offset += 56

            health_factor = (
                total_collateral * 0.85 / total_debt
                if total_debt > 0
                else float("inf")
            )

            return PositionData(
                protocol=Protocol.SOLEND,
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
            logger.error("solend_parse_error", error=str(e))
            return None

    def _calculate_health_factor(self, data: bytes) -> float:
        """Calculate health factor from raw obligation data"""
        try:
            offset = 66
            deposited_lo = struct.unpack_from("<Q", data, offset)[0]
            total_collateral = deposited_lo / 1e18

            offset += 16
            borrowed_lo = struct.unpack_from("<Q", data, offset)[0]
            total_debt = borrowed_lo / 1e18

            if total_debt == 0:
                return float("inf")
            return (total_collateral * 0.85) / total_debt
        except Exception:
            return 0.0

    async def close(self):
        await self.client.aclose()
