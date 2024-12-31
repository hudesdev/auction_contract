"""SudoStar expert konfigürasyon dosyası"""
from typing import Dict, Any
import os

def get_expert_config() -> Dict[str, Any]:
    """Returns expert configuration
    
    Returns:
        Dict[str, Any]: Expert configuration
    """
    return {
        'name': 'sudostar',
        'description': 'SudoStar mobile application expert',
        
        # OpenAI yapılandırması
        'openai': {
            'api_key': os.getenv('OPENAI_API_KEY'),
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        },
        
        # Yerel veri yapılandırması
        'local': {
            'data_file': 'sudostar_knowledge.json',
            'update_interval': 3600  # 1 saat
        },
        
        # URL yapılandırması
        'url': {
            'sources': [
                'https://sudostar.com',
                'https://docs.sudostar.com',
                'https://support.sudostar.com'
            ],
            'update_interval': 7200  # 2 saat
        },
        
        # Sistem mesajları
        'prompts': {
            'system': {
                'general': """Sen bir SudoStar uzmanısın. Aşağıdaki bilgileri kullanarak kısa ve net yanıtlar ver:
                - 1 USD = 5000 elmas (1000 elmas = 0.2 USD)
                - Minimum çekim: 25000 elmas
                - Ödeme süresi: 1-3 iş günü
                - Ödeme yöntemleri: PayPal, Banka transferi, Kripto cüzdan
                
                Kullanıcının sorusuna SADECE ilgili fiyat bilgisini ver. Fazladan açıklama yapma."""
            }
        }
    } 