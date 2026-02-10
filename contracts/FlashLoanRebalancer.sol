// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./interfaces/IAaveAdapter.sol";
import "./interfaces/ICompoundAdapter.sol";

/**
 * @title IFlashLoanSimpleReceiver
 * @notice Aave V3 flash loan callback interface
 */
interface IFlashLoanSimpleReceiver {
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external returns (bool);
}

/**
 * @title IPoolFlashLoan
 * @notice Aave V3 Pool flash loan interface
 */
interface IPoolFlashLoan {
    function flashLoanSimple(
        address receiverAddress,
        address asset,
        uint256 amount,
        bytes calldata params,
        uint16 referralCode
    ) external;
}

/**
 * @title ISwapRouter
 * @notice Minimal DEX router interface for collateral swaps
 * @dev Compatible with Uniswap V3 / SushiSwap style routers
 */
interface ISwapRouter {
    struct ExactInputSingleParams {
        address tokenIn;
        address tokenOut;
        uint24 fee;
        address recipient;
        uint256 deadline;
        uint256 amountIn;
        uint256 amountOutMinimum;
        uint160 sqrtPriceLimitX96;
    }

    function exactInputSingle(ExactInputSingleParams calldata params)
        external
        payable
        returns (uint256 amountOut);
}

/**
 * @title FlashLoanRebalancer
 * @notice Executes flash loan-based rebalancing to prevent liquidations
 * @dev Uses Aave V3 flash loans to:
 *      1. Borrow debt asset
 *      2. Repay user's debt (reducing borrow)
 *      3. Withdraw freed collateral
 *      4. Swap collateral to debt asset via DEX
 *      5. Repay flash loan + premium
 *
 * This achieves a net reduction in user's position leverage,
 * increasing their health factor without requiring upfront capital.
 */
