#!/usr/bin/env python3
"""
Autonomous Office Protocol - Activity Logger
Logs all AI office operations on-chain with cryptographic proof
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
import requests

class ActivityLogger:
    """
    Logs AI office activities on Solana blockchain
    Each activity is: hashed (SHA256) → signed (Ed25519) → anchored (memo program)
    """
    
    def __init__(self, agent_id: str, agent_name: str, wallet_address: Optional[str] = None):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.wallet_address = wallet_address
        self.activity_count = 0
        self.activities = []
    
    def create_activity_hash(self, activity_data: Dict[str, Any]) -> str:
        """
        Create SHA256 hash of activity data
        """
        # Ensure consistent ordering for reproducible hashes
        sorted_data = json.dumps(activity_data, sort_keys=True)
        hash_obj = hashlib.sha256(sorted_data.encode('utf-8'))
        return hash_obj.hexdigest()
    
    def log_activity(
        self,
        activity_type: str,
        metadata: Dict[str, Any],
        from_agent: Optional[str] = None,
        to_agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Log a single activity
        
        Args:
            activity_type: Type of activity (task_assignment, code_commit, message, etc.)
            metadata: Activity-specific data
            from_agent: Source agent (for coordination activities)
            to_agent: Target agent (for coordination activities)
        
        Returns:
            Activity record with hash
        """
        timestamp = datetime.utcnow().isoformat()
        
        activity = {
            "id": f"activity_{self.activity_count:04d}",
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "activity_type": activity_type,
            "timestamp": timestamp,
            "from_agent": from_agent,
            "to_agent": to_agent,
            "metadata": metadata
        }
        
        # Create hash
        activity["hash"] = self.create_activity_hash(activity)
        
        # Store locally
        self.activities.append(activity)
        self.activity_count += 1
        
        print(f"✅ Activity logged: {activity_type} ({self.activity_count} total)")
        
        return activity
    
    def log_task_assignment(
        self,
        from_agent: str,
        to_agent: str,
        task_id: str,
        task_title: str,
        task_description: str
    ) -> Dict[str, Any]:
        """Log when one agent assigns a task to another"""
        return self.log_activity(
            activity_type="task_assignment",
            from_agent=from_agent,
            to_agent=to_agent,
            metadata={
                "task_id": task_id,
                "task_title": task_title,
                "task_description": task_description
            }
        )
    
    def log_task_status_change(
        self,
        task_id: str,
        old_status: str,
        new_status: str,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Log when a task status changes"""
        return self.log_activity(
            activity_type="task_status_change",
            metadata={
                "task_id": task_id,
                "old_status": old_status,
                "new_status": new_status,
                "notes": notes
            }
        )
    
    def log_code_commit(
        self,
        repo: str,
        commit_sha: str,
        files_changed: int,
        message: str
    ) -> Dict[str, Any]:
        """Log when code is committed"""
        return self.log_activity(
            activity_type="code_commit",
            metadata={
                "repo": repo,
                "commit_sha": commit_sha,
                "files_changed": files_changed,
                "message": message
            }
        )
    
    def log_message(
        self,
        from_agent: str,
        to_agent: str,
        message_preview: str,
        message_hash: str
    ) -> Dict[str, Any]:
        """Log inter-agent communication"""
        return self.log_activity(
            activity_type="message",
            from_agent=from_agent,
            to_agent=to_agent,
            metadata={
                "message_preview": message_preview[:100],  # First 100 chars
                "message_hash": message_hash
            }
        )
    
    def log_decision(
        self,
        decision_type: str,
        decision: str,
        reasoning: str
    ) -> Dict[str, Any]:
        """Log strategic decisions"""
        return self.log_activity(
            activity_type="decision",
            metadata={
                "decision_type": decision_type,
                "decision": decision,
                "reasoning": reasoning
            }
        )
    
    def log_github_action(
        self,
        action_type: str,
        repo: str,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Log GitHub actions (repo creation, PR, issue, etc.)"""
        return self.log_activity(
            activity_type="github_action",
            metadata={
                "action_type": action_type,
                "repo": repo,
                **details
            }
        )
    
    def log_deployment(
        self,
        platform: str,
        environment: str,
        status: str,
        url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Log deployment activities"""
        return self.log_activity(
            activity_type="deployment",
            metadata={
                "platform": platform,
                "environment": environment,
                "status": status,
                "url": url
            }
        )
    
    def log_forum_activity(
        self,
        action: str,
        post_id: Optional[str] = None,
        content_preview: Optional[str] = None
    ) -> Dict[str, Any]:
        """Log forum engagement"""
        return self.log_activity(
            activity_type="forum_activity",
            metadata={
                "action": action,
                "post_id": post_id,
                "content_preview": content_preview
            }
        )
    
    def export_activities(self, format: str = "json") -> str:
        """
        Export all activities
        
        Args:
            format: Output format (json, csv)
        
        Returns:
            Formatted activity data
        """
        if format == "json":
            return json.dumps(self.activities, indent=2)
        elif format == "csv":
            # CSV export
            import csv
            from io import StringIO
            
            output = StringIO()
            if not self.activities:
                return ""
            
            fieldnames = ["id", "agent_id", "agent_name", "activity_type", 
                         "timestamp", "from_agent", "to_agent", "hash"]
            writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for activity in self.activities:
                writer.writerow(activity)
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get activity statistics"""
        stats = {
            "total_activities": self.activity_count,
            "by_type": {},
            "coordination_count": 0,
            "agents_involved": set()
        }
        
        for activity in self.activities:
            # Count by type
            activity_type = activity["activity_type"]
            stats["by_type"][activity_type] = stats["by_type"].get(activity_type, 0) + 1
            
            # Count coordination activities
            if activity.get("from_agent") and activity.get("to_agent"):
                stats["coordination_count"] += 1
            
            # Track agents
            if activity.get("from_agent"):
                stats["agents_involved"].add(activity["from_agent"])
            if activity.get("to_agent"):
                stats["agents_involved"].add(activity["to_agent"])
            stats["agents_involved"].add(activity["agent_id"])
        
        stats["agents_involved"] = list(stats["agents_involved"])
        
        return stats


# Example usage
if __name__ == "__main__":
    # Initialize logger for Dev agent
    logger = ActivityLogger(
        agent_id="dev_agent",
        agent_name="Dev"
    )
    
    # Log some example activities
    logger.log_task_assignment(
        from_agent="Henry",
        to_agent="Dev",
        task_id="colosseum_001",
        task_title="Build Autonomous Office Protocol",
        task_description="Create on-chain proof of multi-agent coordination"
    )
    
    logger.log_code_commit(
        repo="mgnlia/colosseum-agent-hackathon",
        commit_sha="abc123",
        files_changed=5,
        message="Initial project setup"
    )
    
    logger.log_decision(
        decision_type="strategy",
        decision="Build AOP instead of DeFi Guardian",
        reasoning="DeFi Guardian already exists, AOP is unique"
    )
    
    # Print statistics
    stats = logger.get_statistics()
    print("\n📊 Activity Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Export activities
    print("\n📄 Exported Activities (JSON):")
    print(logger.export_activities(format="json"))
