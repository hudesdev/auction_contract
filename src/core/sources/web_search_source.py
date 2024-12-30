from typing import Optional
from utils.logger import Logger
from core.tavily_client import TavilySearchClient

class WebSearchSource:
    """Web arama kaynak sınıfı"""
    
    def __init__(self):
        """Web arama kaynağını başlat"""
        self.logger = Logger("WebSearchSource")
        self.client = TavilySearchClient()
        
    def get_response(self, query: str) -> Optional[str]:
        """
        Web aramasından yanıt üret
        
        Args:
            query: Arama sorgusu
            
        Returns:
            str: Yanıt metni veya None
        """
        try:
            # Web'de ara
            results = self.client.search(query)
            if not results:
                return None
                
            # İlk sonucun içeriğini döndür
            for result in results:
                if content := result.get('content'):
                    return content
                if snippet := result.get('snippet'):
                    return snippet
                    
            return None
                
        except Exception as e:
            self.logger.error(f"Yanıt üretme hatası: {str(e)}")
            return None 