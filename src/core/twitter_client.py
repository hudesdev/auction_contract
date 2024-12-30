import tweepy
import os
from typing import Optional
from src.utils.config_loader import ConfigLoader
from src.utils.logger import Logger

class TwitterClient:
    """Twitter API istemcisi"""
    
    def __init__(self):
        """Twitter istemcisini başlat"""
        self.logger = Logger("TwitterClient")
        self.config = ConfigLoader().load_config()
        
        # Twitter API anahtarlarını al
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        
        # Twitter istemcisini oluştur
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)
        
    def tweet(self, message: str) -> Optional[str]:
        """
        Tweet gönder
        
        Args:
            message: Tweet metni
            
        Returns:
            str: Tweet ID veya None
        """
        try:
            tweet = self.api.update_status(message)
            return tweet.id_str
        except Exception as e:
            self.logger.error(f"Tweet gönderme hatası: {str(e)}")
            return None
            
    def reply(self, message: str, tweet_id: str) -> Optional[str]:
        """
        Tweet'e yanıt ver
        
        Args:
            message: Yanıt metni
            tweet_id: Yanıt verilecek tweet ID
            
        Returns:
            str: Yanıt tweet ID veya None
        """
        try:
            tweet = self.api.update_status(
                message,
                in_reply_to_status_id=tweet_id
            )
            return tweet.id_str
        except Exception as e:
            self.logger.error(f"Tweet yanıtlama hatası: {str(e)}")
            return None 