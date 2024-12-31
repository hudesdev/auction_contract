import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterClient:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_API_KEY'),
            os.getenv('TWITTER_API_SECRET')
        )
        self.auth.set_access_token(
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )
        self.api = tweepy.API(self.auth)

    def post_tweet(self, text):
        try:
            self.api.update_status(text)
            return True
        except Exception as e:
            print(f"Tweet gönderilirken hata oluştu: {str(e)}")
            return False 