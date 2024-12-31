"""SudoStar expert module"""
import logging
from typing import Optional, Tuple

from src.experts.base_expert import BaseExpert
from src.utils.web_search import WebSearchClient
from .sources.local_data import get_knowledge_base

logger = logging.getLogger(__name__)

class SudoStarExpert(BaseExpert):
    """Expert for SudoStar related questions"""
    
    def __init__(self):
        """Initialize SudoStar expert"""
        super().__init__()
        self.knowledge_base = get_knowledge_base()
        self.web_search = WebSearchClient()
        
    async def get_response(self, question: str) -> Optional[str]:
        """Get response for SudoStar related question
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Response or None if not applicable
        """
        try:
            # Format knowledge base data for context
            context = []
            
            # Add pricing info
            pricing = self.knowledge_base['pricing']
            context.append(f"Fiyatlandırma bilgileri:")
            context.append(f"- {pricing['conversion_rate']}")
            context.append(f"- Minimum çekim: {pricing['minimum_withdrawal']}")
            context.append(f"- Ödeme süresi: {pricing['payment_time']}")
            
            # Add features
            features = self.knowledge_base['features']
            context.append(f"\nÖzellikler:")
            for feature, desc in features.items():
                context.append(f"- {desc}")
            
            context = "\n".join(context)
            
            # Generate response using OpenAI
            messages = [
                {"role": "system", "content": f"""Sen bir SudoStar uzmanısın. Aşağıdaki bilgilere dayanarak soruları yanıtla:

{context}

Yanıtların kısa, öz ve doğru olmalı. Emin olmadığın konularda kullanıcıyı resmi kaynaklara yönlendir."""},
                {"role": "user", "content": question}
            ]
            
            response = await self.openai_client.chat_completion(messages)
            return response
            
        except Exception as e:
            logger.error(f"Error in SudoStar expert: {str(e)}")
            return None 