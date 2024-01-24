#!/usr/bin/env ts-node
// @ts-ignore
import { program } from 'commander';
import { PublicKey } from '@solana/web3.js';
import { cancelAuction, claimAuction, createAuction,  getAllAuction,  getAuctionInfo,  initialize,  placeBid,  setClusterConfig, getWalletKeypair} from "./script";
import * as log from 'loglevel';

const TAG = '[AUCTION]';

program.version('1.0');
setLogLevel('info');
    

programCommand('init')
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    .action(async (directory, cmd) => {
        const { env, keypair, rpc } = cmd.opts();
        log.debug(TAG, '[init]', 'Solana Env Config:', env);
        log.debug(TAG, '[init]', 'Keypair Path:', keypair);
        log.debug(TAG, '[init]', 'RPC URL:', rpc);

        const walletKeypair = getWalletKeypair(keypair);       
        await setClusterConfig(env,  walletKeypair, rpc);
        await initialize(walletKeypair);
    });


programCommand('create_auction')
    .option('-mint, --mint <string>', 'NFT mint address')
    .option('-s, --start_price <number>', 'start price of the auction [10.1 means 10.1 HTO]')
    .option('-d, --duration <number>', 'duration of the auction [100 means 100 seconds]')
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    .action(async (directory, cmd) => {
        const {env, keypair, rpc, mint, start_price, duration} = cmd.opts();
        log.debug(TAG, '[create_auction]', 'Solana Env Config:', env);
        log.debug(TAG, '[create_auction]', 'Keypair Path:', keypair);
        log.debug(TAG, '[create_auction]', 'RPC URL:', rpc);

        if (mint === undefined) {
            log.error(TAG, '[create_auction]', "Error Mint Address Input");
            return;
          }
        if (start_price === undefined || isNaN(parseInt(start_price))) {
            log.error(TAG, '[create_auction]', "Error Start Price Input");
            return;
        }
        if (duration === undefined || isNaN(parseInt(duration))) {
            log.error(TAG, '[create_auction]', "Error Duration Input");
            return;
        }
        
        const walletKeypair = getWalletKeypair(keypair);       
        await setClusterConfig(env, walletKeypair, rpc);
        await createAuction(new PublicKey(mint), start_price, duration);
    });


programCommand('cancel_auction')
    .option('-pda, --pda <string>', 'auction pda address')
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    .action(async (directory, cmd) => {
        const {env, keypair, rpc, pda} = cmd.opts();
        log.debug(TAG, '[cancel_auction]', 'Solana Env Config:', env);
        log.debug(TAG, '[cancel_auction]', 'Keypair Path:', keypair);
        log.debug(TAG, '[cancel_auction]', 'RPC URL:', rpc);

        if (pda === undefined) {
            log.error(TAG, '[cancel_auction]', "Error PDA Input");
            return;
        }

        const walletKeypair = getWalletKeypair(keypair);       
        await setClusterConfig(env, walletKeypair, rpc);
        await cancelAuction(new PublicKey(pda));
    });


programCommand('claim_auction')
    .option('-pda, --pda <string>', 'auction pda address')
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    .action(async (directory, cmd) => {
        const {env, keypair, rpc, pda} = cmd.opts();
        log.debug(TAG, '[claim_auction]', 'Solana Env Config:', env);
        log.debug(TAG, '[claim_auction]', 'Keypair Path:', keypair);
        log.debug(TAG, '[claim_auction]', 'RPC URL:', rpc);

        if (pda === undefined) {
            log.error(TAG, '[claim_auction]', "Error PDA Input");
            return;
        }

        const walletKeypair = getWalletKeypair(keypair);       
        await setClusterConfig(env, walletKeypair, rpc);
        await claimAuction(new PublicKey(pda));
    });
    

programCommand('place_bid')
    .option('-pda, --pda <string>', 'auction pda address')
    .option('-b, --bid <number>', 'bid amount [10.1 means 10.1 HTO]')
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    .action(async (directory, cmd) => {
        const {env, keypair, rpc, pda, bid} = cmd.opts();
        log.debug(TAG, '[place_bid]', 'Solana Env Config:', env);
        log.debug(TAG, '[place_bid]', 'Keypair Path:', keypair);
        log.debug(TAG, '[place_bid]', 'RPC URL:', rpc);
        
        if (pda === undefined) {
            log.error(TAG, '[place_bid]', "Error PDA Input");
            return;
        }
        if (bid === undefined || isNaN(parseInt(bid))) {
            log.error(TAG, '[place_bid]', "Error Bid Amount Input");
            return;
        }

        const walletKeypair = getWalletKeypair(keypair);       
        await setClusterConfig(env, walletKeypair, rpc);
        await placeBid(new PublicKey(pda), bid);
    });
    
    
programCommand('get_auction_info')
    .option('-pda, --pda <string>', 'auction pda address')
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    .action(async (directory, cmd) => {
        const {env,  keypair, rpc, pda} = cmd.opts();
        log.debug(TAG, '[get_auction_info]', 'Solana Env Config:', env);
        log.debug(TAG, '[get_auction_info]', 'Keypair Path:', keypair);
        log.debug(TAG, '[get_auction_info]', 'RPC URL:', rpc);

        if (pda === undefined) {
            console.log("Error Auction Address Input");
            return;
        }

        const walletKeypair = getWalletKeypair(keypair);       
        await setClusterConfig(env, walletKeypair, rpc);
        log.info(TAG, '[get_auction_info]', 'Auction PDA:', await getAuctionInfo(new PublicKey(pda)));
    });

    
programCommand('get_all_auctions')
    .option('-s, --seller <string>', '[optional] filter for given seller address only')
    .option('-c, --collection <string>', '[optional] filter for given collection address only')
    .option('-b, --bidder <string>', '[optional] filter for given bidder address only')
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    .action(async (directory, cmd) => {
        const {env,  keypair, rpc, seller, collection, bidder} = cmd.opts();
        log.debug(TAG, '[get_all_auctions]', 'Solana Env Config:', env);
        log.debug(TAG, '[get_all_auctions]', 'Keypair Path:', keypair);
        log.debug(TAG, '[get_all_auctions]', 'RPC URL:', rpc);

        const walletKeypair = getWalletKeypair(keypair);       
        await setClusterConfig(env, walletKeypair, rpc);
        log.info(TAG, '[get_all_auctions]', 'Auction PDAs:', await getAllAuction(seller, collection, bidder));  
    });

    
    function programCommand(name: string, requireKeypair?: boolean | undefined) {
        const p = program
            .command(name)
            .option(
                '-e, --env <string>',
                'Solana cluster env name',
                'devnet' //mainnet-beta, testnet, devnet
            )
            .option('-r, --rpc <string>', 'Solana cluster RPC name')
            .option('-l, --log-level <string>', 'log level [trace, debug, info, warn, error]', setLogLevel);
    
        if (requireKeypair === true) {
            p.requiredOption('-k, --keypair <string>', 'Solana wallet Keypair Path');
        } else {
            p.option('-k, --keypair <string>', 'Solana wallet Keypair Path');
        }
    
        return p;
    }
    
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    function setLogLevel(value: any) {
        if (value === undefined || value === null) {
            return;
        }
        log.info('setting the log value to: ' + value);
        log.setLevel(value);
    }
    
    program.parse(process.argv);