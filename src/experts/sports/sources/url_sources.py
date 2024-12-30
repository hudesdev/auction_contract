"""URL sources for sports expert"""
import os
import json
import logging
import aiohttp
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

def get_url_sources() -> Dict[str, List[str]]:
    """Load and return sports related URLs"""
    urls_path = os.path.join(os.path.dirname(__file__), "data", "url_sources.json")
    try:
        with open(urls_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "football": [
                "https://www.tff.org",
                "https://www.goal.com/tr",
                "https://www.mackolik.com"
            ],
            "basketball": [
                "https://www.tbf.org.tr",
                "https://www.eurohoops.net/tr"
            ],
            "volleyball": [
                "https://www.tvf.org.tr",
                "https://www.voleybolplus.com"
            ]
        }

async def fetch_url_content(url: str) -> Optional[str]:
    """Fetch content from URL
    
    Args:
        url (str): URL to fetch
        
    Returns:
        Optional[str]: Content if successful
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
    except Exception as e:
        logger.error(f"Error fetching URL {url}: {str(e)}")
    return None

async def search_url_sources(query: str) -> Optional[str]:
    """Search URL sources for relevant information
    
    Args:
        query (str): Search query
        
    Returns:
        Optional[str]: Relevant information if found
    """
    urls = get_url_sources()
    
    # Fetch content from relevant URLs
    relevant_content = []
    for category, url_list in urls.items():
        for url in url_list:
            content = await fetch_url_content(url)
            if content and query.lower() in content.lower():
                relevant_content.append(content)
                
    if relevant_content:
        # TODO: Implement better content extraction and summarization
        return "\n".join(relevant_content[:3])  # Return first 3 matches
        
    return None 