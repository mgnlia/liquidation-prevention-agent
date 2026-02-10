import { Position, AgentStats, ActivityEntry } from "@/types";

export const MOCK_POSITIONS: Position[] = [
  {
    id: "pos-1",
    protocol: "kamino",
    owner: "7xK9mR2f4nQ8wZp3jL6vT9bY5cA1dE8gH0iK2mN4oP6",
    obligationKey: "KAM-OBL-001",
    healthFactor: 1.15,
    totalCollateralUsd: 5000,
    totalDebtUsd: 3800,
    netValueUsd: 1200,
    riskLevel: "critical",
    collaterals: [
      {
        symbol: "SOL",
        amount: 50,
        valueUsd: 5000,
        ltv: 0.76,
        liquidationThreshold: 0.85,
      },
    ],
    debts: [
      {
        symbol: "USDC",
        amount: 3800,
        valueUsd: 3800,
        borrowApy: 0.058,
      },
    ],
    lastUpdate: Date.now(),
  },
  {
    id: "pos-2",
    protocol: "kamino",
    owner: "7xK9mR2f4nQ8wZp3jL6vT9bY5cA1dE8gH0iK2mN4oP6",
    obligationKey: "KAM-OBL-002",
    healthFactor: 2.1,
    totalCollateralUsd: 3150,
    totalDebtUsd: 1200,
    netValueUsd: 1950,
    riskLevel: "healthy",
    collaterals: [
      {
        symbol: "mSOL",
        amount: 30,
        valueUsd: 3150,
        ltv: 0.38,
        liquidationThreshold: 0.8,
      },
    ],
    debts: [
      {
        symbol: "USDC",
        amount: 1200,
        valueUsd: 1200,
        borrowApy: 0.042,
      },
    ],
    lastUpdate: Date.now(),
  },
  {
    id: "pos-3",
    protocol: "marginfi",
    owner: "7xK9mR2f4nQ8wZp3jL6vT9bY5cA1dE8gH0iK2mN4oP6",
    obligationKey: "MFI-ACC-001",
    healthFactor: 1.32,
    totalCollateralUsd: 10000,
    totalDebtUsd: 6500,
    netValueUsd: 3500,
    riskLevel: "warning",
    collaterals: [
      {
        symbol: "SOL",
        amount: 100,
        valueUsd: 10000,
        ltv: 0.65,
        liquidationThreshold: 0.8,
      },
    ],
    debts: [
      {
        symbol: "USDT",
        amount: 6500,
        valueUsd: 6500,
        borrowApy: 0.072,
      },
    ],
    lastUpdate: Date.now(),
  },
  {
    id: "pos-4",
    protocol: "solend",
    owner: "7xK9mR2f4nQ8wZp3jL6vT9bY5cA1dE8gH0iK2mN4oP6",
    obligationKey: "SLD-OBL-001",
    healthFactor: 2.35,
    totalCollateralUsd: 2200,
    totalDebtUsd: 800,
    netValueUsd: 1400,
    riskLevel: "healthy",
    collaterals: [
      {
        symbol: "JitoSOL",
        amount: 20,
        valueUsd: 2200,
        ltv: 0.36,
        liquidationThreshold: 0.75,
      },
    ],
    debts: [
      {
        symbol: "USDC",
        amount: 800,
        valueUsd: 800,
        borrowApy: 0.035,
      },
    ],
    lastUpdate: Date.now(),
  },
];

export const MOCK_STATS: AgentStats = {
  totalPositions: 4,
  totalValueProtected: 20350,
  liquidationsPrevented: 3,
  rebalancesExecuted: 7,
  uptimeHours: 168,
  avgResponseTime: 2.4,
};

export const MOCK_ACTIVITY: ActivityEntry[] = [
  {
    id: "act-1",
    timestamp: Date.now() - 120000,
    action: "Rebalance Executed",
    details: "Repaid 500 USDC debt on Kamino — HF restored 1.08 → 1.52",
    txSignature: "4xK9mR2f...8gH0",
    riskLevel: "critical",
  },
  {
    id: "act-2",
    timestamp: Date.now() - 300000,
    action: "Risk Alert",
    details: "MarginFi position HF dropped to 1.32 — monitoring closely",
    riskLevel: "warning",
  },
  {
    id: "act-3",
    timestamp: Date.now() - 600000,
    action: "Position Scanned",
    details: "4 positions across 3 protocols — 2 healthy, 1 warning, 1 critical",
  },
  {
    id: "act-4",
    timestamp: Date.now() - 1800000,
    action: "Collateral Swap",
    details: "Swapped 10 SOL → mSOL on Kamino for better yield",
    txSignature: "7jP3nQ8w...2mN4",
    riskLevel: "healthy",
  },
  {
    id: "act-5",
    timestamp: Date.now() - 3600000,
    action: "Agent Started",
    details: "SolShield monitoring loop initiated — 4 wallets loaded",
  },
];
