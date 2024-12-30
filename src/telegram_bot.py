"""Telegram test botu"""
import os
import sys
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.experts import SportsExpert, FoodExpert, AIExpert, SudoStarExpert
from src.core.expert_selector import ExpertSelector
from src.utils.config import ConfigLoader

# Load environment variables
load_dotenv()

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        """Initialize bot"""
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")
            
        # Expert sistemi başlat
        config = ConfigLoader.load_config()
        self.sports_expert = SportsExpert(config)
        self.food_expert = FoodExpert(config)
        self.ai_expert = AIExpert(config)
        self.sudostar_expert = SudoStarExpert()
        self.expert_selector = ExpertSelector()
        self.application = None
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Bot başlatıldığında çalışır"""
        welcome_message = """Merhaba! Ben bir uzman sistemim. 
        Aşağıdaki konularda sorularınızı yanıtlayabilirim:
        
        1. Spor (futbol, basketbol, maçlar, antrenman)
        2. Yemek (tarifler, restoranlar, diyet)
        3. Yapay Zeka (teknolojiler, uygulamalar, etik)
        4. SudoStar (özellikler, ödeme sistemi, elmas sistemi)
        
        Lütfen sorunuzu yazın."""
        
        await update.message.reply_text(welcome_message)
        
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gelen mesajları işle"""
        question = update.message.text
        
        try:
            # Uzman seç
            expert_type = await self.expert_selector.select_expert(question)
            
            if expert_type == "spor":
                response = await self.sports_expert.get_response(question)
            elif expert_type == "yemek":
                response = await self.food_expert.get_response(question)
            elif expert_type == "ai":
                response = await self.ai_expert.get_response(question)
            elif expert_type == "sudostar":
                context = self.sudostar_expert.get_relevant_context(question)
                response = context.get("common_questions", {}).get(question, None)
                if not response:
                    kb = context.get("knowledge_base", {})
                    if "ödemeler" in question.lower() or "para" in question.lower():
                        payment_info = kb.get("rewards_system", {}).get("diamonds", {}).get("payment_processing", {})
                        response = f"Ödemeler {payment_info.get('processing_time', '1-3 gün')} içinde hesabınıza aktarılır."
                    elif "elmas" in question.lower():
                        diamonds = kb.get("rewards_system", {}).get("diamonds", {})
                        conversion = diamonds.get("conversion_rate", {})
                        response = f"Her {conversion.get('diamonds_per_dollar', 5000)} elmas 1 USD'ye eşittir. Minimum çekim miktarı {conversion.get('minimum_withdrawal', 25000)} elmastır."
            else:
                response = None
                
            if response:
                await update.message.reply_text(response)
            else:
                await update.message.reply_text(
                    "Üzgünüm, sorunuzu yanıtlayamadım. "
                    "Lütfen sorunuzu daha açık bir şekilde ifade edin veya "
                    "spor, yemek, yapay zeka ya da SudoStar konularında bir soru sorun."
                )
                
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            await update.message.reply_text(
                "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin."
            )
            
    async def run(self):
        """Bot'u çalıştır"""
        try:
            # Bot oluştur
            self.application = Application.builder().token(self.token).build()
            
            # Komut ve mesaj işleyicileri ekle
            self.application.add_handler(CommandHandler("start", self.start))
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            # Bot'u başlat
            logger.info("Bot starting...")
            
            # Webhook'u temizle
            await self.application.bot.delete_webhook()
            
            # Bot'u başlat
            await self.application.initialize()
            await self.application.start()
            
            # Polling başlat
            await self.application.updater.start_polling(
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES,
                bootstrap_retries=0,
                read_timeout=30,
                write_timeout=30,
                connect_timeout=30,
                pool_timeout=30
            )
            
            # Bot'u çalışır durumda tut
            while True:
                if not self.application.running:
                    break
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error running bot: {str(e)}")
            if self.application:
                try:
                    if self.application.running:
                        await self.application.stop()
                except Exception as stop_error:
                    logger.error(f"Error stopping application: {str(stop_error)}")
            raise e
            
async def main():
    """Main entry point"""
    bot = None
    try:
        bot = TelegramBot()
        await bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
    finally:
        if bot and bot.application and bot.application.running:
            try:
                await bot.application.stop()
            except Exception as shutdown_error:
                logger.error(f"Error during shutdown: {str(shutdown_error)}")
        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {str(e)}") 