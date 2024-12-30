from typing import Any, Optional
import time
from collections import OrderedDict

class Cache:
    def __init__(self, enabled: bool = True, max_size: int = 1000, ttl: int = 3600):
        """Initialize cache
        
        Args:
            enabled (bool): Whether caching is enabled
            max_size (int): Maximum number of items to store
            ttl (int): Time to live in seconds
        """
        self.enabled = enabled
        self.max_size = max_size
        self.ttl = ttl
        self.cache = OrderedDict()  # {key: (value, timestamp)}
        
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache
        
        Args:
            key (str): Cache key
            
        Returns:
            Optional[Any]: Cached value or None if not found/expired
        """
        if not self.enabled:
            return None
            
        if key not in self.cache:
            return None
            
        value, timestamp = self.cache[key]
        
        # Check if expired
        if time.time() - timestamp > self.ttl:
            del self.cache[key]
            return None
            
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        
        return value
        
    def set(self, key: str, value: Any) -> None:
        """Set value in cache
        
        Args:
            key (str): Cache key
            value (Any): Value to cache
        """
        if not self.enabled:
            return
            
        # Remove oldest if at max size
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
            
        self.cache[key] = (value, time.time())
        
    def clear(self) -> None:
        """Clear all cached items"""
        self.cache.clear()
        
    def remove(self, key: str) -> None:
        """Remove item from cache
        
        Args:
            key (str): Cache key to remove
        """
        if key in self.cache:
            del self.cache[key] 