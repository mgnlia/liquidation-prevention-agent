# Deployment Guide - AI-Powered Liquidation Prevention Agent

## Prerequisites

- Node.js >= 18.0.0
- Python >= 3.10
- Sepolia ETH for deployment
- Anthropic API key

## Step 1: Environment Setup

### Contracts Environment

```bash
cd contracts
cp .env.example .env
```

Edit `.env` with:
```
SEPOLIA_RPC_URL=https://rpc.sepolia.org
PRIVATE_KEY=your_private_key_here
ETHERSCAN_API_KEY=your_etherscan_key
AAVE_POOL_ADDRESS_PROVIDER=0x012bAC54348C0E635dCAc9D5FB99f06F24136C9A
AAVE_POOL=0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951
```

### Agent Environment

```bash
cd agent
cp .env.example .env
```

Edit `.env` with:
```
ANTHROPIC_API_KEY=your_anthropic_key
SEPOLIA_RPC_URL=https://rpc.sepolia.org
AGENT_PRIVATE_KEY=your_agent_private_key
```

## Step 2: Get Sepolia ETH

Fund your deployment wallet with Sepolia ETH from faucets:
- https://sepoliafaucet.com
- https://faucet.sepolia.dev
- https://www.alchemy.com/faucets/ethereum-sepolia

You need ~0.1 ETH for deployment and testing.

## Step 3: Install Dependencies

### Contracts
```bash
cd contracts
npm install
```

### Agent
```bash
cd agent
pip install -r requirements.txt
```

## Step 4: Deploy Smart Contracts

```bash
cd contracts
npx hardhat run scripts/deploy.js --network sepolia
```

Expected output:
```
🚀 Deploying Liquidation Prevention System to Sepolia...

✅ AaveV3Adapter deployed to: 0x...
✅ CompoundV3Adapter deployed to: 0x...
✅ FlashLoanRebalancer deployed to: 0x...
✅ LiquidationPrevention deployed to: 0x...

💾 Deployment info saved to deployment-info.json
```

## Step 5: Verify Contracts on Etherscan

```bash
npx hardhat verify --network sepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

Or use the verification script:
```bash
npx hardhat run scripts/verify.js --network sepolia
```

## Step 6: Update Agent Configuration

Copy deployed contract addresses from `deployment-info.json` to `agent/.env`:

```
LIQUIDATION_PREVENTION_ADDRESS=0x...
AAVE_ADAPTER_ADDRESS=0x...
COMPOUND_ADAPTER_ADDRESS=0x...
REBALANCER_ADDRESS=0x...
```

## Step 7: Test Agent

```bash
cd agent
python monitor.py  # Test position monitoring
python analyzer.py  # Test risk analysis
python executor.py  # Test execution setup
```

## Step 8: Start Agent

```bash
cd agent
python agent.py
```

The agent will:
1. Monitor registered user positions every 60 seconds
2. Analyze risk using Claude API
3. Execute rebalancing when health factor < 1.5
4. Log all actions to `execution_log.json`

## Deployment Checklist

- [ ] Sepolia ETH acquired
- [ ] Environment variables configured
- [ ] Dependencies installed
- [ ] Contracts deployed
- [ ] Contracts verified on Etherscan
- [ ] Agent configuration updated
- [ ] Agent tested successfully
- [ ] Agent running in monitoring mode

## Troubleshooting

### "Insufficient funds" error
- Ensure wallet has enough Sepolia ETH
- Check balance: `npx hardhat run scripts/check-balance.js --network sepolia`

### "Contract not found" error
- Verify contract addresses in `.env`
- Check deployment was successful
- Ensure network is set to Sepolia

### Agent connection errors
- Verify RPC URL is accessible
- Check Anthropic API key is valid
- Ensure contract addresses are correct

## Production Considerations

For mainnet deployment:
1. Use hardware wallet or secure key management
2. Audit all smart contracts
3. Test thoroughly on testnet first
4. Set up monitoring and alerts
5. Implement circuit breakers
6. Configure proper access controls
7. Use professional RPC providers (Alchemy, Infura)

## Support

For issues or questions:
- GitHub Issues: https://github.com/mgnlia/liquidation-prevention-agent/issues
- Documentation: https://github.com/mgnlia/liquidation-prevention-agent/docs
