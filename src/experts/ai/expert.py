"""AI Expert implementation"""
from typing import Dict, Any, Optional
import logging
from src.core.expert_base import ExpertBase
from src.utils.cache import Cache
from src.core.openai_client import OpenAIClient

logger = logging.getLogger(__name__)

class AIExpert(ExpertBase):
    def __init__(self, config: Dict[str, Any]):
        """Initialize AIExpert
        
        Args:
            config (Dict[str, Any]): Configuration dictionary
        """
        super().__init__("ai")
        self.config = config
        self.cache = Cache(
            enabled=config["experts"]["ai"]["cache_enabled"],
            ttl=config["experts"]["ai"]["cache_ttl"]
        )
        self.openai_client = OpenAIClient()
        
    async def get_response(self, question: str) -> Optional[str]:
        """Get response for AI related question
        
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
            response = await self._generate_response(question)
            
            # Cache the response
            if response:
                self.cache.set(question, response)
                
            return response
            
        except Exception as e:
            logger.error("Error getting AI response: %s", str(e))
            return None
            
    async def _generate_response(self, question: str) -> Optional[str]:
        """Generate response using OpenAI
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Generated response or None
        """
        system_prompt = """Sen bir yapay zeka uzmanısın.
        Yapay zeka teknolojileri, uygulamaları, etik konuları ve gelişmeler hakkında detaylı bilgi sahibisin.
        Kullanıcının sorduğu yapay zeka ile ilgili soruları yanıtla.
        Eğer soru yapay zeka ile ilgili değilse, bunu belirt."""
        
        try:
            response = await self.openai_client.get_completion(system_prompt, question)
            return response
        except Exception as e:
            logger.error("Error generating AI response: %s", str(e))
            return None 