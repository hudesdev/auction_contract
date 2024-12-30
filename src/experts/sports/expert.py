from typing import Dict, Any, Optional
import logging
from src.core.expert_base import ExpertBase
from src.utils.cache import Cache
from src.core.openai_client import OpenAIClient

logger = logging.getLogger(__name__)

class SportsExpert(ExpertBase):
    def __init__(self, config: Dict[str, Any]):
        """Initialize SportsExpert
        
        Args:
            config (Dict[str, Any]): Configuration dictionary
        """
        super().__init__("sports")
        self.config = config
        self.cache = Cache(
            enabled=config["experts"]["sports"]["cache_enabled"],
            ttl=config["experts"]["sports"]["cache_ttl"]
        )
        self.openai_client = OpenAIClient()
        
    def get_response(self, question: str) -> Optional[str]:
        """Get response for sports related question
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Response or None if no answer found
        """
        try:
            # Check cache first
            cached_response = self.cache.get(question)
            if cached_response:
                logger.info("Cache hit for question: %s", question)
                return cached_response
                
            # Generate response using OpenAI
            response = self._generate_response(question)
            
            # Cache the response
            if response:
                self.cache.set(question, response)
                
            return response
            
        except Exception as e:
            logger.error("Error getting sports response: %s", str(e))
            return None
            
    def _generate_response(self, question: str) -> Optional[str]:
        """Generate response using OpenAI
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Generated response or None on error
        """
        try:
            system_prompt = """Sen bir spor uzmanısın. Futbol, basketbol ve diğer sporlar hakkında detaylı bilgi sahibisin.
            Soruları Türkçe olarak yanıtla ve mümkün olduğunca güncel ve doğru bilgiler ver.
            
            Önemli kurallar:
            1. Sadece güncel ve doğruluğundan emin olduğun bilgileri ver
            2. Eski veya güncel olmayan bilgileri verme (örn: takımdan ayrılmış oyuncular)
            3. Emin olmadığın konularda "Bu konuda güncel bilgim yok" de
            4. Özellikle transfer, piyasa değeri gibi konularda çok dikkatli ol
            5. Mümkünse bilginin tarihini de belirt"""
            
            return self.openai_client.get_completion(system_prompt, question)
            
        except Exception as e:
            logger.error("Error generating response: %s", str(e))
            return None 