"use client";

import { AgentStats } from "@/types";
import { Shield, Zap, Clock, DollarSign, Activity, BarChart3 } from "lucide-react";

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  subtext?: string;
  color: string;
}

function StatCard({ icon, label, value, subtext, color }: StatCardProps) {
  return (
    <div className="glass p-4 flex items-center gap-4">
      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${color}`}>
        {icon}
      </div>
      <div>
        <p className="text-xs text-gray-400">{label}</p>
        <p className="text-lg font-bold text-white">{value}</p>
        {subtext && <p className="text-[10px] text-gray-500">{subtext}</p>}
      </div>
    </div>
  );
}

export function StatsPanel({ stats }: { stats: AgentStats }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
      <StatCard
        icon={<BarChart3 className="w-5 h-5 text-blue-400" />}
        label="Positions"
        value={stats.totalPositions.toString()}
        subtext="Across 3 protocols"
        color="bg-blue-500/20"
      />
      <StatCard
        icon={<DollarSign className="w-5 h-5 text-green-400" />}
        label="Value Protected"
        value={`$${(stats.totalValueProtected / 1000).toFixed(1)}K`}
        subtext="Total collateral"
        color="bg-green-500/20"
      />
      <StatCard
        icon={<Shield className="w-5 h-5 text-shield-400" />}
        label="Liquidations Prevented"
        value={stats.liquidationsPrevented.toString()}
        subtext="Saved ~$3.7K"
        color="bg-shield-500/20"
      />
      <StatCard
        icon={<Zap className="w-5 h-5 text-yellow-400" />}
        label="Rebalances"
        value={stats.rebalancesExecuted.toString()}
        subtext="Auto-executed"
        color="bg-yellow-500/20"
      />
      <StatCard
        icon={<Clock className="w-5 h-5 text-purple-400" />}
        label="Uptime"
        value={`${stats.uptimeHours}h`}
        subtext="7 days"
        color="bg-purple-500/20"
      />
      <StatCard
        icon={<Activity className="w-5 h-5 text-cyan-400" />}
        label="Avg Response"
        value={`${stats.avgResponseTime}s`}
        subtext="Detection → action"
        color="bg-cyan-500/20"
      />
    </div>
  );
}
