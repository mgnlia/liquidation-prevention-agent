use anchor_lang::prelude::*;

declare_id!("SoLShie1dAiPrevention1111111111111111111111");

pub mod state;
pub mod instructions;
pub mod errors;

use instructions::*;

#[program]
pub mod solshield {
    use super::*;

    /// Initialize the SolShield protocol
    pub fn initialize(ctx: Context<Initialize>, config: ProtocolConfig) -> Result<()> {
        instructions::initialize::handler(ctx, config)
    }

    /// Register a user position for monitoring
    pub fn register_position(
        ctx: Context<RegisterPosition>,
        protocol: DeFiProtocol,
        obligation_key: Pubkey,
        warn_threshold: u64,
        critical_threshold: u64,
    ) -> Result<()> {
        instructions::register_position::handler(
            ctx,
            protocol,
            obligation_key,
            warn_threshold,
            critical_threshold,
        )
    }

    /// Update position health factor (called by agent)
    pub fn update_health(
        ctx: Context<UpdateHealth>,
        health_factor: u64,
        total_collateral_usd: u64,
        total_debt_usd: u64,
    ) -> Result<()> {
        instructions::update_health::handler(
            ctx,
            health_factor,
            total_collateral_usd,
            total_debt_usd,
        )
    }

    /// Record a rebalance action executed by the agent
    pub fn record_rebalance(
        ctx: Context<RecordRebalance>,
        action_type: RebalanceAction,
        amount: u64,
        tx_signature: [u8; 64],
        ai_reasoning_hash: [u8; 32],
    ) -> Result<()> {
        instructions::record_rebalance::handler(
            ctx,
            action_type,
            amount,
            tx_signature,
            ai_reasoning_hash,
        )
    }

    /// Emergency pause monitoring for a position
    pub fn pause_position(ctx: Context<PausePosition>) -> Result<()> {
        instructions::pause_position::handler(ctx)
    }

    /// Resume monitoring for a paused position
    pub fn resume_position(ctx: Context<ResumePosition>) -> Result<()> {
        instructions::resume_position::handler(ctx)
    }

    /// Close a monitored position
    pub fn close_position(ctx: Context<ClosePosition>) -> Result<()> {
        instructions::close_position::handler(ctx)
    }
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy, PartialEq, Eq)]
pub enum DeFiProtocol {
    Kamino,
    MarginFi,
    Solend,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy, PartialEq, Eq)]
pub enum RebalanceAction {
    CollateralTopUp,
    DebtRepayment,
    CollateralSwap,
    PositionMigration,
    EmergencyUnwind,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct ProtocolConfig {
    pub agent_authority: Pubkey,
    pub default_warn_threshold: u64,      // basis points (e.g., 15000 = 1.5)
    pub default_critical_threshold: u64,   // basis points (e.g., 12000 = 1.2)
    pub max_positions_per_user: u8,
    pub rebalance_fee_bps: u16,
}
