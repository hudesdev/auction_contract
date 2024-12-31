"""URL sources for SudoStar expert"""

URL_SOURCES = {
    "official": [
        "https://sudostar.com",
        "https://sudostar.com/pricing",
        "https://sudostar.com/features"
    ],
    "documentation": [
        "https://docs.sudostar.com",
        "https://docs.sudostar.com/payment",
        "https://docs.sudostar.com/diamonds"
    ],
    "support": [
        "https://support.sudostar.com",
        "https://support.sudostar.com/faq",
        "https://support.sudostar.com/payment-guide"
    ]
}

def get_url_sources(source_type: str = "official") -> list:
    """Get URL sources by type
    
    Args:
        source_type (str): Type of URLs to get
        
    Returns:
        list: List of URLs
    """
    return URL_SOURCES.get(source_type, []) 