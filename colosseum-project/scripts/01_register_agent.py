#!/usr/bin/env python3
"""
Step 1: Register agent with Colosseum Hackathon API
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

API_BASE = "https://agents.colosseum.com/api"
AGENT_NAME = "Autonomous-Office-Protocol"

def register_agent():
    """Register our agent with Colosseum"""
    url = f"{API_BASE}/agents"
    payload = {"name": AGENT_NAME}
    
    print("=" * 60)
    print("🚀 COLOSSEUM AGENT REGISTRATION")
    print("=" * 60)
    print(f"Agent Name: {AGENT_NAME}")
    print(f"API Endpoint: {url}")
    print()
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        
        print("✅ REGISTRATION SUCCESSFUL!")
        print()
        print("📋 Agent Details:")
        print(f"  ID: {data.get('id', 'N/A')}")
        print(f"  Name: {data.get('name', 'N/A')}")
        print()
        print("🔑 API Key (SAVE THIS - SHOWN ONLY ONCE):")
        print(f"  {data.get('apiKey', 'N/A')}")
        print()
        print("🎫 Claim Code (SHARE WITH HUMAN):")
        print(f"  {data.get('claimCode', 'N/A')}")
        print()
        
        # Save credentials
        save_credentials(data)
        
        # Log this activity
        log_registration_activity(data)
        
        return data
        
    except requests.exceptions.RequestException as e:
        print("❌ REGISTRATION FAILED!")
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        raise

def save_credentials(data):
    """Save API credentials securely"""
    credentials_dir = Path(__file__).parent.parent
    credentials_file = credentials_dir / ".credentials.json"
    
    credentials = {
        "api_key": data.get("apiKey"),
        "claim_code": data.get("claimCode"),
        "agent_id": data.get("id"),
        "agent_name": data.get("name"),
        "registered_at": datetime.now().isoformat(),
        "api_base": API_BASE
    }
    
    with open(credentials_file, 'w') as f:
        json.dump(credentials, f, indent=2)
    
    print("💾 Credentials saved to .credentials.json")
    print("⚠️  KEEP THIS FILE SECRET!")
    print()

def log_registration_activity(data):
    """Log registration as first activity"""
    activity_log = Path(__file__).parent.parent / "activities.json"
    
    activity = {
        "id": "activity_0000",
        "agent_id": data.get("id"),
        "agent_name": data.get("name"),
        "activity_type": "registration",
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "hackathon": "Colosseum Agent Hackathon 2026",
            "registered_at": datetime.now().isoformat()
        }
    }
    
    activities = [activity]
    
    with open(activity_log, 'w') as f:
        json.dump(activities, f, indent=2)
    
    print("📝 First activity logged to activities.json")
    print()

def check_status(api_key):
    """Check agent status"""
    url = f"{API_BASE}/agents/status"
    
    try:
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30
        )
        response.raise_for_status()
        
        status = response.json()
        
        print("=" * 60)
        print("📊 AGENT STATUS")
        print("=" * 60)
        
        hackathon = status.get('hackathon', {})
        print(f"Hackathon: {hackathon.get('name', 'N/A')}")
        print(f"Active: {'✅ YES' if hackathon.get('isActive') else '❌ NO'}")
        print(f"Current Day: {hackathon.get('currentDay', 'N/A')} of 10")
        print(f"Days Remaining: {hackathon.get('daysRemaining', 'N/A')}")
        print(f"Time Remaining: {hackathon.get('timeRemainingFormatted', 'N/A')}")
        print()
        
        engagement = status.get('engagement', {})
        print(f"Forum Posts: {engagement.get('forumPostCount', 0)}")
        print(f"Project Status: {engagement.get('projectStatus', 'none')}")
        print()
        
        if status.get('announcement'):
            print(f"📢 ANNOUNCEMENT:")
            print(f"  {status['announcement']}")
            print()
        
        if status.get('nextSteps'):
            print("🎯 Next Steps:")
            for i, step in enumerate(status['nextSteps'], 1):
                print(f"  {i}. {step}")
            print()
        
        return status
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Status check failed: {e}")
        return None

if __name__ == "__main__":
    print()
    print("🏁 Starting Colosseum Agent Hackathon Registration...")
    print()
    
    # Register
    data = register_agent()
    
    # Check status
    if data.get("apiKey"):
        print("=" * 60)
        check_status(data["apiKey"])
    
    print("=" * 60)
    print("✅ REGISTRATION COMPLETE")
    print("=" * 60)
    print()
    print("🎯 Next Steps:")
    print("  1. Share claim code with Henry: " + data.get("claimCode", "N/A"))
    print("  2. Set up AgentWallet: python scripts/02_setup_agentwallet.py")
    print("  3. Start logging activities on-chain")
    print()
    print("⏰ Time is ticking - move fast!")
    print()
