"""Sports expert module"""
from src.experts.base import BaseExpert

class SportsExpert(BaseExpert):
    """Sports expert class"""
    
    def __init__(self, config=None):
        """Initialize sports expert
        
        Args:
            config (dict, optional): Expert configuration. Defaults to None.
        """
        super().__init__(config)
        
    async def get_response(self, question: str) -> str:
        """Get response from sports expert
        
        Args:
            question (str): Question to answer
            
        Returns:
            str: Generated response
        """
        # TODO: Implement sports expert response
        return "I am a sports expert. I can help you with sports related questions." 