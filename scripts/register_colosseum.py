#!/usr/bin/env python3
"""
Colosseum Agent Hackathon Registration Script

This script handles:
1. Agent registration via Colosseum API
2. API key storage
3. Project creation
4. Initial activity logging setup
"""

import requests
import json
import os
from pathlib import Path
from datetime import datetime

# Configuration
COLOSSEUM_API_BASE = "https://agents.colosseum.com/api"
AGENT_NAME = "autonomous-office-protocol"
PROJECT_NAME = "Liquidation Sentinel"
PROJECT_DESCRIPTION = "AI-powered liquidation prevention on Solana using Claude AI and AgentWallet"
REPO_LINK = "https://github.com/mgnlia/colosseum-agent-hackathon"

def register_agent():
    """Register agent with Colosseum API"""
    print("🤖 Registering agent with Colosseum...")
    
    url = f"{COLOSSEUM_API_BASE}/agents"
    payload = {"name": AGENT_NAME}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        api_key = data.get("apiKey")
        claim_code = data.get("claimCode")
        
        print(f"✅ Agent registered successfully!")
        print(f"📝 Agent Name: {AGENT_NAME}")
        print(f"🔑 API Key: {api_key}")
        print(f"🎟️  Claim Code: {claim_code}")
        print(f"\n⚠️  IMPORTANT: Save your API key - it's only shown once!")
        
        # Save to .env file
        save_credentials(api_key, claim_code)
        
        return api_key, claim_code
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Registration failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None, None

def save_credentials(api_key, claim_code):
    """Save credentials to .env file"""
    env_path = Path(".env")
    
    # Read existing .env or create new
    if env_path.exists():
        with open(env_path, "r") as f:
            env_content = f.read()
    else:
        env_content = ""
    
    # Update or add credentials
    lines = env_content.split("\n")
    updated = False
    
    for i, line in enumerate(lines):
        if line.startswith("COLOSSEUM_API_KEY="):
            lines[i] = f"COLOSSEUM_API_KEY={api_key}"
            updated = True
        elif line.startswith("COLOSSEUM_CLAIM_CODE="):
            lines[i] = f"COLOSSEUM_CLAIM_CODE={claim_code}"
    
    if not updated:
        lines.extend([
            "",
            "# Colosseum Agent Hackathon",
            f"COLOSSEUM_API_KEY={api_key}",
            f"COLOSSEUM_CLAIM_CODE={claim_code}"
        ])
    
    with open(env_path, "w") as f:
        f.write("\n".join(lines))
    
    print(f"💾 Credentials saved to .env")

def create_project(api_key):
    """Create project via Colosseum API"""
    print("\n📦 Creating project...")
    
    url = f"{COLOSSEUM_API_BASE}/my-project"
    payload = {
        "name": PROJECT_NAME,
        "description": PROJECT_DESCRIPTION,
        "repoLink": REPO_LINK
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Project created successfully!")
        print(f"📝 Project: {PROJECT_NAME}")
        print(f"🔗 Repo: {REPO_LINK}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Project creation failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def log_initial_activity(api_key):
    """Log initial registration activity"""
    print("\n📊 Logging initial activity...")
    
    activity = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "activity_type": "registration",
        "data": {
            "agent_name": AGENT_NAME,
            "project_name": PROJECT_NAME,
            "status": "initialized"
        }
    }
    
    # Save locally
    activities_dir = Path("data/activities")
    activities_dir.mkdir(parents=True, exist_ok=True)
    
    activity_file = activities_dir / "registration.json"
    with open(activity_file, "w") as f:
        json.dump(activity, f, indent=2)
    
    print(f"✅ Activity logged locally: {activity_file}")
    
    # TODO: Push to Colosseum API once AgentWallet is set up
    print("⏳ On-chain logging pending AgentWallet setup")

def main():
    """Main registration flow"""
    print("=" * 60)
    print("🏆 COLOSSEUM AGENT HACKATHON - REGISTRATION")
    print("=" * 60)
    print()
    
    # Step 1: Register agent
    api_key, claim_code = register_agent()
    
    if not api_key:
        print("\n❌ Registration failed. Please check your network and try again.")
        print("\n📝 Manual registration command:")
        print(f"curl -X POST {COLOSSEUM_API_BASE}/agents \\")
        print(f'  -H "Content-Type: application/json" \\')
        print(f'  -d \'{{"name": "{AGENT_NAME}"}}\'')
        return
    
    # Step 2: Create project
    project = create_project(api_key)
    
    # Step 3: Log initial activity
    log_initial_activity(api_key)
    
    print("\n" + "=" * 60)
    print("✅ REGISTRATION COMPLETE!")
    print("=" * 60)
    print("\n📋 NEXT STEPS:")
    print("1. Set up AgentWallet: python scripts/setup_agentwallet.py")
    print("2. Start agent: python src/main.py")
    print("3. Monitor dashboard: cd dashboard && npm run dev")
    print("4. Engage on forum: https://colosseum.com/agent-hackathon/forum")
    print("\n🎯 TARGET: 500+ activities over 3 days")
    print("⏰ DEADLINE: February 12, 2026")
    print()

if __name__ == "__main__":
    main()
