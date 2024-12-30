"""Spor uzmanı için yerel veri kaynağı"""

SPORTS_KNOWLEDGE = {
    "football": {
        "news": [
            "Fenerbahçe bu sezon ligde lider durumda.",
            "Galatasaray Şampiyonlar Liginde mücadele ediyor.",
            "Beşiktaş yeni teknik direktör arayışında."
        ],
        "history": [
            "Türkiye A Milli Futbol Takımı, 2002 Dünya Kupası'nda üçüncü oldu.",
            "Galatasaray, 2024 yılında super kupa kazandı."
        ]
    },
    "basketball": {
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

SPORTS_KEYWORDS = {
    "football": ["futbol", "maç", "lig", "kupa", "takım", "transfer", "teknik direktör", "uefa", "şampiyonlar"],
    "basketball": ["basketbol", "nba", "euroleague", "sayı", "basket", "potaya"]
}

def get_sports_response(message: str) -> str:
    """Spor ile ilgili yerel verilerden yanıt üret"""
    message = message.lower()
    message_words = set(message.split())
    
    # Her kategori için kontrol et
    for category, data in SPORTS_KNOWLEDGE.items():
        # Kategorinin anahtar kelimelerini kontrol et
        if any(keyword in message for keyword in SPORTS_KEYWORDS[category]):
            # Alt kategorileri kontrol et
            for subcategory, responses in data.items():
                # İlgili yanıtı bul
                for response in responses:
                    response_lower = response.lower()
                    # Mesajdaki önemli kelimelerin yanıtta geçip geçmediğini kontrol et
                    matching_words = message_words.intersection(response_lower.split())
                    if len(matching_words) >= 2:  # En az 2 kelime eşleşirse
                        return response
                        
    return None 