"""OpenAI API client wrapper"""
import os
import logging
from typing import Optional
from openai import OpenAI, AsyncOpenAI

class OpenAIClient:
    """OpenAI API client wrapper"""
    
    def __init__(self, model: str = 'gpt-4', max_tokens: int = 300, temperature: float = 0.7):
        """Initialize OpenAI client
        
        Args:
            model (str, optional): Model to use. Defaults to 'gpt-4'.
            max_tokens (int, optional): Maximum tokens to generate. Defaults to 300.
            temperature (float, optional): Temperature for response generation. Defaults to 0.7.
        """
        self.logger = logging.getLogger(__name__)
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        self.logger.info("OpenAI client initialized successfully")
        
    async def get_completion(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Get completion from OpenAI API
        
        Args:
            system_prompt (str): System prompt to guide response
            user_prompt (str): User prompt to generate response for
            
        Returns:
            Optional[str]: Generated response or None if failed
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error getting completion: {str(e)}")
            return None 