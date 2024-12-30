from experts.sports.expert import SportsExpert
from experts.food.expert import FoodExpert
from experts.ai.expert import AIExpert
from core.expert_selector import ExpertSelector
from utils.logger import Logger

def main():
    logger = Logger()
    logger.info("Expert Test Sistemi başlatılıyor...")
    
    print("\nExpert Test Sistemi")
    print("-" * 50)
    print("Aşağıdaki konularda sorular sorabilirsiniz:")
    print("1. Spor (futbol, basketbol, maçlar, antrenman)")
    print("2. Yemek (tarifler, restoranlar, diyet)")
    print("3. Yapay Zeka (teknolojiler, uygulamalar, etik)")
    print("-" * 50)
    
    # Expertleri ve seçiciyi başlat
    sports_expert = SportsExpert()
    food_expert = FoodExpert()
    ai_expert = AIExpert()
    expert_selector = ExpertSelector()
    
    while True:
        # Kullanıcıdan soru al
        print("\nSorunuzu yazın (çıkmak için 'q' yazın):")
        question = input("> ")
        
        if question.lower() == 'q':
            break
            
        # Yapay zeka ile expert seç
        expert_type = expert_selector.select_expert(question)
        logger.info(f"Seçilen uzman: {expert_type}")
        
        # Seçilen experte göre yanıt al
        if expert_type == "spor":
            response = sports_expert.get_response(question)
        elif expert_type == "yemek":
            response = food_expert.get_response(question)
        elif expert_type == "ai":
            response = ai_expert.get_response(question)
        else:
            logger.error("Uzman seçilemedi")
            print("\nÜzgünüm, sorunuzu hangi uzmana yönlendireceğimi anlayamadım.")
            print("Lütfen spor, yemek veya yapay zeka ile ilgili bir soru sorun.")
            continue
            
        # Yanıtı göster
        if response:
            print("\nYanıt:", response)
        else:
            print("\nÜzgünüm, bu soruya yanıt üretilemedi.")
            
    logger.info("Test sistemi kapatılıyor...")
    print("\nTest sistemi kapatılıyor...")

if __name__ == "__main__":
    main()