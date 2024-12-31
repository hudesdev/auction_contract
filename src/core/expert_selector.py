"""Expert selector module"""
import logging
from typing import Tuple, Optional
from src.utils.openai_client import OpenAIClient

class ExpertSelector:
    """Expert selector class for routing queries to appropriate experts"""
    
    def __init__(self):
        """Initialize expert selector"""
        self.logger = logging.getLogger(__name__)
        self.openai_client = OpenAIClient(
            model='gpt-4',
            max_tokens=100,
            temperature=0.3
        )
        
    async def select_expert(self, query: str) -> Tuple[Optional[str], Optional[str]]:
        """Select appropriate expert for query
        
        Args:
            query (str): User query
            
        Returns:
            Tuple[Optional[str], Optional[str]]: Expert type and direct response if no expert needed
        """
        try:
            system_prompt = """You are an expert classifier. Your task is to determine which expert should handle a given query.
            Available experts are:
            - sports: For sports and fitness related queries
            - food: For food, cooking, and nutrition related queries
            - ai: For artificial intelligence and technology related queries
            - sudostar: For questions about the SudoStar mobile application
            
            Respond with ONLY the expert type (sports/food/ai/sudostar) or 'none' if no specific expert is needed.
            If responding with 'none', also provide a brief direct response to the query."""
            
            response = await self.openai_client.get_completion(system_prompt, query)
            if not response:
                return None, None
                
            # Parse response
            response = response.strip().lower()
            if response.startswith(('sports', 'food', 'ai', 'sudostar')):
                return response.split()[0], None
                
            # If no specific expert needed, extract direct response
            if response.startswith('none'):
                direct_response = response[5:].strip()  # Remove 'none' prefix
                return None, direct_response if direct_response else None
                
            return None, None
            
        except Exception as e:
            self.logger.error(f"Error selecting expert: {str(e)}")
            return None, None 