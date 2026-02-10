# 🛡️ SolShield — AI-Powered Liquidation Prevention Agent for Solana

> **Colosseum Agent Hackathon 2026** | $100K USDC Prize Pool

An autonomous AI agent that monitors DeFi lending positions across Solana protocols (Kamino, MarginFi, Solend) and proactively prevents liquidations using Claude AI for intelligent decision-making and Jupiter-powered rebalancing.

## 🎯 Problem

DeFi users on Solana lose millions annually to liquidations:
- **No 24/7 monitoring** — positions drift while users sleep
- **Delayed reactions** — market volatility moves faster than humans
- **Multi-protocol complexity** — managing positions across Kamino, MarginFi, Solend simultaneously
- **High cognitive load** — calculating optimal rebalancing strategies in real-time

## 💡 Solution

**SolShield** is an autonomous AI agent that:

1. **Monitors** user lending positions across Solana DeFi protocols in real-time
2. **Analyzes** risk using Claude AI's reasoning capabilities with on-chain data
3. **Executes** autonomous rebalancing via Jupiter swaps before liquidation occurs
4. **Logs** all AI decisions transparently for auditability

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SolShield AI Agent                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Position  │→ │ Claude AI │→ │ Strategy │→ │ TX       │   │
│  │ Monitor   │  │ Analyzer  │  │ Engine   │  │ Executor │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                    ↓                              ↑
┌─────────────────────────────────────────────────────────────┐
│                  Solana On-Chain Layer                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Kamino   │  │ MarginFi │  │ Solend   │  │ Jupiter  │   │
│  │ Lending  │  │ Protocol │  │ V2       │  │ Swap     │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                    ↓                              ↑
┌─────────────────────────────────────────────────────────────┐
│                  Anchor Programs (On-Chain)                  │
│  ┌──────────────────┐  ┌──────────────────────────────┐    │
│  │ SolShield        │  │ Position Registry            │    │
│  │ Orchestrator     │  │ (User position tracking)     │    │
│  └──────────────────┘  └──────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Features

### Core
- ✅ **Multi-Protocol Monitoring** — Kamino, MarginFi, Solend position tracking
- ✅ **Claude AI Risk Analysis** — Intelligent health factor assessment with market context
- ✅ **Jupiter-Powered Rebalancing** — Optimal swap routing for collateral adjustments
- ✅ **Autonomous Execution** — Fully autonomous decision-making loop
- ✅ **AgentWallet Integration** — Secure Solana wallet management

### Solana-Native
- ✅ **Anchor Programs** — On-chain position registry and orchestration
- ✅ **Helius RPC** — Real-time WebSocket position monitoring
- ✅ **SPL Token Support** — Native handling of all Solana tokens
- ✅ **Transaction Optimization** — Priority fees and compute budget management

### AI Attribution
- ✅ **Decision Logging** — Every AI decision logged with reasoning
- ✅ **Cryptographic Verification** — Ed25519 signed activity logs
- ✅ **Transparent Audit Trail** — Full history of agent actions

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Smart Contracts | Anchor Framework (Rust) |
| AI Agent | Python 3.11+, Anthropic Claude API |
| Blockchain | Solana, @solana/web3.js, solders |
| DeFi Protocols | Kamino, MarginFi, Solend |
| Swap Routing | Jupiter Aggregator |
| RPC/Indexing | Helius |
| Wallet | AgentWallet |
| Dashboard | Next.js, TailwindCSS |

## 🛠️ Quick Start

### Prerequisites
- Node.js >= 18
- Python >= 3.11
- Rust + Anchor CLI
- Solana CLI

### 1. Clone & Install

```bash
git clone https://github.com/mgnlia/colosseum-agent-hackathon.git
cd colosseum-agent-hackathon

# Install Anchor dependencies
cd programs && anchor build && cd ..

# Install agent dependencies  
cd agent && pip install -r requirements.txt && cd ..

# Install dashboard
cd dashboard && npm install && cd ..
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your keys:
# - ANTHROPIC_API_KEY
# - HELIUS_API_KEY  
# - AGENT_WALLET_API_KEY
```

### 3. Run the Agent

```bash
cd agent
python main.py
```

### 4. Launch Dashboard

```bash
cd dashboard
npm run dev
```

## 📊 How It Works

### 1. Position Discovery
The agent queries Solana DeFi protocols to find user lending positions:
- Fetches obligation accounts from Kamino/Solend
- Reads MarginFi margin accounts
- Calculates real-time health factors

### 2. Risk Analysis (Claude AI)
When a position's health factor drops below threshold:
```
Health Factor < 1.5 → WARN (monitor closely)
Health Factor < 1.2 → CRITICAL (prepare rebalance)
Health Factor < 1.05 → EMERGENCY (execute immediately)
```

Claude analyzes:
- Current market conditions and volatility
- Historical liquidation patterns
- Optimal rebalancing strategy
- Gas cost vs. liquidation penalty tradeoff

### 3. Autonomous Rebalancing
The agent executes the optimal strategy:
- **Collateral Top-up** — Add more collateral via Jupiter swap
- **Debt Repayment** — Partial debt repayment to improve health
- **Position Migration** — Move to a protocol with better rates
- **Emergency Unwind** — Full position closure if critically at risk

### 4. Verification
All actions are logged with:
- Transaction signatures
- AI reasoning traces
- Cryptographic attestation via AgentWallet

## 🏆 Why SolShield Wins

| Feature | SolShield | Others |
|---------|-----------|--------|
| Multi-protocol | ✅ Kamino + MarginFi + Solend | Single protocol |
| AI-powered | ✅ Claude reasoning | Rule-based |
| Autonomous | ✅ Full loop | Manual alerts |
| On-chain programs | ✅ Anchor | Off-chain only |
| Audit trail | ✅ Cryptographic | None |

## 📄 License

MIT

## 🤖 AI Attribution

This project was built by an autonomous AI agent using Claude (Anthropic) for both code generation and runtime decision-making. All AI decisions are logged in `agent/logs/` with full reasoning traces.
