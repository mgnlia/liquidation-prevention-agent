# 🎥 Video Narration Script - Exact Words to Say

**Duration: 2 minutes**  
**Format: Screen recording with voiceover**

---

## Setup Before Recording:

1. Have these windows ready:
   - Terminal with deployment output
   - VS Code with contracts/LiquidationPrevention.sol open
   - VS Code with agent/main.py open
   - GitHub repo page

2. Test audio levels
3. Close unnecessary tabs/windows
4. 3-2-1 countdown before starting

---

## 🎬 SCENE 1: Title & Problem (0:00 - 0:25)

**[Show: GitHub README or title slide]**

**SAY:**
> "Hi, I'm presenting the AI-Powered Liquidation Prevention Agent for ETHDenver 2026, Futurllama track.
>
> The problem: DeFi users lose millions annually to liquidations. A user deposits ten thousand dollars in ETH as collateral, borrows six thousand in stablecoins. Overnight, ETH drops twenty percent. Health factor falls below one point zero, and they get liquidated, losing ten percent of their collateral.
>
> They were asleep and never saw it coming."

**[Transition to architecture diagram from README]**

---

## 🎬 SCENE 2: Solution Overview (0:25 - 0:50)

**[Show: Architecture diagram]**

**SAY:**
> "Our solution: an autonomous AI agent that monitors positions twenty-four-seven.
>
> When it detects risk, it sends the data to Claude AI from Anthropic. Claude analyzes the situation, evaluates urgency, and recommends an action.
>
> If rebalancing is needed, the agent executes a flash loan from Aave to adjust the position automatically, in seconds.
>
> Three layers: Smart contracts on Ethereum handling protocol integrations. Python AI agent using Claude for decisions. And flash loan rebalancing for capital efficiency."

**[Transition to terminal]**

---

## 🎬 SCENE 3: Deployment Demo (0:50 - 1:10)

**[Show: Terminal with deployment output]**

**SAY:**
> "Here's the deployment to our local testnet. Four contracts:
>
> The Aave Adapter integrates with Aave V3 for health factor monitoring.
>
> The Compound Adapter does the same for Compound V3.
>
> The Flash Loan Rebalancer handles the atomic rebalancing transactions.
>
> And the main Liquidation Prevention contract orchestrates everything.
>
> All contracts deployed successfully and verified."

**[Transition to code]**

---

## 🎬 SCENE 4: Smart Contract Code (1:10 - 1:30)

**[Show: contracts/LiquidationPrevention.sol in VS Code]**

**SAY:**
> "Here's the main contract. Users configure their preferences: minimum health factor threshold, target health factor after rebalancing, and which protocols to monitor.
>
> The contract checks positions across protocols and determines if rebalancing is needed.
>
> When the AI agent calls execute-rebalance, it verifies the agent is authorized, checks the health factor is actually below the threshold, then triggers the flash loan rebalancing."

**[Scroll to show key functions: setUserConfig, checkRebalanceNeeded, executeRebalance]**

---

## 🎬 SCENE 5: AI Agent Integration (1:30 - 1:50)

**[Show: agent/main.py in VS Code]**

**SAY:**
> "Here's the AI agent. It continuously monitors user positions.
>
> When risk is detected, it sends the position data to Claude. Here's the prompt: we ask Claude to analyze the health factor, collateral, debt, and market conditions, then recommend rebalance, monitor, or no action.
>
> Claude responds with its reasoning, urgency level, and recommended amount.
>
> All decisions are logged to our AI attribution file for complete transparency, which is required for the Futurllama track."

**[Highlight: get_claude_recommendation function and _log_ai_decision]**

---

## 🎬 SCENE 6: Closing (1:50 - 2:00)

**[Show: GitHub repo page]**

**SAY:**
> "This is production-ready code with full test coverage, multi-chain support for Ethereum, Base, and Arbitrum, and comprehensive documentation.
>
> The repo is open source at github dot com slash mgnlia slash liquidation prevention agent.
>
> Thank you!"

**[Hold on GitHub repo for 3 seconds]**

---

## 📸 Key Visuals Checklist

Make sure these are clearly visible:

- [ ] Project title and ETHDenver logo
- [ ] Architecture diagram
- [ ] Terminal showing successful deployment
- [ ] Contract addresses
- [ ] Smart contract code (clean, readable)
- [ ] AI agent code with Claude integration
- [ ] GitHub repo URL
- [ ] Test results (if time permits)

---

## 🎙️ Audio Tips

**Pacing:**
- Speak clearly and not too fast
- Pause briefly between sentences
- Emphasize key numbers and terms

**Tone:**
- Professional but enthusiastic
- Confident (you built something awesome!)
- Clear pronunciation of technical terms

**Key Terms to Emphasize:**
- "Claude AI" (our differentiator)
- "Flash loan" (technical innovation)
- "Autonomous" (Futurllama alignment)
- "Production-ready" (completeness)
- "Multi-chain" (scalability)

---

## ⏱️ Timing Breakdown

| Time | Section | Key Message |
|------|---------|-------------|
| 0:00-0:25 | Problem | Liquidations cost users millions |
| 0:25-0:50 | Solution | AI agent + flash loans prevent liquidations |
| 0:50-1:10 | Deployment | 4 contracts deployed and working |
| 1:10-1:30 | Smart Contracts | Clean, secure, well-architected code |
| 1:30-1:50 | AI Integration | Claude makes intelligent decisions |
| 1:50-2:00 | Closing | Open source, production-ready |

---

## 🎬 Alternative: Slides-Based Demo

If screen recording is difficult, use slides:

**Slide 1:** Title + Problem statement  
**Slide 2:** Architecture diagram  
**Slide 3:** Screenshot of deployment  
**Slide 4:** Smart contract code snippet  
**Slide 5:** AI agent code snippet  
**Slide 6:** Test results  
**Slide 7:** GitHub repo + thank you  

Record yourself presenting the slides with this same narration.

---

## ✅ Post-Recording Checklist

After recording:
- [ ] Video is 2-4 minutes long
- [ ] Audio is clear (no background noise)
- [ ] Code is readable (font size large enough)
- [ ] No sensitive info visible (API keys, etc.)
- [ ] Video plays without issues
- [ ] Upload to YouTube (can be unlisted)
- [ ] Get shareable link
- [ ] Add link to README.md
- [ ] Use link in Devfolio registration

---

## 🚨 If Recording Fails

**Plan B: Loom**
- Free screen recorder: loom.com
- Records screen + webcam
- Instant sharing

**Plan C: Slides Only**
- Create PowerPoint/Google Slides
- Export as video with narration
- Upload to YouTube

**Plan D: Text Walkthrough**
- Detailed written demo
- Screenshots at each step
- Submit as documentation

---

**You've got this! Just read this script while showing the code. 2 minutes. Done. 🎬**
