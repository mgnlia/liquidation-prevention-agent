#!/bin/bash

# Deploy liquidation-prevention-agent frontend to Vercel
# This script deploys the /liquidation-frontend directory

echo "🚀 Deploying Liquidation Prevention Agent Frontend to Vercel..."

# Check if we're in the right directory
if [ ! -d "liquidation-frontend" ]; then
    echo "❌ Error: liquidation-frontend directory not found"
    echo "Please run this script from the repository root"
    exit 1
fi

# Navigate to frontend directory
cd liquidation-frontend

echo "📦 Installing dependencies..."
npm install

echo "🏗️ Building Next.js app..."
npm run build

echo "☁️ Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
