"""Solend protocol adapter for Solana.

Solend is one of the original lending protocols on Solana.
This adapter reads obligation accounts to monitor positions.

References:
- Solend V2 Program: So1endDq2YkqhipRh3WViPa8hFb54GbLEaQo5Knh1Lz (deprecated)
- Solend V2 Program: SLendK7ySfcEzyaFqy93gDnSwDmkTRClu6nBVSO4oqd (active)
- Obligation layout: https://github.com/solendprotocol/solana-program-library
"""
from __future__ import annotations

import asyncio
import base64
import struct
from datetime import datetime
from typing import Optional

import httpx

from .base import HealthStatus, Position, ProtocolAdapter, TokenPosition

# Solend program IDs
SOLEND_PROGRAM_V1 = "So1endDq2YkqhipRh3WViPa8hFb54GbLEaQo5Knh1Lz"
SOLEND_PROGRAM_V2 = "SLendK7ySfcEzyaFqy93gDnSwDmkTRClu6nBVSO4oqd"

# Solend main pool
SOLEND_MAIN_POOL = "4UpD2fh7xH3VP9QQaXtsS1YY3bxzWhtfpks7FatyKvdY"

# Solend reserves for common tokens
SOLEND_RESERVES = {
    "SOL": "8PbodeaosQP19SjYFx855UMqWxH2HynZLdBXmsrbac36",
    "USDC": "BgxfHJDzm44T7XG68MYKx7YisTjZu73tVovyZSjJMpmw",
    "USDT": "8K9WC8xoh2rtQNY7iEGXtPvnKqFrRH3AFav1JqomGiDk",
    "mSOL": "CCpirWrgNuBVLdkP2haxLTbD6XEsfiKheLyBTSPieSpY",
}


