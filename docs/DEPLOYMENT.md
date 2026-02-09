# 🚀 Deployment Guide

## Prerequisites

### Required Accounts & Keys
- [ ] Alchemy/Infura account (Sepolia RPC URL)
- [ ] Etherscan API key
- [ ] Anthropic API key (Claude)
- [ ] The Graph Studio account
- [ ] Sepolia testnet ETH (0.5+ recommended)

### Required Software
```bash
node >= 18.0.0
npm >= 9.0.0
python >= 3.10
git
```

## Step 1: Environment Setup

### Contracts Environment
```bash
cd contracts
cp .env.example .env
```

Edit `contracts/.env`:
```env
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY
PRIVATE_KEY=your_deployer_private_key_without_0x
ETHERSCAN_API_KEY=your_etherscan_api_key

# Sepolia Addresses (Pre-configured)
AAVE_POOL_ADDRESS_PROVIDER=0x012bAC54348C0E635dCAc9D5FB99f06F24136C9A
COMPOUND_COMET_ADDRESS=0xAec1F48e02Cfb822Be958B68C7957156EB3F0b6e
```

### Agent Environment
```bash
cd agent
cp .env.example .env
```

Edit `agent/.env`:
```env
ANTHROPIC_API_KEY=sk-ant-xxxxx
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY
PRIVATE_KEY=your_agent_private_key_without_0x

# Will be populated after contract deployment
LIQUIDATION_PREVENTION_ADDRESS=
AAVE_ADAPTER_ADDRESS=
COMPOUND_ADAPTER_ADDRESS=
FLASH_LOAN_REBALANCER_ADDRESS=
```

### Frontend Environment
```bash
cd frontend
cp .env.example .env.local
```

Edit `frontend/.env.local`:
```env
NEXT_PUBLIC_SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY
NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID=your_walletconnect_project_id

# Will be populated after contract deployment
NEXT_PUBLIC_LIQUIDATION_PREVENTION_ADDRESS=
NEXT_PUBLIC_SUBGRAPH_URL=
```

## Step 2: Get Sepolia Testnet ETH

### Recommended Faucets
1. **Alchemy Sepolia Faucet**: https://sepoliafaucet.com/
2. **Infura Sepolia Faucet**: https://www.infura.io/faucet/sepolia
3. **Chainlink Faucet**: https://faucets.chain.link/sepolia

**Minimum Required:** 0.5 ETH (for deployment + testing)

Verify balance:
```bash
cast balance YOUR_ADDRESS --rpc-url $SEPOLIA_RPC_URL
```

## Step 3: Deploy Smart Contracts

### Install Dependencies
```bash
cd contracts
npm install
```

### Compile Contracts
```bash
npx hardhat compile
```

Expected output:
```
✓ Compiled 15 Solidity files successfully
```

### Run Tests (Optional but Recommended)
```bash
npx hardhat test
```

### Deploy to Sepolia
```bash
npx hardhat run scripts/deploy.js --network sepolia
```

**Expected Output:**
```
Deploying contracts to Sepolia...

AaveV3Adapter deployed to: 0x1234...
CompoundV3Adapter deployed to: 0x5678...
FlashLoanRebalancer deployed to: 0x9abc...
LiquidationPrevention deployed to: 0xdef0...

✅ All contracts deployed successfully!

Save these addresses to agent/.env and frontend/.env.local
```

### Verify Contracts on Etherscan
```bash
npx hardhat run scripts/verify.js --network sepolia
```

**Expected Output:**
```
Verifying contracts on Etherscan...

✅ AaveV3Adapter verified: https://sepolia.etherscan.io/address/0x1234...
✅ CompoundV3Adapter verified: https://sepolia.etherscan.io/address/0x5678...
✅ FlashLoanRebalancer verified: https://sepolia.etherscan.io/address/0x9abc...
✅ LiquidationPrevention verified: https://sepolia.etherscan.io/address/0xdef0...
```

## Step 4: Deploy Subgraph

### Install Graph CLI
```bash
npm install -g @graphprotocol/graph-cli
```

### Authenticate with The Graph Studio
```bash
graph auth --studio YOUR_DEPLOY_KEY
```

### Deploy Subgraph
```bash
cd subgraph
npm install

# Update subgraph.yaml with deployed contract addresses
# Then deploy:
graph codegen
graph build
graph deploy --studio liquidation-prevention-agent
```

**Save the subgraph URL** to `frontend/.env.local`:
```env
NEXT_PUBLIC_SUBGRAPH_URL=https://api.studio.thegraph.com/query/xxxxx/liquidation-prevention-agent/version/latest
```

## Step 5: Configure AI Agent

