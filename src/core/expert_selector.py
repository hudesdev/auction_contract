"""Expert seçici modülü"""
import logging
import json
from typing import Dict, Any, Optional, Tuple
from src.utils.openai_client import OpenAIClient
from src.utils.web_search import WebSearchClient

logger = logging.getLogger(__name__)

class ExpertSelector:
    def __init__(self):
        """Initialize expert selector"""
        self.openai_client = OpenAIClient()
        self.web_search = WebSearchClient()
        
    async def select_expert(self, question: str) -> Tuple[Optional[str], Optional[str]]:
        """Select appropriate expert based on question or generate response

        Args:
            question (str): User's question

        Returns:
            Tuple[Optional[str], Optional[str]]: (Selected expert type, Generated response if no expert)
        """
        try:
            # Sistem promptu
            system_prompt = """Sen bir soru sınıflandırma uzmanısın.
            Verilen soruyu analiz edip en uygun uzmana yönlendirmelisin.
            Yanıtı JSON formatında ver: {"expert": string, "confidence": float, "needs_current_data": boolean}
            Expert tipleri: 
            - "sports": Futbol, basketbol, voleybol ve diğer sporlarla ilgili sorular
            - "food": Yemek tarifleri, restoranlar ve beslenme ile ilgili sorular
            - "ai": Yapay zeka teknolojileri ve uygulamaları ile ilgili sorular
            - "sudostar": SudoStar uygulaması, özellikleri ve ödeme sistemi ile ilgili sorular
            
            Eğer soru bu expertlerden hiçbirine uygun değilse expert alanını null olarak döndür.
            needs_current_data alanı sorunun güncel veri gerektirip gerektirmediğini belirtir (örn: hava durumu, borsa, güncel haberler)."""
            
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
                needs_current_data = result.get("needs_current_data", False)
                
                # Güven skoru yeterli mi kontrol et
                if confidence >= 0.5 and expert:
                    return expert, None
                    
                # Expert bulunamadıysa veya güven skoru düşükse
                if needs_current_data:
                    # Web araması yap
                    search_results = await self.web_search.search(question)
                    if search_results:
                        # OpenAI ile yanıt üret
                        response = await self._generate_response_from_search(question, search_results)
                        if response:
                            # Yanıt doğruluğunu kontrol et
                            if await self._validate_response(response, search_results):
                                return None, response
                
                # Web araması başarısız olduysa veya güncel veri gerekmiyorsa
                # OpenAI ile direkt yanıt üret
                direct_response = await self._generate_direct_response(question)
                return None, direct_response
                
            except json.JSONDecodeError:
                logger.error(f"Failed to parse expert selector response: {response}")
                return None, None
                
        except Exception as e:
            logger.error(f"Error selecting expert: {str(e)}")
            return None, None
            
    async def _generate_response_from_search(self, question: str, search_results: list) -> Optional[str]:
        """Generate response using web search results"""
        try:
            context = "\n".join(search_results[:3])
            system_prompt = """Web arama sonuçlarını kullanarak soruya kapsamlı ve doğru bir yanıt üretmelisin.
            Yanıt üretirken şu kurallara uy:
            1. Web arama sonuçlarındaki bilgilerin doğruluğunu kontrol et
            2. Bilgilerin güncelliğini kontrol et
            3. Çelişkili bilgiler varsa en güvenilir kaynağı seç
            4. Emin olmadığın bilgileri verme
            5. Yanıtı net ve anlaşılır bir şekilde ver"""
            
            response = await self.openai_client.get_completion(
                system_prompt=system_prompt,
                user_prompt=f"Soru: {question}\n\nWeb arama sonuçları:\n{context}"
            )
            return response
        except Exception as e:
            logger.error(f"Error generating response from search: {str(e)}")
            return None
            
    async def _validate_response(self, response: str, search_results: list) -> bool:
        """Validate generated response"""
        try:
            context = "\n".join(search_results[:3])
            system_prompt = """Web arama sonuçlarından üretilen yanıtın doğruluğunu kontrol et.
            Yanıt güvenilir ve güncel bilgiler içeriyorsa onay ver.
            Yanıt JSON formatında olmalı: {"is_valid": boolean, "reason": string}"""
            
            validation = await self.openai_client.get_completion(
                system_prompt=system_prompt,
                user_prompt=f"Yanıt: {response}\n\nKaynaklar:\n{context}"
            )
            
            try:
                result = json.loads(validation)
                return result.get("is_valid", False)
            except:
                return False
                
        except Exception as e:
            logger.error(f"Error validating response: {str(e)}")
            return False
            
    async def _generate_direct_response(self, question: str) -> Optional[str]:
        """Generate direct response using OpenAI"""
        try:
            system_prompt = """Sen bir genel bilgi asistanısın.
            Soruya mevcut bilgi birikimini kullanarak kapsamlı ve doğru bir yanıt üretmelisin.
            Emin olmadığın konularda bunu belirtmelisin."""
            
            response = await self.openai_client.get_completion(
                system_prompt=system_prompt,
                user_prompt=question
            )
            return response
        except Exception as e:
            logger.error(f"Error generating direct response: {str(e)}")
            return None 