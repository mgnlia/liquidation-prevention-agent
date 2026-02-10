use anchor_lang::prelude::*;
use crate::state::{ProtocolState, MonitoredPosition, PositionStatus};
use crate::DeFiProtocol;
use crate::errors::SolShieldError;

#[derive(Accounts)]
#[instruction(protocol: DeFiProtocol, obligation_key: Pubkey)]
pub struct RegisterPosition<'info> {
    #[account(
        mut,
        seeds = [b"protocol-state"],
        bump = protocol_state.bump,
    )]
    pub protocol_state: Account<'info, ProtocolState>,

    #[account(
        init,
        payer = owner,
        space = MonitoredPosition::SIZE,
        seeds = [
            b"position",
            owner.key().as_ref(),
            obligation_key.as_ref(),
        ],
        bump,
    )]
    pub position: Account<'info, MonitoredPosition>,

    #[account(mut)]
    pub owner: Signer<'info>,

    pub system_program: Program<'info, System>,
}

pub fn handler(
    ctx: Context<RegisterPosition>,
    protocol: DeFiProtocol,
    obligation_key: Pubkey,
    warn_threshold: u64,
    critical_threshold: u64,
) -> Result<()> {
    require!(
        warn_threshold > critical_threshold,
        SolShieldError::InvalidThresholds
    );

    let clock = Clock::get()?;
    let position = &mut ctx.accounts.position;
    let state = &mut ctx.accounts.protocol_state;

    position.owner = ctx.accounts.owner.key();
    position.protocol = protocol;
    position.obligation_key = obligation_key;
    position.health_factor = 0; // Will be set on first check
    position.total_collateral_usd = 0;
    position.total_debt_usd = 0;
    position.warn_threshold = warn_threshold;
    position.critical_threshold = critical_threshold;
    position.status = PositionStatus::Active;
    position.rebalance_count = 0;
    position.last_check_ts = 0;
    position.last_rebalance_ts = 0;
    position.created_at = clock.unix_timestamp;
    position.bump = ctx.bumps.position;

    state.total_positions = state.total_positions.checked_add(1).unwrap();

    msg!("Position registered for monitoring");
    msg!("Protocol: {:?}", protocol as u8);
    msg!("Obligation: {}", obligation_key);
    msg!("Warn threshold: {} bps", warn_threshold);

    Ok(())
}
