# 🛡️ AI-Powered Liquidation Prevention Agent

**ETHDenver 2026 | Futurllama Track Submission**

An autonomous AI agent that monitors DeFi positions across multiple protocols and proactively prevents liquidations using Claude AI for intelligent decision-making and flash loan-based rebalancing.

## 🎯 Problem

DeFi users lose millions annually to liquidations due to:
- Lack of 24/7 position monitoring
- Delayed reactions to market volatility
- Complex multi-protocol position management
- High cognitive load for manual rebalancing

## 💡 Solution

An AI-powered agent that:
1. **Monitors** user positions across Aave V3 and Compound V3 in real-time
2. **Analyzes** risk using Claude AI's reasoning capabilities
3. **Executes** autonomous rebalancing via flash loans before liquidation occurs
4. **Supports** multi-chain deployment (Ethereum, Base, Arbitrum)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Agent (Python)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Monitor  │→ │ Claude AI │→ │ Executor │→ │  Logger  │   │
│  │ Positions│  │ Analysis  │  │ Rebalance│  │Attribution│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓ ↑
┌─────────────────────────────────────────────────────────────┐
│              Smart Contracts (Solidity)                      │
│  ┌──────────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Liquidation      │  │ Aave Adapter │  │ Compound     │ │
│  │ Prevention       │→ │              │  │ Adapter      │ │
│  │ (Orchestrator)   │  └──────────────┘  └──────────────┘ │
│  └──────────────────┘                                       │
│           ↓                                                  │
│  ┌──────────────────┐                                       │
│  │ Flash Loan       │                                       │
│  │ Rebalancer       │                                       │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
                            ↓ ↑
┌─────────────────────────────────────────────────────────────┐
│              DeFi Protocols & The Graph                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │ Aave V3  │  │Compound V3│  │The Graph │                 │
│  │ Pools    │  │  Comet    │  │ Subgraph │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Features

### Core Functionality
- ✅ **Multi-Protocol Support**: Aave V3 and Compound V3 integration
- ✅ **AI-Powered Analysis**: Claude 3.5 Sonnet for intelligent risk assessment
- ✅ **Flash Loan Rebalancing**: Gas-efficient position adjustments using Aave flash loans
- ✅ **Real-time Monitoring**: Continuous health factor tracking
- ✅ **Multi-Chain**: Deployed on Sepolia, Base Sepolia, and Arbitrum Sepolia

### Futurllama Track Differentiators
- 🤖 **Autonomous AI Agent**: Fully autonomous decision-making loop
- 🌐 **Multi-Chain Architecture**: Seamless cross-chain position monitoring
- 📊 **The Graph Integration**: Efficient historical data indexing
- 🔍 **Transparent AI Attribution**: All AI decisions logged for auditability

## 📦 Tech Stack

- **Smart Contracts**: Solidity 0.8.20, Hardhat, OpenZeppelin
- **AI Agent**: Python 3.11+, Anthropic Claude API, LangGraph
- **Blockchain**: Web3.py, ethers.js
- **Indexing**: The Graph Protocol
- **Frontend**: React, Next.js, TailwindCSS
- **Testing**: Hardhat, pytest, Jest

## 🛠️ Setup & Installation

### Prerequisites
```bash
node >= 18.0.0
python >= 3.11
```

### 1. Clone Repository
```bash
git clone https://github.com/mgnlia/liquidation-prevention-agent.git
cd liquidation-prevention-agent
```

### 2. Install Dependencies

**Contracts:**
```bash
npm install
```

**Agent:**
```bash
cd agent
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 3. Configure Environment
```bash
cp .env.example .env
```

Edit `.env`:
```env
# Network
NETWORK=sepolia
SEPOLIA_RPC_URL=https://rpc.sepolia.org
BASE_SEPOLIA_RPC_URL=https://sepolia.base.org
ARBITRUM_SEPOLIA_RPC_URL=https://sepolia-rollup.arbitrum.io/rpc

# Deployment
PRIVATE_KEY=your_private_key_here
ETHERSCAN_API_KEY=your_etherscan_key

# AI Agent
ANTHROPIC_API_KEY=your_claude_api_key
CHECK_INTERVAL=60
MIN_HEALTH_FACTOR=1.5
TARGET_HEALTH_FACTOR=2.0

