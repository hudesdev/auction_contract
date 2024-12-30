"""Kaynak yöneticisi"""
import logging
from typing import Dict, Any, Optional
from src.core.openai_client import OpenAIClient
from src.core.tavily_client import TavilyClient
from src.utils.config import ConfigLoader

logger = logging.getLogger(__name__)

class ResourceManager:
    """API istemcilerini yöneten sınıf"""
    
    def __init__(self):
        """Initialize resource manager"""
        self.config = ConfigLoader.load_config()
        self._clients = {}
        
        try:
            # OpenAI istemcisi
            self._clients["openai"] = OpenAIClient()
            logger.info("OpenAI client başarıyla oluşturuldu")
            
            # Tavily istemcisi
            self._clients["tavily"] = TavilyClient()
            logger.info("Tavily client başarıyla oluşturuldu")
            
        except Exception as e:
            logger.error(f"API istemcileri başlatma hatası: {str(e)}")
            raise
            
    def get_client(self, client_type: str) -> Any:
        """Get API client by type
        
        Args:
            client_type (str): Type of client ("openai" or "tavily")
            
        Returns:
            Any: API client instance
        """
        return self._clients.get(client_type)
        
    def __del__(self):
        """Cleanup resources"""
        # İstemcileri temizle
        self._clients.clear() 