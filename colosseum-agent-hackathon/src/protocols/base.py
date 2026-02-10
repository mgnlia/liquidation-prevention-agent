"""Base protocol adapter interface for DeFi position monitoring."""
from __future__ import annotations

import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


class HealthStatus(enum.Enum):
    """Position health classification."""
    HEALTHY = "healthy"          # HF > 1.5
    WARNING = "warning"          # 1.2 < HF <= 1.5
    CRITICAL = "critical"        # 1.05 < HF <= 1.2
    EMERGENCY = "emergency"      # HF <= 1.05
    LIQUIDATED = "liquidated"    # HF < 1.0

    @classmethod
    def from_health_factor(cls, hf: float) -> "HealthStatus":
        if hf < 1.0:
            return cls.LIQUIDATED
        elif hf <= 1.05:
            return cls.EMERGENCY
        elif hf <= 1.2:
            return cls.CRITICAL
        elif hf <= 1.5:
            return cls.WARNING
        return cls.HEALTHY


@dataclass
class TokenPosition:
    """Individual token within a position."""
    mint: str
    symbol: str
    amount: float
    usd_value: float
    decimals: int = 9


@dataclass
class Position:
    """Unified DeFi lending position across protocols."""
    protocol: str
    owner: str
    position_key: str
    collateral: list[TokenPosition] = field(default_factory=list)
    debt: list[TokenPosition] = field(default_factory=list)
    total_collateral_usd: float = 0.0
    total_debt_usd: float = 0.0
    health_factor: float = 0.0
    liquidation_threshold: float = 0.0
    ltv: float = 0.0
    status: HealthStatus = HealthStatus.HEALTHY
    last_updated: datetime = field(default_factory=datetime.utcnow)
    raw_data: Optional[dict] = None

    @property
    def available_borrow_usd(self) -> float:
        """How much more can be borrowed before liquidation."""
        if self.liquidation_threshold == 0:
            return 0.0
        max_debt = self.total_collateral_usd * self.liquidation_threshold
        return max(0, max_debt - self.total_debt_usd)

    @property
    def distance_to_liquidation_pct(self) -> float:
        """Percentage drop in collateral value before liquidation."""
        if self.total_collateral_usd == 0 or self.total_debt_usd == 0:
            return 100.0
        liq_price = self.total_debt_usd / self.liquidation_threshold
        return max(0, (self.total_collateral_usd - liq_price) / self.total_collateral_usd * 100)


class ProtocolAdapter(ABC):
    """Abstract base class for DeFi protocol adapters."""

    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url

    @property
    @abstractmethod
    def name(self) -> str:
        """Protocol name."""
        ...

    @abstractmethod
    async def get_positions(self, owner: str) -> list[Position]:
        """Fetch all lending positions for a wallet."""
        ...

    @abstractmethod
    async def get_health_factor(self, position_key: str) -> float:
        """Get current health factor for a specific position."""
        ...

    @abstractmethod
    async def get_liquidation_price(self, position_key: str) -> dict[str, float]:
        """Get liquidation prices for each collateral asset."""
        ...

    async def is_at_risk(self, position: Position, threshold: float = 1.5) -> bool:
        """Check if position health factor is below threshold."""
        return position.health_factor < threshold
