"""Tests for the Rebalance Executor"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from protocols.base import PositionData, Protocol, RiskLevel, CollateralPosition, DebtPosition
from analyzer import RebalanceStrategy, AnalysisResult
from executor import RebalanceExecutor, ExecutionResult, TOKENS
import time


def make_position(health_factor: float = 1.15) -> PositionData:
    risk = RiskLevel.CRITICAL if health_factor < 1.2 else RiskLevel.WARNING
    return PositionData(
        protocol=Protocol.KAMINO,
        owner="TestWallet111111111111111111111111111111111",
        obligation_key="TestObligation1111111111111111111111111",
        health_factor=health_factor,
        total_collateral_usd=5000,
        total_debt_usd=3800,
        net_value_usd=1200,
        risk_level=risk,
        collaterals=[
            CollateralPosition(
                mint="So11111111111111111111111111111111111111112",
                symbol="SOL",
                amount=50,
                value_usd=5000,
                ltv=0.76,
                liquidation_threshold=0.85,
            )
        ],
        debts=[
            DebtPosition(
                mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                symbol="USDC",
                amount=3800,
                value_usd=3800,
                borrow_rate_apy=0.058,
            )
        ],
    )


def make_analysis(
    strategy: RebalanceStrategy = RebalanceStrategy.DEBT_REPAYMENT,
    amount: float = 500.0,
    confidence: float = 0.9,
) -> AnalysisResult:
    return AnalysisResult(
        position_key="TestObligation1111111111111111111111111",
        risk_level=RiskLevel.CRITICAL,
        strategy=strategy,
        reasoning="Test reasoning for rebalance",
        confidence=confidence,
        suggested_amount_usd=amount,
        urgency_score=0.8,
        reasoning_hash="a" * 64,
        timestamp=time.time(),
    )


class TestRebalanceExecutor:
    """Test executor in dry-run mode"""

    def setup_method(self):
        self.executor = RebalanceExecutor(
            rpc_url="https://api.devnet.solana.com",
            wallet_api_key="test-key",
            wallet_id="test-wallet",
            dry_run=True,
        )

    @pytest.mark.asyncio
    async def test_no_action_returns_success(self):
        position = make_position()
        analysis = make_analysis(strategy=RebalanceStrategy.NO_ACTION, amount=0)
        result = await self.executor.execute_rebalance(position, analysis)
        assert result.success
        assert result.tx_signature is None
        assert result.amount_usd == 0

    @pytest.mark.asyncio
    async def test_dry_run_collateral_topup(self):
        position = make_position()
        analysis = make_analysis(strategy=RebalanceStrategy.COLLATERAL_TOP_UP, amount=500)
        result = await self.executor.execute_rebalance(position, analysis)
        assert result.success
        assert result.tx_signature is not None
        assert result.tx_signature.startswith("DRY_RUN_")
        assert result.amount_usd == 500

    @pytest.mark.asyncio
    async def test_dry_run_debt_repayment(self):
        position = make_position()
        analysis = make_analysis(strategy=RebalanceStrategy.DEBT_REPAYMENT, amount=300)
        result = await self.executor.execute_rebalance(position, analysis)
        assert result.success
        assert result.tx_signature.startswith("DRY_RUN_")

    @pytest.mark.asyncio
    async def test_dry_run_emergency_unwind(self):
        position = make_position(health_factor=1.02)
        analysis = make_analysis(strategy=RebalanceStrategy.EMERGENCY_UNWIND, amount=3800)
        result = await self.executor.execute_rebalance(position, analysis)
        assert result.success
        assert "EMERGENCY" in result.tx_signature

    @pytest.mark.asyncio
    async def test_dry_run_collateral_swap(self):
        position = make_position()
        analysis = make_analysis(strategy=RebalanceStrategy.COLLATERAL_SWAP, amount=1000)
        result = await self.executor.execute_rebalance(position, analysis)
        assert result.success
        assert result.tx_signature.startswith("DRY_RUN_")


class TestTokenConstants:
    """Test token address constants"""

    def test_sol_address(self):
        assert TOKENS["SOL"] == "So11111111111111111111111111111111111111112"

    def test_usdc_address(self):
        assert TOKENS["USDC"] == "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

    def test_all_tokens_are_base58(self):
        for name, addr in TOKENS.items():
            assert len(addr) >= 32, f"{name} address too short"


class TestExecutionResult:
    """Test ExecutionResult model"""

    def test_to_dict(self):
        result = ExecutionResult(
            success=True,
            tx_signature="test_sig",
            strategy=RebalanceStrategy.DEBT_REPAYMENT,
            amount_usd=500,
            timestamp=1234567890,
        )
        d = result.to_dict()
        assert d["success"] is True
        assert d["strategy"] == "debt_repayment"
        assert d["amount_usd"] == 500

    def test_failed_result(self):
        result = ExecutionResult(
            success=False,
            tx_signature=None,
            strategy=RebalanceStrategy.COLLATERAL_TOP_UP,
            amount_usd=0,
            error="Jupiter quote failed",
            timestamp=1234567890,
        )
        d = result.to_dict()
        assert d["success"] is False
        assert d["error"] == "Jupiter quote failed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
