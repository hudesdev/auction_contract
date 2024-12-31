"""Cache utility for storing responses"""
import time
from typing import Dict, Any, Optional

class Cache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self, enabled: bool = True, ttl: int = 3600):
        """Initialize cache
        
        Args:
            enabled (bool, optional): Whether caching is enabled. Defaults to True.
            ttl (int, optional): Time to live in seconds. Defaults to 3600 (1 hour).
        """
        self.enabled = enabled
        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        
    def get(self, key: str) -> Optional[str]:
        """Get value from cache if not expired
        
        Args:
            key (str): Cache key
            
        Returns:
            Optional[str]: Cached value or None if expired/not found
        """
        if not self.enabled:
            return None
            
        if key not in self._cache:
            return None
            
        cache_data = self._cache[key]
        if time.time() - cache_data['timestamp'] > self.ttl:
            del self._cache[key]
            return None
            
        return cache_data['value']
        
    def set(self, key: str, value: str) -> None:
        """Set value in cache with current timestamp
        
        Args:
            key (str): Cache key
            value (str): Value to cache
        """
        if not self.enabled:
            return
            
        self._cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
        
    def clear(self) -> None:
        """Clear all cached values"""
        self._cache.clear()
        
    def remove(self, key: str) -> None:
        """Remove specific key from cache
        
        Args:
            key (str): Cache key to remove
        """
        if key in self._cache:
            del self._cache[key]
            
    def cleanup(self) -> None:
        """Remove all expired entries"""
        if not self.enabled:
            return
            
        current_time = time.time()
        expired_keys = [
            key for key, data in self._cache.items()
            if current_time - data['timestamp'] > self.ttl
        ]
        for key in expired_keys:
            del self._cache[key] 