// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./adapters/AaveV3Adapter.sol";
import "./adapters/CompoundV3Adapter.sol";
import "./FlashLoanRebalancer.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title LiquidationPrevention
 * @notice Main orchestrator contract for AI-powered liquidation prevention
 * @dev Coordinates monitoring, risk analysis, and automated rebalancing
 */
contract LiquidationPrevention is Ownable, ReentrancyGuard {
    // Protocol adapters
    AaveV3Adapter public aaveAdapter;
    CompoundV3Adapter public compoundAdapter;
    FlashLoanRebalancer public rebalancer;
    
    // AI agent address
    address public aiAgent;
    
    // User registration
    mapping(address => bool) public registeredUsers;
    mapping(address => Protocol[]) public userProtocols;
    
    enum Protocol {
        AAVE_V3,
        COMPOUND_V3
    }
    
    // Events
    event UserRegistered(address indexed user, Protocol[] protocols);
    event UserUnregistered(address indexed user);
    event PositionMonitored(address indexed user, Protocol protocol, uint256 timestamp);
    event RebalanceTriggered(address indexed user, Protocol protocol, uint256 timestamp);
    event AIAgentUpdated(address indexed oldAgent, address indexed newAgent);
    
    // Errors
    error UnauthorizedAgent();
    error UserNotRegistered();
    error UserAlreadyRegistered();
    
    modifier onlyAIAgent() {
        if (msg.sender != aiAgent && msg.sender != owner()) {
            revert UnauthorizedAgent();
        }
        _;
    }
    
    constructor(
        address _aaveAdapter,
        address _compoundAdapter,
        address _rebalancer,
        address _aiAgent
    ) Ownable(msg.sender) {
        require(_aaveAdapter != address(0), "Invalid Aave adapter");
        require(_compoundAdapter != address(0), "Invalid Compound adapter");
        require(_rebalancer != address(0), "Invalid rebalancer");
        require(_aiAgent != address(0), "Invalid AI agent");
        
        aaveAdapter = AaveV3Adapter(_aaveAdapter);
        compoundAdapter = CompoundV3Adapter(_compoundAdapter);
        rebalancer = FlashLoanRebalancer(_rebalancer);
        aiAgent = _aiAgent;
    }
    
    /**
     * @notice Register user for monitoring
     * @param protocols Array of protocols to monitor
     */
    function registerUser(Protocol[] calldata protocols) external {
        if (registeredUsers[msg.sender]) {
            revert UserAlreadyRegistered();
        }
        
        registeredUsers[msg.sender] = true;
        
        for (uint256 i = 0; i < protocols.length; i++) {
            userProtocols[msg.sender].push(protocols[i]);
        }
        
        emit UserRegistered(msg.sender, protocols);
    }
    
    /**
     * @notice Unregister user from monitoring
     */
    function unregisterUser() external {
        if (!registeredUsers[msg.sender]) {
            revert UserNotRegistered();
        }
        
        registeredUsers[msg.sender] = false;
        delete userProtocols[msg.sender];
        
        emit UserUnregistered(msg.sender);
    }
    
    /**
     * @notice Get user's registration status
     * @param user User address
     * @return isRegistered Registration status
     * @return protocols Monitored protocols
     */
    function getUserInfo(address user) external view returns (bool isRegistered, Protocol[] memory protocols) {
        return (registeredUsers[user], userProtocols[user]);
    }
    
    /**
     * @notice Monitor user's position across all registered protocols
     * @param user User address
     */
    function monitorUser(address user) external onlyAIAgent {
        if (!registeredUsers[user]) {
            revert UserNotRegistered();
        }
        
        Protocol[] memory protocols = userProtocols[user];
        
        for (uint256 i = 0; i < protocols.length; i++) {
            if (protocols[i] == Protocol.AAVE_V3) {
                aaveAdapter.monitorPosition(user);
                emit PositionMonitored(user, Protocol.AAVE_V3, block.timestamp);
            } else if (protocols[i] == Protocol.COMPOUND_V3) {
                compoundAdapter.monitorPosition(user);
                emit PositionMonitored(user, Protocol.COMPOUND_V3, block.timestamp);
            }
        }
    }
    
    /**
     * @notice Batch monitor multiple users
     * @param users Array of user addresses
     */
    function monitorUsersBatch(address[] calldata users) external onlyAIAgent {
        for (uint256 i = 0; i < users.length; i++) {
            if (registeredUsers[users[i]]) {
                Protocol[] memory protocols = userProtocols[users[i]];
                
                for (uint256 j = 0; j < protocols.length; j++) {
                    if (protocols[j] == Protocol.AAVE_V3) {
                        aaveAdapter.monitorPosition(users[i]);
                        emit PositionMonitored(users[i], Protocol.AAVE_V3, block.timestamp);
                    } else if (protocols[j] == Protocol.COMPOUND_V3) {
                        compoundAdapter.monitorPosition(users[i]);
                        emit PositionMonitored(users[i], Protocol.COMPOUND_V3, block.timestamp);
                    }
                }
            }
        }
    }
    
    /**
     * @notice Get Aave health factor for user
     * @param user User address
     * @return healthFactor Health factor
     */
    function getAaveHealthFactor(address user) external view returns (uint256 healthFactor) {
        return aaveAdapter.getHealthFactor(user);
    }
    
    /**
     * @notice Check if Aave position is at risk
     * @param user User address
     * @return isAtRisk Risk status
     * @return healthFactor Health factor
     */
    function isAavePositionAtRisk(address user) external view returns (bool isAtRisk, uint256 healthFactor) {
        return aaveAdapter.isPositionAtRisk(user);
    }
    
    /**
     * @notice Check if Compound position is at risk
     * @param user User address
     * @return isAtRisk Risk status
     */
    function isCompoundPositionAtRisk(address user) external view returns (bool isAtRisk) {
        return compoundAdapter.isPositionAtRisk(user);
    }
    
    /**
     * @notice Trigger rebalancing for user (called by AI agent)
     * @param params Rebalancing parameters
     */
    function triggerRebalance(FlashLoanRebalancer.RebalanceParams calldata params) 
        external 
        onlyAIAgent 
        nonReentrant 
    {
        if (!registeredUsers[params.user]) {
            revert UserNotRegistered();
        }
        
        rebalancer.executeRebalance(params);
        
        emit RebalanceTriggered(params.user, Protocol.AAVE_V3, block.timestamp);
    }
    
    /**
     * @notice Update AI agent address
     * @param _newAgent New AI agent address
     */
    function setAIAgent(address _newAgent) external onlyOwner {
        require(_newAgent != address(0), "Invalid AI agent");
        address oldAgent = aiAgent;
        aiAgent = _newAgent;
        emit AIAgentUpdated(oldAgent, _newAgent);
    }
    
    /**
     * @notice Update protocol adapters
     * @param _aaveAdapter New Aave adapter
     * @param _compoundAdapter New Compound adapter
     */
    function updateAdapters(address _aaveAdapter, address _compoundAdapter) external onlyOwner {
        require(_aaveAdapter != address(0), "Invalid Aave adapter");
        require(_compoundAdapter != address(0), "Invalid Compound adapter");
        
        aaveAdapter = AaveV3Adapter(_aaveAdapter);
        compoundAdapter = CompoundV3Adapter(_compoundAdapter);
    }
    
    /**
     * @notice Update rebalancer
     * @param _rebalancer New rebalancer address
     */
    function updateRebalancer(address _rebalancer) external onlyOwner {
        require(_rebalancer != address(0), "Invalid rebalancer");
        rebalancer = FlashLoanRebalancer(_rebalancer);
    }
}
