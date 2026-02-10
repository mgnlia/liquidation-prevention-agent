#!/bin/bash
# Check Colosseum Agent Hackathon status

if [ -z "$COLOSSEUM_API_KEY" ]; then
    echo "❌ COLOSSEUM_API_KEY not set. Export it first:"
    echo "export COLOSSEUM_API_KEY=your_api_key_here"
    exit 1
fi

echo "📊 Checking hackathon status..."
echo ""

# Check agent status
curl -s -H "Authorization: Bearer $COLOSSEUM_API_KEY" \
  https://agents.colosseum.com/api/agents/status | jq '.'

echo ""
echo "🏆 Checking leaderboard..."
echo ""

# Check leaderboard
curl -s https://agents.colosseum.com/api/leaderboard | jq '.top10'

echo ""
echo "📰 Checking forum activity (hot posts)..."
echo ""

# Check forum hot posts
curl -s "https://agents.colosseum.com/api/forum/posts?sort=hot&limit=10" | jq '.posts[] | {title: .title, author: .author, votes: .votes, tags: .tags}'
