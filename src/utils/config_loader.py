import json
import os
import logging
from typing import Dict, Any, Optional

class ConfigError(Exception):
    """Yapılandırma ile ilgili hatalar için özel istisna"""
    pass

class ConfigLoader:
    def __init__(self, config_dir='config', required_fields: Dict[str, Any] = None):
        self.config_dir = config_dir
        self.required_fields = required_fields or {}
        self.logger = logging.getLogger(__name__)
        
        # Yapılandırma dizinini oluştur
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            
    def _validate_config(self, config: Dict[str, Any], config_name: str) -> None:
        """Yapılandırmayı doğrula"""
        for field, default in self.required_fields.items():
            if field not in config:
                if default is None:
                    raise ConfigError(f"'{config_name}' yapılandırmasında zorunlu alan eksik: {field}")
                config[field] = default
                
    def load_config(self, config_name: str) -> Dict[str, Any]:
        """Yapılandırma dosyasını yükle"""
        config_path = os.path.join(self.config_dir, f"{config_name}.json")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self._validate_config(config, config_name)
                return config
        except FileNotFoundError:
            self.logger.warning(f"Yapılandırma dosyası bulunamadı: {config_path}")
            # Varsayılan yapılandırmayı oluştur
            config = {k: v for k, v in self.required_fields.items() if v is not None}
            self.save_config(config_name, config)
            return config
        except json.JSONDecodeError as e:
            raise ConfigError(f"Yapılandırma dosyası geçersiz JSON formatı: {str(e)}")
            
    def save_config(self, config_name: str, config_data: Dict[str, Any]) -> None:
        """Yapılandırma dosyasını kaydet"""
        config_path = os.path.join(self.config_dir, f"{config_name}.json")
        
        try:
            # Yapılandırmayı doğrula
            self._validate_config(config_data, config_name)
            
            # Dizin yoksa oluştur
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise ConfigError(f"Yapılandırma kaydedilemedi: {str(e)}")
            
    def update_config(self, config_name: str, updates: Dict[str, Any]) -> None:
        """Mevcut yapılandırmayı güncelle"""
        try:
            config = self.load_config(config_name)
            config.update(updates)
            self.save_config(config_name, config)
        except Exception as e:
            raise ConfigError(f"Yapılandırma güncellenemedi: {str(e)}")
            
    def get_value(self, config_name: str, key: str, default: Any = None) -> Any:
        """Yapılandırmadan değer al"""
        try:
            config = self.load_config(config_name)
            return config.get(key, default)
        except Exception as e:
            self.logger.error(f"Yapılandırma değeri alınamadı: {str(e)}")
            return default
            
    def ensure_config_exists(self, config_name: str, template: Dict[str, Any]) -> None:
        """Yapılandırma dosyasının varlığını kontrol et ve yoksa oluştur"""
        if not os.path.exists(os.path.join(self.config_dir, f"{config_name}.json")):
            self.save_config(config_name, template) 