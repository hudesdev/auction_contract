from typing import Optional
from utils.logger import Logger
from core.twitter_client import TwitterClient
from core.expert_selector import ExpertSelector
from utils.config_loader import ConfigLoader

class TweetHandler:
    """Tweet işleme ve yanıtlama sınıfı"""
    
    def __init__(self):
        self.logger = Logger("TweetHandler")
        
        # Yapılandırmayı yükle
        config_loader = ConfigLoader()
        self.config = config_loader.load_config("app")
        
        # Twitter istemcisini başlat
        self.twitter = TwitterClient(
            api_key=self.config['twitter']['api_key'],
            api_secret=self.config['twitter']['api_secret'],
            access_token=self.config['twitter']['access_token'],
            access_token_secret=self.config['twitter']['access_token_secret']
        )
        
        # Uzman seçiciyi başlat
        self.expert_selector = ExpertSelector()
        
    def process_mentions(self) -> bool:
        """
        Mention'ları işle ve yanıtla
        
        Returns:
            bool: İşlem başarılı mı
        """
        try:
            # Son mention'ları al
            mentions = self.twitter.get_mentions()
            if not mentions:
                self.logger.info("İşlenecek mention bulunamadı")
                return True
                
            # Her mention'ı işle
            for mention in mentions:
                # Uzman seçip yanıt al
                response = self.expert_selector.get_response(mention.text)
                
                if response:
                    # Yanıtı tweet at
                    self.twitter.reply_to_tweet(
                        tweet_id=mention.id,
                        text=response
                    )
                    self.logger.info(f"Mention yanıtlandı: {mention.id}")
                else:
                    self.logger.warning(f"Mention için yanıt üretilemedi: {mention.id}")
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Mention işleme hatası: {str(e)}")
            return False
            
    def process_replies(self) -> bool:
        """
        Yanıtları işle
        
        Returns:
            bool: İşlem başarılı mı
        """
        try:
            # Son yanıtları al
            replies = self.twitter.get_replies()
            if not replies:
                self.logger.info("İşlenecek yanıt bulunamadı")
                return True
                
            # Her yanıtı işle
            for reply in replies:
                # Uzman seçip yanıt al
                response = self.expert_selector.get_response(reply.text)
                
                if response:
                    # Yanıtı tweet at
                    self.twitter.reply_to_tweet(
                        tweet_id=reply.id,
                        text=response
                    )
                    self.logger.info(f"Yanıt işlendi: {reply.id}")
                else:
                    self.logger.warning(f"Yanıt için cevap üretilemedi: {reply.id}")
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Yanıt işleme hatası: {str(e)}")
            return False
            
    def generate_tweet(self, topic: Optional[str] = None) -> bool:
        """
        Tweet oluştur ve gönder
        
        Args:
            topic: Tweet konusu (None ise rastgele konu seçilir)
            
        Returns:
            bool: İşlem başarılı mı
        """
        try:
            # Uzmandan tweet al
            tweet = self.expert_selector.get_tweet(topic)
            
            if tweet:
                # Tweet'i gönder
                self.twitter.send_tweet(tweet)
                self.logger.info("Tweet gönderildi")
                return True
            else:
                self.logger.warning("Tweet oluşturulamadı")
                return False
                
        except Exception as e:
            self.logger.error(f"Tweet oluşturma hatası: {str(e)}")
            return False 