### Update Agent Configuration
Edit `agent/.env` with deployed contract addresses from Step 3.

### Install Python Dependencies
```bash
cd agent
pip install -r requirements.txt
```

### Test Agent Connection
```bash
python -c "from web3 import Web3; print(Web3(Web3.HTTPProvider('YOUR_RPC_URL')).is_connected())"
```

Expected: `True`

### Test Claude API
```bash
python -c "import anthropic; client = anthropic.Anthropic(api_key='YOUR_KEY'); print('✓ Claude API connected')"
```

## Step 6: Deploy Frontend

### Install Dependencies
```bash
cd frontend
npm install
```

### Build Production Bundle
```bash
npm run build
```

### Deploy to Vercel (Recommended)
```bash
npm install -g vercel
vercel --prod
```

Or deploy to Netlify:
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=out
```

## Step 7: End-to-End Testing

### 1. Start AI Agent
```bash
cd agent
python agent.py
```

Expected output:
```
🤖 AI Liquidation Prevention Agent Started
📊 Monitoring interval: 60s
🔗 Connected to Sepolia: 0xdef0...
✅ Agent ready
```

### 2. Open Frontend
Navigate to your deployed frontend URL or run locally:
```bash
cd frontend
npm run dev
# Open http://localhost:3000
```

### 3. Register Test Position

**Option A: Use Frontend**
1. Connect wallet (MetaMask)
2. Click "Register Position"
3. Approve transaction

**Option B: Use Hardhat Console**
```bash
cd contracts
npx hardhat console --network sepolia
```

```javascript
const LiquidationPrevention = await ethers.getContractFactory("LiquidationPrevention");
const contract = LiquidationPrevention.attach("YOUR_DEPLOYED_ADDRESS");
await contract.registerPosition();
```

### 4. Monitor Agent Logs
Watch for:
```
📊 Fetching positions from subgraph...
✅ Found 1 position(s) to monitor
🔍 Analyzing position 0x1234... (HF: 2.15)
✅ Position healthy - no action needed
```

### 5. Test Risk Scenario (Optional)
To trigger AI analysis:
1. Borrow near liquidation threshold on Aave Sepolia
2. Wait for agent to detect (< 60s)
3. Agent should suggest rebalancing strategy

## Troubleshooting

### "Insufficient funds for gas"
- Get more Sepolia ETH from faucets
- Check balance: `cast balance YOUR_ADDRESS --rpc-url $SEPOLIA_RPC_URL`

### "Contract not verified"
- Wait 1-2 minutes after deployment
- Re-run: `npx hardhat run scripts/verify.js --network sepolia`

### "Subgraph indexing failed"
- Check contract addresses in `subgraph/subgraph.yaml`
- Verify events are emitting: Check Etherscan contract logs

### "Agent not fetching positions"
- Verify subgraph is synced: Check The Graph Studio dashboard
- Test RPC connection: `curl -X POST $SEPOLIA_RPC_URL -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'`

### "Claude API errors"
- Verify API key: https://console.anthropic.com/
- Check rate limits (free tier: 5 req/min)

## Production Checklist

- [ ] All contracts deployed to Sepolia
- [ ] All contracts verified on Etherscan
- [ ] Subgraph deployed and syncing
- [ ] Agent running with valid API keys
- [ ] Frontend deployed and accessible
- [ ] Test position registered successfully
- [ ] Agent detected and analyzed position
- [ ] Documentation complete (README, DEMO.md, AI_ATTRIBUTION.md)
- [ ] Video demo recorded (2-4 minutes)
- [ ] GitHub repo public with clean commit history

## Deployment Costs (Sepolia)

| Component | Gas Cost | USD Equivalent (Testnet) |
|-----------|----------|--------------------------|
| AaveV3Adapter | ~1.2M gas | $0 (testnet) |
| CompoundV3Adapter | ~1.1M gas | $0 (testnet) |
| FlashLoanRebalancer | ~2.5M gas | $0 (testnet) |
| LiquidationPrevention | ~1.8M gas | $0 (testnet) |
| **Total** | **~6.6M gas** | **$0 (testnet)** |

**Mainnet Estimate:** ~$150-250 (at 30 gwei, ETH @ $3000)

## Next Steps

After successful deployment:
1. Update `README.md` with live links
2. Record demo video following `DEMO.md` script
3. Submit to HackMoney 2026
4. Share on Twitter/Discord

## Support

Issues? Check:
- [GitHub Issues](https://github.com/mgnlia/liquidation-prevention-agent/issues)
- [HackMoney Discord](https://discord.gg/ethglobal)
- [Documentation](./ARCHITECTURE.md)
