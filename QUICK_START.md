# ⚡ QUICK START - ETHDenver Emergency Guide

**Time to demo: 30 minutes**

---

## 🚀 Fastest Path to Submission

### Step 1: Clone & Setup (5 min)
```bash
git clone https://github.com/mgnlia/liquidation-prevention-agent.git
cd liquidation-prevention-agent
chmod +x DEMO_NOW.sh
./DEMO_NOW.sh
```

### Step 2: Record Demo (15 min)
```bash
# Follow the prompts from DEMO_NOW.sh
# Or manually:
npx hardhat console --network localhost

# In console, run:
const LP = await ethers.getContractAt("LiquidationPrevention", "0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9");
await LP.setUserConfig(ethers.parseEther("1.5"), ethers.parseEther("2.0"), true, false);
```

**Record your screen showing:**
1. Deployment output
2. Contract interaction
3. Code walkthrough

### Step 3: Upload & Register (10 min)
1. Upload video to YouTube
2. Go to https://ethdenver2026.devfolio.co/
3. Copy details from `SUBMISSION_CHECKLIST.md`
4. Submit

---

## 📋 Devfolio Quick Copy-Paste

**Project Name:**
```
AI-Powered Liquidation Prevention Agent
```

**Tagline:**
```
Autonomous AI agent preventing DeFi liquidations using Claude AI and flash loans
```

**Track:**
```
Futurllama
```

**GitHub:**
```
https://github.com/mgnlia/liquidation-prevention-agent
```

**Description:**
```
An AI agent that monitors DeFi positions across Aave and Compound, uses Claude AI for risk analysis, and executes flash loan rebalancing to prevent liquidations. Features multi-chain support, transparent AI attribution, and production-ready code.

Tech: Solidity, Hardhat, Python, Claude API, The Graph, React
```

---

## 🆘 If Something Breaks

**Can't install dependencies?**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Compilation errors?**
```bash
npx hardhat clean
npx hardhat compile
```

**Node won't start?**
```bash
pkill -f hardhat
npx hardhat node
```

---

## ✅ Pre-Submission Checklist

- [ ] Demo video recorded (2-4 min)
- [ ] Video uploaded to YouTube
- [ ] Video link added to README
- [ ] Registered on Devfolio
- [ ] All form fields filled
- [ ] Submission confirmed

---

## 📞 Contract Addresses (Localhost)

After running `DEMO_NOW.sh`, you'll see:

```
AaveAdapter: 0x5FbDB2315678afecb367f032d93F642f64180aa3
CompoundAdapter: 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512
FlashLoanRebalancer: 0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0
LiquidationPrevention: 0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9
```

Use these in your demo!

---

## 🎥 Demo Script (2 min version)

**[0:00-0:20] Intro**
"Hi, I'm presenting the AI-Powered Liquidation Prevention Agent for ETHDenver. This system uses Claude AI to monitor DeFi positions and prevent liquidations."

**[0:20-0:50] Show Deployment**
"Here are the deployed contracts on localhost. We have the main orchestrator, protocol adapters, and flash loan rebalancer."

**[0:50-1:20] Show Code**
"The AI agent uses Claude for decision-making. Here's the integration - it analyzes health factors and recommends actions."

**[1:20-1:50] Demonstrate**
"Let me configure a user position... Setting minimum health factor to 1.5, target to 2.0. Transaction confirmed."

**[1:50-2:00] Close**
"Production-ready code, multi-chain support, full documentation. Check out the repo. Thanks!"

---

**GO GO GO! 🚀**
