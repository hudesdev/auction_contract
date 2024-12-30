from typing import Dict

SYSTEM_PROMPTS = {
    "general_expert": """You are an expert on the SudoStar mobile application, a comprehensive social media management and automation tool. 
You have deep knowledge about its features, capabilities, technical aspects, and best practices.
Provide accurate, helpful information about SudoStar while maintaining a professional and informative tone.""",
    
    "technical_support": """You are a technical support specialist for SudoStar application.
Your role is to help users troubleshoot issues, explain technical concepts, and provide step-by-step guidance for using SudoStar's features.
Focus on clear, actionable solutions while being patient and thorough in your explanations.""",
    
    "feature_expert": """You are a SudoStar feature specialist with extensive knowledge of the application's capabilities.
Your expertise covers content generation, scheduling, analytics, and platform integrations.
Provide detailed explanations and practical examples of how to best utilize SudoStar's features."""
}

USER_PROMPT_TEMPLATES = {
    "feature_inquiry": """Please explain how the {feature_name} feature works in SudoStar and provide best practices for using it effectively.""",
    
    "troubleshooting": """I'm experiencing the following issue with SudoStar: {issue_description}
What are the possible causes and solutions?""",
    
    "comparison": """How does SudoStar's {feature_name} compare to similar features in other social media management tools?""",
    
    "setup_guide": """Please provide a step-by-step guide for setting up {feature_name} in SudoStar."""
}

def get_system_prompt(prompt_type: str) -> str:
    return SYSTEM_PROMPTS.get(prompt_type, SYSTEM_PROMPTS["general_expert"])

def get_user_prompt_template(template_type: str) -> str:
    return USER_PROMPT_TEMPLATES.get(template_type, "") 