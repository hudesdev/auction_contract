from datetime import datetime, timezone
from utils.logger import Logger

class RateLimiter:
    def __init__(self, daily_limit):
        self.daily_limit = daily_limit
        self.tweet_count = 0
        self.logger = Logger()

    def can_tweet(self):
        """Check if we can send more tweets"""
        if self.tweet_count >= self.daily_limit:
            self.logger.warning(f"Tweet limiti aşıldı: {self.tweet_count}/{self.daily_limit}")
            return False
        return True

    def increment_counter(self):
        """Increment the tweet counter"""
        self.tweet_count += 1
        self.logger.info(f"Tweet sayacı: {self.tweet_count}/{self.daily_limit}")

    def get_remaining_tweets(self):
        """Get remaining tweets"""
        return self.daily_limit - self.tweet_count 