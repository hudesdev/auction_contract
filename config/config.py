import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API Configuration
TWITTER_CONFIG = {
    "API_KEY": os.getenv("TWITTER_API_KEY"),
    "API_KEY_SECRET": os.getenv("TWITTER_API_KEY_SECRET"),
    "BEARER_TOKEN": os.getenv("TWITTER_BEARER_TOKEN"),
    "ACCESS_TOKEN": os.getenv("TWITTER_ACCESS_TOKEN"),
    "ACCESS_TOKEN_SECRET": os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
}

# OpenAI Configuration
OPENAI_CONFIG = {
    "API_KEY": os.getenv("OPENAI_API_KEY"),
    'model': 'gpt-3.5-turbo',
    'max_tokens': 100,
}

# Tavily API Configuration
TAVILY_CONFIG = {
    "API_KEY": os.getenv("TAVILY_API_KEY")
}

# Application Settings
APP_CONFIG = {
    'daily_tweet_limit': 50,
    'check_interval': 60,  # seconds
    'max_retries': 3,
    'retry_delay': 60,  # seconds
}

# System Messages
SYSTEM_MESSAGES = {
    'openai_prompt': "Sen profesyonel ve arkadaş canlısı bir Twitter asistanısın. En fazla 3 kısa cümle kullanarak, özlü ve yararlı yanıtlar vermelisin. Emoji kullanabilirsin."
} 