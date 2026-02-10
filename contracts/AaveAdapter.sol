// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./interfaces/IAaveAdapter.sol";

/**
 * @title IPoolAddressesProvider
 * @notice Aave V3 PoolAddressesProvider interface
 */
interface IPoolAddressesProvider {
    function getPool() external view returns (address);
    function getPriceOracle() external view returns (address);
}

/**
 * @title IPool
 * @notice Aave V3 Pool interface (subset used by this adapter)
 */
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

    function repay(
        address asset,
        uint256 amount,
        uint256 interestRateMode,
        address onBehalfOf
    ) external returns (uint256);

    function withdraw(
        address asset,
        uint256 amount,
        address to
    ) external returns (uint256);

    function supply(
        address asset,
        uint256 amount,
        address onBehalfOf,
        uint16 referralCode
    ) external;
}

/**
 * @title AaveAdapter
 * @notice Adapter contract for Aave V3 protocol integration
 * @dev Implements IAaveAdapter to provide standardized access to Aave V3
 *
 * Key Aave V3 concepts:
 * - Health Factor: ratio of collateral value to debt value, liquidation at < 1.0
 * - getUserAccountData returns all position data in a single call
 * - Flash loans available for gas-efficient rebalancing
 */
contract AaveAdapter is IAaveAdapter, Ownable {
    IPoolAddressesProvider public immutable addressesProvider;
    IPool public pool;

    // Authorized callers (LiquidationPrevention contract)
    mapping(address => bool) public authorizedCallers;

    event PoolUpdated(address indexed newPool);
    event CallerAuthorized(address indexed caller, bool authorized);
    event DebtRepaid(address indexed user, address indexed asset, uint256 amount);
    event CollateralWithdrawn(address indexed user, address indexed asset, uint256 amount);

    modifier onlyAuthorized() {
        require(authorizedCallers[msg.sender] || msg.sender == owner(), "Not authorized");
        _;
    }

    /**
     * @param _addressesProvider Aave V3 PoolAddressesProvider address
     */
    constructor(address _addressesProvider) Ownable(msg.sender) {
        addressesProvider = IPoolAddressesProvider(_addressesProvider);
        pool = IPool(IPoolAddressesProvider(_addressesProvider).getPool());
    }

    /**
     * @notice Refresh the pool address from the addresses provider
     * @dev Call this if the pool address changes (rare but possible)
     */
    function refreshPool() external onlyOwner {
        pool = IPool(addressesProvider.getPool());
        emit PoolUpdated(address(pool));
    }

    /**
     * @notice Set authorized caller status
     */
    function setAuthorizedCaller(address caller, bool authorized) external onlyOwner {
        authorizedCallers[caller] = authorized;
        emit CallerAuthorized(caller, authorized);
    }

    /**
     * @inheritdoc IAaveAdapter
     */
    function getHealthFactor(address user) external view override returns (uint256 healthFactor) {
        (, , , , , healthFactor) = pool.getUserAccountData(user);
        return healthFactor;
    }

    /**
     * @inheritdoc IAaveAdapter
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
     * @inheritdoc IAaveAdapter
     * @dev Requires this contract to have approval to spend the asset on behalf of msg.sender
     */
    function repayDebt(
        address asset,
        uint256 amount,
        uint256 rateMode,
        address onBehalfOf
    ) external override onlyAuthorized {
        // Transfer tokens from caller to this contract
        IERC20(asset).transferFrom(msg.sender, address(this), amount);

        // Approve pool to spend
        IERC20(asset).approve(address(pool), amount);

        // Repay on behalf of user
        pool.repay(asset, amount, rateMode, onBehalfOf);

        emit DebtRepaid(onBehalfOf, asset, amount);
    }

    /**
     * @inheritdoc IAaveAdapter
     * @dev User must have delegated credit to this contract via Aave's credit delegation
     */
    function withdrawCollateral(
        address asset,
        uint256 amount,
        address to
    ) external override onlyAuthorized {
        // Withdraw from Aave pool
        // Note: user must have approved this contract as a delegate
        pool.withdraw(asset, amount, to);

        emit CollateralWithdrawn(to, asset, amount);
    }

    /**
     * @notice Supply additional collateral on behalf of a user
     * @param asset The asset to supply
     * @param amount The amount to supply
     * @param onBehalfOf The user to supply on behalf of
     */
    function supplyCollateral(
        address asset,
        uint256 amount,
        address onBehalfOf
    ) external onlyAuthorized {
        IERC20(asset).transferFrom(msg.sender, address(this), amount);
        IERC20(asset).approve(address(pool), amount);
        pool.supply(asset, amount, onBehalfOf, 0);
    }

    /**
     * @notice Check if a position is at risk of liquidation
     * @param user The user address
     * @param threshold The health factor threshold (scaled by 1e18)
     * @return atRisk True if health factor is below threshold
     * @return currentHealthFactor The current health factor
     */
    function isAtRisk(address user, uint256 threshold)
        external
        view
        returns (bool atRisk, uint256 currentHealthFactor)
    {
        (, , , , , currentHealthFactor) = pool.getUserAccountData(user);
        atRisk = currentHealthFactor > 0 && currentHealthFactor < threshold;
    }
}
