use anchor_lang::prelude::*;
use crate::state::{MonitoredPosition, PositionStatus};
use crate::errors::SolShieldError;

#[derive(Accounts)]
pub struct ResumePosition<'info> {
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

pub fn handler(ctx: Context<ResumePosition>) -> Result<()> {
    let position = &mut ctx.accounts.position;

    require!(
        position.status == PositionStatus::Paused,
        SolShieldError::PositionNotPaused
    );

    position.status = PositionStatus::Active;
    msg!("Position resumed by owner");

    Ok(())
}
