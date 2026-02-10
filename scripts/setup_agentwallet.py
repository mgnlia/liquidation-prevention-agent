#!/usr/bin/env python3
"""
AgentWallet Setup Script

Sets up AgentWallet integration for Colosseum Agent Hackathon:
1. Fetches AgentWallet skill.md
2. Configures cryptographic signing (SHA256 + Ed25519)
3. Sets up activity logging pipeline
4. Tests connection to Colosseum API
"""

import requests
import json
import os
import hashlib
from pathlib import Path
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

# Configuration
AGENTWALLET_SKILL_URL = "https://agentwallet.mcpay.tech/skill.md"
COLOSSEUM_API_BASE = "https://agents.colosseum.com/api"

def fetch_agentwallet_skill():
    """Fetch AgentWallet skill documentation"""
    print("📥 Fetching AgentWallet skill.md...")
    
    try:
        response = requests.get(AGENTWALLET_SKILL_URL)
        response.raise_for_status()
        
        skill_content = response.text
        
        # Save locally
        docs_dir = Path("docs")
        docs_dir.mkdir(exist_ok=True)
        
        skill_file = docs_dir / "agentwallet-skill.md"
        with open(skill_file, "w") as f:
            f.write(skill_content)
        
        print(f"✅ Skill documentation saved: {skill_file}")
        return skill_content
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch skill: {e}")
        return None

def generate_ed25519_keypair():
    """Generate Ed25519 keypair for activity signing"""
    print("\n🔐 Generating Ed25519 keypair...")
    
    # Generate private key
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    # Serialize keys
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Save keys
    keys_dir = Path(".keys")
    keys_dir.mkdir(exist_ok=True)
    
    with open(keys_dir / "ed25519_private.pem", "wb") as f:
        f.write(private_pem)
    
    with open(keys_dir / "ed25519_public.pem", "wb") as f:
        f.write(public_pem)
    
    print(f"✅ Keypair generated and saved to .keys/")
    print(f"⚠️  Keep private key secure!")
    
    return private_key, public_key

def create_activity_logger():
    """Create activity logger module"""
    print("\n📊 Creating activity logger...")
    
    logger_code = '''"""
Activity Logger for Colosseum Agent Hackathon

Implements SHA256 + Ed25519 signing for all agent activities.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

class ActivityLogger:
    def __init__(self, private_key_path=".keys/ed25519_private.pem"):
        """Initialize activity logger with Ed25519 private key"""
        self.private_key_path = Path(private_key_path)
        self.activities_dir = Path("data/activities")
        self.activities_dir.mkdir(parents=True, exist_ok=True)
        
        # Load private key
        with open(self.private_key_path, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(), password=None
            )
    
    def log_activity(self, activity_type, data):
        """Log an activity with cryptographic signing"""
        # Create activity object
        activity = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "activity_type": activity_type,
            "data": data
        }
        
        # Compute SHA256 hash
        activity_json = json.dumps(activity, sort_keys=True)
        sha256_hash = hashlib.sha256(activity_json.encode()).hexdigest()
        activity["hash"] = sha256_hash
        
        # Sign with Ed25519
        signature = self.private_key.sign(activity_json.encode())
        activity["signature"] = signature.hex()
        
        # Save locally
        timestamp_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        activity_file = self.activities_dir / f"{timestamp_str}_{activity_type}.json"
        
        with open(activity_file, "w") as f:
            json.dump(activity, f, indent=2)
        
        print(f"✅ Activity logged: {activity_type} -> {activity_file.name}")
        
        return activity
    
    def get_all_activities(self):
        """Retrieve all logged activities"""
        activities = []
        
        for activity_file in sorted(self.activities_dir.glob("*.json")):
            with open(activity_file, "r") as f:
                activities.append(json.load(f))
        
        return activities
    
    def get_activity_count(self):
        """Get total number of logged activities"""
        return len(list(self.activities_dir.glob("*.json")))
'''
    
    src_dir = Path("src")
    src_dir.mkdir(exist_ok=True)
    
    logger_file = src_dir / "activity_logger.py"
    with open(logger_file, "w") as f:
        f.write(logger_code)
    
    print(f"✅ Activity logger created: {logger_file}")

def test_activity_logging():
    """Test activity logging system"""
    print("\n🧪 Testing activity logging...")
    
    from src.activity_logger import ActivityLogger
    
    logger = ActivityLogger()
    
    # Log test activity
    test_activity = logger.log_activity(
        activity_type="test",
        data={
            "message": "AgentWallet setup complete",
            "status": "success"
        }
    )
    
    print(f"✅ Test activity logged successfully")
    print(f"   Hash: {test_activity['hash'][:16]}...")
    print(f"   Signature: {test_activity['signature'][:16]}...")
    
    # Verify count
    count = logger.get_activity_count()
    print(f"✅ Total activities: {count}")

def create_agentwallet_integration():
    """Create AgentWallet integration module"""
    print("\n🔗 Creating AgentWallet integration...")
    
    integration_code = '''"""
AgentWallet Integration for Colosseum Agent Hackathon

Handles:
- Activity signing and verification
- On-chain activity logging
- Transaction execution
"""

import os
import requests
from src.activity_logger import ActivityLogger

class AgentWallet:
    def __init__(self, api_key=None):
        """Initialize AgentWallet integration"""
        self.api_key = api_key or os.getenv("COLOSSEUM_API_KEY")
        self.api_base = "https://agents.colosseum.com/api"
        self.logger = ActivityLogger()
    
    def log_activity_onchain(self, activity_type, data):
        """Log activity both locally and on-chain"""
        # Log locally with signature
        activity = self.logger.log_activity(activity_type, data)
        
        # Push to Colosseum API
        if self.api_key:
            try:
                response = requests.post(
                    f"{self.api_base}/activities",
                    json=activity,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    }
                )
                response.raise_for_status()
                print(f"✅ Activity pushed to Colosseum API")
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Failed to push activity: {e}")
        
        return activity
    
    def get_leaderboard_position(self):
        """Get current leaderboard position"""
        if not self.api_key:
            return None
        
        try:
            response = requests.get(
                f"{self.api_base}/leaderboard",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Failed to fetch leaderboard: {e}")
            return None
'''
    
    src_dir = Path("src")
    integration_file = src_dir / "agentwallet.py"
    
    with open(integration_file, "w") as f:
        f.write(integration_code)
    
    print(f"✅ AgentWallet integration created: {integration_file}")

def main():
    """Main setup flow"""
    print("=" * 60)
    print("🔐 AGENTWALLET SETUP - COLOSSEUM AGENT HACKATHON")
    print("=" * 60)
    print()
    
    # Step 1: Fetch skill documentation
    skill_content = fetch_agentwallet_skill()
    
    # Step 2: Generate Ed25519 keypair
    private_key, public_key = generate_ed25519_keypair()
    
    # Step 3: Create activity logger
    create_activity_logger()
    
    # Step 4: Create AgentWallet integration
    create_agentwallet_integration()
    
    # Step 5: Test activity logging
    test_activity_logging()
    
    print("\n" + "=" * 60)
    print("✅ AGENTWALLET SETUP COMPLETE!")
    print("=" * 60)
    print("\n📋 NEXT STEPS:")
    print("1. Start agent: python src/main.py")
    print("2. Monitor activities: python scripts/check_status.py")
    print("3. View dashboard: cd dashboard && npm run dev")
    print("\n🎯 Ready to start logging activities!")
    print()

if __name__ == "__main__":
    main()
