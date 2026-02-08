# 🚀 Deployment Guide

Complete guide for deploying the AI-Powered Liquidation Prevention Agent to Sepolia testnet.

## Prerequisites

### Required Tools
```bash
node >= 18.0.0
npm >= 9.0.0
python >= 3.10
git
```

### API Keys & Accounts
1. **Alchemy/Infura** - Sepolia RPC endpoint
2. **Etherscan** - API key for contract verification
3. **Anthropic** - Claude API key
4. **MetaMask** - Wallet with Sepolia ETH

### Get Testnet ETH
```bash
# Sepolia Faucets:
# https://sepoliafaucet.com/
# https://www.alchemy.com/faucets/ethereum-sepolia
# https://faucet.quicknode.com/ethereum/sepolia
```

## Step 1: Clone & Install

```bash
# Clone repository
git clone https://github.com/mgnlia/liquidation-prevention-agent.git
cd liquidation-prevention-agent

# Install contract dependencies
cd contracts
npm install

# Install agent dependencies
cd ../agent
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

## Step 2: Environment Configuration

### Contracts Environment

Create `contracts/.env`:

```bash
# Network Configuration
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
PRIVATE_KEY=your_private_key_here
ETHERSCAN_API_KEY=your_etherscan_api_key

# Sepolia Contract Addresses (Official)
AAVE_V3_POOL=0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951
AAVE_V3_POOL_ADDRESSES_PROVIDER=0x012bAC54348C0E635dCAc9D5FB99f06F24136C9A
COMPOUND_V3_COMET_USDC=0xAec1F48e02Cfb822Be958B68C7957156EB3F0b6e

# Deployment Configuration
AI_AGENT_ADDRESS=0xYourAgentWalletAddress
HEALTH_FACTOR_THRESHOLD=1500000000000000000  # 1.5 in wei (18 decimals)
```

### Agent Environment

Create `agent/.env`:

```bash
# Blockchain Configuration
WEB3_PROVIDER_URI=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
CHAIN_ID=11155111
NETWORK_NAME=sepolia

# Contract Addresses (will be filled after deployment)
LIQUIDATION_PREVENTION_ADDRESS=
AAVE_ADAPTER_ADDRESS=
COMPOUND_ADAPTER_ADDRESS=
FLASH_LOAN_REBALANCER_ADDRESS=

# Agent Configuration
AGENT_PRIVATE_KEY=your_agent_wallet_private_key
ANTHROPIC_API_KEY=sk-ant-your-claude-api-key

# Monitoring Configuration
MONITOR_INTERVAL_SECONDS=60
HEALTH_FACTOR_THRESHOLD=1.5
MIN_AGENT_BALANCE_ETH=0.1

# The Graph (optional - for production)
SUBGRAPH_URL=https://api.studio.thegraph.com/query/YOUR_SUBGRAPH
```

### Frontend Environment

Create `frontend/.env.local`:

```bash
NEXT_PUBLIC_CHAIN_ID=11155111
NEXT_PUBLIC_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
NEXT_PUBLIC_LIQUIDATION_PREVENTION_ADDRESS=
NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID=your_walletconnect_project_id
```

## Step 3: Deploy Smart Contracts

### Compile Contracts

```bash
cd contracts
npx hardhat compile
```

Expected output:
```
Compiled 12 Solidity files successfully
```

### Run Tests

```bash
npx hardhat test
```

All tests should pass ✅

### Deploy to Sepolia

```bash
npx hardhat run scripts/deploy.js --network sepolia
```

**Expected Output:**
```
🚀 Deploying Liquidation Prevention System to sepolia...

📋 Deployment Configuration:
   Network: sepolia (11155111)
   Deployer: 0x...
   Balance: 1.5 ETH

📦 Deploying Contracts...

✅ AaveV3Adapter deployed to: 0x...
✅ CompoundV3Adapter deployed to: 0x...
✅ FlashLoanRebalancer deployed to: 0x...
✅ LiquidationPrevention deployed to: 0x...

💾 Saving deployment addresses...
✅ Deployment complete!

📝 Contract Addresses:
{
  "network": "sepolia",
  "chainId": 11155111,
  "contracts": {
    "LiquidationPrevention": "0x...",
    "AaveV3Adapter": "0x...",
    "CompoundV3Adapter": "0x...",
    "FlashLoanRebalancer": "0x..."
  },
  "timestamp": "2026-01-30T..."
}
```

**Important:** Save these addresses! You'll need them for:
- Agent configuration
- Frontend configuration
- Etherscan verification

### Verify on Etherscan

```bash
npx hardhat run scripts/verify.js --network sepolia
```

This will verify all 4 contracts on Etherscan, making them publicly viewable and trustworthy.

**Verification URLs:**
- LiquidationPrevention: `https://sepolia.etherscan.io/address/0x...#code`
- AaveV3Adapter: `https://sepolia.etherscan.io/address/0x...#code`
- CompoundV3Adapter: `https://sepolia.etherscan.io/address/0x...#code`
- FlashLoanRebalancer: `https://sepolia.etherscan.io/address/0x...#code`

## Step 4: Update Configuration

### Update Agent .env

After deployment, update `agent/.env` with deployed addresses:

```bash
LIQUIDATION_PREVENTION_ADDRESS=0xYourDeployedAddress
AAVE_ADAPTER_ADDRESS=0xYourDeployedAddress
COMPOUND_ADAPTER_ADDRESS=0xYourDeployedAddress
FLASH_LOAN_REBALANCER_ADDRESS=0xYourDeployedAddress
```

