"""Web search client using Tavily API"""
import os
import logging
from typing import List, Optional
from tavily import TavilyClient

logger = logging.getLogger(__name__)

class WebSearchClient:
    """Web search client using Tavily API"""
    
    def __init__(self):
        """Initialize web search client"""
        api_key = os.getenv('TAVILY_API_KEY')
        if not api_key:
            logger.error("TAVILY_API_KEY not found!")
            raise ValueError("TAVILY_API_KEY environment variable is not set")
        self.client = TavilyClient(api_key=api_key)
        logger.info("Web search client initialized successfully")
        
    async def search(self, query: str, max_results: int = 3) -> Optional[List[str]]:
        """Perform web search
        
        Args:
            query (str): Search query
            max_results (int, optional): Maximum number of results. Defaults to 3.
            
        Returns:
            Optional[List[str]]: List of search results or None if error
        """
        try:
            # Perform search
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results
            )
            
            # Extract content from results
            results = []
            for result in response.get('results', []):
                content = result.get('content')
                if content:
                    results.append(content)
                    
            return results if results else None
            
        except Exception as e:
            logger.error(f"Web search error: {str(e)}")
            return None 