// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "../interfaces/IAaveV3Pool.sol";

/**
 * @title AaveV3Adapter
 * @notice Adapter contract for monitoring and interacting with Aave V3 positions
 * @dev Provides health factor monitoring and position data for the AI agent
 */
contract AaveV3Adapter is Ownable, ReentrancyGuard {
    IAaveV3Pool public immutable aavePool;
    
    // Health factor threshold (1.5 in 18 decimals = 1.5e18)
    uint256 public constant HEALTH_FACTOR_THRESHOLD = 1.5e18;
    
    // Events
    event PositionMonitored(
        address indexed user,
        uint256 healthFactor,
        uint256 totalCollateral,
        uint256 totalDebt,
        uint256 timestamp
    );
    
    event RiskDetected(
        address indexed user,
        uint256 healthFactor,
        uint256 timestamp
    );

    /**
     * @notice Constructor
     * @param _aavePool Address of Aave V3 Pool contract
     */
    constructor(address _aavePool) {
        require(_aavePool != address(0), "Invalid Aave pool address");
        aavePool = IAaveV3Pool(_aavePool);
    }

    /**
     * @notice Get user's health factor from Aave V3
     * @param user Address of the user
     * @return healthFactor The user's current health factor (18 decimals)
     */
    function getHealthFactor(address user) external view returns (uint256 healthFactor) {
        (,,,,,healthFactor) = aavePool.getUserAccountData(user);
        return healthFactor;
    }

    /**
     * @notice Get complete user account data from Aave V3
     * @param user Address of the user
     * @return totalCollateral Total collateral in base currency
     * @return totalDebt Total debt in base currency
     * @return availableBorrows Available borrowing power
     * @return liquidationThreshold Current liquidation threshold
     * @return ltv Loan-to-value ratio
     * @return healthFactor Current health factor
     */
    function getUserAccountData(address user)
        external
        view
        returns (
            uint256 totalCollateral,
            uint256 totalDebt,
            uint256 availableBorrows,
            uint256 liquidationThreshold,
            uint256 ltv,
            uint256 healthFactor
        )
    {
        return aavePool.getUserAccountData(user);
    }

    /**
     * @notice Check if user's position is at risk (health factor < threshold)
     * @param user Address of the user
     * @return isAtRisk True if health factor is below threshold
     * @return healthFactor Current health factor
     */
    function isPositionAtRisk(address user)
        external
        view
        returns (bool isAtRisk, uint256 healthFactor)
    {
        (,,,,,healthFactor) = aavePool.getUserAccountData(user);
        isAtRisk = healthFactor < HEALTH_FACTOR_THRESHOLD && healthFactor > 0;
        return (isAtRisk, healthFactor);
    }

    /**
     * @notice Monitor user position and emit events for off-chain indexing
     * @param user Address of the user to monitor
     */
    function monitorPosition(address user) external {
        (
            uint256 totalCollateral,
            uint256 totalDebt,
            ,
            ,
            ,
            uint256 healthFactor
        ) = aavePool.getUserAccountData(user);

        emit PositionMonitored(
            user,
            healthFactor,
            totalCollateral,
            totalDebt,
            block.timestamp
        );

        if (healthFactor < HEALTH_FACTOR_THRESHOLD && healthFactor > 0) {
            emit RiskDetected(user, healthFactor, block.timestamp);
        }
    }

    /**
     * @notice Batch monitor multiple user positions
     * @param users Array of user addresses to monitor
     */
    function monitorPositions(address[] calldata users) external {
        for (uint256 i = 0; i < users.length; i++) {
            (
                uint256 totalCollateral,
                uint256 totalDebt,
                ,
                ,
                ,
                uint256 healthFactor
            ) = aavePool.getUserAccountData(users[i]);

            emit PositionMonitored(
                users[i],
                healthFactor,
                totalCollateral,
                totalDebt,
                block.timestamp
            );

            if (healthFactor < HEALTH_FACTOR_THRESHOLD && healthFactor > 0) {
                emit RiskDetected(users[i], healthFactor, block.timestamp);
            }
        }
    }

    /**
     * @notice Calculate distance to liquidation
     * @param user Address of the user
     * @return distanceToLiquidation How far the health factor is from 1.0 (liquidation point)
     */
    function getDistanceToLiquidation(address user)
        external
        view
        returns (uint256 distanceToLiquidation)
    {
        (,,,,,uint256 healthFactor) = aavePool.getUserAccountData(user);
        
        if (healthFactor <= 1e18) {
            return 0;
        }
        
        return healthFactor - 1e18;
    }
}
