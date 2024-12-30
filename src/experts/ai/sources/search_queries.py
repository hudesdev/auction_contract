"""AI konuları için arama sorguları"""

SEARCH_QUERIES = {
    "general": [
        "yapay zeka nedir",
        "artificial intelligence basics",
        "machine learning fundamentals",
        "deep learning explained"
    ],
    "models": [
        "GPT-4 özellikleri",
        "BERT model architecture",
        "LLaMA model capabilities",
        "Stable Diffusion tutorial"
    ],
    "applications": [
        "AI business applications",
        "artificial intelligence in healthcare",
        "AI in scientific research",
        "machine learning use cases"
    ],
    "ethics": [
        "AI ethics principles",
        "yapay zeka etik kuralları",
        "artificial intelligence regulations",
        "AI privacy concerns"
    ]
}

def get_search_queries() -> dict:
    """Arama sorgularını döndür"""
    return SEARCH_QUERIES 