# 🏆 HackMoney 2026 Submission Checklist

**Project:** AI-Powered Liquidation Prevention Agent  
**Repository:** https://github.com/mgnlia/liquidation-prevention-agent  
**Deadline:** February 11, 2026

---

## 📋 Pre-Submission Requirements

### Environment Setup
- [ ] Sepolia testnet ETH obtained (0.5+ ETH)
  - Faucet 1: https://sepoliafaucet.com/
  - Faucet 2: https://www.alchemy.com/faucets/ethereum-sepolia
  - Faucet 3: https://faucet.quicknode.com/ethereum/sepolia
- [ ] Alchemy/Infura Sepolia RPC URL configured
- [ ] Deployer wallet private key secured
- [ ] Agent wallet private key secured (separate from deployer)
- [ ] Etherscan API key obtained
- [ ] Anthropic Claude API key obtained

### Code Verification
- [ ] All contracts compile: `npx hardhat compile`
- [ ] All tests pass: `npx hardhat test`
- [ ] Agent dependencies installed: `pip install -r requirements.txt`
- [ ] Frontend builds: `cd frontend && npm run build`
- [ ] No console errors or warnings
- [ ] Git history is clean (small, meaningful commits)

---

## 🚀 Deployment Steps

### 1. Deploy Smart Contracts
- [ ] Configure `contracts/.env` with all required variables
- [ ] Run deployment: `npx hardhat run scripts/deploy.js --network sepolia`
- [ ] Save deployment addresses from output
- [ ] Verify deployment was successful (4 contracts deployed)
- [ ] Check deployer balance after deployment (should have remaining ETH)

**Expected Output:**
```
✅ AaveV3Adapter deployed to: 0x...
✅ CompoundV3Adapter deployed to: 0x...
✅ FlashLoanRebalancer deployed to: 0x...
✅ LiquidationPrevention deployed to: 0x...
```

### 2. Verify Contracts on Etherscan
- [ ] Run verification: `npx hardhat run scripts/verify.js --network sepolia`
- [ ] Confirm all 4 contracts show "Verified" on Etherscan
- [ ] Check contract source code is readable on Etherscan
- [ ] Test "Read Contract" and "Write Contract" tabs work

**Verification URLs:**
- [ ] LiquidationPrevention: https://sepolia.etherscan.io/address/0x...#code
- [ ] AaveV3Adapter: https://sepolia.etherscan.io/address/0x...#code
- [ ] CompoundV3Adapter: https://sepolia.etherscan.io/address/0x...#code
- [ ] FlashLoanRebalancer: https://sepolia.etherscan.io/address/0x...#code

### 3. Configure AI Agent
- [ ] Update `agent/.env` with deployed contract addresses
- [ ] Configure Claude API key
- [ ] Set agent wallet private key
- [ ] Configure RPC endpoint
- [ ] Test agent wallet has sufficient balance (0.1+ ETH)

### 4. Test Agent Functionality
- [ ] Start agent: `python agent.py`
- [ ] Verify agent initializes without errors
- [ ] Check agent connects to contracts successfully
- [ ] Confirm monitoring cycle runs (even with no users)
- [ ] Test Claude API integration works

**Expected Console Output:**
```
🤖 Initializing AI Liquidation Prevention Agent...
✅ Agent initialized successfully
🚀 LIQUIDATION PREVENTION AGENT STARTING
💰 Agent Wallet: 0x...
   Balance: 0.5000 ETH
⏱️  Monitor Interval: 60s
```

### 5. Create Test Position (Optional but Recommended)
- [ ] Visit Aave V3 Sepolia: https://app.aave.com/?marketName=proto_sepolia_v3
- [ ] Get test tokens from faucet: https://staging.aave.com/faucet/
- [ ] Supply collateral (e.g., 1 ETH)
- [ ] Borrow stablecoins (e.g., 500 USDC)
- [ ] Register position for monitoring via frontend or contract call
- [ ] Verify agent detects and monitors position

---

