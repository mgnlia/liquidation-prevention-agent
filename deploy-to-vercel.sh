#!/bin/bash

# Vercel Deployment Script for Liquidation Prevention Agent Frontend
# This script automates the Vercel deployment process

set -e

echo "🚀 Liquidation Prevention Agent - Vercel Deployment"
echo "=================================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if we're in the right directory
if [ ! -d "liquidation-frontend" ]; then
    echo "❌ Error: liquidation-frontend directory not found"
    echo "Please run this script from the repository root"
    exit 1
fi

echo "✅ Found liquidation-frontend directory"

# Navigate to frontend directory
cd liquidation-frontend

# Check for required files
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found in liquidation-frontend"
    exit 1
fi

if [ ! -f "next.config.js" ]; then
    echo "❌ Error: next.config.js not found"
    exit 1
fi

echo "✅ Configuration files found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

# Build locally to verify
echo ""
echo "🔨 Building project locally (verification)..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Local build successful!"
else
    echo "❌ Local build failed. Please fix errors before deploying."
    exit 1
fi

# Check for environment variables
echo ""
echo "🔍 Checking environment variables..."

if [ -z "$NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID" ]; then
    echo "⚠️  Warning: NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID not set"
    echo "   Get one from: https://cloud.walletconnect.com"
fi

if [ -z "$NEXT_PUBLIC_ALCHEMY_API_KEY" ]; then
    echo "⚠️  Warning: NEXT_PUBLIC_ALCHEMY_API_KEY not set"
    echo "   Get one from: https://dashboard.alchemy.com"
fi

# Deploy to Vercel
echo ""
echo "🚀 Deploying to Vercel..."
echo "   (You may need to login if this is your first time)"
echo ""

# Check if VERCEL_TOKEN is set for CI/CD
if [ -n "$VERCEL_TOKEN" ]; then
    echo "✅ Using VERCEL_TOKEN for authentication"
    vercel --prod --token="$VERCEL_TOKEN" --yes
else
    echo "📝 Interactive deployment (login required)"
    vercel --prod
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "🎉 Your app is now live!"
    echo ""
    echo "Next steps:"
    echo "1. Visit the URL shown above"
    echo "2. Test wallet connection"
    echo "3. Verify health factor dashboard"
    echo "4. Update README.md with the live URL"
    echo ""
    echo "📚 Need to set environment variables?"
    echo "   Run: vercel env add NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID"
    echo ""
else
    echo "❌ Deployment failed. Check the error messages above."
    exit 1
fi
