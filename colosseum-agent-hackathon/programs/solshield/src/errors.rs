use anchor_lang::prelude::*;

#[error_code]
pub enum SolShieldError {
    #[msg("Unauthorized: only the agent authority can perform this action")]
    UnauthorizedAgent,

    #[msg("Unauthorized: only the position owner can perform this action")]
    UnauthorizedOwner,

    #[msg("Position is currently paused")]
    PositionPaused,

    #[msg("Position is already closed")]
    PositionClosed,

    #[msg("Position is not paused")]
    PositionNotPaused,

    #[msg("Maximum positions per user exceeded")]
    MaxPositionsExceeded,

    #[msg("Invalid health factor: must be greater than 0")]
    InvalidHealthFactor,

    #[msg("Invalid threshold: warn must be greater than critical")]
    InvalidThresholds,

    #[msg("Health factor is healthy, no rebalance needed")]
    HealthFactorHealthy,

    #[msg("Rebalance cooldown not elapsed")]
    RebalanceCooldown,

    #[msg("Invalid protocol specified")]
    InvalidProtocol,
}
