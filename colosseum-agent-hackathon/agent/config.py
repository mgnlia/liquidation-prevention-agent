"""SolShield Agent Configuration"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class SolanaConfig:
    cluster: str = os.getenv("SOLANA_CLUSTER", "devnet")
    helius_api_key: str = os.getenv("HELIUS_API_KEY", "")
    rpc_url: str = os.getenv(
        "HELIUS_RPC_URL",
        "https://api.devnet.solana.com"
    )
    ws_url: str = os.getenv(
        "HELIUS_WS_URL",
        "wss://api.devnet.solana.com"
    )


@dataclass
class AIConfig:
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    model: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
    max_tokens: int = 4096
    temperature: float = 0.1  # Low temperature for consistent risk analysis


@dataclass
class AgentWalletConfig:
    api_key: str = os.getenv("AGENT_WALLET_API_KEY", "")
    wallet_id: str = os.getenv("AGENT_WALLET_ID", "")
    base_url: str = "https://agentwallet.mcpay.tech/api"


@dataclass
class MonitoringConfig:
    check_interval_seconds: int = int(os.getenv("CHECK_INTERVAL_SECONDS", "30"))
    health_factor_warn: float = float(os.getenv("HEALTH_FACTOR_WARN", "1.5"))
    health_factor_critical: float = float(os.getenv("HEALTH_FACTOR_CRITICAL", "1.2"))
    health_factor_emergency: float = float(os.getenv("HEALTH_FACTOR_EMERGENCY", "1.05"))
    max_rebalance_attempts: int = 3
    rebalance_cooldown_seconds: int = 60


@dataclass
class ProtocolAddresses:
    """Solana program IDs for DeFi protocols"""
    kamino_program: str = os.getenv(
        "KAMINO_PROGRAM_ID",
        "KLend2g3cP87ber41GRRLYPqxQ1p57Y5MR8D68Lds"
    )
    marginfi_program: str = os.getenv(
        "MARGINFI_PROGRAM_ID",
        "MFv2hWf31Z9kbCa1snEPYctwafyhdJnV4QSdzCrRKg"
    )
    solend_program: str = os.getenv(
        "SOLEND_PROGRAM_ID",
        "So1endDq2YkqhipRh3WViPa8hFMqRV1JimkXg5H2RGD"
    )
    jupiter_program: str = os.getenv(
        "JUPITER_PROGRAM_ID",
        "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4"
    )
    solshield_program: str = os.getenv(
        "SOLSHIELD_PROGRAM_ID",
        "SoLShie1dAiPrevention1111111111111111111111"
    )


@dataclass
class ColosseumConfig:
    api_key: str = os.getenv("COLOSSEUM_API_KEY", "")
    agent_name: str = os.getenv("COLOSSEUM_AGENT_NAME", "solshield")
    api_base: str = "https://agents.colosseum.com/api"


@dataclass
class AppConfig:
    solana: SolanaConfig = field(default_factory=SolanaConfig)
    ai: AIConfig = field(default_factory=AIConfig)
    wallet: AgentWalletConfig = field(default_factory=AgentWalletConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    protocols: ProtocolAddresses = field(default_factory=ProtocolAddresses)
    colosseum: ColosseumConfig = field(default_factory=ColosseumConfig)
    log_dir: str = os.getenv("LOG_DIR", "agent/logs")


def get_config() -> AppConfig:
    return AppConfig()
