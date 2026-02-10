# Vercel Deployment Instructions

## Frontend Location
The Next.js frontend is located in: `/liquidation-frontend`

## Deployment Steps

### Option 1: Vercel CLI (Recommended)
```bash
# Install Vercel CLI globally
npm i -g vercel

# Navigate to repository root
cd liquidation-prevention-agent

# Deploy (will use vercel.json config automatically)
vercel --prod

# Or deploy from frontend directory
cd liquidation-frontend
vercel --prod
```

### Option 2: Vercel Dashboard
1. Go to https://vercel.com/new
2. Import repository: `mgnlia/liquidation-prevention-agent`
3. Vercel will auto-detect the `vercel.json` config
4. Root Directory: `liquidation-frontend`
5. Framework Preset: Next.js
6. Click Deploy

### Option 3: GitHub Integration
1. Connect GitHub repo to Vercel
2. Vercel will auto-deploy on push to main
3. Uses vercel.json configuration

## Environment Variables (if needed)
- `NEXT_PUBLIC_ALCHEMY_ID` - Alchemy API key for RPC
- `NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID` - WalletConnect project ID

## Expected Output
- Live URL: `https://liquidation-prevention-agent.vercel.app` (or similar)
- Preview URLs for each commit

## Verification
After deployment, verify:
- ✅ Homepage loads with dashboard
- ✅ Wallet connect button works
- ✅ Health factor chart displays
- ✅ Rebalance history table renders
