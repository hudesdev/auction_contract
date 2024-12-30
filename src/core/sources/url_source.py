from typing import Optional, List
from utils.logger import Logger

class URLSource:
    """URL kaynak sınıfı - Temel sınıf"""
    
    def __init__(self):
        """URL kaynağını başlat"""
        self.logger = Logger("URLSource")
        
    def get_response(self, message: str, urls: List[str] = None) -> Optional[str]:
        """
        URL'lerden yanıt üret
        
        Args:
            message: Gelen mesaj
            urls: Kontrol edilecek URL'ler (opsiyonel)
            
        Returns:
            str: Yanıt metni veya None
        """
        try:
            # Bu metod alt sınıflar tarafından override edilmeli
            return None
                
        except Exception as e:
            self.logger.error(f"Yanıt üretme hatası: {str(e)}")
            return None 