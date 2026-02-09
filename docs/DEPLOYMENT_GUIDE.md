# 🚀 Deployment Guide

Complete guide for deploying the AI-Powered Liquidation Prevention Agent to testnets and mainnet.

## Prerequisites

### 1. Get Testnet ETH

**Sepolia:**
- https://sepoliafaucet.com/
- https://www.alchemy.com/faucets/ethereum-sepolia

**Base Sepolia:**
- https://www.coinbase.com/faucets/base-ethereum-sepolia-faucet
- Bridge from Sepolia: https://bridge.base.org/

**Arbitrum Sepolia:**
- https://faucet.quicknode.com/arbitrum/sepolia
- Bridge from Sepolia: https://bridge.arbitrum.io/

### 2. Get API Keys

**Etherscan/Basescan/Arbiscan** (for verification):
- Etherscan: https://etherscan.io/myapikey
- Basescan: https://basescan.org/myapikey
- Arbiscan: https://arbiscan.io/myapikey

**Anthropic Claude API**:
- https://console.anthropic.com/
- Get API key from Account Settings

**RPC Providers** (optional, for better reliability):
- Alchemy: https://www.alchemy.com/
- Infura: https://infura.io/
- QuickNode: https://www.quicknode.com/

## Step-by-Step Deployment

### 1. Environment Setup

Create `.env` file:

```bash
# Network Configuration
NETWORK=sepolia

# RPC URLs (use public or your own)
SEPOLIA_RPC_URL=https://rpc.sepolia.org
BASE_SEPOLIA_RPC_URL=https://sepolia.base.org
ARBITRUM_SEPOLIA_RPC_URL=https://sepolia-rollup.arbitrum.io/rpc

# Deployment Wallet
PRIVATE_KEY=0x... # Your private key (NEVER commit this!)

# API Keys for Verification
ETHERSCAN_API_KEY=ABC123...
BASESCAN_API_KEY=ABC123...
ARBISCAN_API_KEY=ABC123...

# AI Agent Configuration
ANTHROPIC_API_KEY=sk-ant-...
CHECK_INTERVAL=60
MIN_HEALTH_FACTOR=1.5
TARGET_HEALTH_FACTOR=2.0

# Multi-chain Support
SUPPORTED_CHAINS=sepolia,baseSepolia,arbitrumSepolia
```

### 2. Install Dependencies

```bash
npm install
cd agent && pip install -r requirements.txt && cd ..
cd frontend && npm install && cd ..
```

### 3. Compile Contracts

```bash
npx hardhat compile
```

Expected output:
```
Compiled 15 Solidity files successfully
```

### 4. Deploy to Sepolia

```bash
npx hardhat run scripts/deploy.js --network sepolia
```

**Expected Output:**
```
Deploying contracts with account: 0x...
Network: sepolia
Account balance: 1000000000000000000

1. Deploying AaveAdapter...
AaveAdapter deployed to: 0xABC...

2. Deploying CompoundAdapter...
CompoundAdapter deployed to: 0xDEF...

3. Deploying FlashLoanRebalancer...
FlashLoanRebalancer deployed to: 0xGHI...

4. Deploying LiquidationPrevention...
LiquidationPrevention deployed to: 0xJKL...

5. Configuring FlashLoanRebalancer...
FlashLoanRebalancer configured

=== DEPLOYMENT SUMMARY ===
Network: sepolia
AaveAdapter: 0xABC...
CompoundAdapter: 0xDEF...
FlashLoanRebalancer: 0xGHI...
LiquidationPrevention: 0xJKL...
```

**Save these addresses!** You'll need them for:
- Agent configuration
- Frontend configuration
- Contract verification

### 5. Verify Contracts on Etherscan

```bash
# Verify AaveAdapter
npx hardhat verify --network sepolia <AAVE_ADAPTER_ADDRESS> 0x012bAC54348C0E635dCAc9D5FB99f06F24136C9A

# Verify CompoundAdapter
npx hardhat verify --network sepolia <COMPOUND_ADAPTER_ADDRESS> 0xAec1F48e02Cfb822Be958B68C7957156EB3F0b6e

# Verify FlashLoanRebalancer
npx hardhat verify --network sepolia <FLASH_LOAN_REBALANCER_ADDRESS> 0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951

# Verify LiquidationPrevention
npx hardhat verify --network sepolia <LIQUIDATION_PREVENTION_ADDRESS> <AAVE_ADAPTER_ADDRESS> <COMPOUND_ADAPTER_ADDRESS> <FLASH_LOAN_REBALANCER_ADDRESS>
```

### 6. Deploy to Base Sepolia

```bash
npx hardhat run scripts/deploy.js --network baseSepolia
```

Then verify:
```bash
npx hardhat verify --network baseSepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

### 7. Deploy to Arbitrum Sepolia

```bash
npx hardhat run scripts/deploy.js --network arbitrumSepolia
```

Then verify:
```bash
npx hardhat verify --network arbitrumSepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

### 8. Configure Agent

Update `.env` with deployed addresses:

```env
# Sepolia Contracts
LIQUIDATION_PREVENTION_ADDRESS=0x...
AAVE_ADAPTER_ADDRESS=0x...
COMPOUND_ADAPTER_ADDRESS=0x...

# Base Sepolia Contracts (if deployed)
BASE_LIQUIDATION_PREVENTION_ADDRESS=0x...
BASE_AAVE_ADAPTER_ADDRESS=0x...

# Arbitrum Sepolia Contracts (if deployed)
ARBITRUM_LIQUIDATION_PREVENTION_ADDRESS=0x...
ARBITRUM_AAVE_ADAPTER_ADDRESS=0x...
```

