// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/IAaveAdapter.sol";

interface IPool {
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
        );
}

interface IPoolAddressesProvider {
    function getPool() external view returns (address);
}

/**
 * @title AaveAdapter
 * @notice Adapter for Aave V3 protocol integration
 */
contract AaveAdapter is IAaveAdapter, Ownable {
    
    IPoolAddressesProvider public immutable addressesProvider;
    IPool public pool;
    
    constructor(address _addressesProvider) Ownable(msg.sender) {
        addressesProvider = IPoolAddressesProvider(_addressesProvider);
        pool = IPool(addressesProvider.getPool());
    }
    
    /**
     * @notice Get user's health factor on Aave
     * @param user User address
     * @return healthFactor Health factor (scaled by 1e18, 1e18 = 1.0)
     */
    function getHealthFactor(address user) external view override returns (uint256) {
        (,,,,,uint256 healthFactor) = pool.getUserAccountData(user);
        return healthFactor;
    }
    
    /**
     * @notice Get detailed user account data from Aave
     */
    function getUserAccountData(address user)
        external
        view
        override
        returns (
            uint256 totalCollateralBase,
            uint256 totalDebtBase,
            uint256 availableBorrowsBase,
            uint256 currentLiquidationThreshold,
            uint256 ltv,
            uint256 healthFactor
        )
    {
        return pool.getUserAccountData(user);
    }
    
    /**
     * @notice Check if user is at risk of liquidation
     * @param user User address
     * @param threshold Health factor threshold (e.g., 1.5e18 for 1.5)
     * @return atRisk True if health factor below threshold
     */
    function isAtRisk(address user, uint256 threshold) external view override returns (bool) {
        (,,,,,uint256 healthFactor) = pool.getUserAccountData(user);
        
        // Health factor of 0 means no debt, not at risk
        if (healthFactor == 0) {
            return false;
        }
        
        return healthFactor < threshold;
    }
    
    /**
     * @notice Update pool address if provider changes it
     */
    function updatePool() external onlyOwner {
        pool = IPool(addressesProvider.getPool());
    }
}
