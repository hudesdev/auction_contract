"""Local data for SudoStar expert"""
from typing import Dict

SUDOSTAR_KNOWLEDGE_BASE = {
    "pricing": {
        "conversion_rates": {
            "usd_to_diamonds": 5000,  # 1 USD = 5000 diamonds
            "diamonds_to_usd": 0.0002  # 1 diamond = 0.0002 USD
        },
        "minimum_withdrawal": {
            "amount": 25000,
            "unit": "diamonds"
        },
        "payment_methods": [
            "PayPal",
            "Bank Transfer",
            "Crypto Wallet"
        ],
        "processing_time": "1-3 business days"
    },
    "common_questions": {
        "diamond_conversion": "1 USD = 5000 elmas, 1000 elmas = 0.2 USD",
        "minimum_withdrawal": "Minimum çekim miktarı 25000 elmastır",
        "payment_time": "Ödemeler 1-3 iş günü içinde yapılır",
        "payment_methods": "PayPal, Banka transferi veya Kripto cüzdan ile ödeme alabilirsiniz"
    }
}

def get_knowledge_base() -> Dict:
    """Get knowledge base
    
    Returns:
        Dict: Knowledge base data
    """
    return SUDOSTAR_KNOWLEDGE_BASE 