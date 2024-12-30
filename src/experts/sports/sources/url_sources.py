"""Sports Expert için URL kaynakları"""

SPORTS_URLS = {
    "football": {
        "news": [
            "https://www.goal.com/tr",
            "https://www.sporx.com/futbol",
            "https://www.mackolik.com/"
        ],
        "stats": [
            "https://www.transfermarkt.com.tr/",
            "https://www.whoscored.com/",
            "https://www.sofascore.com/football"
        ]
    },
    "basketball": {
        "news": [
            "https://www.eurohoops.net/tr",
            "https://www.basketfaul.com/",
            "https://www.nba.com/news"
        ],
        "stats": [
            "https://www.basketball-reference.com/",
            "https://www.euroleague.net/statistics",
            "https://www.sofascore.com/basketball"
        ]
    },
    "live": {
        "scores": [
            "https://www.livescore.com/tr/",
            "https://www.flashscore.com.tr/",
            "https://www.sofascore.com/"
        ],
        "streaming": [
            "https://www.beinconnect.com.tr/spor",
            "https://www.s-sport.tv/",
            "https://www.nbaplus.tv/"
        ]
    }
}

def get_urls(category: str, subcategory: str = None) -> list:
    """Belirtilen kategori için URL'leri döndür"""
    if subcategory:
        return SPORTS_URLS.get(category, {}).get(subcategory, [])
    urls = []
    for subcats in SPORTS_URLS.get(category, {}).values():
        urls.extend(subcats)
    return urls 