### 9. Test Agent Locally

```bash
cd agent
python main.py
```

Expected output:
```
🤖 Starting Liquidation Prevention Agent on sepolia
📊 Monitoring interval: 60s

🔍 Monitoring cycle at 2026-02-15T10:00:00
👤 Checking user: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
✅ No positions at risk
```

### 10. Deploy Frontend

**Local:**
```bash
cd frontend
npm run dev
```

**Production (Vercel):**
```bash
cd frontend
vercel --prod
```

**Production (Netlify):**
```bash
cd frontend
npm run build
netlify deploy --prod --dir=build
```

## Post-Deployment Checklist

- [ ] All contracts deployed and verified on Etherscan
- [ ] Contract addresses saved in `.env`
- [ ] Agent successfully connects to contracts
- [ ] Frontend connects to deployed contracts
- [ ] Test transaction executed successfully
- [ ] AI attribution logging working
- [ ] Multi-chain support tested (if applicable)

## Testing Deployment

### 1. Test Contract Interaction

```bash
npx hardhat console --network sepolia
```

```javascript
const LiquidationPrevention = await ethers.getContractFactory("LiquidationPrevention");
const lp = await LiquidationPrevention.attach("0x...");

// Set user config
await lp.setUserConfig(
  ethers.parseEther("1.5"),  // min health factor
  ethers.parseEther("2.0"),  // target health factor
  true,  // enable Aave
  true   // enable Compound
);

// Check health factors
const result = await lp.getUserHealthFactors("0x...");
console.log("Aave HF:", ethers.formatEther(result[0]));
console.log("Compound HF:", ethers.formatEther(result[1]));
```

### 2. Test Agent Monitoring

Create a test user with a position:

```bash
cd agent
python -c "
from main import LiquidationPreventionAgent
from config import Config
import asyncio

async def test():
    config = Config.from_env()
    agent = LiquidationPreventionAgent(config)
    positions = await agent.monitor.get_user_positions('0x...')
    print(f'Found {len(positions)} positions')

asyncio.run(test())
"
```

### 3. Test AI Analysis

```bash
cd agent
python -c "
from main import LiquidationPreventionAgent, UserPosition
from config import Config
from datetime import datetime
import asyncio

async def test():
    config = Config.from_env()
    agent = LiquidationPreventionAgent(config)
    
    # Create test position
    position = UserPosition(
        address='0x...',
        protocol='aave',
        health_factor=1.2,
        total_collateral=10000,
        total_debt=7000,
        at_risk=True,
        timestamp=datetime.now()
    )
    
    recommendation = await agent.get_claude_recommendation(position)
    print(f'Claude recommends: {recommendation}')

asyncio.run(test())
"
```

## Troubleshooting

### Common Issues

**1. "Insufficient funds for gas"**
- Get more testnet ETH from faucets
- Check your wallet balance: `npx hardhat run scripts/check-balance.js --network sepolia`

**2. "Contract verification failed"**
- Ensure constructor arguments match deployment
- Check Solidity version matches (0.8.20)
- Try manual verification on Etherscan UI

**3. "Agent can't connect to contract"**
- Verify contract addresses in `.env`
- Check RPC URL is correct
- Ensure ABI files are in correct location

**4. "Claude API error"**
- Verify `ANTHROPIC_API_KEY` is correct
- Check API quota/limits
- Test API key: `curl https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY"`

**5. "Transaction reverted"**
- Check health factor is actually below threshold
- Ensure user has enabled auto-rebalance
- Verify agent is authorized: `lp.authorizedAgents(agentAddress)`

### Getting Help

- Check logs in `agent/logs/`
- Review AI attribution: `docs/ai-attribution.jsonl`
- Test contracts: `npx hardhat test`
- Verify on block explorer

## Security Considerations

### Before Mainnet Deployment

1. **Audit Contracts**: Get professional security audit
2. **Test Thoroughly**: Run on testnets for weeks
3. **Limit Exposure**: Start with small position limits
4. **Monitor Closely**: Set up alerting for failures
5. **Emergency Pause**: Implement pause mechanism
6. **Insurance Fund**: Consider integrating with Nexus Mutual

### Operational Security

- **Never commit private keys** to git
- Use **hardware wallet** for mainnet deployment
- Implement **multi-sig** for contract ownership
- Set up **monitoring** and **alerting**
- Have **incident response** plan

## Mainnet Deployment (When Ready)

```bash
# 1. Deploy to mainnet
NETWORK=mainnet npx hardhat run scripts/deploy.js --network mainnet

# 2. Verify contracts
npx hardhat verify --network mainnet <CONTRACT_ADDRESS> <ARGS>

# 3. Transfer ownership to multi-sig
npx hardhat run scripts/transfer-ownership.js --network mainnet

# 4. Start agent with production config
cd agent
NETWORK=mainnet python main.py
```

## Cost Estimates

**Deployment (per network):**
- AaveAdapter: ~0.002 ETH
- CompoundAdapter: ~0.002 ETH
- FlashLoanRebalancer: ~0.003 ETH
- LiquidationPrevention: ~0.004 ETH
- **Total: ~0.011 ETH** (~$35 at $3000 ETH)

**Operational:**
- Agent monitoring: Free (just RPC calls)
- Claude API: ~$0.01 per analysis
- Rebalancing tx: ~0.001-0.005 ETH + flash loan fee (0.09%)

---

**Ready to deploy? Let's prevent some liquidations! 🛡️**