## 🎬 Demo Video Requirements

### Recording Setup
- [ ] Screen recording software ready (OBS Studio/Loom/QuickTime)
- [ ] Microphone tested (clear audio, no background noise)
- [ ] Recording resolution: 1080p or 720p minimum
- [ ] Browser tabs prepared in order:
  1. GitHub repository
  2. Aave V3 Sepolia (showing position)
  3. Frontend dashboard
  4. Agent terminal
  5. Etherscan transactions
  6. Architecture diagram

### Demo Script
- [ ] Follow DEMO.md script structure
- [ ] Duration: 2-4 minutes (not longer!)
- [ ] Show problem → solution → execution → results
- [ ] Highlight sponsor integrations (Aave, Claude, The Graph)
- [ ] Speak clearly and at normal pace (NO speed-ups)
- [ ] Use your own voice (NO text-to-speech)
- [ ] Include call-to-action (GitHub repo link)

### Demo Content Checklist
- [ ] **Intro** (15s): Project name, problem statement
- [ ] **Problem** (20s): Show at-risk position on Aave
- [ ] **Registration** (30s): Demonstrate user registration flow
- [ ] **AI Monitoring** (45s): Show agent terminal with Claude analysis
- [ ] **Execution** (45s): Show Etherscan transaction and results
- [ ] **Technical** (30s): Highlight architecture and integrations
- [ ] **Closing** (15s): GitHub link and thank you

### Video Quality Check
- [ ] Audio is clear and understandable
- [ ] Screen is readable (text not too small)
- [ ] No personal information visible (private keys, emails, etc.)
- [ ] Smooth transitions between sections
- [ ] Professional presentation (no errors or stuttering)
- [ ] File format: MP4 (H.264 codec recommended)
- [ ] File size: Under 500MB

### Upload & Hosting
- [ ] Upload to YouTube (unlisted or public)
- [ ] Test video plays correctly
- [ ] Copy video URL for submission
- [ ] (Optional) Upload to Loom/Vimeo as backup

---

## 📝 Submission Platform

### ETHGlobal HackMoney 2026
**URL:** https://ethglobal.com/events/hackmoney2026

### Required Information
- [ ] Project name: "AI-Powered Liquidation Prevention Agent"
- [ ] Tagline: "Autonomous AI agent preventing DeFi liquidations using Aave flash loans and Claude API"
- [ ] GitHub repository URL
- [ ] Demo video URL (YouTube/Loom)
- [ ] Live demo URL (if deployed frontend)
- [ ] Team members listed
- [ ] Technologies used selected
- [ ] Sponsor prizes selected (max 3):
  - [ ] Aave Grants DAO
  - [ ] Anthropic
  - [ ] The Graph

### Project Description
```
An AI-powered autonomous agent that monitors DeFi positions across Aave V3 and Compound V3, 
using Claude API for intelligent risk analysis and Aave flash loans for capital-efficient 
rebalancing. The agent prevents liquidations before they happen by proactively executing 
rebalancing strategies, protecting billions in user funds.

Key Features:
• Real-time position monitoring via The Graph
• Claude-powered risk analysis and strategy generation
• Automated flash loan rebalancing (zero capital required)
• Support for Aave V3 and Compound V3
• Production-ready with comprehensive tests and docs

Tech Stack: Solidity, Hardhat, OpenZeppelin, Python, LangGraph, Claude API, The Graph, React
```

### Deployed Contracts (Sepolia)
- [ ] LiquidationPrevention: 0x...
- [ ] AaveV3Adapter: 0x...
- [ ] CompoundV3Adapter: 0x...
- [ ] FlashLoanRebalancer: 0x...

### Links to Include
- [ ] GitHub: https://github.com/mgnlia/liquidation-prevention-agent
- [ ] Etherscan (main contract): https://sepolia.etherscan.io/address/0x...
- [ ] Demo video: [YouTube URL]
- [ ] Live demo: [Frontend URL if deployed]
- [ ] Documentation: Link to README.md

