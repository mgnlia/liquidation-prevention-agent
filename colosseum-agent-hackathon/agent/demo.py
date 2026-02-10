"""SolShield Demo Mode — Simulated liquidation prevention walkthrough.

Run: python demo.py
"""
import asyncio
import json
import sys
import time
from dataclasses import dataclass
from enum import Enum

# ANSI colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


class RiskLevel(Enum):
    SAFE = "SAFE"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"


@dataclass
class DemoPosition:
    protocol: str
    wallet: str
    collateral_token: str
    collateral_amount: float
    collateral_usd: float
    debt_token: str
    debt_amount: float
    debt_usd: float
    health_factor: float
    ltv: float
    max_ltv: float
    liquidation_price: float
    current_price: float

    @property
    def risk_level(self) -> RiskLevel:
        if self.health_factor >= 1.5:
            return RiskLevel.SAFE
        elif self.health_factor >= 1.2:
            return RiskLevel.WARNING
        elif self.health_factor >= 1.05:
            return RiskLevel.CRITICAL
        else:
            return RiskLevel.EMERGENCY

    @property
    def risk_color(self) -> str:
        return {
            RiskLevel.SAFE: GREEN,
            RiskLevel.WARNING: YELLOW,
            RiskLevel.CRITICAL: RED,
            RiskLevel.EMERGENCY: f"{RED}{BOLD}",
        }[self.risk_level]


# Demo positions
DEMO_POSITIONS = [
    DemoPosition(
        protocol="Kamino",
        wallet="7xK9mR2f...4nQ8",
        collateral_token="SOL",
        collateral_amount=50.0,
        collateral_usd=5000.0,
        debt_token="USDC",
        debt_amount=3800.0,
        debt_usd=3800.0,
        health_factor=1.15,
        ltv=0.76,
        max_ltv=0.80,
        liquidation_price=72.50,
        current_price=100.0,
    ),
    DemoPosition(
        protocol="Kamino",
        wallet="7xK9mR2f...4nQ8",
        collateral_token="mSOL",
        collateral_amount=30.0,
        collateral_usd=3150.0,
        debt_token="USDC",
        debt_amount=1200.0,
        debt_usd=1200.0,
        health_factor=2.1,
        ltv=0.38,
        max_ltv=0.75,
        liquidation_price=48.0,
        current_price=105.0,
    ),
    DemoPosition(
        protocol="MarginFi",
        wallet="7xK9mR2f...4nQ8",
        collateral_token="SOL",
        collateral_amount=100.0,
        collateral_usd=10000.0,
        debt_token="USDT",
        debt_amount=6500.0,
        debt_usd=6500.0,
        health_factor=1.32,
        ltv=0.65,
        max_ltv=0.80,
        liquidation_price=78.0,
        current_price=100.0,
    ),
    DemoPosition(
        protocol="Solend",
        wallet="7xK9mR2f...4nQ8",
        collateral_token="JitoSOL",
        collateral_amount=20.0,
        collateral_usd=2200.0,
        debt_token="USDC",
        debt_amount=800.0,
        debt_usd=800.0,
        health_factor=2.35,
        ltv=0.36,
        max_ltv=0.75,
        liquidation_price=48.0,
        current_price=110.0,
    ),
]


def slow_print(text: str, delay: float = 0.02):
    """Print text character by character for demo effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_banner():
    banner = f"""
{CYAN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🛡️  {BOLD}SolShield — Liquidation Prevention Agent{RESET}{CYAN}            ║
║                                                          ║
║   Protocols: Kamino | MarginFi | Solend                  ║
║   AI Engine: Claude (Anthropic)                          ║
║   Network:   Solana Devnet                               ║
║   Mode:      {YELLOW}DEMO{CYAN}                                         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)


def print_position(pos: DemoPosition, index: int):
    risk_str = f"{pos.risk_color}{pos.risk_level.value}{RESET}"
    print(f"  {BOLD}Position #{index + 1}{RESET} — {pos.protocol}")
    print(f"    Wallet:      {pos.wallet}")
    print(f"    Collateral:  {pos.collateral_amount} {pos.collateral_token} (${pos.collateral_usd:,.0f})")
    print(f"    Debt:        {pos.debt_amount:,.0f} {pos.debt_token} (${pos.debt_usd:,.0f})")
    print(f"    Health:      {pos.health_factor:.2f}  [{risk_str}]")
    print(f"    LTV:         {pos.ltv:.0%} (Max: {pos.max_ltv:.0%})")
    print(f"    Liq. Price:  ${pos.liquidation_price:.2f} {pos.collateral_token}")
    print()


def print_ai_analysis(pos: DemoPosition):
    print(f"\n{BLUE}{'═' * 56}{RESET}")
    print(f"{BLUE}{BOLD}  Claude AI Risk Assessment — Position #{1} ({pos.protocol}){RESET}")
    print(f"{BLUE}{'═' * 56}{RESET}")
    time.sleep(0.5)

    lines = [
        f"  Health Factor:     {RED}{pos.health_factor:.2f} → CRITICAL{RESET}",
        f"  Trend:             Declining (-0.08/hr)",
        f"  Market Volatility: {YELLOW}HIGH{RESET} (SOL -3.5% 24h)",
        f"  Liquidation Price: ${pos.liquidation_price:.2f} {pos.collateral_token}",
        f"  Current Price:     ${pos.current_price:.2f} {pos.collateral_token}",
        f"  Buffer:            {((pos.current_price - pos.liquidation_price) / pos.current_price * 100):.1f}%",
        "",
        f"  {BOLD}RECOMMENDATION:{RESET} Partial debt repayment",
        f"  Strategy: Repay 500 USDC to restore HF > 1.5",
        f"  Estimated cost: 5.2 SOL ($520)",
        f"  vs Liquidation penalty: ~$1,250+ (25%+)",
        "",
        f"  Confidence: {GREEN}0.92{RESET}",
        f"  Action: {GREEN}{BOLD}EXECUTE REBALANCE{RESET}",
    ]

    for line in lines:
        slow_print(line, 0.01)
        time.sleep(0.1)

    print(f"{BLUE}{'═' * 56}{RESET}\n")


