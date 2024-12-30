"""Food expert için yerel veri kaynağı"""
from typing import Dict, Optional

FOOD_KNOWLEDGE_BASE = {
    "yemekler": {
        "kebap": {
            "malzemeler": [
                "kuzu eti veya dana eti",
                "soğan",
                "sarımsak",
                "zeytinyağı",
                "tuz",
                "karabiber",
                "kırmızı biber"
            ],
            "tarif": """
            1. Eti küçük parçalar halinde doğrayın
            2. Soğan ve sarımsağı ince ince doğrayın
            3. Tüm malzemeleri karıştırıp marine edin
            4. En az 2 saat buzdolabında bekletin
            5. Şişlere dizin
            6. Mangalda veya fırında pişirin
            7. Lavaş ekmek ve közlenmiş sebzelerle servis yapın
            """
        },
        "pide": {
            "malzemeler": [
                "un",
                "maya",
                "su",
                "tuz",
                "kıyma",
                "soğan",
                "karabiber"
            ],
            "tarif": """
            1. Hamur için malzemeleri yoğurun
            2. 30 dakika mayalanmaya bırakın
            3. İç harcı hazırlayın
            4. Hamuru açın ve iç harcı yayın
            5. Kenarlarını kıvırın
            6. 200 derece fırında 15-20 dakika pişirin
            """
        }
    },
    "tarifler": {
        "kolay": [
            "Menemen",
            "Makarna",
            "Pilav",
            "Omlet"
        ],
        "orta": [
            "Pide",
            "Lahmacun",
            "Mantı",
            "Karnıyarık"
        ],
        "zor": [
            "Kebap",
            "İskender",
            "Hünkar Beğendi",
            "Kuru Fasulye"
        ]
    }
}

COMMON_QUESTIONS = {
    "Kebap nasıl yapılır?": """
    Kebap yapımı için:
    1. Eti küçük parçalar halinde doğrayın
    2. Soğan ve sarımsağı ince ince doğrayın
    3. Tüm malzemeleri karıştırıp marine edin
    4. En az 2 saat buzdolabında bekletin
    5. Şişlere dizin
    6. Mangalda veya fırında pişirin
    7. Lavaş ekmek ve közlenmiş sebzelerle servis yapın
    """,
    "Pide nasıl yapılır?": """
    Pide yapımı için:
    1. Hamur için malzemeleri yoğurun
    2. 30 dakika mayalanmaya bırakın
    3. İç harcı hazırlayın
    4. Hamuru açın ve iç harcı yayın
    5. Kenarlarını kıvırın
    6. 200 derece fırında 15-20 dakika pişirin
    """
}

def get_knowledge_base() -> Dict:
    """Get food knowledge base
    
    Returns:
        Dict: Food knowledge base
    """
    return FOOD_KNOWLEDGE_BASE

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
    
    # Kebap tarifi sorusu
    if "kebap" in question and ("nasıl" in question or "tarif" in question):
        return FOOD_KNOWLEDGE_BASE["yemekler"]["kebap"]["tarif"]
        
    # Pide tarifi sorusu
    if "pide" in question and ("nasıl" in question or "tarif" in question):
        return FOOD_KNOWLEDGE_BASE["yemekler"]["pide"]["tarif"]
        
    return None 