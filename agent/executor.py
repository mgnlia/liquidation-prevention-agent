"""
Transaction Executor - Executes rebalancing transactions on-chain
"""
import os
import json
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()

class TransactionExecutor:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('SEPOLIA_RPC_URL')))
        self.account = Account.from_key(os.getenv('AGENT_PRIVATE_KEY'))
        
        self.liquidation_prevention_address = os.getenv('LIQUIDATION_PREVENTION_ADDRESS')
        self.rebalancer_address = os.getenv('REBALANCER_ADDRESS')
        
        # Load contract ABIs
        self.liquidation_prevention_abi = self._load_abi('LiquidationPrevention')
        self.rebalancer_abi = self._load_abi('FlashLoanRebalancer')
        
        # Initialize contracts
        if self.liquidation_prevention_address:
            self.liquidation_prevention = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.liquidation_prevention_address),
                abi=self.liquidation_prevention_abi
            )
        if self.rebalancer_address:
            self.rebalancer = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.rebalancer_address),
                abi=self.rebalancer_abi
            )
    
    def _load_abi(self, contract_name: str) -> list:
        """Load contract ABI from artifacts"""
        try:
            abi_path = f'../contracts/artifacts/contracts/{contract_name}.sol/{contract_name}.json'
            with open(abi_path, 'r') as f:
                contract_json = json.load(f)
                return contract_json['abi']
        except FileNotFoundError:
            print(f"⚠️  ABI not found for {contract_name}")
            return []
    
    def execute_rebalancing(self, user_address: str, strategy: Dict) -> Optional[str]:
        """Execute rebalancing strategy on-chain"""
        
        if not self.liquidation_prevention_address:
            print("❌ Liquidation prevention contract not configured")
            return None
        
        try:
            # Build rebalancing parameters
            params = self._build_rebalance_params(user_address, strategy)
            
            # Build transaction
            tx = self.liquidation_prevention.functions.triggerRebalance(params).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': strategy.get('estimatedGas', 500000),
                'gasPrice': self.w3.eth.gas_price,
                'chainId': 11155111  # Sepolia
            })
            
            # Sign transaction
            signed_tx = self.account.sign_transaction(tx)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            print(f"✅ Rebalancing transaction sent: {tx_hash.hex()}")
            
            # Wait for confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt['status'] == 1:
                print(f"✅ Rebalancing successful! Gas used: {receipt['gasUsed']}")
                return tx_hash.hex()
            else:
                print(f"❌ Rebalancing transaction failed")
                return None
                
        except Exception as e:
            print(f"❌ Error executing rebalancing: {e}")
            return None
    
    def _build_rebalance_params(self, user_address: str, strategy: Dict) -> tuple:
        """Build parameters for rebalancing transaction"""
        
        # This is a simplified version - in production would need:
        # - Actual token addresses
        # - Proper amount calculations
        # - DEX swap data
        
        # Placeholder addresses (would be actual tokens on Sepolia)
        USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # Placeholder
        WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"  # Placeholder
        
        debt_to_repay = int(strategy.get('debtToRepay', 0) * 1e6)  # Assuming USDC (6 decimals)
        
        params = (
            Web3.to_checksum_address(user_address),
            Web3.to_checksum_address(WETH_ADDRESS),  # collateralAsset
            Web3.to_checksum_address(USDC_ADDRESS),  # debtAsset
            0,  # collateralAmount (calculated in contract)
            debt_to_repay,  # debtAmount
            0,  # minCollateralOut (slippage protection)
            b''  # swapData (DEX-specific)
        )
        
        return params
    
    def monitor_position_onchain(self, user_address: str) -> Optional[str]:
        """Trigger on-chain position monitoring"""
        
        if not self.liquidation_prevention_address:
            print("❌ Liquidation prevention contract not configured")
            return None
        
        try:
            user_address = Web3.to_checksum_address(user_address)
            
            # Build transaction
            tx = self.liquidation_prevention.functions.monitorUser(user_address).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
                'chainId': 11155111
            })
            
            # Sign and send
            signed_tx = self.account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            print(f"✅ Monitoring transaction sent: {tx_hash.hex()}")
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"❌ Error monitoring position: {e}")
            return None
    
    def get_transaction_status(self, tx_hash: str) -> Dict:
        """Get status of a transaction"""
        try:
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            
            return {
                "hash": tx_hash,
                "status": "success" if receipt['status'] == 1 else "failed",
                "blockNumber": receipt['blockNumber'],
                "gasUsed": receipt['gasUsed'],
                "confirmed": True
            }
        except Exception as e:
            return {
                "hash": tx_hash,
                "status": "pending",
                "confirmed": False,
                "error": str(e)
            }
    
    def estimate_gas(self, user_address: str, strategy: Dict) -> int:
        """Estimate gas for rebalancing transaction"""
        try:
            params = self._build_rebalance_params(user_address, strategy)
            
            gas_estimate = self.liquidation_prevention.functions.triggerRebalance(params).estimate_gas({
                'from': self.account.address
            })
            
            # Add 20% buffer
            return int(gas_estimate * 1.2)
            
        except Exception as e:
            print(f"⚠️  Gas estimation failed: {e}")
            return 500000  # Default fallback
    
    def check_agent_balance(self) -> Dict:
        """Check agent wallet balance"""
        balance_wei = self.w3.eth.get_balance(self.account.address)
        balance_eth = self.w3.from_wei(balance_wei, 'ether')
        
        return {
            "address": self.account.address,
            "balance": float(balance_eth),
            "balanceWei": balance_wei,
            "hasSufficientBalance": balance_eth > 0.01  # Need at least 0.01 ETH
        }

if __name__ == "__main__":
    print("⚡ Transaction Executor - Testing")
    print("=" * 60)
    
    executor = TransactionExecutor()
    
    # Check agent balance
    balance_info = executor.check_agent_balance()
    print(f"\n💰 Agent Wallet:")
    print(f"   Address: {balance_info['address']}")
    print(f"   Balance: {balance_info['balance']:.6f} ETH")
    print(f"   Sufficient: {balance_info['hasSufficientBalance']}")
    
    # Test gas estimation
    test_strategy = {
        "debtToRepay": 1000,
        "estimatedGas": 300000
    }
    
    print(f"\n⛽ Gas Estimation Test:")
    gas_estimate = executor.estimate_gas("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", test_strategy)
    print(f"   Estimated Gas: {gas_estimate}")
    
    print("\n" + "=" * 60)
