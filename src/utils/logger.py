"""Logging utilities"""
import logging

class Logger:
    def __init__(self, name=None):
        self.logger = logging.getLogger(name if name else __name__)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)
        
    def error(self, message):
        self.logger.error(message)
        
    def warning(self, message):
        self.logger.warning(message)
        
    def debug(self, message):
        self.logger.debug(message)

def setup_logger(name=None, level=logging.INFO):
    """Setup and return a logger instance
    
    Args:
        name (str, optional): Logger name. Defaults to None.
        level (int, optional): Logging level. Defaults to logging.INFO.
        
    Returns:
        Logger: Configured logger instance
    """
    return Logger(name) 