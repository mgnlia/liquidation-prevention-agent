#!/bin/bash

# AI-Powered Liquidation Prevention Agent - Setup Script
# HackMoney 2026

set -e

echo "🚀 AI-Powered Liquidation Prevention Agent - Setup"
echo "=================================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Node.js
echo "🔍 Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found. Please install Node.js >= 18.0.0${NC}"
    exit 1
fi
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo -e "${RED}❌ Node.js version too old. Please upgrade to >= 18.0.0${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js $(node -v) found${NC}"

# Check Python
echo "🔍 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python >= 3.10${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f2)
if [ "$PYTHON_VERSION" -lt 10 ]; then
    echo -e "${RED}❌ Python version too old. Please upgrade to >= 3.10${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $(python3 --version) found${NC}"

# Check npm
echo "🔍 Checking npm..."
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm not found. Please install npm${NC}"
    exit 1
fi
echo -e "${GREEN}✅ npm $(npm -v) found${NC}"

# Check pip
echo "🔍 Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 not found. Please install pip3${NC}"
    exit 1
fi
echo -e "${GREEN}✅ pip3 found${NC}"

echo ""
echo "📦 Installing dependencies..."
echo ""

# Install contract dependencies
echo "1️⃣  Installing contract dependencies..."
cd contracts
npm install
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Contract dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install contract dependencies${NC}"
    exit 1
fi
cd ..

# Install agent dependencies
echo ""
echo "2️⃣  Installing agent dependencies..."
cd agent
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Agent dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install agent dependencies${NC}"
    exit 1
fi
cd ..

# Install frontend dependencies
echo ""
echo "3️⃣  Installing frontend dependencies..."
cd frontend
npm install
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install frontend dependencies${NC}"
    exit 1
fi
cd ..

echo ""
echo "🔧 Creating environment files..."
echo ""

# Create contracts .env if not exists
if [ ! -f "contracts/.env" ]; then
    cat > contracts/.env << 'EOF'
# Network Configuration
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
PRIVATE_KEY=your_private_key_without_0x_prefix
ETHERSCAN_API_KEY=your_etherscan_api_key

# Sepolia Contract Addresses (Official Aave V3 & Compound V3)
AAVE_V3_POOL=0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951
AAVE_V3_POOL_ADDRESSES_PROVIDER=0x012bAC54348C0E635dCAc9D5FB99f06F24136C9A
COMPOUND_V3_COMET_USDC=0xAec1F48e02Cfb822Be958B68C7957156EB3F0b6e

# Deployment Configuration
AI_AGENT_ADDRESS=your_agent_wallet_address
HEALTH_FACTOR_THRESHOLD=1500000000000000000
EOF
    echo -e "${GREEN}✅ Created contracts/.env${NC}"
    echo -e "${YELLOW}⚠️  Please edit contracts/.env with your API keys${NC}"
else
    echo -e "${YELLOW}ℹ️  contracts/.env already exists${NC}"
fi

# Create agent .env if not exists
if [ ! -f "agent/.env" ]; then
    cat > agent/.env << 'EOF'
# Blockchain Configuration
WEB3_PROVIDER_URI=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
CHAIN_ID=11155111
NETWORK_NAME=sepolia

# Contract Addresses (fill after deployment)
LIQUIDATION_PREVENTION_ADDRESS=
AAVE_ADAPTER_ADDRESS=
COMPOUND_ADAPTER_ADDRESS=
FLASH_LOAN_REBALANCER_ADDRESS=

# Agent Configuration
AGENT_PRIVATE_KEY=your_agent_wallet_private_key
ANTHROPIC_API_KEY=sk-ant-your-claude-api-key

# Monitoring Configuration
MONITOR_INTERVAL_SECONDS=60
HEALTH_FACTOR_THRESHOLD=1.5
MIN_AGENT_BALANCE_ETH=0.1

# The Graph (optional)
SUBGRAPH_URL=
EOF
    echo -e "${GREEN}✅ Created agent/.env${NC}"
    echo -e "${YELLOW}⚠️  Please edit agent/.env with your API keys${NC}"
else
    echo -e "${YELLOW}ℹ️  agent/.env already exists${NC}"
fi

# Create frontend .env.local if not exists
if [ ! -f "frontend/.env.local" ]; then
    cat > frontend/.env.local << 'EOF'
NEXT_PUBLIC_CHAIN_ID=11155111
NEXT_PUBLIC_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
NEXT_PUBLIC_LIQUIDATION_PREVENTION_ADDRESS=
NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID=your_walletconnect_project_id
EOF
    echo -e "${GREEN}✅ Created frontend/.env.local${NC}"
    echo -e "${YELLOW}⚠️  Please edit frontend/.env.local with your API keys${NC}"
else
    echo -e "${YELLOW}ℹ️  frontend/.env.local already exists${NC}"
fi

echo ""
echo "🧪 Compiling contracts..."
cd contracts
npx hardhat compile
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Contracts compiled successfully${NC}"
else
    echo -e "${RED}❌ Contract compilation failed${NC}"
    exit 1
fi
cd ..

echo ""
echo "=================================================="
echo -e "${GREEN}✅ Setup complete!${NC}"
echo "=================================================="
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Get Sepolia ETH from faucets:"
echo "   • https://sepoliafaucet.com/"
echo "   • https://www.alchemy.com/faucets/ethereum-sepolia"
echo ""
echo "2. Configure environment files:"
echo "   • contracts/.env - Add RPC URL, private key, Etherscan API key"
echo "   • agent/.env - Add Claude API key, agent private key"
echo "   • frontend/.env.local - Add RPC URL, WalletConnect project ID"
echo ""
echo "3. Deploy contracts:"
echo "   cd contracts"
echo "   npx hardhat run scripts/deploy.js --network sepolia"
echo ""
echo "4. Verify contracts:"
echo "   npx hardhat run scripts/verify.js --network sepolia"
echo ""
echo "5. Update agent/.env with deployed contract addresses"
echo ""
echo "6. Start the AI agent:"
echo "   cd agent"
echo "   python3 agent.py"
echo ""
echo "7. Start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "📖 For detailed instructions, see:"
echo "   • QUICKSTART.md - 10-minute quick start"
echo "   • docs/DEPLOYMENT.md - Complete deployment guide"
echo "   • docs/DEMO.md - Demo video script"
echo "   • SUBMISSION_CHECKLIST.md - Submission checklist"
echo ""
echo "🏆 Good luck with HackMoney 2026!"
echo ""
