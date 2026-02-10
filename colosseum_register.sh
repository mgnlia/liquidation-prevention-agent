#!/bin/bash
# Colosseum Agent Hackathon Registration Script
# Execute this to register the agent

echo "🚀 Registering agent: autonomous-office-protocol"
echo "================================================"

# Step 1: Register Agent
echo -e "\n📝 Step 1: Registering agent..."
RESPONSE=$(curl -X POST https://agents.colosseum.com/api/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "autonomous-office-protocol"}' \
  -s)

echo "$RESPONSE"

# Extract apiKey and claimCode (requires jq)
if command -v jq &> /dev/null; then
  API_KEY=$(echo "$RESPONSE" | jq -r '.apiKey')
  CLAIM_CODE=$(echo "$RESPONSE" | jq -r '.claimCode')
  
  echo -e "\n✅ Registration successful!"
  echo "API_KEY: $API_KEY"
  echo "CLAIM_CODE: $CLAIM_CODE"
  
  # Save to .env file
  echo -e "\n💾 Saving credentials..."
  cat > .env.colosseum << EOF
COLOSSEUM_API_KEY=$API_KEY
COLOSSEUM_CLAIM_CODE=$CLAIM_CODE
COLOSSEUM_AGENT_NAME=autonomous-office-protocol
EOF
  
  echo "✅ Credentials saved to .env.colosseum"
  echo ""
  echo "⚠️  IMPORTANT: Save these credentials securely!"
  echo "   API Key cannot be recovered if lost."
  echo ""
  
else
  echo -e "\n⚠️  jq not found. Please manually extract apiKey and claimCode from response above."
fi

echo "================================================"
echo "Next steps:"
echo "1. Save the API_KEY and CLAIM_CODE"
echo "2. Run: source .env.colosseum"
echo "3. Create project (see colosseum_create_project.sh)"
echo "4. Set up AgentWallet"
echo "5. Start logging activities"
