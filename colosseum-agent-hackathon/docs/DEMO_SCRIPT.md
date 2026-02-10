# SolShield Demo Script

## 2-Minute Video Demo Narration

### Scene 1: The Problem (0:00-0:20)
**[Show DeFi dashboard with dropping health factors]**

"Every day, DeFi users on Solana lose thousands to liquidations. You're sleeping, the market crashes, and by the time you wake up — your position is gone. SolShield changes that."

### Scene 2: How It Works (0:20-0:50)
**[Show architecture diagram]**

"SolShield is an autonomous AI agent that monitors your lending positions across Kamino, MarginFi, and Solend — 24/7. When your health factor drops, Claude AI analyzes the situation and automatically rebalances your position using Jupiter swaps — before liquidation hits."

### Scene 3: Live Demo (0:50-1:30)
**[Run `python agent/demo.py`]**

"Let's see it in action. Here we have three positions:
- A healthy Kamino position at 2.1x health factor
- A MarginFi position dropping to 1.35x — warning level
- A Solend position at 1.08x — critical, near liquidation

Watch as Claude AI analyzes each position... recommends debt repayment for MarginFi... and triggers emergency collateral top-up for Solend. All executed autonomously, all logged on-chain."

### Scene 4: On-Chain Verification (1:30-1:50)
**[Show Solana Explorer with rebalance records]**

"Every decision is recorded on Solana with a hash of the AI's reasoning. You can verify any action. Full transparency, full auditability."

### Scene 5: Closing (1:50-2:00)
**[Show SolShield logo + stats]**

"SolShield: Never get liquidated again. Built on Solana. Powered by Claude AI. Open source."

## Running the Demo

```bash
# Quick demo (no API key needed)
cd agent && python demo.py

# Full demo with Claude AI
export ANTHROPIC_API_KEY=your_key
cd agent && python demo.py

# Live agent mode
cd agent && python main.py --wallet YOUR_WALLET_ADDRESS
```

## Key Talking Points for Judges

1. **Real problem**: Liquidations cost DeFi users millions annually
2. **Multi-protocol**: First agent covering Kamino + MarginFi + Solend
3. **AI-native**: Claude AI for intelligent risk assessment, not just rules
4. **On-chain verification**: Every AI decision recorded on Solana
5. **Audit trail**: Tamper-evident hash chain for all agent activities
6. **Production-ready**: Anchor programs, comprehensive tests, clean architecture
