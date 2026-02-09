"""
Configuration for the Liquidation Prevention Agent
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Agent configuration"""
    
    # Network Configuration
    network: str = os.getenv("NETWORK", "sepolia")
    rpc_url: str = os.getenv("SEPOLIA_RPC_URL", "https://rpc.sepolia.org")
    
    # Contract Addresses
    liquidation_prevention_address: Optional[str] = os.getenv("LIQUIDATION_PREVENTION_ADDRESS")
    aave_adapter_address: Optional[str] = os.getenv("AAVE_ADAPTER_ADDRESS")
    compound_adapter_address: Optional[str] = os.getenv("COMPOUND_ADAPTER_ADDRESS")
    flash_loan_rebalancer_address: Optional[str] = os.getenv("FLASH_LOAN_REBALANCER_ADDRESS")
    
    # AI Configuration
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    claude_model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 1024
    
    # Monitoring Configuration
    check_interval: int = int(os.getenv("CHECK_INTERVAL", "60"))  # seconds
    min_health_factor: float = float(os.getenv("MIN_HEALTH_FACTOR", "1.5"))
    target_health_factor: float = float(os.getenv("TARGET_HEALTH_FACTOR", "2.0"))
    
    # Risk Thresholds
    critical_threshold: float = 1.15  # Immediate action required
    warning_threshold: float = 1.3    # Monitor closely
    safe_threshold: float = 1.5       # Healthy position
    
    # Execution Configuration
    max_gas_price_gwei: int = 100
    slippage_tolerance: float = 0.01  # 1%
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    ai_attribution_file: str = "docs/ai-attribution.jsonl"
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables"""
        return cls()
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        
        if not self.liquidation_prevention_address:
            raise ValueError("LIQUIDATION_PREVENTION_ADDRESS not set")
        
        if self.min_health_factor <= 1.0:
            raise ValueError("MIN_HEALTH_FACTOR must be > 1.0")
        
        if self.target_health_factor <= self.min_health_factor:
            raise ValueError("TARGET_HEALTH_FACTOR must be > MIN_HEALTH_FACTOR")
        
        return True
    
    def get_network_rpc(self) -> str:
        """Get RPC URL for current network"""
        network_rpcs = {
            "sepolia": os.getenv("SEPOLIA_RPC_URL", "https://rpc.sepolia.org"),
            "baseSepolia": os.getenv("BASE_SEPOLIA_RPC_URL", "https://sepolia.base.org"),
            "arbitrumSepolia": os.getenv("ARBITRUM_SEPOLIA_RPC_URL", "https://sepolia-rollup.arbitrum.io/rpc"),
        }
        return network_rpcs.get(self.network, self.rpc_url)
