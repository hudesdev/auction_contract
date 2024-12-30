from typing import List, Dict

SEARCH_QUERIES = {
    "general": [
        "SudoStar app features and capabilities",
        "SudoStar social media automation",
        "SudoStar content generation AI",
        "SudoStar app reviews and ratings",
        "How to use SudoStar for social media"
    ],
    "technical": [
        "SudoStar API documentation",
        "SudoStar system requirements",
        "SudoStar integration guides",
        "SudoStar security features",
        "SudoStar performance metrics"
    ],
    "comparison": [
        "SudoStar vs other social media managers",
        "SudoStar alternatives comparison",
        "Best features of SudoStar",
        "SudoStar pricing comparison"
    ],
    "troubleshooting": [
        "SudoStar common issues",
        "SudoStar error solutions",
        "SudoStar setup guide",
        "SudoStar connection problems"
    ]
}

def get_search_queries() -> Dict[str, List[str]]:
    return SEARCH_QUERIES

def get_queries_by_category(category: str) -> List[str]:
    return SEARCH_QUERIES.get(category, []) 