// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title IAaveAdapter
 * @notice Interface for the Aave V3 protocol adapter
 * @dev Abstracts Aave V3 interactions for the LiquidationPrevention system
 */
interface IAaveAdapter {
    /**
     * @notice Get user's health factor on Aave V3
     * @param user The user address
     * @return healthFactor The health factor scaled by 1e18 (1e18 = 1.0)
     */
    function getHealthFactor(address user) external view returns (uint256 healthFactor);

    /**
     * @notice Get user's full account data on Aave V3
     * @param user The user address
     * @return totalCollateralBase Total collateral in base currency (USD, 8 decimals)
     * @return totalDebtBase Total debt in base currency (USD, 8 decimals)
     * @return availableBorrowsBase Available borrows in base currency
     * @return currentLiquidationThreshold Current liquidation threshold (percentage, 4 decimals)
     * @return ltv Current loan-to-value ratio (percentage, 4 decimals)
     * @return healthFactor Health factor scaled by 1e18
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
        );

    /**
     * @notice Repay debt on behalf of a user
     * @param asset The debt asset to repay
     * @param amount The amount to repay
     * @param rateMode The interest rate mode (1 = stable, 2 = variable)
     * @param onBehalfOf The user whose debt to repay
     */
    function repayDebt(
        address asset,
        uint256 amount,
        uint256 rateMode,
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
