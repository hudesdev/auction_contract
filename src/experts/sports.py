"""Sports expert module"""
from src.experts.base import BaseExpert

class SportsExpert(BaseExpert):
    def __init__(self, config=None):
        super().__init__()
        self.set_config(config)
        
    async def get_response(self, question: str) -> str:
        return "I am a sports expert. I can help you with sports related questions." 