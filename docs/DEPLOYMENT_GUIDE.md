# 🚀 Deployment Guide - Liquidation Prevention Agent

Complete guide for deploying the AI-Powered Liquidation Prevention Agent to testnets and mainnet.

---

## 📋 Prerequisites

### Required Tools
```bash
node >= 18.0.0
npm >= 9.0.0
python >= 3.11
git
```

### Required Accounts
- Ethereum wallet with testnet ETH
- Anthropic API key (Claude)
- Etherscan API key
- RPC provider (Alchemy/Infura) - optional but recommended

### Get Testnet Funds
- **Sepolia:** https://sepoliafaucet.com/
- **Base Sepolia:** https://portal.cdp.coinbase.com/products/faucet
- **Arbitrum Sepolia:** https://faucet.quicknode.com/arbitrum/sepolia

---

## 🔧 Setup

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
cd ..
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 3. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your values:
```env
# Network
NETWORK=sepolia
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY
BASE_SEPOLIA_RPC_URL=https://base-sepolia.g.alchemy.com/v2/YOUR_KEY
ARBITRUM_SEPOLIA_RPC_URL=https://arb-sepolia.g.alchemy.com/v2/YOUR_KEY

# Deployment (DO NOT commit this file!)
PRIVATE_KEY=your_private_key_without_0x_prefix

# API Keys
ETHERSCAN_API_KEY=your_etherscan_api_key
BASESCAN_API_KEY=your_basescan_api_key
ARBISCAN_API_KEY=your_arbiscan_api_key
ANTHROPIC_API_KEY=sk-ant-your-claude-api-key

# Agent Configuration
CHECK_INTERVAL=60
MIN_HEALTH_FACTOR=1.5
TARGET_HEALTH_FACTOR=2.0
```

**⚠️ SECURITY WARNING:**
- Never commit `.env` to git
- Use a separate wallet for deployment (not your main wallet)
- For mainnet, use hardware wallet or secure key management

---

## 📦 Contract Deployment

### Sepolia Testnet

**1. Compile Contracts:**
```bash
npx hardhat compile
```

**2. Deploy:**
```bash
npx hardhat run scripts/deploy.js --network sepolia
```

**Expected Output:**
```
🚀 Deploying Liquidation Prevention Agent...
Network: sepolia
Deploying with account: 0x...

📦 Deploying AaveAdapter...
✅ AaveAdapter deployed to: 0xABC...

📦 Deploying CompoundAdapter...
✅ CompoundAdapter deployed to: 0xDEF...

📦 Deploying FlashLoanRebalancer...
✅ FlashLoanRebalancer deployed to: 0xGHI...

📦 Deploying LiquidationPrevention...
✅ LiquidationPrevention deployed to: 0xJKL...

🔧 Configuring permissions...
✅ Authorized LiquidationPrevention on FlashLoanRebalancer

🎉 Deployment Complete!
```

**3. Save Contract Addresses:**

Copy the addresses to your `.env`:
```env
LIQUIDATION_PREVENTION_ADDRESS=0xJKL...
AAVE_ADAPTER_ADDRESS=0xABC...
COMPOUND_ADAPTER_ADDRESS=0xDEF...
FLASH_LOAN_REBALANCER_ADDRESS=0xGHI...
```

**4. Verify Contracts:**
```bash
npx hardhat verify --network sepolia <AAVE_ADAPTER_ADDRESS> 0x0496275d34753A48320CA58103d5220d394FF77F

npx hardhat verify --network sepolia <COMPOUND_ADAPTER_ADDRESS> 0x0000000000000000000000000000000000000000

npx hardhat verify --network sepolia <FLASH_LOAN_REBALANCER_ADDRESS> <AAVE_POOL_ADDRESS> <AAVE_ADAPTER_ADDRESS> <COMPOUND_ADAPTER_ADDRESS>

npx hardhat verify --network sepolia <LIQUIDATION_PREVENTION_ADDRESS> <AAVE_ADAPTER_ADDRESS> <COMPOUND_ADAPTER_ADDRESS> <FLASH_LOAN_REBALANCER_ADDRESS>
```

