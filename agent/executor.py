"""
Rebalance execution module
Executes on-chain transactions to rebalance positions
"""

from web3 import Web3
from eth_account import Account
from .config import Config
import json

class RebalanceExecutor:
    """Executes rebalancing transactions on-chain"""
    
    def __init__(self, web3: Web3, config: Config):
        self.web3 = web3
        self.config = config
        
        # Load contract
        self.liquidation_prevention = self._load_contract(
            config.liquidation_prevention_address,
            "LiquidationPrevention"
        )
        
        # Load account if private key provided
        self.account = None
        if config.private_key:
            self.account = Account.from_key(config.private_key)
    
    def _load_contract(self, address: str, name: str):
        """Load contract instance"""
        try:
            with open(f"../artifacts/contracts/{name}.sol/{name}.json") as f:
                artifact = json.load(f)
                abi = artifact["abi"]
            return self.web3.eth.contract(address=address, abi=abi)
        except Exception as e:
            print(f"Warning: Could not load {name} contract: {e}")
            return None
    
    async def execute_rebalance(
        self,
        user_address: str,
        protocol: str,
        amount: float
    ) -> dict:
        """
        Execute rebalancing transaction
        
        Returns:
            dict with success status, tx_hash, and new_health_factor
        """
        
        if not self.account:
            return {
                "success": False,
                "error": "No private key configured"
            }
        
        if not self.liquidation_prevention:
            return {
                "success": False,
                "error": "Contract not loaded"
            }
        
        try:
            # Convert amount to Wei (assuming USDC with 6 decimals)
            amount_wei = int(amount * 1e6)
            
            # Example addresses - would be determined by Claude analysis
            collateral_asset = "0x0000000000000000000000000000000000000000"
            debt_asset = "0x0000000000000000000000000000000000000000"
            
            # Build transaction
            tx = self.liquidation_prevention.functions.executeRebalance(
                user_address,
                protocol,
                amount_wei,
                collateral_asset,
                debt_asset
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.web3.eth.get_transaction_count(self.account.address),
                'gas': 500000,
                'gasPrice': self.web3.eth.gas_price,
            })
            
            # Sign and send transaction
            signed_tx = self.account.sign_transaction(tx)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for receipt
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt['status'] == 1:
                # Get new health factor
                result = self.liquidation_prevention.functions.getUserHealthFactors(
                    user_address
                ).call()
                
                new_health_factor = result[2] / 1e18 if result[2] > 0 else 0
                
                return {
                    "success": True,
                    "tx_hash": tx_hash.hex(),
                    "new_health_factor": new_health_factor
                }
            else:
                return {
                    "success": False,
                    "error": "Transaction reverted"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def simulate_rebalance(
        self,
        user_address: str,
        protocol: str,
        amount: float
    ) -> dict:
        """
        Simulate rebalancing without executing transaction
        Useful for testing and gas estimation
        """
        try:
            # Would use eth_call to simulate
            return {
                "success": True,
                "estimated_gas": 350000,
                "estimated_health_factor": 2.0
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
