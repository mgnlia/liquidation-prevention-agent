"""
Risk Analyzer - Claude-powered risk scoring and rebalancing strategy generation
"""
import os
import json
from typing import Dict, Optional
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class RiskAnalyzer:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-3-5-sonnet-20241022"
        self.health_factor_threshold = float(os.getenv('HEALTH_FACTOR_THRESHOLD', '1.5'))
    
    def analyze_position(self, position_data: Dict) -> Dict:
        """Analyze position risk using Claude"""
        
        # Quick risk assessment without API call for efficiency
        health_factor = position_data.get('healthFactorFormatted', float('inf'))
        
        risk_level = self._calculate_risk_level(health_factor)
        
        # If high risk, use Claude for strategy generation
        if risk_level in ['HIGH', 'CRITICAL']:
            strategy = self._generate_rebalancing_strategy(position_data)
        else:
            strategy = None
        
        return {
            "riskLevel": risk_level,
            "healthFactor": health_factor,
            "needsAction": risk_level in ['HIGH', 'CRITICAL'],
            "strategy": strategy,
            "timestamp": position_data.get('timestamp'),
            "analysis": self._get_risk_description(risk_level, health_factor)
        }
    
    def _calculate_risk_level(self, health_factor: float) -> str:
        """Calculate risk level based on health factor"""
        if health_factor == float('inf'):
            return "SAFE"
        elif health_factor >= 2.0:
            return "LOW"
        elif health_factor >= 1.5:
            return "MEDIUM"
        elif health_factor >= 1.2:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def _get_risk_description(self, risk_level: str, health_factor: float) -> str:
        """Get human-readable risk description"""
        descriptions = {
            "SAFE": "No debt position detected. Position is safe.",
            "LOW": f"Health factor {health_factor:.4f} is healthy. No immediate action needed.",
            "MEDIUM": f"Health factor {health_factor:.4f} is approaching threshold. Monitor closely.",
            "HIGH": f"⚠️  Health factor {health_factor:.4f} is below threshold. Rebalancing recommended.",
            "CRITICAL": f"🚨 CRITICAL: Health factor {health_factor:.4f}. Immediate action required!"
        }
        return descriptions.get(risk_level, "Unknown risk level")
    
    def _generate_rebalancing_strategy(self, position_data: Dict) -> Optional[Dict]:
        """Use Claude to generate optimal rebalancing strategy"""
        
        prompt = self._build_strategy_prompt(position_data)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse Claude's response
            strategy_text = response.content[0].text
            strategy = self._parse_strategy_response(strategy_text, position_data)
            
            return strategy
            
        except Exception as e:
            print(f"❌ Error generating strategy with Claude: {e}")
            # Fallback to simple strategy
            return self._generate_fallback_strategy(position_data)
    
    def _build_strategy_prompt(self, position_data: Dict) -> str:
        """Build prompt for Claude to generate rebalancing strategy"""
        
        return f"""You are a DeFi risk management AI analyzing a liquidation risk scenario.

POSITION DATA:
- Health Factor: {position_data.get('healthFactorFormatted', 0):.4f}
- Total Collateral: ${position_data.get('collateralUSD', 0):.2f}
- Total Debt: ${position_data.get('debtUSD', 0):.2f}
- Utilization Rate: {position_data.get('utilizationRate', 0):.2f}%
- Liquidation Threshold: {position_data.get('currentLiquidationThreshold', 0) / 100:.2f}%

CONTEXT:
- Health factor below 1.5 indicates liquidation risk
- Health factor below 1.0 means position can be liquidated
- Current health factor is {position_data.get('healthFactorFormatted', 0):.4f}

TASK:
Generate an optimal rebalancing strategy to bring health factor above 2.0 (safe zone).

Respond in JSON format with:
{{
  "action": "REPAY_DEBT" or "ADD_COLLATERAL" or "SWAP_AND_REPAY",
  "reasoning": "Brief explanation of why this strategy is optimal",
  "debtToRepay": <amount in USD>,
  "collateralToAdd": <amount in USD>,
  "expectedHealthFactor": <estimated new health factor>,
  "urgency": "LOW" or "MEDIUM" or "HIGH" or "CRITICAL"
}}

Provide ONLY the JSON response, no additional text."""

    def _parse_strategy_response(self, response_text: str, position_data: Dict) -> Dict:
        """Parse Claude's JSON response"""
        try:
            # Extract JSON from response
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.split('```json')[1].split('```')[0]
            elif response_text.startswith('```'):
                response_text = response_text.split('```')[1].split('```')[0]
            
            strategy = json.loads(response_text)
            
            # Add execution parameters
            strategy['executable'] = True
            strategy['estimatedGas'] = 300000  # Estimated gas for flash loan rebalancing
            
            return strategy
            
        except json.JSONDecodeError:
            print(f"⚠️  Failed to parse Claude response as JSON: {response_text}")
            return self._generate_fallback_strategy(position_data)
    
    def _generate_fallback_strategy(self, position_data: Dict) -> Dict:
        """Generate simple fallback strategy without Claude"""
        
        health_factor = position_data.get('healthFactorFormatted', 0)
        debt_usd = position_data.get('debtUSD', 0)
        
        # Simple strategy: repay enough debt to reach HF of 2.0
        # HF = collateral / debt, so to double HF, repay half the debt
        debt_to_repay = debt_usd * 0.3  # Repay 30% of debt as conservative approach
        
        return {
            "action": "REPAY_DEBT",
            "reasoning": f"Fallback strategy: Repay 30% of debt to improve health factor from {health_factor:.4f} to ~{health_factor * 1.4:.4f}",
            "debtToRepay": debt_to_repay,
            "collateralToAdd": 0,
            "expectedHealthFactor": health_factor * 1.4,
            "urgency": "HIGH" if health_factor < 1.2 else "MEDIUM",
            "executable": True,
            "estimatedGas": 300000
        }
    
    def should_execute_immediately(self, analysis: Dict) -> bool:
        """Determine if strategy should be executed immediately"""
        
        if not analysis.get('needsAction'):
            return False
        
        risk_level = analysis.get('riskLevel')
        health_factor = analysis.get('healthFactor', float('inf'))
        
        # Execute immediately if critical or health factor very low
        if risk_level == 'CRITICAL' or health_factor < 1.2:
            return True
        
        # For HIGH risk, execute if strategy is available
        if risk_level == 'HIGH' and analysis.get('strategy'):
            return True
        
        return False

