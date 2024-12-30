import sys
import os
import logging
from typing import Optional

# Add src directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.experts import SportsExpert, FoodExpert, AIExpert
from src.core.expert_selector import ExpertSelector
from src.utils.config import ConfigLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestSystem:
    def __init__(self):
        """Initialize test system with experts and selector"""
        # Load config
        config = ConfigLoader.load_config("config")
        
        # Initialize experts
        self.sports_expert = SportsExpert(config)
        self.food_expert = FoodExpert(config)
        self.ai_expert = AIExpert(config)
        self.expert_selector = ExpertSelector()
        
    def print_welcome(self):
        """Display welcome message and instructions"""
        print("\nUzman Test Sistemi")
        print("-" * 50)
        print("Aşağıdaki konularda sorular sorabilirsiniz:")
        print("1. Spor (futbol, basketbol, maçlar, antrenman)")
        print("2. Yemek (tarifler, restoranlar, diyet)")
        print("3. Yapay Zeka (teknolojiler, uygulamalar, etik)")
        print("-" * 50)

    def get_response(self, question: str) -> Optional[str]:
        """Get response from appropriate expert based on question

        Args:
            question (str): User's question

        Returns:
            Optional[str]: Expert's response or None if no expert found
        """
        try:
            expert_type = self.expert_selector.select_expert(question)
            
            if expert_type == "spor":
                response = self.sports_expert.get_response(question)
            elif expert_type == "yemek":
                response = self.food_expert.get_response(question)
            elif expert_type == "ai":
                response = self.ai_expert.get_response(question)
            else:
                logger.warning(f"No expert found for question: {question}")
                return None
                
            if response:
                return response
            else:
                logger.warning(f"Expert {expert_type} could not generate response")
                return None
                
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}")
            return None

    def run(self):
        """Run the test system main loop"""
        self.print_welcome()
        
        while True:
            try:
                print("\nSorunuzu yazın (çıkmak için 'q' yazın):")
                question = input("> ").strip()
                
                if question.lower() == 'q':
                    break
                    
                if not question:
                    print("\nLütfen bir soru girin.")
                    continue
                    
                response = self.get_response(question)
                
                if response:
                    print("\nYanıt:", response)
                else:
                    print("\nÜzgünüm, sorunuzu yanıtlayamadım.")
                    print("Lütfen sorunuzu daha açık bir şekilde ifade edin veya")
                    print("spor, yemek ya da yapay zeka konularında bir soru sorun.")
                    
            except KeyboardInterrupt:
                print("\nProgram sonlandırılıyor...")
                break
                
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                print("\nBir hata oluştu. Lütfen tekrar deneyin.")

def main():
    """Main entry point"""
    try:
        test_system = TestSystem()
        test_system.run()
    except Exception as e:
        logger.error(f"Failed to start test system: {str(e)}")
    finally:
        print("\nTest sistemi kapatılıyor...")

if __name__ == "__main__":
    main() 