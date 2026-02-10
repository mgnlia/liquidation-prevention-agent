#!/usr/bin/env python3
"""
Colosseum Agent Hackathon Registration Script
Registers our agent with the hackathon API
"""

import requests
import json
import os
from datetime import datetime

API_BASE = "https://agents.colosseum.com/api"

def register_agent(agent_name: str):
    """
    Register agent with Colosseum hackathon
    Returns: (api_key, claim_code, agent_data)
    """
    url = f"{API_BASE}/agents"
    payload = {"name": agent_name}
    
    print(f"🚀 Registering agent: {agent_name}")
    print(f"📡 Endpoint: {url}")
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        data = response.json()
        
        print("✅ Registration successful!")
        print(f"🔑 API Key: {data.get('apiKey', 'N/A')}")
        print(f"🎫 Claim Code: {data.get('claimCode', 'N/A')}")
        print(f"📋 Agent ID: {data.get('id', 'N/A')}")
        
        # Save credentials securely
        save_credentials(data)
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Registration failed: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        raise

def save_credentials(data: dict):
    """Save API credentials to secure file"""
    credentials_file = "../.credentials.json"
    
    credentials = {
        "api_key": data.get("apiKey"),
        "claim_code": data.get("claimCode"),
        "agent_id": data.get("id"),
        "agent_name": data.get("name"),
        "registered_at": datetime.now().isoformat()
    }
    
    with open(credentials_file, 'w') as f:
        json.dump(credentials, f, indent=2)
    
    print(f"💾 Credentials saved to {credentials_file}")
    print("⚠️  KEEP THIS FILE SECRET - Add to .gitignore")

def get_agent_status(api_key: str):
    """Check agent status"""
    url = f"{API_BASE}/agents/status"
    
    try:
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {api_key}"}
        )
        response.raise_for_status()
        
        status = response.json()
        print("\n📊 Agent Status:")
        print(json.dumps(status, indent=2))
        
        return status
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Status check failed: {e}")
        raise

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python register_agent.py <agent_name>")
        print("Example: python register_agent.py 'AI-Office-Dev'")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    
    # Register
    data = register_agent(agent_name)
    
    # Check status
    if data.get("apiKey"):
        print("\n" + "="*50)
        get_agent_status(data["apiKey"])
    
    print("\n" + "="*50)
    print("🎯 Next Steps:")
    print("1. Share claim code with your human: " + data.get("claimCode", "N/A"))
    print("2. Set up AgentWallet: curl -s https://agentwallet.mcpay.tech/skill.md")
    print("3. Configure heartbeat sync (30min intervals)")
    print("4. Start building your Solana project!")
