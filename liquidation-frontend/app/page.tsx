'use client'

import { ConnectButton } from '@rainbow-me/rainbowkit'
import { useAccount } from 'wagmi'
import { Shield, TrendingUp, Zap, AlertTriangle, Activity } from 'lucide-react'
import Dashboard from '@/components/Dashboard'

export default function Home() {
  const { isConnected } = useAccount()

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Shield className="w-8 h-8 text-blue-400" />
            <h1 className="text-2xl font-bold text-white">AI Liquidation Prevention</h1>
          </div>
          <ConnectButton />
        </div>
      </header>

      {/* Hero Section */}
      {!isConnected ? (
        <div className="container mx-auto px-4 py-20">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 bg-blue-500/20 text-blue-300 px-4 py-2 rounded-full mb-6">
              <Zap className="w-4 h-4" />
              <span className="text-sm font-medium">HackMoney 2026 Project</span>
            </div>
            
            <h2 className="text-5xl font-bold text-white mb-6">
              Never Get Liquidated Again
            </h2>
            
            <p className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
              AI-powered monitoring and automated rebalancing for your DeFi positions 
              across Aave and Compound. Stay safe with proactive protection.
            </p>

            <div className="flex justify-center mb-16">
              <ConnectButton />
            </div>

            {/* Features Grid */}
            <div className="grid md:grid-cols-3 gap-6 mt-12">
              <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
                <Activity className="w-12 h-12 text-blue-400 mb-4 mx-auto" />
                <h3 className="text-lg font-semibold text-white mb-2">Real-Time Monitoring</h3>
                <p className="text-slate-400 text-sm">
                  Track health factors across Aave V3 and Compound V3 positions in real-time
                </p>
              </div>

              <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
                <Shield className="w-12 h-12 text-green-400 mb-4 mx-auto" />
                <h3 className="text-lg font-semibold text-white mb-2">AI-Powered Protection</h3>
                <p className="text-slate-400 text-sm">
                  Claude AI analyzes market conditions and suggests optimal rebalancing strategies
                </p>
              </div>

              <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
                <TrendingUp className="w-12 h-12 text-purple-400 mb-4 mx-auto" />
                <h3 className="text-lg font-semibold text-white mb-2">Flash Loan Rebalancing</h3>
                <p className="text-slate-400 text-sm">
                  Execute capital-efficient rebalancing using Aave flash loans automatically
                </p>
              </div>
            </div>

            {/* Tech Stack */}
            <div className="mt-16 pt-8 border-t border-slate-700">
              <p className="text-slate-400 text-sm mb-4">Built with</p>
              <div className="flex flex-wrap justify-center gap-4 text-slate-300 text-sm">
                <span className="px-3 py-1 bg-slate-800 rounded-full">Aave V3</span>
                <span className="px-3 py-1 bg-slate-800 rounded-full">Compound V3</span>
                <span className="px-3 py-1 bg-slate-800 rounded-full">Claude API</span>
                <span className="px-3 py-1 bg-slate-800 rounded-full">LangGraph</span>
                <span className="px-3 py-1 bg-slate-800 rounded-full">The Graph</span>
                <span className="px-3 py-1 bg-slate-800 rounded-full">Next.js</span>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <Dashboard />
      )}
    </main>
  )
}
