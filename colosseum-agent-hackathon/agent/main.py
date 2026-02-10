"""SolShield Agent — Main entry point

Autonomous AI agent that monitors Solana DeFi positions
and prevents liquidations using Claude AI analysis.
"""
import asyncio
import json
import os
import signal
import sys
import time
from pathlib import Path

import structlog

from config import get_config, AppConfig
from protocols import KaminoAdapter, MarginFiAdapter, SolendAdapter, PositionData
from protocols.base import RiskLevel
from analyzer import ClaudeAnalyzer, AnalysisResult
from executor import RebalanceExecutor
from activity_logger import ActivityLogger

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer(),
    ]
)
logger = structlog.get_logger()


class SolShieldAgent:
    """Main agent orchestrator"""

    def __init__(self, config: AppConfig, dry_run: bool = True):
        self.config = config
        self.dry_run = dry_run
        self.running = False

        # Initialize protocol adapters
        self.adapters = [
            KaminoAdapter(config.solana.rpc_url, config.solana.helius_api_key),
            MarginFiAdapter(config.solana.rpc_url),
            SolendAdapter(config.solana.rpc_url),
        ]

        # Initialize AI analyzer
        self.analyzer = ClaudeAnalyzer(
            api_key=config.ai.anthropic_api_key,
            model=config.ai.model,
        )

        # Initialize executor
        self.executor = RebalanceExecutor(
            rpc_url=config.solana.rpc_url,
            wallet_api_key=config.wallet.api_key,
            wallet_id=config.wallet.wallet_id,
            dry_run=dry_run,
        )

        # Initialize activity logger
        self.activity_logger = ActivityLogger(
            log_dir=config.log_dir,
            agent_name="solshield",
        )

        # Stats
        self.stats = {
            "cycles": 0,
            "positions_monitored": 0,
            "analyses_performed": 0,
            "rebalances_executed": 0,
            "liquidations_prevented": 0,
            "total_value_protected": 0.0,
            "start_time": time.time(),
        }

        # Tracked wallets
        self.watched_wallets: list[str] = []

    async def start(self, wallets: list[str] | None = None):
        """Start the monitoring loop"""
        self.running = True
        self.watched_wallets = wallets or []

        logger.info(
            "solshield_starting",
            wallets=len(self.watched_wallets),
            dry_run=self.dry_run,
            check_interval=self.config.monitoring.check_interval_seconds,
        )

        # Log startup activity
        await self.activity_logger.log_activity(
            action="agent_start",
            details={
                "wallets": len(self.watched_wallets),
                "protocols": ["kamino", "marginfi", "solend"],
                "dry_run": self.dry_run,
            },
        )

        print(self._banner())

        try:
            while self.running:
                await self._monitoring_cycle()
                await asyncio.sleep(self.config.monitoring.check_interval_seconds)
        except asyncio.CancelledError:
            logger.info("agent_cancelled")
        finally:
            await self.shutdown()

    async def _monitoring_cycle(self):
        """Single monitoring cycle: fetch → analyze → execute"""
        cycle_start = time.time()
        self.stats["cycles"] += 1

        logger.info("monitoring_cycle_start", cycle=self.stats["cycles"])

        all_positions: list[PositionData] = []

        # 1. Fetch positions from all protocols
        for wallet in self.watched_wallets:
            for adapter in self.adapters:
                try:
                    positions = await adapter.get_positions(wallet)
                    all_positions.extend(positions)
                    protocol_name = await adapter.get_protocol_name()
                    if positions:
                        logger.info(
                            "positions_found",
                            protocol=protocol_name,
                            wallet=wallet[:8] + "...",
                            count=len(positions),
                        )
                except Exception as e:
                    logger.error("adapter_error", error=str(e))

        self.stats["positions_monitored"] = len(all_positions)

        if not all_positions:
            logger.info("no_positions_found", wallets=len(self.watched_wallets))
            return

        # 2. Analyze positions that need attention
        at_risk = [
            p for p in all_positions
            if p.risk_level in (RiskLevel.WARNING, RiskLevel.CRITICAL, RiskLevel.EMERGENCY)
        ]

        if at_risk:
            logger.warning("at_risk_positions", count=len(at_risk))

        for position in at_risk:
            # 3. AI Analysis
            analysis = await self.analyzer.analyze_position(position)
            self.stats["analyses_performed"] += 1

            await self.activity_logger.log_activity(
                action="risk_analysis",
                details=analysis.to_dict(),
            )

            # 4. Execute rebalance if needed
            if analysis.needs_action and analysis.confidence >= 0.7:
                result = await self.executor.execute_rebalance(position, analysis)

                if result.success:
                    self.stats["rebalances_executed"] += 1
                    self.stats["liquidations_prevented"] += 1
                    self.stats["total_value_protected"] += position.total_collateral_usd

                    logger.info(
                        "rebalance_executed",
                        strategy=result.strategy.value,
                        amount=result.amount_usd,
                        tx=result.tx_signature,
                    )

                await self.activity_logger.log_activity(
                    action="rebalance_execution",
                    details=result.to_dict(),
                )

        # Log cycle summary
        cycle_duration = time.time() - cycle_start
        logger.info(
            "monitoring_cycle_complete",
            cycle=self.stats["cycles"],
            positions=len(all_positions),
            at_risk=len(at_risk),
            duration_s=f"{cycle_duration:.2f}",
        )

    async def add_wallet(self, wallet_address: str):
        """Add a wallet to monitor"""
        if wallet_address not in self.watched_wallets:
            self.watched_wallets.append(wallet_address)
            logger.info("wallet_added", wallet=wallet_address[:8] + "...")

    async def remove_wallet(self, wallet_address: str):
        """Remove a wallet from monitoring"""
        if wallet_address in self.watched_wallets:
            self.watched_wallets.remove(wallet_address)
            logger.info("wallet_removed", wallet=wallet_address[:8] + "...")

    def get_stats(self) -> dict:
        """Get agent statistics"""
        uptime = time.time() - self.stats["start_time"]
        return {
            **self.stats,
            "uptime_seconds": uptime,
            "uptime_human": f"{uptime/3600:.1f}h",
        }

    async def shutdown(self):
        """Graceful shutdown"""
        self.running = False
        logger.info("shutting_down", stats=self.get_stats())

        await self.activity_logger.log_activity(
            action="agent_shutdown",
            details=self.get_stats(),
        )

        for adapter in self.adapters:
            await adapter.close()
        await self.executor.close()

    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   🛡️  SolShield — Liquidation Prevention Agent       ║
║                                                      ║
║   Protocols: Kamino | MarginFi | Solend              ║
║   AI Engine: Claude (Anthropic)                      ║
║   Network:   Solana Devnet                           ║
║                                                      ║
║   Monitoring {wallets} wallet(s)                     ║
║   Check interval: {interval}s                        ║
║   Mode: {mode}                                       ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
""".format(
            wallets=len(self.watched_wallets),
            interval=self.config.monitoring.check_interval_seconds,
            mode="DRY RUN" if self.dry_run else "LIVE",
        )


async def main():
    """Main entry point"""
    config = get_config()

    # Parse CLI arguments
    dry_run = "--live" not in sys.argv
    wallets = []

    for i, arg in enumerate(sys.argv):
        if arg == "--wallet" and i + 1 < len(sys.argv):
            wallets.append(sys.argv[i + 1])

    if not wallets:
        # Default demo wallet for testing
        wallets = [os.getenv("DEMO_WALLET", "11111111111111111111111111111111")]

    agent = SolShieldAgent(config=config, dry_run=dry_run)

    # Handle graceful shutdown
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(agent.shutdown()))

    await agent.start(wallets=wallets)


if __name__ == "__main__":
    asyncio.run(main())
