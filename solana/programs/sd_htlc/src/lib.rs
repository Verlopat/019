use anchor_lang::prelude::*;

declare_id!("SDHTLC111111111111111111111111111111111111");

#[program]
pub mod sd_htlc {
    use super::*;
    pub fn initialize_swap(ctx: Context<InitializeSwap>, swap_id:[u8;32], secret_hash:[u8;32], policy_hash:[u8;32], expiry:i64) -> Result<()> {
        let s=&mut ctx.accounts.swap; s.swap_id=swap_id; s.secret_hash=secret_hash; s.policy_hash=policy_hash; s.expiry=expiry; s.state=0; Ok(())
    }
    pub fn submit_compliance(ctx: Context<MutateSwap>, pass:bool) -> Result<()> { ctx.accounts.swap.compliance=pass; ctx.accounts.swap.state=if pass{1}else{3}; Ok(()) }
    pub fn claim(ctx: Context<MutateSwap>, secret:[u8;32]) -> Result<()> { require!(ctx.accounts.swap.state==1,ErrorCode::NotLocked); require!(Clock::get()?.unix_timestamp<ctx.accounts.swap.expiry,ErrorCode::Expired); require!(ctx.accounts.swap.secret_hash==solana_program::hash::hash(&secret).to_bytes(),ErrorCode::BadSecret); ctx.accounts.swap.state=2; Ok(()) }
    pub fn refund(ctx: Context<MutateSwap>) -> Result<()> { require!(Clock::get()?.unix_timestamp>=ctx.accounts.swap.expiry || ctx.accounts.swap.state==3,ErrorCode::NotRefundable); ctx.accounts.swap.state=4; Ok(()) }
}
#[derive(Accounts)] pub struct InitializeSwap<'info>{ #[account(init,payer=payer,space=8+32+32+32+8+1+1)] pub swap:Account<'info,Swap>, #[account(mut)] pub payer:Signer<'info>, pub system_program:Program<'info,System> }
#[derive(Accounts)] pub struct MutateSwap<'info>{ #[account(mut)] pub swap:Account<'info,Swap> }
#[account] pub struct Swap{pub swap_id:[u8;32],pub secret_hash:[u8;32],pub policy_hash:[u8;32],pub expiry:i64,pub state:u8,pub compliance:bool}
#[error_code] pub enum ErrorCode{#[msg("Not locked")] NotLocked,#[msg("Expired")] Expired,#[msg("Bad secret")] BadSecret,#[msg("Not refundable")] NotRefundable}
