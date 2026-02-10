# Vercel Deployment Guide - Liquidation Prevention Agent Frontend

## 🚀 Quick Deploy (Recommended)

### Option 1: Deploy via Vercel Dashboard (Easiest)

1. **Import Repository**
   - Go to https://vercel.com/new
   - Import `mgnlia/liquidation-prevention-agent`
   - Vercel will auto-detect the Next.js framework

2. **Configure Root Directory**
   - Set **Root Directory** to: `liquidation-frontend`
   - Framework Preset: Next.js (auto-detected)
   - Build Command: `npm run build` (default)
   - Output Directory: `.next` (default)

3. **Add Environment Variables**
   ```
   NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID=<get from https://cloud.walletconnect.com>
   NEXT_PUBLIC_ALCHEMY_API_KEY=<get from https://dashboard.alchemy.com>
   NEXT_PUBLIC_SUBGRAPH_URL=https://api.thegraph.com/subgraphs/name/your-subgraph
   ```

4. **Deploy!**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your app will be live at `https://liquidation-prevention-agent-xxx.vercel.app`

---

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy from liquidation-frontend directory
cd liquidation-frontend
vercel --prod

# Follow prompts:
# - Link to existing project? N
# - Project name: liquidation-prevention-agent
# - Directory: ./ (current)
```

**Set Environment Variables:**
```bash
vercel env add NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID
vercel env add NEXT_PUBLIC_ALCHEMY_API_KEY
vercel env add NEXT_PUBLIC_SUBGRAPH_URL
```

**Redeploy with env vars:**
```bash
vercel --prod
```

---

### Option 3: One-Click Deploy Button

Add this to your README:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fmgnlia%2Fliquidation-prevention-agent&root-directory=liquidation-frontend&env=NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID,NEXT_PUBLIC_ALCHEMY_API_KEY,NEXT_PUBLIC_SUBGRAPH_URL&envDescription=Get%20WalletConnect%20Project%20ID%20from%20cloud.walletconnect.com%20and%20Alchemy%20API%20key%20from%20dashboard.alchemy.com&project-name=liquidation-prevention-agent&repository-name=liquidation-prevention-agent)

---

## 🔧 Configuration Details

### vercel.json (Current Setup)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "liquidation-frontend/package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "liquidation-frontend/$1"
    }
  ]
}
```

### Environment Variables Explained

| Variable | Purpose | Get From |
|----------|---------|----------|
| `NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID` | RainbowKit wallet connection | https://cloud.walletconnect.com |
| `NEXT_PUBLIC_ALCHEMY_API_KEY` | RPC provider for blockchain data | https://dashboard.alchemy.com |
| `NEXT_PUBLIC_SUBGRAPH_URL` | The Graph API endpoint | Your deployed subgraph |

---

## 📊 Frontend Features

✅ **RainbowKit Wallet Connect** - Connect MetaMask, WalletConnect, Coinbase Wallet  
✅ **Health Factor Dashboard** - Real-time monitoring of DeFi positions  
✅ **Rebalance History** - View all AI agent actions  
✅ **Multi-Protocol Support** - Aave V3 + Compound V3  
✅ **Responsive Design** - Works on mobile & desktop  

---

## 🐛 Troubleshooting

### Build Fails: "Module not found"
```bash
cd liquidation-frontend
npm install
npm run build
```

### Wallet Connection Issues
- Ensure `NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID` is set
- Check https://cloud.walletconnect.com for project status

### Subgraph Data Not Loading
- Verify `NEXT_PUBLIC_SUBGRAPH_URL` is correct
- Check subgraph is deployed and synced

---

## 🎯 Post-Deployment Checklist

- [ ] Frontend deployed and live
- [ ] Wallet connection working
- [ ] Health factor dashboard loads
- [ ] Contract addresses configured correctly
- [ ] Subgraph data populating
- [ ] Mobile responsive
- [ ] Update README with live URL

---

## 📝 Expected Live URL Format

After deployment, your app will be at:
```
https://liquidation-prevention-agent.vercel.app
```
or
```
https://liquidation-prevention-agent-<random>.vercel.app
```

You can configure a custom domain in Vercel Dashboard → Settings → Domains.

---

**Need help?** Check Vercel docs: https://vercel.com/docs
