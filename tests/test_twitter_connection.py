from src.twitter_client import TwitterClient

def test_mentions():
    try:
        # Twitter client oluştur
        client = TwitterClient()
        
        # Mention'ları al
        mentions = client.client.get_users_mentions(
            id=client.user_id,
            tweet_fields=['conversation_id', 'created_at', 'author_id', 'text'],
            expansions=['author_id']
        )
        
        if mentions and mentions.data:
            print("\n✅ Mention'lar Bulundu")
            print("-" * 30)
            
            # Tüm mention'ları göster
            for i, mention in enumerate(mentions.data, 1):
                author = next((user for user in mentions.includes['users'] 
                             if user.id == mention.author_id), None)
                if author:
                    print(f"\n{i}. Mention:")
                    print(f"Kimden: @{author.username}")
                    print(f"Mesaj: {mention.text}")
                    print(f"Tweet ID: {mention.id}")
                    print("-" * 30)
            
            # Son mention'ı özel olarak göster
            last_mention = mentions.data[-1]
            last_author = next((user for user in mentions.includes['users'] 
                              if user.id == last_mention.author_id), None)
            
            print("\n🔄 Yanıtlanacak Son Mention:")
            print("-" * 30)
            print(f"Kimden: @{last_author.username}")
            print(f"Mesaj: {last_mention.text}")
            print(f"Tweet ID: {last_mention.id}")
            print("-" * 30)
            
            return True
        else:
            print("\n❌ Hiç mention bulunamadı!")
            return False
            
    except Exception as e:
        print(f"\n❌ Test hatası: {str(e)}")
        return False

if __name__ == "__main__":
    test_mentions() 