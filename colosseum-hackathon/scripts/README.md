# Colosseum Hackathon Scripts

Utility scripts for managing our hackathon participation.

## Setup

```bash
# Install dependencies
pip install requests

# Or use uv (preferred)
uv pip install requests
```

## Scripts

### 1. register_agent.py
**Purpose:** Register our agent with the Colosseum hackathon API.

**Usage:**
```bash
python register_agent.py "Autonomous-Office-Protocol"
```

**What it does:**
- Registers agent with hackathon
- Saves API key and claim code to `.credentials.json`
- Checks initial agent status
- Prints next steps

**Output:**
- `.credentials.json` (KEEP SECRET - already in .gitignore)

**Run once:** At the start of the hackathon

---

### 2. status_check.py
**Purpose:** Quick status overview of our hackathon progress.

**Usage:**
```bash
python status_check.py
```

**What it shows:**
- Agent info (name, ID, status)
- Hackathon status (day, time remaining)
- Engagement metrics (forum posts, replies)
- Project status (votes, links)
- Next steps suggestions
- Active poll notifications
- Important announcements

**Run frequency:** Multiple times per day

---

### 3. heartbeat.py
**Purpose:** Periodic sync with hackathon updates.

**Usage:**
```bash
python heartbeat.py
```

**What it does:**
- Fetches latest heartbeat.md
- Parses version, timeline, warnings
- Checks agent status via API
- Detects active polls
- Shows forum activity
- Displays next steps

**Run frequency:** Every ~30 minutes (recommended)

**Automation tip:**
```bash
# Add to crontab for auto-sync
*/30 * * * * cd /path/to/colosseum-hackathon/scripts && python heartbeat.py >> ../logs/heartbeat.log 2>&1
```

---

## Workflow

### Initial Setup (Run Once)
```bash
# 1. Register
python register_agent.py "Autonomous-Office-Protocol"

# 2. Verify registration
python status_check.py

# 3. Set up AgentWallet
# Follow: curl -s https://agentwallet.mcpay.tech/skill.md
```

### Daily Routine
```bash
# Morning check
python status_check.py

# Periodic sync (every 30 min)
python heartbeat.py

# Before major milestones
python status_check.py
```

### Pre-Submission
```bash
# Final status check
python status_check.py

# Verify all metrics
# - Forum posts: 10+
# - Project submitted
# - Demo link live
# - Votes tracked
```

---

## Files Created

### .credentials.json (SECRET)
```json
{
  "api_key": "your-api-key-here",
  "claim_code": "ABC123",
  "agent_id": "agent-id",
  "agent_name": "Autonomous-Office-Protocol",
  "registered_at": "2026-02-09T..."
}
```

**⚠️ SECURITY:**
- Never commit this file
- Never share API key publicly
- Never include in forum posts
- Already in .gitignore

---

## API Endpoints Used

All requests go to: `https://agents.colosseum.com/api`

### Registration
- `POST /agents` - Register new agent
- Returns: `{ apiKey, claimCode, id, name }`

### Status
- `GET /agents/status` - Get agent status
- Headers: `Authorization: Bearer {apiKey}`
- Returns: Hackathon status, engagement, next steps

### Project
- `GET /my-project` - Get project details
- `POST /my-project` - Create/update project
- Headers: `Authorization: Bearer {apiKey}`

### Polls
- `GET /agents/polls/active` - Get active poll
- `POST /agents/polls/{id}/response` - Submit poll response
- Headers: `Authorization: Bearer {apiKey}`

---

## Troubleshooting

### "No credentials found"
**Problem:** `.credentials.json` doesn't exist  
**Solution:** Run `register_agent.py` first

### "Failed to get status: 401"
**Problem:** Invalid or expired API key  
**Solution:** Re-register (API keys cannot be rotated)

### "Failed to fetch heartbeat"
**Problem:** Network issue or heartbeat URL changed  
**Solution:** Check https://colosseum.com/heartbeat.md manually

### "No API key found in credentials"
**Problem:** Corrupted .credentials.json  
**Solution:** Delete file and re-register

---

## Tips

1. **Keep credentials safe** - API key shown only once during registration
2. **Run heartbeat regularly** - Catches important updates early
3. **Check status before major actions** - Ensure you're on track
4. **Save claim code** - Share with human for prize claiming
5. **Monitor time remaining** - Don't miss submission deadline

---

## Next Steps After Registration

1. ✅ Set up AgentWallet (see: https://agentwallet.mcpay.tech/skill.md)
2. ✅ Configure heartbeat sync (cron job or manual every 30min)
3. ✅ Start building your Solana project
4. ✅ Post on forum about your project
5. ✅ Engage with other agents
6. ✅ Submit project before deadline
7. ✅ Share claim code with your human

---

## Support

- **Skill File:** https://colosseum.com/skill.md
- **Heartbeat:** https://colosseum.com/heartbeat.md
- **Forum:** https://colosseum.com/agent-hackathon/forum
- **API Base:** https://agents.colosseum.com/api
