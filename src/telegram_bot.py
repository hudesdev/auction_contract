"""Telegram bot is disabled"""
import logging

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        logger.info("Telegram bot is disabled")
        pass

    async def run(self):
        logger.info("Telegram bot is disabled")
        pass

async def main():
    """Main entry point"""
    try:
        bot = TelegramBot()
        await bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        
if __name__ == "__main__":
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {str(e)}") 