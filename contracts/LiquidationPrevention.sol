// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./interfaces/IAaveAdapter.sol";
import "./interfaces/ICompoundAdapter.sol";
import "./FlashLoanRebalancer.sol";

/**
 * @title LiquidationPrevention
 * @notice Main contract orchestrating AI-powered liquidation prevention
 * @dev Integrates with Aave V3 and Compound V3 for position monitoring and rebalancing
 */
contract LiquidationPrevention is Ownable, ReentrancyGuard {
    
    // Protocol adapters
    IAaveAdapter public aaveAdapter;
    ICompoundAdapter public compoundAdapter;
    FlashLoanRebalancer public flashLoanRebalancer;
    
    // Authorized AI agents
    mapping(address => bool) public authorizedAgents;
    
    // User settings
    mapping(address => UserConfig) public userConfigs;
    
    struct UserConfig {
        bool autoRebalanceEnabled;
        uint256 minHealthFactor; // Minimum health factor before triggering rebalance (scaled by 1e18)
        uint256 targetHealthFactor; // Target health factor after rebalance (scaled by 1e18)
        bool aaveEnabled;
        bool compoundEnabled;
    }
    
    // Events
    event AgentAuthorized(address indexed agent, bool authorized);
    event UserConfigUpdated(address indexed user, uint256 minHealthFactor, uint256 targetHealthFactor);
    event RebalanceTriggered(address indexed user, string protocol, uint256 healthFactorBefore, uint256 healthFactorAfter);
    event EmergencyWithdraw(address indexed user, address token, uint256 amount);
    
    constructor(
        address _aaveAdapter,
        address _compoundAdapter,
        address _flashLoanRebalancer
    ) Ownable(msg.sender) {
        aaveAdapter = IAaveAdapter(_aaveAdapter);
        compoundAdapter = ICompoundAdapter(_compoundAdapter);
        flashLoanRebalancer = FlashLoanRebalancer(_flashLoanRebalancer);
    }
    
    /**
     * @notice Set user configuration for liquidation prevention
     * @param minHealthFactor Minimum health factor threshold (1.5e18 = 1.5)
     * @param targetHealthFactor Target health factor after rebalance (2.0e18 = 2.0)
     * @param enableAave Enable Aave monitoring
     * @param enableCompound Enable Compound monitoring
     */
    function setUserConfig(
        uint256 minHealthFactor,
        uint256 targetHealthFactor,
        bool enableAave,
        bool enableCompound
    ) external {
        require(minHealthFactor >= 1.1e18, "Min health factor too low");
        require(targetHealthFactor > minHealthFactor, "Target must be > min");
        require(targetHealthFactor <= 5e18, "Target health factor too high");
        
        userConfigs[msg.sender] = UserConfig({
            autoRebalanceEnabled: true,
            minHealthFactor: minHealthFactor,
            targetHealthFactor: targetHealthFactor,
            aaveEnabled: enableAave,
            compoundEnabled: enableCompound
        });
        
        emit UserConfigUpdated(msg.sender, minHealthFactor, targetHealthFactor);
    }
    
    /**
     * @notice Toggle auto-rebalance on/off
     */
    function toggleAutoRebalance(bool enabled) external {
        userConfigs[msg.sender].autoRebalanceEnabled = enabled;
    }
    
    /**
     * @notice Authorize/deauthorize an AI agent
     */
    function setAgentAuthorization(address agent, bool authorized) external onlyOwner {
        authorizedAgents[agent] = authorized;
        emit AgentAuthorized(agent, authorized);
    }
    
    /**
     * @notice Get user's health factor across all enabled protocols
     * @return aaveHealth Health factor on Aave (0 if not enabled)
     * @return compoundHealth Health factor on Compound (0 if not enabled)
     * @return lowestHealth The lowest health factor across protocols
     */
    function getUserHealthFactors(address user) 
        external 
        view 
        returns (
            uint256 aaveHealth,
            uint256 compoundHealth,
            uint256 lowestHealth
        ) 
    {
        UserConfig memory config = userConfigs[user];
        
        if (config.aaveEnabled) {
            aaveHealth = aaveAdapter.getHealthFactor(user);
        }
        
        if (config.compoundEnabled) {
            compoundHealth = compoundAdapter.getHealthFactor(user);
        }
        
        // Determine lowest health factor
        if (config.aaveEnabled && config.compoundEnabled) {
            lowestHealth = aaveHealth < compoundHealth ? aaveHealth : compoundHealth;
        } else if (config.aaveEnabled) {
            lowestHealth = aaveHealth;
        } else if (config.compoundEnabled) {
            lowestHealth = compoundHealth;
        }
    }
    
    /**
     * @notice Check if user needs rebalancing on any protocol
     * @return needsRebalance True if health factor below threshold
     * @return protocol Protocol that needs rebalancing ("aave" or "compound")
     * @return currentHealth Current health factor
     */
    function checkRebalanceNeeded(address user) 
        external 
        view 
        returns (
            bool needsRebalance,
            string memory protocol,
            uint256 currentHealth
        ) 
    {
        UserConfig memory config = userConfigs[user];
        
        if (!config.autoRebalanceEnabled) {
            return (false, "", 0);
        }
        
        // Check Aave
        if (config.aaveEnabled) {
            uint256 aaveHealth = aaveAdapter.getHealthFactor(user);
            if (aaveHealth > 0 && aaveHealth < config.minHealthFactor) {
                return (true, "aave", aaveHealth);
            }
        }
        
        // Check Compound
        if (config.compoundEnabled) {
            uint256 compoundHealth = compoundAdapter.getHealthFactor(user);
            if (compoundHealth > 0 && compoundHealth < config.minHealthFactor) {
                return (true, "compound", compoundHealth);
            }
        }
        
        return (false, "", 0);
    }
    
    /**
     * @notice Execute rebalancing for a user (called by authorized AI agent)
     * @param user User to rebalance
     * @param protocol Protocol to rebalance ("aave" or "compound")
     * @param rebalanceAmount Amount to rebalance
     * @param collateralAsset Collateral asset address
     * @param debtAsset Debt asset address
     */
    function executeRebalance(
        address user,
        string memory protocol,
        uint256 rebalanceAmount,
        address collateralAsset,
        address debtAsset
    ) external nonReentrant {
        require(authorizedAgents[msg.sender], "Not authorized agent");
        
        UserConfig memory config = userConfigs[user];
        require(config.autoRebalanceEnabled, "Auto-rebalance disabled");
        
        // Get health factor before
        uint256 healthBefore;
        if (keccak256(bytes(protocol)) == keccak256(bytes("aave"))) {
            require(config.aaveEnabled, "Aave not enabled");
            healthBefore = aaveAdapter.getHealthFactor(user);
        } else if (keccak256(bytes(protocol)) == keccak256(bytes("compound"))) {
            require(config.compoundEnabled, "Compound not enabled");
            healthBefore = compoundAdapter.getHealthFactor(user);
        } else {
            revert("Invalid protocol");
        }
        
        require(healthBefore < config.minHealthFactor, "Rebalance not needed");
        
        // Execute flash loan rebalance
        flashLoanRebalancer.executeRebalance(
            user,
            protocol,
            rebalanceAmount,
            collateralAsset,
            debtAsset
        );
        
        // Get health factor after
        uint256 healthAfter;
        if (keccak256(bytes(protocol)) == keccak256(bytes("aave"))) {
            healthAfter = aaveAdapter.getHealthFactor(user);
        } else {
            healthAfter = compoundAdapter.getHealthFactor(user);
        }
        
        emit RebalanceTriggered(user, protocol, healthBefore, healthAfter);
    }
    
    /**
     * @notice Emergency withdraw function for users
     */
    function emergencyWithdraw(address token, uint256 amount) external nonReentrant {
        // Implementation depends on how user funds are held
        // This is a safety mechanism
        emit EmergencyWithdraw(msg.sender, token, amount);
    }
}
