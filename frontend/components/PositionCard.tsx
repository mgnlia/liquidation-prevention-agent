import { Shield, AlertTriangle, AlertCircle } from 'lucide-react';

interface PositionCardProps {
  protocol: string;
  collateral: string;
  collateralUSD: string;
  debt: string;
  healthFactor: number;
  status: 'safe' | 'warning' | 'danger';
}

export default function PositionCard({
  protocol,
  collateral,
  collateralUSD,
  debt,
  healthFactor,
  status,
}: PositionCardProps) {
  const statusConfig = {
    safe: {
      icon: Shield,
      color: 'text-green-400',
      bg: 'bg-green-500/10',
      border: 'border-green-500/30',
      label: 'Safe',
    },
    warning: {
      icon: AlertTriangle,
      color: 'text-yellow-400',
      bg: 'bg-yellow-500/10',
      border: 'border-yellow-500/30',
      label: 'Warning',
    },
    danger: {
      icon: AlertCircle,
      color: 'text-red-400',
      bg: 'bg-red-500/10',
      border: 'border-red-500/30',
      label: 'Danger',
    },
  };

  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <div className={`bg-gray-900/50 rounded-lg border ${config.border} p-4 hover:border-opacity-50 transition-all`}>
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-white font-semibold text-lg">{protocol}</h3>
          <p className="text-gray-400 text-sm">Sepolia Testnet</p>
        </div>
        <div className={`flex items-center gap-2 ${config.bg} px-3 py-1 rounded-full`}>
          <Icon className={`w-4 h-4 ${config.color}`} />
          <span className={`text-sm font-medium ${config.color}`}>{config.label}</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-gray-400 text-xs mb-1">Collateral</p>
          <p className="text-white font-semibold">{collateral}</p>
          <p className="text-gray-500 text-xs">{collateralUSD}</p>
        </div>
        <div>
          <p className="text-gray-400 text-xs mb-1">Debt</p>
          <p className="text-white font-semibold">{debt}</p>
        </div>
      </div>

      <div className="border-t border-gray-700 pt-3">
        <div className="flex items-center justify-between">
          <span className="text-gray-400 text-sm">Health Factor</span>
          <span className={`text-lg font-bold ${config.color}`}>{healthFactor.toFixed(2)}</span>
        </div>
        <div className="mt-2 bg-gray-700 rounded-full h-2 overflow-hidden">
          <div
            className={`h-full ${
              status === 'safe' ? 'bg-green-500' : status === 'warning' ? 'bg-yellow-500' : 'bg-red-500'
            }`}
            style={{ width: `${Math.min(healthFactor * 50, 100)}%` }}
          />
        </div>
      </div>
    </div>
  );
}
