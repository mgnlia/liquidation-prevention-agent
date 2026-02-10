"""Claude AI Risk Analyzer — Intelligent DeFi position analysis"""
import json
import hashlib
import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import anthropic
import structlog

from protocols.base import PositionData, RiskLevel

logger = structlog.get_logger()


class RebalanceStrategy(str, Enum):
    COLLATERAL_TOP_UP = "collateral_top_up"
    DEBT_REPAYMENT = "debt_repayment"
    COLLATERAL_SWAP = "collateral_swap"
    POSITION_MIGRATION = "position_migration"
    EMERGENCY_UNWIND = "emergency_unwind"
    NO_ACTION = "no_action"


@dataclass
class AnalysisResult:
    """Result of AI risk analysis"""
    position_key: str
    risk_level: RiskLevel
    strategy: RebalanceStrategy
    reasoning: str
    confidence: float
    suggested_amount_usd: float
    urgency_score: float  # 0-1, 1 = immediate action needed
    reasoning_hash: str  # SHA-256 of reasoning for on-chain attestation
    timestamp: float

    @property
    def needs_action(self) -> bool:
        return self.strategy != RebalanceStrategy.NO_ACTION

    def to_dict(self) -> dict:
        return {
            "position_key": self.position_key,
            "risk_level": self.risk_level.value,
            "strategy": self.strategy.value,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "suggested_amount_usd": self.suggested_amount_usd,
            "urgency_score": self.urgency_score,
            "reasoning_hash": self.reasoning_hash,
            "timestamp": self.timestamp,
        }


SYSTEM_PROMPT = """You are SolShield, an AI-powered DeFi risk analyst specializing in Solana lending protocols.

Your role is to analyze lending positions and recommend optimal rebalancing strategies to prevent liquidations.

You analyze positions from these Solana protocols:
- Kamino Lending (KLend): Solana's leading lending protocol
- MarginFi: Decentralized lending on Solana  
- Solend: Original Solana lending protocol

For each position, you must:
1. Assess the current risk level based on health factor
2. Consider market conditions and volatility
3. Recommend a specific rebalancing strategy
4. Estimate the optimal rebalance amount
5. Assign an urgency score (0-1)

Rebalancing strategies available:
- collateral_top_up: Add more collateral via Jupiter swap
- debt_repayment: Partially repay debt to improve health factor
- collateral_swap: Swap volatile collateral for stable assets
- position_migration: Move position to a protocol with better rates/thresholds
- emergency_unwind: Full position closure (last resort)
- no_action: Position is healthy, no intervention needed

IMPORTANT: Be conservative. False positives (unnecessary rebalances) waste gas.
Only recommend action when health factor is genuinely at risk.

Respond in JSON format:
{
    "risk_assessment": "detailed risk analysis",
    "strategy": "one of the strategy enums",
    "reasoning": "step-by-step reasoning for the recommendation",
    "confidence": 0.0-1.0,
    "suggested_amount_usd": 0.0,
    "urgency_score": 0.0-1.0,
    "market_context": "relevant market observations"
}"""


class ClaudeAnalyzer:
    """Claude AI-powered risk analysis engine"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.analysis_count = 0

    async def analyze_position(
        self,
        position: PositionData,
        market_context: Optional[str] = None,
    ) -> AnalysisResult:
        """Analyze a DeFi position and recommend rebalancing strategy"""
        
        prompt = self._build_analysis_prompt(position, market_context)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0.1,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = response.content[0].text
            result = self._parse_response(response_text, position)
            self.analysis_count += 1

            logger.info(
                "ai_analysis_complete",
                position=position.obligation_key[:16],
                strategy=result.strategy.value,
                urgency=result.urgency_score,
                confidence=result.confidence,
            )

            return result

        except Exception as e:
            logger.error("ai_analysis_error", error=str(e))
            # Fallback to rule-based analysis
            return self._fallback_analysis(position)

    def _build_analysis_prompt(
        self, position: PositionData, market_context: Optional[str]
    ) -> str:
        """Build the analysis prompt for Claude"""
        prompt = f"""Analyze this Solana DeFi lending position:

