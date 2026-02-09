"""
Configuration for the Liquidation Prevention Agent
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Agent configuration"""
    
    # Network settings
    network: str
    rpc_url: str
    chain_id: int
    
    # Contract addresses
    liquidation_prevention_address: str
    aave_adapter_address: str
    compound_adapter_address: str
    
    # API keys
    anthropic_api_key: str
    
    # Agent settings
    check_interval: int = 60  # seconds between checks
    min_health_factor: float = 1.5  # trigger rebalance below this
    target_health_factor: float = 2.0  # target after rebalance
    
    # Private key for executing transactions
    private_key: Optional[str] = None
    
    # Multi-chain support
    supported_chains: list = None
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables"""
        
        network = os.getenv("NETWORK", "sepolia")
        
        # Network-specific RPC URLs
        rpc_urls = {
            "sepolia": os.getenv("SEPOLIA_RPC_URL", "https://rpc.sepolia.org"),
            "base": os.getenv("BASE_RPC_URL", "https://mainnet.base.org"),
            "baseSepolia": os.getenv("BASE_SEPOLIA_RPC_URL", "https://sepolia.base.org"),
            "arbitrum": os.getenv("ARBITRUM_RPC_URL", "https://arb1.arbitrum.io/rpc"),
            "arbitrumSepolia": os.getenv("ARBITRUM_SEPOLIA_RPC_URL", "https://sepolia-rollup.arbitrum.io/rpc"),
        }
        
        chain_ids = {
            "sepolia": 11155111,
            "base": 8453,
            "baseSepolia": 84532,
            "arbitrum": 42161,
            "arbitrumSepolia": 421614,
        }
        
        return cls(
            network=network,
            rpc_url=rpc_urls.get(network, rpc_urls["sepolia"]),
            chain_id=chain_ids.get(network, chain_ids["sepolia"]),
            liquidation_prevention_address=os.getenv("LIQUIDATION_PREVENTION_ADDRESS", ""),
            aave_adapter_address=os.getenv("AAVE_ADAPTER_ADDRESS", ""),
            compound_adapter_address=os.getenv("COMPOUND_ADAPTER_ADDRESS", ""),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            check_interval=int(os.getenv("CHECK_INTERVAL", "60")),
            min_health_factor=float(os.getenv("MIN_HEALTH_FACTOR", "1.5")),
            target_health_factor=float(os.getenv("TARGET_HEALTH_FACTOR", "2.0")),
            private_key=os.getenv("PRIVATE_KEY"),
            supported_chains=os.getenv("SUPPORTED_CHAINS", "sepolia,baseSepolia,arbitrumSepolia").split(","),
        )
    
    def validate(self) -> bool:
        """Validate configuration"""
        errors = []
        
        if not self.rpc_url:
            errors.append("RPC_URL not set")
        
        if not self.anthropic_api_key:
            errors.append("ANTHROPIC_API_KEY not set")
        
        if not self.liquidation_prevention_address:
            errors.append("LIQUIDATION_PREVENTION_ADDRESS not set")
        
        if errors:
            print("❌ Configuration errors:")
            for error in errors:
                print(f"   - {error}")
            return False
        
        return True
