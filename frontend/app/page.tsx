'use client';

import { useState, useEffect } from 'react';
import { ConnectButton } from '@rainbow-me/rainbowkit';
import { useAccount } from 'wagmi';
import { Shield, Activity, AlertTriangle, TrendingUp, Zap, Brain, DollarSign } from 'lucide-react';
import PositionCard from '@/components/PositionCard';
import HealthFactorChart from '@/components/HealthFactorChart';
import AgentActivity from '@/components/AgentActivity';
import StatsGrid from '@/components/StatsGrid';

export default function Home() {
  const { address, isConnected } = useAccount();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-lg">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">AI Liquidation Prevention</h1>
                <p className="text-xs text-gray-400">Powered by Claude AI</p>
              </div>
            </div>
            <ConnectButton />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {!isConnected ? (
          // Landing View
          <div className="max-w-4xl mx-auto text-center py-20">
            <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-4 rounded-full w-24 h-24 mx-auto mb-6 flex items-center justify-center">
              <Shield className="w-12 h-12 text-white" />
            </div>
            <h2 className="text-4xl font-bold text-white mb-4">
              Never Get Liquidated Again
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              AI-powered monitoring and automatic rebalancing for your DeFi positions
            </p>
            
            <div className="grid md:grid-cols-3 gap-6 mb-12">
              <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                <Brain className="w-10 h-10 text-blue-400 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-white mb-2">AI Monitoring</h3>
                <p className="text-gray-400 text-sm">
                  Claude AI analyzes your positions 24/7 and predicts risks before they happen
                </p>
              </div>
              
              <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                <Zap className="w-10 h-10 text-purple-400 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-white mb-2">Auto Rebalancing</h3>
                <p className="text-gray-400 text-sm">
                  Automatic flash loan rebalancing when health factor drops below safe levels
                </p>
              </div>
              
              <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                <DollarSign className="w-10 h-10 text-green-400 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-white mb-2">Save Money</h3>
                <p className="text-gray-400 text-sm">
                  Avoid 5-10% liquidation penalties. That's $500-$1000 saved on a $10k position
                </p>
              </div>
            </div>

            <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-6 mb-8">
              <p className="text-blue-300 font-semibold mb-2">🎯 ETHDenver 2026 | HackMoney 2026</p>
              <p className="text-gray-300 text-sm">
                Live on Sepolia, Base Sepolia, and Arbitrum Sepolia testnets
              </p>
            </div>

            <ConnectButton.Custom>
              {({ openConnectModal }) => (
                <button
                  onClick={openConnectModal}
                  className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:from-blue-600 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl"
                >
                  Connect Wallet to Get Started
                </button>
              )}
            </ConnectButton.Custom>
          </div>
        ) : (
          // Dashboard View
          <div className="space-y-6">
            {/* Stats Grid */}
            <StatsGrid address={address!} />

            {/* Main Grid */}
            <div className="grid lg:grid-cols-3 gap-6">
              {/* Left Column - Positions */}
              <div className="lg:col-span-2 space-y-6">
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg border border-gray-700 p-6">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-semibold text-white flex items-center gap-2">
                      <Activity className="w-5 h-5 text-blue-400" />
                      Your Positions
                    </h2>
                    <button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                      Enable Agent
                    </button>
                  </div>
                  
                  <div className="space-y-4">
                    <PositionCard
                      protocol="Aave V3"
                      collateral="10.5 ETH"
                      collateralUSD="$32,550"
                      debt="15,000 USDC"
                      healthFactor={1.85}
                      status="safe"
                    />
                    <PositionCard
                      protocol="Compound V3"
                      collateral="5.2 ETH"
                      collateralUSD="$16,120"
                      debt="8,500 USDC"
                      healthFactor={1.42}
                      status="warning"
                    />
                  </div>
                </div>

                {/* Health Factor Chart */}
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg border border-gray-700 p-6">
                  <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-green-400" />
                    Health Factor History
                  </h2>
                  <HealthFactorChart />
                </div>
              </div>

              {/* Right Column - Agent Activity */}
              <div className="space-y-6">
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg border border-gray-700 p-6">
                  <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
                    <Brain className="w-5 h-5 text-purple-400" />
                    Agent Activity
                  </h2>
                  <AgentActivity />
                </div>

                {/* Quick Actions */}
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg border border-gray-700 p-6">
                  <h2 className="text-lg font-semibold text-white mb-4">Quick Actions</h2>
                  <div className="space-y-3">
                    <button className="w-full bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-lg font-medium transition-colors">
                      Manual Rebalance
                    </button>
                    <button className="w-full bg-gray-700 hover:bg-gray-600 text-white py-3 rounded-lg font-medium transition-colors">
                      View Transactions
                    </button>
                    <button className="w-full bg-gray-700 hover:bg-gray-600 text-white py-3 rounded-lg font-medium transition-colors">
                      Settings
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 bg-gray-900/50 backdrop-blur-sm mt-20">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-gray-400 text-sm">
              Built for ETHDenver 2026 & HackMoney 2026 | Powered by Claude AI
            </p>
            <div className="flex gap-4 text-sm text-gray-400">
              <a href="https://github.com/mgnlia/liquidation-prevention-agent" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">
                GitHub
              </a>
              <a href="/docs" className="hover:text-white transition-colors">
                Docs
              </a>
              <a href="/demo" className="hover:text-white transition-colors">
                Demo
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
