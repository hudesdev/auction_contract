from typing import Optional, List, Dict, Any
from src.utils.logger import Logger
from src.core.event_bus import EventBus
from src.core.resource_manager import ResourceManager
from src.utils.config import ConfigLoader
import json

class BaseExpert:
    """Temel uzman sınıfı"""
    
    def __init__(self, name: str):
        """Uzmanı başlat"""
        self.name = name
        self.logger = Logger(name)
        self.event_bus = EventBus()
        
        # Konfigürasyon ve resource manager
        self.config = ConfigLoader.load_config()
        self.resource_manager = ResourceManager(self.config)
        
        # API istemcilerini al
        self.openai_client = self.resource_manager.get_openai_client()
        
        # Event'lere abone ol
        self.event_bus.subscribe("question_received", self._on_question_received)
        self.event_bus.subscribe("response_generated", self._on_response_generated)
        
        # Web arama deneme sayısı
        self.max_search_attempts = 3
        self.current_search_attempts = 0
        
    async def get_response(self, message: str) -> Optional[str]:
        """
        Mesaja yanıt üret. Akış:
        1. Bilgi alma (retrieve)
        2. Dokümanları değerlendirme (grade_documents)
        3. Web araması (websearch) - faydalı değilse tekrar
        4. Yanıt üretme (generate) - faydalı ise bitir, desteklenmiyorsa web aramaya dön
        """
        try:
            print("\n" + "="*50)
            print(f"[{self.name}] Yanıt üretme süreci başladı")
            print("="*50)
            
            # Event yayınla
            self.event_bus.publish("question_received", {
                "expert": self.name,
                "message": message
            })
            
            # 1. Bilgi alma - yerel kaynaklardan
            print("\n1. YEREL KAYNAKLARDAN BİLGİ ALMA")
            print("-"*30)
            local_docs = await self._retrieve_local_documents(message)
            if local_docs:
                print(f"- {len(local_docs)} adet yerel doküman bulundu")
            else:
                print("- Yerel doküman bulunamadı")
            
            # 2. Dokümanları değerlendir
            print("\n2. YEREL DOKÜMANLARI DEĞERLENDİRME")
            print("-"*30)
            grade_result = await self._grade_documents(local_docs, message)
            print(f"- Faydalı mı: {grade_result['is_useful']}")
            print(f"- Sebep: {grade_result.get('reason', '-')}")
            if 'relevance_score' in grade_result:
                print(f"- Alaka skoru: {grade_result['relevance_score']:.2f}")
                print(f"- Güncellik skoru: {grade_result['freshness_score']:.2f}")
                print(f"- Güvenilirlik skoru: {grade_result['reliability_score']:.2f}")
            
            if grade_result["is_useful"]:
                print("\n3. YEREL VERİDEN YANIT ÜRETME")
                print("-"*30)
                response = await self._generate_response(local_docs, message)
                if response and response["is_supported"]:
                    print("- Yanıt başarıyla üretildi")
                    print(f"- Güven skoru: {response.get('confidence', 0):.2f}")
                    self.event_bus.publish("response_generated", {
                        "expert": self.name,
                        "message": message,
                        "response": response["text"],
                        "source": "local"
                    })
                    return response["text"]
                else:
                    print("- Yerel veriden yanıt üretilemedi")
            
            # 3. Web araması döngüsü
            print("\n4. WEB ARAMASI BAŞLATILIYOR")
            print("-"*30)
            self.current_search_attempts = 0
            while not self._max_attempts_reached():
                self.current_search_attempts += 1
                print(f"\nWeb arama denemesi {self.current_search_attempts}/{self.max_search_attempts}")
                print("-"*30)
                
                web_docs = await self._websearch(message)
                if web_docs:
                    print(f"- {len(web_docs)} adet web dokümanı bulundu")
                else:
                    print("- Web dokümanı bulunamadı")
                
                # Dokümanları değerlendir
                print("\n5. WEB DOKÜMANLARINI DEĞERLENDİRME")
                print("-"*30)
                grade_result = await self._grade_documents(web_docs, message)
                print(f"- Faydalı mı: {grade_result['is_useful']}")
                print(f"- Sebep: {grade_result.get('reason', '-')}")
                if 'relevance_score' in grade_result:
                    print(f"- Alaka skoru: {grade_result['relevance_score']:.2f}")
                    print(f"- Güncellik skoru: {grade_result['freshness_score']:.2f}")
                    print(f"- Güvenilirlik skoru: {grade_result['reliability_score']:.2f}")
                
                if grade_result["is_useful"]:
                    print("\n6. WEB VERİSİNDEN YANIT ÜRETME")
                    print("-"*30)
                    response = await self._generate_response(web_docs, message)
                    if response and response["is_supported"]:
                        print("- Yanıt başarıyla üretildi")
                        print(f"- Güven skoru: {response.get('confidence', 0):.2f}")
                        self.event_bus.publish("response_generated", {
                            "expert": self.name,
                            "message": message,
                            "response": response["text"],
                            "source": "web"
                        })
                        return response["text"]
                    elif response and not response["is_supported"]:
                        print("- Yanıt desteklenmiyor, web araması tekrarlanacak")
                        continue
                
                print("\n- Web araması başarısız, tekrar deneniyor...")
            
            print("\nMAXIMUM DENEME SAYISINA ULAŞILDI")
            print("-"*30)
            return None
            
        except Exception as e:
            self.logger.error(f"Yanıt üretilirken hata: {str(e)}")
            print(f"\nHATA OLUŞTU: {str(e)}")
            return None

    async def _retrieve_local_documents(self, message: str) -> List[str]:
        """Alt sınıflar tarafından implement edilmeli"""
        return []
        
    async def _grade_documents(self, documents: List[str], message: str) -> Dict[str, Any]:
        """Dokümanların kalitesini ve ilgililiğini değerlendir"""
        if not documents:
            return {"is_useful": False, "reason": "Doküman bulunamadı"}
            
        system_prompt = """Sen bir içerik değerlendirme uzmanısın. 
        Verilen dokümanların soruya uygun ve güvenilir yanıt üretmek için yeterli olup olmadığını değerlendirmelisin.
        Değerlendirme kriterleri:
        1. Dokümanlar soruyla alakalı mı?
        2. Bilgiler güncel mi?
        3. Kaynaklar güvenilir mi?
        4. Yeterli detay var mı?
        
        Yanıtı JSON formatında ver: {
            "is_useful": boolean,
            "reason": string,
            "relevance_score": float,  # 0-1 arası alaka düzeyi
            "freshness_score": float,  # 0-1 arası güncellik
            "reliability_score": float # 0-1 arası güvenilirlik
        }"""
        
        user_message = f"""Soru: {message}
        
        Dokümanlar:
        {chr(10).join(documents)}
        
        Bu dokümanları yukarıdaki kriterlere göre değerlendir."""
        
        try:
            response = await self.openai_client.get_completion(system_prompt, user_message)
            result = json.loads(response)
            
            # Skorlar yeterince yüksek değilse faydasız olarak işaretle
            min_score = 0.7
            if (result.get("relevance_score", 0) < min_score or
                result.get("freshness_score", 0) < min_score or
                result.get("reliability_score", 0) < min_score):
                result["is_useful"] = False
                result["reason"] = "Skorlar yeterince yüksek değil"
                
            return result
        except:
            return {"is_useful": False, "reason": "Değerlendirme yapılamadı"}
            
    async def _websearch(self, message: str) -> List[str]:
        """Web araması yap ve sonuçları döndür"""
        # Araştırma tarihini ekle
        search_query = f"{message} güncel bilgi"
        
        try:
            # Tavily API ile web araması
            results = await self.web_search.search(
                search_query,
                max_results=5
            )
            
            if not results:
                return []
                
            return results
            
        except Exception as e:
            self.logger.error(f"Web arama hatası: {str(e)}")
            return []
            
    def _is_recent(self, date_str: str) -> bool:
        """Tarihin son 1 ay içinde olup olmadığını kontrol et"""
        try:
            from datetime import datetime, timedelta
            publish_date = datetime.strptime(date_str, "%Y-%m-%d")
            one_month_ago = datetime.now() - timedelta(days=30)
            return publish_date >= one_month_ago
        except:
            return True  # Tarih parse edilemezse kabul et
        
    async def _generate_response(self, documents: List[str], message: str) -> Optional[Dict[str, Any]]:
        """Dokümanları kullanarak yanıt üret"""
        if not documents:
            return None
            
        system_prompt = f"""Sen bir {self.name} uzmanısın.
        Verilen web arama sonuçlarını kullanarak soruya kapsamlı ve doğru bir yanıt üretmelisin.
        Yanıt üretirken şu kurallara uy:
        1. Web arama sonuçlarındaki bilgilerin doğruluğunu kontrol et
        2. Bilgilerin güncelliğini kontrol et
        3. Çelişkili bilgiler varsa en güvenilir kaynağı seç
        4. Emin olmadığın bilgileri verme
        5. Yanıtı JSON formatında ver: {{"text": string, "is_supported": boolean, "confidence": float}}
        6. Bilgiler yetersiz, güncel değil veya güvenilir değilse is_supported: false döndür"""
        
        user_message = f"""Soru: {message}

        Web arama sonuçları:
        {chr(10).join(documents)}
        
        Bu bilgileri kullanarak soruya yanıt ver."""
        
        try:
            response = await self.openai_client.get_completion(system_prompt, user_message)
            result = json.loads(response)
            
            # Güven skoru yeterince yüksek değilse desteklenmez olarak işaretle
            if result.get("confidence", 0) < 0.7:
                result["is_supported"] = False
                
            return result
        except:
            return None
            
    def _max_attempts_reached(self) -> bool:
        """Maximum deneme sayısına ulaşılıp ulaşılmadığını kontrol et"""
        return self.current_search_attempts >= self.max_search_attempts
        
    def _on_question_received(self, event_data: Dict[str, Any]):
        """Soru alındığında çalışır"""
        pass
        
    def _on_response_generated(self, event_data: Dict[str, Any]):
        """Yanıt üretildiğinde çalışır"""
        pass
        
    def __del__(self):
        """Cleanup"""
        self.event_bus.unsubscribe_all(self._on_question_received)
        self.event_bus.unsubscribe_all(self._on_response_generated) 