"""
Position monitoring module
Tracks user positions across Aave and Compound
"""

from web3 import Web3
from typing import List
from datetime import datetime
from .config import Config
import json

class PositionMonitor:
    """Monitors DeFi positions across protocols"""
    
    def __init__(self, web3: Web3, config: Config):
        self.web3 = web3
        self.config = config
        
        # Load contract ABIs
        self.liquidation_prevention = self._load_contract(
            config.liquidation_prevention_address,
            "LiquidationPrevention"
        )
    
    def _load_contract(self, address: str, name: str):
        """Load contract instance"""
        # Load ABI from artifacts
        try:
            with open(f"../artifacts/contracts/{name}.sol/{name}.json") as f:
                artifact = json.load(f)
                abi = artifact["abi"]
            return self.web3.eth.contract(address=address, abi=abi)
        except Exception as e:
            print(f"Warning: Could not load {name} contract: {e}")
            return None
    
    async def get_monitored_users(self) -> List[str]:
        """Get list of users who have enabled auto-rebalance"""
        # In production, would query events or maintain a database
        # For MVP, return test addresses
        return [
            "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",  # Example address
        ]
    
    async def get_user_positions(self, user_address: str) -> List:
        """Get user's positions across all protocols"""
        from .main import UserPosition
        
        positions = []
        
        try:
            # Get health factors from contract
            if self.liquidation_prevention:
                result = self.liquidation_prevention.functions.getUserHealthFactors(
                    user_address
                ).call()
                
                aave_health = result[0] / 1e18 if result[0] > 0 else 0
                compound_health = result[1] / 1e18 if result[1] > 0 else 0
                
                # Check Aave position
                if aave_health > 0:
                    positions.append(UserPosition(
                        address=user_address,
                        protocol="aave",
                        health_factor=aave_health,
                        total_collateral=10000,  # Would query actual values
                        total_debt=5000,
                        at_risk=aave_health < self.config.min_health_factor,
                        timestamp=datetime.now()
                    ))
                
                # Check Compound position
                if compound_health > 0:
                    positions.append(UserPosition(
                        address=user_address,
                        protocol="compound",
                        health_factor=compound_health,
                        total_collateral=8000,
                        total_debt=4000,
                        at_risk=compound_health < self.config.min_health_factor,
                        timestamp=datetime.now()
                    ))
        
        except Exception as e:
            print(f"Error fetching positions: {e}")
        
        return positions
    
    async def get_position_details(self, user_address: str, protocol: str) -> dict:
        """Get detailed position information for a specific protocol"""
        # Would implement protocol-specific queries here
        return {
            "collateral_assets": [],
            "debt_assets": [],
            "health_factor": 0,
        }
