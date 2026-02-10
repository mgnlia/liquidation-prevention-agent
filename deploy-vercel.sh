#!/bin/bash
set -e

echo "🚀 Deploying Liquidation Prevention Agent to Vercel..."

# Check if VERCEL_TOKEN is set
if [ -z "$VERCEL_TOKEN" ]; then
  echo "❌ Error: VERCEL_TOKEN environment variable is not set"
  echo "Please set it with: export VERCEL_TOKEN=your_token_here"
  exit 1
fi

# Install Vercel CLI if not present
if ! command -v vercel &> /dev/null; then
  echo "📦 Installing Vercel CLI..."
  npm install -g vercel
fi

# Navigate to frontend directory
cd liquidation-frontend

# Deploy to Vercel
echo "🌐 Deploying to Vercel..."
vercel --prod --token "$VERCEL_TOKEN" --yes

echo "✅ Deployment complete!"
