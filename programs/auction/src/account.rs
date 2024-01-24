use anchor_lang::prelude::*;

#[account]
#[derive(Default)]
pub struct GlobalPool {
    // 8 + 32
    pub super_admin: Pubkey,     // 32
}

#[account(zero_copy)]
pub struct AuctionPool {
    
    pub seller: Pubkey,         // 32
    pub nft_mint: Pubkey,       // 32
    pub nft_collection: Pubkey, // 32

    pub bidder: Pubkey,         // 32
    pub current_bid: u64,       // 8
    
    pub start_price: u64,       // 8
    pub end_time: u64,          // 8

}

impl Default for AuctionPool {
    #[inline]
    fn default() -> AuctionPool {
        AuctionPool {
            seller: Pubkey::default(),

            nft_mint: Pubkey::default(),
            nft_collection: Pubkey::default(),

            bidder: Pubkey::default(),
            current_bid: 0,

            start_price: 0,
            end_time: 0,
        }
    }
}