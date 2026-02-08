// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "../interfaces/ICompoundV3.sol";

/**
 * @title CompoundV3Adapter
 * @notice Adapter contract for monitoring and interacting with Compound V3 (Comet) positions
 * @dev Provides liquidation risk monitoring for the AI agent
 */
contract CompoundV3Adapter is Ownable, ReentrancyGuard {
    ICompoundV3 public immutable comet;
    
    // Events
    event PositionMonitored(
        address indexed user,
        int104 principal,
        uint256 borrowBalance,
        bool isLiquidatable,
        uint256 timestamp
    );
    
    event RiskDetected(
        address indexed user,
        uint256 borrowBalance,
        uint256 timestamp
    );

    /**
     * @notice Constructor
     * @param _comet Address of Compound V3 (Comet) contract
     */
    constructor(address _comet) {
        require(_comet != address(0), "Invalid Comet address");
        comet = ICompoundV3(_comet);
    }

    /**
     * @notice Get user's basic position data
     * @param user Address of the user
     * @return principal User's principal balance (negative = borrowed)
     * @return baseTrackingIndex Tracking index for interest
     * @return baseTrackingAccrued Accrued interest
     */
    function getUserBasic(address user)
        external
        view
        returns (
            int104 principal,
            uint64 baseTrackingIndex,
            uint64 baseTrackingAccrued
        )
    {
        ICompoundV3.UserBasic memory basic = comet.userBasic(user);
        return (basic.principal, basic.baseTrackingIndex, basic.baseTrackingAccrued);
    }

    /**
     * @notice Get user's collateral balance for a specific asset
     * @param user Address of the user
     * @param asset Address of the collateral asset
     * @return balance Collateral balance
     */
    function getUserCollateral(address user, address asset)
        external
        view
        returns (uint128 balance)
    {
        ICompoundV3.UserCollateral memory collateral = comet.userCollateral(user, asset);
        return collateral.balance;
    }

    /**
     * @notice Check if user's position is liquidatable
     * @param user Address of the user
     * @return isLiquidatable True if position can be liquidated
     */
    function isPositionLiquidatable(address user)
        external
        view
        returns (bool isLiquidatable)
    {
        return comet.isLiquidatable(user);
    }

    /**
     * @notice Get user's borrow balance
     * @param user Address of the user
     * @return borrowBalance Current borrow balance
     */
    function getBorrowBalance(address user)
        external
        view
        returns (uint256 borrowBalance)
    {
        return comet.borrowBalanceOf(user);
    }

    /**
     * @notice Check if user's position is at risk
     * @param user Address of the user
     * @return isAtRisk True if position is liquidatable or close to it
     * @return borrowBalance Current borrow balance
     */
    function isPositionAtRisk(address user)
        external
        view
        returns (bool isAtRisk, uint256 borrowBalance)
    {
        isAtRisk = comet.isLiquidatable(user);
        borrowBalance = comet.borrowBalanceOf(user);
        return (isAtRisk, borrowBalance);
    }

    /**
     * @notice Monitor user position and emit events for off-chain indexing
     * @param user Address of the user to monitor
     */
    function monitorPosition(address user) external {
        ICompoundV3.UserBasic memory basic = comet.userBasic(user);
        uint256 borrowBalance = comet.borrowBalanceOf(user);
        bool isLiquidatable = comet.isLiquidatable(user);

        emit PositionMonitored(
            user,
            basic.principal,
            borrowBalance,
            isLiquidatable,
            block.timestamp
        );

        if (isLiquidatable) {
            emit RiskDetected(user, borrowBalance, block.timestamp);
        }
    }

    /**
     * @notice Batch monitor multiple user positions
     * @param users Array of user addresses to monitor
     */
    function monitorPositions(address[] calldata users) external {
        for (uint256 i = 0; i < users.length; i++) {
            ICompoundV3.UserBasic memory basic = comet.userBasic(users[i]);
            uint256 borrowBalance = comet.borrowBalanceOf(users[i]);
            bool isLiquidatable = comet.isLiquidatable(users[i]);

            emit PositionMonitored(
                users[i],
                basic.principal,
                borrowBalance,
                isLiquidatable,
                block.timestamp
            );

            if (isLiquidatable) {
                emit RiskDetected(users[i], borrowBalance, block.timestamp);
            }
        }
    }

    /**
     * @notice Get all collateral assets for monitoring
     * @return assets Array of collateral asset addresses
     */
    function getCollateralAssets() external view returns (address[] memory assets) {
        uint8 numAssets = comet.numAssets();
        assets = new address[](numAssets);
        
        for (uint8 i = 0; i < numAssets; i++) {
            ICompoundV3.AssetInfo memory assetInfo = comet.getAssetInfo(i);
            assets[i] = assetInfo.asset;
        }
        
        return assets;
    }

    /**
     * @notice Get detailed asset info
     * @param index Asset index
     * @return asset Asset address
     * @return borrowCollateralFactor Borrow collateral factor
     * @return liquidateCollateralFactor Liquidation collateral factor
     */
    function getAssetInfo(uint8 index)
        external
        view
        returns (
            address asset,
            uint64 borrowCollateralFactor,
            uint64 liquidateCollateralFactor
        )
    {
        ICompoundV3.AssetInfo memory assetInfo = comet.getAssetInfo(index);
        return (
            assetInfo.asset,
            assetInfo.borrowCollateralFactor,
            assetInfo.liquidateCollateralFactor
        );
    }
}
