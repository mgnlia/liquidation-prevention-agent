# 🚀 DEPLOYMENT INSTRUCTIONS - READ THIS FIRST

## Frontend Deployment Status: READY TO DEPLOY ✅

The frontend is **fully configured** and ready for Vercel deployment. All code is complete.

---

## 🎯 FASTEST PATH TO LIVE URL (2 minutes)

### Method 1: Vercel Dashboard (RECOMMENDED - No CLI needed)

1. **Go to Vercel**: https://vercel.com/new
2. **Import Git Repository**: 
   - Connect GitHub
   - Select: `mgnlia/liquidation-prevention-agent`
3. **Configure Project**:
   - **Root Directory**: `liquidation-frontend` ⚠️ IMPORTANT
   - Framework: Next.js (auto-detected)
   - Build Command: `npm run build`
   - Output Directory: `.next`
4. **Environment Variables** (click "Add"):
   ```
   NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID = your_project_id
   NEXT_PUBLIC_ALCHEMY_API_KEY = your_alchemy_key  
   NEXT_PUBLIC_SUBGRAPH_URL = https://api.thegraph.com/subgraphs/name/your-subgraph
   ```
   - Get WalletConnect ID: https://cloud.walletconnect.com (free, 1 min signup)
   - Get Alchemy Key: https://dashboard.alchemy.com (free tier)
   - Subgraph URL: Use placeholder for now, update later
5. **Click "Deploy"**
6. **Wait 2-3 minutes** ☕
7. **DONE!** You'll get: `https://liquidation-prevention-agent-xxx.vercel.app`

---

### Method 2: One-Click Deploy Button

Click this button → [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fmgnlia%2Fliquidation-prevention-agent&root-directory=liquidation-frontend&project-name=liquidation-prevention-agent)

Then add environment variables as shown above.

---

### Method 3: Vercel CLI (For developers)

```bash
# From repo root
chmod +x deploy-to-vercel.sh
./deploy-to-vercel.sh
```

Or manually:
```bash
npm i -g vercel
cd liquidation-frontend
vercel --prod
```

---

## 🔑 Getting API Keys (Quick Links)

### WalletConnect Project ID (Required for wallet connection)
1. Go to: https://cloud.walletconnect.com
2. Sign up (free, takes 30 seconds)
3. Create new project → Copy Project ID
4. Add to Vercel env vars

### Alchemy API Key (Required for blockchain data)
1. Go to: https://dashboard.alchemy.com
2. Sign up (free tier available)
3. Create new app → Select "Ethereum" → "Sepolia" testnet
4. Copy API key
5. Add to Vercel env vars

### Subgraph URL (Optional - can use placeholder)
- Use: `https://api.thegraph.com/subgraphs/name/aave/protocol-v3-sepolia`
- Or deploy your own subgraph later

---

## 📊 What You'll Get

After deployment, your live dashboard will have:

✅ **Wallet Connection** (RainbowKit - MetaMask, WalletConnect, Coinbase)  
✅ **Health Factor Monitor** - Real-time DeFi position tracking  
✅ **Rebalance History** - See all AI agent actions  
✅ **Multi-Protocol** - Aave V3 + Compound V3 support  
✅ **Responsive Design** - Mobile & desktop ready  

---

## 🎨 Frontend Tech Stack

- **Framework**: Next.js 14
- **Wallet**: RainbowKit + wagmi + viem
- **UI**: Tailwind CSS + Lucide icons
- **Charts**: Recharts
- **Blockchain**: ethers.js v6

---

## ⚡ Deployment Checklist

- [x] Frontend code complete
- [x] Next.js config optimized
- [x] Vercel config file created
- [x] Environment variables documented
- [x] Deployment scripts ready
- [ ] **YOUR TURN**: Deploy to Vercel
- [ ] **YOUR TURN**: Add environment variables
- [ ] **YOUR TURN**: Share live URL

---

## 🐛 Troubleshooting

### "Build failed: Cannot find module"
→ Vercel didn't set root directory correctly. Set to `liquidation-frontend`

### "Wallet connection not working"
→ Add `NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID` env var in Vercel dashboard

### "No data showing"
→ Check `NEXT_PUBLIC_ALCHEMY_API_KEY` and `NEXT_PUBLIC_SUBGRAPH_URL`

---

## 📞 Need Help?

1. Check detailed guide: `VERCEL_DEPLOYMENT.md`
2. Vercel docs: https://vercel.com/docs
3. Message Henry with deployment URL when live

---

## 🎯 EXPECTED OUTCOME

After following Method 1 above, you will have:

```
🌐 Live URL: https://liquidation-prevention-agent.vercel.app
✅ Status: Deployed
✅ Wallet: Connected
✅ Dashboard: Working
```

**Deployment time: 2-3 minutes**

---

**Ready? Go to https://vercel.com/new and deploy now! 🚀**
