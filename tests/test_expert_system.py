"""Expert system interactive test module"""
import os
import sys
import asyncio
import logging
from typing import Optional

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.experts import SportsExpert, FoodExpert, AIExpert, SudoStarExpert
from src.core.expert_selector import ExpertSelector
from src.utils.config import ConfigLoader

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class ExpertSystemTester:
    def __init__(self):
        """Initialize tester"""
        # Load config
        self.config = ConfigLoader.load_config()
        
        # Initialize experts
        self.sports_expert = SportsExpert(self.config)
        self.food_expert = FoodExpert(self.config)
        self.ai_expert = AIExpert(self.config)
        self.sudostar_expert = SudoStarExpert(self.config)
        self.expert_selector = ExpertSelector()
        
        logger.info("Expert system tester initialized")
        
    async def process_question(self, question: str) -> Optional[str]:
        """Process a question and get response
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Response if found
        """
        try:
            # Select expert
            expert_type = await self.expert_selector.select_expert(question)
            logger.info(f"Selected expert: {expert_type}")
            
            # Get response from appropriate expert
            if expert_type == "sports":
                response = await self.sports_expert.get_response(question)
            elif expert_type == "food":
                response = await self.food_expert.get_response(question)
            elif expert_type == "ai":
                response = await self.ai_expert.get_response(question)
            elif expert_type == "sudostar":
                response = await self.sudostar_expert.get_response(question)
            else:
                logger.warning(f"No expert found for type: {expert_type}")
                return None
                
            return response
            
        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return None
            
    def print_help(self):
        """Print help message"""
        print("\nAvailable commands:")
        print("  /help    - Show this help message")
        print("  /quit    - Exit the test tool")
        print("  /experts - List available experts")
        print("  /clear   - Clear the screen")
        print("\nAvailable experts:")
        print("  - Sports Expert (sports, athletes, teams, competitions)")
        print("  - Food Expert (recipes, cooking, nutrition)")
        print("  - AI Expert (artificial intelligence, machine learning)")
        print("  - SudoStar Expert (app features, rewards, diamonds)")
        
    def print_experts(self):
        """Print available experts"""
        print("\nAvailable experts and their capabilities:")
        print("\n1. Sports Expert")
        print("   - Sports news and results")
        print("   - Team and player information")
        print("   - Competition schedules")
        print("   - Training and fitness advice")
        
        print("\n2. Food Expert")
        print("   - Cooking recipes")
        print("   - Ingredient information")
        print("   - Nutritional advice")
        print("   - Restaurant recommendations")
        
        print("\n3. AI Expert")
        print("   - AI technology explanations")
        print("   - Machine learning concepts")
        print("   - AI applications and use cases")
        print("   - AI ethics and future trends")
        
        print("\n4. SudoStar Expert")
        print("   - App features and usage")
        print("   - Rewards system")
        print("   - Diamond earning methods")
        print("   - Payment processing")
            
async def main():
    """Main entry point"""
    tester = ExpertSystemTester()
    
    print("\nExpert System Interactive Tester")
    print("Type /help for available commands")
    print("-" * 50)
    
    while True:
        try:
            # Get question from user
            question = input("\nEnter your question: ").strip()
            
            # Check for commands
            if question.lower() in ['/quit', '/q', 'quit', 'exit']:
                print("\nExiting test tool...")
                break
            elif question.lower() in ['/help', '/h', 'help']:
                tester.print_help()
                continue
            elif question.lower() in ['/experts', '/e']:
                tester.print_experts()
                continue
            elif question.lower() in ['/clear', '/c']:
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            elif not question:
                continue
                
            # Process question
            print("\nProcessing...")
            response = await tester.process_question(question)
            
            # Print response
            if response:
                print(f"\nResponse: {response}")
            else:
                print("\nSorry, I couldn't generate a response. Please try another question.")
                
        except KeyboardInterrupt:
            print("\nExiting test tool...")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")
            print("\nAn error occurred. Please try again.")
            
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest tool stopped by user")
    except Exception as e:
        logger.error(f"Test tool crashed: {str(e)}") 