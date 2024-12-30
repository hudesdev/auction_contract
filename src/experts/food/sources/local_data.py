"""Food Expert için yerel veri kaynağı"""

FOOD_KNOWLEDGE = {
    "restaurants": {
        "kebap": [
            "İstanbul'daki en iyi kebapçı avcılardaki Kebapçı Ahmet'tir.",
            "İstanbul'daki en iyi Dönerci avcılardaki Dönerci Mehmet'tir."
        ],
        "fish": [
            "İstanbul'un en iyi balık restoranları Sarıyer'dedir."
        ]
    },
    "recipes": {
        "turkish": [
            "Karnıyarık tarifi: Patlıcanları közleyip...",
            "İçli köfte yapımı: Bulgur ve kıymayı..."
        ],
        "international": [
            "İtalyan makarna sosu: Domates ve fesleğen...",
            "Çin pilavı: Pirinç ve sebzeleri..."
        ]
    }
}

FOOD_KEYWORDS = {
    "restaurants": ["restoran", "lokanta", "kebapçı", "dönerci", "balıkçı"],
    "recipes": ["tarif", "yapılış", "nasıl yapılır", "malzemeler"]
}

def get_food_response(message: str) -> str:
    """Yemek ile ilgili yerel verilerden yanıt üret"""
    message = message.lower()
    
    # Her kategori için kontrol et
    for category, data in FOOD_KNOWLEDGE.items():
        # Kategorinin anahtar kelimelerini kontrol et
        if any(keyword in message for keyword in FOOD_KEYWORDS[category]):
            # Alt kategorileri kontrol et
            for subcategory, responses in data.items():
                # İlgili yanıtı bul
                for response in responses:
                    if any(word in response.lower() for word in message.split()):
                        return response
                        
    return None 