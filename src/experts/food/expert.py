"""Food expert implementation"""
from typing import Dict, Any, Optional, List
import logging
from src.core.expert_base import ExpertBase
from src.utils.cache import Cache
from src.utils.openai_client import OpenAIClient
from .sources.local_data import get_knowledge_base, get_common_questions, find_answer

logger = logging.getLogger(__name__)

class FoodExpert(ExpertBase):
    def __init__(self, config: Dict[str, Any]):
        """Initialize FoodExpert
        
        Args:
            config (Dict[str, Any]): Configuration dictionary
        """
        super().__init__("food")
        self.config = config
        self.cache = Cache(
            enabled=config["experts"]["food"]["cache_enabled"],
            ttl=config["experts"]["food"]["cache_ttl"]
        )
        self.openai_client = OpenAIClient()
        
        # Load knowledge base
        self.knowledge_base = get_knowledge_base()
        self.common_questions = get_common_questions()
        
    async def find_answer(self, question: str) -> Optional[str]:
        """Find answer in local knowledge base
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Answer if found in local data
        """
        return find_answer(question)
        
    def _get_expert_urls(self) -> List[str]:
        """Get food related URLs
        
        Returns:
            List[str]: List of food URLs
        """
        return [
            "https://www.nefisyemektarifleri.com",  # Nefis Yemek Tarifleri
            "https://yemek.com",  # Yemek.com
            "https://www.lezzet.com.tr",  # Lezzet
            "https://www.ardaninmutfagi.com",  # Arda'nın Mutfağı
            "https://www.refika.com",  # Refika'nın Mutfağı
            "https://www.sabah.com.tr/yemek-tarifleri"  # Sabah Yemek
        ] 