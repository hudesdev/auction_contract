# Twitter Bot

Bu bot, Twitter'da mention'lara ve tweet yanıtlarına otomatik olarak cevap veren bir AI asistanıdır.

## Özellikler

- Mention'lara otomatik yanıt verme
- Tweet'lere gelen yorumlara otomatik yanıt verme
- OpenAI GPT-3.5 ile akıllı yanıtlar oluşturma
- Rate limiting ve günlük tweet limiti kontrolü
- Detaylı loglama sistemi

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. `.env` dosyasını oluşturun ve aşağıdaki değişkenleri ekleyin:
```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
OPENAI_API_KEY=your_openai_api_key
```

## Kullanım

Programı başlatmak için:
```bash
python main.py
```

İki mod arasında seçim yapabilirsiniz:
1. Mention'lara otomatik yanıt verme
2. Tweet'lere gelen yorumlara otomatik yanıt verme

## Proje Yapısı

```
.
├── config/
│   └── config.py         # Konfigürasyon ayarları
├── src/
│   ├── twitter_client.py # Twitter API işlemleri
│   ├── openai_client.py  # OpenAI API işlemleri
│   └── tweet_handler.py  # Tweet işleme mantığı
├── utils/
│   ├── logger.py        # Loglama sistemi
│   └── rate_limiter.py  # Rate limiting işlemleri
├── logs/                # Log dosyaları
├── .env                 # Ortam değişkenleri
├── main.py             # Ana program
└── requirements.txt    # Gerekli paketler
```

## Güvenlik

- API anahtarları `.env` dosyasında güvenli bir şekilde saklanır
- Rate limiting ile API kullanımı kontrol edilir
- Günlük tweet limiti ile aşırı kullanım engellenir

## Lisans

MIT 