### Update Frontend .env.local

```bash
NEXT_PUBLIC_LIQUIDATION_PREVENTION_ADDRESS=0xYourDeployedAddress
```

## Step 5: Deploy The Graph Subgraph (Optional)

For production-grade monitoring, deploy a subgraph:

```bash
cd subgraph

# Install Graph CLI
npm install -g @graphprotocol/graph-cli

# Authenticate
graph auth --studio YOUR_DEPLOY_KEY

# Create subgraph
graph create --studio liquidation-prevention-agent

# Deploy
graph codegen
graph build
graph deploy --studio liquidation-prevention-agent
```

Update agent `.env`:
```bash
SUBGRAPH_URL=https://api.studio.thegraph.com/query/YOUR_SUBGRAPH_ID/liquidation-prevention-agent/v0.0.1
```

## Step 6: Start the AI Agent

```bash
cd agent
python agent.py
```

**Expected Output:**
```
╔════════════════════════════════════════════════════════════╗
║   AI-POWERED LIQUIDATION PREVENTION AGENT                  ║
║   HackMoney 2026                                           ║
║   Autonomous DeFi Position Protection                      ║
╚════════════════════════════════════════════════════════════╝

🤖 Initializing AI Liquidation Prevention Agent...
✅ Agent initialized successfully

============================================================
🚀 LIQUIDATION PREVENTION AGENT STARTING
============================================================

💰 Agent Wallet: 0x...
   Balance: 0.5000 ETH

⏱️  Monitor Interval: 60s
🎯 Health Factor Threshold: 1.5

============================================================
🔄 MONITORING CYCLE - 2026-01-30 10:00:00
============================================================

ℹ️  No registered users found. Waiting for registrations...
```

The agent is now running and will automatically monitor registered positions!

## Step 7: Start the Frontend

```bash
cd frontend
npm run dev
```

Open http://localhost:3000

## Step 8: Test the System

### Register a Test Position

1. Go to frontend dashboard
2. Connect wallet (MetaMask on Sepolia)
3. Click "Register Position"
4. Select protocols to monitor (Aave V3, Compound V3)
5. Confirm transaction

### Create a Test Position on Aave

```bash
# 1. Go to Aave V3 Sepolia
https://app.aave.com/?marketName=proto_sepolia_v3

# 2. Get test tokens from faucet
https://staging.aave.com/faucet/

# 3. Supply collateral (e.g., 1 ETH)
# 4. Borrow stablecoins (e.g., 500 USDC)
# 5. Monitor your health factor
```

### Watch the Agent Work

The agent will:
1. Detect your registered position
2. Monitor health factor every 60s
3. Analyze risk using Claude API
4. Suggest rebalancing if HF < 1.5
5. Execute flash loan rebalancing if critical

**Agent Console Output:**
```
============================================================
🔄 MONITORING CYCLE - 2026-01-30 10:01:00
============================================================

👥 Monitoring 1 registered user(s)

📊 Checking position: 0xYourAddress
   Health Factor: 2.3456
   Risk Level: LOW
   Position is healthy. Continue monitoring.

✅ All positions healthy

⏱️  Cycle completed in 3.45s
============================================================
```

## Step 9: Deploy Frontend (Production)

### Deploy to Vercel

```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### Deploy to Netlify

```bash
cd frontend

# Build
npm run build

# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=out
```

## Deployment Checklist

- [ ] Sepolia testnet ETH obtained (>0.5 ETH)
- [ ] All environment variables configured
- [ ] Contracts compiled successfully
- [ ] Tests passing
- [ ] Contracts deployed to Sepolia
- [ ] Contracts verified on Etherscan
- [ ] Agent .env updated with contract addresses
- [ ] Frontend .env.local updated
- [ ] AI agent running
- [ ] Frontend running
- [ ] Test position registered
- [ ] Agent successfully monitoring
- [ ] (Optional) Subgraph deployed
- [ ] (Optional) Frontend deployed to production

## Troubleshooting

### Contract Deployment Fails

**Error:** `insufficient funds for gas`
- **Solution:** Get more Sepolia ETH from faucets

**Error:** `nonce too low`
- **Solution:** Reset MetaMask nonce or wait for pending tx

### Agent Connection Issues

**Error:** `HTTPError: 401 Unauthorized`
- **Solution:** Check ANTHROPIC_API_KEY is valid

**Error:** `Web3 connection failed`
- **Solution:** Verify SEPOLIA_RPC_URL is correct

### No Positions Detected

- Ensure you called `registerUser()` on the contract
- Check agent is using correct contract address
- Verify wallet has Sepolia ETH for gas

## Production Considerations

### Security
- Use hardware wallet for deployer
- Use separate agent wallet with limited funds
- Enable timelock for contract upgrades
- Conduct security audit before mainnet

### Monitoring
- Set up Sentry for error tracking
- Use Grafana for metrics dashboard
- Enable alerting for critical events

### Scaling
- Use Redis for caching position data
- Deploy multiple agent instances
- Use WebSocket for real-time updates
- Optimize gas usage

## Support

- **Documentation:** [GitHub Wiki](https://github.com/mgnlia/liquidation-prevention-agent/wiki)
- **Issues:** [GitHub Issues](https://github.com/mgnlia/liquidation-prevention-agent/issues)
- **Discord:** [Join our community](#)

---

**Built for HackMoney 2026** 🏆
