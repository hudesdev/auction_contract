from typing import Optional
import os
from openai import OpenAI
from utils.logger import Logger

class OpenAIClient:
    """OpenAI API istemcisi"""
    
    def __init__(self):
        """OpenAI istemcisini başlat"""
        self.logger = Logger()
        self.logger.info("OpenAIClient başlatılıyor...")
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            self.logger.error("OPENAI_API_KEY bulunamadı!")
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.logger.info("OpenAI client başarıyla oluşturuldu")
        
    async def get_completion(self, system_prompt: str, user_message: str) -> Optional[str]:
        """OpenAI API'den yanıt al"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"OpenAI API hatası: {str(e)}")
            return None 