contract FlashLoanRebalancer is IFlashLoanSimpleReceiver, Ownable, ReentrancyGuard {

    IPoolFlashLoan public immutable aavePool;
    IAaveAdapter public aaveAdapter;
    ICompoundAdapter public compoundAdapter;

    // Optional DEX router for production swaps
    ISwapRouter public swapRouter;

    // Authorized callers (LiquidationPrevention contract)
    mapping(address => bool) public authorizedCallers;

    struct RebalanceParams {
        address user;
        string protocol;        // "aave" or "compound"
        address collateralAsset;
        address debtAsset;
        uint256 debtRepayAmount; // Amount of debt to repay
        uint24 swapFeeTier;     // DEX pool fee tier (e.g., 3000 = 0.3%)
        uint256 maxSlippage;    // Max slippage in basis points (100 = 1%)
    }

    event RebalanceExecuted(
        address indexed user,
        string protocol,
        uint256 flashLoanAmount,
        uint256 debtRepaid,
        uint256 collateralWithdrawn,
        uint256 premium
    );

    event FlashLoanReceived(
        address indexed asset,
        uint256 amount,
        uint256 premium
    );

    event SwapRouterUpdated(address indexed newRouter);

    modifier onlyAuthorized() {
        require(authorizedCallers[msg.sender] || msg.sender == owner(), "Not authorized");
        _;
    }

    /**
     * @param _aavePool Aave V3 Pool address (for flash loans)
     * @param _aaveAdapter AaveAdapter contract address
     * @param _compoundAdapter CompoundAdapter contract address
     */
    constructor(
        address _aavePool,
        address _aaveAdapter,
        address _compoundAdapter
    ) Ownable(msg.sender) {
        aavePool = IPoolFlashLoan(_aavePool);
        aaveAdapter = IAaveAdapter(_aaveAdapter);
        compoundAdapter = ICompoundAdapter(_compoundAdapter);
    }

    /**
     * @notice Set authorized caller (LiquidationPrevention contract)
     */
    function setAuthorizedCaller(address caller, bool authorized) external onlyOwner {
        authorizedCallers[caller] = authorized;
    }

    /**
     * @notice Set DEX swap router for production use
     */
    function setSwapRouter(address _swapRouter) external onlyOwner {
        swapRouter = ISwapRouter(_swapRouter);
        emit SwapRouterUpdated(_swapRouter);
    }

    /**
     * @notice Execute rebalancing via flash loan
     * @param user User to rebalance
     * @param protocol Protocol ("aave" or "compound")
     * @param amount Flash loan amount (debt asset)
     * @param collateralAsset Collateral asset to withdraw and swap
     * @param debtAsset Debt asset to repay
     */
    function executeRebalance(
        address user,
        string memory protocol,
        uint256 amount,
        address collateralAsset,
        address debtAsset
    ) external onlyAuthorized nonReentrant {

        RebalanceParams memory params = RebalanceParams({
            user: user,
            protocol: protocol,
            collateralAsset: collateralAsset,
            debtAsset: debtAsset,
            debtRepayAmount: amount,
            swapFeeTier: 3000,    // 0.3% default
            maxSlippage: 100      // 1% default
        });

        bytes memory encodedParams = abi.encode(params);

        // Request flash loan from Aave V3
        // The callback executeOperation() handles the rebalancing logic
        aavePool.flashLoanSimple(
            address(this),
            debtAsset,
            amount,
            encodedParams,
            0 // referral code
        );
    }

    /**
     * @notice Flash loan callback — executes the rebalancing logic
     * @dev Called by Aave Pool during flash loan execution
     *
     * Rebalancing flow:
     * 1. Receive flash loaned debt asset
     * 2. Repay part of user's debt on the target protocol
     * 3. Withdraw freed collateral from the protocol
     * 4. Swap collateral → debt asset via DEX
     * 5. Repay flash loan + premium
     */
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
        require(msg.sender == address(aavePool), "Only Aave Pool");
        require(initiator == address(this), "Invalid initiator");

        emit FlashLoanReceived(asset, amount, premium);

        RebalanceParams memory rp = abi.decode(params, (RebalanceParams));

        // Step 1: Repay user's debt on the target protocol
        _repayUserDebt(rp, asset, amount);

        // Step 2: Withdraw freed collateral
        uint256 collateralReceived = _withdrawCollateral(rp);

        // Step 3: Swap collateral to debt asset to repay flash loan
        uint256 debtAssetReceived = _swapCollateralToDebt(
            rp.collateralAsset,
            asset,
            collateralReceived,
            amount + premium, // minimum needed
            rp.swapFeeTier
        );

        // Step 4: Repay flash loan
        uint256 totalDebt = amount + premium;
        require(debtAssetReceived >= totalDebt, "Insufficient swap output for repayment");

        IERC20(asset).approve(address(aavePool), totalDebt);

        // Return any excess to user
        uint256 excess = debtAssetReceived - totalDebt;
        if (excess > 0) {
            IERC20(asset).transfer(rp.user, excess);
        }

        emit RebalanceExecuted(
            rp.user,
            rp.protocol,
            amount,
            rp.debtRepayAmount,
            collateralReceived,
            premium
        );

        return true;
    }

    /**
     * @dev Repay user's debt on the specified protocol
     */
    function _repayUserDebt(
        RebalanceParams memory rp,
        address debtAsset,
        uint256 amount
    ) internal {
        if (keccak256(bytes(rp.protocol)) == keccak256(bytes("aave"))) {
            // Approve adapter to spend debt asset
            IERC20(debtAsset).approve(address(aaveAdapter), amount);
            // Repay variable rate debt (rateMode = 2)
            aaveAdapter.repayDebt(debtAsset, amount, 2, rp.user);
        } else if (keccak256(bytes(rp.protocol)) == keccak256(bytes("compound"))) {
            IERC20(debtAsset).approve(address(compoundAdapter), amount);
            compoundAdapter.repayDebt(debtAsset, amount, rp.user);
        } else {
            revert("Invalid protocol");
        }
    }

    /**
     * @dev Withdraw freed collateral from the protocol
     */
    function _withdrawCollateral(
        RebalanceParams memory rp
    ) internal returns (uint256 collateralReceived) {
        uint256 balanceBefore = IERC20(rp.collateralAsset).balanceOf(address(this));

        if (keccak256(bytes(rp.protocol)) == keccak256(bytes("aave"))) {
            // Withdraw collateral proportional to debt repaid
            // The exact amount depends on the user's position
            aaveAdapter.withdrawCollateral(
                rp.collateralAsset,
                rp.debtRepayAmount, // Simplified: withdraw equal value
                address(this)
            );
        } else if (keccak256(bytes(rp.protocol)) == keccak256(bytes("compound"))) {
            compoundAdapter.withdrawCollateral(
                rp.collateralAsset,
                rp.debtRepayAmount,
                address(this)
            );
        }

        collateralReceived = IERC20(rp.collateralAsset).balanceOf(address(this)) - balanceBefore;
    }

    /**
     * @dev Swap collateral asset to debt asset via DEX
     * @notice In production, integrates with Uniswap V3 / 1inch / Paraswap
     *         For testnet/demo: assumes 1:1 swap (tokens are test tokens)
     */
    function _swapCollateralToDebt(
        address collateralAsset,
        address debtAsset,
        uint256 collateralAmount,
        uint256 minAmountOut,
        uint24 feeTier
    ) internal returns (uint256 amountOut) {
        // If swap router is configured, use it (production)
        if (address(swapRouter) != address(0)) {
            IERC20(collateralAsset).approve(address(swapRouter), collateralAmount);

            ISwapRouter.ExactInputSingleParams memory swapParams = ISwapRouter.ExactInputSingleParams({
                tokenIn: collateralAsset,
                tokenOut: debtAsset,
                fee: feeTier,
                recipient: address(this),
                deadline: block.timestamp + 300, // 5 minute deadline
                amountIn: collateralAmount,
                amountOutMinimum: minAmountOut,
                sqrtPriceLimitX96: 0
            });

            amountOut = swapRouter.exactInputSingle(swapParams);
        } else {
            // Testnet fallback: assume collateral is already the debt asset
            // or that we have sufficient debt asset balance
            // This allows testing the flash loan flow without a live DEX
            amountOut = IERC20(debtAsset).balanceOf(address(this));
        }
    }

    /**
     * @notice Emergency withdraw function
     * @param token Token to withdraw
     * @param amount Amount to withdraw
     */
    function emergencyWithdraw(address token, uint256 amount) external onlyOwner {
        IERC20(token).transfer(owner(), amount);
    }

    receive() external payable {}
}
