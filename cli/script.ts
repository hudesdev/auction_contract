import { Program, web3 } from '@project-serum/anchor';
import * as anchor from '@project-serum/anchor';
import { TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID} from '@solana/spl-token';
import fs from 'fs';
import NodeWallet from '@project-serum/anchor/dist/cjs/nodewallet';

import { IDL as AuctionIDL } from "../target/types/auction";
import {
    Keypair,
    PublicKey,
    SystemProgram,
    SYSVAR_RENT_PUBKEY,
    Transaction,
    ParsedAccountData
} from '@solana/web3.js';
import {
    AuctionPool,
    AUCTION_SIZE,
    GLOBAL_AUTHORITY_SEED,
} from './types';
import {
    getAssociatedTokenAccount,
    getATokenAccountsNeedCreate,
    getNFTTokenAccount,
    getOwnerOfNFT,
    getMetadata,
    isExistAccount,
} from './utils';
import { programs } from "@metaplex/js";
import { AnchorWallet } from 'solana-vue-wallets';
import * as log from 'loglevel';
import { auction } from '@metaplex/js/lib/programs';

const TAG = '[AUCTION]';

let auctionProgram: Program = null;
let auctionProvider: anchor.Provider = null;
let auctionSolConnection: web3.Connection = null;
let auctionProgramID: PublicKey = null;

let vaultWallet: PublicKey = null;
let htoTokenMint: PublicKey = null;
let htoTokenDecimals: number = null;

export const getWalletKeypair = (keypair: string) => {
    const walletKeypair = Keypair.fromSecretKey(Uint8Array.from(JSON.parse(fs.readFileSync(keypair, 'utf-8'))), {
        skipValidation: true,
    });

    return new NodeWallet(walletKeypair);
};


export const setLoggerMode = (enabled: boolean) => {
    if (enabled) {
        log.enableAll();
    } else {
        log.disableAll();
    }
};


export const setClusterConfig = async (cluster: web3.Cluster, wallet: NodeWallet | AnchorWallet, rpc?: string) => {
    if (!rpc) {
        auctionSolConnection = new web3.Connection(web3.clusterApiUrl(cluster));
    } else {
        auctionSolConnection = new web3.Connection(rpc);
    }

    // Configure the client to use the local cluster.
    anchor.setProvider(
        new anchor.AnchorProvider(auctionSolConnection, wallet as any, {
            skipPreflight: true,
            commitment: 'confirmed',
        })
    );
    auctionProvider = anchor.getProvider();
    if (cluster === 'devnet') {
        auctionProgramID = new PublicKey('6VwSgSesAeqqSw3uXsU8BGMxMAqSzFVQxPPUDUVX8Qw4');
        vaultWallet = new anchor.web3.PublicKey('J1CHG5pAMT4GRprmLwuQ4JzTcjJxTuXD2nsZDqp7924x');
        htoTokenMint = new PublicKey('htoHLBJV1err8xP5oxyQdV2PLQhtVjxLXpKB7FsgJQD');
        htoTokenDecimals = 1_000_000_000;
    } else if (cluster === 'mainnet-beta') {
        // TODO
        auctionProgramID = new PublicKey('BekxgfTSzdzQ2yNV3zSZYqifM3XWmUb4i976hKExtRib');
        vaultWallet = new anchor.web3.PublicKey('J1CHG5pAMT4GRprmLwuQ4JzTcjJxTuXD2nsZDqp7924x');
        htoTokenMint = new PublicKey('htoHLBJV1err8xP5oxyQdV2PLQhtVjxLXpKB7FsgJQD');
        htoTokenDecimals = 1_000_000_000;
    }
    
    log.debug(TAG, '[setClusterConfig]', 'Cluster:', cluster);
    log.debug(TAG, '[setClusterConfig]', 'Wallet address:', wallet.publicKey.toBase58());
    
    // Generate the program client from IDL.
    auctionProgram = new anchor.Program(AuctionIDL as anchor.Idl, auctionProgramID);
    
    log.debug(TAG, '[setClusterConfig]', 'Program ID:', auctionProgram.programId.toBase58());
};


export const initialize = async (wallet: NodeWallet) => {
    const tx = await createInitializeTx(auctionProvider.publicKey);
    // const sendla = await auctionProvider.send(tx, []);
    // cosnt txId = await auctionProvider.simulate(tx, [],)
    tx.feePayer = auctionProvider.publicKey;
    tx.recentBlockhash = (await auctionSolConnection.getLatestBlockhash()).blockhash;

    try {
        const signedTx = await wallet.signTransaction(tx);
        const send = await auctionSolConnection.sendRawTransaction(signedTx.serialize());
        const txId = await auctionSolConnection.confirmTransaction(send, "confirmed");

        // const txId = await auctionProvider.sendAndConfirm(tx, [], {commitment: "confirmed"});
        log.info(TAG, '[initialize]', 'txHash:', txId);
    } catch (e) {
        console.log(e);
    }
}

