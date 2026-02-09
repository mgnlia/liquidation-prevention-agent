'use client'

import { useState } from 'react'
import { X, Zap, TrendingUp, AlertCircle } from 'lucide-react'

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

interface RebalanceModalProps {
  position: Position
  onClose: () => void
}

export default function RebalanceModal({ position, onClose }: RebalanceModalProps) {
  const [strategy, setStrategy] = useState<'add-collateral' | 'repay-debt'>('add-collateral')
  const [amount, setAmount] = useState('')
  const [executing, setExecuting] = useState(false)

  const calculateNewHealthFactor = () => {
    // Simplified calculation for demo
    if (strategy === 'add-collateral') {
      return position.healthFactor + (parseFloat(amount) || 0) * 0.2
    } else {
      return position.healthFactor + (parseFloat(amount) || 0) * 0.00015
    }
  }

  const handleExecute = async () => {
    setExecuting(true)
    // Simulate transaction
    await new Promise(resolve => setTimeout(resolve, 2000))
    setExecuting(false)
    alert('Rebalance executed successfully!')
    onClose()
  }

  const newHealthFactor = calculateNewHealthFactor()

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-slate-800 border border-slate-700 rounded-xl max-w-lg w-full p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <Zap className="w-6 h-6 text-purple-400" />
            <h2 className="text-xl font-bold text-white">AI-Powered Rebalance</h2>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white">
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Current Position */}
        <div className="bg-slate-900/50 rounded-lg p-4 mb-6">
          <p className="text-slate-400 text-sm mb-2">Current Position</p>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-slate-300">Protocol</span>
              <span className="text-white font-medium">{position.protocol}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-300">Health Factor</span>
              <span className="text-yellow-400 font-bold">{position.healthFactor.toFixed(2)}</span>
            </div>
          </div>
        </div>

        {/* Strategy Selection */}
        <div className="mb-6">
          <p className="text-slate-400 text-sm mb-3">Rebalancing Strategy</p>
          <div className="grid grid-cols-2 gap-3">
            <button
              onClick={() => setStrategy('add-collateral')}
              className={`p-3 rounded-lg border transition-colors ${
                strategy === 'add-collateral'
                  ? 'bg-purple-600 border-purple-500 text-white'
                  : 'bg-slate-700 border-slate-600 text-slate-300 hover:border-slate-500'
              }`}
            >
              <TrendingUp className="w-5 h-5 mx-auto mb-1" />
              <p className="text-sm font-medium">Add Collateral</p>
            </button>
            <button
              onClick={() => setStrategy('repay-debt')}
              className={`p-3 rounded-lg border transition-colors ${
                strategy === 'repay-debt'
                  ? 'bg-purple-600 border-purple-500 text-white'
                  : 'bg-slate-700 border-slate-600 text-slate-300 hover:border-slate-500'
              }`}
            >
              <TrendingUp className="w-5 h-5 mx-auto mb-1" />
              <p className="text-sm font-medium">Repay Debt</p>
            </button>
          </div>
        </div>

        {/* Amount Input */}
        <div className="mb-6">
          <label className="text-slate-400 text-sm mb-2 block">
            {strategy === 'add-collateral' ? 'Collateral Amount' : 'Debt Amount'}
          </label>
          <div className="relative">
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="0.0"
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-purple-500"
            />
            <span className="absolute right-4 top-3 text-slate-400">
              {strategy === 'add-collateral' ? position.collateral : position.debt}
            </span>
          </div>
        </div>

        {/* AI Recommendation */}
        <div className="bg-purple-900/30 border border-purple-700/50 rounded-lg p-4 mb-6">
          <div className="flex items-start gap-2">
            <AlertCircle className="w-5 h-5 text-purple-400 mt-0.5" />
            <div>
              <p className="text-purple-200 text-sm font-medium mb-1">AI Recommendation</p>
              <p className="text-purple-300 text-xs">
                {strategy === 'add-collateral'
                  ? `Adding ${amount || '0'} ${position.collateral} will improve your health factor to ${newHealthFactor.toFixed(2)}`
                  : `Repaying ${amount || '0'} ${position.debt} will improve your health factor to ${newHealthFactor.toFixed(2)}`
                }
              </p>
            </div>
          </div>
        </div>

        {/* New Health Factor Preview */}
        {amount && parseFloat(amount) > 0 && (
          <div className="bg-slate-900/50 rounded-lg p-4 mb-6">
            <div className="flex justify-between items-center">
              <span className="text-slate-400">New Health Factor</span>
              <span className={`text-xl font-bold ${
                newHealthFactor >= 2.0 ? 'text-green-400' :
                newHealthFactor >= 1.5 ? 'text-blue-400' :
                'text-yellow-400'
              }`}>
                {newHealthFactor.toFixed(2)}
              </span>
            </div>
          </div>
        )}

        {/* Execute Button */}
        <button
          onClick={handleExecute}
          disabled={!amount || parseFloat(amount) <= 0 || executing}
          className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-slate-700 disabled:text-slate-500 text-white font-medium py-3 rounded-lg transition-colors"
        >
          {executing ? 'Executing...' : 'Execute Flash Loan Rebalance'}
        </button>

        <p className="text-slate-500 text-xs text-center mt-3">
          Uses Aave V3 flash loans for capital-efficient rebalancing
        </p>
      </div>
    </div>
  )
}
