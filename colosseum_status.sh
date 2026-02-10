#!/bin/bash
# Check Colosseum Agent Status

if [ -z "$COLOSSEUM_API_KEY" ]; then
  echo "❌ Error: COLOSSEUM_API_KEY not set"
  echo "Run: source .env.colosseum"
  exit 1
fi

echo "📊 Checking agent status..."
echo "================================================"

curl -s https://agents.colosseum.com/api/agents/status \
  -H "Authorization: Bearer $COLOSSEUM_API_KEY" | jq .

echo ""
echo "================================================"
echo "📈 Checking leaderboard..."
echo ""

curl -s https://agents.colosseum.com/api/leaderboard?limit=10 | jq .
