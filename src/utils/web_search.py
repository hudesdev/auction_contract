"""Web search utility"""
import logging
import os
from typing import List, Optional, Dict, Any
import aiohttp
from tavily import TavilyClient

logger = logging.getLogger(__name__)

class WebSearchClient:
    def __init__(self):
        self.api_key = os.getenv('TAVILY_API_KEY')
        if not self.api_key:
            logger.warning('TAVILY_API_KEY not found in environment variables')
        else:
            self.client = TavilyClient(api_key=self.api_key)
            logger.info('Web search client initialized successfully')

    async def search(self, query: str) -> list:
        if not self.api_key:
            return []
        try:
            response = self.client.search(query=query)
            return response.get('results', [])
        except Exception as e:
            logger.error(f'Error in web search: {str(e)}')
            return [] 