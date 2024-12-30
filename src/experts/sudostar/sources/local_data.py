from typing import Dict, List

SUDOSTAR_KNOWLEDGE_BASE = {
    "general_info": {
        "name": "SudoStar",
        "type": "Mobile Application",
        "platform": "Android & iOS",
        "description": "SudoStar is a powerful mobile application designed for automated social media management and content creation.",
        "users": "30 million users worldwide",
        "main_features": [
            "Automated content generation",
            "Social media post scheduling",
            "Multi-platform support",
            "AI-powered content optimization",
            "Analytics and performance tracking"
        ]
    },
    "key_features": {
        "content_generation": {
            "description": "Uses advanced AI to generate engaging social media content",
            "supported_platforms": ["Twitter", "Instagram", "LinkedIn", "Facebook"],
            "content_types": ["Text posts", "Captions", "Hashtags", "Thread ideas"]
        },
        "scheduling": {
            "description": "Smart scheduling system that determines optimal posting times",
            "features": [
                "Custom scheduling",
                "Auto-scheduling based on audience analytics",
                "Time zone management",
                "Queue management"
            ]
        },
        "analytics": {
            "description": "Comprehensive analytics suite for tracking content performance",
            "metrics": [
                "Engagement rates",
                "Best performing content",
                "Audience growth",
                "Optimal posting times"
            ]
        }
    },
    "rewards_system": {
        "diamonds": {
            "conversion_rate": {
                "diamonds_per_dollar": 5000,
                "minimum_withdrawal": 25000,
                "description": "Every 5000 diamonds earned can be converted to 1 USD"
            },
            "earning_methods": [
                "Content creation",
                "Daily active usage",
                "Engagement achievements",
                "Referral bonuses"
            ],
            "withdrawal_options": [
                "PayPal",
                "Bank Transfer",
                "Crypto Wallet"
            ],
            "payment_processing": {
                "processing_time": "1-3 days",
                "description": "All payments are processed and transferred to your bank account within 1-3 days after withdrawal request"
            }
        }
    },
    "technical_details": {
        "supported_platforms": ["Android 7.0+", "iOS 12.0+"],
        "backend": "Cloud-based infrastructure",
        "api_integration": ["Twitter API", "Instagram API", "OpenAI API"],
        "security": [
            "End-to-end encryption",
            "Secure OAuth authentication",
            "Regular security audits"
        ]
    },
    "use_cases": [
        "Social media managers seeking automation",
        "Content creators needing consistent posting",
        "Businesses managing multiple social accounts",
        "Influencers optimizing their social presence"
    ],
    "pricing": {
        "free_tier": {
            "name": "Basic",
            "features": [
                "Limited content generation",
                "Basic scheduling",
                "Single platform support"
            ]
        },
        "premium": {
            "name": "Professional",
            "features": [
                "Unlimited content generation",
                "Advanced scheduling",
                "Multi-platform support",
                "Full analytics suite"
            ]
        }
    }
}

COMMON_QUESTIONS = {
    "What is SudoStar?": "SudoStar is a comprehensive social media management application that helps users automate content creation and posting across multiple platforms.",
    "How does content generation work?": "SudoStar uses advanced AI algorithms to generate engaging content tailored to your audience and platform preferences.",
    "Is it available for both Android and iOS?": "Yes, SudoStar is available for both Android (7.0+) and iOS (12.0+) devices.",
    "What social media platforms are supported?": "SudoStar supports major platforms including Twitter, Instagram, LinkedIn, and Facebook.",
    "How secure is SudoStar?": "SudoStar implements enterprise-grade security measures including end-to-end encryption and secure OAuth authentication.",
    "How does the diamond reward system work?": "In SudoStar, users can earn diamonds through various activities like content creation and daily usage. Every 5000 diamonds can be converted to 1 USD, which can be withdrawn through PayPal, bank transfer, or crypto wallet.",
    "What is the minimum diamond withdrawal amount?": "The minimum withdrawal amount is 25000 diamonds, which equals to 5 USD.",
    "How long does it take to receive payments?": "After making a withdrawal request, payments are processed and transferred to your bank account within 1-3 days."
}

def get_knowledge_base() -> Dict:
    return SUDOSTAR_KNOWLEDGE_BASE

def get_common_questions() -> Dict[str, str]:
    return COMMON_QUESTIONS 