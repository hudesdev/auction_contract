"""SudoStar expert module"""
import logging
from typing import Optional
from src.experts.base_expert import BaseExpert
from src.utils.event_bus import EventBus
from src.utils.web_search import WebSearch
from .sources.local_data import SUDOSTAR_KNOWLEDGE_BASE
from .sources.url_sources import get_url_sources
from .sources.search_queries import get_search_queries
from .sources.openai_prompts import get_system_prompt

class SudoStarExpert(BaseExpert):
    """Expert for handling SudoStar-related queries"""
    
    def __init__(self, config):
        """Initialize SudoStar expert
        
        Args:
            config: Expert configuration
        """
        super().__init__(config)
        self.event_bus = EventBus()
        self.knowledge_base = SUDOSTAR_KNOWLEDGE_BASE
        self.web_search = WebSearch()
        
        # Subscribe to events
        self.event_bus.subscribe('question_received', self._on_question_received)
        self.event_bus.subscribe('response_generated', self._on_response_generated)
        
    async def get_response(self, query: str) -> Optional[str]:
        """Generate response for SudoStar query
        
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
            system_prompt = get_system_prompt()
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
                
            return "Üzgünüm, bu SudoStar sorusuna yanıt üretemiyorum. Lütfen soruyu daha açık bir şekilde sorar mısınız?"
            
        except Exception as e:
            self.logger.error(f"Error generating SudoStar response: {str(e)}")
            return None
            
    async def _check_url_sources(self, query: str) -> Optional[str]:
        """Check URL sources for answer
        
        Args:
            query (str): User query
            
        Returns:
            Optional[str]: Response from URL sources or None
        """
        try:
            urls = get_url_sources()
            for url in urls:
                # URL'den bilgi çek ve yanıt oluştur
                pass
            return None
        except Exception as e:
            self.logger.error(f"Error checking URL sources: {str(e)}")
            return None
            
    async def _perform_web_search(self, query: str) -> Optional[str]:
        """Perform web search for answer
        
        Args:
            query (str): User query
            
        Returns:
            Optional[str]: Response from web search or None
        """
        try:
            search_queries = get_search_queries("pricing")
            for search_query in search_queries:
                results = await self.web_search.search(f"{search_query} {query}")
                if results:
                    return results[0]
            return None
        except Exception as e:
            self.logger.error(f"Error performing web search: {str(e)}")
            return None
            
    async def _on_question_received(self, question: str) -> None:
        """Handle received question event
        
        Args:
            question (str): Received question
        """
        self.logger.info(f"SudoStar expert received question: {question}")
        
    async def _on_response_generated(self, response: str) -> None:
        """Handle generated response event
        
        Args:
            response (str): Generated response
        """
        self.logger.info(f"SudoStar expert generated response: {response}") 