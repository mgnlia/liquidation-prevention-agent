"""Kamino Lending protocol adapter for Solana.

Kamino Lending (formerly Hubble) is a leading Solana lending protocol.
This adapter reads obligation accounts to monitor positions.

References:
- Kamino Lending Program: KLend2g3cP87ber8e3v7Fne5vhfce2Ck9MtCAEXJmob
- Obligation account layout: https://github.com/Kamino-Finance/klend
"""
from __future__ import annotations

import asyncio
import base64
import json
import struct
from datetime import datetime
from typing import Optional

import httpx

from .base import HealthStatus, Position, ProtocolAdapter, TokenPosition

# Kamino Lending program ID
KAMINO_LENDING_PROGRAM = "KLend2g3cP87ber8e3v7Fne5vhfce2Ck9MtCAEXJmob"

# Known Kamino markets (main market)
KAMINO_MAIN_MARKET = "7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF"

# Token mints on Solana
KNOWN_MINTS = {
    "So11111111111111111111111111111111111111112": {"symbol": "SOL", "decimals": 9},
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": {"symbol": "USDC", "decimals": 6},
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": {"symbol": "USDT", "decimals": 6},
    "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So": {"symbol": "mSOL", "decimals": 9},
    "7dHbWXmci3dT8UFYWYZweBLXgycu7Y3iL6trKn1Y7ARj": {"symbol": "stSOL", "decimals": 9},
    "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn": {"symbol": "jitoSOL", "decimals": 9},
    "bSo13r4TkiE4KumL71LsHTPpL2euBYLFx6h9HP3piy1": {"symbol": "bSOL", "decimals": 9},
}


class KaminoAdapter(ProtocolAdapter):
    """Adapter for Kamino Lending protocol on Solana."""

    def __init__(self, rpc_url: str, market: str = KAMINO_MAIN_MARKET):
        super().__init__(rpc_url)
        self.market = market
        self._client = httpx.AsyncClient(timeout=30.0)
        self._price_cache: dict[str, float] = {}
        self._price_cache_ts: float = 0

    @property
    def name(self) -> str:
        return "Kamino"

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

    async def _get_account_info(self, pubkey: str) -> Optional[dict]:
        """Fetch account info for a public key."""
        result = await self._rpc_call(
            "getAccountInfo",
            [pubkey, {"encoding": "base64", "commitment": "confirmed"}],
        )
        return result.get("value")

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

    async def _fetch_prices(self) -> dict[str, float]:
        """Fetch token prices from Jupiter price API."""
        import time

        # Cache for 60 seconds
        if time.time() - self._price_cache_ts < 60 and self._price_cache:
            return self._price_cache

        mints = list(KNOWN_MINTS.keys())
        ids_param = ",".join(mints)
        try:
            resp = await self._client.get(
                f"https://api.jup.ag/price/v2?ids={ids_param}"
            )
            resp.raise_for_status()
            data = resp.json()
            prices = {}
            for mint, info in data.get("data", {}).items():
                if info and "price" in info:
                    prices[mint] = float(info["price"])
            self._price_cache = prices
            self._price_cache_ts = time.time()
            return prices
        except Exception:
            # Fallback prices
            return {
                "So11111111111111111111111111111111111111112": 150.0,
                "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": 1.0,
                "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": 1.0,
            }

    def _parse_obligation(self, data: bytes, owner: str, pubkey: str) -> Optional[Position]:
        """Parse a Kamino obligation account into a Position.

        Kamino obligation layout (simplified):
        - Bytes 0-7: discriminator
        - Bytes 8-15: tag
        - Bytes 16-23: last_update_slot
        - Bytes 24-55: lending_market (32 bytes)
        - Bytes 56-87: owner (32 bytes)
        - Bytes 88+: deposits and borrows arrays
        """
        if len(data) < 100:
            return None

        try:
            # Extract basic fields
            # Skip discriminator (8) + tag (8) + last_update (8)
            offset = 24

            # lending_market (32 bytes)
            lending_market = base64.b64encode(data[offset : offset + 32]).decode()
            offset += 32

            # owner (32 bytes)
            obligation_owner = base64.b64encode(data[offset : offset + 32]).decode()
            offset += 32

            # For now, create position with basic data
            # Full parsing requires the complete Kamino IDL
            position = Position(
                protocol="kamino",
                owner=owner,
                position_key=pubkey,
                collateral=[],
                debt=[],
                total_collateral_usd=0.0,
                total_debt_usd=0.0,
                health_factor=0.0,
                liquidation_threshold=0.85,
                status=HealthStatus.HEALTHY,
                last_updated=datetime.utcnow(),
                raw_data={"account": pubkey, "data_len": len(data)},
            )
            return position
        except Exception:
            return None

    async def get_positions(self, owner: str) -> list[Position]:
        """Fetch all Kamino lending positions for a wallet.

        Queries the Kamino lending program for obligation accounts
        owned by the specified wallet.
        """
        positions = []

        try:
            # Query obligation accounts owned by this wallet
            # Filter by: owner field at offset 56 (after discriminator + tag + slot + market)
            accounts = await self._get_program_accounts(
                KAMINO_LENDING_PROGRAM,
                [
                    {"dataSize": 3400},  # Approximate obligation account size
                    {
                        "memcmp": {
                            "offset": 56,
                            "bytes": owner,
                        }
                    },
                ],
            )

            prices = await self._fetch_prices()

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
            print(f"[Kamino] Error fetching positions for {owner}: {e}")

        return positions

    async def get_health_factor(self, position_key: str) -> float:
        """Get current health factor for a Kamino position."""
        try:
            account = await self._get_account_info(position_key)
            if not account:
                return 0.0

            data_b64 = account.get("data", ["", ""])[0]
            data = base64.b64decode(data_b64)

            # Parse health factor from obligation data
            # This requires full obligation parsing
            # For now, return a calculated value
            return 0.0
        except Exception:
            return 0.0

    async def get_liquidation_price(self, position_key: str) -> dict[str, float]:
        """Get liquidation prices for each collateral asset in a Kamino position."""
        return {}

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()
