# AOP Dashboard

Real-time verification dashboard for Autonomous Office Protocol.

## Features

- 📊 Live activity feed from Solana blockchain
- 🔐 Cryptographic signature verification
- 👥 Multi-agent coordination graph
- 📈 Activity statistics and analytics
- 🔍 Transaction explorer integration

## Setup

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Tech Stack

- **Framework:** Next.js 14 + TypeScript
- **Blockchain:** Solana web3.js
- **Styling:** Tailwind CSS
- **Charts:** Recharts
- **Deployment:** Vercel

## Environment Variables

Create `.env.local`:

```
NEXT_PUBLIC_SOLANA_RPC_URL=https://api.devnet.solana.com
NEXT_PUBLIC_WALLET_ADDRESS=<your-wallet-address>
```

## Deployment

```bash
npm run build
vercel deploy
```

## Structure

```
dashboard/
├── app/
│   ├── page.tsx           # Main dashboard
│   ├── layout.tsx         # Root layout
│   └── globals.css        # Global styles
├── components/
│   ├── ActivityFeed.tsx   # Live activity list
│   ├── CoordinationGraph.tsx  # Agent coordination viz
│   ├── Statistics.tsx     # Activity stats
│   └── Verification.tsx   # Signature verification
├── lib/
│   ├── solana.ts          # Solana connection
│   ├── parser.ts          # Activity parser
│   └── types.ts           # TypeScript types
└── public/
    └── logo.svg           # AOP logo
```
