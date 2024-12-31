"""Base expert module"""
from abc import ABC, abstractmethod
import logging

class BaseExpert(ABC):
    """Base expert class"""
    
    def __init__(self, config=None):
        """Initialize base expert
        
        Args:
            config (dict, optional): Expert configuration. Defaults to None.
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
    @abstractmethod
    async def get_response(self, question: str) -> str:
        """Get response from expert
        
        Args:
            question (str): Question to answer
            
        Returns:
            str: Generated response
        """
        pass 