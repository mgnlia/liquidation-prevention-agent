"""Tests for the Activity Logger — hash chain integrity"""
import pytest
import asyncio
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from activity_logger import ActivityLogger, ActivityEntry


class TestActivityLogger:
    """Test the cryptographic activity logger"""

    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.logger = ActivityLogger(log_dir=self.tmpdir, agent_name="test")

    @pytest.mark.asyncio
    async def test_log_single_entry(self):
        entry = await self.logger.log_activity(
            action="test_action",
            details={"key": "value"},
        )
        assert entry.action == "test_action"
        assert entry.sequence == 0
        assert entry.previous_hash == "genesis"
        assert len(entry.entry_hash) == 64

    @pytest.mark.asyncio
    async def test_hash_chain_integrity(self):
        await self.logger.log_activity("action_1", {"step": 1})
        await self.logger.log_activity("action_2", {"step": 2})
        await self.logger.log_activity("action_3", {"step": 3})

        is_valid, count = await self.logger.verify_integrity()
        assert is_valid
        assert count == 3

    @pytest.mark.asyncio
    async def test_chain_links(self):
        e1 = await self.logger.log_activity("first", {})
        e2 = await self.logger.log_activity("second", {})
        e3 = await self.logger.log_activity("third", {})

        assert e2.previous_hash == e1.entry_hash
        assert e3.previous_hash == e2.entry_hash

    @pytest.mark.asyncio
    async def test_sequence_increments(self):
        e1 = await self.logger.log_activity("a", {})
        e2 = await self.logger.log_activity("b", {})
        e3 = await self.logger.log_activity("c", {})

        assert e1.sequence == 0
        assert e2.sequence == 1
        assert e3.sequence == 2

    @pytest.mark.asyncio
    async def test_summary(self):
        await self.logger.log_activity("scan", {"positions": 4})
        await self.logger.log_activity("analyze", {"risk": "critical"})
        await self.logger.log_activity("rebalance", {"amount": 500})
        await self.logger.log_activity("scan", {"positions": 4})

        summary = await self.logger.get_summary()
        assert summary["total_entries"] == 4
        assert summary["integrity_valid"]
        assert summary["actions"]["scan"] == 2
        assert summary["actions"]["analyze"] == 1


class TestActivityEntry:
    """Test the ActivityEntry model"""

    def test_compute_hash_deterministic(self):
        entry = ActivityEntry(
            timestamp=1234567890.0,
            action="test",
            details={"key": "value"},
            previous_hash="genesis",
            sequence=0,
        )
        hash1 = entry.compute_hash()
        hash2 = entry.compute_hash()
        assert hash1 == hash2

    def test_different_data_different_hash(self):
        e1 = ActivityEntry(timestamp=1.0, action="a", details={}, previous_hash="x", sequence=0)
        e2 = ActivityEntry(timestamp=2.0, action="a", details={}, previous_hash="x", sequence=0)
        assert e1.compute_hash() != e2.compute_hash()

    def test_to_dict(self):
        entry = ActivityEntry(
            timestamp=1234567890.0,
            action="test",
            details={"k": "v"},
            entry_hash="abc123",
            previous_hash="genesis",
            sequence=0,
        )
        d = entry.to_dict()
        assert d["action"] == "test"
        assert d["entry_hash"] == "abc123"
        assert d["sequence"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