class SolendAdapter(ProtocolAdapter):
    """Adapter for Solend lending protocol on Solana."""

    def __init__(
        self,
        rpc_url: str,
        pool: str = SOLEND_MAIN_POOL,
        program_id: str = SOLEND_PROGRAM_V2,
    ):
        super().__init__(rpc_url)
        self.pool = pool
        self.program_id = program_id
        self._client = httpx.AsyncClient(timeout=30.0)

    @property
    def name(self) -> str:
        return "Solend"

    async def _rpc_call(self, method: str, params: list) -> dict:
        """Make a JSON-RPC call to Solana."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }
        resp = await self._client.post(self.rpc_url, json=payload)
        resp.raise_for_status()
        result = resp.json()
        if "error" in result:
            raise RuntimeError(f"RPC error: {result['error']}")
        return result.get("result", {})

    async def _get_program_accounts(
        self, program_id: str, filters: list[dict]
    ) -> list[dict]:
        """Fetch program accounts with filters."""
        result = await self._rpc_call(
            "getProgramAccounts",
            [
                program_id,
                {
                    "encoding": "base64",
                    "commitment": "confirmed",
                    "filters": filters,
                },
            ],
        )
        return result if isinstance(result, list) else []

    def _parse_obligation(
        self, data: bytes, owner: str, pubkey: str
    ) -> Optional[Position]:
        """Parse a Solend obligation account into a Position.

        Solend obligation layout:
        - 1 byte: version
        - 8 bytes: last_update_slot
        - 1 byte: last_update_stale
        - 32 bytes: lending_market
        - 32 bytes: owner
        - 16 bytes: deposited_value (u128, WAD scaled)
        - 16 bytes: borrowed_value (u128, WAD scaled)
        - 16 bytes: allowed_borrow_value (u128, WAD scaled)
        - 16 bytes: unhealthy_borrow_value (u128, WAD scaled)
        - 1 byte: deposits_len
        - 1 byte: borrows_len
        - Variable: deposit entries (56 bytes each)
        - Variable: borrow entries (80 bytes each)
        """
        if len(data) < 140:
            return None

        try:
            offset = 0

            # Version (1 byte)
            version = data[offset]
            offset += 1

            # Last update slot (8 bytes)
            last_update_slot = struct.unpack_from("<Q", data, offset)[0]
            offset += 8

            # Last update stale (1 byte)
            offset += 1

            # Lending market (32 bytes)
            lending_market = base64.b64encode(data[offset : offset + 32]).decode()
            offset += 32

            # Owner (32 bytes)
            obligation_owner = base64.b64encode(data[offset : offset + 32]).decode()
            offset += 32

            # Deposited value - u128, WAD scaled (1e18)
            deposited_raw = int.from_bytes(data[offset : offset + 16], "little")
            deposited_value = deposited_raw / 1e18
            offset += 16

            # Borrowed value - u128, WAD scaled
            borrowed_raw = int.from_bytes(data[offset : offset + 16], "little")
            borrowed_value = borrowed_raw / 1e18
            offset += 16

            # Allowed borrow value - u128, WAD scaled
            allowed_borrow_raw = int.from_bytes(data[offset : offset + 16], "little")
            allowed_borrow_value = allowed_borrow_raw / 1e18
            offset += 16

            # Unhealthy borrow value - u128, WAD scaled
            unhealthy_raw = int.from_bytes(data[offset : offset + 16], "little")
            unhealthy_borrow_value = unhealthy_raw / 1e18
            offset += 16

            # Calculate health factor
            health_factor = 0.0
            if borrowed_value > 0:
                health_factor = unhealthy_borrow_value / borrowed_value
            elif deposited_value > 0:
                health_factor = 99.0  # No debt = very healthy

            # Liquidation threshold
            liq_threshold = 0.0
            if deposited_value > 0:
                liq_threshold = unhealthy_borrow_value / deposited_value

            status = HealthStatus.from_health_factor(health_factor)

            # Number of deposits and borrows
            deposits_len = data[offset] if offset < len(data) else 0
            offset += 1
            borrows_len = data[offset] if offset < len(data) else 0
            offset += 1

            position = Position(
                protocol="solend",
                owner=owner,
                position_key=pubkey,
                collateral=[],
                debt=[],
                total_collateral_usd=deposited_value,
                total_debt_usd=borrowed_value,
                health_factor=health_factor,
                liquidation_threshold=liq_threshold,
                ltv=borrowed_value / deposited_value if deposited_value > 0 else 0,
                status=status,
                last_updated=datetime.utcnow(),
                raw_data={
                    "account": pubkey,
                    "version": version,
                    "last_update_slot": last_update_slot,
                    "deposited_value": deposited_value,
                    "borrowed_value": borrowed_value,
                    "allowed_borrow_value": allowed_borrow_value,
                    "unhealthy_borrow_value": unhealthy_borrow_value,
                    "deposits_count": deposits_len,
                    "borrows_count": borrows_len,
                },
            )
            return position
        except Exception as e:
            print(f"[Solend] Parse error: {e}")
            return None

    async def get_positions(self, owner: str) -> list[Position]:
        """Fetch all Solend positions for a wallet.

        Queries Solend program for obligation accounts where
        owner field matches the given wallet.
        """
        positions = []

        try:
            # Obligation accounts: owner at offset 42
            # (1 version + 8 slot + 1 stale + 32 market = 42)
            accounts = await self._get_program_accounts(
                self.program_id,
                [
                    {
                        "memcmp": {
                            "offset": 42,
                            "bytes": owner,
                        }
                    },
                    {
                        "memcmp": {
                            "offset": 10,
                            "bytes": self.pool,
                        }
                    },
                ],
            )

            for account in accounts:
                pubkey = account.get("pubkey", "")
                data_b64 = account.get("account", {}).get("data", ["", ""])[0]
                if not data_b64:
                    continue

                data = base64.b64decode(data_b64)
                position = self._parse_obligation(data, owner, pubkey)
                if position:
                    positions.append(position)

        except Exception as e:
            print(f"[Solend] Error fetching positions for {owner}: {e}")

        return positions

    async def get_health_factor(self, position_key: str) -> float:
        """Get current health factor for a Solend position."""
        try:
            result = await self._rpc_call(
                "getAccountInfo",
                [position_key, {"encoding": "base64", "commitment": "confirmed"}],
            )
            value = result.get("value")
            if not value:
                return 0.0

            data_b64 = value.get("data", ["", ""])[0]
            data = base64.b64decode(data_b64)

            position = self._parse_obligation(data, "", position_key)
            if position:
                return position.health_factor
            return 0.0
        except Exception:
            return 0.0

    async def get_liquidation_price(self, position_key: str) -> dict[str, float]:
        """Get liquidation prices for each collateral asset."""
        return {}

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()
