"""OpenAI API client"""
import os
import logging
from typing import Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

class OpenAIClient:
    """OpenAI API client"""
    
    def __init__(self):
        """Initialize OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY not found!")
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        logger.info("OpenAI client initialized successfully")
        
    async def get_completion(self, system_prompt: str, user_prompt: str = None) -> Optional[str]:
        """Get completion from OpenAI API
        
        Args:
            system_prompt (str): System prompt
            user_prompt (str, optional): User prompt. Defaults to None.
            
        Returns:
            Optional[str]: Generated response or None if error
        """
        try:
            messages = [{"role": "system", "content": system_prompt}]
            if user_prompt:
                messages.append({"role": "user", "content": user_prompt})
                
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return None 