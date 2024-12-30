"""Yapılandırma yükleyici"""
import os
import json
from typing import Dict, Any

class ConfigLoader:
    """Yapılandırma yükleyici sınıfı"""
    
    @staticmethod
    def load_config(config_name: str = None) -> Dict[str, Any]:
        """Yapılandırma dosyasını yükle
        
        Args:
            config_name (str, optional): Yapılandırma dosyası adı. Defaults to None.
            
        Returns:
            Dict[str, Any]: Yapılandırma sözlüğü
        """
        # Varsayılan yapılandırma
        config = {
            "experts": {
                "sports": {
                    "cache_enabled": True,
                    "cache_ttl": 3600,
                    "openai": {
                        "model": "gpt-4",
                        "max_tokens": 300,
                        "temperature": 0.7
                    },
                    "tavily": {
                        "max_results": 5,
                        "search_depth": "advanced"
                    }
                },
                "food": {
                    "cache_enabled": True,
                    "cache_ttl": 3600,
                    "openai": {
                        "model": "gpt-4",
                        "max_tokens": 300,
                        "temperature": 0.7
                    },
                    "tavily": {
                        "max_results": 5,
                        "search_depth": "advanced"
                    }
                },
                "ai": {
                    "cache_enabled": True,
                    "cache_ttl": 3600,
                    "openai": {
                        "model": "gpt-4",
                        "max_tokens": 300,
                        "temperature": 0.7
                    },
                    "tavily": {
                        "max_results": 5,
                        "search_depth": "advanced"
                    }
                }
            },
            "api_keys": {
                "openai": os.getenv("OPENAI_API_KEY"),
                "tavily": os.getenv("TAVILY_API_KEY")
            }
        }
        
        # Özel yapılandırma dosyası varsa yükle
        if config_name:
            config_path = os.path.join("config", f"{config_name}.json")
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    custom_config = json.load(f)
                    # Özel yapılandırmayı varsayılan ile birleştir
                    config.update(custom_config)
                    
        return config 