export const createAuction = async (mint: PublicKey, startPrice: number, duration: number) => {
    const tx = await createAuctionTx(auctionProvider.publicKey, mint, startPrice, duration);
    const txId = await auctionProvider.sendAndConfirm(tx, [], {commitment: "confirmed"});
    log.info(TAG, '[createAuction]', 'txHash:', txId);
}

export const cancelAuction = async (auctionPDA: PublicKey) => {
    const tx = await createAuctionCancelTx(auctionProvider.publicKey, auctionPDA);
    const txId = await auctionProvider.sendAndConfirm(tx, [], {commitment: "confirmed"});
    log.info(TAG, '[cancelAuction]', 'txHash:', txId);
}

export const placeBid = async (auctionPDA: PublicKey, bid: number) => {
    const tx = await createPlaceBidTx(auctionProvider.publicKey, auctionPDA, bid);
    const txId = await auctionProvider.sendAndConfirm(tx, [], {commitment: "confirmed"});
    log.info(TAG, '[placeBid]', 'txHash:', txId);
}

export const claimAuction = async (auctionPDA: PublicKey) => {
    const tx = await createAuctionClaimTx(auctionProvider.publicKey, auctionPDA);
    const txId = await auctionProvider.sendAndConfirm(tx, [], {commitment: "confirmed"});
    log.info(TAG, '[claimAuction]', 'txHash:', txId);
}

/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
////////// create TX
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

export const createInitializeTx = async (userAddress: PublicKey) => {
    const [globalAuthority, bump] = await PublicKey.findProgramAddress(
        [Buffer.from(GLOBAL_AUTHORITY_SEED)],
        auctionProgramID,
    );
    
    let tx = new Transaction();

    tx.add(auctionProgram.instruction.initialize(
        bump, {
        accounts: {
            admin: userAddress,
            globalAuthority,
            systemProgram: SystemProgram.programId,
            rent: SYSVAR_RENT_PUBKEY,
        },
        instructions: [],
        signers: [],
    }));

    return tx;
}


export const createAuctionTx = async (userAddress: PublicKey, mint: PublicKey, startPrice: number, duration: number) => {
    const [globalAuthority, bump] = await PublicKey.findProgramAddress(
        [Buffer.from(GLOBAL_AUTHORITY_SEED)],
        auctionProgramID,
    );

    let d = new Date();
    let curTime = Math.floor(d.getTime()/1000);

    let str = "auction" + curTime.toString();
    log.debug(TAG, '[createAuctionTx]', 'seed string', str);
    
    let auctionPDA = await anchor.web3.PublicKey.createWithSeed(
        userAddress,
        str,
        auctionProgramID,
    );

    let ix = SystemProgram.createAccountWithSeed({
        fromPubkey: userAddress,
        basePubkey: userAddress,
        seed: str,
        newAccountPubkey: auctionPDA,
        lamports: await auctionSolConnection.getMinimumBalanceForRentExemption(AUCTION_SIZE),
        space: AUCTION_SIZE,
        programId: auctionProgramID,
    });

    log.debug(TAG, '[createAuctionTx]', 'auctionPDA', auctionPDA.toBase58);
    let auctionAta = await getAssociatedTokenAccount(globalAuthority, mint);

    let userTokenAccount = await getAssociatedTokenAccount(userAddress, mint);
    if (!await isExistAccount(userTokenAccount, auctionSolConnection)) {
        let accountOfNFT = await getNFTTokenAccount(mint, auctionSolConnection);
        if (userTokenAccount.toBase58() != accountOfNFT.toBase58()) {
            let nftOwner = await getOwnerOfNFT(mint, auctionSolConnection);
            if (nftOwner.toBase58() == userAddress.toBase58()) userTokenAccount = accountOfNFT;
        }
    }

    let mintMetadata = await getMetadata(mint);

    let tx = new Transaction();

    tx.add(ix);
    tx.add(auctionProgram.instruction.createAuction(
        new anchor.BN(startPrice * htoTokenDecimals), new anchor.BN(duration), {
        accounts: {
            auction: auctionPDA,
            globalAuthority,
            auctionAta,
            owner: userAddress,
            ownerAta: userTokenAccount,
            mint,
            mintMetadata,
            ataProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
            tokenProgram: TOKEN_PROGRAM_ID,
            systemProgram: SystemProgram.programId,
            rentSysvar: SYSVAR_RENT_PUBKEY,
        },
        instructions: [],
        signers: [],
    }));

    log.info(TAG, '[createAuction]', 'auction:', auctionPDA.toBase58());

    return tx;
}

