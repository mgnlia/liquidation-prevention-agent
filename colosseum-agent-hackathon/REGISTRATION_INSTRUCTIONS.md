# 🚨 REGISTRATION INSTRUCTIONS FOR HENRY — DO THIS NOW 🚨

## Step 1: Register the Agent

Run this in your terminal:

```bash
curl -X POST https://agents.colosseum.com/api/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "SolShield"}'
```

**SAVE THE RESPONSE.** It contains:
- `apiKey` — shown ONCE, cannot be recovered
- `claimCode` — you'll use this to claim prizes
- `id` — our agent ID

## Step 2: Create the Project

Replace `YOUR_API_KEY` with the key from Step 1:

```bash
curl -X POST https://agents.colosseum.com/api/my-project \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SolShield — Autonomous Liquidation Prevention Agent",
    "description": "Autonomous AI agent that monitors DeFi lending positions across Solana protocols (Kamino, MarginFi, Solend) and proactively prevents liquidations. Uses Claude AI for intelligent risk analysis and executes autonomous rebalancing via Jupiter swaps. Unlike simple monitors that only alert, SolShield takes action — analyzing health factors in real-time, computing optimal rebalancing strategies, and executing transactions before liquidation occurs. Features: multi-protocol monitoring, Claude-powered risk reasoning with cryptographic audit trail, Jupiter-routed collateral swaps, Anchor on-chain position registry, and a real-time monitoring dashboard. Built with Python + Anchor + Next.js.",
    "repoLink": "https://github.com/mgnlia/colosseum-agent-hackathon",
    "solanaIntegration": "Anchor programs for on-chain position registry and rebalance records. Monitors Kamino/MarginFi/Solend obligation accounts via Helius RPC. Executes rebalancing through Jupiter swap aggregator. All AI decisions logged with SHA-256 hashes for on-chain attestation via Solana memo program. AgentWallet integration for secure key management."
  }'
```

## Step 3: Set Up AgentWallet

Replace `YOUR_API_KEY`:

```bash
curl -X POST https://agentwallet.mcpay.tech/api/wallets \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "solshield-wallet"}'
```

## Step 4: Claim the Agent (Human Step)

The response from Step 1 includes a `claimCode`. Visit:
```
https://colosseum.com/agent-hackathon/claim?code=YOUR_CLAIM_CODE
```

Sign in with your X (Twitter) account to link the agent to your identity.

## Step 5: Report Back

Send Dev the following from the responses:
- `apiKey` from Step 1
- `claimCode` from Step 1
- `id` (agent ID) from Step 1
- `walletId` from Step 3
- Any `publicKey` / wallet address from Step 3

## IMPORTANT NOTES
- The API key is shown ONCE. Save it immediately.
- The project MUST be created (Step 2) to appear on the projects page.
- Without this, judges cannot see or evaluate our work.
- 3 days remaining.
