'use client'

import { Shield, AlertTriangle } from 'lucide-react'

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

interface PositionCardProps {
  position: Position
  onRebalance: (position: Position) => void
  getHealthStatus: (healthFactor: number) => { text: string; color: string; bg: string }
}

export default function PositionCard({ position, onRebalance, getHealthStatus }: PositionCardProps) {
  const status = getHealthStatus(position.healthFactor)
  const isAtRisk = position.healthFactor < 1.5

  return (
    <div className={`bg-slate-800/50 backdrop-blur border rounded-xl p-6 ${
      isAtRisk ? 'border-yellow-500/50' : 'border-slate-700'
    }`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Shield className="w-5 h-5 text-blue-400" />
          <span className="font-semibold text-white">{position.protocol}</span>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-medium ${status.bg} ${status.color}`}>
          {status.text}
        </div>
      </div>

      {/* Position Details */}
      <div className="space-y-3 mb-4">
        <div className="flex justify-between items-center">
          <span className="text-slate-400 text-sm">Collateral</span>
          <span className="text-white font-medium">
            {position.collateralAmount} {position.collateral}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-slate-400 text-sm">Debt</span>
          <span className="text-white font-medium">
            {position.debtAmount} {position.debt}
          </span>
        </div>
        <div className="pt-3 border-t border-slate-700">
          <div className="flex justify-between items-center mb-2">
            <span className="text-slate-400 text-sm">Health Factor</span>
            <span className={`text-xl font-bold ${status.color}`}>
              {position.healthFactor.toFixed(2)}
            </span>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all ${
                position.healthFactor >= 2.0 ? 'bg-green-500' :
                position.healthFactor >= 1.5 ? 'bg-blue-500' :
                position.healthFactor >= 1.2 ? 'bg-yellow-500' :
                'bg-red-500'
              }`}
              style={{ width: `${Math.min((position.healthFactor / 3) * 100, 100)}%` }}
            />
          </div>
        </div>
      </div>

      {/* Warning Message */}
      {isAtRisk && (
        <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3 mb-4">
          <div className="flex items-start gap-2">
            <AlertTriangle className="w-4 h-4 text-yellow-400 mt-0.5" />
            <p className="text-yellow-200 text-xs">
              Position at risk. Health factor below recommended threshold of 1.5
            </p>
          </div>
        </div>
      )}

      {/* Action Button */}
      <button
        onClick={() => onRebalance(position)}
        className={`w-full py-2 rounded-lg font-medium transition-colors ${
          isAtRisk
            ? 'bg-yellow-600 hover:bg-yellow-700 text-white'
            : 'bg-slate-700 hover:bg-slate-600 text-slate-300'
        }`}
      >
        {isAtRisk ? 'Rebalance Now' : 'Manage Position'}
      </button>
    </div>
  )
}
