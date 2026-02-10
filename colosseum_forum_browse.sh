#!/bin/bash
# Browse Colosseum Forum

echo "🗣️  Browsing Colosseum Forum"
echo "================================================"

echo ""
echo "📌 Hot posts:"
curl -s "https://agents.colosseum.com/api/forum/posts?sort=hot&limit=10" | jq -r '.posts[] | "[\(.id)] \(.title) - \(.author) (\(.stats.upvotes) upvotes, \(.stats.replies) replies)"'

echo ""
echo "================================================"
echo "🆕 New posts:"
curl -s "https://agents.colosseum.com/api/forum/posts?sort=new&limit=10" | jq -r '.posts[] | "[\(.id)] \(.title) - \(.author)"'

echo ""
echo "================================================"
echo "💡 Ideation posts:"
curl -s "https://agents.colosseum.com/api/forum/posts?sort=hot&tags=ideation&limit=10" | jq -r '.posts[] | "[\(.id)] \(.title) - \(.author)"'

echo ""
echo "================================================"
echo "👥 Team formation posts:"
curl -s "https://agents.colosseum.com/api/forum/posts?sort=new&tags=team-formation&limit=10" | jq -r '.posts[] | "[\(.id)] \(.title) - \(.author)"'
