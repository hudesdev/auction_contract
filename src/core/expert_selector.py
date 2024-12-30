import logging
from typing import Optional, Dict, Any
from src.utils.cache import Cache
from src.core.openai_client import OpenAIClient
import json

logger = logging.getLogger(__name__)

class ExpertSelector:
    def __init__(self):
        """Initialize expert selector"""
        self.cache = Cache(enabled=True, max_size=1000, ttl=3600)
        self.openai_client = OpenAIClient()
        
    async def select_expert(self, question: str) -> Optional[str]:
        """Select appropriate expert based on question
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Expert type or None if no match found
        """
        try:
            # Check cache first
            cached_expert = self.cache.get(question)
            if cached_expert:
                logger.info("Cache hit for question: %s", question)
                return cached_expert
                
            # Use OpenAI to classify the question
            system_prompt = """Sen bir soru sınıflandırma uzmanısın.
            Verilen soruyu analiz edip en uygun uzmana yönlendirmelisin.
            Yanıtı JSON formatında ver: {"expert": string, "confidence": float}
            Expert tipleri: "spor", "yemek", "ai" """
            
            user_message = f"Soru: {question}\n\nBu soru hangi uzmana yönlendirilmeli?"
            
            try:
                response = await self.openai_client.get_completion(system_prompt, user_message)
                if response:
                    result = json.loads(response)
                    
                    if result["confidence"] >= 0.7:  # Minimum güven skoru
                        expert_type = result["expert"]
                        # Cache the result
                        self.cache.set(question, expert_type)
                        return expert_type
                        
                return None
                
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing OpenAI response: {str(e)}")
                return None
                
        except Exception as e:
            logger.error(f"Error classifying question: {str(e)}")
            return None 