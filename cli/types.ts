import * as anchor from '@project-serum/anchor';
import { PublicKey } from '@solana/web3.js';

export const GLOBAL_AUTHORITY_SEED = "global-authority";
export const AUCTION_SEED = "auction";

export const AUCTION_SIZE = 160;

export interface AuctionPool {
    // 8 + 152
    seller: PublicKey,          // 32
    nftMint: PublicKey,         // 32
    nftCollection: PublicKey,   // 32

    bidder: PublicKey,          // 32
    currentBid: anchor.BN,      // 8

    startPrice: anchor.BN,      // 8
    endTime: anchor.BN,         // 8
    
}
