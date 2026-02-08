// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title ICompoundV3
 * @notice Interface for Compound V3 (Comet) protocol
 */
interface ICompoundV3 {
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

    struct UserBasic {
        int104 principal;
        uint64 baseTrackingIndex;
        uint64 baseTrackingAccrued;
        uint16 assetsIn;
        uint8 _reserved;
    }

    struct UserCollateral {
        uint128 balance;
        uint128 _reserved;
    }

    /**
     * @notice Get user's basic position info
     * @param account The account to query
     * @return UserBasic struct with position data
     */
    function userBasic(address account) external view returns (UserBasic memory);

    /**
     * @notice Get user's collateral balance for a specific asset
     * @param account The account to query
     * @param asset The collateral asset
     * @return UserCollateral struct with balance data
     */
    function userCollateral(address account, address asset) external view returns (UserCollateral memory);

    /**
     * @notice Get asset info by index
     * @param i Asset index
     * @return AssetInfo struct
     */
    function getAssetInfo(uint8 i) external view returns (AssetInfo memory);

    /**
     * @notice Get the number of assets
     * @return Number of assets
     */
    function numAssets() external view returns (uint8);

    /**
     * @notice Supply collateral to the protocol
     * @param asset The asset to supply
     * @param amount The amount to supply
     */
    function supply(address asset, uint256 amount) external;

    /**
     * @notice Supply collateral on behalf of another account
     * @param to The account to supply for
     * @param asset The asset to supply
     * @param amount The amount to supply
     */
    function supplyTo(address to, address asset, uint256 amount) external;

    /**
     * @notice Withdraw collateral from the protocol
     * @param asset The asset to withdraw
     * @param amount The amount to withdraw
     */
    function withdraw(address asset, uint256 amount) external;

    /**
     * @notice Check if an account's position is liquidatable
     * @param account The account to check
     * @return True if liquidatable
     */
    function isLiquidatable(address account) external view returns (bool);

    /**
     * @notice Get the current borrow balance for an account
     * @param account The account to query
     * @return The borrow balance
     */
    function borrowBalanceOf(address account) external view returns (uint256);

    /**
     * @notice Get the collateral value for an account
     * @param account The account to query
     * @return The collateral value
     */
    function collateralBalanceOf(address account, address asset) external view returns (uint128);
}
