from typing import Optional
from utils.logger import Logger

class OpenAISource:
    """OpenAI kaynak sınıfı - Temel sınıf"""
    
    def __init__(self):
        """OpenAI kaynağını başlat"""
        self.logger = Logger("OpenAISource")
        
    def get_response(self, message: str, system_prompt: str = None) -> Optional[str]:
        """
        OpenAI API'den yanıt üret
        
        Args:
            message: Gelen mesaj
            system_prompt: Sistem promptu (opsiyonel)
            
        Returns:
            str: Yanıt metni veya None
        """
        try:
            # Bu metod alt sınıflar tarafından override edilmeli
            return None
                
        except Exception as e:
            self.logger.error(f"Yanıt üretme hatası: {str(e)}")
            return None 