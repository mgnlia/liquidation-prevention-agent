#!/usr/bin/env bash
set -euo pipefail

# SolShield Demo Runner
# Usage: ./scripts/demo.sh [--full | --agent | --dashboard]

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════╗"
echo "║  🛡️  SolShield Demo Runner                   ║"
echo "╚══════════════════════════════════════════════╝"
echo -e "${NC}"

MODE="${1:---full}"

run_demo_agent() {
    echo -e "${GREEN}▶ Running AI Agent Demo...${NC}"
    echo ""
    cd agent
    python demo.py
    cd ..
}

run_dashboard() {
    echo -e "${GREEN}▶ Starting Dashboard...${NC}"
    echo -e "${YELLOW}  Open http://localhost:3000 in your browser${NC}"
    echo ""
    cd dashboard
    npm run dev
}

run_agent_live() {
    echo -e "${GREEN}▶ Starting SolShield Agent (dry-run mode)...${NC}"
    echo ""
    cd agent
    python main.py --wallet 11111111111111111111111111111111
}

check_deps() {
    echo -e "${CYAN}Checking dependencies...${NC}"

    if ! command -v python &>/dev/null; then
        echo -e "${RED}✗ Python not found. Install Python 3.11+${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Python $(python --version 2>&1 | cut -d' ' -f2)${NC}"

    if ! command -v node &>/dev/null; then
        echo -e "${YELLOW}⚠ Node.js not found (needed for dashboard)${NC}"
    else
        echo -e "${GREEN}✓ Node.js $(node --version)${NC}"
    fi

    if python -c "import anthropic" 2>/dev/null; then
        echo -e "${GREEN}✓ anthropic SDK installed${NC}"
    else
        echo -e "${YELLOW}⚠ Installing agent dependencies...${NC}"
        cd agent && pip install -r requirements.txt && cd ..
    fi

    echo ""
}

case "$MODE" in
    --full)
        check_deps
        echo -e "${CYAN}Running full demo sequence...${NC}"
        echo ""
        run_demo_agent
        echo ""
        echo -e "${GREEN}Demo complete! To start the live dashboard:${NC}"
        echo -e "  cd dashboard && npm install && npm run dev"
        ;;
    --agent)
        check_deps
        run_agent_live
        ;;
    --dashboard)
        run_dashboard
        ;;
    --help | -h)
        echo "Usage: ./scripts/demo.sh [MODE]"
        echo ""
        echo "Modes:"
        echo "  --full       Run demo agent + show instructions (default)"
        echo "  --agent      Start live agent in dry-run mode"
        echo "  --dashboard  Start Next.js dashboard"
        echo "  --help       Show this help"
        ;;
    *)
        echo -e "${RED}Unknown mode: $MODE${NC}"
        echo "Run: ./scripts/demo.sh --help"
        exit 1
        ;;
esac
