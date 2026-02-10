'use client';

import { useEffect, useState } from 'react';

interface Activity {
  timestamp: string;
  activity_type: string;
  data: any;
  hash: string;
  signature: string;
}

export default function Dashboard() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [stats, setStats] = useState({
    total: 0,
    lastHour: 0,
    lastDay: 0,
    rate: 0
  });

  useEffect(() => {
    // Fetch activities from backend
    const fetchActivities = async () => {
      try {
        const response = await fetch('/api/activities');
        const data = await response.json();
        setActivities(data.activities || []);
        setStats(data.stats || stats);
      } catch (error) {
        console.error('Failed to fetch activities:', error);
      }
    };

    fetchActivities();
    const interval = setInterval(fetchActivities, 30000); // Refresh every 30s

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="mb-12 text-center">
          <h1 className="text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
            🤖 Autonomous Office Protocol
          </h1>
          <p className="text-xl text-gray-300">
            Colosseum Agent Hackathon 2026
          </p>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <StatCard
            title="Total Activities"
            value={stats.total}
            icon="📊"
            color="from-blue-500 to-cyan-500"
          />
          <StatCard
            title="Last Hour"
            value={stats.lastHour}
            icon="⏰"
            color="from-green-500 to-emerald-500"
          />
          <StatCard
            title="Last 24h"
            value={stats.lastDay}
            icon="📈"
            color="from-purple-500 to-pink-500"
          />
          <StatCard
            title="Rate (per hour)"
            value={stats.rate.toFixed(1)}
            icon="⚡"
            color="from-orange-500 to-red-500"
          />
        </div>

        {/* Activity Feed */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl">
          <h2 className="text-3xl font-bold mb-6 flex items-center">
            <span className="mr-3">📝</span>
            Recent Activities
          </h2>
          
          <div className="space-y-4 max-h-[600px] overflow-y-auto">
            {activities.length === 0 ? (
              <div className="text-center py-12 text-gray-400">
                <p className="text-xl mb-2">No activities yet</p>
                <p className="text-sm">Start the agent to begin logging activities</p>
              </div>
            ) : (
              activities.map((activity, index) => (
                <ActivityCard key={index} activity={activity} />
              ))
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-400">
          <p>Built for Colosseum Agent Hackathon 2026</p>
          <p className="text-sm mt-2">
            Powered by Claude AI + AgentWallet + Solana
          </p>
        </footer>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon, color }: {
  title: string;
  value: string | number;
  icon: string;
  color: string;
}) {
  return (
    <div className={`bg-gradient-to-br ${color} rounded-xl p-6 shadow-lg transform hover:scale-105 transition-transform`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-4xl">{icon}</span>
        <span className="text-3xl font-bold">{value}</span>
      </div>
      <p className="text-sm font-medium opacity-90">{title}</p>
    </div>
  );
}

function ActivityCard({ activity }: { activity: Activity }) {
  const getActivityIcon = (type: string) => {
    const icons: Record<string, string> = {
      position_monitor: '👀',
      ai_analysis: '🧠',
      action_execution: '⚡',
      registration: '🎯',
      test: '🧪',
      default: '📌'
    };
    return icons[type] || icons.default;
  };

  const getActivityColor = (type: string) => {
    const colors: Record<string, string> = {
      position_monitor: 'from-blue-500/20 to-cyan-500/20 border-blue-500',
      ai_analysis: 'from-purple-500/20 to-pink-500/20 border-purple-500',
      action_execution: 'from-orange-500/20 to-red-500/20 border-orange-500',
      registration: 'from-green-500/20 to-emerald-500/20 border-green-500',
      test: 'from-yellow-500/20 to-amber-500/20 border-yellow-500',
      default: 'from-gray-500/20 to-slate-500/20 border-gray-500'
    };
    return colors[activity.activity_type] || colors.default;
  };

  return (
    <div className={`bg-gradient-to-r ${getActivityColor(activity.activity_type)} border-l-4 rounded-lg p-4 hover:shadow-lg transition-shadow`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center mb-2">
            <span className="text-2xl mr-3">{getActivityIcon(activity.activity_type)}</span>
            <div>
              <h3 className="font-bold text-lg capitalize">
                {activity.activity_type.replace(/_/g, ' ')}
              </h3>
              <p className="text-sm text-gray-300">
                {new Date(activity.timestamp).toLocaleString()}
              </p>
            </div>
          </div>
          
          {activity.data && (
            <div className="ml-11 text-sm text-gray-200">
              <pre className="bg-black/20 rounded p-2 overflow-x-auto">
                {JSON.stringify(activity.data, null, 2)}
              </pre>
            </div>
          )}
        </div>
        
        <div className="ml-4 text-xs text-gray-400">
          <p title={activity.hash}>🔐 {activity.hash?.substring(0, 8)}...</p>
          <p title={activity.signature}>✍️ {activity.signature?.substring(0, 8)}...</p>
        </div>
      </div>
    </div>
  );
}
