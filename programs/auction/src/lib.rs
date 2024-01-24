use anchor_lang::prelude::*;
use anchor_lang::solana_program::{system_program, sysvar};
use anchor_spl::token::{self, Mint, Token, TokenAccount, Transfer};
use mpl_token_metadata::state::{Creator, Metadata, TokenMetadataAccount};
use solana_program::log::sol_log_compute_units;
use solana_program::program::invoke_signed;

pub mod account;
pub mod error;
pub mod utils;

use account::*;
use error::*;
use utils::*;

declare_id!("6VwSgSesAeqqSw3uXsU8BGMxMAqSzFVQxPPUDUVX8Qw4");

#[program]
pub mod auction {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, _global_bump: u8) -> Result<()> {
        let global_authority = &mut ctx.accounts.global_authority;
        global_authority.super_admin = ctx.accounts.admin.key();

        Ok(())
    }

    pub fn create_auction(
        ctx: Context<CreateAuction>,
        start_price: u64,
        duration: u64,
    ) -> Result<()> {
        let mut auction = ctx.accounts.auction.load_init()?;
        let auction_ata = &ctx.accounts.auction_ata;
        let owner = &ctx.accounts.owner;
        let owner_ata = &ctx.accounts.owner_ata;
        let mint = &ctx.accounts.mint;
        let token_program = &ctx.accounts.token_program;
        let ata_program = &ctx.accounts.ata_program;
        let system_program = &ctx.accounts.system_program;
        let rent_sysvar = &ctx.accounts.rent_sysvar;

        let mint_metadata = &mut &ctx.accounts.mint_metadata;

        let (metadata, _) = Pubkey::find_program_address(
            &[
                mpl_token_metadata::state::PREFIX.as_bytes(),
                mpl_token_metadata::id().as_ref(),
                mint.key().as_ref(),
            ],
            &mpl_token_metadata::id(),
        );

        if metadata != mint_metadata.key() {
            return Err(error!(AuctionError::InvalidMetadata));
        }
        // verify metadata is legit
        let nft_metadata = Metadata::from_account_info(mint_metadata)?;

        let mut _collection: Pubkey = Pubkey::default();

        if let Some(collection) = nft_metadata.collection {
            if collection.verified {
                _collection = collection.key;
            }
        }

        if _collection == Pubkey::default() {
            if let Some(creators) = nft_metadata.data.creators {
                for i in 0..creators.len() {
                    if creators[i].verified {
                        _collection = creators[i].address;
                        break;
                    }
                }
            }
        }

        if _collection == Pubkey::default() {
            return Err(error!(AuctionError::MetadataCreatorParseError));
        }

        msg!("Collection= {:?}", _collection);

        let cur_time: u64 = Clock::get()?.unix_timestamp as u64;

        if duration < DAY || duration > 14 * DAY {
            return Err(error!(AuctionError::InvalidDuration));
        }

        if start_price <= 0 {
            return Err(error!(AuctionError::InvalidBidFloor));
        }

        auction.seller = *owner.key;
        auction.nft_mint = mint.key();
        auction.nft_collection = _collection;

        auction.end_time = cur_time + duration;
        auction.start_price = start_price;

        auction.bidder = Pubkey::default();
        auction.current_bid = 0;

        if auction_ata.to_account_info().data_is_empty() {
            create_ata(
                owner.to_account_info(),
                ctx.accounts.global_authority.to_account_info(),
                mint.to_account_info(),
                auction_ata.to_account_info(),
                token_program.to_account_info(),
                ata_program.to_account_info(),
                system_program.to_account_info(),
                rent_sysvar.to_account_info(),
            )?;
        } else {
            // TODO: what happens if we get here?
        }
        transfer_spl(
            owner.to_account_info(),
            owner_ata.to_account_info(),
            auction_ata.to_account_info(),
            1,
            token_program.to_account_info(),
            &[],
        )?;

        Ok(())
    }

    /**
     * @dev Cancel Auction
     * In this function the owner of the auction can cancel his auction
     */
    pub fn cancel_auction(ctx: Context<CancelAuction>, bump: u8) -> Result<()> {
        let auction = ctx.accounts.auction.load_mut()?;

        if auction.current_bid != 0 {
            return Err(error!(AuctionError::InvalidCancel));
        }
        if auction.seller != ctx.accounts.seller.key() {
            return Err(error!(AuctionError::InvalidCancel));
        }

        // Transfer Back nft to the seller
        transfer_spl(
            ctx.accounts.global_authority.to_account_info(),
            ctx.accounts.auction_ata.to_account_info(),
            ctx.accounts.owner_ata.to_account_info(),
            1,
            ctx.accounts.token_program.to_account_info(),
            &[&[GLOBAL_AUTHORITY_SEED.as_bytes(), &[bump]]],
        )?;

        // Close the auction PDA
        let owner = &mut ctx.accounts.seller;
        let origin_lamports: u64 = owner.lamports();
        **owner.lamports.borrow_mut() = origin_lamports + ctx.accounts.auction.as_ref().lamports();
        **ctx.accounts.auction.as_ref().lamports.borrow_mut() = 0;

        Ok(())
    }

    /**
     * @dev Uers can palce bid for the auction with this function
     * In this function, users can place bid by HTO amount
     */
    pub fn place_bid(ctx: Context<PlaceBid>, bid: u64, bump: u8) -> Result<()> {
        let mut auction_data_info = ctx.accounts.auction.load_mut()?;
        let timestamp: u64 = Clock::get()?.unix_timestamp as u64;
        msg!("Place Date: {}", timestamp);

        if auction_data_info.current_bid == 0 && auction_data_info.start_price > bid {
            return Err(error!(AuctionError::InsufficientFirstBid));
        }

        // Assert Auction Already Ended
        if auction_data_info.end_time < timestamp {
            return Err(error!(AuctionError::EndedAuction));
        }

        // New Bid should be increased more than min_increase_amount
        if auction_data_info.current_bid + MIN_INCREMENT > bid
            || auction_data_info.current_bid * (1 + MIN_INCREMENT_PERCENT / 100) > bid
        {
            return Err(error!(AuctionError::InsufficientBid));
        }

        // Assert OutBidder Address with the Last Bidder
        if Pubkey::default() != auction_data_info.bidder
            && ctx.accounts.out_bidder.key() != auction_data_info.bidder
        {
            return Err(error!(AuctionError::OutBidderMismatch));
        }

        // Sets auction to run for 10 mins if the bidder bids in last 10 mins
        if auction_data_info.end_time - MIN_DURATION_AFTER_BID_SECS < timestamp {
            auction_data_info.end_time = timestamp + MIN_DURATION_AFTER_BID_SECS;
        }

        // Refund Last Bidder Escrow
        if !Pubkey::default().eq(&auction_data_info.bidder) {
            transfer_spl(
                ctx.accounts.global_authority.to_account_info(),
                ctx.accounts.auction_vault.to_account_info(),
                ctx.accounts.out_bidder_account.to_account_info(),
                auction_data_info.current_bid,
                ctx.accounts.token_program.to_account_info(),
                &[&[GLOBAL_AUTHORITY_SEED.as_bytes(), &[bump]]],
            )?;
        }

        // Escrow New Bidder funds
        transfer_spl(
            ctx.accounts.bidder.to_account_info(),
            ctx.accounts.new_bidder_account.to_account_info(),
            ctx.accounts.auction_vault.to_account_info(),
            bid,
            ctx.accounts.token_program.to_account_info(),
            &[],
        )?;

        auction_data_info.bidder = ctx.accounts.bidder.key();
        auction_data_info.current_bid = bid;

        Ok(())
    }

    pub fn claim_auction<'info>(
        ctx: Context<'_, '_, '_, 'info, ClaimAuction<'info>>,
        bump: u8,
    ) -> Result<()> {
        let auction_data_info = ctx.accounts.auction.load_mut()?;
        let timestamp: u64 = Clock::get()?.unix_timestamp as u64;

        // The claimer should be Last bidder or Seller
        if ctx.accounts.claimer.key() != auction_data_info.bidder
            && ctx.accounts.claimer.key() != auction_data_info.seller
        {
            return Err(error!(AuctionError::InvalidClaimer));
        }

        // The auction should be ended before
        if timestamp < auction_data_info.end_time {
            return Err(error!(AuctionError::NotEndedAuction));
        }

        // Winner ATA's owner should be the last bidder
        // The NFT should be sent to the winner's wallet so this check is necessary
        if ctx.accounts.winner_ata.owner != auction_data_info.bidder {
            return Err(error!(AuctionError::InvalidWinner));
        }

        // Seller ATA's owner should be the auction creator
        // The HTO token should be sent to the auction creator so this check is necessary
        if ctx.accounts.seller_ata.owner != auction_data_info.seller {
            return Err(error!(AuctionError::InvalidSeller));
        }

        // Get Collection address from Metadata
        let mint_metadata = &mut &ctx.accounts.mint_metadata;
        msg!("Metadata Account: {:?}", ctx.accounts.mint_metadata.key());
        let (metadata, _) = Pubkey::find_program_address(
            &[
                mpl_token_metadata::state::PREFIX.as_bytes(),
                mpl_token_metadata::id().as_ref(),
                ctx.accounts.nft_mint.key().as_ref(),
            ],
            &mpl_token_metadata::id(),
        );

        if metadata != mint_metadata.key() {
            return Err(error!(AuctionError::InvalidMetadata));
        }

        // verify metadata is legit
        let nft_metadata = Metadata::from_account_info(mint_metadata)?;

        let creators: &Vec<Creator>;
        if let Some(crts) = &nft_metadata.data.creators {
            creators = crts;
        } else {
            return Err(error!(AuctionError::MetadataCreatorParseError));
        };

        // Share Fee to distribute to creators
        let total_share_fee = auction_data_info.current_bid
            * (nft_metadata.data.seller_fee_basis_points as u64)
            / PERMYRIAD;

        // Auction Fee to VAULT_WALLET
        let auction_fee = auction_data_info.current_bid * FEE_PERCENT / 100;

        let token_program = &mut &ctx.accounts.token_program;
        let seeds = &[GLOBAL_AUTHORITY_SEED.as_bytes(), &[bump]];
        let signer = &[&seeds[..]];

        // Get remaining Accounts
        let remaining_accounts: Vec<AccountInfo> = ctx.remaining_accounts.to_vec();
        msg!(
            "SC creators: {:?} Remaining Accouts {:?}",
            creators.len(),
            remaining_accounts.len()
        );
        if creators.len() != remaining_accounts.len() {
            return Err(error!(AuctionError::AccountCountMismatch));
        }
        for i in 0..remaining_accounts.len() {
            let creator_ata = spl_associated_token_account::get_associated_token_address(
                &creators[i].address,
                &HTO_TOKEN_MINT.parse::<Pubkey>().unwrap(),
            );
            if creator_ata == remaining_accounts[i].key() && creators[i].share != 0 {
                let share_amount: u64 = total_share_fee * (creators[i].share as u64) / 100;
                msg!("Share Amount: {:?}", share_amount);
                // Distribute HTO to the Creator's wallets
                let cpi_accounts = Transfer {
                    from: ctx.accounts.auction_vault.to_account_info().clone(),
                    to: remaining_accounts[i].clone(),
                    authority: ctx.accounts.global_authority.to_account_info(),
                };
                token::transfer(
                    CpiContext::new_with_signer(
                        token_program.clone().to_account_info(),
                        cpi_accounts,
                        signer,
                    ),
                    share_amount,
                )?;
                continue;
            }
            sol_log_compute_units();
        }

        msg!("Auction Fee : {:?}", auction_fee);
        // Transfer HTO to the HL address as fee: 2%
        let cpi_accounts = Transfer {
            from: ctx.accounts.auction_vault.to_account_info().clone(),
            to: ctx.accounts.hl_vault.to_account_info().clone(),
            authority: ctx.accounts.global_authority.to_account_info(),
        };
        token::transfer(
            CpiContext::new_with_signer(
                token_program.clone().to_account_info(),
                cpi_accounts,
                signer,
            ),
            auction_fee,
        )?;
        sol_log_compute_units();

        msg!(
            "HTO to Seller : {:?}",
            auction_data_info.current_bid - total_share_fee - auction_fee
        );
        // Transfer HTO to the seller 100% - HL fee (2%) - royalties
        let cpi_accounts = Transfer {
            from: ctx.accounts.auction_vault.to_account_info().clone(),
            to: ctx.accounts.seller_ata.to_account_info().clone(),
            authority: ctx.accounts.global_authority.to_account_info().clone(),
        };
        token::transfer(
            CpiContext::new_with_signer(
                token_program.clone().to_account_info(),
                cpi_accounts,
                signer,
            ),
            auction_data_info.current_bid - total_share_fee - auction_fee,
        )?;
        sol_log_compute_units();
        // Close HTO account of the auction PDA
        invoke_signed(
            &spl_token::instruction::close_account(
                token_program.key,
                &ctx.accounts.auction_vault.key(),
                ctx.accounts.claimer.key,
                &ctx.accounts.global_authority.key(),
                &[],
            )?,
            &[
                token_program.clone().to_account_info(),
                ctx.accounts.auction_vault.to_account_info().clone(),
                ctx.accounts.claimer.to_account_info().clone(),
                ctx.accounts.global_authority.to_account_info().clone(),
            ],
            &[&[GLOBAL_AUTHORITY_SEED.as_bytes(), &[bump]]],
        )?;

        // Transfer NFT to the winner
        let cpi_accounts = Transfer {
            from: ctx.accounts.auction_ata.to_account_info().clone(),
            to: ctx.accounts.winner_ata.to_account_info().clone(),
            authority: ctx.accounts.global_authority.to_account_info().clone(),
        };
        token::transfer(
            CpiContext::new_with_signer(
                token_program.clone().to_account_info(),
                cpi_accounts,
                signer,
            ),
            1,
        )?;
        sol_log_compute_units();
        // Close NFT account of the auction PDA
        invoke_signed(
            &spl_token::instruction::close_account(
                token_program.key,
                &ctx.accounts.auction_ata.key(),
                ctx.accounts.claimer.key,
                &ctx.accounts.global_authority.key(),
                &[],
            )?,
            &[
                token_program.clone().to_account_info(),
                ctx.accounts.auction_ata.to_account_info().clone(),
                ctx.accounts.claimer.to_account_info().clone(),
                ctx.accounts.global_authority.to_account_info().clone(),
            ],
            &[&[GLOBAL_AUTHORITY_SEED.as_bytes(), &[bump]]],
        )?;
        sol_log_compute_units();

        // Close the auction PDA
        let owner = &mut ctx.accounts.claimer;
        let origin_lamports: u64 = owner.lamports();
        **owner.lamports.borrow_mut() = origin_lamports + ctx.accounts.auction.as_ref().lamports();
        **ctx.accounts.auction.as_ref().lamports.borrow_mut() = 0;

        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(mut)]
    pub admin: Signer<'info>,
    #[account(
        init,
        seeds = [GLOBAL_AUTHORITY_SEED.as_ref()],
        bump,
        space = 8 + 32,
        payer = admin
    )]
    pub global_authority: Account<'info, GlobalPool>,

    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct CreateAuction<'info> {
    // Main Auction PDA to store the data
    #[account(zero)]
    pub auction: AccountLoader<'info, AuctionPool>,

    #[account(
        mut,
        seeds = [GLOBAL_AUTHORITY_SEED.as_ref()],
        bump,
    )]
    pub global_authority: Account<'info, GlobalPool>,

    // The NFT's Auction ATA
    #[account(mut)]
    /// CHECK: This is not dangerous because we don't read or write from this account
    pub auction_ata: AccountInfo<'info>,

    // The auction creator
    #[account(mut)]
    pub owner: Signer<'info>,

    // The NFT's owner ATA
    #[account(
        mut,
        constraint = owner_ata.mint == *mint.to_account_info().key,
        constraint = owner_ata.owner == *owner.key,
    )]
    pub owner_ata: Account<'info, TokenAccount>,

    // The NFT mint address
    pub mint: Account<'info, Mint>,

    #[account(
        mut,
        constraint = mint_metadata.owner == &mpl_token_metadata::ID
    )]
    /// CHECK: This is not dangerous because we don't read or write from this account
    pub mint_metadata: AccountInfo<'info>,

    #[account(address = spl_associated_token_account::ID)]
    /// CHECK: This is not dangerous because we don't read or write from this account
    pub ata_program: AccountInfo<'info>,

    #[account(address = anchor_spl::token::ID)]
    pub token_program: Program<'info, Token>,

    #[account(address = system_program::ID)]
    pub system_program: Program<'info, System>,

    #[account(address = sysvar::rent::ID)]
    pub rent_sysvar: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct CancelAuction<'info> {
    #[account(mut)]
    pub auction: AccountLoader<'info, AuctionPool>,

    // The NFT's Auction ATA
    #[account(mut)]
    /// CHECK: This is not dangerous because we don't read or write from this account
    pub owner_ata: AccountInfo<'info>,

    #[account(
        mut,
        seeds = [GLOBAL_AUTHORITY_SEED.as_ref()],
        bump,
    )]
    pub global_authority: Account<'info, GlobalPool>,

    // The NFT's owner ATA
    #[account(
        mut,
        constraint = auction_ata.mint == *nft_mint.to_account_info().key,
        constraint = auction_ata.owner == *global_authority.to_account_info().key
    )]
    pub auction_ata: Account<'info, TokenAccount>,

    // The NFT mint address
    pub nft_mint: Account<'info, Mint>,

    // The seller address who created auction
    #[account(mut)]
    pub seller: Signer<'info>,

    #[account(address = anchor_spl::token::ID)]
    pub token_program: Program<'info, Token>,
}

