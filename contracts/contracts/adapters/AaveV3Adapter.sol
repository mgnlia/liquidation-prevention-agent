// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../interfaces/IAaveV3Pool.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title AaveV3Adapter
 * @notice Adapter for monitoring Aave V3 positions and health factors
 * @dev Integrates with Aave V3 Pool to fetch user account data
 */
contract AaveV3Adapter is Ownable {
    IAaveV3Pool public immutable aavePool;
    
    // Health factor threshold (1.5 = 150% = 1.5e18)
    uint256 public constant HEALTH_FACTOR_THRESHOLD = 1.5e18;
    
    // Events
    event PositionMonitored(address indexed user, uint256 healthFactor, uint256 timestamp);
    event LowHealthFactorDetected(address indexed user, uint256 healthFactor);
    
    constructor(address _aavePool) Ownable(msg.sender) {
        require(_aavePool != address(0), "Invalid Aave pool address");
        aavePool = IAaveV3Pool(_aavePool);
    }
    
    /**
     * @notice Get user's health factor from Aave V3
     * @param user Address of the user
     * @return healthFactor User's current health factor (1e18 = 1.0)
     */
    function getHealthFactor(address user) external view returns (uint256 healthFactor) {
        (,,,, , healthFactor) = aavePool.getUserAccountData(user);
        return healthFactor;
    }
    
    /**
     * @notice Get complete account data for a user
     * @param user Address of the user
     * @return totalCollateralBase Total collateral in base currency
     * @return totalDebtBase Total debt in base currency
     * @return availableBorrowsBase Available borrows in base currency
     * @return currentLiquidationThreshold Current liquidation threshold
     * @return ltv Loan to value ratio
     * @return healthFactor Health factor
     */
    function getUserAccountData(address user)
        external
        view
        returns (
            uint256 totalCollateralBase,
            uint256 totalDebtBase,
            uint256 availableBorrowsBase,
            uint256 currentLiquidationThreshold,
            uint256 ltv,
            uint256 healthFactor
        )
    {
        return aavePool.getUserAccountData(user);
    }
    
    /**
     * @notice Check if user's position is at risk (health factor below threshold)
     * @param user Address of the user
     * @return isAtRisk True if health factor is below threshold
     * @return healthFactor Current health factor
     */
    function isPositionAtRisk(address user) external view returns (bool isAtRisk, uint256 healthFactor) {
        (,,,, , healthFactor) = aavePool.getUserAccountData(user);
        
        // Health factor of 0 means no debt (safe position)
        if (healthFactor == 0) {
            return (false, type(uint256).max);
        }
        
        isAtRisk = healthFactor < HEALTH_FACTOR_THRESHOLD;
        return (isAtRisk, healthFactor);
    }
    
    /**
     * @notice Monitor position and emit event if at risk
     * @param user Address of the user
     */
    function monitorPosition(address user) external {
        (,,,, , uint256 healthFactor) = aavePool.getUserAccountData(user);
        
        emit PositionMonitored(user, healthFactor, block.timestamp);
        
        if (healthFactor > 0 && healthFactor < HEALTH_FACTOR_THRESHOLD) {
            emit LowHealthFactorDetected(user, healthFactor);
        }
    }
    
    /**
     * @notice Batch monitor multiple positions
     * @param users Array of user addresses to monitor
     */
    function monitorPositionsBatch(address[] calldata users) external {
        for (uint256 i = 0; i < users.length; i++) {
            (,,,, , uint256 healthFactor) = aavePool.getUserAccountData(users[i]);
            
            emit PositionMonitored(users[i], healthFactor, block.timestamp);
            
            if (healthFactor > 0 && healthFactor < HEALTH_FACTOR_THRESHOLD) {
                emit LowHealthFactorDetected(users[i], healthFactor);
            }
        }
    }
}
