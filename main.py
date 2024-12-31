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
            print("1: Tweet gönder")
            print("2: Çıkış")
            print("-" * 30)
            
            choice = input("\nHangi işlemi yapmak istersiniz? (1-2): ").strip()
            
            if choice == "1":
                tweet_text = input("\nGöndermek istediğiniz tweet'i yazın: ").strip()
                if client.post_tweet(tweet_text):
                    print("\n✅ Tweet başarıyla gönderildi!")
                else:
                    print("\n❌ Tweet gönderilemedi!")
                
            elif choice == "2":
                print("\n✅ Program sonlandırılıyor...")
                break
                
            else:
                print("\n❌ Geçersiz seçim! Lütfen 1-2 arasında bir sayı girin.")
            
            # Her işlemden sonra kısa bir bekleme
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Program kullanıcı tarafından sonlandırıldı.")
    except Exception as e:
        print(f"\n❌ Program hatası: {str(e)}")

if __name__ == "__main__":
    main() 