---

## 🎯 Sponsor Prize Requirements

### Aave Grants DAO
- [ ] Uses Aave V3 flash loans
- [ ] Implements IPool interface
- [ ] Monitors health factors
- [ ] Novel use case (prevention vs liquidation)
- [ ] Production-ready code
- [ ] Comprehensive documentation

### Anthropic
- [ ] Integrates Claude API
- [ ] Demonstrates autonomous reasoning
- [ ] Complex decision-making (multi-factor analysis)
- [ ] Clear AI attribution in docs/AI_ATTRIBUTION.md
- [ ] Showcases Claude's capabilities

### The Graph
- [ ] Deploys subgraph for position indexing
- [ ] Uses GraphQL queries for data fetching
- [ ] Event-driven architecture
- [ ] Efficient on-chain data access
- [ ] Documentation of subgraph usage

---

## ✅ Final Checks

### GitHub Repository
- [ ] README.md is comprehensive and clear
- [ ] All code is pushed to main branch
- [ ] No sensitive data in repo (keys, passwords)
- [ ] LICENSE file included (MIT)
- [ ] .gitignore properly configured
- [ ] Clean commit history (meaningful messages)
- [ ] All links in README work
- [ ] Badges added (if applicable)

### Documentation
- [ ] DEPLOYMENT.md complete
- [ ] DEMO.md script ready
- [ ] QUICKSTART.md tested
- [ ] AI_ATTRIBUTION.md filled out
- [ ] ARCHITECTURE.md explains design
- [ ] All docs have correct links

### Code Quality
- [ ] No console.log or debug statements
- [ ] Code is commented where necessary
- [ ] Error handling implemented
- [ ] Input validation on all functions
- [ ] Gas optimization considered
- [ ] Security best practices followed

### Testing
- [ ] Unit tests for smart contracts
- [ ] Integration tests for agent
- [ ] All tests pass
- [ ] Test coverage documented
- [ ] Edge cases handled

---

## 🚨 Common Pitfalls to Avoid

- [ ] ❌ Don't submit with unverified contracts
- [ ] ❌ Don't use text-to-speech in demo video
- [ ] ❌ Don't speed up demo video excessively
- [ ] ❌ Don't exceed 4-minute video length
- [ ] ❌ Don't include private keys in screenshots
- [ ] ❌ Don't submit without testing deployment
- [ ] ❌ Don't forget to select sponsor prizes
- [ ] ❌ Don't use Lorem Ipsum or placeholder text
- [ ] ❌ Don't submit with broken links
- [ ] ❌ Don't skip the demo video

---

## 📊 Submission Metrics

### Target Metrics to Highlight
- **Response Time:** <60s from risk detection to execution
- **Gas Efficiency:** ~300k gas per rebalancing transaction
- **Uptime:** 24/7 autonomous monitoring
- **Accuracy:** Tested against historical liquidation data
- **Coverage:** Aave V3 + Compound V3 (expandable)

### Innovation Points
- First AI agent using flash loans for liquidation prevention
- Autonomous decision-making with Claude API
- Zero capital required for rebalancing
- Production-ready with comprehensive tests
- Modular architecture for protocol expansion

---

## 🎉 Post-Submission

- [ ] Confirm submission received (check email)
- [ ] Share on Twitter with #HackMoney2026
- [ ] Post in ETHGlobal Discord
- [ ] Monitor submission status
- [ ] Prepare for potential judging Q&A
- [ ] Keep agent running for live demos

---

## 📞 Support Contacts

**ETHGlobal Support:** support@ethglobal.com  
**Discord:** ETHGlobal Discord #hackmoney-2026  
**Documentation:** https://ethglobal.com/help

---

## ⏰ Timeline

**Target Submission:** February 10, 2026 (1 day before deadline)  
**Deadline:** February 11, 2026 23:59 UTC  
**Results:** February 15-18, 2026 (estimated)

---

**GOOD LUCK! 🍀 LET'S WIN THIS! 🏆**
