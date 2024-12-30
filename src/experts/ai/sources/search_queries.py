"""Search query generation for AI expert"""
from typing import List, Optional
import json
import os

def get_search_queries() -> List[str]:
    """Load and return predefined search queries"""
    queries_path = os.path.join(os.path.dirname(__file__), "data", "search_queries.json")
    try:
        with open(queries_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def generate_search_query(question: str) -> str:
    """Generate optimized search query from question
    
    Args:
        question (str): User's question
        
    Returns:
        str: Optimized search query
    """
    # Remove common words and punctuation
    stop_words = ["what", "is", "are", "how", "why", "when", "where", "which", "who"]
    words = question.lower().split()
    keywords = [w for w in words if w not in stop_words]
    
    # Add AI context if not present
    if not any(kw in keywords for kw in ["ai", "artificial", "intelligence"]):
        keywords.append("ai")
        
    return " ".join(keywords)

def get_related_queries(query: str) -> List[str]:
    """Get related search queries
    
    Args:
        query (str): Original query
        
    Returns:
        List[str]: List of related queries
    """
    base_query = generate_search_query(query)
    
    # Generate variations
    variations = [
        base_query,
        f"latest {base_query}",
        f"{base_query} tutorial",
        f"{base_query} examples",
        f"how does {base_query} work"
    ]
    
    return variations 