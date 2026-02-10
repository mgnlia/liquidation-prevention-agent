'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'

const mockData = [
  { time: '00:00', healthFactor: 1.85 },
  { time: '04:00', healthFactor: 1.72 },
  { time: '08:00', healthFactor: 1.58 },
  { time: '12:00', healthFactor: 1.45 },
  { time: '16:00', healthFactor: 1.32 },
  { time: '20:00', healthFactor: 1.28 },
  { time: '24:00', healthFactor: 1.31 },
]

export default function HealthFactorChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={mockData}>
        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
        <XAxis dataKey="time" stroke="#94a3b8" />
        <YAxis stroke="#94a3b8" domain={[0, 3]} />
        <Tooltip
          contentStyle={{
            backgroundColor: '#1e293b',
            border: '1px solid #475569',
            borderRadius: '8px',
          }}
          labelStyle={{ color: '#cbd5e1' }}
        />
        <ReferenceLine y={1.0} stroke="#ef4444" strokeDasharray="3 3" label="Liquidation" />
        <ReferenceLine y={1.5} stroke="#eab308" strokeDasharray="3 3" label="Warning" />
        <Line
          type="monotone"
          dataKey="healthFactor"
          stroke="#3b82f6"
          strokeWidth={3}
          dot={{ fill: '#3b82f6', r: 4 }}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
