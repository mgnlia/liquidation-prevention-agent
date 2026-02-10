import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Autonomous Office Protocol | AOP Dashboard',
  description: 'First on-chain verified autonomous software company. Real-time multi-agent coordination proof on Solana.',
}

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="mb-12 text-center">
          <h1 className="text-5xl font-bold text-white mb-4">
            Autonomous Office Protocol
          </h1>
          <p className="text-xl text-purple-200 mb-2">
            First on-chain verified autonomous software company
          </p>
          <p className="text-sm text-purple-300">
            Multi-agent AI office with cryptographic proof on Solana
          </p>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <StatCard
            title="Activities Logged"
            value="0"
            subtitle="Target: 500+"
            icon="📊"
          />
          <StatCard
            title="Agents Coordinating"
            value="3"
            subtitle="Henry, Dev, Sage"
            icon="👥"
          />
          <StatCard
            title="Verification Rate"
            value="100%"
            subtitle="All activities signed"
            icon="🔐"
          />
          <StatCard
            title="On-Chain Proofs"
            value="0"
            subtitle="Solana devnet"
            icon="⛓️"
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Activity Feed */}
          <div className="bg-slate-800/50 backdrop-blur rounded-lg p-6 border border-purple-500/20">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
              <span className="mr-2">📝</span>
              Live Activity Feed
            </h2>
            <div className="text-purple-200 text-center py-8">
              <p className="mb-2">⏳ Waiting for registration...</p>
              <p className="text-sm text-purple-300">
                Activities will appear here once agent is registered and on-chain logging begins
              </p>
            </div>
          </div>

          {/* Coordination Graph */}
          <div className="bg-slate-800/50 backdrop-blur rounded-lg p-6 border border-purple-500/20">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
              <span className="mr-2">🔗</span>
              Agent Coordination
            </h2>
            <div className="text-purple-200 text-center py-8">
              <div className="flex justify-center items-center space-x-4 mb-4">
                <AgentNode name="Henry" role="CSO" />
                <span className="text-2xl">→</span>
                <AgentNode name="Dev" role="Engineer" />
                <span className="text-2xl">→</span>
                <AgentNode name="Sage" role="Architect" />
              </div>
              <p className="text-sm text-purple-300 mt-4">
                Multi-agent coordination graph will show real-time task flows
              </p>
            </div>
          </div>
        </div>

        {/* How It Works */}
        <div className="bg-slate-800/50 backdrop-blur rounded-lg p-6 border border-purple-500/20 mb-12">
          <h2 className="text-2xl font-bold text-white mb-4">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
            <Step
              number="1"
              title="Activity Occurs"
              description="Task assignment, code commit, decision made"
            />
            <Step
              number="2"
              title="SHA256 Hash"
              description="Activity data is hashed for integrity"
            />
            <Step
              number="3"
              title="Ed25519 Sign"
              description="Agent signs hash with private key"
            />
            <Step
              number="4"
              title="On-Chain Anchor"
              description="Signature anchored to Solana via memo program"
            />
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center text-purple-300 text-sm">
          <p className="mb-2">
            Built for <a href="https://colosseum.com/agent-hackathon/" className="text-purple-400 hover:text-purple-300 underline" target="_blank" rel="noopener noreferrer">Colosseum Agent Hackathon 2026</a>
          </p>
          <p>
            <a href="https://github.com/mgnlia/colosseum-agent-hackathon" className="text-purple-400 hover:text-purple-300 underline" target="_blank" rel="noopener noreferrer">
              View on GitHub
            </a>
          </p>
        </footer>
      </div>
    </main>
  )
}

// Components
function StatCard({ title, value, subtitle, icon }: { title: string; value: string; subtitle: string; icon: string }) {
  return (
    <div className="bg-slate-800/50 backdrop-blur rounded-lg p-6 border border-purple-500/20">
      <div className="text-4xl mb-2">{icon}</div>
      <div className="text-3xl font-bold text-white mb-1">{value}</div>
      <div className="text-sm font-medium text-purple-200 mb-1">{title}</div>
      <div className="text-xs text-purple-300">{subtitle}</div>
    </div>
  )
}

function AgentNode({ name, role }: { name: string; role: string }) {
  return (
    <div className="bg-purple-900/50 border border-purple-500/30 rounded-lg p-3 text-center">
      <div className="text-lg font-bold text-white">{name}</div>
      <div className="text-xs text-purple-300">{role}</div>
    </div>
  )
}

function Step({ number, title, description }: { number: string; title: string; description: string }) {
  return (
    <div className="text-purple-200">
      <div className="text-3xl font-bold text-purple-400 mb-2">{number}</div>
      <div className="text-sm font-bold text-white mb-1">{title}</div>
      <div className="text-xs text-purple-300">{description}</div>
    </div>
  )
}
