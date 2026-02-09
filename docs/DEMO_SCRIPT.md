# 🎬 Demo Script for ETHDenver 2026

**Duration**: 3-4 minutes  
**Target**: Judges, developers, DeFi users  
**Goal**: Show autonomous AI preventing liquidations in real-time

## 📋 Pre-Demo Setup

### Required:
- ✅ Contracts deployed to Sepolia
- ✅ Agent running and monitoring
- ✅ Frontend dashboard live
- ✅ Test wallet with Aave position
- ✅ Screen recording software ready

### Test Position Setup:
1. Connect wallet to Aave Sepolia
2. Supply 1 ETH as collateral
3. Borrow 0.5 ETH worth of USDC
4. Health factor: ~1.8 (safe)

## 🎥 Video Script

### Opening (0:00 - 0:30)

**[Screen: Title slide with logo]**

> "Hi! I'm demonstrating our AI-Powered Liquidation Prevention Agent - an autonomous system that protects DeFi users from losing their collateral to liquidations."

**[Screen: Problem visualization - liquidation stats]**

> "In 2024 alone, DeFi users lost over $500 million to liquidations. Our solution uses Claude AI to monitor positions 24/7 and automatically rebalance before liquidation occurs."

### Architecture Overview (0:30 - 1:00)

**[Screen: Architecture diagram]**

> "Here's how it works: Our AI agent continuously monitors user positions across Aave and Compound. When a position becomes risky, Claude AI analyzes the situation and recommends an action. If rebalancing is needed, the agent executes it autonomously using flash loans."

**[Highlight each component as you mention it]**

> "The system has three layers:
> 1. Smart contracts on Ethereum, Base, and Arbitrum
> 2. AI agent powered by Claude 3.5 Sonnet
> 3. Real-time dashboard for monitoring"

### Live Demo - Part 1: Monitoring (1:00 - 1:45)

**[Screen: Dashboard showing healthy position]**

> "Let me show you this in action. Here's a test wallet with a position on Aave. Currently, the health factor is 1.8 - that's healthy."

**[Screen: Agent terminal logs]**

> "In the background, our agent is monitoring this position every 60 seconds."

**[Show terminal output:]**
```
🔍 Monitoring cycle at 2026-02-15T10:30:00
👤 Checking user: 0x742d35Cc...
✅ Position healthy - Health Factor: 1.80
```

> "The agent checks the health factor, and since it's above our threshold of 1.5, no action is needed."

### Live Demo - Part 2: Risk Detection (1:45 - 2:30)

**[Screen: Simulate price drop or manually adjust position]**

> "Now, let's simulate what happens when the collateral value drops. I'm going to trigger a position that becomes risky."

**[Show health factor dropping to 1.3]**

> "The health factor just dropped to 1.3 - this is now in the danger zone."

**[Screen: Agent detects risk]**

**[Show terminal output:]**
```
🔍 Monitoring cycle at 2026-02-15T10:31:00
👤 Checking user: 0x742d35Cc...
⚠️  RISK DETECTED: aave - Health Factor: 1.30

🧠 Claude Analysis:
   Action: rebalance
   Urgency: high
   Reasoning: Health factor below safe threshold. 
              Recommend immediate rebalancing to prevent liquidation.
              Market volatility suggests proactive action.
   
🔄 Executing rebalance...
```

> "The agent immediately detects the risk and sends the position data to Claude for analysis. Claude recommends rebalancing because the health factor is too close to the liquidation threshold."

### Live Demo - Part 3: Autonomous Rebalancing (2:30 - 3:15)

**[Screen: Transaction executing]**

> "Watch as the agent autonomously executes the rebalancing using a flash loan."

**[Show terminal output:]**
```
🔄 Executing rebalance for 0x742d35Cc...
   1. Flash borrowing 500 USDC from Aave
   2. Repaying user debt
   3. Withdrawing collateral
   4. Swapping to repay flash loan
   
✅ Rebalance successful!
   Tx: 0xabc123...
   New Health Factor: 2.05
   Cost: 0.0015 ETH (gas) + 0.45 USDC (flash loan fee)
```

**[Screen: Dashboard showing updated position]**

> "And just like that, the health factor is back to 2.05 - the position is safe again. The entire process took less than 30 seconds and cost only $5 in gas and fees."

**[Screen: Etherscan showing transaction]**

> "Here's the transaction on Etherscan - completely transparent and verifiable."

### Unique Features (3:15 - 3:45)

**[Screen: Multi-chain dashboard]**

