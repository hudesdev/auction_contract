import unittest
from src.experts import SudoStarExpert

class TestSudoStarExpert(unittest.TestCase):
    def setUp(self):
        self.expert = SudoStarExpert()

    def test_expert_initialization(self):
        """Test if expert initializes correctly with all required attributes"""
        self.assertIsNotNone(self.expert)
        self.assertEqual(self.expert.name, "sudostar")
        self.assertIsNotNone(self.expert.knowledge_base)
        self.assertIsNotNone(self.expert.common_questions)
        self.assertIsNotNone(self.expert.search_queries)
        self.assertIsNotNone(self.expert.url_sources)

    def test_get_expert_info(self):
        """Test if expert info is returned correctly"""
        info = self.expert.get_expert_info()
        self.assertIsInstance(info, dict)
        self.assertIn("name", info)
        self.assertIn("description", info)
        self.assertIn("capabilities", info)
        self.assertIsInstance(info["capabilities"], list)
        self.assertTrue(len(info["capabilities"]) > 0)

    def test_get_relevant_context(self):
        """Test if relevant context is returned for a query"""
        query = "How does content generation work in SudoStar?"
        context = self.expert.get_relevant_context(query)
        
        self.assertIsInstance(context, dict)
        self.assertIn("knowledge_base", context)
        self.assertIn("common_questions", context)
        self.assertIn("urls", context)

    def test_get_system_prompt(self):
        """Test if appropriate system prompts are returned"""
        # Test general prompt
        general_prompt = self.expert.get_system_prompt()
        self.assertIsInstance(general_prompt, str)
        self.assertIn("SudoStar", general_prompt)

        # Test technical prompt
        technical_prompt = self.expert.get_system_prompt("technical setup")
        self.assertIsInstance(technical_prompt, str)
        self.assertIn("technical", technical_prompt.lower())

        # Test feature prompt
        feature_prompt = self.expert.get_system_prompt("feature explanation")
        self.assertIsInstance(feature_prompt, str)
        self.assertIn("feature", feature_prompt.lower())

    def test_knowledge_base_content(self):
        """Test if knowledge base contains required information"""
        kb = self.expert.knowledge_base
        
        # Check general info
        self.assertIn("general_info", kb)
        self.assertEqual(kb["general_info"]["name"], "SudoStar")
        
        # Check key features
        self.assertIn("key_features", kb)
        self.assertIn("content_generation", kb["key_features"])
        self.assertIn("scheduling", kb["key_features"])
        self.assertIn("analytics", kb["key_features"])

        # Check technical details
        self.assertIn("technical_details", kb)
        self.assertIn("supported_platforms", kb["technical_details"])
        self.assertIn("security", kb["technical_details"])

    def test_common_questions(self):
        """Test if common questions are available and formatted correctly"""
        questions = self.expert.common_questions
        self.assertIsInstance(questions, dict)
        self.assertTrue(len(questions) > 0)
        
        # Check if questions have answers
        for question, answer in questions.items():
            self.assertIsInstance(question, str)
            self.assertIsInstance(answer, str)
            self.assertTrue(len(answer) > 0)

    def test_pricing_information(self):
        """Test querying pricing information"""
        # Get knowledge base
        kb = self.expert.knowledge_base
        
        # Check pricing structure
        self.assertIn("pricing", kb)
        pricing = kb["pricing"]
        
        # Test Free Tier
        self.assertIn("free_tier", pricing)
        free_tier = pricing["free_tier"]
        self.assertEqual(free_tier["name"], "Basic")
        self.assertIsInstance(free_tier["features"], list)
        self.assertIn("Limited content generation", free_tier["features"])
        
        # Test Premium Tier
        self.assertIn("premium", pricing)
        premium = pricing["premium"]
        self.assertEqual(premium["name"], "Professional")
        self.assertIsInstance(premium["features"], list)
        self.assertIn("Unlimited content generation", premium["features"])
        
        # Test getting context for pricing query
        context = self.expert.get_relevant_context("What are the pricing plans for SudoStar?")
        self.assertIn("knowledge_base", context)
        self.assertIn("pricing", context["knowledge_base"])

    def test_diamond_reward_system(self):
        """Test diamond reward system information"""
        # Get knowledge base
        kb = self.expert.knowledge_base
        
        # Check rewards system structure
        self.assertIn("rewards_system", kb)
        self.assertIn("diamonds", kb["rewards_system"])
        
        # Check conversion rate
        diamonds = kb["rewards_system"]["diamonds"]
        self.assertIn("conversion_rate", diamonds)
        conversion = diamonds["conversion_rate"]
        self.assertEqual(conversion["diamonds_per_dollar"], 5000)
        self.assertEqual(conversion["minimum_withdrawal"], 5000)
        
        # Check earning methods
        self.assertIn("earning_methods", diamonds)
        self.assertIsInstance(diamonds["earning_methods"], list)
        self.assertTrue(len(diamonds["earning_methods"]) > 0)
        
        # Check payment processing information
        self.assertIn("payment_processing", diamonds)
        processing = diamonds["payment_processing"]
        self.assertEqual(processing["processing_time"], "2 days")
        self.assertIn("bank account within 2 days", processing["description"])
        
        # Check common questions about payments
        questions = self.expert.common_questions
        self.assertIn("How long does it take to receive payments?", questions)
        self.assertIn("2 days", questions["How long does it take to receive payments?"])

if __name__ == '__main__':
    unittest.main() 