from typing import Optional
from utils.logger import Logger

class LocalSource:
    """Yerel kaynak sınıfı - Temel sınıf"""
    
    def __init__(self):
        """Yerel kaynağı başlat"""
        self.logger = Logger("LocalSource")
        
    def get_response(self, message: str) -> Optional[str]:
        """
        Yerel veritabanından yanıt üret
        
        Args:
            message: Gelen mesaj
            
        Returns:
            str: Yanıt metni veya None
        """
        try:
            # Bu metod alt sınıflar tarafından override edilmeli
            return None
                
        except Exception as e:
            self.logger.error(f"Yanıt üretme hatası: {str(e)}")
            return None 