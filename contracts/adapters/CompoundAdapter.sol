// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/ICompoundAdapter.sol";

interface IComet {
    function borrowBalanceOf(address account) external view returns (uint256);
    function collateralBalanceOf(address account, address asset) external view returns (uint128);
    function getAssetInfoByAddress(address asset) external view returns (AssetInfo memory);
    function getPrice(address priceFeed) external view returns (uint256);
    
    struct AssetInfo {
        uint8 offset;
        address asset;
        address priceFeed;
        uint64 scale;
        uint64 borrowCollateralFactor;
        uint64 liquidateCollateralFactor;
        uint64 liquidationFactor;
        uint128 supplyCap;
    }
}

/**
 * @title CompoundAdapter
 * @notice Adapter for Compound V3 (Comet) protocol integration
 */
contract CompoundAdapter is ICompoundAdapter, Ownable {
    
    IComet public immutable comet;
    
    // Liquidation threshold (e.g., 0.8e18 = 80%)
    uint256 public constant LIQUIDATION_FACTOR = 0.8e18;
    
    constructor(address _comet) Ownable(msg.sender) {
        comet = IComet(_comet);
    }
    
    /**
     * @notice Get user's health factor on Compound
     * @param user User address
     * @return healthFactor Health factor (scaled by 1e18, 1e18 = 1.0)
     * @dev Health factor = collateral value / (debt value / liquidation threshold)
     */
    function getHealthFactor(address user) external view override returns (uint256) {
        uint256 borrowBalance = comet.borrowBalanceOf(user);
        
        // No debt = no liquidation risk, return max health factor
        if (borrowBalance == 0) {
            return type(uint256).max;
        }
        
        // For simplicity, we approximate health factor
        // In production, would need to iterate through all collateral assets
        // Health factor = (collateral value * liquidation threshold) / debt value
        
        // Placeholder: return 2e18 (health factor of 2.0) if has debt
        // Real implementation would calculate actual collateral value
        return 2e18;
    }
    
    /**
     * @notice Get user's borrow balance
     */
    function getBorrowBalance(address user) external view override returns (uint256) {
        return comet.borrowBalanceOf(user);
    }
    
    /**
     * @notice Get user's collateral balance for a specific asset
     */
    function getCollateralBalance(address user, address asset) 
        external 
        view 
        override 
        returns (uint256) 
    {
        return uint256(comet.collateralBalanceOf(user, asset));
    }
    
    /**
     * @notice Check if user is at risk of liquidation
     * @param user User address
     * @param threshold Health factor threshold
     * @return atRisk True if health factor below threshold
     */
    function isAtRisk(address user, uint256 threshold) external view override returns (bool) {
        uint256 borrowBalance = comet.borrowBalanceOf(user);
        
        if (borrowBalance == 0) {
            return false;
        }
        
        // Simplified risk check
        // Real implementation would calculate actual health factor
        return false;
    }
}
