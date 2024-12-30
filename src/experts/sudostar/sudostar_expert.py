from typing import Dict, List, Optional
from src.core.base_expert import BaseExpert
from .sources import (
    get_knowledge_base,
    get_common_questions,
    get_search_queries,
    get_system_prompt,
    get_url_sources
)

class SudoStarExpert(BaseExpert):
    def __init__(self):
        super().__init__("sudostar")
        self.knowledge_base = get_knowledge_base()
        self.common_questions = get_common_questions()
        self.search_queries = get_search_queries()
        self.url_sources = get_url_sources()

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