export const createAuctionCancelTx = async (userAddress: PublicKey, auctionPDA: PublicKey) => {
    let auctionState = await getAuctionState(auctionPDA);
    let nftMint = auctionState.nftMint;

    const [globalAuthority, bump] = await PublicKey.findProgramAddress(
        [Buffer.from(GLOBAL_AUTHORITY_SEED)],
        auctionProgramID,
    );

    let auctionAta = await getAssociatedTokenAccount(globalAuthority, nftMint);

    let { instructions, destinationAccounts } = await getATokenAccountsNeedCreate(
        auctionSolConnection,
        userAddress,
        userAddress,
        [nftMint]
    );

    let tx = new Transaction();
    if (instructions.length > 0) instructions.map((ix) => tx.add(ix));
    tx.add(auctionProgram.instruction.cancelAuction(
        bump, 
        {
            accounts: {
                auction: auctionPDA,
                ownerAta: destinationAccounts[0],
                globalAuthority,
                auctionAta,
                nftMint,
                seller: userAddress,
                tokenProgram: TOKEN_PROGRAM_ID,
            },
            instructions: [],
            signers: []
        }
    ));

    return tx;
}


export const createPlaceBidTx = async (userAddress: PublicKey, auctionPDA: PublicKey, bid: number) => {
    let auctionState = await getAuctionState(auctionPDA);
    let outBidder = auctionState.bidder;

    const [globalAuthority, bump] = await PublicKey.findProgramAddress(
        [Buffer.from(GLOBAL_AUTHORITY_SEED)],
        auctionProgramID,
    );

    let ret1 = await getATokenAccountsNeedCreate(
        auctionSolConnection,
        userAddress,
        globalAuthority,
        [htoTokenMint]
    );
    let ret2 = await getATokenAccountsNeedCreate(
        auctionSolConnection,
        userAddress,
        userAddress,
        [htoTokenMint]
    );
    let ret3 = await getATokenAccountsNeedCreate(
        auctionSolConnection,
        userAddress,
        outBidder,
        [htoTokenMint]
    );
    let tx = new Transaction();

    if (ret1.instructions.length > 0) ret1.instructions.map((ix) => tx.add(ix));
    if (ret2.instructions.length > 0) ret2.instructions.map((ix) => tx.add(ix));
    if (ret3.instructions.length > 0) ret3.instructions.map((ix) => tx.add(ix));
    
    let outBidderAccount = ret3.destinationAccounts[0];
    if (outBidder.toBase58() === PublicKey.default.toBase58()) {
        outBidder = userAddress;
        outBidderAccount = ret2.destinationAccounts[0];
    }

    tx.add(auctionProgram.instruction.placeBid(
        new anchor.BN(bid * htoTokenDecimals), bump, {
            accounts: {
                bidder: userAddress,
                auction: auctionPDA,
                globalAuthority,
                auctionVault: ret1.destinationAccounts[0],
                outBidderAccount,
                outBidder,
                newBidderAccount: ret2.destinationAccounts[0],
                tokenProgram: TOKEN_PROGRAM_ID,
            },
            instructions: [],
            signers: []
        }
    ));

    return tx;
}


