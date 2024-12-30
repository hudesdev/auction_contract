"""Base class for all experts"""
from typing import Optional
import logging
from src.utils.openai_client import OpenAIClient
from src.utils.web_search import WebSearch
from src.utils.cache import Cache

logger = logging.getLogger(__name__)

class ExpertBase:
    def __init__(self, expert_type: str):
        """Initialize expert
        
        Args:
            expert_type (str): Type of expert (sports, food, ai, sudostar)
        """
        self.expert_type = expert_type
        self.openai_client = OpenAIClient()
        self.web_search = WebSearch()
        
    async def get_response(self, question: str) -> Optional[str]:
        """Get response for the question using multiple methods
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Response or None if no answer found
        """
        try:
            # 1. Try local data first
            if hasattr(self, 'find_answer'):
                logger.info("Trying local data...")
                if local_answer := await self.find_answer(question):
                    logger.info("Found answer in local data")
                    return local_answer
                    
            # 2. Try web search
            logger.info("Trying web search...")
            if web_answer := await self.web_search.search(question):
                logger.info("Found answer from web search")
                return web_answer
                
            # 3. Try generating with OpenAI
            logger.info("Trying OpenAI generation...")
            if generated_answer := await self._generate_response(question):
                logger.info("Generated answer with OpenAI")
                return generated_answer
                
            # 4. If all methods fail, try web search again with modified query
            logger.info("Trying web search again with modified query...")
            modified_query = f"{question} {self.expert_type}"
            if modified_answer := await self.web_search.search(modified_query):
                logger.info("Found answer from modified web search")
                return modified_answer
                
            # 5. If everything fails, return None
            logger.warning("All response generation methods failed")
            return None
            
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}", exc_info=True)
            return None
            
    async def _generate_response(self, question: str) -> Optional[str]:
        """Generate response using OpenAI
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Generated response or None
        """
        try:
            system_prompt = f"""Sen bir {self.expert_type} uzmanısın.
            Kullanıcının sorduğu soruları detaylı ve doğru şekilde yanıtla.
            Eğer soruyu yanıtlayamıyorsan, bunu belirt."""
            
            response = await self.openai_client.get_completion(system_prompt, question)
            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
            return None 