if __name__ == "__main__":
    print("🧠 Risk Analyzer - Testing")
    print("=" * 60)
    
    analyzer = RiskAnalyzer()
    
    # Test with sample position data
    test_position = {
        "healthFactorFormatted": 1.35,
        "collateralUSD": 10000,
        "debtUSD": 6500,
        "utilizationRate": 65,
        "currentLiquidationThreshold": 8000,
        "timestamp": 1234567890
    }
    
    print("\n📊 Analyzing test position...")
    print(f"   Health Factor: {test_position['healthFactorFormatted']}")
    print(f"   Collateral: ${test_position['collateralUSD']}")
    print(f"   Debt: ${test_position['debtUSD']}")
    
    analysis = analyzer.analyze_position(test_position)
    
    print(f"\n✅ Analysis Complete:")
    print(f"   Risk Level: {analysis['riskLevel']}")
    print(f"   Needs Action: {analysis['needsAction']}")
    print(f"   Description: {analysis['analysis']}")
    
    if analysis.get('strategy'):
        print(f"\n💡 Recommended Strategy:")
        strategy = analysis['strategy']
        print(f"   Action: {strategy.get('action')}")
        print(f"   Reasoning: {strategy.get('reasoning')}")
        print(f"   Debt to Repay: ${strategy.get('debtToRepay', 0):.2f}")
        print(f"   Expected HF: {strategy.get('expectedHealthFactor', 0):.4f}")
        print(f"   Urgency: {strategy.get('urgency')}")
    
    print(f"\n🚀 Execute Immediately: {analyzer.should_execute_immediately(analysis)}")
    print("\n" + "=" * 60)
