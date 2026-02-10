# 🚀 DEPLOY TO VERCEL NOW

## Option 1: One-Click Deploy (FASTEST)

Click this button and follow the prompts:

**👉 [DEPLOY TO VERCEL](https://vercel.com/new/clone?repository-url=https://github.com/mgnlia/liquidation-prevention-agent&project-name=liquidation-prevention-agent&root-directory=liquidation-frontend&framework=nextjs) 👈**

Configuration will be:
- **Root Directory**: `liquidation-frontend`
- **Framework**: Next.js
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `.next` (auto-detected)

## Option 2: Import from Vercel Dashboard

1. Go to: https://vercel.com/new
2. Click "Import Git Repository"
3. Select: `mgnlia/liquidation-prevention-agent`
4. In "Configure Project":
   - Set **Root Directory** to: `liquidation-frontend`
   - Framework Preset: Next.js (auto-detected)
5. Click "Deploy"

## Option 3: Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Navigate to the frontend directory
cd liquidation-prevention-agent/liquidation-frontend

# Login to Vercel (opens browser)
vercel login

# Deploy to production
vercel --prod

# You'll get a URL like: https://liquidation-prevention-agent-xyz.vercel.app
```

## Expected Result

After deployment completes (usually 1-2 minutes), you'll get:

✅ **Production URL**: `https://liquidation-prevention-agent-[hash].vercel.app`

The dashboard will show:
- AI Liquidation Prevention header
- Connect Wallet button (RainbowKit)
- Feature cards (Real-Time Monitoring, AI-Powered Protection, Flash Loan Rebalancing)
- Tech stack badges
- Demo mode works without wallet connection

## Verification Checklist

- [ ] Homepage loads successfully
- [ ] "Connect Wallet" button appears
- [ ] No console errors
- [ ] Responsive design works on mobile
- [ ] Tech stack section visible

## Troubleshooting

**Build fails?**
- Ensure root directory is set to `liquidation-frontend`
- Check Node.js version is 18.x or higher in Vercel settings

**Blank page?**
- Check browser console for errors
- Verify deployment logs in Vercel dashboard

**Need help?**
- Deployment logs: https://vercel.com/dashboard
- Vercel docs: https://vercel.com/docs

---

**STATUS**: Ready to deploy ✅  
**REPO**: https://github.com/mgnlia/liquidation-prevention-agent  
**FRONTEND PATH**: `/liquidation-frontend`
