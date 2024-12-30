"""Web search functionality using Tavily API"""
import os
import logging
from typing import Optional
from tavily import TavilyClient

logger = logging.getLogger(__name__)

class WebSearch:
    def __init__(self):
        """Initialize WebSearch with Tavily API"""
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
    async def search(self, query: str) -> Optional[str]:
        """Search web using Tavily API
        
        Args:
            query (str): Search query
            
        Returns:
            Optional[str]: Search result or None if not found
        """
        try:
            # Tavily API'yi kullanarak arama yap
            response = self.client.search(
                query=query,
                search_depth="advanced",  # Detaylı arama
                max_results=3,  # En alakalı 3 sonuç
                language="tr"  # Türkçe sonuçlar
            )
            
            if not response or not response.get("results"):
                logger.warning("No results found from Tavily search")
                return None
                
            # Sonuçları birleştir
            results = response["results"]
            content = "\n\n".join([
                f"Başlık: {result['title']}\n"
                f"İçerik: {result['content']}"
                for result in results
            ])
            
            return content
            
        except Exception as e:
            logger.error(f"Error in Tavily search: {str(e)}")
            return None 