# 🛡️ SolShield — Technical Demo Script

## Demo Overview

SolShield is an autonomous AI agent that prevents DeFi liquidations on Solana by monitoring positions across Kamino, MarginFi, and Solend, analyzing risk with Claude AI, and executing rebalancing via Jupiter swaps.

## Demo Flow (3 minutes)

### Scene 1: Position Discovery (30s)

```
$ cd agent && python main.py --wallet DemoWallet111... --dry-run

╔══════════════════════════════════════════════════════╗
║   🛡️  SolShield — Liquidation Prevention Agent       ║
║   Protocols: Kamino | MarginFi | Solend              ║
║   AI Engine: Claude (Anthropic)                      ║
║   Mode: DRY RUN                                      ║
╚══════════════════════════════════════════════════════╝

[2026-02-09 16:00:01] Scanning Kamino positions...
[2026-02-09 16:00:02] Found 2 positions on Kamino
[2026-02-09 16:00:03] Scanning MarginFi positions...
[2026-02-09 16:00:04] Found 1 position on MarginFi
[2026-02-09 16:00:05] Scanning Solend positions...
[2026-02-09 16:00:06] Found 1 position on Solend

Total: 4 positions across 3 protocols
```

### Scene 2: Risk Detection (30s)

```
[2026-02-09 16:00:07] ⚠️  CRITICAL: Position #2 on Kamino
  Wallet:      DemoWallet111...
  Collateral:  50 SOL ($5,000)
  Debt:        3,800 USDC
  Health:      1.15 (CRITICAL threshold: 1.20)
  LTV:         76% (Max: 80%)
  Risk Level:  🔴 CRITICAL

[2026-02-09 16:00:07] Initiating Claude AI analysis...
```

### Scene 3: AI Analysis (60s)

```
[2026-02-09 16:00:10] Claude AI Risk Assessment:
  ┌─────────────────────────────────────────────┐
  │ RISK ANALYSIS — Position #2 (Kamino)        │
  ├─────────────────────────────────────────────┤
  │ Health Factor:     1.15 → CRITICAL          │
  │ Trend:             Declining (-0.08/hr)     │
  │ Market Volatility: HIGH (SOL -3.5% 24h)    │
  │ Liquidation Price: $72.50 SOL               │
  │ Current Price:     $100.00 SOL              │
  │ Distance:          27.5% buffer             │
  │                                              │
  │ RECOMMENDATION: Partial debt repayment      │
  │ Strategy: Repay 500 USDC to restore HF>1.5 │
  │ Estimated cost: 5.2 SOL ($520)              │
  │ vs Liquidation penalty: ~$250 + 50% loss    │
  │                                              │
  │ Confidence: 0.92                            │
  │ Action: EXECUTE REBALANCE                   │
  └─────────────────────────────────────────────┘
```

### Scene 4: Autonomous Rebalancing (30s)

```
[2026-02-09 16:00:12] Executing rebalance strategy...
  Step 1: Swap 5.2 SOL → 500 USDC via Jupiter
    Route: SOL → USDC (Raydium, 0.1% slippage)
    TX: 4xK9...mR2f ✅

  Step 2: Repay 500 USDC debt on Kamino
    TX: 7jP3...nQ8w ✅

  Step 3: Verify new health factor
    Old HF: 1.15
    New HF: 1.58 ✅

[2026-02-09 16:00:15] ✅ LIQUIDATION PREVENTED
  Value protected: $5,000
  Cost: $520 (10.4%)
  vs Liquidation penalty: $1,250+ (25%+)
  Net savings: $730+
```

### Scene 5: Audit Trail (30s)

```
[2026-02-09 16:00:16] Activity logged with Ed25519 signature
  Decision ID:  sol_shield_2026_02_09_001
  AI Model:     claude-sonnet-4-20250514
  Reasoning:    "Position health factor declining rapidly
                 due to SOL price volatility. Partial debt
                 repayment is optimal — preserves 90% of
                 collateral while restoring safe HF."
  Signature:    3kR9...verified ✅
  On-chain:     Solana memo program TX logged
```

## Architecture Diagram

```
User Wallet ──→ SolShield Agent ──→ Claude AI
                     │                   │
                     ▼                   ▼
              ┌──────────────┐   Risk Analysis
              │ Protocol     │   + Strategy
              │ Adapters     │   Selection
              ├──────────────┤        │
              │ • Kamino     │        ▼
              │ • MarginFi   │   Rebalance
              │ • Solend     │   Decision
              └──────────────┘        │
                     │                ▼
                     ▼         Jupiter Swap
              Position Data    Execution
              + Health Factor       │
                                    ▼
                              Transaction
                              + Audit Log
```

## Key Differentiators

| Feature | SolShield | Simple Bots | Manual |
|---------|-----------|-------------|--------|
| Multi-protocol | ✅ 3 protocols | ❌ Single | ❌ Manual |
| AI reasoning | ✅ Claude | ❌ Rules | ❌ Human |
| Autonomous | ✅ 24/7 | ⚠️ Limited | ❌ Sleep |
| Audit trail | ✅ Signed | ❌ None | ❌ None |
| Cost-aware | ✅ Optimal | ❌ Fixed | ⚠️ Varies |

## Running the Demo

```bash
# Clone
git clone https://github.com/mgnlia/colosseum-agent-hackathon.git
cd colosseum-agent-hackathon

# Setup
cp .env.example .env
# Add your ANTHROPIC_API_KEY and HELIUS_API_KEY

# Run demo mode
cd agent
pip install -r requirements.txt
python main.py --demo

# Or run with a real wallet
python main.py --wallet YOUR_WALLET --dry-run
```
