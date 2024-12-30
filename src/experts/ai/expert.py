"""AI expert implementation"""
from typing import Dict, Any, Optional, List
import logging
from src.core.expert_base import ExpertBase
from src.utils.cache import Cache
from src.utils.openai_client import OpenAIClient
from .sources.local_data import get_knowledge_base, get_common_questions, find_answer

logger = logging.getLogger(__name__)

class AIExpert(ExpertBase):
    def __init__(self, config: Dict[str, Any]):
        """Initialize AIExpert
        
        Args:
            config (Dict[str, Any]): Configuration dictionary
        """
        super().__init__("ai")
        self.config = config
        self.cache = Cache(
            enabled=config["experts"]["ai"]["cache_enabled"],
            ttl=config["experts"]["ai"]["cache_ttl"]
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
        """Get AI related URLs
        
        Returns:
            List[str]: List of AI URLs
        """
        return [
            "https://openai.com/blog",  # OpenAI Blog
            "https://www.deeplearning.ai",  # DeepLearning.AI
            "https://www.tensorflow.org",  # TensorFlow
            "https://pytorch.org",  # PyTorch
            "https://huggingface.co/blog",  # Hugging Face Blog
            "https://www.fast.ai"  # Fast.ai
        ] 