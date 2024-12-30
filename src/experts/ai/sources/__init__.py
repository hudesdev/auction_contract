"""AI expert için kaynak modülleri"""

from .local_data import get_knowledge_base, get_common_questions, find_answer
from .search_queries import get_search_queries
from .url_sources import get_url_sources
from .openai_prompts import get_prompts

__all__ = [
    'get_ai_response',
    'get_system_prompt',
    'get_urls',
    'get_search_query'
] 