// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ICompoundAdapter
 * @notice Interface for the Compound V3 (Comet) protocol adapter
 * @dev Abstracts Compound V3 interactions for the LiquidationPrevention system
 */
interface ICompoundAdapter {
    /**
     * @notice Get user's health factor on Compound V3
     * @param user The user address
     * @return healthFactor The health factor scaled by 1e18 (1e18 = 1.0)
     */
    function getHealthFactor(address user) external view returns (uint256 healthFactor);

    /**
     * @notice Get user's position data on Compound V3
     * @param user The user address
     * @return collateralValue Total collateral value in USD (8 decimals)
     * @return borrowBalance Total borrow balance in base asset
     * @return borrowCapacity Maximum borrow capacity
     * @return liquidationPoint Collateral value at which liquidation occurs
     */
    function getUserPosition(address user)
        external
        view
        returns (
            uint256 collateralValue,
            uint256 borrowBalance,
            uint256 borrowCapacity,
            uint256 liquidationPoint
        );

    /**
     * @notice Repay debt on behalf of a user
     * @param asset The base asset to repay
     * @param amount The amount to repay
     * @param onBehalfOf The user whose debt to repay
     */
    function repayDebt(
        address asset,
        uint256 amount,
        address onBehalfOf
    ) external;

    /**
     * @notice Withdraw collateral on behalf of a user
     * @param asset The collateral asset to withdraw
     * @param amount The amount to withdraw
     * @param to The address to receive the withdrawn asset
     */
    function withdrawCollateral(
        address asset,
        uint256 amount,
        address to
    ) external;
}