---

### Base Sepolia

**Deploy:**
```bash
npx hardhat run scripts/deploy.js --network baseSepolia
```

**Verify:**
```bash
npx hardhat verify --network baseSepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

---

### Arbitrum Sepolia

**Deploy:**
```bash
npx hardhat run scripts/deploy.js --network arbitrumSepolia
```

**Verify:**
```bash
npx hardhat verify --network arbitrumSepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

---

## 🤖 AI Agent Setup

### 1. Configure Agent

Edit `agent/config.py` or use environment variables:
```python
class Config:
    # Network
    network = "sepolia"
    rpc_url = os.getenv("SEPOLIA_RPC_URL")
    
    # Contracts
    liquidation_prevention_address = os.getenv("LIQUIDATION_PREVENTION_ADDRESS")
    
    # AI
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    # Monitoring
    check_interval = 60  # seconds
    min_health_factor = 1.5
    target_health_factor = 2.0
```

### 2. Test Agent Locally

**Run in test mode:**
```bash
cd agent
python main.py --test
```

**Expected Output:**
```
🤖 Starting Liquidation Prevention Agent on sepolia
📊 Monitoring interval: 60s

🔍 Monitoring cycle at 2026-02-15T10:30:00Z
👤 Checking user: 0x...
✅ All positions healthy
```

### 3. Add Test Position

**Option A: Use your own wallet**
1. Get Sepolia ETH from faucet
2. Deposit collateral on Aave Sepolia
3. Borrow against it
4. Enable auto-rebalance in contract

**Option B: Monitor existing positions**
```bash
python scripts/add_monitored_user.py --address 0x...
```

### 4. Run Agent in Production

**Using systemd (Linux):**
```bash
# Create service file
sudo nano /etc/systemd/system/liquidation-agent.service
```

```ini
[Unit]
Description=Liquidation Prevention Agent
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/liquidation-prevention-agent/agent
Environment="ANTHROPIC_API_KEY=your_key"
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable liquidation-agent
sudo systemctl start liquidation-agent
sudo systemctl status liquidation-agent
```

**Using Docker:**
```bash
# Build image
docker build -t liquidation-agent ./agent

# Run container
docker run -d \
  --name liquidation-agent \
  --env-file .env \
  --restart unless-stopped \
  liquidation-agent
```

**Using PM2 (Node.js process manager):**
```bash
npm install -g pm2
pm2 start agent/main.py --interpreter python3 --name liquidation-agent
pm2 save
pm2 startup
```

---

## 🌐 Frontend Deployment

### Local Development
```bash
cd frontend
npm run dev
```

Visit: http://localhost:3000

### Production Deployment

**Vercel:**
```bash
npm install -g vercel
cd frontend
vercel
```

**Netlify:**
```bash
npm install -g netlify-cli
cd frontend
npm run build
netlify deploy --prod
```

**GitHub Pages:**
```bash
cd frontend
npm run build
npm run export
# Push dist/ to gh-pages branch
```

---

## 📊 The Graph Subgraph (Optional)

### 1. Initialize Subgraph
```bash
cd subgraph
npm install -g @graphprotocol/graph-cli
graph init --from-contract <LIQUIDATION_PREVENTION_ADDRESS>
```

### 2. Deploy to Hosted Service
```bash
graph auth --product hosted-service <ACCESS_TOKEN>
graph deploy --product hosted-service <USERNAME>/liquidation-prevention
```

### 3. Deploy to Decentralized Network
```bash
graph auth --product subgraph-studio <DEPLOY_KEY>
graph deploy --studio liquidation-prevention
```

---

## 🧪 Testing

### Smart Contracts
```bash
npx hardhat test
npx hardhat coverage
```

### Agent
```bash
cd agent
pytest tests/
pytest tests/ --cov=. --cov-report=html
```