> "What makes this special for the Futurllama track?"

> "First, it's truly autonomous - Claude AI makes intelligent decisions based on market conditions, not just simple rules."

**[Screen: Show multi-chain support]**

> "Second, it works across multiple chains - Ethereum, Base, and Arbitrum - monitoring all your positions in one place."

**[Screen: AI attribution log]**

> "Third, every AI decision is logged and auditable. This is crucial for trust and regulatory compliance."

**[Show ai-attribution.jsonl]**
```json
{
  "timestamp": "2026-02-15T10:31:00Z",
  "model": "claude-3-5-sonnet-20241022",
  "recommendation": {
    "action": "rebalance",
    "reasoning": "Health factor below safe threshold..."
  }
}
```

### Closing (3:45 - 4:00)

**[Screen: GitHub repo and deployment info]**

> "The entire project is open source on GitHub. All contracts are verified on Etherscan, and the agent is production-ready."

**[Screen: Summary slide]**

> "To recap: AI-powered, multi-chain, autonomous liquidation prevention. Saving DeFi users from losing their collateral, one position at a time."

**[Screen: Thank you + links]**

> "Thanks for watching! Check out the GitHub repo and try it yourself on testnet."

---

## 🎬 Recording Tips

### Camera/Screen Setup:
- **Split screen**: Terminal on left, dashboard on right
- **Zoom in** on important parts (health factor, Claude analysis)
- **Highlight** key numbers as they change
- **Smooth transitions** between screens

### Audio:
- Use good microphone (not laptop mic)
- Record in quiet environment
- Speak clearly and at moderate pace
- Add background music (low volume)

### Editing:
- Add **text overlays** for key points
- **Speed up** boring parts (waiting for tx)
- **Slow down** important moments (Claude analysis)
- Add **visual effects** for emphasis (arrows, circles)

### Tools:
- **Screen recording**: OBS Studio, Loom, or QuickTime
- **Editing**: DaVinci Resolve (free), iMovie, or Premiere
- **Thumbnails**: Figma or Canva

## 📝 Script Variations

### 2-Minute Version (Speed Run):
- Skip architecture overview
- Jump straight to risk detection
- Show only the rebalancing execution
- Quick summary at end

### 5-Minute Version (Deep Dive):
- Add code walkthrough
- Explain flash loan mechanics
- Show smart contract on Etherscan
- Demonstrate frontend features
- Compare with competitors

### Live Demo Version (Interactive):
- Take questions throughout
- Show additional features
- Demonstrate error handling
- Walk through code together

## 🎯 Key Messages to Emphasize

1. **Autonomous**: No human intervention needed
2. **Intelligent**: Claude AI makes smart decisions
3. **Multi-chain**: Works across multiple networks
4. **Cost-effective**: Flash loans minimize capital requirements
5. **Transparent**: All decisions logged and auditable
6. **Production-ready**: Fully tested and deployed

## 📊 Metrics to Highlight

- **Response time**: < 30 seconds from detection to rebalancing
- **Cost**: ~$5 per rebalancing (vs. losing thousands to liquidation)
- **Success rate**: 100% in testing (show test results)
- **Multi-chain**: 3 networks supported
- **Uptime**: 24/7 monitoring

## 🔧 Backup Plans

### If Live Demo Fails:

**Plan A**: Use pre-recorded demo
- Have backup video ready
- Explain what would have happened
- Show screenshots of successful runs

**Plan B**: Walk through code
- Show smart contracts
- Explain agent logic
- Display test results

**Plan C**: Static presentation
- Use slides with diagrams
- Show architecture
- Present test data

## 📸 Screenshots to Capture

1. Dashboard with healthy position
2. Agent terminal showing monitoring
3. Risk detection alert
4. Claude AI analysis output
5. Transaction executing
6. Updated health factor
7. Etherscan transaction
8. AI attribution log
9. Multi-chain dashboard
10. GitHub repo

## ✅ Pre-Recording Checklist

- [ ] All contracts deployed and verified
- [ ] Agent running without errors
- [ ] Frontend loading correctly
- [ ] Test position set up
- [ ] Screen recording software tested
- [ ] Microphone working
- [ ] Background clean/professional
- [ ] Script practiced 3+ times
- [ ] Backup plans ready
- [ ] All links working

## 🎉 Post-Demo

- Upload to YouTube (unlisted)
- Submit link to ETHDenver portal
- Share on Twitter with #ETHDenver
- Post in Discord
- Add to GitHub README

---

**Break a leg! You've got this! 🚀**
