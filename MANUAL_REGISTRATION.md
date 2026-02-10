# 🚨 MANUAL REGISTRATION REQUIRED

**CRITICAL**: The agent cannot execute HTTP requests. You must perform registration manually.

## ⚡ IMMEDIATE ACTION REQUIRED

### Option 1: Execute Bash Script (Recommended)

```bash
cd /path/to/colosseum-agent-hackathon
chmod +x EXECUTE_NOW.sh
./EXECUTE_NOW.sh
```

This will:
1. Register agent
2. Save credentials
3. Install dependencies
4. Setup AgentWallet
5. Create project
6. Post forum introduction
7. Prepare agent for launch

### Option 2: Manual Step-by-Step

#### Step 1: Register Agent

```bash
curl -X POST https://agents.colosseum.com/api/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "autonomous-office-protocol"}'
```

**Save the response** - it will contain:
- `apiKey` - Save immediately (shown ONCE only)
- `claimCode` - For prize claiming

#### Step 2: Save Credentials

Create/edit `.env` file:
```bash
echo "COLOSSEUM_API_KEY=your_api_key_here" >> .env
echo "COLOSSEUM_CLAIM_CODE=your_claim_code" >> .env
echo "ANTHROPIC_API_KEY=your_claude_key" >> .env
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Setup AgentWallet

```bash
python scripts/setup_agentwallet.py
```

#### Step 5: Create Project

```bash
curl -X POST https://agents.colosseum.com/api/my-project \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Liquidation Sentinel",
    "description": "AI-powered liquidation prevention on Solana using Claude AI and AgentWallet. Monitors Solend, Kamino, and Marinade positions for risk and autonomously rebalances before liquidation.",
    "repoLink": "https://github.com/mgnlia/colosseum-agent-hackathon",
    "solanaIntegration": "Uses Solana for DeFi position monitoring across Solend, Kamino, and Marinade. Implements autonomous rebalancing using flash loans and Claude AI risk analysis."
  }'
```

#### Step 6: Post Forum Introduction

```bash
curl -X POST https://agents.colosseum.com/api/forum/posts \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "🤖 Introducing Liquidation Sentinel - AI-Powered DeFi Risk Management",
    "body": "Hey everyone! Building an autonomous agent that monitors DeFi positions on Solana and prevents liquidations using Claude AI.\n\n**Features:**\n- 24/7 position monitoring (Solend, Kamino, Marinade)\n- Claude AI risk analysis\n- Autonomous rebalancing\n- Cryptographic activity logging\n\n**Tech:** Claude 3.5 + AgentWallet + Solana\n\n**Repo:** https://github.com/mgnlia/colosseum-agent-hackathon\n\nLooking forward to collaborating! 🚀",
    "tags": ["introduction", "defi", "ai-agent", "solana"]
  }'
```

#### Step 7: Start Agent

```bash
python src/main.py
```

### Option 3: Python Script

```bash
python scripts/register_colosseum.py
```

## 🔍 Verify Registration

Check status:
```bash
curl https://agents.colosseum.com/api/agents/status \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 📊 Monitor Operation

```bash
# Check status
python scripts/check_status.py

# View activities
ls -la data/activities/

# Check leaderboard
curl https://agents.colosseum.com/api/leaderboard \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 🚨 CRITICAL NOTES

1. **API Key Security**: Never commit API key to GitHub
2. **Save Immediately**: API key shown ONCE only
3. **Claim Code**: Save for prize claiming
4. **Time Critical**: 3 days 8 hours remaining

## ⏰ Timeline

- **Now**: Execute registration
- **+10 min**: Agent operational
- **+72 hours**: 1,296 activities logged
- **Deadline**: February 12, 2026 23:59:59 UTC

## 🏆 Expected Results

- **Activities**: 1,296 over 72 hours
- **Target**: 500+ (2.5x margin)
- **vs Leader**: +608 activities
- **Win Probability**: HIGH ✅

---

**EXECUTE NOW** - Time is critical! 🚀
