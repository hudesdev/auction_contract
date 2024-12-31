"""Expert selector module"""
import logging
from typing import Optional, Tuple

from src.utils.openai_client import OpenAIClient

logger = logging.getLogger(__name__)

class ExpertSelector:
    """Expert selector class"""
    
    def __init__(self):
        """Initialize expert selector"""
        self.openai_client = OpenAIClient()
        
    async def select_expert(self, question: str) -> Tuple[Optional[str], Optional[str]]:
        """Select appropriate expert for question
        
        Args:
            question (str): User's question
            
        Returns:
            Tuple[Optional[str], Optional[str]]: Expert type and direct response if any
        """
        try:
            messages = [
                {"role": "system", "content": """Sen bir uzman seçici sistemsin. Kullanıcının sorusuna göre hangi uzmanın yanıt vermesi gerektiğine karar verirsin.

Mevcut uzmanlar:
- sports: Spor, futbol, basketbol vb. konular
- food: Yemek, mutfak, tarifler vb. konular
- ai: Yapay zeka, teknoloji vb. konular
- sudostar: SudoStar uygulaması, elmas, ödeme vb. konular

Eğer soru bu uzmanlardan hiçbirine uygun değilse None döndür."""},
                {"role": "user", "content": question}
            ]
            
            response = await self.openai_client.chat_completion(messages)
            
            # Parse response to get expert type
            response = response.lower().strip()
            if any(expert in response for expert in ['sports', 'food', 'ai', 'sudostar']):
                for expert in ['sports', 'food', 'ai', 'sudostar']:
                    if expert in response:
                        return expert, None
            
            return None, "Üzgünüm, bu soruya yanıt verebilecek uygun bir uzman bulamadım."
            
        except Exception as e:
            logger.error(f"Error selecting expert: {str(e)}")
            return None, None 