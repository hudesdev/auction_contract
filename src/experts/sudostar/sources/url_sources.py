from typing import Dict, List

URL_SOURCES = {
    "official": {
        "main_website": "https://sudostar.com",
        "documentation": "https://docs.sudostar.com",
        "api_docs": "https://api.sudostar.com/docs",
        "blog": "https://blog.sudostar.com"
    },
    "social_media": {
        "twitter": "https://twitter.com/SudoStarApp",
        "linkedin": "https://linkedin.com/company/sudostar",
        "facebook": "https://facebook.com/SudoStarApp",
        "instagram": "https://instagram.com/sudostar"
    },
    "support": {
        "help_center": "https://help.sudostar.com",
        "community": "https://community.sudostar.com",
        "status": "https://status.sudostar.com"
    }
}

REFERENCE_ARTICLES = [
    {
        "title": "Getting Started with SudoStar",
        "url": "https://docs.sudostar.com/getting-started",
        "category": "documentation"
    },
    {
        "title": "SudoStar API Integration Guide",
        "url": "https://docs.sudostar.com/api-guide",
        "category": "technical"
    },
    {
        "title": "Best Practices for Content Generation",
        "url": "https://blog.sudostar.com/content-generation-guide",
        "category": "tutorial"
    },
    {
        "title": "Security and Privacy in SudoStar",
        "url": "https://docs.sudostar.com/security",
        "category": "documentation"
    }
]

def get_url_sources() -> Dict:
    return URL_SOURCES

def get_reference_articles() -> List[Dict]:
    return REFERENCE_ARTICLES

def get_articles_by_category(category: str) -> List[Dict]:
    return [article for article in REFERENCE_ARTICLES if article["category"] == category] 