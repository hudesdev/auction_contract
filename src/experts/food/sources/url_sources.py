"""Food Expert için URL kaynakları"""

FOOD_URLS = {
    "recipes": {
        "turkish": [
            "https://www.nefisyemektarifleri.com/",
            "https://yemek.com/",
            "https://www.ardaninmutfagi.com/"
        ],
        "international": [
            "https://www.allrecipes.com/",
            "https://www.foodnetwork.com/",
            "https://www.epicurious.com/"
        ]
    },
    "restaurants": {
        "reviews": [
            "https://www.tripadvisor.com/Restaurants",
            "https://www.zomato.com/",
            "https://www.yelp.com/restaurants"
        ],
        "guides": [
            "https://guide.michelin.com/",
            "https://www.theworlds50best.com/",
            "https://www.eater.com/"
        ]
    },
    "diet": {
        "nutrition": [
            "https://www.nutritionix.com/",
            "https://www.myfitnesspal.com/",
            "https://www.eatright.org/"
        ],
        "health": [
            "https://www.healthline.com/nutrition",
            "https://www.webmd.com/diet/",
            "https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating"
        ]
    }
}

def get_urls(category: str, subcategory: str = None) -> list:
    """Belirtilen kategori için URL'leri döndür"""
    if subcategory:
        return FOOD_URLS.get(category, {}).get(subcategory, [])
    urls = []
    for subcats in FOOD_URLS.get(category, {}).values():
        urls.extend(subcats)
    return urls 