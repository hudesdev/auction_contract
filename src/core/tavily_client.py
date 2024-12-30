"""Tavily API istemcisi"""
import os
import logging
from typing import List, Dict, Any, Optional
import aiohttp

logger = logging.getLogger(__name__)

class TavilyClient:
    """Tavily API istemcisi"""
    
    def __init__(self):
        """Initialize Tavily client"""
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY environment variable is not set")
            
        self.base_url = "https://api.tavily.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    async def search(
        self,
        query: str,
        search_depth: str = "advanced",
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Web araması yap
        
        Args:
            query (str): Arama sorgusu
            search_depth (str): Arama derinliği ("basic" veya "advanced")
            include_domains (List[str], optional): Dahil edilecek domainler
            exclude_domains (List[str], optional): Hariç tutulacak domainler
            max_results (int): Maksimum sonuç sayısı
            
        Returns:
            List[Dict[str, Any]]: Arama sonuçları
        """
        try:
            url = f"{self.base_url}/search"
            
            data = {
                "query": query,
                "search_depth": search_depth,
                "max_results": max_results
            }
            
            if include_domains:
                data["include_domains"] = include_domains
            if exclude_domains:
                data["exclude_domains"] = exclude_domains
                
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self.headers, json=data) as response:
                    response.raise_for_status()
                    result = await response.json()
                    results = result.get("results", [])
                    return results[:max_results]
            
        except Exception as e:
            logger.error(f"Tavily arama hatası: {str(e)}")
            return [] 