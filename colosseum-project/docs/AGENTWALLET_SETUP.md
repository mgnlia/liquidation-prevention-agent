# AgentWallet Setup Guide

**Purpose:** Set up persistent Solana wallet for on-chain activity logging

## Step 1: Fetch AgentWallet Skill

```bash
curl -s https://agentwallet.mcpay.tech/skill.md > agentwallet-skill.md
cat agentwallet-skill.md
```

## Step 2: Follow AgentWallet Instructions

AgentWallet provides:
- **Persistent Solana wallet** (survives restarts)
- **Ed25519 signing** (for activity verification)
- **Devnet SOL funding** (reliable, no rate limits)
- **Transaction sending** (memo program integration)

## Step 3: Key Operations Needed

### Get Wallet Address
```python
# We'll need to call AgentWallet API to get our address
wallet_address = agentwallet.get_address()
```

### Sign Activity Data
```python
# Sign activity hash with Ed25519
signature = agentwallet.sign(activity_hash)
```

### Send to Solana Memo Program
```python
# Send signed activity to blockchain
tx_signature = agentwallet.send_memo(
    memo_data=activity_data,
    signature=signature
)
```

## Step 4: Integration with Activity Logger

Update `agent/activity_logger.py` to:
1. Sign each activity with AgentWallet
2. Send to Solana memo program
3. Store transaction signature
4. Verify on-chain

## Step 5: Verification

```bash
# Check wallet balance
agentwallet balance

# View recent transactions
agentwallet transactions

# Verify specific activity
agentwallet verify <tx_signature>
```

## Timeline

- **Minute 0-10:** Read AgentWallet skill.md
- **Minute 10-20:** Set up wallet credentials
- **Minute 20-25:** Test signing
- **Minute 25-30:** Test memo program integration
- **Minute 30:** First on-chain activity! 🎉

## Next Steps After Setup

1. Update activity logger with AgentWallet integration
2. Log registration activity on-chain
3. Log all previous activities (retroactive)
4. Begin continuous logging
5. Target: 10+ activities in first hour

## Security Notes

- AgentWallet handles private keys (don't manage raw keys yourself)
- Credentials stored securely by AgentWallet
- Never expose wallet private keys
- All operations via AgentWallet API

## Troubleshooting

### "No devnet SOL"
- AgentWallet provides reliable funding
- Don't use `solana airdrop` (rate limited)

### "Wallet not found"
- Re-run AgentWallet setup
- Check credentials file

### "Transaction failed"
- Check devnet RPC status
- Verify memo program address
- Check SOL balance

## Resources

- AgentWallet Skill: https://agentwallet.mcpay.tech/skill.md
- Solana Memo Program: https://spl.solana.com/memo
- Devnet Explorer: https://explorer.solana.com/?cluster=devnet
