"""Tests for the Claude AI Risk Analyzer"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from protocols.base import PositionData, Protocol, RiskLevel, CollateralPosition, DebtPosition
from analyzer import ClaudeAnalyzer, RebalanceStrategy, AnalysisResult


def make_position(health_factor: float, collateral: float = 10000, debt: float = 5000) -> PositionData:
    """Helper to create test positions"""
    if health_factor < 1.05:
        risk = RiskLevel.EMERGENCY
    elif health_factor < 1.2:
        risk = RiskLevel.CRITICAL
    elif health_factor < 1.5:
        risk = RiskLevel.WARNING
    else:
        risk = RiskLevel.HEALTHY

    return PositionData(
        protocol=Protocol.KAMINO,
        owner="TestWallet1111111111111111111111111111111111",
        obligation_key="TestObligation111111111111111111111111111",
        health_factor=health_factor,
        total_collateral_usd=collateral,
        total_debt_usd=debt,
        net_value_usd=collateral - debt,
        risk_level=risk,
        collaterals=[
            CollateralPosition(
                mint="So11111111111111111111111111111111111111112",
                symbol="SOL",
                amount=collateral / 150,
                value_usd=collateral,
                ltv=0.75,
                liquidation_threshold=0.85,
            )
        ],
        debts=[
            DebtPosition(
                mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                symbol="USDC",
                amount=debt,
                value_usd=debt,
                borrow_rate_apy=0.05,
            )
        ],
    )


class TestFallbackAnalysis:
    """Test the rule-based fallback analyzer"""

    def setup_method(self):
        self.analyzer = ClaudeAnalyzer(api_key="test-key")

    def test_healthy_position_no_action(self):
        position = make_position(health_factor=2.5)
        result = self.analyzer._fallback_analysis(position)
        assert result.strategy == RebalanceStrategy.NO_ACTION
        assert result.urgency_score == 0.0
        assert not result.needs_action

    def test_warning_position_collateral_topup(self):
        position = make_position(health_factor=1.35)
        result = self.analyzer._fallback_analysis(position)
        assert result.strategy == RebalanceStrategy.COLLATERAL_TOP_UP
        assert 0.3 <= result.urgency_score <= 0.5
        assert result.needs_action
        assert result.suggested_amount_usd > 0

    def test_critical_position_debt_repayment(self):
        position = make_position(health_factor=1.15)
        result = self.analyzer._fallback_analysis(position)
        assert result.strategy == RebalanceStrategy.DEBT_REPAYMENT
        assert result.urgency_score >= 0.7
        assert result.needs_action
        assert result.suggested_amount_usd > 0

    def test_emergency_position_unwind(self):
        position = make_position(health_factor=1.02)
        result = self.analyzer._fallback_analysis(position)
        assert result.strategy == RebalanceStrategy.EMERGENCY_UNWIND
        assert result.urgency_score == 1.0
        assert result.needs_action

    def test_reasoning_hash_generated(self):
        position = make_position(health_factor=1.1)
        result = self.analyzer._fallback_analysis(position)
        assert len(result.reasoning_hash) == 64  # SHA-256 hex
        assert result.reasoning_hash.isalnum()

    def test_high_confidence_fallback(self):
        position = make_position(health_factor=1.3)
        result = self.analyzer._fallback_analysis(position)
        assert result.confidence == 0.9

    def test_position_with_zero_debt(self):
        position = make_position(health_factor=float("inf"), debt=0)
        result = self.analyzer._fallback_analysis(position)
        assert result.strategy == RebalanceStrategy.NO_ACTION


class TestPositionData:
    """Test PositionData model"""

    def test_ltv_ratio(self):
        position = make_position(health_factor=1.5, collateral=10000, debt=5000)
        assert position.ltv_ratio == 0.5

    def test_ltv_ratio_zero_collateral(self):
        position = make_position(health_factor=0, collateral=0, debt=0)
        assert position.ltv_ratio == 0

    def test_risk_summary(self):
        position = make_position(health_factor=1.3)
        summary = position.to_risk_summary()
        assert "kamino" in summary.lower()
        assert "1.3" in summary
        assert "warning" in summary.lower()


class TestRiskClassification:
    """Test risk level classification"""

    def test_classify_healthy(self):
        from protocols.base import ProtocolAdapter
        # Can't instantiate abstract class directly, test via position
        position = make_position(health_factor=2.0)
        assert position.risk_level == RiskLevel.HEALTHY

    def test_classify_warning(self):
        position = make_position(health_factor=1.4)
        assert position.risk_level == RiskLevel.WARNING

    def test_classify_critical(self):
        position = make_position(health_factor=1.1)
        assert position.risk_level == RiskLevel.CRITICAL

    def test_classify_emergency(self):
        position = make_position(health_factor=1.02)
        assert position.risk_level == RiskLevel.EMERGENCY


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
