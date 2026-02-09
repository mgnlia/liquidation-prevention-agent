"""
Position monitoring module
Tracks user positions across Aave and Compound
"""

from typing import List, Dict
from web3 import Web3
from datetime import datetime
import json

from .config import Config

class UserPosition:
    """Represents a user's DeFi position"""
    
    def __init__(self, address: str, protocol: str, health_factor: float, 
                 total_collateral: float, total_debt: float, at_risk: bool):
        self.address = address
        self.protocol = protocol
        self.health_factor = health_factor
        self.total_collateral = total_collateral
        self.total_debt = total_debt
        self.at_risk = at_risk
        self.timestamp = datetime.now()

class PositionMonitor:
    """Monitors user positions across protocols"""
    
    def __init__(self, web3: Web3, config: Config):
        self.web3 = web3
        self.config = config
        
        # Load contract ABIs
        self.liquidation_prevention_abi = self._load_abi("LiquidationPrevention")
        self.aave_adapter_abi = self._load_abi("AaveAdapter")
        
        # Initialize contracts
        if config.liquidation_prevention_address:
            self.liquidation_prevention = web3.eth.contract(
                address=Web3.to_checksum_address(config.liquidation_prevention_address),
                abi=self.liquidation_prevention_abi
            )
    
    def _load_abi(self, contract_name: str) -> List:
        """Load contract ABI from artifacts"""
        try:
            with open(f"../artifacts/contracts/{contract_name}.sol/{contract_name}.json") as f:
                artifact = json.load(f)
                return artifact["abi"]
        except FileNotFoundError:
            # Fallback: return minimal ABI for testing
            return []
    
    async def get_monitored_users(self) -> List[str]:
        """Get list of users with auto-rebalance enabled"""
        # In production, this would query events or a subgraph
        # For now, return test users from environment
        users = []
        
        # Check for test users in environment
        test_user = self.config.__dict__.get("test_user_address")
        if test_user:
            users.append(test_user)
        
        return users
    
    async def get_user_positions(self, user_address: str) -> List[UserPosition]:
        """Get all positions for a user across protocols"""
        positions = []
        
        try:
            # Get user config
            user_config = self.liquidation_prevention.functions.userConfigs(
                Web3.to_checksum_address(user_address)
            ).call()
            
            auto_rebalance_enabled = user_config[0]
            min_health_factor = user_config[1] / 1e18  # Convert from wei
            
            if not auto_rebalance_enabled:
                return positions
            
            # Get health factors
            health_factors = self.liquidation_prevention.functions.getUserHealthFactors(
                Web3.to_checksum_address(user_address)
            ).call()
            
            aave_health = health_factors[0] / 1e18 if health_factors[0] > 0 else 0
            compound_health = health_factors[1] / 1e18 if health_factors[1] > 0 else 0
            
            # Check Aave position
            if aave_health > 0:
                at_risk = aave_health < min_health_factor
                position = UserPosition(
                    address=user_address,
                    protocol="aave",
                    health_factor=aave_health,
                    total_collateral=0,  # Would fetch from Aave in production
                    total_debt=0,
                    at_risk=at_risk
                )
                positions.append(position)
            
            # Check Compound position
            if compound_health > 0:
                at_risk = compound_health < min_health_factor
                position = UserPosition(
                    address=user_address,
                    protocol="compound",
                    health_factor=compound_health,
                    total_collateral=0,  # Would fetch from Compound in production
                    total_debt=0,
                    at_risk=at_risk
                )
                positions.append(position)
                
        except Exception as e:
            print(f"Error fetching positions for {user_address}: {e}")
        
        return positions
    
    async def check_rebalance_needed(self, user_address: str) -> Dict:
        """Check if user needs rebalancing"""
        try:
            result = self.liquidation_prevention.functions.checkRebalanceNeeded(
                Web3.to_checksum_address(user_address)
            ).call()
            
            return {
                "needs_rebalance": result[0],
                "protocol": result[1],
                "current_health": result[2] / 1e18
            }
        except Exception as e:
            print(f"Error checking rebalance for {user_address}: {e}")
            return {"needs_rebalance": False, "protocol": "", "current_health": 0}
