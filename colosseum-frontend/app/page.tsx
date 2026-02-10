'use client'

import { Cpu, Zap, TrendingUp, Shield, Activity, ArrowRight } from 'lucide-react'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Cpu className="w-8 h-8 text-purple-400" />
            <h1 className="text-2xl font-bold text-white">Colosseum Agent</h1>
          </div>
          <a 
            href="https://github.com/mgnlia/colosseum-agent-hackathon"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
          >
            View on GitHub
          </a>
        </div>
      </header>

      {/* Hero Section */}
      <div className="container mx-auto px-4 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-purple-500/20 text-purple-300 px-4 py-2 rounded-full mb-6">
            <Zap className="w-4 h-4" />
            <span className="text-sm font-medium">Colosseum Hackathon 2024</span>
          </div>
          
          <h2 className="text-5xl font-bold text-white mb-6">
            AI-Powered Solana Agent
          </h2>
          
          <p className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
            Autonomous DeFi agent leveraging Claude AI for intelligent trading, 
            yield optimization, and risk management on Solana.
          </p>

          <div className="flex justify-center gap-4 mb-16">
            <a 
              href="https://github.com/mgnlia/colosseum-agent-hackathon"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center gap-2"
            >
              View Source Code
              <ArrowRight className="w-4 h-4" />
            </a>
            <a 
              href="https://github.com/mgnlia/colosseum-agent-hackathon/blob/main/README.md"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-slate-800 hover:bg-slate-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              Documentation
            </a>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-6 mt-12">
            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
              <Activity className="w-12 h-12 text-purple-400 mb-4 mx-auto" />
              <h3 className="text-lg font-semibold text-white mb-2">Autonomous Trading</h3>
              <p className="text-slate-400 text-sm">
                AI-driven trading strategies powered by Claude for optimal execution
              </p>
            </div>

            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
              <Shield className="w-12 h-12 text-green-400 mb-4 mx-auto" />
              <h3 className="text-lg font-semibold text-white mb-2">Risk Management</h3>
              <p className="text-slate-400 text-sm">
                Intelligent position monitoring and automated risk mitigation
              </p>
            </div>

            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
              <TrendingUp className="w-12 h-12 text-blue-400 mb-4 mx-auto" />
              <h3 className="text-lg font-semibold text-white mb-2">Yield Optimization</h3>
              <p className="text-slate-400 text-sm">
                Automatic yield farming and liquidity provision optimization
              </p>
            </div>
          </div>

          {/* Architecture Overview */}
          <div className="mt-16 bg-slate-800/30 backdrop-blur border border-slate-700 rounded-xl p-8">
            <h3 className="text-2xl font-bold text-white mb-6">Architecture</h3>
            <div className="grid md:grid-cols-2 gap-6 text-left">
              <div>
                <h4 className="text-lg font-semibold text-purple-400 mb-3">Core Components</h4>
                <ul className="space-y-2 text-slate-300">
                  <li className="flex items-start gap-2">
                    <span className="text-purple-400 mt-1">•</span>
                    <span>Claude AI reasoning engine for decision-making</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-purple-400 mt-1">•</span>
                    <span>Solana Web3.js for on-chain interactions</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-purple-400 mt-1">•</span>
                    <span>Real-time market data aggregation</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-purple-400 mt-1">•</span>
                    <span>Multi-protocol DeFi integrations</span>
                  </li>
                </ul>
              </div>
              <div>
                <h4 className="text-lg font-semibold text-purple-400 mb-3">Key Features</h4>
                <ul className="space-y-2 text-slate-300">
                  <li className="flex items-start gap-2">
                    <span className="text-purple-400 mt-1">•</span>
                    <span>Automated portfolio rebalancing</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-purple-400 mt-1">•</span>
                    <span>MEV-aware transaction execution</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-purple-400 mt-1">•</span>
                    <span>Gas optimization strategies</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-purple-400 mt-1">•</span>
                    <span>Comprehensive risk analytics</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Tech Stack */}
          <div className="mt-16 pt-8 border-t border-slate-700">
            <p className="text-slate-400 text-sm mb-4">Built with</p>
            <div className="flex flex-wrap justify-center gap-4 text-slate-300 text-sm">
              <span className="px-3 py-1 bg-slate-800 rounded-full">Solana</span>
              <span className="px-3 py-1 bg-slate-800 rounded-full">Claude API</span>
              <span className="px-3 py-1 bg-slate-800 rounded-full">Python</span>
              <span className="px-3 py-1 bg-slate-800 rounded-full">Web3.js</span>
              <span className="px-3 py-1 bg-slate-800 rounded-full">Next.js</span>
              <span className="px-3 py-1 bg-slate-800 rounded-full">TypeScript</span>
            </div>
          </div>

          {/* Stats */}
          <div className="grid md:grid-cols-4 gap-4 mt-12">
            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-4">
              <p className="text-3xl font-bold text-purple-400">70+</p>
              <p className="text-slate-400 text-sm mt-1">Files</p>
            </div>
            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-4">
              <p className="text-3xl font-bold text-purple-400">12+</p>
              <p className="text-slate-400 text-sm mt-1">Commits</p>
            </div>
            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-4">
              <p className="text-3xl font-bold text-purple-400">5+</p>
              <p className="text-slate-400 text-sm mt-1">Protocols</p>
            </div>
            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-4">
              <p className="text-3xl font-bold text-purple-400">100%</p>
              <p className="text-slate-400 text-sm mt-1">AI-Powered</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
