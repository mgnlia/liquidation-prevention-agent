# Demo Script - AI-Powered Liquidation Prevention Agent

## 🎬 2-Minute Demo Flow

### Scene 1: Introduction (15s)
**"Hi! I'm demonstrating an AI-powered agent that prevents DeFi liquidations before they happen."**

Show:
- Project README on screen
- Architecture diagram

### Scene 2: The Problem (20s)
**"Users lose billions to liquidations because they can't monitor positions 24/7. Current bots are reactive - they liquidate positions. We prevent liquidations proactively."**

Show:
- Statistics about DeFi liquidations
- Example of a liquidation event

### Scene 3: Smart Contracts (25s)
**"Our system has 4 key contracts deployed on Sepolia testnet:"**

Show Etherscan pages:
1. **LiquidationPrevention** - Main orchestrator
2. **AaveV3Adapter** - Monitors Aave positions & health factors
3. **CompoundV3Adapter** - Monitors Compound positions
4. **FlashLoanRebalancer** - Executes gas-efficient rebalancing via flash loans

**"Users register their positions once, and our AI monitors them continuously."**

### Scene 4: AI Agent in Action (40s)
**"The AI agent runs autonomously using Claude API for risk analysis."**

Show terminal with agent running:
```
🔄 MONITORING CYCLE - 2026-02-08 14:30:00
👥 Monitoring 3 registered users

📊 Checking position: 0x742d...
   Health Factor: 1.35
   Risk Level: HIGH
   ⚠️ Health factor below threshold. Rebalancing recommended.

💡 Claude's Strategy:
   Action: REPAY_DEBT
   Reasoning: Repay 30% of debt to improve health factor to 1.89
   Debt to Repay: $1,950
   Expected HF: 1.89
   Urgency: HIGH

⚡ EXECUTING REBALANCING NOW...
✅ Transaction sent: 0xabc123...
✅ Rebalancing successful! Health Factor improved to 1.91
```

**"The agent detected risk, Claude generated an optimal strategy, and executed it automatically using Aave V3 flash loans."**

### Scene 5: Dashboard (20s)
**"Users can monitor their positions in real-time through our dashboard."**

Show frontend:
- Connected wallet
- Current health factor: 1.91 (green, improved)
- Collateral & debt breakdown
- Recent rebalancing history
- AI decision log

### Scene 6: Key Innovation (15s)
**"What makes this unique:"**

Show slide:
1. ✅ **Predictive** - Uses AI to predict risk before liquidation
2. ✅ **Autonomous** - No user intervention needed
3. ✅ **Gas-Efficient** - Flash loans for zero-capital rebalancing
4. ✅ **Multi-Protocol** - Works with Aave, Compound, and more
5. ✅ **Transparent** - All AI decisions logged and explainable

### Scene 7: Technical Highlights (15s)
**"Built with cutting-edge tech:"**

Show code snippets:
- Solidity + Hardhat + OpenZeppelin
- Claude API for risk analysis
- LangGraph for agent orchestration
- The Graph for on-chain indexing
- React + Wagmi for frontend

### Scene 8: Impact & Closing (10s)
**"This prevents liquidations, saves users money, and makes DeFi safer for everyone. Thank you!"**

Show:
- GitHub repo: github.com/mgnlia/liquidation-prevention-agent
- Live demo: [URL]
- Deployed contracts: [Sepolia Etherscan links]

---

## 🎥 Recording Tips

### Setup Checklist
- [ ] Agent running with live monitoring
- [ ] Test user with position near liquidation threshold
- [ ] Dashboard showing real-time data
- [ ] Etherscan tabs open for all contracts
- [ ] Terminal with clean output
- [ ] Screen recording software ready (OBS, Loom)

### Screen Layout
```
┌─────────────────┬─────────────────┐
│   Terminal      │   Dashboard     │
│   (Agent)       │   (Frontend)    │
├─────────────────┼─────────────────┤
│   Etherscan     │   Code/Docs     │
│   (Contracts)   │   (GitHub)      │
└─────────────────┴─────────────────┘
```

### Voice-Over Script

**[0:00-0:15] Introduction**
"Hi everyone! I'm excited to show you our AI-Powered Liquidation Prevention Agent - a system that prevents DeFi liquidations before they happen, using Claude AI and smart contracts."

**[0:15-0:35] Problem Statement**
"Here's the problem: DeFi users lose billions to liquidations every year. Why? Because they can't monitor their positions 24/7. And current liquidation bots? They're reactive - they profit from liquidating you. We flip this model. Our AI agent protects you proactively."

**[0:35-1:00] Smart Contract Architecture**
"Let me show you our deployed contracts on Sepolia. We have four key components: The LiquidationPrevention orchestrator, adapters for Aave and Compound that monitor health factors, and a FlashLoanRebalancer that executes gas-efficient rebalancing. Users register once, and we monitor continuously."

**[1:00-1:40] AI Agent Demo**
"Now watch the AI in action. Here's our agent monitoring a position with a health factor of 1.35 - that's risky. The agent detects this, sends the data to Claude API, which analyzes the situation and generates an optimal strategy: repay 30% of debt to improve the health factor. The agent then executes this automatically using Aave V3 flash loans. And boom - health factor improved to 1.91. Position saved from liquidation."

**[1:40-2:00] Dashboard & Features**
"Users see everything in our dashboard - current health factor, collateral breakdown, and a complete log of all AI decisions. The system is transparent, autonomous, and works across multiple protocols."

**[2:00-2:15] Technical Stack**
"Built with Solidity and Hardhat, Claude API for AI reasoning, LangGraph for agent orchestration, and The Graph for indexing. All open source on GitHub."

**[2:15-2:30] Closing**
"This is more than a hackathon project - it's a real solution to a billion-dollar problem. By combining AI with DeFi, we're making the ecosystem safer for everyone. Check out the repo, test it on Sepolia, and let me know what you think. Thanks for watching!"

---

## 📸 Screenshots to Capture

1. **Architecture Diagram** - High-level system overview
2. **Etherscan Verified Contracts** - All 4 contracts with green checkmarks
3. **Agent Terminal** - Live monitoring cycle with risk detection
4. **Claude API Response** - Strategy generation JSON
5. **Transaction Success** - Etherscan tx showing rebalancing
6. **Dashboard Before/After** - Health factor improvement
7. **Code Highlights** - Key functions in contracts and agent
8. **Execution Log** - JSON file showing decision history

---

## 🎯 Key Messages to Emphasize

1. **Preventive, not reactive** - We save positions, not liquidate them
2. **AI-powered** - Claude analyzes risk and generates strategies
3. **Autonomous** - No user intervention needed
4. **Gas-efficient** - Flash loans enable zero-capital rebalancing
5. **Multi-protocol** - Works with Aave, Compound, expandable
6. **Production-ready** - Real contracts, real monitoring, real value

---

## 🔗 Links to Include

- **GitHub Repo**: https://github.com/mgnlia/liquidation-prevention-agent
- **Live Demo**: [Deploy to Vercel/Netlify]
- **Contracts (Sepolia)**:
  - LiquidationPrevention: 0x...
  - AaveV3Adapter: 0x...
  - CompoundV3Adapter: 0x...
  - FlashLoanRebalancer: 0x...
- **Documentation**: Full README and guides in repo
- **Video**: [Upload to YouTube/Loom]

---

## 🎬 Post-Production

1. Add captions for key technical terms
2. Highlight code sections as they're discussed
3. Add zoom effects on important UI elements
4. Include background music (subtle, professional)
5. Add title cards for each section
6. Include GitHub/Etherscan links as overlays
7. End with clear CTA: "Try it on Sepolia!"
