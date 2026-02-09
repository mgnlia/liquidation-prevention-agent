#!/bin/bash
# ETHDenver Emergency Localhost Demo
# Run this for immediate demo without testnet

echo "🏠 ETHDenver Localhost Demo Setup"
echo "================================="

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Compile contracts
echo "🔨 Compiling contracts..."
npx hardhat compile

# Start local node in background
echo "🌐 Starting local Hardhat node..."
npx hardhat node > hardhat-node.log 2>&1 &
NODE_PID=$!
echo "Node PID: $NODE_PID"
sleep 5

# Deploy to localhost
echo "🚀 Deploying contracts to localhost..."
npx hardhat run scripts/deploy.js --network localhost

echo ""
echo "✅ Localhost deployment complete!"
echo ""
echo "📹 NOW RECORD YOUR DEMO:"
echo "1. Open another terminal"
echo "2. Run: npx hardhat console --network localhost"
echo "3. Follow docs/LOCALHOST_DEMO.md for demo script"
echo "4. Record your screen while demonstrating"
echo ""
echo "To stop the node: kill $NODE_PID"
echo "Node logs: tail -f hardhat-node.log"
