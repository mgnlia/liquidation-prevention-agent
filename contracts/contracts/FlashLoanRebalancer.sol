// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./interfaces/IAaveV3Pool.sol";
import "./interfaces/IFlashLoanSimpleReceiver.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title FlashLoanRebalancer
 * @notice Executes automated rebalancing using Aave V3 flash loans
 * @dev Receives flash loan, swaps collateral, repays debt, returns flash loan
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
        address collateralAsset;
        address debtAsset;
        uint256 collateralAmount;
        uint256 debtAmount;
        uint256 minCollateralOut;
        bytes swapData;
    }
    
    // Events
    event RebalanceExecuted(
        address indexed user,
        address collateralAsset,
        address debtAsset,
        uint256 collateralSwapped,
        uint256 debtRepaid,
        uint256 flashLoanFee
    );
    event ExecutorUpdated(address indexed oldExecutor, address indexed newExecutor);
    
    // Errors
    error UnauthorizedExecutor();
    error FlashLoanFailed();
    error InsufficientCollateral();
    
    modifier onlyExecutor() {
        if (msg.sender != executor && msg.sender != owner()) {
            revert UnauthorizedExecutor();
        }
        _;
    }
    
    constructor(address _addressesProvider, address _pool, address _executor) Ownable(msg.sender) {
        require(_addressesProvider != address(0), "Invalid addresses provider");
        require(_pool != address(0), "Invalid pool");
        require(_executor != address(0), "Invalid executor");
        
        ADDRESSES_PROVIDER = _addressesProvider;
        POOL = _pool;
        executor = _executor;
    }
    
    /**
     * @notice Update authorized executor
     * @param _newExecutor New executor address
     */
    function setExecutor(address _newExecutor) external onlyOwner {
        require(_newExecutor != address(0), "Invalid executor");
        address oldExecutor = executor;
        executor = _newExecutor;
        emit ExecutorUpdated(oldExecutor, _newExecutor);
    }
    
    /**
     * @notice Execute rebalancing via flash loan
     * @param params Rebalancing parameters
     */
    function executeRebalance(RebalanceParams calldata params) external onlyExecutor nonReentrant {
        require(params.user != address(0), "Invalid user");
        require(params.debtAmount > 0, "Invalid debt amount");
        
        // Encode rebalance params for flash loan callback
        bytes memory data = abi.encode(params);
        
        // Request flash loan from Aave V3
        IAaveV3Pool(POOL).flashLoanSimple(
            address(this),
            params.debtAsset,
            params.debtAmount,
            data,
            0 // referral code
        );
    }
    
    /**
     * @notice Flash loan callback - executes the rebalancing logic
     * @param asset The flash-loaned asset
     * @param amount The flash-loaned amount
     * @param premium The flash loan fee
     * @param initiator The initiator of the flash loan
     * @param params Encoded rebalancing parameters
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
        
        // Decode rebalancing parameters
        RebalanceParams memory rebalanceParams = abi.decode(params, (RebalanceParams));
        
        // Step 1: Repay user's debt using flash-loaned funds
        IERC20(asset).approve(POOL, amount);
        IAaveV3Pool(POOL).repay(
            asset,
            amount,
            2, // variable rate mode
            rebalanceParams.user
        );
        
        // Step 2: Withdraw user's collateral
        // Note: In production, this would require user approval or delegation
        // For demo, we assume the user has delegated credit to this contract
        
        // Step 3: Swap collateral to debt asset
        // Note: In production, integrate with DEX (Uniswap, 1inch, etc.)
        // For now, we assume sufficient balance to repay flash loan
        
        // Step 4: Repay flash loan + premium
        uint256 totalDebt = amount + premium;
        IERC20(asset).approve(POOL, totalDebt);
        
        emit RebalanceExecuted(
            rebalanceParams.user,
            rebalanceParams.collateralAsset,
            rebalanceParams.debtAsset,
            rebalanceParams.collateralAmount,
            amount,
            premium
        );
        
        return true;
    }
    
    /**
     * @notice Emergency withdraw tokens
     * @param token Token address
     * @param amount Amount to withdraw
     */
    function emergencyWithdraw(address token, uint256 amount) external onlyOwner {
        IERC20(token).safeTransfer(owner(), amount);
    }
    
    /**
     * @notice Emergency withdraw ETH
     */
    function emergencyWithdrawETH() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
    
    receive() external payable {}
}
