use anchor_lang::prelude::*;
use crate::state::{ProtocolState, MonitoredPosition, RebalanceRecord, PositionStatus};
use crate::RebalanceAction;
use crate::errors::SolShieldError;

#[derive(Accounts)]
pub struct RecordRebalance<'info> {
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
    )]
    pub position: Account<'info, MonitoredPosition>,

    #[account(
        init,
        payer = agent,
        space = RebalanceRecord::SIZE,
        seeds = [
            b"rebalance",
            position.key().as_ref(),
            &position.rebalance_count.to_le_bytes(),
        ],
        bump,
    )]
    pub rebalance_record: Account<'info, RebalanceRecord>,

    /// The agent authority executing the rebalance
    #[account(
        mut,
        constraint = agent.key() == protocol_state.agent_authority @ SolShieldError::UnauthorizedAgent
    )]
    pub agent: Signer<'info>,

    pub system_program: Program<'info, System>,
}

pub fn handler(
    ctx: Context<RecordRebalance>,
    action_type: RebalanceAction,
    amount: u64,
    tx_signature: [u8; 64],
    ai_reasoning_hash: [u8; 32],
) -> Result<()> {
    let position = &mut ctx.accounts.position;
    let state = &mut ctx.accounts.protocol_state;
    let record = &mut ctx.accounts.rebalance_record;
    let clock = Clock::get()?;

    require!(
        position.status != PositionStatus::Closed,
        SolShieldError::PositionClosed
    );

    // Minimum 60 second cooldown between rebalances
    if position.last_rebalance_ts > 0 {
        require!(
            clock.unix_timestamp - position.last_rebalance_ts >= 60,
            SolShieldError::RebalanceCooldown
        );
    }

    // Record the rebalance
    record.position = position.key();
    record.owner = position.owner;
    record.action_type = action_type;
    record.amount = amount;
    record.health_before = position.health_factor;
    record.health_after = 0; // Will be updated on next health check
    record.tx_signature = tx_signature;
    record.ai_reasoning_hash = ai_reasoning_hash;
    record.timestamp = clock.unix_timestamp;
    record.bump = ctx.bumps.rebalance_record;

    // Update position
    position.rebalance_count = position.rebalance_count.checked_add(1).unwrap();
    position.last_rebalance_ts = clock.unix_timestamp;

    // Update protocol stats
    state.total_rebalances = state.total_rebalances.checked_add(1).unwrap();

    msg!("🔄 Rebalance recorded: action={:?}, amount={}", action_type as u8, amount);
    msg!("AI reasoning hash: {:?}", &ai_reasoning_hash[..8]);
    msg!("TX signature recorded on-chain for verification");

    Ok(())
}
