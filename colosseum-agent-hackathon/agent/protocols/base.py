"""Base protocol adapter interface"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import time


class Protocol(str, Enum):
    KAMINO = "kamino"
    MARGINFI = "marginfi"
    SOLEND = "solend"


class RiskLevel(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class CollateralPosition:
    """Individual collateral asset in a position"""
    mint: str
    symbol: str
    amount: float
    value_usd: float
    ltv: float  # Loan-to-value ratio
    liquidation_threshold: float


@dataclass
class DebtPosition:
    """Individual debt asset in a position"""
    mint: str
    symbol: str
    amount: float
    value_usd: float
    borrow_rate_apy: float


@dataclass
class PositionData:
    """Unified position data across all protocols"""
    protocol: Protocol
    owner: str
    obligation_key: str
    health_factor: float
    total_collateral_usd: float
    total_debt_usd: float
    net_value_usd: float
    risk_level: RiskLevel
    collaterals: list[CollateralPosition] = field(default_factory=list)
    debts: list[DebtPosition] = field(default_factory=list)
    liquidation_price: Optional[float] = None
    timestamp: float = field(default_factory=time.time)

    @property
    def ltv_ratio(self) -> float:
        if self.total_collateral_usd == 0:
            return 0
        return self.total_debt_usd / self.total_collateral_usd

    def to_risk_summary(self) -> str:
        return (
            f"Protocol: {self.protocol.value}\n"
            f"Health Factor: {self.health_factor:.4f}\n"
            f"Collateral: ${self.total_collateral_usd:,.2f}\n"
            f"Debt: ${self.total_debt_usd:,.2f}\n"
            f"Net Value: ${self.net_value_usd:,.2f}\n"
            f"LTV: {self.ltv_ratio:.2%}\n"
            f"Risk Level: {self.risk_level.value}\n"
            f"Collateral Assets: {', '.join(c.symbol for c in self.collaterals)}\n"
            f"Debt Assets: {', '.join(d.symbol for d in self.debts)}"
        )


class ProtocolAdapter(ABC):
    """Base class for DeFi protocol adapters"""

    @abstractmethod
    async def get_positions(self, wallet_address: str) -> list[PositionData]:
        """Fetch all positions for a wallet on this protocol"""
        ...

    @abstractmethod
    async def get_health_factor(self, obligation_key: str) -> float:
        """Get the current health factor for an obligation"""
        ...

    @abstractmethod
    async def get_protocol_name(self) -> str:
        """Return the protocol name"""
        ...

    def classify_risk(self, health_factor: float, warn: float = 1.5, critical: float = 1.2, emergency: float = 1.05) -> RiskLevel:
        """Classify risk level based on health factor"""
        if health_factor < emergency:
            return RiskLevel.EMERGENCY
        elif health_factor < critical:
            return RiskLevel.CRITICAL
        elif health_factor < warn:
            return RiskLevel.WARNING
        return RiskLevel.HEALTHY
