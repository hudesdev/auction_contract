"""Base expert module"""
import logging
from typing import Optional

from src.utils.openai_client import OpenAIClient
from src.utils.web_search import WebSearchClient

logger = logging.getLogger(__name__)

class BaseExpert:
    """Base expert class"""
    
    def __init__(self):
        """Initialize base expert"""
        self.openai_client = OpenAIClient()
        self.web_search = WebSearchClient()
        
    async def get_response(self, question: str) -> Optional[str]:
        """Get response for question
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Response or None if not applicable
        """
        raise NotImplementedError("Subclasses must implement get_response method") 