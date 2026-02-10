#!/usr/bin/env python3
"""
EXECUTE REGISTRATION NOW
This script will be run to register our agent
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import and run registration
from scripts.register_agent_01 import register_agent, check_status, save_credentials, log_registration_activity
import requests
import json
from datetime import datetime
from pathlib import Path

API_BASE = "https://agents.colosseum.com/api"
AGENT_NAME = "Autonomous-Office-Protocol"

print("\n" + "="*70)
print("🚀 COLOSSEUM AGENT HACKATHON - REGISTRATION STARTING")
print("="*70 + "\n")

print(f"⏰ Timestamp: {datetime.now().isoformat()}")
print(f"🤖 Agent Name: {AGENT_NAME}")
print(f"📡 API Endpoint: {API_BASE}/agents")
print()

# Execute registration
try:
    url = f"{API_BASE}/agents"
    payload = {"name": AGENT_NAME}
    
    print("📤 Sending registration request...")
    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    print(f"📥 Response Status: {response.status_code}")
    
    if response.status_code == 201 or response.status_code == 200:
        data = response.json()
        
        print("\n" + "="*70)
        print("✅ REGISTRATION SUCCESSFUL!")
        print("="*70 + "\n")
        
        print("📋 Agent Details:")
        print(f"   ID: {data.get('id', 'N/A')}")
        print(f"   Name: {data.get('name', 'N/A')}")
        print()
        
        print("🔑 API Key (SAVE THIS - SHOWN ONLY ONCE):")
        print(f"   {data.get('apiKey', 'N/A')}")
        print()
        
        print("🎫 Claim Code (SHARE WITH HENRY):")
        print(f"   {data.get('claimCode', 'N/A')}")
        print()
        
        # Save credentials
        credentials_file = Path(__file__).parent.parent / ".credentials.json"
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
        
        # Check status
        print("="*70)
        print("📊 CHECKING AGENT STATUS")
        print("="*70 + "\n")
        
        status_url = f"{API_BASE}/agents/status"
        status_response = requests.get(
            status_url,
            headers={"Authorization": f"Bearer {data.get('apiKey')}"},
            timeout=30
        )
        
        if status_response.status_code == 200:
            status = status_response.json()
            hackathon = status.get('hackathon', {})
            
            print(f"🏆 Hackathon: {hackathon.get('name', 'N/A')}")
            print(f"✅ Active: {'YES' if hackathon.get('isActive') else 'NO'}")
            print(f"📅 Day: {hackathon.get('currentDay', 'N/A')} of 10")
            print(f"⏰ Days Remaining: {hackathon.get('daysRemaining', 'N/A')}")
            print(f"⏳ Time Remaining: {hackathon.get('timeRemainingFormatted', 'N/A')}")
            print()
            
            if status.get('nextSteps'):
                print("🎯 Next Steps:")
                for step in status['nextSteps']:
                    print(f"   • {step}")
                print()
        
        print("="*70)
        print("✅ REGISTRATION COMPLETE - READY FOR PHASE 2")
        print("="*70 + "\n")
        
        print("🎯 Immediate Next Actions:")
        print("   1. Share claim code with Henry: " + data.get('claimCode', 'N/A'))
        print("   2. Set up AgentWallet (30 min)")
        print("   3. Start on-chain activity logging")
        print()
        
    else:
        print(f"\n❌ Registration failed with status {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ Registration error: {e}")
    import traceback
    traceback.print_exc()
