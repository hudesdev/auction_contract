"""Sports expert için yerel veri kaynağı"""
from typing import Dict, Optional

SPORTS_KNOWLEDGE_BASE = {
    "futbol": {
        "galatasaray": {
            "kuruluş": "1905",
            "renkler": "Sarı-Kırmızı",
            "stadyum": "NEF Stadyumu",
            "başarılar": {
                "süper_lig": "23 kez şampiyon",
                "türkiye_kupası": "18 kez şampiyon",
                "uefa_kupası": "2000 yılında Arsenal'i penaltılarla yenerek kazandı",
                "süper_kupa": "16 kez kazandı"
            }
        },
        "fenerbahçe": {
            "kuruluş": "1907",
            "renkler": "Sarı-Lacivert",
            "stadyum": "Şükrü Saracoğlu Stadyumu",
            "başarılar": {
                "süper_lig": "19 kez şampiyon",
                "türkiye_kupası": "6 kez şampiyon",
                "süper_kupa": "9 kez kazandı"
            }
        },
        "beşiktaş": {
            "kuruluş": "1903",
            "renkler": "Siyah-Beyaz",
            "stadyum": "Vodafone Park",
            "başarılar": {
                "süper_lig": "16 kez şampiyon",
                "türkiye_kupası": "10 kez şampiyon",
                "süper_kupa": "8 kez kazandı"
            }
        }
    },
    "basketbol": {
        "news": [
            "Anadolu Efes Euroleague'de başarılı performans gösteriyor.",
            "12 Dev Adam milli maçlara hazırlanıyor."
        ],
        "history": [
            "Türkiye Basketbol Milli Takımı, 2010 Dünya Şampiyonası'nda gümüş madalya kazandı.",
            "Fenerbahçe, 2017'de Euroleague şampiyonu oldu."
        ]
    }
}

COMMON_QUESTIONS = {
    "Galatasaray kaç yılında UEFA kupasını kazandı?": "Galatasaray, 2000 yılında Arsenal'i penaltılarla yenerek UEFA kupasını kazandı.",
    "Fenerbahçe kaç kez şampiyon oldu?": "Fenerbahçe Süper Lig'de 19 kez şampiyon oldu.",
    "Beşiktaş'ın stadı nerede?": "Beşiktaş'ın stadı Vodafone Park'tır.",
    "Türk basketbol tarihinin en büyük başarısı nedir?": "Türkiye Basketbol Milli Takımı'nın 2010 Dünya Şampiyonası'nda kazandığı gümüş madalya en büyük başarılardan biridir."
}

def get_knowledge_base() -> Dict:
    """Get sports knowledge base
    
    Returns:
        Dict: Sports knowledge base
    """
    return SPORTS_KNOWLEDGE_BASE

def get_common_questions() -> Dict[str, str]:
    """Get common questions and answers
    
    Returns:
        Dict[str, str]: Common questions and answers
    """
    return COMMON_QUESTIONS

def find_answer(question: str) -> Optional[str]:
    """Find answer for the given question
    
    Args:
        question (str): Question to find answer for
        
    Returns:
        Optional[str]: Answer if found, None otherwise
    """
    # Önce yaygın sorularda ara
    if question in COMMON_QUESTIONS:
        return COMMON_QUESTIONS[question]
        
    # Bilgi tabanında ara
    question = question.lower()
    
    # Galatasaray UEFA kupası sorusu
    if "galatasaray" in question and "uefa" in question:
        return SPORTS_KNOWLEDGE_BASE["futbol"]["galatasaray"]["başarılar"]["uefa_kupası"]
        
    # Fenerbahçe şampiyonluk sorusu
    if "fenerbahçe" in question and "şampiyon" in question:
        return SPORTS_KNOWLEDGE_BASE["futbol"]["fenerbahçe"]["başarılar"]["süper_lig"]
        
    # Beşiktaş stad sorusu
    if "beşiktaş" in question and "stad" in question:
        return SPORTS_KNOWLEDGE_BASE["futbol"]["beşiktaş"]["stadyum"]
        
    # Basketbol başarısı sorusu
    if "basketbol" in question and "başarı" in question:
        return SPORTS_KNOWLEDGE_BASE["basketbol"]["history"][0]
        
    return None 