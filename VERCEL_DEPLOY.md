# Vercel Deployment Guide

## Automatic Deployment (Recommended)

Click this button to deploy directly to Vercel:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/mgnlia/liquidation-prevention-agent&project-name=liquidation-prevention-agent&root-directory=liquidation-frontend&framework=nextjs)

## Manual Deployment Steps

### Option 1: Vercel Dashboard
1. Go to [vercel.com/new](https://vercel.com/new)
2. Import `mgnlia/liquidation-prevention-agent`
3. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `liquidation-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
4. Click "Deploy"

### Option 2: Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend
cd liquidation-frontend

# Login to Vercel
vercel login

# Deploy to production
vercel --prod
```

## Expected Deployment URL

After deployment, you'll get a URL like:
- `https://liquidation-prevention-agent.vercel.app`
- `https://liquidation-prevention-agent-[hash].vercel.app`

## Verification

Once deployed, verify:
- ✅ Homepage loads with "AI Liquidation Prevention" header
- ✅ "Connect Wallet" button appears
- ✅ Tech stack badges visible
- ✅ Demo features work without wallet connection

## Troubleshooting

If build fails:
1. Check that `liquidation-frontend` is set as root directory
2. Ensure Node.js version is 18.x or higher
3. Verify all dependencies in package.json are accessible

## Environment Variables

No environment variables required for demo deployment. The app works with:
- Sepolia testnet by default
- Mock data for demo mode
- Public RPC endpoints
