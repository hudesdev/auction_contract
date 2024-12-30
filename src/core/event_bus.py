from typing import Dict, List, Callable
from src.utils.logger import Logger

class EventBus:
    """Event bus sistemi - Expertler arası iletişim için"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if not self._initialized:
            self.logger = Logger("EventBus")
            self.subscribers: Dict[str, List[Callable]] = {}
            self._initialized = True
            
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Event'e abone ol"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        self.logger.info(f"'{event_type}' event'ine yeni abone eklendi")
        
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Event aboneliğini iptal et"""
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)
            self.logger.info(f"'{event_type}' event'inden abonelik kaldırıldı")
            
    def unsubscribe_all(self, callback: Callable) -> None:
        """Tüm event'lerden aboneliği iptal et
        
        Args:
            callback (Callable): İptal edilecek callback fonksiyonu
        """
        for event_type in list(self.subscribers.keys()):
            if callback in self.subscribers[event_type]:
                self.subscribers[event_type].remove(callback)
                self.logger.info(f"'{event_type}' event'inden abonelik kaldırıldı")
            
    def publish(self, event_type: str, data: dict = None) -> None:
        """Event yayınla"""
        if event_type in self.subscribers:
            self.logger.info(f"'{event_type}' event'i yayınlanıyor")
            for callback in self.subscribers[event_type]:
                try:
                    callback(data or {})
                except Exception as e:
                    self.logger.error(f"Event işleme hatası: {str(e)}")
                    
    def clear(self) -> None:
        """Tüm abonelikleri temizle"""
        self.subscribers.clear()
        self.logger.info("Tüm event abonelikleri temizlendi") 