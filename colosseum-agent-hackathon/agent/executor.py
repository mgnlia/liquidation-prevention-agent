"""Transaction Executor — Jupiter swaps and protocol interactions"""
import hashlib
import json
import time
from dataclasses import dataclass
from typing import Optional

import httpx
import structlog

from analyzer import RebalanceStrategy, AnalysisResult
from protocols.base import PositionData

logger = structlog.get_logger()

JUPITER_QUOTE_API = "https://quote-api.jup.ag/v6/quote"
JUPITER_SWAP_API = "https://quote-api.jup.ag/v6/swap"

# Common Solana token mints
TOKENS = {
    "SOL": "So11111111111111111111111111111111111111112",
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
    "mSOL": "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So",
    "stSOL": "7dHbWXmci3dT8UFYWYZweBLXgycu7Y3iL6trKn1Y7ARj",
    "jitoSOL": "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn",
}


@dataclass
class ExecutionResult:
    """Result of a rebalance execution"""
    success: bool
    tx_signature: Optional[str]
    strategy: RebalanceStrategy
    amount_usd: float
    error: Optional[str] = None
    gas_cost_sol: float = 0.0
    timestamp: float = 0.0

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "tx_signature": self.tx_signature,
            "strategy": self.strategy.value,
            "amount_usd": self.amount_usd,
            "error": self.error,
            "gas_cost_sol": self.gas_cost_sol,
            "timestamp": self.timestamp,
        }


