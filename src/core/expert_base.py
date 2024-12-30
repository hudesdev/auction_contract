"""Base class for all experts"""
from typing import Optional, Tuple, List
import logging
import aiohttp
from bs4 import BeautifulSoup
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
        self.cache = Cache()
        
    async def get_response(self, question: str) -> Optional[str]:
        """Get response using multiple data sources:
        1. Local data (knowledge base)
        2. OpenAI API
        3. URL content
        4. Web search
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Response or None if no answer found
        """
        try:
            # Check cache first
            if cached := self.cache.get(question):
                logger.info("Cache hit")
                return cached
                
            # 1. Try local knowledge base
            if local_answer := await self._get_local_answer(question):
                logger.info("Found answer in local data")
                self.cache.set(question, local_answer)
                return local_answer
                
            # 2. Try OpenAI
            if ai_answer := await self._get_ai_answer(question):
                logger.info("Generated answer with OpenAI")
                self.cache.set(question, ai_answer)
                return ai_answer
                
            # 3. Try URL content
            if url_answer := await self._get_url_content(question):
                logger.info("Found answer in URL content")
                self.cache.set(question, url_answer)
                return url_answer
                
            # 4. Try web search
            if web_answer := await self._get_web_answer(question):
                logger.info("Found answer from web search")
                self.cache.set(question, web_answer)
                return web_answer
                
            logger.warning("No answer found from any source")
            return None
            
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}", exc_info=True)
            return None
            
    async def _get_local_answer(self, question: str) -> Optional[str]:
        """Get answer from local knowledge base
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Answer if found in local data
        """
        try:
            if hasattr(self, 'find_answer'):
                return await self.find_answer(question)
            return None
        except Exception as e:
            logger.error(f"Error getting local answer: {str(e)}")
            return None
            
    async def _get_ai_answer(self, question: str) -> Optional[str]:
        """Get answer from OpenAI
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Generated answer from OpenAI
        """
        try:
            system_prompt = f"""Sen bir {self.expert_type} uzmanısın.
            Kullanıcının sorduğu soruları detaylı ve doğru şekilde yanıtla.
            Eğer soruyu yanıtlayamıyorsan veya emin değilsen, bunu belirt."""
            
            return await self.openai_client.get_completion(system_prompt, question)
            
        except Exception as e:
            logger.error(f"Error getting AI answer: {str(e)}")
            return None
            
    async def _get_url_content(self, question: str) -> Optional[str]:
        """Get answer from relevant URLs
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Answer extracted from URLs
        """
        try:
            # Get relevant URLs for the expert type
            urls = self._get_expert_urls()
            
            if not urls:
                return None
                
            # Fetch and parse content from URLs
            async with aiohttp.ClientSession() as session:
                for url in urls:
                    try:
                        async with session.get(url) as response:
                            if response.status == 200:
                                html = await response.text()
                                soup = BeautifulSoup(html, 'html.parser')
                                
                                # Remove script and style elements
                                for script in soup(["script", "style"]):
                                    script.decompose()
                                    
                                # Get text content
                                text = soup.get_text()
                                
                                # Use OpenAI to extract relevant answer
                                system_prompt = """Verilen metin içeriğinden soruya en uygun yanıtı çıkar.
                                Eğer uygun yanıt bulunamazsa None döndür."""
                                
                                user_prompt = f"""Soru: {question}
                                
                                Metin: {text[:2000]}  # İlk 2000 karakter
                                
                                Yanıt:"""
                                
                                if answer := await self.openai_client.get_completion(system_prompt, user_prompt):
                                    if answer.lower() != "none":
                                        return answer
                                        
                    except Exception as e:
                        logger.error(f"Error fetching URL {url}: {str(e)}")
                        continue
                        
            return None
            
        except Exception as e:
            logger.error(f"Error getting URL content: {str(e)}")
            return None
            
    async def _get_web_answer(self, question: str) -> Optional[str]:
        """Get answer from web search
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Answer from web search
        """
        try:
            return await self.web_search.search(question)
        except Exception as e:
            logger.error(f"Error getting web answer: {str(e)}")
            return None
            
    def _get_expert_urls(self) -> List[str]:
        """Get relevant URLs for the expert type
        
        Returns:
            List[str]: List of relevant URLs
        """
        # Her expert kendi URL'lerini override edebilir
        return [] 