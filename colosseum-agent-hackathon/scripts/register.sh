#!/bin/bash
# Register SolShield agent on Colosseum Agent Hackathon
curl -s -X POST https://agents.colosseum.com/api/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "solshield"}'
