#!/usr/bin/env python3
"""
Quick status checker for Colosseum Hackathon
Shows: agent status, project status, time remaining, activity count
"""

import requests
import json
import os
from datetime import datetime

API_BASE = "https://agents.colosseum.com/api"

def load_credentials():
    """Load saved credentials"""
    try:
        with open("../.credentials.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ No credentials found. Run register_agent.py first.")
        return None

def get_status(api_key):
    """Get agent status"""
    try:
        response = requests.get(
            f"{API_BASE}/agents/status",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get status: {e}")
        return None

def get_project(api_key):
    """Get project details"""
    try:
        response = requests.get(
            f"{API_BASE}/my-project",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

def format_time(ms):
    """Format milliseconds to human readable"""
    seconds = ms / 1000
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{days}d {hours}h {minutes}m"

def main():
    print("=" * 60)
    print("🏆 COLOSSEUM HACKATHON STATUS")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    creds = load_credentials()
    if not creds:
        return
    
    api_key = creds.get("api_key")
    if not api_key:
        print("❌ No API key found in credentials")
        return
    
    # Get agent status
    status = get_status(api_key)
    if not status:
        return
    
    # Display agent info
    print("🤖 AGENT INFO")
    print("-" * 60)
    print(f"Name: {status.get('name', 'N/A')}")
    print(f"ID: {status.get('id', 'N/A')}")
    print(f"Status: {status.get('status', 'N/A')}")
    
    # Display hackathon info
    hackathon = status.get('hackathon', {})
    print(f"\n📅 HACKATHON STATUS")
    print("-" * 60)
    print(f"Name: {hackathon.get('name', 'N/A')}")
    print(f"Active: {'✅ YES' if hackathon.get('isActive') else '❌ NO'}")
    print(f"Current Day: {hackathon.get('currentDay', 'N/A')} of 10")
    print(f"Days Remaining: {hackathon.get('daysRemaining', 'N/A')}")
    
    if hackathon.get('timeRemainingMs'):
        time_str = format_time(hackathon['timeRemainingMs'])
        print(f"Time Remaining: {time_str}")
    
    # Display engagement
    engagement = status.get('engagement', {})
    print(f"\n💬 ENGAGEMENT")
    print("-" * 60)
    print(f"Forum Posts: {engagement.get('forumPostCount', 0)}")
    print(f"Replies Received: {engagement.get('repliesOnYourPosts', 0)}")
    print(f"Project Status: {engagement.get('projectStatus', 'none')}")
    
    # Display project if exists
    project = get_project(api_key)
    if project:
        print(f"\n🚀 PROJECT")
        print("-" * 60)
        print(f"Name: {project.get('name', 'N/A')}")
        print(f"Status: {project.get('status', 'N/A')}")
        if project.get('votes'):
            votes = project['votes']
            print(f"Human Votes: {votes.get('human', 0)}")
            print(f"Agent Votes: {votes.get('agent', 0)}")
            print(f"Total Votes: {votes.get('total', 0)}")
        if project.get('repoLink'):
            print(f"Repo: {project['repoLink']}")
        if project.get('demoLink'):
            print(f"Demo: {project['demoLink']}")
    
    # Display next steps
    next_steps = status.get('nextSteps', [])
    if next_steps:
        print(f"\n🎯 NEXT STEPS")
        print("-" * 60)
        for i, step in enumerate(next_steps, 1):
            print(f"{i}. {step}")
    
    # Display announcement
    announcement = status.get('announcement')
    if announcement:
        print(f"\n📢 ANNOUNCEMENT")
        print("-" * 60)
        print(announcement)
    
    # Check for active poll
    if status.get('hasActivePoll'):
        print(f"\n🗳️  ACTIVE POLL DETECTED")
        print("-" * 60)
        print("Run: python scripts/check_poll.py")
    
    print("\n" + "=" * 60)
    print("✅ Status check complete")
    print("💡 Tip: Run this script regularly to stay updated")

if __name__ == "__main__":
    main()
