"""Web search utility"""
import logging
from typing import Optional
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class WebSearch:
    def __init__(self):
        """Initialize web search"""
        self.search_url = "https://www.google.com/search"
        
    async def search(self, query: str) -> Optional[str]:
        """Search web for answer
        
        Args:
            query (str): Search query
            
        Returns:
            Optional[str]: Answer from web or None if not found
        """
        try:
            # Format query
            params = {
                "q": query,
                "hl": "tr",
                "gl": "tr"
            }
            
            # Make request
            async with aiohttp.ClientSession() as session:
                async with session.get(self.search_url, params=params) as response:
                    if response.status == 200:
                        # Parse response
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        
                        # Try to find answer in featured snippet
                        if snippet := soup.find("div", {"class": "ILfuVd"}):
                            return snippet.get_text()
                            
                        # Try to find answer in knowledge panel
                        if panel := soup.find("div", {"class": "kno-rdesc"}):
                            return panel.get_text()
                            
                        # Try to find answer in search results
                        if results := soup.find_all("div", {"class": "BNeawe"}):
                            return results[0].get_text()
                            
            return None
            
        except Exception as e:
            logger.error(f"Error searching web: {str(e)}", exc_info=True)
            return None 