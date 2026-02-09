# 🎬 ETHDenver 2026 Demo Script

**Project:** AI-Powered Liquidation Prevention Agent  
**Track:** Futurllama (AI + Crypto + DePIN)  
**Duration:** 2-4 minutes

---

## 🎯 Demo Flow

### 1. Introduction (30 seconds)

**Script:**
> "Hi! I'm presenting the AI-Powered Liquidation Prevention Agent - an autonomous system that uses Claude AI to monitor DeFi positions and prevent liquidations before they happen. Every year, DeFi users lose millions to liquidations because they can't monitor their positions 24/7. Our agent solves this."

**Visual:** Show title slide with logo and problem statement

---

### 2. The Problem (30 seconds)

**Script:**
> "Here's the problem: You deposit $10,000 ETH as collateral on Aave, borrow $6,000 USDC. Your health factor is 1.66 - safe. But overnight, ETH drops 20%. Your health factor falls to 1.1. At 1.0, you get liquidated and lose 10% of your collateral. You were sleeping and didn't see it coming."

**Visual:** 
- Show simple diagram of collateral/debt
- Animate ETH price drop
- Show health factor declining toward liquidation

---

### 3. Our Solution (45 seconds)

**Script:**
> "Our agent continuously monitors your position. When it detects risk, it sends the data to Claude AI for analysis. Claude evaluates the urgency, market conditions, and recommends an action. If rebalancing is needed, the agent executes a flash loan to adjust your position - all automatically, in seconds."

**Visual:**
- Show architecture diagram
- Highlight: Monitor → Claude Analysis → Execute
- Show Claude's reasoning in real-time

**Demo the agent:**
```bash
# Terminal 1: Show agent running
python agent/main.py

# Output shows:
🤖 Starting Liquidation Prevention Agent on sepolia
🔍 Monitoring cycle...
👤 Checking user: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
⚠️  RISK DETECTED: aave - Health Factor: 1.15

🧠 Claude Analysis:
   Action: rebalance
   Urgency: high
   Reasoning: Health factor critically low at 1.15, approaching liquidation threshold...
```

---

### 4. Technical Deep Dive (45 seconds)

**Script:**
> "Under the hood, we integrate with Aave V3 and Compound V3 using custom adapters. When rebalancing is needed, we use Aave's flash loans - borrow funds with zero collateral, repay debt, withdraw and swap collateral, repay the flash loan. All in one atomic transaction. The system is deployed on Sepolia, Base, and Arbitrum testnets."

**Visual:**
- Show contract architecture
- Animate flash loan flow diagram
- Show verified contracts on Etherscan

**Show code snippet:**
```solidity
// FlashLoanRebalancer.sol
function executeRebalance(
    address user,
    string memory protocol,
    uint256 amount
) external {
    // Flash borrow from Aave
    POOL.flashLoanSimple(
        address(this),
        debtAsset,
        amount,
        params,
        0
    );
}
```

---

### 5. Live Demo (30 seconds)

**Script:**
> "Let me show you the dashboard. Here's a user with declining health factor. The agent detected it, Claude analyzed it, and recommended rebalancing. Watch as the transaction executes... Success! Health factor restored to 2.05. Liquidation prevented."

**Visual:**
- Show React dashboard
- Real-time health factor chart
- Show transaction on Etherscan
- Confetti animation on success ✨

---

### 6. Futurllama Track Alignment (20 seconds)

**Script:**
> "For the Futurllama track, we demonstrate: autonomous AI agents making real financial decisions, multi-chain infrastructure supporting cross-chain positions, and transparent AI attribution - every Claude decision is logged for auditability. This is production-ready AI for DeFi."

**Visual:** Show ai-attribution.jsonl file

---

### 7. Closing (10 seconds)

**Script:**
> "The code is open source, fully tested, and deployed on testnet. Check out the repo and docs. Thank you!"

**Visual:** 
- Show GitHub repo
- QR code for repo
- Contact info

---

## 🎥 Recording Tips

