# 🚀 Sepolia Deployment Guide

## Prerequisites

### 1. Get Sepolia ETH
You need Sepolia testnet ETH for deployment. Use these faucets:
- **Alchemy Faucet**: https://www.alchemy.com/faucets/ethereum-sepolia
- **Sepolia PoW Faucet**: https://sepolia-faucet.pk910.de/
- **QuickNode Faucet**: https://faucet.quicknode.com/ethereum/sepolia

**Recommended**: Get at least 0.5 SepoliaETH to cover deployment + gas

### 2. Setup Environment Variables

```bash
cd contracts
cp .env.example .env
```

Edit `.env` with your values:

```bash
# Get RPC URL from:
# - Alchemy: https://www.alchemy.com/ (free tier)
# - Infura: https://www.infura.io/
# - QuickNode: https://www.quicknode.com/
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY

# Your wallet private key (KEEP SECRET!)
# Export from MetaMask: Settings > Security & Privacy > Reveal Private Key
PRIVATE_KEY=0x...

# Get from https://etherscan.io/myapikey
ETHERSCAN_API_KEY=YOUR_ETHERSCAN_API_KEY
```

### 3. Install Dependencies

```bash
cd contracts
npm install
```

## Deployment Steps

### Step 1: Compile Contracts

```bash
npx hardhat compile
```

Expected output: `Compiled X Solidity files successfully`

### Step 2: Deploy to Sepolia

```bash
npx hardhat run scripts/deploy.js --network sepolia
```

**This will deploy 4 contracts:**
1. ✅ AaveV3Adapter
2. ✅ CompoundV3Adapter  
3. ✅ FlashLoanRebalancer
4. ✅ LiquidationPrevention

**Save the contract addresses!** They'll be printed and saved to `deployments/sepolia-{timestamp}.json`

### Step 3: Verify Contracts on Etherscan

```bash
npx hardhat run scripts/verify.js --network sepolia
```

This will verify all 4 contracts automatically. Wait 1-2 minutes for Etherscan indexing if you get errors.

### Step 4: Update Agent Configuration

Copy the deployed contract addresses to agent configuration:

```bash
# Edit agent/.env
LIQUIDATION_PREVENTION_ADDRESS=0x...
AAVE_ADAPTER_ADDRESS=0x...
COMPOUND_ADAPTER_ADDRESS=0x...
REBALANCER_ADDRESS=0x...
```

## Verification

### Check Deployment

```bash
npx hardhat console --network sepolia
```

```javascript
const LiquidationPrevention = await ethers.getContractFactory("LiquidationPrevention");
const contract = await LiquidationPrevention.attach("YOUR_CONTRACT_ADDRESS");
const stats = await contract.getStats();
console.log("Stats:", stats);
```

### View on Etherscan

- Navigate to: `https://sepolia.etherscan.io/address/YOUR_CONTRACT_ADDRESS`
- Check "Contract" tab shows verified ✅ green checkmark
- Try "Read Contract" and "Write Contract" functions

## Troubleshooting

### "Insufficient funds" error
- Get more SepoliaETH from faucets above
- Check balance: `npx hardhat console --network sepolia` → `(await ethers.provider.getBalance("YOUR_ADDRESS")).toString()`

### "Invalid API key" error
- Double-check your Etherscan API key in `.env`
- Create new key at https://etherscan.io/myapikey

### "Already verified" on Etherscan
- This is OK! Contract is already verified ✅

### RPC connection errors
- Check your `SEPOLIA_RPC_URL` is correct
- Try alternative RPC providers (Alchemy, Infura, QuickNode)

## Next Steps

After successful deployment:

1. ✅ Update task status: `sAwZdoCQBgrPOL4wa3QXK` → DONE
2. ✅ Configure AI agent with contract addresses
3. ✅ Test agent monitoring cycle
4. ✅ Record demo video
5. ✅ Submit to HackMoney 2026

## Contract Addresses (Sepolia)

**Protocol Addresses (Pre-deployed):**
- Aave V3 Pool: `0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951`
- Aave Pool Provider: `0x0496275d34753A48320CA58103d5220d394FF77F`
- Compound Comet (USDC): `0xAec1F48e02Cfb822Be958B68C7957156EB3F0b6e`

**Your Deployed Contracts:**
- AaveV3Adapter: `[DEPLOYED_ADDRESS]`
- CompoundV3Adapter: `[DEPLOYED_ADDRESS]`
- FlashLoanRebalancer: `[DEPLOYED_ADDRESS]`
- LiquidationPrevention: `[DEPLOYED_ADDRESS]`

---

**Need help?** Check Hardhat docs: https://hardhat.org/hardhat-runner/docs/guides/deploying
