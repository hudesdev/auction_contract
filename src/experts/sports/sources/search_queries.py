"""Sports Expert için arama sorguları"""

SEARCH_TEMPLATES = {
    "football": {
        "match": "{team} son maç sonucu",
        "live": "{team} canlı skor",
        "stats": "{team} puan durumu",
        "transfer": "{team} transfer haberleri"
    },
    "basketball": {
        "match": "{team} basketbol maç sonucu",
        "live": "{team} basketbol canlı skor",
        "stats": "{team} basketbol istatistikleri",
        "player": "{player} oyuncu performansı"
    },
    "training": {
        "program": "{sport} antrenman programı",
        "technique": "{sport} teknik geliştirme",
        "nutrition": "{sport} beslenme programı",
        "equipment": "{sport} ekipman önerileri"
    }
}

def get_search_query(category: str, template: str, **kwargs) -> str:
    """Arama sorgusu oluştur"""
    query_template = SEARCH_TEMPLATES.get(category, {}).get(template)
    if query_template:
        return query_template.format(**kwargs)
    return None 