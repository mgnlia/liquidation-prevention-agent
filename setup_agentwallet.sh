#!/bin/bash
# AgentWallet Setup Script

echo "🔐 AgentWallet Setup"
echo "================================================"
echo ""
echo "AgentWallet provides persistent Solana wallets for agents."
echo "DO NOT use 'solana-keygen new' or 'solana airdrop'."
echo ""
echo "Setup options:"
echo ""
echo "Option 1: Web Flow (Recommended for first-time setup)"
echo "  1. Go to: https://agentwallet.mcpay.tech/connect?email=YOUR_EMAIL"
echo "  2. Enter the 6-digit OTP sent to your email"
echo "  3. Save the credentials displayed"
echo ""
echo "Option 2: API Flow (for automation)"
read -p "Enter your email: " EMAIL

echo ""
echo "📧 Sending OTP to $EMAIL..."

RESPONSE=$(curl -X POST https://agentwallet.mcpay.tech/api/connect/start \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\"}" \
  -s)

echo "$RESPONSE"

USERNAME=$(echo "$RESPONSE" | jq -r '.username')

if [ "$USERNAME" != "null" ] && [ -n "$USERNAME" ]; then
  echo ""
  echo "✅ OTP sent! Username: $USERNAME"
  echo ""
  read -p "Enter the 6-digit OTP from your email: " OTP
  
  echo ""
  echo "🔑 Completing setup..."
  
  COMPLETE_RESPONSE=$(curl -X POST https://agentwallet.mcpay.tech/api/connect/complete \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$USERNAME\",\"email\":\"$EMAIL\",\"otp\":\"$OTP\"}" \
    -s)
  
  echo "$COMPLETE_RESPONSE"
  
  API_TOKEN=$(echo "$COMPLETE_RESPONSE" | jq -r '.apiToken')
  EVM_ADDRESS=$(echo "$COMPLETE_RESPONSE" | jq -r '.evmAddress')
  SOLANA_ADDRESS=$(echo "$COMPLETE_RESPONSE" | jq -r '.solanaAddress')
  
  if [ "$API_TOKEN" != "null" ] && [ -n "$API_TOKEN" ]; then
    echo ""
    echo "✅ AgentWallet setup complete!"
    echo ""
    echo "Username: $USERNAME"
    echo "EVM Address: $EVM_ADDRESS"
    echo "Solana Address: $SOLANA_ADDRESS"
    echo "API Token: $API_TOKEN"
    echo ""
    
    # Save to config
    mkdir -p ~/.agentwallet
    cat > ~/.agentwallet/config.json << EOF
{
  "username": "$USERNAME",
  "email": "$EMAIL",
  "evmAddress": "$EVM_ADDRESS",
  "solanaAddress": "$SOLANA_ADDRESS",
  "apiToken": "$API_TOKEN",
  "moltbookLinked": false,
  "moltbookUsername": null,
  "xHandle": null
}
EOF
    chmod 600 ~/.agentwallet/config.json
    
    echo "✅ Config saved to ~/.agentwallet/config.json"
    echo ""
    echo "Next steps:"
    echo "1. Fund your wallet: https://agentwallet.mcpay.tech/u/$USERNAME"
    echo "2. Check balance: curl https://agentwallet.mcpay.tech/api/wallets/$USERNAME/balances -H \"Authorization: Bearer $API_TOKEN\""
    echo "3. Start building on Solana!"
  else
    echo "❌ Setup failed. Check OTP and try again."
  fi
else
  echo "❌ Failed to send OTP. Check email and try again."
fi
