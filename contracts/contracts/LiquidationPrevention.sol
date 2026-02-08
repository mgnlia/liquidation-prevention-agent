// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./adapters/AaveV3Adapter.sol";
import "./adapters/CompoundV3Adapter.sol";
import "./FlashLoanRebalancer.sol";

/**
 * @title LiquidationPrevention
 * @notice Main orchestrator contract for AI-powered liquidation prevention
 * @dev Manages user registrations, monitoring, and coordinates rebalancing actions
 */
contract LiquidationPrevention is AccessControl, Pausable, ReentrancyGuard {
    bytes32 public constant AGENT_ROLE = keccak256("AGENT_ROLE");
    bytes32 public constant MONITOR_ROLE = keccak256("MONITOR_ROLE");
    
    AaveV3Adapter public immutable aaveAdapter;
    CompoundV3Adapter public immutable compoundAdapter;
    FlashLoanRebalancer public immutable rebalancer;
    
    // User registration tracking
    struct UserConfig {
        bool isRegistered;
        bool monitorAave;
        bool monitorCompound;
        uint256 minHealthFactor; // Minimum acceptable health factor (18 decimals)
        uint256 registeredAt;
        uint256 lastMonitored;
    }
    
    mapping(address => UserConfig) public userConfigs;
    address[] public registeredUsers;
    
    // Monitoring statistics
    struct MonitoringStats {
        uint256 totalMonitored;
        uint256 risksDetected;
        uint256 rebalancesExecuted;
        uint256 liquidationsPrevented;
    }
    
    MonitoringStats public stats;
    
    // Events
    event UserRegistered(
        address indexed user,
        bool monitorAave,
        bool monitorCompound,
        uint256 minHealthFactor,
        uint256 timestamp
    );
    
    event UserUnregistered(address indexed user, uint256 timestamp);
    
    event UserConfigUpdated(
        address indexed user,
        bool monitorAave,
        bool monitorCompound,
        uint256 minHealthFactor,
        uint256 timestamp
    );
    
    event MonitoringExecuted(
        address indexed user,
        string protocol,
        bool riskDetected,
        uint256 timestamp
    );
    
    event RebalanceRequested(
        address indexed user,
        string protocol,
        uint256 healthFactor,
        uint256 timestamp
    );

    /**
     * @notice Constructor
     * @param _aaveAdapter AaveV3Adapter contract address
     * @param _compoundAdapter CompoundV3Adapter contract address
     * @param _rebalancer FlashLoanRebalancer contract address
     */
    constructor(
        address _aaveAdapter,
        address _compoundAdapter,
        address _rebalancer
    ) {
        require(_aaveAdapter != address(0), "Invalid Aave adapter");
        require(_compoundAdapter != address(0), "Invalid Compound adapter");
        require(_rebalancer != address(0), "Invalid rebalancer");
        
        aaveAdapter = AaveV3Adapter(_aaveAdapter);
        compoundAdapter = CompoundV3Adapter(_compoundAdapter);
        rebalancer = FlashLoanRebalancer(_rebalancer);
        
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(AGENT_ROLE, msg.sender);
        _grantRole(MONITOR_ROLE, msg.sender);
    }

    /**
     * @notice Register user for liquidation prevention monitoring
     * @param monitorAave Enable Aave position monitoring
     * @param monitorCompound Enable Compound position monitoring
     * @param minHealthFactor Minimum acceptable health factor (18 decimals, e.g., 1.5e18 = 1.5)
     */
    function registerUser(
        bool monitorAave,
        bool monitorCompound,
        uint256 minHealthFactor
    ) external whenNotPaused {
        require(!userConfigs[msg.sender].isRegistered, "Already registered");
        require(monitorAave || monitorCompound, "Must monitor at least one protocol");
        require(minHealthFactor >= 1.2e18, "Min health factor too low");
        require(minHealthFactor <= 3e18, "Min health factor too high");
        
        userConfigs[msg.sender] = UserConfig({
            isRegistered: true,
            monitorAave: monitorAave,
            monitorCompound: monitorCompound,
            minHealthFactor: minHealthFactor,
            registeredAt: block.timestamp,
            lastMonitored: 0
        });
        
        registeredUsers.push(msg.sender);
        
        emit UserRegistered(
            msg.sender,
            monitorAave,
            monitorCompound,
            minHealthFactor,
            block.timestamp
        );
    }

    /**
     * @notice Unregister user from monitoring
     */
    function unregisterUser() external {
        require(userConfigs[msg.sender].isRegistered, "Not registered");
        
        userConfigs[msg.sender].isRegistered = false;
        
        emit UserUnregistered(msg.sender, block.timestamp);
    }

    /**
     * @notice Update user monitoring configuration
     * @param monitorAave Enable/disable Aave monitoring
     * @param monitorCompound Enable/disable Compound monitoring
     * @param minHealthFactor New minimum health factor
     */
    function updateUserConfig(
        bool monitorAave,
        bool monitorCompound,
        uint256 minHealthFactor
    ) external {
        require(userConfigs[msg.sender].isRegistered, "Not registered");
        require(monitorAave || monitorCompound, "Must monitor at least one protocol");
        require(minHealthFactor >= 1.2e18, "Min health factor too low");
        require(minHealthFactor <= 3e18, "Min health factor too high");
        
        userConfigs[msg.sender].monitorAave = monitorAave;
        userConfigs[msg.sender].monitorCompound = monitorCompound;
        userConfigs[msg.sender].minHealthFactor = minHealthFactor;
        
        emit UserConfigUpdated(
            msg.sender,
            monitorAave,
            monitorCompound,
            minHealthFactor,
            block.timestamp
        );
    }

    /**
     * @notice Monitor a specific user's positions (called by AI agent)
     * @param user Address of user to monitor
     */
    function monitorUser(address user) external onlyRole(MONITOR_ROLE) whenNotPaused {
        UserConfig storage config = userConfigs[user];
        require(config.isRegistered, "User not registered");
        
        bool riskDetected = false;
        
        // Monitor Aave position
        if (config.monitorAave) {
            (bool isAtRisk, uint256 healthFactor) = aaveAdapter.isPositionAtRisk(user);
            
            if (isAtRisk && healthFactor < config.minHealthFactor) {
                riskDetected = true;
                emit RebalanceRequested(user, "Aave", healthFactor, block.timestamp);
            }
            
            emit MonitoringExecuted(user, "Aave", isAtRisk, block.timestamp);
        }
        
        // Monitor Compound position
        if (config.monitorCompound) {
            (bool isAtRisk,) = compoundAdapter.isPositionAtRisk(user);
            
            if (isAtRisk) {
                riskDetected = true;
                emit RebalanceRequested(user, "Compound", 0, block.timestamp);
            }
            
            emit MonitoringExecuted(user, "Compound", isAtRisk, block.timestamp);
        }
        
        config.lastMonitored = block.timestamp;
        stats.totalMonitored++;
        
        if (riskDetected) {
            stats.risksDetected++;
        }
    }

    /**
     * @notice Batch monitor multiple users
     * @param users Array of user addresses to monitor
     */
    function monitorUsers(address[] calldata users)
        external
        onlyRole(MONITOR_ROLE)
        whenNotPaused
    {
        for (uint256 i = 0; i < users.length; i++) {
            if (userConfigs[users[i]].isRegistered) {
                this.monitorUser(users[i]);
            }
        }
    }

    /**
     * @notice Execute rebalancing for a user (called by AI agent after analysis)
     * @param user Address of user to rebalance
     * @param params Flash loan rebalancing parameters
     */
    function executeRebalance(
        address user,
        FlashLoanRebalancer.RebalanceParams calldata params
    ) external onlyRole(AGENT_ROLE) whenNotPaused nonReentrant {
        require(userConfigs[user].isRegistered, "User not registered");
        require(params.user == user, "User mismatch");
        
        // Execute flash loan rebalancing
        rebalancer.initiateRebalance(params);
        
        stats.rebalancesExecuted++;
        stats.liquidationsPrevented++;
    }

    /**
     * @notice Get total number of registered users
     * @return count Number of registered users
     */
    function getRegisteredUsersCount() external view returns (uint256 count) {
        return registeredUsers.length;
    }

    /**
     * @notice Get user configuration
     * @param user Address of user
     * @return config User configuration struct
     */
    function getUserConfig(address user) external view returns (UserConfig memory config) {
        return userConfigs[user];
    }

    /**
     * @notice Get monitoring statistics
     * @return MonitoringStats struct
     */
    function getStats() external view returns (MonitoringStats memory) {
        return stats;
    }

    /**
     * @notice Pause contract (emergency)
     */
    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    /**
     * @notice Unpause contract
     */
    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }
}
