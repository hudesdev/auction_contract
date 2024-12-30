"""Yapay zeka uzmanı için yerel veri kaynağı"""

AI_KNOWLEDGE = {
    "general": {
        "basics": [
            "Yapay zeka, insan zekasını taklit eden sistemlerdir.",
            "Machine learning, veriden öğrenen AI sistemleridir.",
            "Deep learning, çok katmanlı yapay sinir ağlarını kullanan bir AI yaklaşımıdır."
        ],
        "history": [
            "İlk yapay zeka terimi 1956'da Dartmouth Konferansı'nda ortaya atıldı.",
            "Deep Blue, 1997'de dünya satranç şampiyonu Kasparov'u yendi.",
            "GPT modelleri 2018'den itibaren dil işlemede devrim yarattı."
        ]
    },
    "models": {
        "language": [
            "GPT-4 şu an en gelişmiş dil modelidir.",
            "BERT, Google tarafından geliştirilen çift yönlü bir dil modelidir.",
            "LLaMA, Meta'nın açık kaynak dil modelidir."
        ],
        "vision": [
            "DALL-E 2, metinden görüntü üreten bir AI modelidir.",
            "Stable Diffusion, açık kaynak bir görüntü üretme modelidir.",
            "Midjourney, sanatsal görüntüler üreten bir AI modelidir."
        ]
    },
    "applications": {
        "business": [
            "AI chatbotlar müşteri hizmetlerinde yaygın kullanılıyor.",
            "Yapay zeka, veri analitiğinde insan performansını artırıyor.",
            "Otomatik içerik üretimi için AI sistemleri kullanılıyor."
        ],
        "science": [
            "AI, protein yapılarını tahmin etmede devrim yarattı.",
            "Yapay zeka, ilaç keşfini hızlandırıyor.",
            "Bilimsel araştırmalarda AI destekli veri analizi önemli."
        ]
    },
    "ethics": {
        "principles": [
            "AI sistemleri şeffaf ve açıklanabilir olmalıdır.",
            "Yapay zeka kullanımında gizlilik önemlidir.",
            "AI kararları adil ve önyargısız olmalıdır."
        ],
        "challenges": [
            "AI sistemlerinde veri yanlılığı önemli bir sorundur.",
            "Yapay zekanın iş gücüne etkisi tartışılıyor.",
            "AI'nin etik kullanımı için düzenlemeler gerekiyor."
        ]
    }
}

COMMON_QUESTIONS = {
    "what_is_ai": "Yapay zeka nedir?",
    "how_works": "Yapay zeka nasıl çalışır?",
    "applications": "Yapay zeka nerelerde kullanılır?",
    "future": "Yapay zekanın geleceği nasıl olacak?",
    "ethics": "Yapay zeka kullanımında etik konular nelerdir?",
    "risks": "Yapay zekanın riskleri nelerdir?",
    "benefits": "Yapay zekanın faydaları nelerdir?",
    "learning": "Yapay zeka nasıl öğrenir?",
    "difference": "AI ve ML arasındaki fark nedir?",
    "impact": "AI'nin topluma etkisi ne olacak?"
}

AI_KEYWORDS = {
    "general": ["yapay zeka", "ai", "artificial intelligence", "machine learning", "deep learning"],
    "models": ["model", "gpt", "bert", "dalle", "diffusion", "transformer"],
    "applications": ["uygulama", "chatbot", "otomasyon", "analiz", "tahmin"],
    "ethics": ["etik", "gizlilik", "güvenlik", "yanlılık", "düzenleme", "kural"]
}

def get_knowledge_base() -> dict:
    """AI bilgi tabanını döndür"""
    return AI_KNOWLEDGE

def get_common_questions() -> dict:
    """Sık sorulan soruları döndür"""
    return COMMON_QUESTIONS

def find_answer(question: str) -> str:
    """Soruya uygun yanıtı bul"""
    question = question.lower()
    
    # Her kategori için kontrol et
    for category, data in AI_KNOWLEDGE.items():
        # Kategorinin anahtar kelimelerini kontrol et
        if any(keyword in question for keyword in AI_KEYWORDS[category]):
            # Alt kategorileri kontrol et
            for subcategory, responses in data.items():
                # İlgili yanıtı bul
                for response in responses:
                    if any(word in response.lower() for word in question.split()):
                        return response
    
    # Eğer spesifik bir yanıt bulunamazsa, genel bir yanıt döndür
    return "Üzgünüm, bu soruya özel bir yanıtım yok. Yapay zeka hakkında başka bir soru sormak ister misiniz?" 