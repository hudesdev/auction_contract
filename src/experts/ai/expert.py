"""AI Expert implementation"""
import datetime
from src.core.expert_base import ExpertBase

class AIExpert(ExpertBase):
    def __init__(self, config):
        """Initialize AIExpert
        
        Args:
            config (Dict[str, Any]): Configuration dictionary
        """
        system_message = """Sen bir yapay zeka uzmanısın. Yapay zeka teknolojileri, uygulamaları ve etik konularında detaylı bilgi sahibisin.
            Soruları Türkçe olarak yanıtla ve mümkün olduğunca teknik detayları anlaşılır şekilde açıkla.
            Tarih ve zaman ile ilgili sorularda datetime modülünü kullanarak güncel bilgi ver."""
        super().__init__("ai", system_message)
        
    def get_response(self, message: str) -> str:
        """Get response for AI related question
        
        Args:
            message (str): User's message
            
        Returns:
            str: Response
        """
        # Eğer tarih/zaman sorusu ise, güncel bilgiyi döndür
        if "hangi yıl" in message.lower():
            current_year = datetime.datetime.now().year
            return f"Şu anda {current_year} yılındayız."
            
        # Diğer sorular için OpenAI'dan yanıt al
        return super().get_response(message) 