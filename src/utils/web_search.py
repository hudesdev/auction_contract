"""Web search utility"""
import logging
import os
from typing import List, Optional, Dict, Any
import aiohttp
from tavily import TavilyClient

class WebSearchClient:
    """Web search client using Tavily API"""
    
    def __init__(self, max_results: int = 5, search_depth: str = 'advanced'):
        """Initialize web search client
        
        Args:
            max_results (int, optional): Maximum number of results to return. Defaults to 5.
            search_depth (str, optional): Search depth level. Defaults to 'advanced'.
        """
        self.logger = logging.getLogger(__name__)
        
        api_key = os.getenv('TAVILY_API_KEY')
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable is not set")
            
        self.client = TavilyClient(api_key=api_key)
        self.max_results = max_results
        self.search_depth = search_depth
        
        self.logger.info("Web search client initialized successfully")
        
    async def search(self, query: str) -> Optional[str]:
        """Perform web search
        
        Args:
            query (str): Search query
            
        Returns:
            Optional[str]: Search results summary or None if failed
        """
        try:
            response = await self.client.search(
                query=query,
                max_results=self.max_results,
                search_depth=self.search_depth
            )
            
            if not response or 'results' not in response:
                return None
                
            # Extract relevant information from results
            results = response['results']
            if not results:
                return None
                
            # Combine titles and snippets
            summary = []
            for result in results:
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                if title and snippet:
                    summary.append(f"{title}: {snippet}")
                    
            return "\n\n".join(summary) if summary else None
            
        except Exception as e:
            self.logger.error(f"Error performing web search: {str(e)}")
            return None

class WebSearch:
    """Simple web search client"""
    
    def __init__(self):
        """Initialize web search client"""
        self.logger = logging.getLogger(__name__)
        
    async def search(self, query: str) -> Optional[List[str]]:
        """Perform web search
        
        Args:
            query (str): Search query
            
        Returns:
            Optional[List[str]]: Search results or None if failed
        """
        try:
            # Burada gerçek bir web araması yapılabilir
            # Şimdilik sadece query'yi döndürelim
            return [query]
        except Exception as e:
            self.logger.error(f"Error performing web search: {str(e)}")
            return None 