# Architecture - Autonomous Office Protocol

## Overview

The Autonomous Office Protocol (AOP) is a Solana-native AI agent system designed for the Colosseum Agent Hackathon. It demonstrates autonomous decision-making, cryptographic activity logging, and DeFi risk management.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Next.js Dashboard (dashboard/)                           │  │
│  │  - Real-time activity visualization                       │  │
│  │  - Statistics and metrics                                 │  │
│  │  - Leaderboard tracking                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                      Agent Core Layer                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Autonomous Agent (src/main.py)                           │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │  │
│  │  │  Monitor   │→ │  Analyze   │→ │  Execute   │         │  │
│  │  │ Positions  │  │  (Claude)  │  │  Actions   │         │  │
│  │  └────────────┘  └────────────┘  └────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                    Integration Layer                             │
│  ┌──────────────────────┐  ┌──────────────────────────────┐   │
│  │  AgentWallet         │  │  Claude AI                    │   │
│  │  (src/agentwallet.py)│  │  (Anthropic API)              │   │
│  │  - Activity logging  │  │  - Risk analysis              │   │
│  │  - Cryptographic     │  │  - Decision making            │   │
│  │    signing           │  │  - Reasoning                  │   │
│  │  - API integration   │  └──────────────────────────────┘   │
│  └──────────────────────┘                                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                          │
│  ┌──────────────────────┐  ┌──────────────────────────────┐   │
│  │  Colosseum API       │  │  Solana Blockchain            │   │
│  │  - Agent registration│  │  - Solend                     │   │
│  │  - Activity tracking │  │  - Kamino                     │   │
│  │  - Leaderboard       │  │  - Marinade                   │   │
│  └──────────────────────┘  └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Agent Core (`src/main.py`)

The main autonomous agent that orchestrates all operations.

**Key Functions:**
- `monitor_positions()` - Monitors DeFi positions across Solana protocols
- `analyze_risk_with_claude()` - Uses Claude AI for risk analysis
- `execute_action()` - Executes recommended actions
- `run_cycle()` - Runs complete agent cycle
- `run()` - Continuous operation loop

**Cycle Flow:**
1. Monitor positions → 2. Analyze with Claude → 3. Execute action → 4. Log activity

**Configuration:**
- Cycle interval: 600 seconds (10 minutes)
- Activities per cycle: ~3 (monitor + analysis + execution)
- Target rate: 6-7 activities/hour

### 2. AgentWallet Integration (`src/agentwallet.py`)

Handles cryptographic activity logging and Colosseum API integration.

**Features:**
- SHA256 hashing of activity data
- Ed25519 signature generation
- Local activity storage
- API activity submission
- Leaderboard position tracking

**Activity Structure:**
```json
{
  "timestamp": "2026-02-09T10:00:00Z",
  "activity_type": "position_monitor",
  "data": {
    "protocols_checked": ["solend", "kamino"],
    "status": "healthy"
  },
  "hash": "sha256_hash_of_activity",
  "signature": "ed25519_signature"
}
```

### 3. Activity Logger (`src/activity_logger.py`)

Low-level cryptographic activity logging.

**Key Functions:**
- `log_activity()` - Creates and signs activity
- `get_all_activities()` - Retrieves all activities
- `get_activity_count()` - Returns total count

**Cryptographic Process:**
1. Create activity JSON
2. Compute SHA256 hash
3. Sign with Ed25519 private key
4. Store locally
5. Push to Colosseum API

### 4. Dashboard (`dashboard/`)

Next.js-based visualization dashboard.

**Features:**
- Real-time activity feed
- Statistics dashboard (total, hourly, daily rates)
- Activity type breakdown
- Leaderboard position
- Cryptographic verification display

**Tech Stack:**
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS

### 5. Registration System (`scripts/`)

Automated registration and setup scripts.

**Scripts:**
- `register_colosseum.py` - Agent registration
- `setup_agentwallet.py` - AgentWallet configuration
- `check_status.py` - Status monitoring

## Data Flow

### Activity Logging Flow

```
Agent Action
    ↓
Create Activity Object
    ↓
Compute SHA256 Hash
    ↓
Sign with Ed25519
    ↓
Store Locally (data/activities/)
    ↓
Push to Colosseum API
    ↓
Update Leaderboard
```

