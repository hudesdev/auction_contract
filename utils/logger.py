import logging
import sys
import os
from datetime import datetime

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('twitter_bot')
        self.logger.setLevel(logging.INFO)
        
        # Eğer handler zaten varsa tekrar ekleme
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', 
                                               datefmt='%Y-%m-%d %H:%M:%S')
            console_handler.setFormatter(console_formatter)
            
            # File handler
            log_dir = 'logs'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
                
            log_file = os.path.join(log_dir, f'bot_{datetime.now().strftime("%Y%m%d")}.log')
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                            datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(file_formatter)
            
            # Add handlers
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def info(self, message):
        """Log info level message"""
        try:
            self.logger.info(message)
        except UnicodeEncodeError:
            # Emoji ve özel karakterleri kaldır
            clean_message = ''.join(char for char in message if ord(char) < 128)
            self.logger.info(clean_message)
        except Exception as e:
            print(f"Logging error: {str(e)}")

    def error(self, message):
        """Log error level message"""
        try:
            self.logger.error(message)
        except UnicodeEncodeError:
            # Emoji ve özel karakterleri kaldır
            clean_message = ''.join(char for char in message if ord(char) < 128)
            self.logger.error(clean_message)
        except Exception as e:
            print(f"Logging error: {str(e)}")

    def warning(self, message):
        """Log warning level message"""
        try:
            self.logger.warning(message)
        except UnicodeEncodeError:
            # Emoji ve özel karakterleri kaldır
            clean_message = ''.join(char for char in message if ord(char) < 128)
            self.logger.warning(clean_message)
        except Exception as e:
            print(f"Logging error: {str(e)}")

    def debug(self, message):
        """Log debug level message"""
        try:
            self.logger.debug(message)
        except UnicodeEncodeError:
            # Emoji ve özel karakterleri kaldır
            clean_message = ''.join(char for char in message if ord(char) < 128)
            self.logger.debug(clean_message)
        except Exception as e:
            print(f"Logging error: {str(e)}") 