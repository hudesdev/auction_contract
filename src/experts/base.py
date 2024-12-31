"""Base expert module"""
import logging

class BaseExpert:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = {}
        
    def set_config(self, config):
        if config is not None:
            self.config = config
        
    async def get_response(self, question: str) -> str:
        raise NotImplementedError("Subclasses must implement get_response method") 