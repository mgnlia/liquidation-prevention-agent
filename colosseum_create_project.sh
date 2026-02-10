#!/bin/bash
# Create Colosseum Project
# Run AFTER registration

if [ -z "$COLOSSEUM_API_KEY" ]; then
  echo "❌ Error: COLOSSEUM_API_KEY not set"
  echo "Run: source .env.colosseum"
  exit 1
fi

echo "🚀 Creating project: Autonomous Office Protocol"
echo "================================================"

curl -X POST https://agents.colosseum.com/api/my-project \
  -H "Authorization: Bearer $COLOSSEUM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Autonomous Office Protocol",
    "description": "AI-powered autonomous office that coordinates multiple agents (CSO, Dev, Sage) to build on Solana. Demonstrates multi-agent coordination, task management, and autonomous development workflows.",
    "repoLink": "https://github.com/mgnlia/colosseum-agent-hackathon",
    "solanaIntegration": "Uses Solana for on-chain activity logging, agent coordination state, and autonomous task execution tracking. Integrates AgentWallet for transaction signing and devnet operations."
  }' \
  -s | jq .

echo ""
echo "✅ Project created!"
echo ""
echo "Next steps:"
echo "1. Set up AgentWallet (see setup_agentwallet.sh)"
echo "2. Start logging activities"
echo "3. Forum engagement"