### Integration Tests
```bash
npm run test:integration
```

---

## 🔍 Monitoring & Debugging

### Check Agent Logs
```bash
# Systemd
sudo journalctl -u liquidation-agent -f

# Docker
docker logs -f liquidation-agent

# PM2
pm2 logs liquidation-agent
```

### Monitor Contract Events
```bash
npx hardhat run scripts/monitor-events.js --network sepolia
```

### Check Health Status
```bash
curl http://localhost:8080/health
```

---

## 🚨 Troubleshooting

### Agent Not Starting
```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies
pip list | grep anthropic

# Test Claude API
python -c "from anthropic import Anthropic; print(Anthropic().messages.create(model='claude-3-5-sonnet-20241022', max_tokens=10, messages=[{'role':'user','content':'test'}]))"
```

### Transactions Failing
```bash
# Check gas price
npx hardhat run scripts/check-gas.js --network sepolia

# Check wallet balance
npx hardhat run scripts/check-balance.js --network sepolia

# Simulate transaction
npx hardhat run scripts/simulate-rebalance.js --network sepolia
```

### Contract Verification Failing
```bash
# Flatten contract
npx hardhat flatten contracts/LiquidationPrevention.sol > flattened.sol

# Verify manually on Etherscan
# Upload flattened.sol with compiler version 0.8.20
```

---

## 🔐 Security Checklist

### Before Mainnet Deployment
- [ ] Complete security audit
- [ ] Test all edge cases
- [ ] Implement rate limiting
- [ ] Add circuit breakers
- [ ] Set up monitoring/alerts
- [ ] Use multisig for admin functions
- [ ] Implement timelock for upgrades
- [ ] Test with small amounts first
- [ ] Have emergency pause mechanism
- [ ] Document all risks

### Operational Security
- [ ] Use hardware wallet for mainnet
- [ ] Rotate API keys regularly
- [ ] Monitor for unusual activity
- [ ] Set up backup agents
- [ ] Have incident response plan
- [ ] Regular security reviews
- [ ] Bug bounty program

---

## 📈 Scaling

### For High Volume
- Use WebSocket for real-time data
- Implement caching layer (Redis)
- Run multiple agent instances
- Use load balancer
- Optimize gas usage
- Batch transactions where possible

### Multi-Chain Support
- Deploy to each chain separately
- Use unified monitoring dashboard
- Implement cross-chain messaging
- Consider LayerZero/Axelar for bridging

---

## 🆘 Support

### Issues
- GitHub Issues: https://github.com/mgnlia/liquidation-prevention-agent/issues
- Discord: [Coming soon]

### Documentation
- README: [README.md](../README.md)
- Demo Script: [DEMO_SCRIPT.md](DEMO_SCRIPT.md)
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 📝 Mainnet Deployment (Production)

**⚠️ WARNING: Only deploy to mainnet after thorough testing and auditing**

### Additional Steps for Mainnet:
1. **Security Audit:** Get contracts audited by reputable firm
2. **Insurance:** Consider Nexus Mutual or similar
3. **Monitoring:** Set up Tenderly, Defender, or similar
4. **Legal:** Consult lawyer for regulatory compliance
5. **Testing:** Run on testnet for at least 2 weeks
6. **Gradual Rollout:** Start with small TVL limits

### Mainnet Networks:
```javascript
// hardhat.config.js
mainnet: {
  url: process.env.MAINNET_RPC_URL,
  accounts: [process.env.MAINNET_PRIVATE_KEY],
  chainId: 1,
},
base: {
  url: process.env.BASE_RPC_URL,
  accounts: [process.env.MAINNET_PRIVATE_KEY],
  chainId: 8453,
},
arbitrum: {
  url: process.env.ARBITRUM_RPC_URL,
  accounts: [process.env.MAINNET_PRIVATE_KEY],
  chainId: 42161,
}
```

---

**Good luck with your deployment! 🚀**
