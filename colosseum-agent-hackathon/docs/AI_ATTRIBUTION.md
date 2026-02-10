# AI Attribution Log

## Overview

SolShield uses AI in two ways:

1. **Development**: Claude (Anthropic) assisted with code generation and architecture design
2. **Runtime**: Claude claude-sonnet-4-20250514 powers the real-time risk analysis engine

## Development AI Usage

| Component | AI Contribution | Human Review |
|-----------|----------------|--------------|
| Anchor Programs | Architecture + implementation | Reviewed + tested |
| Protocol Adapters | Initial scaffolding | Customized for each protocol |
| AI Analyzer | Prompt engineering + fallback logic | Validated against test cases |
| Dashboard | Component generation | UI/UX refinement |
| Demo Script | Narrative flow | Verified accuracy |

## Runtime AI Usage

### Claude Risk Analyzer

The agent uses Claude claude-sonnet-4-20250514 for real-time position analysis:

- **Input**: Position data (health factor, collateral, debt, market context)
- **Output**: Risk assessment + recommended strategy + confidence score
- **Temperature**: 0.1 (low, for consistent risk analysis)
- **Fallback**: Rule-based analyzer if AI call fails

### Decision Transparency

Every AI decision includes:
- Full reasoning trace (stored in `agent/logs/`)
- SHA-256 hash of reasoning (recorded on-chain)
- Confidence score (only actions with ≥0.7 confidence are executed)
- Strategy recommendation with estimated amounts

### Verification

```bash
# Verify activity log integrity
cd agent
python -c "
import asyncio
from activity_logger import ActivityLogger
logger = ActivityLogger()
result = asyncio.run(logger.verify_integrity())
print(f'Valid: {result[0]}, Entries: {result[1]}')
"
```

## Model Details

| Parameter | Value |
|-----------|-------|
| Model | claude-sonnet-4-20250514 |
| Provider | Anthropic |
| Max Tokens | 2048 |
| Temperature | 0.1 |
| Use Case | DeFi risk analysis |

## Ethical Considerations

- Agent operates in dry-run mode by default
- All actions require minimum 0.7 confidence threshold
- Conservative bias: false positives (unnecessary rebalances) are preferred over false negatives (missed liquidations)
- Full audit trail for accountability
- User can pause/resume monitoring at any time
