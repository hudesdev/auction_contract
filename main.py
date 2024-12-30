from src.twitter_client import TwitterClient
import time

def main():
    try:
        # Twitter client oluştur
        client = TwitterClient()
        print("✅ Twitter hesabına bağlandı\n")
        
        while True:
            print("\nTwitter Bot Başlatılıyor...")
            print("-" * 30)
            print("1: Karakterleri listele")
            print("2: Aktif karakter seç")
            print("3: Tweet gönder")
            print("4: Mention'lara yanıt ver")
            print("5: Son tweet'e gelen yorumlara yanıt ver")
            print("6: Çıkış")
            print("-" * 30)
            
            choice = input("\nHangi işlemi yapmak istersiniz? (1-6): ").strip()
            
            if choice == "1":
                client.list_characters()
                
            elif choice == "2":
                print("\nKarakter Tipleri:")
                print("- sports (Spor Uzmanı)")
                print("- ai (AI Uzmanı)")
                print("- food (Yemek Uzmanı)")
                char_type = input("\nHangi karakteri aktif yapmak istersiniz?: ").strip().lower()
                client.set_active_character(char_type)
                
            elif choice == "3":
                print("\nTweet gönderiliyor...")
                client.send_tweet()
                
            elif choice == "4":
                print("\nMention'lar kontrol ediliyor...")
                client.process_mentions()
                
            elif choice == "5":
                print("\nYorumlar kontrol ediliyor...")
                client.process_replies()
                
            elif choice == "6":
                print("\n✅ Program sonlandırılıyor...")
                break
                
            else:
                print("\n❌ Geçersiz seçim! Lütfen 1-6 arasında bir sayı girin.")
            
            # Her işlemden sonra kısa bir bekleme
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Program kullanıcı tarafından sonlandırıldı.")
    except Exception as e:
        print(f"\n❌ Program hatası: {str(e)}")

if __name__ == "__main__":
    main() 