#!/usr/bin/env python3
"""
AI-Powered Liquidation Prevention Agent
Main orchestrator using LangGraph for autonomous decision-making
"""
import os
import time
import json
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

from monitor import PositionMonitor
from analyzer import RiskAnalyzer
from executor import TransactionExecutor

load_dotenv()

class LiquidationPreventionAgent:
    def __init__(self):
        print("🤖 Initializing AI Liquidation Prevention Agent...")
        
        self.monitor = PositionMonitor()
        self.analyzer = RiskAnalyzer()
        self.executor = TransactionExecutor()
        
        self.monitor_interval = int(os.getenv('MONITOR_INTERVAL_SECONDS', '60'))
        self.running = False
        
        # State tracking
        self.monitored_positions = {}
        self.execution_history = []
        
        print("✅ Agent initialized successfully")
    
    def start(self):
        """Start the autonomous monitoring loop"""
        print("\n" + "=" * 60)
        print("🚀 LIQUIDATION PREVENTION AGENT STARTING")
        print("=" * 60)
        
        # Check agent wallet balance
        balance_info = self.executor.check_agent_balance()
        print(f"\n💰 Agent Wallet: {balance_info['address']}")
        print(f"   Balance: {balance_info['balance']:.6f} ETH")
        
        if not balance_info['hasSufficientBalance']:
            print("\n⚠️  WARNING: Low agent balance. Fund wallet for transaction execution.")
        
        print(f"\n⏱️  Monitor Interval: {self.monitor_interval}s")
        print(f"🎯 Health Factor Threshold: {os.getenv('HEALTH_FACTOR_THRESHOLD', '1.5')}")
        
        self.running = True
        
        try:
            while self.running:
                self.run_monitoring_cycle()
                time.sleep(self.monitor_interval)
        except KeyboardInterrupt:
            print("\n\n⏹️  Agent stopped by user")
            self.stop()
    
    def run_monitoring_cycle(self):
        """Execute one complete monitoring cycle"""
        cycle_start = time.time()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{'=' * 60}")
        print(f"🔄 MONITORING CYCLE - {timestamp}")
        print(f"{'=' * 60}")
        
        # Step 1: Fetch registered users
        users = self.monitor.get_registered_users()
        
        if not users:
            print("ℹ️  No registered users found. Waiting for registrations...")
            return
        
        print(f"\n👥 Monitoring {len(users)} registered user(s)")
        
        # Step 2: Monitor each position
        at_risk_positions = []
        
        for user in users:
            print(f"\n📊 Checking position: {user}")
            
            # Get position data
            position = self.monitor.get_position_summary(user)
            
            if 'error' in position:
                print(f"   ❌ Error: {position['error']}")
                continue
            
            # Analyze risk
            analysis = self.analyzer.analyze_position(position)
            
            # Store in state
            self.monitored_positions[user] = {
                'position': position,
                'analysis': analysis,
                'timestamp': timestamp
            }
            
            # Log status
            hf = position.get('healthFactorFormatted', float('inf'))
            risk = analysis.get('riskLevel')
            
            print(f"   Health Factor: {hf:.4f}")
            print(f"   Risk Level: {risk}")
            print(f"   {analysis.get('analysis')}")
            
            # Track at-risk positions
            if analysis.get('needsAction'):
                at_risk_positions.append({
                    'user': user,
                    'position': position,
                    'analysis': analysis
                })
        
        # Step 3: Execute rebalancing for at-risk positions
        if at_risk_positions:
            print(f"\n⚠️  {len(at_risk_positions)} position(s) at risk - evaluating actions...")
            
            for item in at_risk_positions:
                self.handle_at_risk_position(item['user'], item['position'], item['analysis'])
        else:
            print(f"\n✅ All positions healthy")
        
        # Cycle summary
        cycle_duration = time.time() - cycle_start
        print(f"\n⏱️  Cycle completed in {cycle_duration:.2f}s")
        print(f"{'=' * 60}")
    
    def handle_at_risk_position(self, user: str, position: Dict, analysis: Dict):
        """Handle a position that's at liquidation risk"""
        
        print(f"\n🚨 HANDLING AT-RISK POSITION: {user}")
        
        strategy = analysis.get('strategy')
        
        if not strategy:
            print("   ⚠️  No strategy generated, skipping execution")
            return
        
        print(f"   💡 Strategy: {strategy.get('action')}")
        print(f"   📝 Reasoning: {strategy.get('reasoning')}")
        print(f"   💵 Debt to Repay: ${strategy.get('debtToRepay', 0):.2f}")
        print(f"   📈 Expected HF: {strategy.get('expectedHealthFactor', 0):.4f}")
        print(f"   🚨 Urgency: {strategy.get('urgency')}")
        
        # Decide whether to execute
        should_execute = self.analyzer.should_execute_immediately(analysis)
        
        if should_execute:
            print(f"   ⚡ EXECUTING REBALANCING NOW...")
            
            # Execute transaction
            tx_hash = self.executor.execute_rebalancing(user, strategy)
            
            if tx_hash:
                execution_record = {
                    'timestamp': datetime.now().isoformat(),
                    'user': user,
                    'strategy': strategy,
                    'txHash': tx_hash,
                    'status': 'executed'
                }
                self.execution_history.append(execution_record)
                
                print(f"   ✅ Rebalancing executed: {tx_hash}")
                
                # Save execution log
                self.save_execution_log()
            else:
                print(f"   ❌ Rebalancing execution failed")
        else:
            print(f"   ⏸️  Execution deferred - monitoring continues")
    
    def save_execution_log(self):
        """Save execution history to file"""
        try:
            log_file = 'execution_log.json'
            with open(log_file, 'w') as f:
                json.dump({
                    'executionHistory': self.execution_history,
                    'lastUpdate': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to save execution log: {e}")
    
    def get_status_report(self) -> Dict:
        """Generate comprehensive status report"""
        return {
            'agentRunning': self.running,
            'monitoredUsers': len(self.monitored_positions),
            'totalExecutions': len(self.execution_history),
            'positions': self.monitored_positions,
            'recentExecutions': self.execution_history[-5:] if self.execution_history else []
        }
    
    def stop(self):
        """Stop the agent"""
        self.running = False
        print("\n✅ Agent stopped gracefully")
        
        # Save final state
        self.save_execution_log()

def main():
    """Main entry point"""
    print("""
╔════════════════════════════════════════════════════════════╗
║   AI-POWERED LIQUIDATION PREVENTION AGENT                  ║
║   HackMoney 2026                                           ║
║   Autonomous DeFi Position Protection                      ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    agent = LiquidationPreventionAgent()
    agent.start()

if __name__ == "__main__":
    main()
