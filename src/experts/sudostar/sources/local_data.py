"""Local data for SudoStar expert"""
from typing import Dict

SUDOSTAR_KNOWLEDGE_BASE = {
    'pricing': {
        'conversion_rate': '5000 elmas = 1 USD',
        'minimum_withdrawal': '25000 elmas',
        'payment_time': '1-3 gün'
    },
    'features': {
        'live_streaming': 'Canlı yayın yapabilme',
        'gifts': 'Hediye gönderme ve alma',
        'chat': 'Sohbet etme',
        'following': 'Takip etme ve takipçi kazanma'
    },
    'common_questions': [
        'Elmaslar nasıl paraya çevrilir?',
        'Minimum çekim miktarı nedir?',
        'Ödemeler ne kadar sürede yapılır?',
        'Elmas fiyatları nedir?'
    ]
}

def get_knowledge_base():
    return SUDOSTAR_KNOWLEDGE_BASE

def get_common_questions():
    return SUDOSTAR_KNOWLEDGE_BASE['common_questions'] 