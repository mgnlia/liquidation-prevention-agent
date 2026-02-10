use anchor_lang::prelude::*;
use crate::state::{MonitoredPosition, PositionStatus};
use crate::errors::SolShieldError;

#[derive(Accounts)]
pub struct PausePosition<'info> {
    #[account(
        mut,
        seeds = [
            b"position",
            position.owner.as_ref(),
            position.obligation_key.as_ref(),
        ],
        bump = position.bump,
        constraint = position.owner == owner.key() @ SolShieldError::UnauthorizedOwner,
    )]
    pub position: Account<'info, MonitoredPosition>,

    pub owner: Signer<'info>,
}

pub fn handler(ctx: Context<PausePosition>) -> Result<()> {
    let position = &mut ctx.accounts.position;

    require!(
        position.status != PositionStatus::Closed,
        SolShieldError::PositionClosed
    );
    require!(
        position.status != PositionStatus::Paused,
        SolShieldError::PositionPaused
    );

    position.status = PositionStatus::Paused;
    msg!("Position paused by owner");

    Ok(())
}