## Position Details
{position.to_risk_summary()}

## Thresholds
- Warning: Health Factor < 1.5
- Critical: Health Factor < 1.2  
- Emergency: Health Factor < 1.05
- Liquidation: Health Factor < 1.0

## Collateral Breakdown
"""
        for c in position.collaterals:
            prompt += f"- {c.symbol}: ${c.value_usd:,.2f} (LTV: {c.ltv:.0%}, Liq Threshold: {c.liquidation_threshold:.0%})\n"

        prompt += "\n## Debt Breakdown\n"
        for d in position.debts:
            prompt += f"- {d.symbol}: ${d.value_usd:,.2f} (Borrow APY: {d.borrow_rate_apy:.2%})\n"

        if market_context:
            prompt += f"\n## Market Context\n{market_context}\n"

        prompt += """
## Task
Analyze this position and provide your recommendation in the specified JSON format.
Consider: current health factor, collateral composition, debt levels, and market conditions.
"""
        return prompt

    def _parse_response(self, response_text: str, position: PositionData) -> AnalysisResult:
        """Parse Claude's response into an AnalysisResult"""
        try:
            # Extract JSON from response
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                data = json.loads(response_text[json_start:json_end])
            else:
                raise ValueError("No JSON found in response")

            reasoning = data.get("reasoning", response_text)
            reasoning_hash = hashlib.sha256(reasoning.encode()).hexdigest()

            strategy_str = data.get("strategy", "no_action")
            try:
                strategy = RebalanceStrategy(strategy_str)
            except ValueError:
                strategy = RebalanceStrategy.NO_ACTION

            return AnalysisResult(
                position_key=position.obligation_key,
                risk_level=position.risk_level,
                strategy=strategy,
                reasoning=reasoning,
                confidence=float(data.get("confidence", 0.5)),
                suggested_amount_usd=float(data.get("suggested_amount_usd", 0)),
                urgency_score=float(data.get("urgency_score", 0)),
                reasoning_hash=reasoning_hash,
                timestamp=time.time(),
            )

        except (json.JSONDecodeError, KeyError) as e:
            logger.warning("ai_response_parse_error", error=str(e))
            return self._fallback_analysis(position)

    def _fallback_analysis(self, position: PositionData) -> AnalysisResult:
        """Rule-based fallback when AI analysis fails"""
        if position.health_factor < 1.05:
            strategy = RebalanceStrategy.EMERGENCY_UNWIND
            urgency = 1.0
            amount = position.total_debt_usd
            reasoning = f"EMERGENCY: Health factor {position.health_factor:.4f} below 1.05. Immediate unwind required."
        elif position.health_factor < 1.2:
            strategy = RebalanceStrategy.DEBT_REPAYMENT
            urgency = 0.8
            # Repay enough to bring health to 1.5
            target_debt = position.total_collateral_usd * 0.85 / 1.5
            amount = max(0, position.total_debt_usd - target_debt)
            reasoning = f"CRITICAL: Health factor {position.health_factor:.4f}. Repaying ${amount:,.2f} to restore health to 1.5."
        elif position.health_factor < 1.5:
            strategy = RebalanceStrategy.COLLATERAL_TOP_UP
            urgency = 0.4
            # Add collateral to bring health to 2.0
            needed_collateral = (position.total_debt_usd * 2.0) / 0.85
            amount = max(0, needed_collateral - position.total_collateral_usd)
            reasoning = f"WARNING: Health factor {position.health_factor:.4f}. Adding ${amount:,.2f} collateral recommended."
        else:
            strategy = RebalanceStrategy.NO_ACTION
            urgency = 0.0
            amount = 0
            reasoning = f"Position healthy. Health factor {position.health_factor:.4f} above warning threshold."

        reasoning_hash = hashlib.sha256(reasoning.encode()).hexdigest()

        return AnalysisResult(
            position_key=position.obligation_key,
            risk_level=position.risk_level,
            strategy=strategy,
            reasoning=reasoning,
            confidence=0.9,
            suggested_amount_usd=amount,
            urgency_score=urgency,
            reasoning_hash=reasoning_hash,
            timestamp=time.time(),
        )
