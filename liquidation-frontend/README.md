# AI Liquidation Prevention Agent - Frontend

## 🚀 Quick Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/mgnlia/liquidation-prevention-agent&project-name=liquidation-prevention-agent&root-directory=liquidation-frontend)

## Local Development

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Manual Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from this directory
vercel --prod
```

## Environment Variables

No environment variables required for demo mode. The app will work with Sepolia testnet by default.

## Features

- 🔌 **RainbowKit Wallet Connect** - Connect with MetaMask, WalletConnect, Coinbase Wallet
- 📊 **Real-Time Health Factor Monitoring** - Track Aave V3 and Compound V3 positions
- 🤖 **AI Analysis Dashboard** - See Claude AI recommendations
- ⚡ **Flash Loan Rebalancing** - Execute automated position rebalancing
- 📈 **Historical Charts** - View health factor trends over time

## Tech Stack

- **Next.js 14** - React framework with App Router
- **RainbowKit** - Wallet connection UI
- **wagmi** - React hooks for Ethereum
- **viem** - TypeScript Ethereum library
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Lucide Icons** - Icon library

## Contract Addresses (Sepolia Testnet)

The dashboard connects to deployed contracts on Sepolia:
- LiquidationPrevention: `0x...` (auto-detected)
- AaveAdapter: `0x...` (auto-detected)
- CompoundAdapter: `0x...` (auto-detected)

## Demo Mode

The dashboard works in demo mode even without connected wallet, showing:
- Sample health factors
- Mock rebalancing history
- AI analysis examples

Perfect for hackathon judging and presentations!
