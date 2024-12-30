from src.twitter_client import TwitterClient
import time
import tweepy

def test_last_mention():
    try:
        print("\n🔄 Twitter API'ye bağlanılıyor...")
        # Twitter client oluştur
        client = TwitterClient()
        
        # Mention'ları al
        try:
            mentions = client.client.get_users_mentions(
                id=client.user_id,
                tweet_fields=['conversation_id', 'created_at', 'author_id', 'text'],
                expansions=['author_id'],
                max_results=5  # Daha az mention al
            )
        except tweepy.errors.TooManyRequests:
            print("\n⚠️ Rate limit aşıldı. Lütfen birkaç dakika sonra tekrar deneyin.")
            return False
        except Exception as e:
            print(f"\n❌ Mention'lar alınırken hata: {str(e)}")
            return False
            
        if mentions and mentions.data:
            print("\n📝 Tüm Mention'lar:")
            print("-" * 50)
            
            # Tüm mention'ları göster
            for i, mention in enumerate(mentions.data, 1):
                author = next((user for user in mentions.includes['users'] 
                             if user.id == mention.author_id), None)
                if author:
                    print(f"\n{i}. Mention:")
                    print(f"Tarih: {mention.created_at}")
                    print(f"Kimden: @{author.username}")
                    print(f"Mesaj: {mention.text}")
                    print("-" * 50)
            
            # Son mention'ı özel olarak göster
            last_mention = mentions.data[-1]
            last_author = next((user for user in mentions.includes['users'] 
                              if user.id == last_mention.author_id), None)
            
            print("\n🎯 Yanıtlanacak Son Mention:")
            print("=" * 50)
            print(f"Tarih: {last_mention.created_at}")
            print(f"Kimden: @{last_author.username}")
            print(f"Mesaj: {last_mention.text}")
            print(f"Tweet ID: {last_mention.id}")
            print("=" * 50)
            
            # Kullanıcıdan onay iste
            onay = input("\nBu mention'a yanıt vermek istiyor musunuz? (E/H): ").strip().lower()
            if onay == 'e':
                print("\n✅ Test başarılı! Bu mention'a yanıt verebilirsiniz.")
                return True
            else:
                print("\n❌ Test iptal edildi! Yanıt verilmeyecek.")
                return False
                
        else:
            print("\n❌ Hiç mention bulunamadı!")
            return False
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Test kullanıcı tarafından durduruldu.")
        return False
    except Exception as e:
        print(f"\n❌ Test hatası: {str(e)}")
        return False

if __name__ == "__main__":
    test_last_mention() 