### Setup Checklist
- [ ] Agent running on testnet with real positions
- [ ] Dashboard open in browser
- [ ] Terminal with agent logs visible
- [ ] Etherscan tab ready
- [ ] Slides prepared
- [ ] Screen recording software ready (OBS/Loom)
- [ ] Test audio/video quality

### Camera Setup
- Use 1080p minimum
- Good lighting
- Clean background
- Professional attire

### Screen Layout
```
┌─────────────────────────────────────┐
│  Webcam (bottom right corner)       │
│                                      │
│  ┌──────────┐  ┌──────────┐        │
│  │Dashboard │  │ Terminal  │        │
│  │          │  │  Logs     │        │
│  └──────────┘  └──────────┘        │
└─────────────────────────────────────┘
```

### Timing Breakdown
- 0:00-0:30 - Intro
- 0:30-1:00 - Problem
- 1:00-1:45 - Solution + Agent Demo
- 1:45-2:30 - Technical Deep Dive
- 2:30-3:00 - Live Demo
- 3:00-3:20 - Futurllama Alignment
- 3:20-3:30 - Closing

---

## 🎬 Demo Scenarios

### Scenario A: Successful Rebalancing
1. User has HF 1.15 on Aave
2. Agent detects risk
3. Claude recommends rebalancing $1,500
4. Transaction executes
5. HF restored to 2.05 ✅

### Scenario B: Monitoring (No Action)
1. User has HF 1.8 on Compound
2. Agent detects minor risk
3. Claude recommends continued monitoring
4. No transaction needed
5. Position remains stable ✅

### Scenario C: Multi-Chain
1. User has positions on Sepolia + Base
2. Agent monitors both chains
3. Base position at risk
4. Rebalances on Base
5. Sepolia position unaffected ✅

---

## 📊 Metrics to Highlight

- **Response Time:** < 30 seconds from detection to execution
- **Success Rate:** 100% on testnet (X successful rebalances)
- **Gas Efficiency:** ~$5-10 per rebalance (flash loan fees)
- **Multi-Chain:** 3 testnets supported
- **AI Decisions:** All logged with full transparency

---

## 🚨 Troubleshooting

### If Agent Fails
- Show fallback rule-based logic
- Explain redundancy built-in
- Highlight error handling

### If Transaction Fails
- Show simulation results
- Explain why (e.g., insufficient liquidity)
- Show retry mechanism

### If Demo Crashes
- Have backup recording ready
- Show GitHub repo as fallback
- Walk through code instead

---

## 🎯 Key Messages

1. **Real Problem:** Liquidations cost users millions
2. **AI Solution:** Claude makes intelligent decisions
3. **Production Ready:** Tested, deployed, documented
4. **Multi-Chain:** Works across Ethereum L2s
5. **Transparent:** All AI decisions logged
6. **Open Source:** Available for community use

---

## 📝 Q&A Prep

**Q: How do you handle gas costs?**  
A: Flash loans are capital-efficient. Users only pay ~0.09% fee + gas. We're exploring gas sponsorship for high-value positions.

**Q: What if Claude API is down?**  
A: We have fallback rule-based logic that triggers rebalancing at critical thresholds (HF < 1.15).

**Q: Can this work on mainnet?**  
A: Yes! All protocols used (Aave V3, flash loans) are production-ready. We're on testnet for the hackathon but mainnet deployment is straightforward.

**Q: How do you prevent malicious rebalancing?**  
A: Users must opt-in and set their own thresholds. Agent is authorized per-user. All actions are on-chain and auditable.

**Q: What about other protocols?**  
A: Architecture is modular. Adding Maker, Morpho, etc. is just creating new adapters. Roadmap item!

---

## 🎬 Final Checklist

Before recording:
- [ ] Test full flow end-to-end
- [ ] Verify all contracts on Etherscan
- [ ] Check Claude API quota
- [ ] Prepare backup scenarios
- [ ] Review script 3x times
- [ ] Test screen recording
- [ ] Clear browser history/tabs
- [ ] Close distracting apps
- [ ] Charge laptop
- [ ] Good internet connection

**Let's win this! 🏆**
