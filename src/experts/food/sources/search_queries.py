"""Food Expert için arama sorguları"""

SEARCH_TEMPLATES = {
    "recipes": {
        "general": "{dish} tarifi nasıl yapılır",
        "ingredients": "{dish} malzemeleri nelerdir",
        "tips": "{dish} püf noktaları",
        "variations": "{dish} çeşitleri"
    },
    "restaurants": {
        "best": "{city} en iyi {cuisine} restoranları",
        "new": "{city} yeni açılan restoranlar",
        "reviews": "{restaurant} yorumları",
        "menu": "{restaurant} menü fiyatları"
    },
    "diet": {
        "nutrition": "{food} besin değerleri",
        "calories": "{food} kaç kalori",
        "health": "{food} faydaları",
        "alternatives": "{food} yerine ne yenir"
    }
}

def get_search_query(category: str, template: str, **kwargs) -> str:
    """Arama sorgusu oluştur"""
    query_template = SEARCH_TEMPLATES.get(category, {}).get(template)
    if query_template:
        return query_template.format(**kwargs)
    return None 