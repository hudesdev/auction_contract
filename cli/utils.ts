import {
    Connection,
    PublicKey,
    SystemProgram,
    SYSVAR_RENT_PUBKEY,
    TransactionInstruction,
    Transaction,
    Keypair,
} from '@solana/web3.js';
import { TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID, Token, MintLayout } from "@solana/spl-token";

export const METAPLEX = new PublicKey('metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s');

export const getOwnerOfNFT = async (nftMintPk: PublicKey, connection: Connection): Promise<PublicKey> => {
    let tokenAccountPK = await getNFTTokenAccount(nftMintPk, connection);
    let tokenAccountInfo = await connection.getAccountInfo(tokenAccountPK);

    if (tokenAccountInfo && tokenAccountInfo.data) {
        let ownerPubkey = new PublicKey(tokenAccountInfo.data.slice(32, 64))
        console.log("ownerPubkey=", ownerPubkey.toBase58());
        return ownerPubkey;
    }
    return new PublicKey("");
}

export const getTokenAccount = async (mintPk: PublicKey, userPk: PublicKey, connection: Connection): Promise<PublicKey> => {
    let tokenAccount = await connection.getProgramAccounts(
        TOKEN_PROGRAM_ID,
        {
            filters: [
                {
                    dataSize: 165
                },
                {
                    memcmp: {
                        offset: 0,
                        bytes: mintPk.toBase58()
                    }
                },
                {
                    memcmp: {
                        offset: 32,
                        bytes: userPk.toBase58()
                    }
                },
            ]
        }
    );
    return tokenAccount[0].pubkey;
}

export const getNFTTokenAccount = async (nftMintPk: PublicKey, connection: Connection): Promise<PublicKey> => {
    let tokenAccount = await connection.getProgramAccounts(
        TOKEN_PROGRAM_ID,
        {
            filters: [
                {
                    dataSize: 165
                },
                {
                    memcmp: {
                        offset: 64,
                        bytes: '2'
                    }
                },
                {
                    memcmp: {
                        offset: 0,
                        bytes: nftMintPk.toBase58()
                    }
                },
            ]
        }
    );
    return tokenAccount[0].pubkey;
}

export const getAssociatedTokenAccount = async (ownerPubkey: PublicKey, mintPk: PublicKey): Promise<PublicKey> => {
    let associatedTokenAccountPubkey = (await PublicKey.findProgramAddress(
        [
            ownerPubkey.toBuffer(),
            TOKEN_PROGRAM_ID.toBuffer(),
            mintPk.toBuffer(), // mint address
        ],
        ASSOCIATED_TOKEN_PROGRAM_ID
    ))[0];
    return associatedTokenAccountPubkey;
}

export const getATokenAccountsNeedCreate = async (
    connection: Connection,
    walletAddress: PublicKey,
    owner: PublicKey,
    nfts: PublicKey[],
) => {
    let instructions = [], destinationAccounts = [];
    for (const mint of nfts) {
        const destinationPubkey = await getAssociatedTokenAccount(owner, mint);
        const response = await connection.getAccountInfo(destinationPubkey);
        if (!response) {
            const createATAIx = createAssociatedTokenAccountInstruction(
                destinationPubkey,
                walletAddress,
                owner,
                mint,
            );
            instructions.push(createATAIx);
        }
        destinationAccounts.push(destinationPubkey);
    }
    return {
        instructions,
        destinationAccounts,
    };
}

export const createAssociatedTokenAccountInstruction = (
    associatedTokenAddress: PublicKey,
    payer: PublicKey,
    walletAddress: PublicKey,
    splTokenMintAddress: PublicKey
) => {
    const keys = [
        { pubkey: payer, isSigner: true, isWritable: true },
        { pubkey: associatedTokenAddress, isSigner: false, isWritable: true },
        { pubkey: walletAddress, isSigner: false, isWritable: false },
        { pubkey: splTokenMintAddress, isSigner: false, isWritable: false },
        {
            pubkey: SystemProgram.programId,
            isSigner: false,
            isWritable: false,
        },
        { pubkey: TOKEN_PROGRAM_ID, isSigner: false, isWritable: false },
        {
            pubkey: SYSVAR_RENT_PUBKEY,
            isSigner: false,
            isWritable: false,
        },
    ];
    return new TransactionInstruction({
        keys,
        programId: ASSOCIATED_TOKEN_PROGRAM_ID,
        data: Buffer.from([]),
    });
}

/** Get metaplex mint metadata account address */
export const getMetadata = async (mint: PublicKey): Promise<PublicKey> => {
    return (
        await PublicKey.findProgramAddress([Buffer.from('metadata'), METAPLEX.toBuffer(), mint.toBuffer()], METAPLEX)
    )[0];
};

export const airdropSOL = async (address: PublicKey, amount: number, connection: Connection) => {
    try {
        const txId = await connection.requestAirdrop(address, amount);
        await connection.confirmTransaction(txId);
    } catch (e) {
        console.log('Aridrop Failure', address.toBase58(), amount);
    }
}

export const createTokenMint = async (
    connection: Connection,
    payer: Keypair,
    mint: Keypair,
) => {
    const ret = await connection.getAccountInfo(mint.publicKey);
    if (ret && ret.data) {
        console.log('Token already in use', mint.publicKey.toBase58());
        return;
    };
    // Allocate memory for the account
    const balanceNeeded = await Token.getMinBalanceRentForExemptMint(
        connection,
    );
    const transaction = new Transaction();
    transaction.add(
        SystemProgram.createAccount({
            fromPubkey: payer.publicKey,
            newAccountPubkey: mint.publicKey,
            lamports: balanceNeeded,
            space: MintLayout.span,
            programId: TOKEN_PROGRAM_ID,
        }),
    );
    transaction.add(
        Token.createInitMintInstruction(
            TOKEN_PROGRAM_ID,
            mint.publicKey,
            9,
            payer.publicKey,
            payer.publicKey,
        ),
    );
    const txId = await connection.sendTransaction(transaction, [payer, mint]);
    await connection.confirmTransaction(txId);

    console.log('Tx Hash=', txId);
}

export const isExistAccount = async (address: PublicKey, connection: Connection) => {
    try {
        const res = await connection.getAccountInfo(address);
        if (res && res.data) return true;
    } catch (e) {
        return false;
    }
}

export const getTokenAccountBalance = async (account: PublicKey, connection: Connection) => {
    try {
        const res = await connection.getTokenAccountBalance(account);
        if (res && res.value) return res.value.uiAmount;
        return 0;
    } catch (e) {
        console.log(e)
        return 0;
    }
}