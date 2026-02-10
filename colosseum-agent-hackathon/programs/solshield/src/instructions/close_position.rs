use anchor_lang::prelude::*;
use crate::state::{ProtocolState, MonitoredPosition, PositionStatus};
use crate::errors::SolShieldError;

#[derive(Accounts)]
pub struct ClosePosition<'info> {
    #[account(
        mut,
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
        constraint = position.owner == owner.key() @ SolShieldError::UnauthorizedOwner,
        close = owner,
    )]
    pub position: Account<'info, MonitoredPosition>,

    #[account(mut)]
    pub owner: Signer<'info>,
}

pub fn handler(ctx: Context<ClosePosition>) -> Result<()> {
    let state = &mut ctx.accounts.protocol_state;

    // Position account will be closed and rent returned to owner
    // via the `close = owner` constraint above
    state.total_positions = state.total_positions.saturating_sub(1);

    msg!("Position closed, rent returned to owner");

    Ok(())
}
