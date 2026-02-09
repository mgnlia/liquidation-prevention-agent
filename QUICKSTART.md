# ⚡ Quick Start Guide

Get the AI Liquidation Prevention Agent running in **under 10 minutes**.

---

## 🎯 What You'll Build

A working demo that:
1. Monitors a DeFi position on Aave V3 (Sepolia)
2. Uses Claude AI to analyze liquidation risk
3. Executes automated rebalancing via flash loans

---

## 📋 Prerequisites

### Required
- **Node.js** 18+ ([download](https://nodejs.org/))
- **Python** 3.10+ ([download](https://www.python.org/))
- **Git** ([download](https://git-scm.com/))
- **MetaMask** or similar Web3 wallet

### Required API Keys (Free Tier OK)
- [ ] **Alchemy/Infura** - Sepolia RPC ([sign up](https://www.alchemy.com/))
- [ ] **Etherscan** - Contract verification ([sign up](https://etherscan.io/apis))
- [ ] **Anthropic** - Claude API ([sign up](https://console.anthropic.com/))

### Required Testnet Assets
- [ ] **Sepolia ETH** - 0.5+ from [faucets](https://sepoliafaucet.com/)

---

## 🚀 5-Step Setup

### Step 1: Clone & Install (2 min)

```bash
# Clone repo
git clone https://github.com/mgnlia/liquidation-prevention-agent.git
cd liquidation-prevention-agent

# Install contracts
cd contracts
npm install

# Install agent
cd ../agent
pip install -r requirements.txt

# Install frontend (optional)
cd ../frontend
npm install
```

---

### Step 2: Configure Environment (2 min)

#### Contracts Config
```bash
cd contracts
cp .env.example .env
nano .env  # or use your favorite editor
```

Add:
```env
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
PRIVATE_KEY=your_private_key_without_0x_prefix
ETHERSCAN_API_KEY=your_etherscan_api_key
```

#### Agent Config
```bash
cd ../agent
cp .env.example .env
nano .env
```

Add:
```env
ANTHROPIC_API_KEY=sk-ant-your_claude_api_key
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
PRIVATE_KEY=your_private_key_without_0x_prefix
```

---

### Step 3: Deploy Contracts (3 min)

```bash
cd contracts

# Compile
npx hardhat compile

# Deploy to Sepolia
npx hardhat run scripts/deploy.js --network sepolia
```

**Save the output addresses!** Example:
```
AaveV3Adapter deployed to: 0x1234...
CompoundV3Adapter deployed to: 0x5678...
FlashLoanRebalancer deployed to: 0x9abc...
LiquidationPrevention deployed to: 0xdef0...
```

Update `agent/.env`:
```env
LIQUIDATION_PREVENTION_ADDRESS=0xdef0...
AAVE_ADAPTER_ADDRESS=0x1234...
COMPOUND_ADAPTER_ADDRESS=0x5678...
FLASH_LOAN_REBALANCER_ADDRESS=0x9abc...
```

---

### Step 4: Verify Contracts (1 min)

```bash
npx hardhat run scripts/verify.js --network sepolia
```

Check Etherscan for verified contracts ✅

---

### Step 5: Run AI Agent (2 min)

```bash
cd ../agent
python agent.py
```

Expected output:
```
🤖 AI Liquidation Prevention Agent Started
📊 Monitoring interval: 60s
🔗 Connected to Sepolia
✅ Agent ready - waiting for positions...
```

---

## 🧪 Test the System

### Option A: Register Position via Script

```bash
cd contracts
npx hardhat console --network sepolia
```

In console:
```javascript
const LP = await ethers.getContractFactory("LiquidationPrevention");
const lp = LP.attach("YOUR_DEPLOYED_ADDRESS");
await lp.registerPosition();
```

### Option B: Use Frontend (Recommended)

```bash
cd frontend
npm run dev
# Open http://localhost:3000
```

1. Connect wallet
2. Click "Register Position"
3. Approve transaction

---

## 📊 Monitor Agent Activity

Watch terminal for:
```
📊 Fetching positions...
✅ Found 1 position(s)

🔍 Analyzing position 0x1234...
   Protocol: Aave V3
   Health Factor: 2.15
   Risk Level: LOW
   
✅ Position healthy - no action needed
```

---

## 🎬 Trigger a Demo Scenario

### Simulate Liquidation Risk

1. **Go to Aave V3 Sepolia:** https://app.aave.com/?marketName=proto_sepolia_v3
2. **Borrow more assets** to lower your health factor
3. **Watch agent detect it** within 60 seconds:

```
⚠️  RISK DETECTED!
   Health Factor: 1.28
   
🤖 Claude AI Strategy:
   "Recommend flash loan rebalancing:
    - Borrow 500 USDC
    - Repay debt
    - Improve HF to 1.55"
   
🚀 Executing rebalancing...
✅ Transaction: 0xabc123...
```

4. **Check Etherscan** for the rebalancing transaction

---

## 🎯 Next Steps

### For Demo Video
- Follow [DEMO.md](./docs/DEMO.md) script
- Record agent logs + Etherscan transactions
- Show before/after health factor

### For Development
- Read [ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- Add more protocols (see `/contracts/adapters/`)
- Customize AI prompts (see `/agent/analyzer.py`)

### For Deployment
- Follow [DEPLOYMENT.md](./docs/DEPLOYMENT.md)
- Deploy subgraph to The Graph Studio
- Host frontend on Vercel/Netlify

---

## 🐛 Troubleshooting

### "Insufficient funds for gas"
```bash
# Check balance
cast balance YOUR_ADDRESS --rpc-url $SEPOLIA_RPC_URL

# Get testnet ETH
# Visit: https://sepoliafaucet.com/
```

### "Contract verification failed"
```bash
# Wait 1-2 minutes, then retry
npx hardhat run scripts/verify.js --network sepolia
```

### "Claude API rate limit"
Free tier: 5 requests/min. Wait 60s between tests or upgrade plan.

### "Agent not detecting positions"
1. Check subgraph is deployed (or use RPC fallback)
2. Verify contract addresses in `agent/.env`
3. Ensure position is registered on-chain

---

## 📚 Full Documentation

- **Architecture:** [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- **Deployment:** [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)
- **Demo Script:** [docs/DEMO.md](./docs/DEMO.md)
- **AI Attribution:** [docs/AI_ATTRIBUTION.md](./docs/AI_ATTRIBUTION.md)

---

## 🏆 HackMoney 2026 Submission

This project targets:
- 🥇 **Aave Grants DAO** - Flash loan innovation
- 🥇 **Anthropic** - Autonomous AI agents
- 🥈 **The Graph** - Position indexing

---

## 💬 Support

- **Issues:** [GitHub Issues](https://github.com/mgnlia/liquidation-prevention-agent/issues)
- **Discord:** [ETHGlobal Discord](https://discord.gg/ethglobal)
- **Docs:** [Full Documentation](./docs/)

---

**Built with ❤️ for HackMoney 2026**