class RebalanceExecutor:
    """Executes rebalancing transactions on Solana"""

    def __init__(
        self,
        rpc_url: str,
        wallet_api_key: str,
        wallet_id: str,
        dry_run: bool = True,
    ):
        self.rpc_url = rpc_url
        self.wallet_api_key = wallet_api_key
        self.wallet_id = wallet_id
        self.dry_run = dry_run
        self.client = httpx.AsyncClient(timeout=60)
        self.execution_count = 0

    async def execute_rebalance(
        self,
        position: PositionData,
        analysis: AnalysisResult,
    ) -> ExecutionResult:
        """Execute a rebalancing strategy based on AI analysis"""

        logger.info(
            "executing_rebalance",
            strategy=analysis.strategy.value,
            amount=analysis.suggested_amount_usd,
            position=position.obligation_key[:16],
            dry_run=self.dry_run,
        )

        try:
            if analysis.strategy == RebalanceStrategy.NO_ACTION:
                return ExecutionResult(
                    success=True,
                    tx_signature=None,
                    strategy=analysis.strategy,
                    amount_usd=0,
                    timestamp=time.time(),
                )

            if analysis.strategy == RebalanceStrategy.COLLATERAL_TOP_UP:
                return await self._execute_collateral_topup(position, analysis)
            elif analysis.strategy == RebalanceStrategy.DEBT_REPAYMENT:
                return await self._execute_debt_repayment(position, analysis)
            elif analysis.strategy == RebalanceStrategy.COLLATERAL_SWAP:
                return await self._execute_collateral_swap(position, analysis)
            elif analysis.strategy == RebalanceStrategy.EMERGENCY_UNWIND:
                return await self._execute_emergency_unwind(position, analysis)
            elif analysis.strategy == RebalanceStrategy.POSITION_MIGRATION:
                return await self._execute_position_migration(position, analysis)
            else:
                return ExecutionResult(
                    success=False,
                    tx_signature=None,
                    strategy=analysis.strategy,
                    amount_usd=0,
                    error=f"Unknown strategy: {analysis.strategy}",
                    timestamp=time.time(),
                )

        except Exception as e:
            logger.error("execution_error", error=str(e))
            return ExecutionResult(
                success=False,
                tx_signature=None,
                strategy=analysis.strategy,
                amount_usd=analysis.suggested_amount_usd,
                error=str(e),
                timestamp=time.time(),
            )

    async def _execute_collateral_topup(
        self, position: PositionData, analysis: AnalysisResult
    ) -> ExecutionResult:
        """Add collateral by swapping available assets via Jupiter"""

        # Determine swap: convert USDC to the primary collateral asset
        input_mint = TOKENS["USDC"]
        output_mint = TOKENS["SOL"]  # Default to SOL as collateral

        if position.collaterals:
            # Use the largest collateral's token type
            primary = max(position.collaterals, key=lambda c: c.value_usd)
            if "SOL" in primary.symbol.upper():
                output_mint = TOKENS["SOL"]
            elif "MSOL" in primary.symbol.upper():
                output_mint = TOKENS["mSOL"]

        # Amount in USDC (6 decimals)
        amount = int(analysis.suggested_amount_usd * 1e6)

        if self.dry_run:
            logger.info("dry_run_collateral_topup", amount_usd=analysis.suggested_amount_usd)
            return ExecutionResult(
                success=True,
                tx_signature="DRY_RUN_" + hashlib.sha256(str(time.time()).encode()).hexdigest()[:32],
                strategy=analysis.strategy,
                amount_usd=analysis.suggested_amount_usd,
                timestamp=time.time(),
            )

        # Get Jupiter quote
        quote = await self._get_jupiter_quote(input_mint, output_mint, amount)
        if not quote:
            return ExecutionResult(
                success=False, tx_signature=None,
                strategy=analysis.strategy, amount_usd=analysis.suggested_amount_usd,
                error="Failed to get Jupiter quote", timestamp=time.time(),
            )

        # Execute swap via AgentWallet
        tx_sig = await self._execute_jupiter_swap(quote)

        self.execution_count += 1
        return ExecutionResult(
            success=tx_sig is not None,
            tx_signature=tx_sig,
            strategy=analysis.strategy,
            amount_usd=analysis.suggested_amount_usd,
            timestamp=time.time(),
        )

    async def _execute_debt_repayment(
        self, position: PositionData, analysis: AnalysisResult
    ) -> ExecutionResult:
        """Repay debt on the lending protocol"""

        if self.dry_run:
            logger.info("dry_run_debt_repayment", amount_usd=analysis.suggested_amount_usd)
            return ExecutionResult(
                success=True,
                tx_signature="DRY_RUN_" + hashlib.sha256(str(time.time()).encode()).hexdigest()[:32],
                strategy=analysis.strategy,
                amount_usd=analysis.suggested_amount_usd,
                timestamp=time.time(),
            )

        # Build repayment transaction based on protocol
        # This would interact with Kamino/MarginFi/Solend repay instructions
        logger.info(
            "debt_repayment",
            protocol=position.protocol.value,
            amount=analysis.suggested_amount_usd,
        )

        # Placeholder for actual protocol interaction
        return ExecutionResult(
            success=True,
            tx_signature=None,
            strategy=analysis.strategy,
            amount_usd=analysis.suggested_amount_usd,
            error="Protocol repay instruction not yet implemented",
            timestamp=time.time(),
        )

    async def _execute_collateral_swap(
        self, position: PositionData, analysis: AnalysisResult
    ) -> ExecutionResult:
        """Swap volatile collateral for stable collateral"""

        if self.dry_run:
            logger.info("dry_run_collateral_swap", amount_usd=analysis.suggested_amount_usd)
            return ExecutionResult(
                success=True,
                tx_signature="DRY_RUN_" + hashlib.sha256(str(time.time()).encode()).hexdigest()[:32],
                strategy=analysis.strategy,
                amount_usd=analysis.suggested_amount_usd,
                timestamp=time.time(),
            )

        # Swap SOL collateral to USDC via Jupiter
        amount = int(analysis.suggested_amount_usd * 1e9 / 100)  # Approximate SOL amount
        quote = await self._get_jupiter_quote(TOKENS["SOL"], TOKENS["USDC"], amount)

        if not quote:
            return ExecutionResult(
                success=False, tx_signature=None,
                strategy=analysis.strategy, amount_usd=analysis.suggested_amount_usd,
                error="Failed to get Jupiter quote for collateral swap",
                timestamp=time.time(),
            )

        tx_sig = await self._execute_jupiter_swap(quote)
        self.execution_count += 1

        return ExecutionResult(
            success=tx_sig is not None,
            tx_signature=tx_sig,
            strategy=analysis.strategy,
            amount_usd=analysis.suggested_amount_usd,
            timestamp=time.time(),
        )

    async def _execute_emergency_unwind(
        self, position: PositionData, analysis: AnalysisResult
    ) -> ExecutionResult:
        """Emergency full position closure"""

        logger.warning(
            "emergency_unwind",
            position=position.obligation_key[:16],
            health_factor=position.health_factor,
        )

        if self.dry_run:
            return ExecutionResult(
                success=True,
                tx_signature="DRY_RUN_EMERGENCY_" + hashlib.sha256(str(time.time()).encode()).hexdigest()[:32],
                strategy=analysis.strategy,
                amount_usd=position.total_debt_usd,
                timestamp=time.time(),
            )

        # Full unwind: repay all debt, withdraw all collateral
        return ExecutionResult(
            success=True,
            tx_signature=None,
            strategy=analysis.strategy,
            amount_usd=position.total_debt_usd,
            error="Emergency unwind requires manual confirmation",
            timestamp=time.time(),
        )

    async def _execute_position_migration(
        self, position: PositionData, analysis: AnalysisResult
    ) -> ExecutionResult:
        """Migrate position to a different protocol"""

        if self.dry_run:
            return ExecutionResult(
                success=True,
                tx_signature="DRY_RUN_MIGRATE_" + hashlib.sha256(str(time.time()).encode()).hexdigest()[:32],
                strategy=analysis.strategy,
                amount_usd=analysis.suggested_amount_usd,
                timestamp=time.time(),
            )

        return ExecutionResult(
            success=False,
            tx_signature=None,
            strategy=analysis.strategy,
            amount_usd=analysis.suggested_amount_usd,
            error="Position migration requires multi-step atomic execution",
            timestamp=time.time(),
        )

    async def _get_jupiter_quote(
        self, input_mint: str, output_mint: str, amount: int
    ) -> Optional[dict]:
        """Get a swap quote from Jupiter aggregator"""
        try:
            params = {
                "inputMint": input_mint,
                "outputMint": output_mint,
                "amount": str(amount),
                "slippageBps": "50",  # 0.5% slippage
            }

            response = await self.client.get(JUPITER_QUOTE_API, params=params)
            if response.status_code == 200:
                return response.json()

            logger.warning("jupiter_quote_failed", status=response.status_code)
            return None

        except Exception as e:
            logger.error("jupiter_quote_error", error=str(e))
            return None

    async def _execute_jupiter_swap(self, quote: dict) -> Optional[str]:
        """Execute a Jupiter swap using AgentWallet for signing"""
        try:
            # Get swap transaction from Jupiter
            swap_payload = {
                "quoteResponse": quote,
                "userPublicKey": self.wallet_id,
                "wrapAndUnwrapSol": True,
                "computeUnitPriceMicroLamports": 50000,
            }

            response = await self.client.post(JUPITER_SWAP_API, json=swap_payload)
            if response.status_code != 200:
                logger.error("jupiter_swap_failed", status=response.status_code)
                return None

            swap_data = response.json()
            swap_tx = swap_data.get("swapTransaction")

            if not swap_tx:
                return None

            # Sign and send via AgentWallet
            tx_sig = await self._sign_and_send(swap_tx)
            return tx_sig

        except Exception as e:
            logger.error("jupiter_swap_error", error=str(e))
            return None

    async def _sign_and_send(self, transaction_base64: str) -> Optional[str]:
        """Sign and send a transaction via AgentWallet API"""
        try:
            wallet_url = f"https://agentwallet.mcpay.tech/api/wallets/{self.wallet_id}/sign-and-send"
            headers = {"Authorization": f"Bearer {self.wallet_api_key}"}
            payload = {"transaction": transaction_base64}

            response = await self.client.post(wallet_url, json=payload, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result.get("signature")

            logger.error("wallet_sign_failed", status=response.status_code)
            return None

        except Exception as e:
            logger.error("wallet_sign_error", error=str(e))
            return None

    async def close(self):
        await self.client.aclose()
