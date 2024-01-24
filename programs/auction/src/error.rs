use anchor_lang::prelude::*;

#[error_code]
pub enum AuctionError {
    
    // 0x0 ~ 0x13 - 0 ~ 19
    // Please refer this https://github.com/solana-labs/solana-program-library/blob/master/token/program/src/error.rs

    // 0x64 ~ 0x1388 - 100 ~ 5000
    // Please refer this https://github.com/project-serum/anchor/blob/master/lang/src/error.rs

    // 0x1770
    #[msg("Invalid Metadata Address")]
    InvalidMetadata,

    // 0x1771
    #[msg("Can't Parse The NFT's Creators")]
    MetadataCreatorParseError,

    // 0x1772
    #[msg("Duration time must be in 1~14 days.")]
    InvalidDuration,

    // 0x1773
    #[msg("Bid floor must be at least 1 lamport.")]
    InvalidBidFloor,

    // 0x1774
    #[msg("The Auction is already Ended")]
    EndedAuction,

    // 0x1775
    #[msg("Must bid at least 5% over or 10 HTO higher than current Bid.")]
    InsufficientBid,

    // 0x1776
    #[msg("First Bid must be higher than start Price")]
    InsufficientFirstBid,

    // 0x1777
    #[msg("The Out Bidder is not Match with the Auction Data.")]
    OutBidderMismatch,

    // 0x1778
    #[msg("Invalid Claimer - not Seller or Winning Bidder.")]
    InvalidClaimer,

    // 0x1779
    #[msg("The Auction is not Ended yet.")]
    NotEndedAuction,

    // 0x177a
    #[msg("The Winner is Should be the last bidder.")]
    InvalidWinner,

    // 0x177b
    #[msg("The HTO ATA's owner should be the auction creator.")]
    InvalidSeller,

    // 0x177c
    #[msg("The Number of Remaining Accounts is mismatch with the creators.")]
    AccountCountMismatch,

    // 0x177d
    #[msg("Cannot cancel auction if there is a bid.")]
    InvalidCancel

}