export type RiskLevel = "healthy" | "warning" | "critical" | "emergency";
export type Protocol = "kamino" | "marginfi" | "solend";

export interface CollateralAsset {
  symbol: string;
  amount: number;
  valueUsd: number;
  ltv: number;
  liquidationThreshold: number;
}

export interface DebtAsset {
  symbol: string;
  amount: number;
  valueUsd: number;
  borrowApy: number;
}

export interface Position {
  id: string;
  protocol: Protocol;
  owner: string;
  obligationKey: string;
  healthFactor: number;
  totalCollateralUsd: number;
  totalDebtUsd: number;
  netValueUsd: number;
  riskLevel: RiskLevel;
  collaterals: CollateralAsset[];
  debts: DebtAsset[];
  lastUpdate: number;
}

export interface AgentStats {
  totalPositions: number;
  totalValueProtected: number;
  liquidationsPrevented: number;
  rebalancesExecuted: number;
  uptimeHours: number;
  avgResponseTime: number;
}

export interface ActivityEntry {
  id: string;
  timestamp: number;
  action: string;
  details: string;
  txSignature?: string;
  riskLevel?: RiskLevel;
}

export function getRiskLevel(healthFactor: number): RiskLevel {
  if (healthFactor < 1.05) return "emergency";
  if (healthFactor < 1.2) return "critical";
  if (healthFactor < 1.5) return "warning";
  return "healthy";
}

export function getRiskColor(risk: RiskLevel): string {
  switch (risk) {
    case "healthy":
      return "text-green-400";
    case "warning":
      return "text-yellow-400";
    case "critical":
      return "text-red-400";
    case "emergency":
      return "text-red-600";
  }
}

export function getRiskBgColor(risk: RiskLevel): string {
  switch (risk) {
    case "healthy":
      return "bg-green-500/20 border-green-500/30";
    case "warning":
      return "bg-yellow-500/20 border-yellow-500/30";
    case "critical":
      return "bg-red-500/20 border-red-500/30";
    case "emergency":
      return "bg-red-700/30 border-red-600/50";
  }
}
