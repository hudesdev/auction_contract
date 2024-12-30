"""OpenAI prompts for sports expert"""
import logging
from typing import Optional
from src.utils.openai_client import OpenAIClient

logger = logging.getLogger(__name__)

async def get_openai_response(question: str) -> Optional[str]:
    """Get response from OpenAI
    
    Args:
        question (str): User's question
        
    Returns:
        Optional[str]: Response if found, None otherwise
    """
    try:
        client = OpenAIClient()
        
        system_prompt = """Sen bir spor uzmanısın.
        Futbol, basketbol, voleybol ve diğer sporlar hakkında detaylı bilgi sahibisin.
        Türk ve dünya sporuna hakimsin.
        Soruları kısa ve öz bir şekilde yanıtla."""
        
        user_prompt = f"Soru: {question}\n\nYanıt:"
        
        response = await client.get_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )
        
        if response and len(response.strip()) > 0:
            return response.strip()
            
        return None
        
    except Exception as e:
        logger.error(f"Error getting OpenAI response: {str(e)}")
        return None 