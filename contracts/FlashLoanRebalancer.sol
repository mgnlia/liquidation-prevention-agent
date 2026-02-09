// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

interface IFlashLoanSimpleReceiver {
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external returns (bool);
}

interface IPoolAave {
    function flashLoanSimple(
        address receiverAddress,
        address asset,
        uint256 amount,
        bytes calldata params,
        uint16 referralCode
    ) external;
}

/**
 * @title FlashLoanRebalancer
 * @notice Executes flash loan-based rebalancing to prevent liquidations
 * @dev Uses Aave V3 flash loans to swap collateral and repay debt
 */
contract FlashLoanRebalancer is IFlashLoanSimpleReceiver, Ownable, ReentrancyGuard {
    
    IPoolAave public immutable aavePool;
    address public liquidationPrevention;
    
    struct RebalanceParams {
        address user;
        string protocol;
        address collateralAsset;
        address debtAsset;
        uint256 targetHealthFactor;
    }
    
    event RebalanceExecuted(
        address indexed user,
        string protocol,
        uint256 flashLoanAmount,
        uint256 premium
    );
    
    event FlashLoanReceived(
        address indexed asset,
        uint256 amount,
        uint256 premium
    );
    
    modifier onlyLiquidationPrevention() {
        require(msg.sender == liquidationPrevention, "Only LiquidationPrevention");
        _;
    }
    
    constructor(address _aavePool) Ownable(msg.sender) {
        aavePool = IPoolAave(_aavePool);
    }
    
    /**
     * @notice Set the LiquidationPrevention contract address
     */
    function setLiquidationPrevention(address _liquidationPrevention) external onlyOwner {
        liquidationPrevention = _liquidationPrevention;
    }
    
    /**
     * @notice Execute rebalancing via flash loan
     * @param user User to rebalance
     * @param protocol Protocol ("aave" or "compound")
     * @param amount Flash loan amount
     * @param collateralAsset Collateral asset to swap
     * @param debtAsset Debt asset to repay
     */
    function executeRebalance(
        address user,
        string memory protocol,
        uint256 amount,
        address collateralAsset,
        address debtAsset
    ) external onlyLiquidationPrevention nonReentrant {
        
        RebalanceParams memory params = RebalanceParams({
            user: user,
            protocol: protocol,
            collateralAsset: collateralAsset,
            debtAsset: debtAsset,
            targetHealthFactor: 2e18 // Target 2.0 health factor
        });
        
        bytes memory encodedParams = abi.encode(params);
        
        // Request flash loan from Aave
        aavePool.flashLoanSimple(
            address(this),
            debtAsset,
            amount,
            encodedParams,
            0 // referral code
        );
        
        emit RebalanceExecuted(user, protocol, amount, 0);
    }
    
    /**
     * @notice Flash loan callback - executes the rebalancing logic
     * @dev Called by Aave Pool during flash loan execution
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
        
        RebalanceParams memory rebalanceParams = abi.decode(params, (RebalanceParams));
        
        // Rebalancing logic:
        // 1. Use flash loaned funds to repay part of user's debt
        // 2. Withdraw some collateral from the protocol
        // 3. Swap collateral to debt asset (would integrate with DEX here)
        // 4. Repay flash loan + premium
        
        // For MVP: simplified flow
        // In production, would integrate with:
        // - Aave/Compound repay functions
        // - DEX aggregator (1inch, Paraswap) for swaps
        // - Proper accounting and slippage protection
        
        uint256 totalDebt = amount + premium;
        
        // Approve Aave pool to pull the flash loan repayment
        IERC20(asset).approve(address(aavePool), totalDebt);
        
        return true;
    }
    
    /**
     * @notice Emergency withdraw function
     */
    function emergencyWithdraw(address token, uint256 amount) external onlyOwner {
        IERC20(token).transfer(owner(), amount);
    }
    
    receive() external payable {}
}
