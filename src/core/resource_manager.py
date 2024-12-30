"""Resource manager for managing shared resources"""
import logging
from typing import Dict, Any
from src.utils.openai_client import OpenAIClient
from src.utils.cache import Cache

logger = logging.getLogger(__name__)

class ResourceManager:
    def __init__(self, config: Dict[str, Any]):
        """Initialize resource manager
        
        Args:
            config (Dict[str, Any]): Configuration dictionary
        """
        self.config = config
        self.openai_client = OpenAIClient()
        self.cache = Cache(
            enabled=config["cache"]["enabled"],
            ttl=config["cache"]["ttl"]
        )
        
    def get_openai_client(self) -> OpenAIClient:
        """Get OpenAI client instance
        
        Returns:
            OpenAIClient: OpenAI client instance
        """
        return self.openai_client
        
    def get_cache(self) -> Cache:
        """Get cache instance
        
        Returns:
            Cache: Cache instance
        """
        return self.cache 