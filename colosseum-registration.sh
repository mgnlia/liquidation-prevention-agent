#!/bin/bash
# Colosseum Agent Hackathon Registration Script
# DO NOT COMMIT THIS FILE - Contains sensitive API keys

echo "🚀 Registering agent for Colosseum Agent Hackathon..."

# Register agent
RESPONSE=$(curl -s -X POST https://agents.colosseum.com/api/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "liquidation-sentinel"}')

echo "Registration Response:"
echo "$RESPONSE" | jq '.'

# Extract and save API key and claim code
API_KEY=$(echo "$RESPONSE" | jq -r '.apiKey // empty')
CLAIM_CODE=$(echo "$RESPONSE" | jq -r '.claimCode // empty')

if [ -n "$API_KEY" ]; then
    echo ""
    echo "✅ Registration successful!"
    echo ""
    echo "⚠️  SAVE THESE CREDENTIALS IMMEDIATELY - SHOWN ONLY ONCE:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "API_KEY: $API_KEY"
    echo "CLAIM_CODE: $CLAIM_CODE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Next steps:"
    echo "1. Save API_KEY to .env as COLOSSEUM_API_KEY"
    echo "2. Give CLAIM_CODE to Henry (for prize claiming)"
    echo "3. Run: ./colosseum-setup-wallet.sh"
else
    echo "❌ Registration failed. Response:"
    echo "$RESPONSE"
    exit 1
fi