# Contract Addresses (filled after deployment)
LIQUIDATION_PREVENTION_ADDRESS=
AAVE_ADAPTER_ADDRESS=
COMPOUND_ADAPTER_ADDRESS=
```

### 4. Deploy Contracts

**Sepolia:**
```bash
npx hardhat run scripts/deploy.js --network sepolia
```

**Base Sepolia:**
```bash
npx hardhat run scripts/deploy.js --network baseSepolia
```

**Arbitrum Sepolia:**
```bash
npx hardhat run scripts/deploy.js --network arbitrumSepolia
```

### 5. Verify Contracts
```bash
npx hardhat verify --network sepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

### 6. Run Agent
```bash
cd agent
python main.py
```

### 7. Start Frontend
```bash
cd frontend
npm run dev
```

## 📊 Usage

### For Users

1. **Connect Wallet** to the dashboard
2. **Enable Auto-Rebalance** for your address
3. **Set Thresholds**:
   - Minimum Health Factor: 1.5 (trigger)
   - Target Health Factor: 2.0 (goal)
4. **Monitor** your positions in real-time

### For Developers

**Monitor a position:**
```python
from agent.monitor import PositionMonitor

monitor = PositionMonitor(web3, config)
positions = await monitor.get_user_positions("0x...")
```

**Get AI recommendation:**
```python
from agent.main import LiquidationPreventionAgent

agent = LiquidationPreventionAgent(config)
recommendation = await agent.get_claude_recommendation(position)
```

**Execute rebalancing:**
```python
from agent.executor import RebalanceExecutor

executor = RebalanceExecutor(web3, config)
result = await executor.execute_rebalance(user, protocol, amount)
```

## 🧪 Testing

**Smart Contracts:**
```bash
npx hardhat test
npx hardhat coverage
```

**Agent:**
```bash
cd agent
pytest tests/
```

**Frontend:**
```bash
cd frontend
npm test
```

## 📈 Demo Scenario

1. User has $10,000 ETH collateral, $6,000 USDC debt on Aave
2. Health factor: 1.3 (safe, but declining)
3. ETH price drops 15%
4. Health factor drops to 1.15 (risky)
5. **Agent detects risk** → sends to Claude for analysis
6. **Claude recommends** rebalancing $1,500 to reach HF 2.0
7. **Agent executes** flash loan rebalancing:
   - Flash borrow 1,500 USDC
   - Repay debt
   - Withdraw ETH collateral
   - Swap ETH → USDC
   - Repay flash loan
8. **New health factor: 2.05** ✅ Liquidation prevented!

## 🎥 Demo Video

[Link to 2-4 minute demo video - TO BE RECORDED]

## 📝 AI Attribution

All AI-generated decisions are logged in `docs/ai-attribution.jsonl`:

```json
{
  "timestamp": "2026-02-15T10:30:00Z",
  "model": "claude-3-5-sonnet-20241022",
  "position": {
    "user": "0x...",
    "protocol": "aave",
    "health_factor": 1.15
  },
  "recommendation": {
    "action": "rebalance",
    "reasoning": "Health factor critically low...",
    "urgency": "high"
  }
}
```

## 🏆 ETHDenver 2026 Submission

**Track**: Futurllama (AI + Crypto + DePIN)

**Differentiators**:
1. **Autonomous AI Loop**: Fully autonomous monitoring → analysis → execution
2. **Multi-Chain Support**: Works across Ethereum, Base, and Arbitrum
3. **Real-World Impact**: Prevents actual liquidations, saves users money
4. **Production Ready**: Complete testing, CI/CD, documentation

## 🚧 Roadmap

- [ ] Support for additional protocols (Maker, Morpho)
- [ ] Cross-chain rebalancing (bridge integration)
- [ ] DePIN oracle integration for price feeds
- [ ] Mobile app with push notifications
- [ ] DAO governance for parameter tuning
- [ ] Insurance fund for failed rebalances

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 👥 Team

Built for ETHDenver 2026 by the AI Office team.

## 🔗 Links

- **GitHub**: https://github.com/mgnlia/liquidation-prevention-agent
- **Demo**: [Coming soon]
- **Docs**: [docs/](docs/)
- **Contracts**: [Etherscan verification links]

## 🙏 Acknowledgments

- Anthropic for Claude API
- Aave V3 for flash loan infrastructure
- The Graph for data indexing
- ETHDenver & Futurllama for the opportunity

---

**Built with ❤️ for ETHDenver 2026**
