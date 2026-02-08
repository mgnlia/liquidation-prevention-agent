# ⚡ Quick Start - Deploy in 10 Minutes

**Goal:** Get the AI Liquidation Prevention Agent running on Sepolia testnet ASAP.

## 1️⃣ Get Testnet ETH (2 min)

Visit any faucet and get 0.5+ ETH on Sepolia:
- https://sepoliafaucet.com/
- https://www.alchemy.com/faucets/ethereum-sepolia
- https://faucet.quicknode.com/ethereum/sepolia

## 2️⃣ Clone & Install (2 min)

```bash
git clone https://github.com/mgnlia/liquidation-prevention-agent.git
cd liquidation-prevention-agent

# Install contracts
cd contracts && npm install && cd ..

# Install agent
cd agent && pip install -r requirements.txt && cd ..
```

## 3️⃣ Configure Environment (2 min)

### contracts/.env
```bash
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY
PRIVATE_KEY=your_private_key_no_0x
ETHERSCAN_API_KEY=your_etherscan_key
AI_AGENT_ADDRESS=your_agent_wallet_address
```

### agent/.env
```bash
WEB3_PROVIDER_URI=https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY
AGENT_PRIVATE_KEY=your_agent_private_key
ANTHROPIC_API_KEY=sk-ant-your-claude-key
CHAIN_ID=11155111
```

## 4️⃣ Deploy Contracts (2 min)

```bash
cd contracts
npx hardhat compile
npx hardhat run scripts/deploy.js --network sepolia
```

**Save the output addresses!** You'll need them.

## 5️⃣ Update Agent Config (1 min)

Edit `agent/.env` with deployed addresses from step 4:
```bash
LIQUIDATION_PREVENTION_ADDRESS=0x...
AAVE_ADAPTER_ADDRESS=0x...
COMPOUND_ADAPTER_ADDRESS=0x...
FLASH_LOAN_REBALANCER_ADDRESS=0x...
```

## 6️⃣ Run Agent (1 min)

```bash
cd agent
python agent.py
```

You should see:
```
🤖 Initializing AI Liquidation Prevention Agent...
✅ Agent initialized successfully
🚀 LIQUIDATION PREVENTION AGENT STARTING
💰 Agent Wallet: 0x...
   Balance: 0.5000 ETH
```

## ✅ Done!

Your agent is now monitoring for registered positions!

### Next Steps:

1. **Register a position:** Use the frontend or call `registerUser()` directly
2. **Create test position:** Go to https://app.aave.com/?marketName=proto_sepolia_v3
3. **Watch the agent work:** It will monitor and protect your position automatically

### Verify Deployment:

Check your contracts on Etherscan:
```
https://sepolia.etherscan.io/address/YOUR_CONTRACT_ADDRESS
```

---

**Need help?** See full [DEPLOYMENT.md](./docs/DEPLOYMENT.md) or open an issue.

**Ready to demo?** Follow [DEMO.md](./docs/DEMO.md) script.
