#!/usr/bin/env python3
"""
Colosseum Hackathon Heartbeat Monitor
Fetches heartbeat.md and checks for important updates
Should run every ~30 minutes
"""

import requests
import json
import os
from datetime import datetime
import re

HEARTBEAT_URL = "https://colosseum.com/heartbeat.md"
API_BASE = "https://agents.colosseum.com/api"

def fetch_heartbeat():
    """Fetch the latest heartbeat file"""
    try:
        response = requests.get(HEARTBEAT_URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch heartbeat: {e}")
        return None

def parse_heartbeat(content: str):
    """Parse heartbeat content for actionable items"""
    lines = content.split('\n')
    
    info = {
        "version": None,
        "current_day": None,
        "time_remaining": None,
        "action_items": [],
        "warnings": [],
        "forum_activity": []
    }
    
    for line in lines:
        # Extract version
        if "version:" in line.lower():
            info["version"] = line.split(":")[-1].strip()
        
        # Extract day info
        if "day " in line.lower() and "of 10" in line.lower():
            info["current_day"] = line.strip()
        
        # Extract time remaining
        if "remaining" in line.lower():
            info["time_remaining"] = line.strip()
        
        # Extract action items (lines starting with - [ ])
        if line.strip().startswith("- [ ]"):
            info["action_items"].append(line.strip()[6:])
        
        # Extract warnings (lines with ⚠️ or WARNING)
        if "⚠️" in line or "WARNING" in line.upper():
            info["warnings"].append(line.strip())
        
        # Extract forum mentions
        if "forum" in line.lower():
            info["forum_activity"].append(line.strip())
    
    return info

def check_agent_status(api_key: str):
    """Check agent status via API"""
    if not api_key:
        return None
    
    try:
        response = requests.get(
            f"{API_BASE}/agents/status",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Status check failed: {e}")
        return None

def check_active_poll(api_key: str):
    """Check if there's an active poll"""
    if not api_key:
        return None
    
    try:
        response = requests.get(
            f"{API_BASE}/agents/polls/active",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

def load_credentials():
    """Load API credentials"""
    try:
        with open("../.credentials.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def main():
    print("🫀 Colosseum Hackathon Heartbeat Check")
    print("=" * 50)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Fetch heartbeat
    print("📡 Fetching heartbeat...")
    content = fetch_heartbeat()
    
    if content:
        info = parse_heartbeat(content)
        
        print(f"📋 Version: {info['version']}")
        print(f"📅 {info['current_day']}")
        print(f"⏳ {info['time_remaining']}\n")
        
        if info['warnings']:
            print("⚠️  WARNINGS:")
            for warning in info['warnings']:
                print(f"  {warning}")
            print()
        
        if info['action_items']:
            print("✅ Action Items:")
            for item in info['action_items']:
                print(f"  • {item}")
            print()
        
        if info['forum_activity']:
            print("💬 Forum Activity:")
            for activity in info['forum_activity'][:5]:
                print(f"  • {activity}")
            print()
    
    # Check agent status
    creds = load_credentials()
    if creds and creds.get("api_key"):
        print("\n" + "=" * 50)
        print("🤖 Agent Status Check")
        
        status = check_agent_status(creds["api_key"])
        if status:
            print(f"  Agent: {status.get('name', 'N/A')}")
            print(f"  Current Day: {status.get('currentDay', 'N/A')}")
            print(f"  Days Remaining: {status.get('daysRemaining', 'N/A')}")
            print(f"  Time Remaining: {status.get('timeRemainingFormatted', 'N/A')}")
            
            if status.get('announcement'):
                print(f"\n  📢 ANNOUNCEMENT: {status['announcement']}")
            
            if status.get('hasActivePoll'):
                print("\n  🗳️  ACTIVE POLL DETECTED")
                poll = check_active_poll(creds["api_key"])
                if poll:
                    print(f"     Question: {poll.get('question', 'N/A')}")
                    print(f"     Respond via: POST /agents/polls/{poll.get('id')}/respond")
            
            if status.get('nextSteps'):
                print("\n  🎯 Suggested Next Steps:")
                for step in status['nextSteps'][:3]:
                    print(f"     • {step}")
    
    print("\n" + "=" * 50)
    print("✅ Heartbeat check complete")
    print("⏰ Next check in ~30 minutes")

if __name__ == "__main__":
    main()
