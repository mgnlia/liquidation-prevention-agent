#!/bin/bash
# ETHDenver Emergency Deployment Script
# Run this if you have Sepolia ETH and want to deploy

echo "🚀 ETHDenver Emergency Deployment"
echo "================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Creating from template..."
    cp .env.example .env
    echo "⚠️  EDIT .env with your keys before continuing!"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Compile contracts
echo "🔨 Compiling contracts..."
npx hardhat compile

# Run tests (optional but recommended)
echo "🧪 Running tests..."
npx hardhat test

# Deploy to Sepolia
echo "🚀 Deploying to Sepolia..."
npx hardhat run scripts/deploy.js --network sepolia

echo ""
echo "✅ Deployment complete!"
echo "📝 Copy the contract addresses and update .env"
echo ""
echo "Next steps:"
echo "1. Verify contracts on Etherscan"
echo "2. Test agent with deployed contracts"
echo "3. Record demo video"
echo "4. Register on Devfolio"
