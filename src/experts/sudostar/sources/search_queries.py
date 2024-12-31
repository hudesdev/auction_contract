"""Search queries for SudoStar expert"""

SEARCH_QUERIES = {
    "pricing": [
        "SudoStar elmas fiyatları",
        "SudoStar diamond prices",
        "SudoStar ödeme sistemi",
        "SudoStar minimum çekim"
    ],
    "features": [
        "SudoStar özellikleri",
        "SudoStar nasıl kullanılır",
        "SudoStar app features"
    ],
    "payment": [
        "SudoStar para çekme",
        "SudoStar ödeme yöntemleri",
        "SudoStar payment methods"
    ]
}

def get_search_queries(query_type: str) -> list:
    """Get search queries by type
    
    Args:
        query_type (str): Type of queries to get
        
    Returns:
        list: List of search queries
    """
    return SEARCH_QUERIES.get(query_type, []) 