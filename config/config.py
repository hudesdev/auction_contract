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
    'model': 'gpt-4',
    'max_tokens': 300,
    'temperature': 0.7
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
    'cache_enabled': True,
    'cache_ttl': 3600  # 1 hour
}

# Expert System Configuration
EXPERT_CONFIG = {
    'sports': {
        'cache_enabled': True,
        'cache_ttl': 3600,
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        },
        'tavily': {
            'max_results': 5,
            'search_depth': 'advanced'
        }
    },
    'food': {
        'cache_enabled': True,
        'cache_ttl': 3600,
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        },
        'tavily': {
            'max_results': 5,
            'search_depth': 'advanced'
        }
    },
    'ai': {
        'cache_enabled': True,
        'cache_ttl': 3600,
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        },
        'tavily': {
            'max_results': 5,
            'search_depth': 'advanced'
        }
    },
    'sudostar': {
        'cache_enabled': True,
        'cache_ttl': 3600,
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        }
    }
}

# System Messages
SYSTEM_MESSAGES = {
    'openai_prompt': "Sen profesyonel ve arkadaş canlısı bir asistansın. En fazla 3 kısa cümle kullanarak, özlü ve yararlı yanıtlar vermelisin. Emoji kullanabilirsin."
} 