"""Local knowledge base for sports expert"""
import os
import json
from typing import Dict, Optional

def get_knowledge_base() -> Dict:
    """Load and return sports knowledge base"""
    kb_path = os.path.join(os.path.dirname(__file__), "data", "knowledge_base.json")
    try:
        with open(kb_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "football": {
                "teams": {
                    "galatasaray": {
                        "name": "Galatasaray",
                        "founded": 1905,
                        "stadium": "NEF Arena",
                        "titles": {
                            "super_lig": 23,
                            "turkish_cup": 18,
                            "uefa_cup": 1
                        }
                    },
                    "fenerbahce": {
                        "name": "Fenerbahçe",
                        "founded": 1907,
                        "stadium": "Şükrü Saracoğlu",
                        "titles": {
                            "super_lig": 19,
                            "turkish_cup": 6
                        }
                    }
                }
            }
        }

def get_common_questions() -> Dict[str, str]:
    """Load and return common sports questions"""
    qa_path = os.path.join(os.path.dirname(__file__), "data", "common_questions.json")
    try:
        with open(qa_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "galatasaray_uefa": "Galatasaray UEFA Kupası'nı 2000 yılında kazanmıştır.",
            "fb_gs_derby": "Fenerbahçe-Galatasaray derbisi Türkiye'nin en büyük futbol rekabetlerinden biridir.",
            "super_lig_champion": "En çok şampiyonluğu olan takım 23 şampiyonlukla Galatasaray'dır."
        }

def find_answer(question: str, knowledge_base: Optional[Dict] = None) -> Optional[str]:
    """Find answer in knowledge base
    
    Args:
        question (str): User's question
        knowledge_base (Optional[Dict]): Optional knowledge base to search in
        
    Returns:
        Optional[str]: Answer if found
    """
    if knowledge_base is None:
        knowledge_base = get_knowledge_base()
        
    # Check common questions first
    common_questions = get_common_questions()
    for q, a in common_questions.items():
        if any(word in question.lower() for word in q.lower().split("_")):
            return a
            
    # Check knowledge base
    question = question.lower()
    
    # Check football teams
    if "football" in knowledge_base:
        teams = knowledge_base["football"]["teams"]
        for team_key, team_data in teams.items():
            if team_key in question:
                # Questions about founding year
                if any(word in question for word in ["founded", "kuruldu", "kuruluş"]):
                    return f"{team_data['name']} {team_data['founded']} yılında kurulmuştur."
                    
                # Questions about stadium
                if any(word in question for word in ["stadium", "stadyum", "stat"]):
                    return f"{team_data['name']}'ın stadyumu {team_data['stadium']}'dır."
                    
                # Questions about titles
                if any(word in question for word in ["titles", "şampiyonluk", "kupa"]):
                    titles = team_data["titles"]
                    return (
                        f"{team_data['name']}'ın kazandığı kupalar:\n"
                        f"Süper Lig: {titles.get('super_lig', 0)}\n"
                        f"Türkiye Kupası: {titles.get('turkish_cup', 0)}\n"
                        f"UEFA Kupası: {titles.get('uefa_cup', 0)}"
                    )
                    
    return None 