export const createAuctionClaimTx = async (userAddress: PublicKey, auctionPDA: PublicKey) => {
    let auctionState = await getAuctionState(auctionPDA);
    let winner = auctionState.bidder;
    let seller = auctionState.seller;
    let nftMint = auctionState.nftMint;

    const [globalAuthority, bump] = await PublicKey.findProgramAddress(
        [Buffer.from(GLOBAL_AUTHORITY_SEED)],
        auctionProgramID,
    );

    let ret1 = await getATokenAccountsNeedCreate(
        auctionSolConnection,
        userAddress,
        globalAuthority,
        [htoTokenMint, nftMint]
    );

    let ret2 = await getATokenAccountsNeedCreate(
        auctionSolConnection,
        userAddress,
        vaultWallet,
        [htoTokenMint]
    );

    let ret3 = await getATokenAccountsNeedCreate(
        auctionSolConnection,
        userAddress,
        winner,
        [nftMint]
    );

    let ret4 = await getATokenAccountsNeedCreate(
        auctionSolConnection,
        userAddress,
        seller,
        [htoTokenMint]
    );

    let { metadata: { Metadata } } = programs;
    let metadataAccount = await Metadata.getPDA(nftMint);
    const metadata = await Metadata.load(auctionSolConnection, metadataAccount);
    let creators = metadata.data.data.creators;

    let mintMetadata = await getMetadata(nftMint);

    let tx = new Transaction();
    if (ret1.instructions.length > 0) ret1.instructions.map((ix) => tx.add(ix));
    if (ret2.instructions.length > 0) ret2.instructions.map((ix) => tx.add(ix));
    if (ret3.instructions.length > 0) ret3.instructions.map((ix) => tx.add(ix));
    if (ret4.instructions.length > 0) ret4.instructions.map((ix) => tx.add(ix));
    
    let remainingAccounts = [];
    for (let i = 0; i< creators.length; i++) {
        let { instructions, destinationAccounts } = await getATokenAccountsNeedCreate(
            auctionSolConnection,
            userAddress,
            new PublicKey(creators[i].address),
            [htoTokenMint]
        );
        log.debug(TAG, '[createAuctionClaimTx]', 'creator', creators[i].address);
        log.debug(TAG, '[createAuctionClaimTx]', 'creatorATA', destinationAccounts[0].toBase58());
        remainingAccounts.push({
            pubkey: destinationAccounts[0],
            isWritable: true,
            isSigner: false,
        })
        if (instructions.length > 0) instructions.map((ix) => tx.add(ix));
    }

    tx.add(auctionProgram.instruction.claimAuction(
        bump, {
            accounts: {
                claimer: userAddress,
                auction: auctionPDA,
                globalAuthority,
                auctionAta: ret1.destinationAccounts[1], 
                auctionVault: ret1.destinationAccounts[0],
                hlVault: ret2.destinationAccounts[0],
                nftMint,
                winnerAta: ret3.destinationAccounts[0],
                sellerAta: ret4.destinationAccounts[0],
                mintMetadata,
                tokenProgram: TOKEN_PROGRAM_ID,
            },
            remainingAccounts,
            instructions: [],
            signers: []
        }
    ));

    return tx;
    }

/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
////////// read PDA
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

export const getAllAuction = async (seller: string | undefined, nftCollection: string | undefined, bidder: string | undefined) => {
    let filters = [];
    filters.push(
        {
            dataSize: AUCTION_SIZE
        }
    );
    if (seller != undefined) {
        filters.push(
            {
                memcmp: {
                    offset: 8,
                    bytes: seller
                }
            }
        );    
    }
    if (nftCollection != undefined) {
        filters.push(
            {
                memcmp: {
                    offset: 72,
                    bytes: nftCollection
                }
            }
        );
    }
    if (bidder != undefined) {
        filters.push(
            {
                memcmp: {
                    offset: 104,
                    bytes: bidder
                }
            }
        );
    }

    let auctionAccounts = await auctionSolConnection.getProgramAccounts(auctionProgramID, {filters});
    let auctions = [];
    
    for (let i = 0; i < auctionAccounts.length; i++) {
        let data = auctionAccounts[i].account.data;
        const seller = new PublicKey(data.slice(8, 40));
        const nftMint = new PublicKey(data.slice(40, 72));
        const nftCollection = new PublicKey(data.slice(72, 104));
        const bidder = new PublicKey(data.slice(104, 136));
        const currentBid = new anchor.BN(data.slice(136, 144).reverse());
        const startPrice = new anchor.BN(data.slice(144, 152).reverse());
        const endTime = new anchor.BN(data.slice(152, 160).reverse());

        auctions.push({
            pda : auctionAccounts[i].pubkey.toBase58(),
            seller: seller.toBase58(),
            nftMint: nftMint.toBase58(),
            nftCollection: nftCollection.toBase58(),
            bidder: bidder.toBase58(),
            currentBid: currentBid.toNumber(),
            startPrice: startPrice.toNumber(),
            endTime: endTime.toNumber(),
        });
    }
    return auctions;
}


export const getAuctionInfo = async (auctionPDA: PublicKey) => {
    const auctionInfo: AuctionPool = await getAuctionState(auctionPDA);
    return {
        pda: auctionPDA.toBase58(),
        seller: auctionInfo.seller.toBase58(),
        nftMint: auctionInfo.nftMint.toBase58(),
        nftCollection: auctionInfo.nftCollection.toBase58(),
        bidder: auctionInfo.bidder.toBase58(),
        currentBid: auctionInfo.currentBid.toNumber(),
        startPrice: auctionInfo.startPrice.toNumber(),
        endTime: auctionInfo.endTime.toNumber(),
    };
}


export const getAuctionState = async (auctionPDA: PublicKey): Promise<AuctionPool | null> => {
    try {
        let auctionState = await auctionProgram.account.auctionPool.fetch(auctionPDA);
        return auctionState as unknown as AuctionPool;
    } catch {
        return null;
    }
}
