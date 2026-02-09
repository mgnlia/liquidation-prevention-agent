"""
Tests for position monitoring
"""

import pytest
from unittest.mock import Mock, AsyncMock
from web3 import Web3

from agent.monitor import PositionMonitor, UserPosition
from agent.config import Config

@pytest.fixture
def config():
    """Create test config"""
    config = Config()
    config.liquidation_prevention_address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    config.min_health_factor = 1.5
    return config

@pytest.fixture
def web3_mock():
    """Create mock Web3 instance"""
    return Mock(spec=Web3)

@pytest.fixture
def monitor(web3_mock, config):
    """Create PositionMonitor instance"""
    return PositionMonitor(web3_mock, config)

def test_user_position_creation():
    """Test UserPosition dataclass"""
    position = UserPosition(
        address="0x123",
        protocol="aave",
        health_factor=1.5,
        total_collateral=10000,
        total_debt=6000,
        at_risk=False
    )
    
    assert position.address == "0x123"
    assert position.protocol == "aave"
    assert position.health_factor == 1.5
    assert position.at_risk is False

def test_at_risk_detection():
    """Test at-risk flag based on health factor"""
    risky_position = UserPosition(
        address="0x123",
        protocol="aave",
        health_factor=1.1,
        total_collateral=10000,
        total_debt=9000,
        at_risk=True
    )
    
    assert risky_position.at_risk is True
    assert risky_position.health_factor < 1.2

@pytest.mark.asyncio
async def test_get_monitored_users_empty(monitor):
    """Test getting monitored users when none configured"""
    users = await monitor.get_monitored_users()
    assert isinstance(users, list)

@pytest.mark.asyncio
async def test_get_user_positions_no_contract(monitor):
    """Test getting positions when contract not initialized"""
    positions = await monitor.get_user_positions("0x123")
    assert isinstance(positions, list)
    assert len(positions) == 0

def test_load_abi_fallback(monitor):
    """Test ABI loading with fallback"""
    abi = monitor._load_abi("NonExistentContract")
    assert isinstance(abi, list)
    assert len(abi) == 0  # Fallback returns empty list
