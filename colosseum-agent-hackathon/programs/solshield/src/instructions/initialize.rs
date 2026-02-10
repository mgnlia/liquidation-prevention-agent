use anchor_lang::prelude::*;
use crate::state::ProtocolState;
use crate::ProtocolConfig;
use crate::errors::SolShieldError;

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = authority,
        space = ProtocolState::SIZE,
        seeds = [b"protocol-state"],
        bump,
    )]
    pub protocol_state: Account<'info, ProtocolState>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}

pub fn handler(ctx: Context<Initialize>, config: ProtocolConfig) -> Result<()> {
    require!(
        config.default_warn_threshold > config.default_critical_threshold,
        SolShieldError::InvalidThresholds
    );

    let state = &mut ctx.accounts.protocol_state;
    state.authority = ctx.accounts.authority.key();
    state.agent_authority = config.agent_authority;
    state.default_warn_threshold = config.default_warn_threshold;
    state.default_critical_threshold = config.default_critical_threshold;
    state.max_positions_per_user = config.max_positions_per_user;
    state.rebalance_fee_bps = config.rebalance_fee_bps;
    state.total_positions = 0;
    state.total_rebalances = 0;
    state.total_value_protected = 0;
    state.bump = ctx.bumps.protocol_state;

    msg!("SolShield protocol initialized");
    msg!("Agent authority: {}", config.agent_authority);
    msg!("Warn threshold: {} bps", config.default_warn_threshold);
    msg!("Critical threshold: {} bps", config.default_critical_threshold);

    Ok(())
}
