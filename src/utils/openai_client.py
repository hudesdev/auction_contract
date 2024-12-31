"""OpenAI client module"""
import os
import logging
from openai import OpenAI, AsyncOpenAI

logger = logging.getLogger(__name__)

def init_openai():
    """Initialize OpenAI API key
    
    Returns:
        str: OpenAI API key or None if not found
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.error('OPENAI_API_KEY not found in environment variables')
        return None
    return api_key

class OpenAIClient:
    """OpenAI client class"""
    
    def __init__(self):
        """Initialize OpenAI client"""
        self.api_key = init_openai()
        if not self.api_key:
            logger.warning('OpenAI client initialized without API key')
        else:
            self.client = AsyncOpenAI(api_key=self.api_key)
            logger.info('OpenAI client initialized successfully')
            
    async def chat_completion(self, messages: list) -> str:
        """Get chat completion from OpenAI
        
        Args:
            messages (list): List of message dictionaries
            
        Returns:
            str: Generated response
        """
        try:
            if not self.api_key:
                return "OpenAI API key not configured"
                
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f'Error in chat completion: {str(e)}')
            return None 