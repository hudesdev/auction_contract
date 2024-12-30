"""Sports expert implementation"""
from typing import Dict, Any, Optional, List
import logging
from src.core.expert_base import ExpertBase
from src.utils.cache import Cache
from src.utils.openai_client import OpenAIClient
from .sources.local_data import get_knowledge_base, get_common_questions, find_answer

logger = logging.getLogger(__name__)

class SportsExpert(ExpertBase):
    def __init__(self, config: Dict[str, Any]):
        """Initialize SportsExpert
        
        Args:
            config (Dict[str, Any]): Configuration dictionary
        """
        super().__init__("sports")
        self.config = config
        self.cache = Cache(
            enabled=config["experts"]["sports"]["cache_enabled"],
            ttl=config["experts"]["sports"]["cache_ttl"]
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
        """Get sports related URLs
        
        Returns:
            List[str]: List of sports URLs
        """
        return [
            "https://www.tff.org",  # Türkiye Futbol Federasyonu
            "https://www.galatasaray.org",  # Galatasaray
            "https://www.fenerbahce.org",  # Fenerbahçe
            "https://www.bjk.com.tr",  # Beşiktaş
            "https://www.ntvspor.net",  # NTV Spor
            "https://www.sporx.com"  # Sporx
        ] 