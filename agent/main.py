"""
AI-Powered Liquidation Prevention Agent
Main orchestration loop using LangGraph and Claude API
"""

import asyncio
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from web3 import Web3
from anthropic import Anthropic
import json
from datetime import datetime

from .monitor import PositionMonitor
from .analyzer import RiskAnalyzer
from .executor import RebalanceExecutor
from .config import Config

@dataclass
class UserPosition:
    """User DeFi position data"""
    address: str
    protocol: str
    health_factor: float
    total_collateral: float
    total_debt: float
    at_risk: bool
    timestamp: datetime

class LiquidationPreventionAgent:
    """
    Main AI agent that monitors DeFi positions and prevents liquidations
    using Claude API for intelligent decision making
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.web3 = Web3(Web3.HTTPProvider(config.rpc_url))
        self.anthropic = Anthropic(api_key=config.anthropic_api_key)
        
        # Initialize components
        self.monitor = PositionMonitor(self.web3, config)
        self.analyzer = RiskAnalyzer(config)
        self.executor = RebalanceExecutor(self.web3, config)
        
        # State
        self.monitored_users: List[str] = []
        self.last_check: Dict[str, datetime] = {}
        
    async def start(self):
        """Start the agent monitoring loop"""
        print(f"🤖 Starting Liquidation Prevention Agent on {self.config.network}")
        print(f"📊 Monitoring interval: {self.config.check_interval}s")
        
        while True:
            try:
                await self.monitoring_cycle()
                await asyncio.sleep(self.config.check_interval)
            except Exception as e:
                print(f"❌ Error in monitoring cycle: {e}")
                await asyncio.sleep(60)  # Wait before retry
    
    async def monitoring_cycle(self):
        """Execute one monitoring cycle"""
        print(f"\n🔍 Monitoring cycle at {datetime.now().isoformat()}")
        
        # Get all monitored users
        users = await self.monitor.get_monitored_users()
        
        for user_address in users:
            try:
                await self.check_user_position(user_address)
            except Exception as e:
                print(f"❌ Error checking user {user_address}: {e}")
    
    async def check_user_position(self, user_address: str):
        """Check a single user's position across all protocols"""
        print(f"\n👤 Checking user: {user_address}")
        
        # Get position data from all protocols
        positions = await self.monitor.get_user_positions(user_address)
        
        for position in positions:
            if position.at_risk:
                print(f"⚠️  RISK DETECTED: {position.protocol} - Health Factor: {position.health_factor:.2f}")
                
                # Use Claude to analyze and recommend action
                recommendation = await self.get_claude_recommendation(position)
                
                if recommendation["action"] == "rebalance":
                    print(f"🔄 Claude recommends rebalancing")
                    await self.execute_rebalance(position, recommendation)
                elif recommendation["action"] == "monitor":
                    print(f"👀 Claude recommends continued monitoring")
                else:
                    print(f"✅ No action needed")
    
    async def get_claude_recommendation(self, position: UserPosition) -> Dict:
        """
        Use Claude API to analyze position and recommend action
        """
        prompt = f"""You are an expert DeFi risk analyst. Analyze this position and recommend an action.

Position Details:
- Protocol: {position.protocol}
- Health Factor: {position.health_factor}
- Total Collateral: ${position.total_collateral:,.2f}
- Total Debt: ${position.total_debt:,.2f}
- Current Status: {"AT RISK" if position.at_risk else "HEALTHY"}

Context:
- Health factor below 1.2 is dangerous (liquidation at 1.0)
- Rebalancing costs gas + flash loan fees (~0.09%)
- User preference: maintain position, avoid liquidation

Analyze the risk level and recommend ONE of:
1. "rebalance" - Execute immediate rebalancing to increase health factor
2. "monitor" - Continue monitoring, not urgent yet
3. "none" - Position is healthy

Respond in JSON format:
{{
  "action": "rebalance|monitor|none",
  "reasoning": "brief explanation",
  "urgency": "low|medium|high|critical",
  "recommended_amount": <amount to rebalance in USD>
}}
"""

        try:
            message = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            response_text = message.content[0].text
            
            # Parse JSON response
            recommendation = json.loads(response_text)
            
            # Log Claude's reasoning
            print(f"\n🧠 Claude Analysis:")
            print(f"   Action: {recommendation['action']}")
            print(f"   Urgency: {recommendation['urgency']}")
            print(f"   Reasoning: {recommendation['reasoning']}")
            
            # Log to attribution file
            self._log_ai_decision(position, recommendation)
            
            return recommendation
            
        except Exception as e:
            print(f"❌ Error getting Claude recommendation: {e}")
            # Fallback to rule-based decision
            return self._fallback_decision(position)
    
    def _fallback_decision(self, position: UserPosition) -> Dict:
        """Fallback rule-based decision if Claude API fails"""
        if position.health_factor < 1.15:
            return {
                "action": "rebalance",
                "reasoning": "Health factor critically low (fallback rule)",
                "urgency": "critical",
                "recommended_amount": position.total_debt * 0.2
            }
        elif position.health_factor < 1.3:
            return {
                "action": "monitor",
                "reasoning": "Health factor low but not critical (fallback rule)",
                "urgency": "medium",
                "recommended_amount": 0
            }
        else:
            return {
                "action": "none",
                "reasoning": "Health factor acceptable (fallback rule)",
                "urgency": "low",
                "recommended_amount": 0
            }
    
    async def execute_rebalance(self, position: UserPosition, recommendation: Dict):
        """Execute the rebalancing transaction"""
        try:
            print(f"\n🔄 Executing rebalance for {position.address}")
            
            result = await self.executor.execute_rebalance(
                user_address=position.address,
                protocol=position.protocol,
                amount=recommendation["recommended_amount"]
            )
            
            if result["success"]:
                print(f"✅ Rebalance successful!")
                print(f"   Tx: {result['tx_hash']}")
                print(f"   New Health Factor: {result['new_health_factor']:.2f}")
            else:
                print(f"❌ Rebalance failed: {result['error']}")
                
        except Exception as e:
            print(f"❌ Error executing rebalance: {e}")
    
    def _log_ai_decision(self, position: UserPosition, recommendation: Dict):
        """Log AI decision to attribution file for hackathon compliance"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": "claude-3-5-sonnet-20241022",
            "position": {
                "user": position.address,
                "protocol": position.protocol,
                "health_factor": position.health_factor,
            },
            "recommendation": recommendation
        }
        
        log_file = "docs/ai-attribution.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

async def main():
    """Main entry point"""
    config = Config.from_env()
    agent = LiquidationPreventionAgent(config)
    await agent.start()

if __name__ == "__main__":
    asyncio.run(main())
