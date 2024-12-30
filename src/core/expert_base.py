"""Base class for all experts"""
from typing import Optional
from src.utils.openai_client import OpenAIClient

class ExpertBase:
    def __init__(self, expert_type: str, system_message: str = None):
        """Initialize expert
        
        Args:
            expert_type (str): Type of expert (spor, yemek, ai)
            system_message (str, optional): System message for the expert
        """
        self.expert_type = expert_type
        self.system_message = system_message or ""
        self.openai_client = OpenAIClient()
        
    async def get_response(self, message: str) -> Optional[str]:
        """Get response for the message
        
        Args:
            message (str): User's message
            
        Returns:
            Optional[str]: Response or None if no answer found
        """
        try:
            response = await self.openai_client.get_completion(self.system_message, message)
            return response
        except Exception as e:
            print(f"Error getting response: {str(e)}")
            return None 