# AI Liquidation Prevention Agent - Frontend

Real-time DeFi position monitoring dashboard with AI-powered rebalancing recommendations.

## Features

- 🔍 Real-time position monitoring across Aave V3 and Compound V3
- 🤖 AI-powered rebalancing recommendations using Claude API
- ⚡ Flash loan-based capital-efficient rebalancing
- 📊 Health factor tracking and visualization
- 🔔 Proactive liquidation warnings

## Tech Stack

- **Next.js 14** - React framework
- **RainbowKit** - Wallet connection
- **Wagmi** - Ethereum interactions
- **Recharts** - Data visualization
- **Tailwind CSS** - Styling

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
# Add your WalletConnect Project ID and other keys
```

3. Run development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000)

## Deployment

Deploy to Vercel:
```bash
npx vercel --prod
```

## HackMoney 2026

This project is built for ETHGlobal HackMoney 2026, demonstrating:
- Integration with Aave V3 and Compound V3 protocols
- AI-powered DeFi risk management
- Flash loan optimization
- Real-time on-chain data indexing via The Graph

## License

MIT
