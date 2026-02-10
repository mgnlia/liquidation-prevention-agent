"use client";

import { useState, useEffect } from "react";
import { useWallet } from "@solana/wallet-adapter-react";
import { WalletMultiButton } from "@solana/wallet-adapter-react-ui";
import { Header } from "@/components/Header";
import { PositionCard } from "@/components/PositionCard";
import { AgentStatus } from "@/components/AgentStatus";
import { ActivityFeed } from "@/components/ActivityFeed";
import { HealthGauge } from "@/components/HealthGauge";
import { StatsPanel } from "@/components/StatsPanel";
import { Position, AgentStats, ActivityEntry } from "@/types";
import { MOCK_POSITIONS, MOCK_STATS, MOCK_ACTIVITY } from "@/lib/mock-data";

export default function Dashboard() {
  const { connected, publicKey } = useWallet();
  const [positions, setPositions] = useState<Position[]>(MOCK_POSITIONS);
  const [stats, setStats] = useState<AgentStats>(MOCK_STATS);
  const [activity, setActivity] = useState<ActivityEntry[]>(MOCK_ACTIVITY);
  const [agentRunning, setAgentRunning] = useState(true);

  // Simulate real-time health factor updates
  useEffect(() => {
    const interval = setInterval(() => {
      setPositions((prev) =>
        prev.map((p) => ({
          ...p,
          healthFactor: p.healthFactor + (Math.random() - 0.52) * 0.05,
          lastUpdate: Date.now(),
        }))
      );
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-shield-400 to-shield-600 bg-clip-text text-transparent">
                SolShield Dashboard
              </h1>
              <p className="text-gray-400 mt-1">
                AI-powered liquidation prevention for your Solana DeFi positions
              </p>
            </div>
            <div className="flex items-center gap-4">
              <AgentStatus running={agentRunning} onToggle={() => setAgentRunning(!agentRunning)} />
              <WalletMultiButton className="!bg-shield-600 hover:!bg-shield-700 !rounded-lg" />
            </div>
          </div>
        </div>

        {/* Stats Overview */}
        <StatsPanel stats={stats} />

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
          {/* Positions Column */}
          <div className="lg:col-span-2 space-y-4">
            <h2 className="text-xl font-semibold text-white flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-shield-500 animate-pulse" />
              Monitored Positions
            </h2>
            {positions.map((position) => (
              <PositionCard key={position.id} position={position} />
            ))}
            {positions.length === 0 && (
              <div className="glass p-12 text-center">
                <p className="text-gray-400">No positions found. Connect your wallet to start monitoring.</p>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Health Overview */}
            <div className="glass p-6">
              <h3 className="text-lg font-semibold mb-4">Portfolio Health</h3>
              <HealthGauge
                value={
                  positions.length > 0
                    ? positions.reduce((sum, p) => sum + p.healthFactor, 0) / positions.length
                    : 0
                }
              />
            </div>

            {/* Activity Feed */}
            <div className="glass p-6">
              <h3 className="text-lg font-semibold mb-4">Agent Activity</h3>
              <ActivityFeed entries={activity} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
