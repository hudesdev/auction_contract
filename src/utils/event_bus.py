"""Event bus for handling application events"""
import logging
from typing import Dict, List, Callable, Any

class EventBus:
    """Simple event bus implementation"""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        """Initialize event bus"""
        if self._initialized:
            return
            
        self.logger = logging.getLogger(__name__)
        self._subscribers: Dict[str, List[Callable]] = {}
        self._initialized = True
        
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe to an event
        
        Args:
            event_type (str): Event type to subscribe to
            callback (Callable): Callback function to execute when event occurs
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
            
        self._subscribers[event_type].append(callback)
        self.logger.info(f"'{event_type}' event'ine yeni abone eklendi")
        
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe from an event
        
        Args:
            event_type (str): Event type to unsubscribe from
            callback (Callable): Callback function to remove
        """
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)
            self.logger.info(f"'{event_type}' event'inden abone çıkarıldı")
            
    async def publish(self, event_type: str, data: Any = None) -> None:
        """Publish an event
        
        Args:
            event_type (str): Event type to publish
            data (Any, optional): Event data to pass to subscribers. Defaults to None.
        """
        if event_type not in self._subscribers:
            return
            
        self.logger.info(f"'{event_type}' event'i yayınlandı")
        for callback in self._subscribers[event_type]:
            try:
                if data is not None:
                    await callback(data)
                else:
                    await callback()
            except Exception as e:
                self.logger.error(f"Event handler error: {str(e)}")
                
    def clear(self) -> None:
        """Clear all subscribers"""
        self._subscribers.clear()
        self.logger.info("Tüm abonelikler temizlendi") 