### Decision Making Flow

```
Monitor Positions
    ↓
Extract Position Data
    ↓
Send to Claude AI
    ↓
Receive Analysis & Recommendation
    ↓
Parse Action Type
    ↓
Execute Action
    ↓
Log Result
```

## Security Architecture

### Cryptographic Components

1. **Ed25519 Keypair**
   - Private key: `.keys/ed25519_private.pem` (never shared)
   - Public key: `.keys/ed25519_public.pem` (verifiable)
   - Purpose: Activity signature

2. **SHA256 Hashing**
   - Input: Activity JSON (sorted keys)
   - Output: 256-bit hash
   - Purpose: Data integrity verification

3. **Activity Verification**
   ```python
   # Verify activity integrity
   computed_hash = sha256(activity_json)
   assert computed_hash == activity.hash
   
   # Verify signature
   public_key.verify(signature, activity_json)
   ```

### API Security

- **Authentication**: Bearer token (API key)
- **Rate Limiting**: Respects Colosseum API limits
- **Error Handling**: Graceful degradation if API unavailable

## Scalability Considerations

### Horizontal Scaling

- **Multiple Agents**: Can run multiple agent instances
- **Activity Deduplication**: SHA256 hash prevents duplicates
- **Load Distribution**: Different protocols per agent

### Performance Optimization

- **Async Operations**: All I/O operations are async
- **Batching**: Activities batched before API submission
- **Caching**: Position data cached between cycles
- **Rate Control**: Configurable cycle intervals

## Monitoring & Observability

### Metrics Tracked

1. **Activity Metrics**
   - Total activities logged
   - Activities per hour/day
   - Activity type distribution

2. **Performance Metrics**
   - Cycle execution time
   - API response times
   - Error rates

3. **Competition Metrics**
   - Leaderboard position
   - Gap to leader
   - Required rate to reach target

### Logging

- **Console Logs**: Real-time operation logs
- **Activity Files**: JSON files in `data/activities/`
- **Status Reports**: Generated by `check_status.py`

## Deployment Architecture

### Development
```
Local Machine
├── Agent (Python)
├── Dashboard (Next.js dev server)
└── Data (local filesystem)
```

### Production
```
Cloud Infrastructure
├── Agent (Docker container)
├── Dashboard (Vercel)
└── Data (S3/persistent volume)
```

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **AI**: Anthropic Claude 3.5 Sonnet
- **Blockchain**: Solana (via solana-py)
- **Crypto**: cryptography library (Ed25519)
- **HTTP**: requests library

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Deployment**: Vercel

### Infrastructure
- **Version Control**: Git/GitHub
- **CI/CD**: GitHub Actions (future)
- **Monitoring**: Custom scripts
- **Storage**: Local filesystem / S3

## Future Enhancements

### Phase 2 (Post-Hackathon)
1. **Real DeFi Integration**
   - Actual Solend position monitoring
   - Kamino vault tracking
   - Marinade staking analysis

2. **Advanced AI**
   - Multi-agent coordination
   - Predictive analytics
   - Automated rebalancing

3. **Enhanced Security**
   - Hardware wallet integration
   - Multi-sig support
   - Audit logging

4. **Production Features**
   - Database backend
   - API gateway
   - Load balancing
   - Auto-scaling

### Phase 3 (Mainnet)
1. **Mainnet Deployment**
2. **Real Money Operations**
3. **Insurance Fund**
4. **DAO Governance**

## Design Principles

1. **Autonomy**: Minimal human intervention required
2. **Transparency**: All decisions logged and verifiable
3. **Security**: Cryptographic verification at every step
4. **Scalability**: Designed for high-volume operations
5. **Modularity**: Components can be independently upgraded
6. **Reliability**: Graceful error handling and recovery

## References

- [Colosseum Agent Hackathon](https://colosseum.com/agent-hackathon/)
- [AgentWallet Documentation](https://agentwallet.mcpay.tech/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Solana Documentation](https://docs.solana.com/)
- [Ed25519 Signatures](https://ed25519.cr.yp.to/)
