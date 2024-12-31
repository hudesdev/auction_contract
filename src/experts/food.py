"""Food expert module"""
from src.experts.base import BaseExpert

class FoodExpert(BaseExpert):
    """Food expert class"""
    
    def __init__(self, config=None):
        """Initialize food expert
        
        Args:
            config (dict, optional): Expert configuration. Defaults to None.
        """
        super().__init__(config=config)
        
    async def get_response(self, question: str) -> str:
        """Get response from food expert
        
        Args:
            question (str): Question to answer
            
        Returns:
            str: Generated response
        """
        # TODO: Implement food expert response
        return "I am a food expert. I can help you with food related questions." 