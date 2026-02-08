"""
Position Monitor - Fetches live DeFi positions from on-chain data
"""
import os
import json
from web3 import Web3
from dotenv import load_dotenv
from typing import Dict, List, Optional

load_dotenv()

class PositionMonitor:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('SEPOLIA_RPC_URL')))
        self.liquidation_prevention_address = os.getenv('LIQUIDATION_PREVENTION_ADDRESS')
        self.aave_adapter_address = os.getenv('AAVE_ADAPTER_ADDRESS')
        
        # Load contract ABIs
        self.liquidation_prevention_abi = self._load_abi('LiquidationPrevention')
        self.aave_adapter_abi = self._load_abi('AaveV3Adapter')
        
        # Initialize contracts
        if self.liquidation_prevention_address:
            self.liquidation_prevention = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.liquidation_prevention_address),
                abi=self.liquidation_prevention_abi
            )
        if self.aave_adapter_address:
            self.aave_adapter = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.aave_adapter_address),
                abi=self.aave_adapter_abi
            )
    
    def _load_abi(self, contract_name: str) -> List:
        """Load contract ABI from artifacts"""
        try:
            abi_path = f'../contracts/artifacts/contracts/{contract_name}.sol/{contract_name}.json'
            with open(abi_path, 'r') as f:
                contract_json = json.load(f)
                return contract_json['abi']
        except FileNotFoundError:
            print(f"⚠️  ABI not found for {contract_name}, using minimal ABI")
            return []
    
    def get_aave_position(self, user_address: str) -> Dict:
        """Fetch Aave V3 position data for a user"""
        try:
            if not self.aave_adapter_address:
                return {"error": "Aave adapter not configured"}
            
            user_address = Web3.to_checksum_address(user_address)
            
            # Get account data from Aave adapter
            account_data = self.aave_adapter.functions.getUserAccountData(user_address).call()
            
            return {
                "protocol": "Aave V3",
                "user": user_address,
                "totalCollateralBase": account_data[0],
                "totalDebtBase": account_data[1],
                "availableBorrowsBase": account_data[2],
                "currentLiquidationThreshold": account_data[3],
                "ltv": account_data[4],
                "healthFactor": account_data[5],
                "healthFactorFormatted": account_data[5] / 1e18 if account_data[5] > 0 else float('inf'),
                "isAtRisk": account_data[5] > 0 and account_data[5] < 1.5e18
            }
        except Exception as e:
            return {"error": str(e), "user": user_address}
    
    def get_health_factor(self, user_address: str) -> float:
        """Get health factor for a user"""
        try:
            if not self.aave_adapter_address:
                return float('inf')
            
            user_address = Web3.to_checksum_address(user_address)
            health_factor = self.aave_adapter.functions.getHealthFactor(user_address).call()
            
            if health_factor == 0:
                return float('inf')
            
            return health_factor / 1e18
        except Exception as e:
            print(f"❌ Error fetching health factor: {e}")
            return float('inf')
    
    def is_position_at_risk(self, user_address: str) -> tuple[bool, float]:
        """Check if position is at liquidation risk"""
        try:
            if not self.aave_adapter_address:
                return (False, float('inf'))
            
            user_address = Web3.to_checksum_address(user_address)
            result = self.aave_adapter.functions.isPositionAtRisk(user_address).call()
            
            is_at_risk = result[0]
            health_factor = result[1] / 1e18 if result[1] > 0 else float('inf')
            
            return (is_at_risk, health_factor)
        except Exception as e:
            print(f"❌ Error checking risk: {e}")
            return (False, float('inf'))
    
    def get_registered_users(self) -> List[str]:
        """Get list of registered users (from events)"""
        try:
            if not self.liquidation_prevention_address:
                return []
            
            # Get UserRegistered events
            event_filter = self.liquidation_prevention.events.UserRegistered.create_filter(
                fromBlock='earliest'
            )
            events = event_filter.get_all_entries()
            
            users = [event['args']['user'] for event in events]
            return list(set(users))  # Remove duplicates
        except Exception as e:
            print(f"❌ Error fetching registered users: {e}")
            return []
    
    def monitor_all_positions(self) -> List[Dict]:
        """Monitor all registered user positions"""
        users = self.get_registered_users()
        positions = []
        
        for user in users:
            position = self.get_aave_position(user)
            if 'error' not in position:
                positions.append(position)
                
                if position['isAtRisk']:
                    print(f"⚠️  RISK DETECTED: {user} - Health Factor: {position['healthFactorFormatted']:.4f}")
        
        return positions
    
    def get_position_summary(self, user_address: str) -> Dict:
        """Get comprehensive position summary for analysis"""
        position = self.get_aave_position(user_address)
        
        if 'error' in position:
            return position
        
        # Calculate additional metrics
        collateral_usd = position['totalCollateralBase'] / 1e8  # Assuming 8 decimals
        debt_usd = position['totalDebtBase'] / 1e8
        
        summary = {
            **position,
            "collateralUSD": collateral_usd,
            "debtUSD": debt_usd,
            "utilizationRate": (debt_usd / collateral_usd * 100) if collateral_usd > 0 else 0,
            "liquidationPrice": self._estimate_liquidation_price(position),
            "timestamp": self.w3.eth.get_block('latest')['timestamp']
        }
        
        return summary
    
    def _estimate_liquidation_price(self, position: Dict) -> Optional[float]:
        """Estimate liquidation price (simplified)"""
        # This is a simplified calculation
        # In production, would need actual asset prices and more complex logic
        if position['totalCollateralBase'] == 0:
            return None
        
        liquidation_threshold = position['currentLiquidationThreshold'] / 10000
        return (position['totalDebtBase'] / position['totalCollateralBase']) / liquidation_threshold

if __name__ == "__main__":
    print("🔍 Position Monitor - Testing")
    print("=" * 60)
    
    monitor = PositionMonitor()
    
    # Test with a sample address
    test_address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    
    print(f"\n📊 Fetching position for: {test_address}")
    position = monitor.get_position_summary(test_address)
    
    if 'error' not in position:
        print(f"\n✅ Position Data:")
        print(f"   Health Factor: {position['healthFactorFormatted']:.4f}")
        print(f"   Collateral: ${position['collateralUSD']:.2f}")
        print(f"   Debt: ${position['debtUSD']:.2f}")
        print(f"   Utilization: {position['utilizationRate']:.2f}%")
        print(f"   At Risk: {position['isAtRisk']}")
    else:
        print(f"\n❌ Error: {position['error']}")
    
    print("\n" + "=" * 60)
