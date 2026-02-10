# Setup Guide - Autonomous Office Protocol

Complete setup guide for the Colosseum Agent Hackathon submission.

## Prerequisites

- Python 3.11+
- Node.js 18+
- Solana CLI 1.18+
- Git

## Step-by-Step Setup

### 1. Clone Repository

```bash
git clone https://github.com/mgnlia/colosseum-agent-hackathon.git
cd colosseum-agent-hackathon
```

### 2. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Required environment variables:
- `ANTHROPIC_API_KEY` - Get from https://console.anthropic.com/
- `COLOSSEUM_API_KEY` - Obtained after registration (see step 4)
- `SOLANA_RPC_URL` - Use devnet: https://api.devnet.solana.com

### 4. Register with Colosseum

```bash
python scripts/register_colosseum.py
```

This will:
- Register your agent with Colosseum API
- Save API key and claim code to `.env`
- Create initial project
- Log first activity

**IMPORTANT**: Save your API key - it's only shown once!

### 5. Set Up AgentWallet

```bash
python scripts/setup_agentwallet.py
```

This will:
- Fetch AgentWallet documentation
- Generate Ed25519 keypair for activity signing
- Create activity logger module
- Test activity logging system

### 6. Run Agent

```bash
python src/main.py
```

The agent will:
- Monitor DeFi positions every 10 minutes
- Analyze risk using Claude AI
- Execute recommended actions
- Log all activities with cryptographic signatures

### 7. Monitor Status

In a separate terminal:

```bash
python scripts/check_status.py
```

This displays:
- Total activities logged
- Time remaining until deadline
- Required activity rate
- Leaderboard position
- Recommendations

## Troubleshooting

### "ANTHROPIC_API_KEY not set"

1. Get API key from https://console.anthropic.com/
2. Add to `.env`: `ANTHROPIC_API_KEY=your_key_here`
3. Restart agent

### "COLOSSEUM_API_KEY not set"

1. Run registration: `python scripts/register_colosseum.py`
2. API key will be automatically saved to `.env`
3. Restart agent

### "Failed to fetch leaderboard"

- Check your internet connection
- Verify API key is correct in `.env`
- Ensure Colosseum API is accessible

### No activities logging

1. Check agent is running: `ps aux | grep main.py`
2. Check activities directory: `ls -la data/activities/`
3. Review agent logs for errors
4. Verify Ed25519 keys exist: `ls -la .keys/`

## Advanced Configuration

### Adjust Activity Rate

Edit `src/main.py`:

```python
# Change cycle interval (default: 600 seconds = 10 minutes)
await agent.run(interval=300)  # 5 minutes = higher activity rate
```

### Add Custom Activities

Create new activity types in `src/main.py`:

```python
self.wallet.log_activity_onchain(
    activity_type="custom_activity",
    data={
        "timestamp": datetime.utcnow().isoformat(),
        "custom_field": "value",
        "status": "success"
    }
)
```

### Forum Integration

1. Visit https://colosseum.com/agent-hackathon/forum
2. Create account
3. Post updates about your agent
4. Engage with other participants

## Next Steps

1. **Keep agent running** - Continuous operation is key
2. **Monitor dashboard** - Check status regularly
3. **Engage on forum** - Build community presence
4. **Optimize activities** - Add more activity types
5. **Deploy frontend** - Build visualization dashboard

## Support

- **GitHub Issues**: https://github.com/mgnlia/colosseum-agent-hackathon/issues
- **Colosseum Forum**: https://colosseum.com/agent-hackathon/forum
- **Documentation**: See `docs/` directory

## Competition Strategy

### Target Metrics
- **Activities**: 500+ over 3 days
- **Rate**: ~7 activities/hour
- **Diversity**: Multiple activity types
- **Consistency**: 24/7 operation

### Activity Types
1. Position monitoring
2. AI risk analysis
3. Action execution
4. Forum posts
5. Dashboard updates
6. Transaction simulations
7. Data analysis
8. Status reports

### Winning Factors
1. **Volume**: High activity count
2. **Quality**: Meaningful, diverse activities
3. **Consistency**: Continuous operation
4. **Innovation**: Unique activity types
5. **Documentation**: Clear, comprehensive docs
6. **Community**: Active forum engagement

Good luck! 🏆
