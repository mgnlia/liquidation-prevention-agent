"use client";

import { getRiskLevel, getRiskColor } from "@/types";

export function HealthGauge({ value }: { value: number }) {
  const risk = getRiskLevel(value);
  const angle = Math.min(Math.max((value - 0.5) / 2.5, 0), 1) * 180;

  const strokeColor =
    risk === "healthy"
      ? "#22c55e"
      : risk === "warning"
      ? "#f59e0b"
      : risk === "critical"
      ? "#ef4444"
      : "#dc2626";

  return (
    <div className="flex flex-col items-center">
      <svg viewBox="0 0 200 120" className="w-48 h-28">
        {/* Background arc */}
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="rgba(255,255,255,0.1)"
          strokeWidth="12"
          strokeLinecap="round"
        />
        {/* Value arc */}
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke={strokeColor}
          strokeWidth="12"
          strokeLinecap="round"
          strokeDasharray={`${(angle / 180) * 251.3} 251.3`}
          className="transition-all duration-1000"
        />
        {/* Center text */}
        <text
          x="100"
          y="85"
          textAnchor="middle"
          className="fill-white text-3xl font-bold"
          style={{ fontSize: "28px" }}
        >
          {value.toFixed(2)}
        </text>
        <text
          x="100"
          y="105"
          textAnchor="middle"
          className="fill-gray-400"
          style={{ fontSize: "11px" }}
        >
          Avg Health Factor
        </text>
      </svg>

      <div className="flex items-center gap-2 mt-2">
        <div className={`w-2 h-2 rounded-full`} style={{ backgroundColor: strokeColor }} />
        <span className={`text-sm font-medium capitalize ${getRiskColor(risk)}`}>
          {risk}
        </span>
      </div>

      <div className="grid grid-cols-4 gap-2 w-full mt-4 text-center">
        {[
          { label: "EMG", threshold: "< 1.05", color: "text-red-600" },
          { label: "CRIT", threshold: "< 1.2", color: "text-red-400" },
          { label: "WARN", threshold: "< 1.5", color: "text-yellow-400" },
          { label: "SAFE", threshold: "≥ 1.5", color: "text-green-400" },
        ].map((t) => (
          <div key={t.label}>
            <p className={`text-[10px] font-bold ${t.color}`}>{t.label}</p>
            <p className="text-[9px] text-gray-500">{t.threshold}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
