"""AI expert module"""
from src.experts.base import BaseExpert

class AIExpert(BaseExpert):
    def __init__(self, config=None):
        super().__init__()
        self.set_config(config)
        
    async def get_response(self, question: str) -> str:
        return "I am an AI expert. I can help you with AI related questions." 