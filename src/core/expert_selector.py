"""Expert seçici modülü"""
import logging
import json
from typing import Dict, Any, Optional
from src.utils.openai_client import OpenAIClient

logger = logging.getLogger(__name__)

class ExpertSelector:
    def __init__(self):
        """Initialize expert selector"""
        self.openai_client = OpenAIClient()
        
    async def select_expert(self, question: str) -> Optional[str]:
        """Select appropriate expert based on question

        Args:
            question (str): User's question

        Returns:
            Optional[str]: Selected expert type or None if no match
        """
        try:
            # Sistem promptu
            system_prompt = """Sen bir soru sınıflandırma uzmanısın.
            Verilen soruyu analiz edip en uygun uzmana yönlendirmelisin.
            Yanıtı JSON formatında ver: {"expert": string, "confidence": float}
            Expert tipleri: 
            - "sports": Futbol, basketbol, voleybol ve diğer sporlarla ilgili sorular
            - "food": Yemek tarifleri, restoranlar ve beslenme ile ilgili sorular
            - "ai": Yapay zeka teknolojileri ve uygulamaları ile ilgili sorular
            - "sudostar": SudoStar uygulaması, özellikleri ve ödeme sistemi ile ilgili sorular"""
            
            # Kullanıcı promptu
            user_prompt = f"Soru: {question}\n\nBu soru hangi uzmana yönlendirilmeli?"
            
            # OpenAI'dan yanıt al
            response = await self.openai_client.get_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
            
            # JSON yanıtı parse et
            try:
                result = json.loads(response)
                expert = result.get("expert")
                confidence = result.get("confidence", 0.0)
                
                # Güven skoru yeterli mi kontrol et
                if confidence >= 0.5:
                    return expert
                return None
                
            except json.JSONDecodeError:
                logger.error(f"Failed to parse expert selector response: {response}")
                return None
                
        except Exception as e:
            logger.error(f"Error selecting expert: {str(e)}")
            return None 