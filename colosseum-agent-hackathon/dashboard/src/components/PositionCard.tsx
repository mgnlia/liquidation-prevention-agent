"use client";

import { Position, getRiskLevel, getRiskColor, getRiskBgColor } from "@/types";
import { AlertTriangle, TrendingDown, TrendingUp, Shield } from "lucide-react";

const PROTOCOL_LABELS: Record<string, string> = {
  kamino: "Kamino",
  marginfi: "MarginFi",
  solend: "Solend",
};

const PROTOCOL_COLORS: Record<string, string> = {
  kamino: "text-purple-400",
  marginfi: "text-blue-400",
  solend: "text-orange-400",
};

function HealthBar({ value }: { value: number }) {
  const pct = Math.min(Math.max((value - 1) / 2, 0), 1) * 100;
  const risk = getRiskLevel(value);
  const barColor =
    risk === "healthy"
      ? "bg-green-500"
      : risk === "warning"
      ? "bg-yellow-500"
      : risk === "critical"
      ? "bg-red-500"
      : "bg-red-700 animate-pulse";

  return (
    <div className="w-full">
      <div className="flex justify-between text-xs mb-1">
        <span className="text-gray-400">Health Factor</span>
        <span className={getRiskColor(risk) + " font-mono font-bold"}>
          {value.toFixed(2)}
        </span>
      </div>
      <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-1000 ${barColor}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <div className="flex justify-between text-[10px] text-gray-600 mt-0.5">
        <span>1.0 (Liquidation)</span>
        <span>3.0+</span>
      </div>
    </div>
  );
}

export function PositionCard({ position }: { position: Position }) {
  const risk = getRiskLevel(position.healthFactor);
  const borderClass = getRiskBgColor(risk);

  return (
    <div className={`glass p-5 border ${borderClass} transition-all duration-300`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div
            className={`w-10 h-10 rounded-lg flex items-center justify-center ${
              risk === "healthy"
                ? "bg-green-500/20"
                : risk === "warning"
                ? "bg-yellow-500/20"
                : "bg-red-500/20"
            }`}
          >
            {risk === "healthy" ? (
              <Shield className="w-5 h-5 text-green-400" />
            ) : risk === "warning" ? (
              <AlertTriangle className="w-5 h-5 text-yellow-400" />
            ) : (
              <AlertTriangle className="w-5 h-5 text-red-400 animate-pulse" />
            )}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className={`text-sm font-bold ${PROTOCOL_COLORS[position.protocol]}`}>
                {PROTOCOL_LABELS[position.protocol]}
              </span>
              <span
                className={`text-[10px] px-2 py-0.5 rounded-full font-medium uppercase tracking-wider ${borderClass}`}
              >
                {risk}
              </span>
            </div>
            <p className="text-xs text-gray-500 font-mono mt-0.5">
              {position.obligationKey}
            </p>
          </div>
        </div>

        <div className="text-right">
          <p className="text-lg font-bold text-white">
            ${position.netValueUsd.toLocaleString()}
          </p>
          <p className="text-xs text-gray-400">Net Value</p>
        </div>
      </div>

      <HealthBar value={position.healthFactor} />

      <div className="grid grid-cols-2 gap-4 mt-4">
        <div>
          <p className="text-xs text-gray-400 mb-1">Collateral</p>
          {position.collaterals.map((c, i) => (
            <div key={i} className="flex items-center gap-1.5">
              <TrendingUp className="w-3 h-3 text-green-400" />
              <span className="text-sm text-white font-medium">
                {c.amount} {c.symbol}
              </span>
              <span className="text-xs text-gray-500">
                (${c.valueUsd.toLocaleString()})
              </span>
            </div>
          ))}
        </div>
        <div>
          <p className="text-xs text-gray-400 mb-1">Debt</p>
          {position.debts.map((d, i) => (
            <div key={i} className="flex items-center gap-1.5">
              <TrendingDown className="w-3 h-3 text-red-400" />
              <span className="text-sm text-white font-medium">
                {d.amount.toLocaleString()} {d.symbol}
              </span>
              <span className="text-xs text-gray-500">
                ({(d.borrowApy * 100).toFixed(1)}% APY)
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="flex items-center justify-between mt-4 pt-3 border-t border-white/5">
        <span className="text-xs text-gray-500">
          LTV: {((position.totalDebtUsd / position.totalCollateralUsd) * 100).toFixed(1)}%
        </span>
        <span className="text-xs text-gray-500">
          Updated {Math.round((Date.now() - position.lastUpdate) / 1000)}s ago
        </span>
      </div>
    </div>
  );
}
