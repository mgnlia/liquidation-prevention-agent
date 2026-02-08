// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title IComet
 * @notice Minimal interface for Compound V3 (Comet)
 */
interface IComet {
    function borrowBalanceOf(address account) external view returns (uint256);
    function collateralBalanceOf(address account, address asset) external view returns (uint128);
    function isLiquidatable(address account) external view returns (bool);
    function getAssetInfo(uint8 i) external view returns (AssetInfo memory);
    function numAssets() external view returns (uint8);
    
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
 * @title CompoundV3Adapter
 * @notice Adapter for monitoring Compound V3 (Comet) positions
 * @dev Integrates with Compound V3 to track collateral and debt
 */
contract CompoundV3Adapter is Ownable {
    IComet public immutable comet;
    
    // Liquidation threshold (similar to health factor concept)
    uint256 public constant LIQUIDATION_THRESHOLD = 150; // 150% = 1.5x collateralization
    
    // Events
    event PositionMonitored(address indexed user, uint256 borrowBalance, uint256 timestamp);
    event LiquidationRiskDetected(address indexed user, uint256 borrowBalance);
    
    constructor(address _comet) Ownable(msg.sender) {
        require(_comet != address(0), "Invalid Comet address");
        comet = IComet(_comet);
    }
    
    /**
     * @notice Get user's borrow balance
     * @param user Address of the user
     * @return borrowBalance Amount borrowed
     */
    function getBorrowBalance(address user) external view returns (uint256 borrowBalance) {
        return comet.borrowBalanceOf(user);
    }
    
    /**
     * @notice Get user's collateral balance for a specific asset
     * @param user Address of the user
     * @param asset Address of the collateral asset
     * @return collateralBalance Amount of collateral
     */
    function getCollateralBalance(address user, address asset) external view returns (uint128 collateralBalance) {
        return comet.collateralBalanceOf(user, asset);
    }
    
    /**
     * @notice Check if user's position is liquidatable
     * @param user Address of the user
     * @return isLiquidatable True if position can be liquidated
     */
    function isPositionLiquidatable(address user) external view returns (bool) {
        return comet.isLiquidatable(user);
    }
    
    /**
     * @notice Check if user's position is at risk
     * @param user Address of the user
     * @return isAtRisk True if position is at risk or liquidatable
     */
    function isPositionAtRisk(address user) external view returns (bool isAtRisk) {
        return comet.isLiquidatable(user);
    }
    
    /**
     * @notice Monitor position and emit events
     * @param user Address of the user
     */
    function monitorPosition(address user) external {
        uint256 borrowBalance = comet.borrowBalanceOf(user);
        bool liquidatable = comet.isLiquidatable(user);
        
        emit PositionMonitored(user, borrowBalance, block.timestamp);
        
        if (liquidatable) {
            emit LiquidationRiskDetected(user, borrowBalance);
        }
    }
    
    /**
     * @notice Batch monitor multiple positions
     * @param users Array of user addresses to monitor
     */
    function monitorPositionsBatch(address[] calldata users) external {
        for (uint256 i = 0; i < users.length; i++) {
            uint256 borrowBalance = comet.borrowBalanceOf(users[i]);
            bool liquidatable = comet.isLiquidatable(users[i]);
            
            emit PositionMonitored(users[i], borrowBalance, block.timestamp);
            
            if (liquidatable) {
                emit LiquidationRiskDetected(users[i], borrowBalance);
            }
        }
    }
    
    /**
     * @notice Get all asset info from Comet
     * @return assets Array of asset information
     */
    function getAllAssets() external view returns (IComet.AssetInfo[] memory assets) {
        uint8 numAssets = comet.numAssets();
        assets = new IComet.AssetInfo[](numAssets);
        
        for (uint8 i = 0; i < numAssets; i++) {
            assets[i] = comet.getAssetInfo(i);
        }
        
        return assets;
    }
}
