"""Base expert class for all expert types"""
import logging
from typing import Optional, Dict, Any
from src.utils.openai_client import OpenAIClient
from src.utils.web_search import WebSearchClient
from src.utils.cache import Cache

class BaseExpert:
    """Base expert class that all other experts inherit from"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the expert with configuration
        
        Args:
            config (Dict[str, Any]): Expert configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI client
        openai_config = config.get('openai', {})
        self.openai_client = OpenAIClient(
            model=openai_config.get('model', 'gpt-4'),
            max_tokens=openai_config.get('max_tokens', 300),
            temperature=openai_config.get('temperature', 0.7)
        )
        
        # Initialize web search client if Tavily config exists
        self.web_search = None
        tavily_config = config.get('tavily', {})
        if tavily_config:
            self.web_search = WebSearchClient(
                max_results=tavily_config.get('max_results', 5),
                search_depth=tavily_config.get('search_depth', 'advanced')
            )
            
        # Initialize cache if enabled
        self.cache = None
        if config.get('cache_enabled', True):
            self.cache = Cache(
                enabled=True,
                ttl=config.get('cache_ttl', 3600)
            )
            
    async def get_response(self, query: str) -> Optional[str]:
        """Main response generation pipeline
        
        Args:
            query (str): User query to respond to
            
        Returns:
            Optional[str]: Generated response or None if failed
        """
        raise NotImplementedError("Subclasses must implement get_response method")
        
    async def _check_local_knowledge(self, query: str) -> Optional[str]:
        """Check local knowledge base for relevant information
        
        Args:
            query (str): User query to check against local knowledge
            
        Returns:
            Optional[str]: Response from local knowledge or None if not found
        """
        return None
        
    async def _check_url_sources(self, query: str) -> Optional[str]:
        """Check URL sources for relevant information
        
        Args:
            query (str): User query to check against URL sources
            
        Returns:
            Optional[str]: Response from URL sources or None if not found
        """
        return None
        
    async def _generate_ai_response(self, query: str) -> Optional[str]:
        """Generate response using OpenAI
        
        Args:
            query (str): User query to generate response for
            
        Returns:
            Optional[str]: Generated response or None if failed
        """
        try:
            system_prompt = """You are an expert assistant. Provide accurate and helpful responses
            about your area of expertise. If you're not confident about the answer, indicate that."""
            
            response = await self.openai_client.get_completion(system_prompt, query)
            return response
        except Exception as e:
            self.logger.error(f"Error generating AI response: {str(e)}")
            return None
            
    async def _perform_web_search(self, query: str) -> Optional[str]:
        """Perform web search for relevant information
        
        Args:
            query (str): User query to search for
            
        Returns:
            Optional[str]: Response from web search or None if failed
        """
        if not self.web_search:
            return None
            
        try:
            return await self.web_search.search(query)
        except Exception as e:
            self.logger.error(f"Error performing web search: {str(e)}")
            return None 