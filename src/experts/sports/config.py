from typing import Dict, Any
import os

def load_sports_expert_config() -> Dict[str, Any]:
    """Spor uzmanı için yapılandırma yükle"""
    return {
        'name': 'SportsExpert',
        'description': 'Spor ve fitness konularında uzman AI asistan',
        
        # OpenAI yapılandırması
        'openai': {
            'api_key': os.getenv('OPENAI_API_KEY'),
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        },
        
        # Yerel dosya yapılandırması
        'local': {
            'data_file': 'sports_knowledge.json',
            'update_interval': 3600  # 1 saat
        },
        
        # URL yapılandırması
        'url': {
            'sources': [
                'https://www.sporx.com',
                'https://www.ntvspor.net',
                'https://www.mackolik.com'
            ],
            'update_interval': 7200  # 2 saat
        },
        
        # Tavily yapılandırması
        'tavily': {
            'api_key': os.getenv('TAVILY_API_KEY'),
            'max_results': 5,
            'search_depth': 'advanced'
        },
        
        # Bilgi kaynakları öncelikleri (0-1 arası)
        'source_weights': {
            'openai': 0.4,
            'local': 0.3,
            'url': 0.2,
            'web_search': 0.1
        }
    } 