"""MarginFi protocol adapter for Solana.

MarginFi is a decentralized lending protocol on Solana with a focus on
risk management and capital efficiency.

References:
- MarginFi V2 Program: MFv2hWf31Z9kbCa1snEPYctwafyhdvnV7FZnsebVacA
- MarginFi Account layout: https://github.com/mrgnlabs/marginfi-v2
"""
from __future__ import annotations

import asyncio
import base64
import struct
from datetime import datetime
from typing import Optional

import httpx

from .base import HealthStatus, Position, ProtocolAdapter, TokenPosition

# MarginFi V2 program ID
MARGINFI_PROGRAM = "MFv2hWf31Z9kbCa1snEPYctwafyhdvnV7FZnsebVacA"

# MarginFi group (main pool)
MARGINFI_GROUP = "4qp6Fx6tnZkY5Wropq9wUYgtFxXKwE6viZxFkKP5AfQH"

# Bank accounts for common tokens
MARGINFI_BANKS = {
    "SOL": "CCKtUs6Cgwo4aaQUmBPmyoApH2gUDErxNZCAoD2sYNa6",
    "USDC": "2s37akK2eyBbp8DZgCm7RtsaEz8eJP3Nxd4urLHQv7yB",
    "USDT": "HmpMfL8942u22htC4EMiWgLX931g3sacXFR6KjuLgKLV",
    "mSOL": "BYQFZ5MjyqHNJgKLYQoXoD9UiMfX1MCXE5TYApYBwxjt",
    "jitoSOL": "Bohoc1ikHLD7xKJuzTyiTyCwzaL3e4a268Yo61BGJjhp",
}


class MarginFiAdapter(ProtocolAdapter):
    """Adapter for MarginFi V2 lending protocol on Solana."""

    def __init__(self, rpc_url: str, group: str = MARGINFI_GROUP):
        super().__init__(rpc_url)
        self.group = group
        self._client = httpx.AsyncClient(timeout=30.0)

    @property
    def name(self) -> str:
        return "MarginFi"

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

    async def _fetch_bank_data(self, bank_pubkey: str) -> Optional[dict]:
        """Fetch and parse a MarginFi bank account."""
        result = await self._rpc_call(
            "getAccountInfo",
            [bank_pubkey, {"encoding": "base64", "commitment": "confirmed"}],
        )
        value = result.get("value")
        if not value:
            return None

        data_b64 = value.get("data", ["", ""])[0]
        data = base64.b64decode(data_b64)

        # Bank account layout (simplified):
        # 8 bytes discriminator
        # 32 bytes mint
        # 16 bytes total_asset_shares (I128)
        # 16 bytes total_liability_shares (I128)
        # ... more fields
        if len(data) < 72:
            return None

        mint = base64.b64encode(data[8:40]).decode()
        return {
            "pubkey": bank_pubkey,
            "mint": mint,
            "data_len": len(data),
        }

    def _parse_marginfi_account(
        self, data: bytes, owner: str, pubkey: str
    ) -> Optional[Position]:
        """Parse a MarginFi margin account into a Position.

        MarginFi account layout (simplified):
        - 8 bytes: discriminator
        - 32 bytes: group
        - 32 bytes: authority (owner)
        - N * lending_account_balance entries
        """
        if len(data) < 80:
            return None

        try:
            # Skip discriminator (8 bytes)
            offset = 8

            # Group (32 bytes)
            group = base64.b64encode(data[offset : offset + 32]).decode()
            offset += 32

            # Authority/owner (32 bytes)
            authority = base64.b64encode(data[offset : offset + 32]).decode()
            offset += 32

            position = Position(
                protocol="marginfi",
                owner=owner,
                position_key=pubkey,
                collateral=[],
                debt=[],
                total_collateral_usd=0.0,
                total_debt_usd=0.0,
                health_factor=0.0,
                liquidation_threshold=0.80,  # MarginFi typical LT
                status=HealthStatus.HEALTHY,
                last_updated=datetime.utcnow(),
                raw_data={"account": pubkey, "group": group, "data_len": len(data)},
            )
            return position
        except Exception:
            return None

    async def get_positions(self, owner: str) -> list[Position]:
        """Fetch all MarginFi positions for a wallet.

        Queries MarginFi program for marginfi accounts where
        authority == owner.
        """
        positions = []

        try:
            # MarginFi accounts: filter by authority at offset 40
            # (8 discriminator + 32 group = 40)
            accounts = await self._get_program_accounts(
                MARGINFI_PROGRAM,
                [
                    {
                        "memcmp": {
                            "offset": 8,
                            "bytes": self.group,
                        }
                    },
                    {
                        "memcmp": {
                            "offset": 40,
                            "bytes": owner,
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
                position = self._parse_marginfi_account(data, owner, pubkey)
                if position:
                    positions.append(position)

        except Exception as e:
            print(f"[MarginFi] Error fetching positions for {owner}: {e}")

        return positions

    async def get_health_factor(self, position_key: str) -> float:
        """Get current health factor for a MarginFi position."""
        return 0.0

    async def get_liquidation_price(self, position_key: str) -> dict[str, float]:
        """Get liquidation prices for each collateral asset."""
        return {}

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()