#[derive(Accounts)]
pub struct PlaceBid<'info> {
    #[account(mut)]
    pub bidder: Signer<'info>,

    #[account(mut)]
    pub auction: AccountLoader<'info, AuctionPool>,

    #[account(
        mut,
        seeds = [GLOBAL_AUTHORITY_SEED.as_ref()],
        bump,
    )]
    pub global_authority: Account<'info, GlobalPool>,

    // The Auction's HTO token ATA to store them
    #[account(
        mut,
        constraint = auction_vault.mint == HTO_TOKEN_MINT.parse::<Pubkey>().unwrap(),
        constraint = auction_vault.owner == *global_authority.to_account_info().key
    )]
    pub auction_vault: Account<'info, TokenAccount>,

    // The Out_bidder's HTO token ATA
    #[account(
        mut,
        constraint = out_bidder_account.mint == HTO_TOKEN_MINT.parse::<Pubkey>().unwrap(),
        constraint = out_bidder_account.owner == *out_bidder.to_account_info().key
    )]
    pub out_bidder_account: Account<'info, TokenAccount>,

    #[account(mut)]
    /// CHECK: This is not dangerous because we don't read or write from this account
    pub out_bidder: SystemAccount<'info>,

    // The Auction's HTO token ATA to store them
    #[account(
        mut,
        constraint = new_bidder_account.mint == HTO_TOKEN_MINT.parse::<Pubkey>().unwrap(),
        constraint = new_bidder_account.owner == *bidder.to_account_info().key
    )]
    pub new_bidder_account: Account<'info, TokenAccount>,

    #[account(address = anchor_spl::token::ID)]
    pub token_program: Program<'info, Token>,
}

