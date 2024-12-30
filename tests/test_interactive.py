from src.experts import SudoStarExpert

def get_concise_answer(context, question):
    """En fazla 3 cümlelik özet yanıt oluştur"""
    if "rewards_system" in context["knowledge_base"]:
        rewards = context["knowledge_base"]["rewards_system"]["diamonds"]
        
        # İngilizce terimleri Türkçeye çevir
        method_translations = {
            "Content creation": "İçerik oluşturma",
            "Daily active usage": "Günlük aktif kullanım",
            "Engagement achievements": "Etkileşim başarıları",
            "Referral bonuses": "Referans bonusları"
        }
        
        # Ödeme süresini Türkçeleştir
        payment_time = rewards['payment_processing']['processing_time'].replace("days", "gün")
        
        # Soru elmas-dolar dönüşümü ile ilgiliyse
        if "dönüşüm" in question.lower() or "kaç dolar" in question.lower() or "kaç elmas" in question.lower():
            return f"SudoStar'da {rewards['conversion_rate']['diamonds_per_dollar']} elmas = 1 USD"
            
        # Soru minimum çekim ile ilgiliyse
        if "minimum" in question.lower() or "en az" in question.lower():
            return f"Minimum çekim miktarı {rewards['conversion_rate']['minimum_withdrawal']} elmastır."
            
        # Soru ödeme süresi ile ilgiliyse
        if "kaç gün" in question.lower() or "ne zaman" in question.lower() or "süre" in question.lower():
            return f"Ödemeler {payment_time} içinde hesabınıza aktarılır."
        
        # Soru kazanma yöntemleri ile ilgiliyse
        if "nasıl kazan" in question.lower() or "nasıl elde ed" in question.lower():
            methods = [method_translations.get(m, m) for m in rewards["earning_methods"]]
            methods_str = ", ".join(methods)
            return f"Elmas kazanma yöntemleri: {methods_str}"
            
        # Soru ödeme yöntemleri ile ilgiliyse
        if "ödeme" in question.lower() or "para çek" in question.lower() or "nasıl çek" in question.lower():
            options = ", ".join(rewards["withdrawal_options"])
            return f"Ödeme seçenekleri: {options}"
            
        # Soru elmas ödül sistemi hakkındaysa
        if "ödül sistemi" in question.lower() or "nasıl çalışır" in question.lower():
            methods = [method_translations.get(m, m) for m in rewards["earning_methods"]]
            methods_str = ", ".join(methods)
            return f"SudoStar'da {methods_str} yoluyla elmas kazanabilirsiniz. Her {rewards['conversion_rate']['diamonds_per_dollar']} elmas = 1 USD'dir. Minimum çekim {rewards['conversion_rate']['minimum_withdrawal']} elmastır."
    
    # Sık sorulan sorulardan yanıt varsa
    if "common_questions" in context:
        for q, a in context["common_questions"].items():
            if any(keyword in question.lower() for keyword in q.lower().split()):
                return a
    
    return "Üzgünüm, bu soru için yeterli bilgi bulamadım."

def main():
    # Expert'i oluştur
    expert = SudoStarExpert()
    
    print("\nSudoStar Expert Test Sistemi")
    print("-" * 50)
    print("SudoStar uygulaması hakkında sorularınızı sorabilirsiniz.")
    print("Çıkmak için 'q' yazın.")
    print("-" * 50)
    
    while True:
        # Kullanıcıdan soru al
        print("\nSorunuzu yazın:")
        question = input("> ").strip()
        
        # Çıkış kontrolü
        if question.lower() == 'q':
            print("\nProgram sonlandırılıyor...")
            break
            
        if not question:
            print("\nLütfen bir soru girin.")
            continue
            
        # Soruyu yanıtla
        context = expert.get_relevant_context(question)
        answer = get_concise_answer(context, question)
        
        print("\nYanıt:")
        print("-" * 30)
        print(answer)

if __name__ == "__main__":
    main() 