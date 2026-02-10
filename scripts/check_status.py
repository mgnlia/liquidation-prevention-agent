#!/usr/bin/env python3
"""
Status Checker for Colosseum Agent Hackathon

Displays:
- Total activities logged
- Leaderboard position
- Time remaining
- Activity rate
- Recommendations
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Configuration
COLOSSEUM_API_BASE = "https://agents.colosseum.com/api"
HACKATHON_END = datetime(2026, 2, 12, 23, 59, 59)  # Feb 12, 2026

def get_local_activity_count():
    """Count activities logged locally"""
    activities_dir = Path("data/activities")
    if not activities_dir.exists():
        return 0
    return len(list(activities_dir.glob("*.json")))

def get_leaderboard_position(api_key):
    """Fetch current leaderboard position"""
    if not api_key:
        return None
    
    try:
        response = requests.get(
            f"{COLOSSEUM_API_BASE}/leaderboard",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Failed to fetch leaderboard: {e}")
        return None

def calculate_time_remaining():
    """Calculate time remaining until deadline"""
    now = datetime.utcnow()
    remaining = HACKATHON_END - now
    
    days = remaining.days
    hours = remaining.seconds // 3600
    minutes = (remaining.seconds % 3600) // 60
    
    return days, hours, minutes, remaining.total_seconds()

def calculate_required_rate(current_count, target=500):
    """Calculate required activity rate to reach target"""
    _, _, _, seconds_remaining = calculate_time_remaining()
    
    activities_needed = target - current_count
    hours_remaining = seconds_remaining / 3600
    
    if hours_remaining <= 0:
        return 0, 0
    
    rate_per_hour = activities_needed / hours_remaining
    rate_per_day = rate_per_hour * 24
    
    return rate_per_hour, rate_per_day

def main():
    """Display status dashboard"""
    print("=" * 70)
    print("📊 COLOSSEUM AGENT HACKATHON - STATUS DASHBOARD")
    print("=" * 70)
    print()
    
    # Get API key
    api_key = os.getenv("COLOSSEUM_API_KEY")
    
    # Time remaining
    days, hours, minutes, _ = calculate_time_remaining()
    print(f"⏰ TIME REMAINING: {days}d {hours}h {minutes}m")
    print(f"📅 Deadline: {HACKATHON_END.strftime('%B %d, %Y %H:%M:%S UTC')}")
    print()
    
    # Activity count
    local_count = get_local_activity_count()
    print(f"📊 ACTIVITIES:")
    print(f"   Local: {local_count}")
    
    # Leaderboard
    if api_key:
        leaderboard = get_leaderboard_position(api_key)
        if leaderboard:
            print(f"   On-chain: {leaderboard.get('activity_count', 'N/A')}")
            print(f"   Rank: #{leaderboard.get('rank', 'N/A')}")
        else:
            print(f"   On-chain: Unable to fetch")
    else:
        print(f"   On-chain: Not configured (set COLOSSEUM_API_KEY)")
    print()
    
    # Target analysis
    TARGET = 500
    rate_hour, rate_day = calculate_required_rate(local_count, TARGET)
    
    print(f"🎯 TARGET ANALYSIS:")
    print(f"   Target: {TARGET} activities")
    print(f"   Current: {local_count}")
    print(f"   Remaining: {TARGET - local_count}")
    print(f"   Required rate: {rate_hour:.1f}/hour ({rate_day:.0f}/day)")
    print()
    
    # Competition intel
    print(f"🏆 COMPETITION:")
    print(f"   Leader (jarvis): 688+ activities")
    print(f"   Your position: {local_count} activities")
    print(f"   Gap: {688 - local_count}")
    print()
    
    # Recommendations
    print(f"💡 RECOMMENDATIONS:")
    
    if local_count == 0:
        print(f"   ❌ CRITICAL: No activities logged yet!")
        print(f"   → Run: python scripts/register_colosseum.py")
        print(f"   → Run: python scripts/setup_agentwallet.py")
        print(f"   → Run: python src/main.py")
    elif rate_hour < 7:
        print(f"   ✅ On track - maintain current rate")
    elif rate_hour < 15:
        print(f"   ⚠️  Moderate effort needed - {rate_hour:.1f} activities/hour")
        print(f"   → Reduce cycle interval in src/main.py")
        print(f"   → Add forum engagement activities")
    else:
        print(f"   🔴 AGGRESSIVE action needed - {rate_hour:.1f} activities/hour")
        print(f"   → Run agent continuously")
        print(f"   → Add automated forum posting")
        print(f"   → Increase activity diversity")
    
    print()
    print(f"📝 NEXT ACTIONS:")
    print(f"   1. Ensure agent is running: python src/main.py")
    print(f"   2. Monitor this dashboard: python scripts/check_status.py")
    print(f"   3. Engage on forum: https://colosseum.com/agent-hackathon/forum")
    print(f"   4. Review activities: ls -la data/activities/")
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
