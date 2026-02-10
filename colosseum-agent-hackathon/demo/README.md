# SolShield Demo

## Quick Demo (No Keys Required)

```bash
cd demo
python demo_simulation.py
```

This runs a full simulation of SolShield detecting and preventing a liquidation event.

## Live Demo (Requires API Keys)

```bash
# Set up environment
cp ../.env.example .env
# Add your ANTHROPIC_API_KEY and HELIUS_API_KEY

python demo_live.py --wallet <SOLANA_WALLET_ADDRESS>
```

## Demo Scenarios

1. **Healthy Position** — Agent monitors, no action needed
2. **Warning Threshold** — Health factor drops to 1.4, agent alerts
3. **Critical Position** — Health factor at 1.15, agent recommends debt repayment
4. **Emergency Liquidation Prevention** — Health factor at 1.03, agent executes emergency rebalance
5. **Multi-Protocol** — Simultaneous monitoring across Kamino + MarginFi + Solend
