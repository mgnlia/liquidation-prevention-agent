use anchor_lang::prelude::*;
use crate::state::{ProtocolState, MonitoredPosition, PositionStatus};
use crate::errors::SolShieldError;

#[derive(Accounts)]
pub struct UpdateHealth<'info> {
    #[account(
        seeds = [b"protocol-state"],
        bump = protocol_state.bump,
    )]
    pub protocol_state: Account<'info, ProtocolState>,

    #[account(
        mut,
        seeds = [
            b"position",
            position.owner.as_ref(),
            position.obligation_key.as_ref(),
        ],
        bump = position.bump,
    )]
    pub position: Account<'info, MonitoredPosition>,

    /// The agent authority that is authorized to update health
    #[account(
        constraint = agent.key() == protocol_state.agent_authority @ SolShieldError::UnauthorizedAgent
    )]
    pub agent: Signer<'info>,
}

pub fn handler(
    ctx: Context<UpdateHealth>,
    health_factor: u64,
    total_collateral_usd: u64,
    total_debt_usd: u64,
) -> Result<()> {
    require!(health_factor > 0, SolShieldError::InvalidHealthFactor);

    let position = &mut ctx.accounts.position;
    let state = &ctx.accounts.protocol_state;

    require!(
        position.status != PositionStatus::Paused,
        SolShieldError::PositionPaused
    );
    require!(
        position.status != PositionStatus::Closed,
        SolShieldError::PositionClosed
    );

    let clock = Clock::get()?;

    // Update position data
    let old_collateral = position.total_collateral_usd;
    position.health_factor = health_factor;
    position.total_collateral_usd = total_collateral_usd;
    position.total_debt_usd = total_debt_usd;
    position.last_check_ts = clock.unix_timestamp;

    // Update status based on health factor
    if health_factor < position.critical_threshold {
        position.status = PositionStatus::Critical;
        msg!("⚠️ CRITICAL: Health factor {} below critical threshold {}", 
            health_factor, position.critical_threshold);
    } else if health_factor < position.warn_threshold {
        position.status = PositionStatus::Warning;
        msg!("⚡ WARNING: Health factor {} below warn threshold {}", 
            health_factor, position.warn_threshold);
    } else {
        position.status = PositionStatus::Active;
    }

    // Update total value protected in protocol state
    // Note: We'd need a mutable reference for this in production
    msg!("Health updated: {} bps | Collateral: ${} | Debt: ${}", 
        health_factor, total_collateral_usd, total_debt_usd);

    Ok(())
}
