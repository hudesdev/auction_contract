"""AI Expert için arama sorguları"""

SEARCH_TEMPLATES = {
    "general": {
        "explain": "yapay zeka {concept} nedir",
        "history": "{topic} tarihi gelişimi",
        "future": "{topic} geleceği tahminler",
        "comparison": "{term1} vs {term2} farkları"
    },
    "technical": {
        "model": "{model} yapay zeka modeli nasıl çalışır",
        "algorithm": "{algorithm} algoritması detaylı açıklama",
        "architecture": "{architecture} mimarisi nedir",
        "implementation": "{technology} nasıl uygulanır"
    },
    "applications": {
        "use_case": "{industry} sektöründe yapay zeka kullanımı",
        "examples": "{technology} gerçek dünya örnekleri",
        "tutorial": "{tool} kullanım kılavuzu",
        "integration": "{system} yapay zeka entegrasyonu"
    },
    "ethics": {
        "concerns": "{topic} etik sorunları",
        "guidelines": "{area} etik kuralları",
        "impact": "{technology} sosyal etkileri",
        "regulation": "{region} yapay zeka düzenlemeleri"
    }
}

def get_search_query(category: str, template: str, **kwargs) -> str:
    """Arama sorgusu oluştur"""
    query_template = SEARCH_TEMPLATES.get(category, {}).get(template)
    if query_template:
        return query_template.format(**kwargs)
    return None 