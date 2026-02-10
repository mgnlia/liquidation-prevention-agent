#!/bin/bash
# Scout Colosseum forum for winning strategies and collaboration opportunities

echo "🔍 Scouting Colosseum Agent Hackathon Forum..."
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📈 TOP 20 HOT POSTS (What's winning)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "https://agents.colosseum.com/api/forum/posts?sort=hot&limit=20" | \
  jq -r '.posts[] | "[\(.votes) votes] \(.title) - by @\(.author) | Tags: \(.tags | join(", "))"'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🆕 LATEST 20 POSTS (Recent activity)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "https://agents.colosseum.com/api/forum/posts?sort=new&limit=20" | \
  jq -r '.posts[] | "[\(.createdAt)] \(.title) - by @\(.author)"'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 IDEATION POSTS (Project ideas)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "https://agents.colosseum.com/api/forum/posts?sort=hot&tags=ideation&limit=15" | \
  jq -r '.posts[] | "[\(.votes) votes] \(.title) - by @\(.author)"'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🤝 TEAM FORMATION (Collaboration opportunities)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "https://agents.colosseum.com/api/forum/posts?sort=new&tags=team-formation&limit=15" | \
  jq -r '.posts[] | "\(.title) - by @\(.author)"'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏆 CURRENT LEADERBOARD TOP 10"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s https://agents.colosseum.com/api/leaderboard | \
  jq -r '.top10[] | "#\(.rank) @\(.agent) - \(.projectName) | Score: \(.score) | Votes: \(.votes)"'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔥 ACTIVE HACKATHONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "https://agents.colosseum.com/api/hackathons/active" | jq '.'

echo ""
echo "✅ Scout complete. Analysis:"
echo "1. Review hot posts for winning project patterns"
echo "2. Check leaderboard for competitive landscape"
echo "3. Look for collaboration opportunities in team-formation"
echo "4. Identify gaps in current submissions"
