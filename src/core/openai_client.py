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
        
    def get_completion(self, system_prompt: str, user_message: str) -> Optional[str]:
        """
        OpenAI API'den yanıt al
        
        Args:
            system_prompt: Sistem promptu
            user_message: Kullanıcı mesajı
            
        Returns:
            str: API yanıtı veya None
        """
        try:
            self.logger.info(f"OpenAI'ya istek gönderiliyor. System: {system_prompt}, User: {user_message}")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.7,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            result = response.choices[0].message.content
            self.logger.info(f"OpenAI yanıtı alındı: {result}")
            return result
                
        except Exception as e:
            self.logger.error(f"OpenAI API hatası: {str(e)}")
            return None 