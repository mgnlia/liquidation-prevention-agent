// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "./interfaces/IAaveV3Pool.sol";
import "./interfaces/IFlashLoanSimpleReceiver.sol";

/**
 * @title FlashLoanRebalancer
 * @notice Executes flash loan-based rebalancing to prevent liquidations
 * @dev Implements Aave V3 flash loan receiver interface
 */
contract FlashLoanRebalancer is IFlashLoanSimpleReceiver, Ownable, ReentrancyGuard {
    using SafeERC20 for IERC20;

    address public immutable override ADDRESSES_PROVIDER;
    address public immutable override POOL;
    
    // Authorized executor (AI agent)
    address public executor;
    
    // Rebalancing parameters
    struct RebalanceParams {
        address user;
        address debtAsset;
        uint256 debtAmount;
        address collateralAsset;
        uint256 collateralAmount;
        uint256 minHealthFactor;
    }
    
    // Events
    event RebalanceExecuted(
        address indexed user,
        address debtAsset,
        uint256 debtRepaid,
        address collateralAsset,
        uint256 collateralSwapped,
        uint256 newHealthFactor,
        uint256 timestamp
    );
    
    event ExecutorUpdated(address indexed oldExecutor, address indexed newExecutor);
    
    event FlashLoanReceived(
        address indexed asset,
        uint256 amount,
        uint256 premium,
        uint256 timestamp
    );

    /**
     * @notice Constructor
     * @param _addressesProvider Aave V3 addresses provider
     * @param _pool Aave V3 pool address
     * @param _executor Authorized executor address (AI agent)
     */
    constructor(
        address _addressesProvider,
        address _pool,
        address _executor
    ) {
        require(_addressesProvider != address(0), "Invalid addresses provider");
        require(_pool != address(0), "Invalid pool address");
        require(_executor != address(0), "Invalid executor address");
        
        ADDRESSES_PROVIDER = _addressesProvider;
        POOL = _pool;
        executor = _executor;
    }

    /**
     * @notice Modifier to restrict access to authorized executor
     */
    modifier onlyExecutor() {
        require(msg.sender == executor, "Not authorized executor");
        _;
    }

    /**
     * @notice Update authorized executor
     * @param newExecutor New executor address
     */
    function setExecutor(address newExecutor) external onlyOwner {
        require(newExecutor != address(0), "Invalid executor address");
        address oldExecutor = executor;
        executor = newExecutor;
        emit ExecutorUpdated(oldExecutor, newExecutor);
    }

    /**
     * @notice Initiate flash loan rebalancing
     * @param params Rebalancing parameters
     */
    function initiateRebalance(RebalanceParams calldata params)
        external
        onlyExecutor
        nonReentrant
    {
        require(params.user != address(0), "Invalid user address");
        require(params.debtAsset != address(0), "Invalid debt asset");
        require(params.debtAmount > 0, "Invalid debt amount");
        
        // Encode rebalancing parameters
        bytes memory data = abi.encode(params);
        
        // Request flash loan from Aave V3
        IAaveV3Pool(POOL).flashLoanSimple(
            address(this),
            params.debtAsset,
            params.debtAmount,
            data,
            0 // referralCode
        );
    }

    /**
     * @notice Execute operation after receiving flash loan
     * @param asset The address of the flash-borrowed asset
     * @param amount The amount of the flash-borrowed asset
     * @param premium The fee of the flash-borrowed asset
     * @param initiator The address of the flashloan initiator
     * @param params The byte-encoded params passed when initiating the flashloan
     * @return True if the execution succeeds
     */
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
        require(msg.sender == POOL, "Caller must be Pool");
        require(initiator == address(this), "Initiator must be this contract");
        
        emit FlashLoanReceived(asset, amount, premium, block.timestamp);
        
        // Decode rebalancing parameters
        RebalanceParams memory rebalanceParams = abi.decode(params, (RebalanceParams));
        
        // Step 1: Repay user's debt on Aave
        IERC20(asset).safeApprove(POOL, amount);
        IAaveV3Pool(POOL).repay(
            asset,
            amount,
            2, // variable rate
            rebalanceParams.user
        );
        
        // Step 2: Withdraw user's collateral
        // Note: In production, this would require user authorization via delegation
        // For now, this demonstrates the logic flow
        
        // Step 3: Swap collateral to debt asset (via DEX integration)
        // This would integrate with Uniswap/1inch in production
        // For demo purposes, we assume the swap is handled externally
        
        // Step 4: Approve and repay flash loan + premium
        uint256 totalDebt = amount + premium;
        IERC20(asset).safeApprove(POOL, totalDebt);
        
        // Get new health factor
        (,,,,,uint256 newHealthFactor) = IAaveV3Pool(POOL).getUserAccountData(rebalanceParams.user);
        
        require(
            newHealthFactor >= rebalanceParams.minHealthFactor,
            "Health factor still too low"
        );
        
        emit RebalanceExecuted(
            rebalanceParams.user,
            rebalanceParams.debtAsset,
            amount,
            rebalanceParams.collateralAsset,
            rebalanceParams.collateralAmount,
            newHealthFactor,
            block.timestamp
        );
        
        return true;
    }

    /**
     * @notice Emergency withdrawal function
     * @param token Token to withdraw
     * @param amount Amount to withdraw
     */
    function emergencyWithdraw(address token, uint256 amount) external onlyOwner {
        IERC20(token).safeTransfer(owner(), amount);
    }

    /**
     * @notice Receive ETH
     */
    receive() external payable {}
}
