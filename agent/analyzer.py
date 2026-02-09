"""
Risk analysis module
Analyzes positions and determines risk levels
"""

from typing import Dict
from .config import Config

class RiskAnalyzer:
    """Analyzes DeFi position risk"""
    
    def __init__(self, config: Config):
        self.config = config
    
    def analyze_position(self, health_factor: float, total_collateral: float, 
                        total_debt: float) -> Dict:
        """Analyze position and return risk assessment"""
        
        # Determine risk level
        if health_factor < self.config.critical_threshold:
            risk_level = "critical"
            urgency = "immediate"
        elif health_factor < self.config.warning_threshold:
            risk_level = "high"
            urgency = "high"
        elif health_factor < self.config.safe_threshold:
            risk_level = "medium"
            urgency = "medium"
        else:
            risk_level = "low"
            urgency = "low"
        
        # Calculate recommended rebalance amount
        if health_factor < self.config.min_health_factor:
            # Calculate amount needed to reach target health factor
            # Simplified calculation: increase collateral or reduce debt
            ltv_current = total_debt / total_collateral if total_collateral > 0 else 0
            ltv_target = ltv_current * (health_factor / self.config.target_health_factor)
            
            # Amount to rebalance (reduce debt)
            recommended_amount = total_debt * 0.2  # Reduce debt by 20%
        else:
            recommended_amount = 0
        
        return {
            "risk_level": risk_level,
            "urgency": urgency,
            "recommended_amount": recommended_amount,
            "health_factor": health_factor,
            "needs_action": health_factor < self.config.min_health_factor
        }
    
    def calculate_target_rebalance(self, current_health: float, 
                                   target_health: float,
                                   total_debt: float) -> float:
        """Calculate exact amount to rebalance to reach target health factor"""
        
        if current_health >= target_health:
            return 0
        
        # Simplified calculation
        # In production, would use actual collateral/debt ratios and liquidation thresholds
        ratio = target_health / current_health
        amount = total_debt * (1 - (1 / ratio))
        
        return max(0, amount)
