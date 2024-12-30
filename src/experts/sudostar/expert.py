from typing import Dict, List, Optional, Any
from src.core.base_expert import BaseExpert
from .sources import (
    get_knowledge_base,
    get_common_questions,
    get_search_queries,
    get_system_prompt,
    get_url_sources
)
from src.utils.cache import Cache
from src.utils.openai_client import OpenAIClient

class SudoStarExpert(BaseExpert):
    def __init__(self, config: Dict[str, Any]):
        """Initialize SudoStarExpert
        
        Args:
            config (Dict[str, Any]): Configuration dictionary
        """
        super().__init__("sudostar")
        self.config = config
        self.cache = Cache(
            enabled=config["experts"]["sudostar"]["cache_enabled"],
            ttl=config["experts"]["sudostar"]["cache_ttl"]
        )
        self.openai_client = OpenAIClient()
        
        # Load knowledge base
        self.knowledge_base = get_knowledge_base()
        self.common_questions = get_common_questions()
        self.search_queries = get_search_queries()
        self.url_sources = get_url_sources()
        
    async def get_response(self, question: str) -> Optional[str]:
        """Get response for SudoStar related question
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Response or None if no answer found
        """
        try:
            # Check cache first
            cached_response = self.cache.get(question)
            if cached_response:
                self.logger.info("Cache hit for question: %s", question)
                return cached_response
                
            # Check common questions
            if question in self.common_questions:
                response = self.common_questions[question]
                self.cache.set(question, response)
                return response
                
            # Check knowledge base
            kb = self.knowledge_base
            if "ödemeler" in question.lower() or "para" in question.lower():
                payment_info = kb.get("rewards_system", {}).get("diamonds", {}).get("payment_processing", {})
                response = f"Ödemeler {payment_info.get('processing_time', '1-3 gün')} içinde hesabınıza aktarılır."
                self.cache.set(question, response)
                return response
            elif "elmas" in question.lower():
                diamonds = kb.get("rewards_system", {}).get("diamonds", {})
                conversion = diamonds.get("conversion_rate", {})
                response = f"Her {conversion.get('diamonds_per_dollar', 5000)} elmas 1 USD'ye eşittir. Minimum çekim miktarı {conversion.get('minimum_withdrawal', 25000)} elmastır."
                self.cache.set(question, response)
                return response
                
            # Generate response using OpenAI
            response = await self._generate_response(question)
            
            # Cache the response
            if response:
                self.cache.set(question, response)
                
            return response
            
        except Exception as e:
            self.logger.error("Error getting SudoStar response: %s", str(e))
            return None
            
    async def _generate_response(self, question: str) -> Optional[str]:
        """Generate response using OpenAI
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Generated response or None
        """
        system_prompt = """Sen bir SudoStar uzmanısın.
        SudoStar mobil uygulamasının özellikleri, ödeme sistemi ve elmas sistemi hakkında detaylı bilgi sahibisin.
        Kullanıcının sorduğu SudoStar ile ilgili soruları yanıtla.
        Eğer soru SudoStar ile ilgili değilse, bunu belirt."""
        
        try:
            response = await self.openai_client.get_completion(system_prompt, question)
            return response
        except Exception as e:
            self.logger.error("Error generating SudoStar response: %s", str(e))
            return None

    def get_expert_info(self) -> Dict:
        """Returns basic information about the SudoStar expert."""
        return {
            "name": "SudoStar Expert",
            "description": "Expert in SudoStar mobile application features, capabilities, and best practices",
            "capabilities": [
                "Provide detailed information about SudoStar features",
                "Help with technical setup and configuration",
                "Offer best practices for social media automation",
                "Assist with troubleshooting common issues",
                "Guide users through platform integrations"
            ]
        }

    def get_relevant_context(self, query: str) -> Dict:
        """Returns relevant context based on the user's query."""
        context = {
            "knowledge_base": self._filter_relevant_knowledge(query),
            "common_questions": self._find_related_questions(query),
            "urls": self._get_relevant_urls(query)
        }
        return context

    def _filter_relevant_knowledge(self, query: str) -> Dict:
        """Filters and returns relevant knowledge based on the query."""
        # In a real implementation, this would use more sophisticated
        # matching algorithms. For now, we return the full knowledge base
        return self.knowledge_base

    def _find_related_questions(self, query: str) -> Dict[str, str]:
        """Finds and returns related common questions and answers."""
        # In a real implementation, this would use semantic matching
        return self.common_questions

    def _get_relevant_urls(self, query: str) -> Dict:
        """Returns relevant URLs based on the query context."""
        # In a real implementation, this would filter based on query context
        return self.url_sources

    def get_system_prompt(self, context: Optional[str] = None) -> str:
        """Returns the appropriate system prompt based on context."""
        prompt_type = "general_expert"
        if context and "technical" in context.lower():
            prompt_type = "technical_support"
        elif context and "feature" in context.lower():
            prompt_type = "feature_expert"
        return get_system_prompt(prompt_type) 