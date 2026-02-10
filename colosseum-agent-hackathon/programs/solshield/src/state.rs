use anchor_lang::prelude::*;
use crate::{DeFiProtocol, RebalanceAction};

/// Global protocol state
#[account]
#[derive(Default)]
pub struct ProtocolState {
    /// Protocol admin
    pub authority: Pubkey,
    /// Agent authorized to update positions
    pub agent_authority: Pubkey,
    /// Default health factor warning threshold (basis points, e.g. 15000 = 1.5x)
    pub default_warn_threshold: u64,
    /// Default critical threshold (basis points)
    pub default_critical_threshold: u64,
    /// Max positions per user
    pub max_positions_per_user: u8,
    /// Fee for rebalancing (basis points)
    pub rebalance_fee_bps: u16,
    /// Total positions registered
    pub total_positions: u64,
    /// Total rebalances executed
    pub total_rebalances: u64,
    /// Total value protected (USD, 6 decimals)
    pub total_value_protected: u64,
    /// Bump seed
    pub bump: u8,
}

impl ProtocolState {
    pub const SIZE: usize = 8 + // discriminator
        32 +  // authority
        32 +  // agent_authority
        8 +   // default_warn_threshold
        8 +   // default_critical_threshold
        1 +   // max_positions_per_user
        2 +   // rebalance_fee_bps
        8 +   // total_positions
        8 +   // total_rebalances
        8 +   // total_value_protected
        1 +   // bump
        64;   // padding
}

/// A monitored DeFi position
#[account]
pub struct MonitoredPosition {
    /// Owner of the position
    pub owner: Pubkey,
    /// Which protocol this position is on
    pub protocol: DeFiProtocol,
    /// The obligation/margin account key on the lending protocol
    pub obligation_key: Pubkey,
    /// Current health factor (basis points, e.g. 15000 = 1.5x)
    pub health_factor: u64,
    /// Total collateral value (USD, 6 decimals)
    pub total_collateral_usd: u64,
    /// Total debt value (USD, 6 decimals)
    pub total_debt_usd: u64,
    /// Warning threshold (basis points)
    pub warn_threshold: u64,
    /// Critical threshold (basis points)
    pub critical_threshold: u64,
    /// Position status
    pub status: PositionStatus,
    /// Number of rebalances performed
    pub rebalance_count: u32,
    /// Last health check timestamp
    pub last_check_ts: i64,
    /// Last rebalance timestamp
    pub last_rebalance_ts: i64,
    /// Creation timestamp
    pub created_at: i64,
    /// Bump seed
    pub bump: u8,
}

impl MonitoredPosition {
    pub const SIZE: usize = 8 + // discriminator
        32 +  // owner
        1 +   // protocol (enum)
        32 +  // obligation_key
        8 +   // health_factor
        8 +   // total_collateral_usd
        8 +   // total_debt_usd
        8 +   // warn_threshold
        8 +   // critical_threshold
        1 +   // status (enum)
        4 +   // rebalance_count
        8 +   // last_check_ts
        8 +   // last_rebalance_ts
        8 +   // created_at
        1 +   // bump
        64;   // padding
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy, PartialEq, Eq)]
pub enum PositionStatus {
    Active,
    Warning,
    Critical,
    Paused,
    Closed,
}

impl Default for PositionStatus {
    fn default() -> Self {
        PositionStatus::Active
    }
}

/// Record of a rebalance action
#[account]
pub struct RebalanceRecord {
    /// The monitored position this rebalance was for
    pub position: Pubkey,
    /// Owner of the position
    pub owner: Pubkey,
    /// Type of rebalance action
    pub action_type: RebalanceAction,
    /// Amount involved (in lamports or token smallest unit)
    pub amount: u64,
    /// Health factor before rebalance (basis points)
    pub health_before: u64,
    /// Health factor after rebalance (basis points)
    pub health_after: u64,
    /// Transaction signature of the rebalance tx
    pub tx_signature: [u8; 64],
    /// SHA-256 hash of the AI reasoning trace
    pub ai_reasoning_hash: [u8; 32],
    /// Timestamp
    pub timestamp: i64,
    /// Bump seed
    pub bump: u8,
}

impl RebalanceRecord {
    pub const SIZE: usize = 8 + // discriminator
        32 +  // position
        32 +  // owner
        1 +   // action_type (enum)
        8 +   // amount
        8 +   // health_before
        8 +   // health_after
        64 +  // tx_signature
        32 +  // ai_reasoning_hash
        8 +   // timestamp
        1 +   // bump
        64;   // padding
}