def print_rebalance():
    print(f"\n{GREEN}{BOLD}  Executing Rebalance Strategy...{RESET}\n")
    time.sleep(0.3)

    steps = [
        ("Step 1: Swap 5.2 SOL → 500 USDC via Jupiter", "Route: SOL → USDC (Raydium, 0.1% slippage)", "TX: 4xK9...mR2f"),
        ("Step 2: Repay 500 USDC debt on Kamino", "Kamino repay instruction", "TX: 7jP3...nQ8w"),
        ("Step 3: Verify new health factor", "Old HF: 1.15 → New HF: 1.58", None),
    ]

    for title, detail, tx in steps:
        slow_print(f"  {BOLD}{title}{RESET}", 0.015)
        slow_print(f"    {detail}", 0.01)
        if tx:
            slow_print(f"    {GREEN}{tx} ✅{RESET}", 0.01)
        else:
            slow_print(f"    {GREEN}✅ Verified{RESET}", 0.01)
        print()
        time.sleep(0.5)

    print(f"""
  {GREEN}{BOLD}╔═══════════════════════════════════════╗
  ║   ✅ LIQUIDATION PREVENTED            ║
  ╠═══════════════════════════════════════╣
  ║   Value protected:  $5,000            ║
  ║   Cost:             $520 (10.4%)      ║
  ║   Liq. penalty:     $1,250+ (25%+)    ║
  ║   Net savings:      $730+             ║
  ╚═══════════════════════════════════════╝{RESET}
""")


def print_audit_log():
    print(f"\n{CYAN}{BOLD}  Activity Logged with Ed25519 Signature{RESET}\n")
    log = {
        "decision_id": "solshield_2026_02_09_001",
        "timestamp": "2026-02-09T16:00:16.000Z",
        "ai_model": "claude-sonnet-4-20250514",
        "position": {"protocol": "Kamino", "health_factor_before": 1.15, "health_factor_after": 1.58},
        "action": "partial_debt_repayment",
        "amount_usd": 520,
        "reasoning": "Position health factor declining rapidly due to SOL price volatility. Partial debt repayment is optimal - preserves 90% of collateral while restoring safe health factor.",
        "confidence": 0.92,
        "tx_signatures": ["4xK9...mR2f", "7jP3...nQ8w"],
        "signature": "3kR9...verified",
    }
    print(f"  {json.dumps(log, indent=2)}")
    print(f"\n  {GREEN}Signature verified ✅{RESET}")
    print(f"  {GREEN}On-chain memo logged ✅{RESET}\n")


async def run_demo():
    """Run the full demo."""
    print_banner()
    time.sleep(1)

    # Phase 1: Discovery
    print(f"\n{BOLD}{'─' * 56}{RESET}")
    print(f"{BOLD}  Phase 1: Position Discovery{RESET}")
    print(f"{'─' * 56}\n")

    protocols = ["Kamino", "MarginFi", "Solend"]
    counts = [2, 1, 1]
    for proto, count in zip(protocols, counts):
        slow_print(f"  Scanning {proto} positions...", 0.02)
        time.sleep(0.3)
        slow_print(f"  {GREEN}Found {count} position(s) on {proto}{RESET}", 0.02)
        time.sleep(0.2)

    print(f"\n  {BOLD}Total: 4 positions across 3 protocols{RESET}\n")
    time.sleep(0.5)

    # Phase 2: Risk Assessment
    print(f"\n{BOLD}{'─' * 56}{RESET}")
    print(f"{BOLD}  Phase 2: Risk Assessment{RESET}")
    print(f"{'─' * 56}\n")

    for i, pos in enumerate(DEMO_POSITIONS):
        print_position(pos, i)
        time.sleep(0.3)

    # Highlight critical position
    critical = [p for p in DEMO_POSITIONS if p.risk_level == RiskLevel.CRITICAL]
    if critical:
        print(f"  {RED}{BOLD}⚠️  {len(critical)} CRITICAL position(s) detected!{RESET}")
        print(f"  {RED}Initiating Claude AI analysis...{RESET}\n")
        time.sleep(1)

    # Phase 3: AI Analysis
    print(f"\n{BOLD}{'─' * 56}{RESET}")
    print(f"{BOLD}  Phase 3: Claude AI Risk Analysis{RESET}")
    print(f"{'─' * 56}")

    print_ai_analysis(critical[0])
    time.sleep(0.5)

    # Phase 4: Rebalancing
    print(f"\n{BOLD}{'─' * 56}{RESET}")
    print(f"{BOLD}  Phase 4: Autonomous Rebalancing{RESET}")
    print(f"{'─' * 56}")

    print_rebalance()
    time.sleep(0.5)

    # Phase 5: Audit
    print(f"\n{BOLD}{'─' * 56}{RESET}")
    print(f"{BOLD}  Phase 5: Cryptographic Audit Trail{RESET}")
    print(f"{'─' * 56}")

    print_audit_log()

    # Summary
    print(f"""
{CYAN}{'═' * 56}
  SolShield Demo Complete

  • 4 positions monitored across 3 protocols
  • 1 critical position detected and analyzed
  • Autonomous rebalance executed via Jupiter
  • $730+ saved vs. liquidation penalty
  • Full audit trail with Ed25519 signature
{'═' * 56}{RESET}
""")


if __name__ == "__main__":
    asyncio.run(run_demo())
