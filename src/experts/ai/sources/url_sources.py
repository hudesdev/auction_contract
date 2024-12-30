"""AI konuları için URL kaynakları"""

URL_SOURCES = {
    "general": [
        "https://www.yapayzekatr.com/yapay-zeka-nedir/",
        "https://www.ibm.com/tr-tr/topics/artificial-intelligence",
        "https://aws.amazon.com/tr/machine-learning/what-is-ai/",
        "https://www.microsoft.com/tr-tr/ai"
    ],
    "models": [
        "https://openai.com/gpt-4",
        "https://huggingface.co/docs/transformers/model_doc/bert",
        "https://ai.meta.com/llama/",
        "https://stability.ai/stable-diffusion"
    ],
    "applications": [
        "https://www.ibm.com/tr-tr/watson",
        "https://cloud.google.com/ai-platform",
        "https://azure.microsoft.com/tr-tr/solutions/ai/",
        "https://aws.amazon.com/tr/machine-learning/"
    ],
    "ethics": [
        "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics",
        "https://www.tubitak.gov.tr/tr/yapay-zeka-etik-ilkeleri",
        "https://www.europarl.europa.eu/news/en/headlines/society/20230601STO93804/eu-ai-act-first-regulation-on-artificial-intelligence",
        "https://www.who.int/news/item/28-06-2021-who-issues-first-global-report-on-ai-in-health"
    ]
}

def get_url_sources() -> dict:
    """URL kaynaklarını döndür"""
    return URL_SOURCES 