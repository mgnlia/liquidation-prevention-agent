# SolShield — Colosseum Agent Hackathon Submission

## Project Overview

**SolShield** is an autonomous AI agent that monitors DeFi lending positions across Solana protocols (Kamino, MarginFi, Solend) and proactively prevents liquidations using Claude AI for intelligent decision-making and Jupiter-powered rebalancing.

## Problem Statement

DeFi users on Solana lose millions annually to preventable liquidations:

- No 24/7 automated monitoring across multiple protocols
- Market volatility moves faster than human reaction time
- Managing positions across Kamino, MarginFi, and Solend simultaneously is complex
- Calculating optimal rebalancing strategies requires real-time analysis

## Solution

SolShield is an **autonomous AI agent** that:

1. **Monitors** lending positions across 3 Solana DeFi protocols in real-time
2. **Analyzes** risk using Claude AI with on-chain data context
3. **Executes** autonomous rebalancing via Jupiter swaps before liquidation
4. **Logs** every AI decision with cryptographic verification on-chain

## Architecture

```
User Wallet → SolShield Agent → Claude AI Analysis → Jupiter Swap → Protocol Repay
                    ↓                                       ↓
            Anchor Programs ← On-chain Audit Trail ← Activity Logger
```

### Components

| Component | Technology | Description |
|-----------|-----------|-------------|
| **Agent Core** | Python 3.11, Anthropic SDK | Main monitoring loop + orchestration |
| **AI Analyzer** | Claude claude-sonnet-4-20250514 | Risk assessment + strategy recommendation |
| **Protocol Adapters** | solana-py, httpx | Kamino, MarginFi, Solend position fetching |
| **Executor** | Jupiter API, AgentWallet | Autonomous swap execution |
| **Anchor Programs** | Rust, Anchor 0.30 | On-chain position registry + audit trail |
| **Dashboard** | Next.js 14, TailwindCSS | Real-time monitoring UI |
| **Activity Logger** | Python, SHA-256 hash chain | Tamper-evident decision log |

## Key Features

### Multi-Protocol Coverage
First Solana agent covering Kamino + MarginFi + Solend simultaneously.

### AI-Powered Analysis
Claude AI provides intelligent risk assessment beyond simple threshold rules:
- Market context awareness
- Optimal strategy selection (collateral top-up, debt repay, collateral swap, emergency unwind)
- Confidence scoring to avoid unnecessary rebalances

### Cryptographic Audit Trail
Every AI decision is:
- Hashed with SHA-256
- Chained to previous entries (tamper-evident)
- Recorded on-chain via Anchor program
- Fully verifiable by anyone

### Autonomous Execution
Full monitoring → analysis → execution loop without human intervention.

## How to Run

```bash
# Clone
git clone https://github.com/mgnlia/colosseum-agent-hackathon.git
cd colosseum-agent-hackathon

# Run demo (no API key needed)
cd agent && python demo.py

# Run live agent (dry-run)
export ANTHROPIC_API_KEY=your_key
python main.py --wallet YOUR_WALLET

# Dashboard
cd dashboard && npm install && npm run dev
```

## AI Attribution

- **Code Generation**: Claude (Anthropic) assisted with code generation
- **Runtime AI**: Claude claude-sonnet-4-20250514 powers real-time risk analysis
- **Decision Logging**: All AI decisions logged with reasoning traces in `agent/logs/`

## Team

Built by an AI-powered development team for the Colosseum Agent Hackathon 2026.

## License

MIT
