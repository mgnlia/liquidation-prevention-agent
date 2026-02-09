'use client'

import { useState, useEffect } from 'react'
import { useAccount } from 'wagmi'
import { AlertTriangle, TrendingUp, Shield, Zap, RefreshCw } from 'lucide-react'
import PositionCard from './PositionCard'
import HealthFactorChart from './HealthFactorChart'
import RebalanceModal from './RebalanceModal'

interface Position {
  protocol: 'Aave V3' | 'Compound V3'
  collateral: string
  collateralAmount: string
  debt: string
  debtAmount: string
  healthFactor: number
  liquidationThreshold: number
  address: string
}

export default function Dashboard() {
  const { address } = useAccount()
  const [positions, setPositions] = useState<Position[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedPosition, setSelectedPosition] = useState<Position | null>(null)
  const [showRebalanceModal, setShowRebalanceModal] = useState(false)

  useEffect(() => {
    // Mock data for demo - in production, fetch from The Graph
    const mockPositions: Position[] = [
      {
        protocol: 'Aave V3',
        collateral: 'ETH',
        collateralAmount: '5.5',
        debt: 'USDC',
        debtAmount: '8500',
        healthFactor: 1.45,
        liquidationThreshold: 1.0,
        address: '0x...'
      },
      {
        protocol: 'Compound V3',
        collateral: 'WBTC',
        collateralAmount: '0.25',
        debt: 'USDC',
        debtAmount: '12000',
        healthFactor: 1.18,
        liquidationThreshold: 1.0,
        address: '0x...'
      }
    ]

    setTimeout(() => {
      setPositions(mockPositions)
      setLoading(false)
    }, 1000)
  }, [address])

  const handleRebalance = (position: Position) => {
    setSelectedPosition(position)
    setShowRebalanceModal(true)
  }

  const getHealthStatus = (healthFactor: number) => {
    if (healthFactor >= 2.0) return { text: 'Healthy', color: 'text-green-400', bg: 'bg-green-500/20' }
    if (healthFactor >= 1.5) return { text: 'Good', color: 'text-blue-400', bg: 'bg-blue-500/20' }
    if (healthFactor >= 1.2) return { text: 'Warning', color: 'text-yellow-400', bg: 'bg-yellow-500/20' }
    return { text: 'Critical', color: 'text-red-400', bg: 'bg-red-500/20' }
  }

  const avgHealthFactor = positions.length > 0
    ? positions.reduce((sum, p) => sum + p.healthFactor, 0) / positions.length
    : 0

  const criticalPositions = positions.filter(p => p.healthFactor < 1.5).length

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-20">
        <div className="flex items-center justify-center">
          <RefreshCw className="w-8 h-8 text-blue-400 animate-spin" />
          <span className="ml-3 text-white text-lg">Loading positions...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Stats Overview */}
      <div className="grid md:grid-cols-4 gap-4 mb-8">
        <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-slate-400 text-sm">Active Positions</span>
            <Shield className="w-5 h-5 text-blue-400" />
          </div>
          <p className="text-3xl font-bold text-white">{positions.length}</p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-slate-400 text-sm">Avg Health Factor</span>
            <TrendingUp className="w-5 h-5 text-green-400" />
          </div>
          <p className="text-3xl font-bold text-white">{avgHealthFactor.toFixed(2)}</p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-slate-400 text-sm">At Risk</span>
            <AlertTriangle className="w-5 h-5 text-yellow-400" />
          </div>
          <p className="text-3xl font-bold text-white">{criticalPositions}</p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-slate-400 text-sm">AI Status</span>
            <Zap className="w-5 h-5 text-purple-400" />
          </div>
          <p className="text-lg font-semibold text-green-400">Active</p>
        </div>
      </div>

      {/* Health Factor Chart */}
      <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6 mb-8">
        <h3 className="text-xl font-semibold text-white mb-4">Health Factor History</h3>
        <HealthFactorChart />
      </div>

      {/* Positions List */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-white mb-4">Your Positions</h3>
        <div className="grid md:grid-cols-2 gap-4">
          {positions.map((position, idx) => (
            <PositionCard
              key={idx}
              position={position}
              onRebalance={handleRebalance}
              getHealthStatus={getHealthStatus}
            />
          ))}
        </div>
      </div>

      {/* AI Insights */}
      <div className="bg-gradient-to-r from-purple-900/50 to-blue-900/50 backdrop-blur border border-purple-700/50 rounded-xl p-6">
        <div className="flex items-start gap-4">
          <Zap className="w-6 h-6 text-purple-400 mt-1" />
          <div>
            <h3 className="text-lg font-semibold text-white mb-2">AI Recommendation</h3>
            <p className="text-slate-300 mb-4">
              Your Compound V3 position (Health Factor: 1.18) is approaching the warning threshold. 
              Consider rebalancing by adding 0.05 WBTC collateral or repaying 2,000 USDC debt to improve your health factor to 1.5+.
            </p>
            <button 
              onClick={() => positions[1] && handleRebalance(positions[1])}
              className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
            >
              Execute Rebalance
            </button>
          </div>
        </div>
      </div>

      {/* Rebalance Modal */}
      {showRebalanceModal && selectedPosition && (
        <RebalanceModal
          position={selectedPosition}
          onClose={() => setShowRebalanceModal(false)}
        />
      )}
    </div>
  )
}