#[derive(Accounts)]
pub struct ClaimAuction<'info> {
    #[account(mut)]
    pub claimer: Signer<'info>,

    #[account(mut)]
    pub auction: AccountLoader<'info, AuctionPool>,

    #[account(
        mut,
        seeds = [GLOBAL_AUTHORITY_SEED.as_ref()],
        bump,
    )]
    pub global_authority: Account<'info, GlobalPool>,

    // The NFT's owner ATA
    #[account(
        mut,
        constraint = auction_ata.mint == *nft_mint.to_account_info().key,
        constraint = auction_ata.owner == *global_authority.to_account_info().key
    )]
    pub auction_ata: Box<Account<'info, TokenAccount>>,

    // The Auction's HTO token ATA to store them
    #[account(
        mut,
        constraint = auction_vault.mint == HTO_TOKEN_MINT.parse::<Pubkey>().unwrap(),
        constraint = auction_vault.owner == *global_authority.to_account_info().key
    )]
    pub auction_vault: Box<Account<'info, TokenAccount>>,

    // The VAULT_WALLET's HTO token ATA to store them
    #[account(
        mut,
        constraint = hl_vault.mint == HTO_TOKEN_MINT.parse::<Pubkey>().unwrap(),
        constraint = hl_vault.owner == VAULT_WALLET.parse::<Pubkey>().unwrap()
    )]
    pub hl_vault: Box<Account<'info, TokenAccount>>,

    // The NFT mint address
    pub nft_mint: Box<Account<'info, Mint>>,

    // The NFT's winner ATA
    #[account(
        mut,
        constraint = winner_ata.mint == *nft_mint.to_account_info().key,
    )]
    pub winner_ata: Box<Account<'info, TokenAccount>>,

    // The Creator's HTO token ATA
    #[account(
        mut,
        constraint = seller_ata.mint == HTO_TOKEN_MINT.parse::<Pubkey>().unwrap(),
    )]
    pub seller_ata: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        constraint = mint_metadata.owner == &mpl_token_metadata::ID
    )]
    /// CHECK: This is not dangerous because we don't read or write from this account
    pub mint_metadata: AccountInfo<'info>,

    #[account(address = anchor_spl::token::ID)]
    pub token_program: Program<'info, Token>,
}
