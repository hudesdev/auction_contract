"""Local knowledge base for AI expert"""
from typing import Dict, Optional
import json
import os

def get_knowledge_base() -> Dict:
    """Load and return the AI knowledge base"""
    kb_path = os.path.join(os.path.dirname(__file__), "data", "knowledge_base.json")
    try:
        with open(kb_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def get_common_questions() -> Dict[str, str]:
    """Load and return common AI questions and answers"""
    qa_path = os.path.join(os.path.dirname(__file__), "data", "common_questions.json")
    try:
        with open(qa_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def find_answer(question: str, knowledge_base: Optional[Dict] = None) -> Optional[str]:
    """Find answer in knowledge base using semantic search
    
    Args:
        question (str): User's question
        knowledge_base (Optional[Dict]): Optional knowledge base to search in
        
    Returns:
        Optional[str]: Answer if found
    """
    if knowledge_base is None:
        knowledge_base = get_knowledge_base()
        
    # TODO: Implement semantic search using embeddings
    # For now just do basic keyword matching
    question = question.lower()
    
    # Check common questions first
    common_questions = get_common_questions()
    for q, a in common_questions.items():
        if question in q.lower():
            return a
            
    # Check knowledge base sections
    for section, content in knowledge_base.items():
        if any(kw in question for kw in content.get("keywords", [])):
            return content.get("answer")
            
    return None 