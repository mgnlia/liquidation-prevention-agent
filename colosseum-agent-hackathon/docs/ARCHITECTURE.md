# SolShield Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SolShield AI Agent                           │
│                                                                     │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────┐            │
│  │   Position    │  │   Claude AI   │  │   Rebalance  │            │
│  │   Monitor     │→ │   Analyzer    │→ │   Executor   │            │
│  │              │  │               │  │              │            │
│  │ • Kamino     │  │ • Risk Score  │  │ • Jupiter    │            │
│  │ • MarginFi   │  │ • Strategy    │  │ • AgentWallet│            │
│  │ • Solend     │  │ • Confidence  │  │ • Dry Run    │            │
│  └──────────────┘  └───────────────┘  └──────────────┘            │
│         ↕                  ↕                  ↕                    │
│  ┌─────────────────────────────────────────────────────┐          │
│  │            Activity Logger (Hash Chain)              │          │
│  │  [Entry₀] → [Entry₁] → [Entry₂] → ... → [Entryₙ]  │          │
│  │   hash₀  ←   hash₁  ←   hash₂  ← ... ←   hashₙ   │          │
│  └─────────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────┘
         ↕                                          ↕
┌─────────────────────┐              ┌──────────────────────────┐
│   Solana Blockchain  │              │   Dashboard (Next.js)    │
│                     │              │                          │
│  ┌───────────────┐  │              │  • Position Cards        │
│  │  SolShield    │  │              │  • Health Gauges         │
│  │  Anchor       │  │              │  • Activity Feed         │
│  │  Program      │  │              │  • Agent Status          │
│  │               │  │              │  • Stats Panel           │
│  │  • Registry   │  │              │  • Wallet Connect        │
│  │  • Audit Log  │  │              └──────────────────────────┘
│  │  • Rebalance  │  │
│  │    Records    │  │
│  └───────────────┘  │
│                     │
│  ┌──────┐ ┌──────┐ │
│  │Kamino│ │MarFi │ │
│  └──────┘ └──────┘ │
│  ┌──────┐ ┌──────┐ │
│  │Solend│ │Jupiter│ │
│  └──────┘ └──────┘ │
└─────────────────────┘
```

## Data Flow

### 1. Position Discovery
```
Agent Loop (every 30s)
  → For each watched wallet:
    → KaminoAdapter.get_positions(wallet)
      → RPC: getProgramAccounts(KLend program, filter by owner)
      → Parse obligation accounts
      → Calculate health factor
    → MarginFiAdapter.get_positions(wallet)
      → RPC: getProgramAccounts(MarginFi program)
      → Parse margin accounts
    → SolendAdapter.get_positions(wallet)
      → RPC: getProgramAccounts(Solend program)
      → Parse obligation accounts
  → Collect all PositionData objects
  → Filter: risk_level in (WARNING, CRITICAL, EMERGENCY)
```

### 2. AI Risk Analysis
```
For each at-risk position:
  → Build analysis prompt with:
    - Position details (HF, collateral, debt)
    - Collateral breakdown (token, LTV, liq threshold)
    - Debt breakdown (token, APY)
    - Market context (optional)
  → Claude API call (temperature=0.1)
  → Parse JSON response → AnalysisResult
  → If parse fails → fallback_analysis (rule-based)
  → Log to ActivityLogger
```

### 3. Execution Decision
```
If analysis.needs_action AND analysis.confidence >= 0.7:
  → Select execution strategy:
    COLLATERAL_TOP_UP → Jupiter swap USDC→collateral token
    DEBT_REPAYMENT    → Jupiter swap + protocol repay
    COLLATERAL_SWAP   → Jupiter swap volatile→stable
    EMERGENCY_UNWIND  → Full position closure
  → Execute via AgentWallet (or dry-run)
  → Record on-chain via Anchor program
  → Log result to ActivityLogger
```

## On-Chain Program (Anchor)

### Accounts

| Account | Seeds | Description |
|---------|-------|-------------|
| `ProtocolState` | `["protocol-state"]` | Global config + stats |
| `MonitoredPosition` | `["position", owner, obligation_key]` | Per-position monitoring data |
| `RebalanceRecord` | `["rebalance", position, count]` | Audit record per rebalance |

### Instructions

| Instruction | Signer | Description |
|-------------|--------|-------------|
| `initialize` | Authority | Set up protocol config |
| `register_position` | Owner | Start monitoring a position |
| `update_health` | Agent | Update health factor data |
| `record_rebalance` | Agent | Log a rebalance action |
| `pause_position` | Owner | Pause monitoring |
| `resume_position` | Owner | Resume monitoring |
| `close_position` | Owner | Stop monitoring + reclaim rent |

## Security Model

1. **Agent Authority**: Only the designated agent wallet can update health and record rebalances
2. **Owner Control**: Users can pause/resume/close their own positions
3. **Cooldown**: Minimum 60s between rebalances to prevent rapid-fire actions
4. **Confidence Threshold**: AI must be ≥70% confident to execute
5. **Dry Run Default**: Agent starts in dry-run mode; explicit `--live` flag required
6. **Hash Chain**: Activity log uses SHA-256 hash chain for tamper detection
