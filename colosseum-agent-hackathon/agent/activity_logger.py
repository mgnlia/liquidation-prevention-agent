"""Activity Logger — Cryptographically verified audit trail"""
import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import structlog

logger = structlog.get_logger()


@dataclass
class ActivityEntry:
    """Single activity log entry"""
    timestamp: float
    action: str
    details: dict
    entry_hash: str = ""
    previous_hash: str = ""
    sequence: int = 0

    def compute_hash(self) -> str:
        """Compute SHA-256 hash of this entry"""
        data = json.dumps({
            "timestamp": self.timestamp,
            "action": self.action,
            "details": self.details,
            "previous_hash": self.previous_hash,
            "sequence": self.sequence,
        }, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "action": self.action,
            "details": self.details,
            "entry_hash": self.entry_hash,
            "previous_hash": self.previous_hash,
            "sequence": self.sequence,
        }


class ActivityLogger:
    """
    Append-only activity log with hash chain for integrity verification.
    
    Each entry includes a SHA-256 hash of its contents plus the previous
    entry's hash, creating a tamper-evident chain similar to a blockchain.
    """

    def __init__(self, log_dir: str = "agent/logs", agent_name: str = "solshield"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.agent_name = agent_name
        self.sequence = 0
        self.last_hash = "genesis"
        self.entries: list[ActivityEntry] = []

        # Load existing log if present
        self._load_existing()

    def _load_existing(self):
        """Load existing log entries to continue the hash chain"""
        log_file = self.log_dir / f"{self.agent_name}_activity.jsonl"
        if log_file.exists():
            try:
                with open(log_file, "r") as f:
                    for line in f:
                        entry_data = json.loads(line.strip())
                        self.sequence = entry_data.get("sequence", 0) + 1
                        self.last_hash = entry_data.get("entry_hash", "genesis")
            except Exception as e:
                logger.warning("log_load_error", error=str(e))

    async def log_activity(
        self,
        action: str,
        details: dict,
        timestamp: Optional[float] = None,
    ) -> ActivityEntry:
        """Log an activity with hash chain integrity"""

        entry = ActivityEntry(
            timestamp=timestamp or time.time(),
            action=action,
            details=details,
            previous_hash=self.last_hash,
            sequence=self.sequence,
        )
        entry.entry_hash = entry.compute_hash()

        # Update chain
        self.last_hash = entry.entry_hash
        self.sequence += 1
        self.entries.append(entry)

        # Persist to disk
        await self._persist_entry(entry)

        logger.debug(
            "activity_logged",
            action=action,
            sequence=entry.sequence,
            hash=entry.entry_hash[:16],
        )

        return entry

    async def _persist_entry(self, entry: ActivityEntry):
        """Append entry to JSONL log file"""
        log_file = self.log_dir / f"{self.agent_name}_activity.jsonl"
        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(entry.to_dict()) + "\n")
        except Exception as e:
            logger.error("log_persist_error", error=str(e))

    async def verify_integrity(self) -> tuple[bool, int]:
        """
        Verify the hash chain integrity of the activity log.
        Returns (is_valid, num_entries_verified).
        """
        log_file = self.log_dir / f"{self.agent_name}_activity.jsonl"
        if not log_file.exists():
            return True, 0

        previous_hash = "genesis"
        count = 0

        with open(log_file, "r") as f:
            for line in f:
                entry_data = json.loads(line.strip())
                entry = ActivityEntry(
                    timestamp=entry_data["timestamp"],
                    action=entry_data["action"],
                    details=entry_data["details"],
                    previous_hash=entry_data["previous_hash"],
                    sequence=entry_data["sequence"],
                )

                # Verify previous hash chain
                if entry.previous_hash != previous_hash:
                    logger.error(
                        "integrity_violation",
                        sequence=entry.sequence,
                        expected=previous_hash,
                        got=entry.previous_hash,
                    )
                    return False, count

                # Verify entry hash
                computed = entry.compute_hash()
                if computed != entry_data["entry_hash"]:
                    logger.error(
                        "hash_mismatch",
                        sequence=entry.sequence,
                        expected=entry_data["entry_hash"],
                        computed=computed,
                    )
                    return False, count

                previous_hash = entry_data["entry_hash"]
                count += 1

        return True, count

    async def get_summary(self) -> dict:
        """Get a summary of all logged activities"""
        actions = {}
        for entry in self.entries:
            actions[entry.action] = actions.get(entry.action, 0) + 1

        is_valid, count = await self.verify_integrity()

        return {
            "total_entries": self.sequence,
            "actions": actions,
            "integrity_valid": is_valid,
            "entries_verified": count,
            "last_hash": self.last_hash,
        }
