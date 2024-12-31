"""Food expert module"""
import logging
from typing import Optional
from src.experts.base_expert import BaseExpert
from src.utils.event_bus import EventBus

class FoodExpert(BaseExpert):
    """Expert for handling food-related queries"""
    
    def __init__(self, config):
        """Initialize food expert
        
        Args:
            config: Expert configuration
        """
        super().__init__(config)
        self.event_bus = EventBus()
        
        # Subscribe to events
        self.event_bus.subscribe('question_received', self._on_question_received)
        self.event_bus.subscribe('response_generated', self._on_response_generated)
        
    async def get_response(self, query: str) -> Optional[str]:
        """Generate response for food query
        
        Args:
            query (str): User query
            
        Returns:
            Optional[str]: Generated response or None if failed
        """
        try:
            # Check cache first
            if self.cache:
                cached_response = self.cache.get(query)
                if cached_response:
                    return cached_response
                    
            # Check local knowledge base
            local_response = await self._check_local_knowledge(query)
            if local_response:
                if self.cache:
                    self.cache.set(query, local_response)
                return local_response
                
            # Check URL sources
            url_response = await self._check_url_sources(query)
            if url_response:
                if self.cache:
                    self.cache.set(query, url_response)
                return url_response
                
            # Generate response using OpenAI
            system_prompt = """Sen bir yemek ve mutfak uzmanısın. Yemek tarifleri, pişirme teknikleri, malzemeler ve beslenme konularında detaylı bilgi sahibisin.
            Soruları kısa ve öz bir şekilde yanıtla. Emin olmadığın konularda bunu belirt.
            Yanıtlarında pratik ve uygulanabilir bilgiler vermeye özen göster."""
            
            ai_response = await self.openai_client.get_completion(system_prompt, query)
            if ai_response:
                if self.cache:
                    self.cache.set(query, ai_response)
                return ai_response
                
            # Perform web search as last resort
            web_response = await self._perform_web_search(query)
            if web_response:
                if self.cache:
                    self.cache.set(query, web_response)
                return web_response
                
            return "Üzgünüm, bu yemek sorusuna yanıt üretemiyorum. Lütfen soruyu daha açık bir şekilde sorar mısınız?"
            
        except Exception as e:
            self.logger.error(f"Error generating food response: {str(e)}")
            return None
            
    async def _on_question_received(self, question: str) -> None:
        """Handle received question event
        
        Args:
            question (str): Received question
        """
        self.logger.info(f"Food expert received question: {question}")
        
    async def _on_response_generated(self, response: str) -> None:
        """Handle generated response event
        
        Args:
            response (str): Generated response
        """
        self.logger.info(f"Food expert generated response: {response}") 