// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./interfaces/ICompoundAdapter.sol";

/**
 * @title IComet
 * @notice Compound V3 (Comet) interface (subset used by this adapter)
 * @dev Compound V3 uses a single-asset model per Comet deployment
 */
interface IComet {
    function supply(address asset, uint256 amount) external;
    function supplyTo(address dst, address asset, uint256 amount) external;
    function withdraw(address asset, uint256 amount) external;
    function withdrawTo(address to, address asset, uint256 amount) external;

    function borrowBalanceOf(address account) external view returns (uint256);
    function collateralBalanceOf(address account, address asset) external view returns (uint256);

    function getAssetInfo(uint8 i) external view returns (AssetInfo memory);
    function getAssetInfoByAddress(address asset) external view returns (AssetInfo memory);
    function numAssets() external view returns (uint8);

    function getPrice(address priceFeed) external view returns (uint256);
    function baseTokenPriceFeed() external view returns (address);
    function baseToken() external view returns (address);
    function baseScale() external view returns (uint256);

    function isLiquidatable(address account) external view returns (bool);

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
 * @notice Adapter contract for Compound V3 (Comet) protocol integration
 * @dev Implements ICompoundAdapter to provide standardized access to Compound V3
 *
 * Key Compound V3 concepts:
 * - Single borrowable asset per Comet market (e.g., USDC)
 * - Multiple collateral assets per market
 * - Health factor derived from collateral value vs borrow balance
 * - isLiquidatable() for direct liquidation check
 */
contract CompoundAdapter is ICompoundAdapter, Ownable {
    IComet public immutable comet;

    // Authorized callers (LiquidationPrevention contract)
    mapping(address => bool) public authorizedCallers;

    event CallerAuthorized(address indexed caller, bool authorized);
    event DebtRepaid(address indexed user, address indexed asset, uint256 amount);
    event CollateralWithdrawn(address indexed user, address indexed asset, uint256 amount);

    modifier onlyAuthorized() {
        require(authorizedCallers[msg.sender] || msg.sender == owner(), "Not authorized");
        _;
    }

    /**
     * @param _comet Compound V3 Comet contract address
     */
    constructor(address _comet) Ownable(msg.sender) {
        comet = IComet(_comet);
    }

    /**
     * @notice Set authorized caller status
     */
    function setAuthorizedCaller(address caller, bool authorized) external onlyOwner {
        authorizedCallers[caller] = authorized;
        emit CallerAuthorized(caller, authorized);
    }

    /**
     * @inheritdoc ICompoundAdapter
     * @dev Compound V3 doesn't have a native health factor concept.
     *      We calculate it as: (total collateral value * liquidation factor) / borrow balance
     *      Returns type(uint256).max if no borrows (infinitely healthy)
     */
    function getHealthFactor(address user) external view override returns (uint256 healthFactor) {
        uint256 borrowBalance = comet.borrowBalanceOf(user);

        // No borrows = infinitely healthy
        if (borrowBalance == 0) {
            return type(uint256).max;
        }

        // Calculate total collateral value weighted by liquidation factors
        uint256 weightedCollateralValue = _getWeightedCollateralValue(user);

        // Get base token price for borrow value
        uint256 basePrice = comet.getPrice(comet.baseTokenPriceFeed());
        uint256 baseScale = comet.baseScale();
        uint256 borrowValue = (borrowBalance * basePrice) / baseScale;

        // Health factor = weighted collateral / borrow value (scaled by 1e18)
        if (borrowValue == 0) {
            return type(uint256).max;
        }

        healthFactor = (weightedCollateralValue * 1e18) / borrowValue;
    }

    /**
     * @inheritdoc ICompoundAdapter
     */
    function getUserPosition(address user)
        external
        view
        override
        returns (
            uint256 collateralValue,
            uint256 borrowBalance,
            uint256 borrowCapacity,
            uint256 liquidationPoint
        )
    {
        borrowBalance = comet.borrowBalanceOf(user);
        collateralValue = _getTotalCollateralValue(user);

        // Borrow capacity = sum of (collateral * borrowCollateralFactor)
        borrowCapacity = _getBorrowCapacity(user);

        // Liquidation point = borrow balance / average liquidation factor
        // Simplified: the collateral value at which liquidation occurs
        if (borrowBalance > 0) {
            uint256 basePrice = comet.getPrice(comet.baseTokenPriceFeed());
            uint256 baseScale = comet.baseScale();
            uint256 borrowValue = (borrowBalance * basePrice) / baseScale;
            // Approximate: liquidation when collateral drops to borrow value
            liquidationPoint = borrowValue;
        }
    }

    /**
     * @inheritdoc ICompoundAdapter
     */
    function repayDebt(
        address asset,
        uint256 amount,
        address onBehalfOf
    ) external override onlyAuthorized {
        IERC20(asset).transferFrom(msg.sender, address(this), amount);
        IERC20(asset).approve(address(comet), amount);
        comet.supplyTo(onBehalfOf, asset, amount);

        emit DebtRepaid(onBehalfOf, asset, amount);
    }

    /**
     * @inheritdoc ICompoundAdapter
     */
    function withdrawCollateral(
        address asset,
        uint256 amount,
        address to
    ) external override onlyAuthorized {
        // Note: caller must have been granted permission by the user via Comet.allow()
        comet.withdrawTo(to, asset, amount);

        emit CollateralWithdrawn(to, asset, amount);
    }

    /**
     * @notice Check if a user is liquidatable on Compound V3
     * @param user The user address
     * @return True if the user can be liquidated
     */
    function isLiquidatable(address user) external view returns (bool) {
        return comet.isLiquidatable(user);
    }

    /**
     * @dev Calculate total collateral value weighted by liquidation factors
     */
    function _getWeightedCollateralValue(address user) internal view returns (uint256 totalValue) {
        uint8 numAssets = comet.numAssets();

        for (uint8 i = 0; i < numAssets; i++) {
            IComet.AssetInfo memory info = comet.getAssetInfo(i);
            uint256 balance = comet.collateralBalanceOf(user, info.asset);

            if (balance > 0) {
                uint256 price = comet.getPrice(info.priceFeed);
                uint256 value = (balance * price) / info.scale;
                // Weight by liquidation collateral factor (scaled by 1e18)
                totalValue += (value * info.liquidateCollateralFactor) / 1e18;
            }
        }
    }

    /**
     * @dev Calculate total unweighted collateral value
     */
    function _getTotalCollateralValue(address user) internal view returns (uint256 totalValue) {
        uint8 numAssets = comet.numAssets();

        for (uint8 i = 0; i < numAssets; i++) {
            IComet.AssetInfo memory info = comet.getAssetInfo(i);
            uint256 balance = comet.collateralBalanceOf(user, info.asset);

            if (balance > 0) {
                uint256 price = comet.getPrice(info.priceFeed);
                totalValue += (balance * price) / info.scale;
            }
        }
    }

    /**
     * @dev Calculate borrow capacity based on collateral factors
     */
    function _getBorrowCapacity(address user) internal view returns (uint256 capacity) {
        uint8 numAssets = comet.numAssets();

        for (uint8 i = 0; i < numAssets; i++) {
            IComet.AssetInfo memory info = comet.getAssetInfo(i);
            uint256 balance = comet.collateralBalanceOf(user, info.asset);

            if (balance > 0) {
                uint256 price = comet.getPrice(info.priceFeed);
                uint256 value = (balance * price) / info.scale;
                capacity += (value * info.borrowCollateralFactor) / 1e18;
            }
        }
    }
}
