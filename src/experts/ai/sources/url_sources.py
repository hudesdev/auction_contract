"""AI Expert için URL kaynakları"""

AI_URLS = {
    "news": {
        "general": [
            "https://www.artificialintelligence-news.com/",
            "https://www.ai-trends.com/",
            "https://venturebeat.com/category/ai/"
        ],
        "research": [
            "https://arxiv.org/list/cs.AI/recent",
            "https://paperswithcode.com/",
            "https://www.nature.com/subjects/artificial-intelligence"
        ]
    },
    "learning": {
        "tutorials": [
            "https://www.deeplearning.ai/",
            "https://www.fast.ai/",
            "https://www.coursera.org/courses?query=artificial%20intelligence"
        ],
        "documentation": [
            "https://huggingface.co/docs",
            "https://pytorch.org/docs/",
            "https://www.tensorflow.org/guide"
        ]
    },
    "applications": {
        "tools": [
            "https://openai.com/blog/",
            "https://stability.ai/blog",
            "https://www.anthropic.com/blog"
        ],
        "examples": [
            "https://github.com/topics/artificial-intelligence",
            "https://paperswithcode.com/sota",
            "https://huggingface.co/models"
        ]
    },
    "ethics": {
        "guidelines": [
            "https://www.partnershiponai.org/",
            "https://www.aiethics.cc/",
            "https://ethicsinaction.ieee.org/"
        ],
        "discussions": [
            "https://hai.stanford.edu/",
            "https://www.fast.ai/topics/#ethics",
            "https://www.eff.org/ai"
        ]
    }
}

def get_urls(category: str, subcategory: str = None) -> list:
    """Belirtilen kategori için URL'leri döndür"""
    if subcategory:
        return AI_URLS.get(category, {}).get(subcategory, [])
    urls = []
    for subcats in AI_URLS.get(category, {}).values():
        urls.extend(subcats)
    return urls 