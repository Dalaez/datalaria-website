import os
import tweepy
import requests
import random 
from dotenv import load_dotenv

class SocialMediaManager:
    def __init__(self):
        load_dotenv()
        self.twitter_api_key = os.getenv("TWITTER_API_KEY")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET")
        self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self.linkedin_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.company_id = os.getenv("LINKEDIN_COMPANY_ID")

    def _clean_text(self, text):
        """Elimina espacios extra y caracteres invisibles que confunden a las APIs."""
        return " ".join(text.split())

    def _smart_truncate(self, text, url, max_length=240): # Bajamos a 240 por seguridad (emojis)
        """
        Corta el texto reservando espacio para URL.
        """
        text = self._clean_text(text)
        url_length = 23
        # Dejamos espacio para URL + espacio + puntos suspensivos
        available_chars = max_length - url_length - 5 
        
        if len(text) <= available_chars:
            return f"{text} {url}"
        
        truncated_text = text[:available_chars] + "..."
        return f"{truncated_text} {url}"

    def post_to_twitter(self, text, url):
        """Publica en Twitter."""
        # TRUCO ANTI-DUPLICADOS: Añadimos un ID invisible o pequeño al final si estamos probando
        # Esto evita el error 403 por "Status is a duplicate"
        # Cuando todo funcione estable, puedes quitar la siguiente línea.
        run_id = random.randint(1000, 9999)
        
        clean_text = self._smart_truncate(text, url)
        
        # Opcional: Añadir ID para debug (evita error de duplicado)
        # full_text = f"{clean_text} [ID:{run_id}]" 
        # Pero mejor intentamos enviar limpio primero con el truncado agresivo
        full_text = clean_text 

        print(f"DTO - Posting to Twitter ({len(full_text)} chars): {full_text}")
        
        try:
            client = tweepy.Client(
                consumer_key=self.twitter_api_key,
                consumer_secret=self.twitter_api_secret,
                access_token=self.twitter_access_token,
                access_token_secret=self.twitter_access_token_secret
            )
            response = client.create_tweet(text=full_text)
            print(f"✅ Twitter Success! Tweet ID: {response.data['id']}")
        except Exception as e:
            print(f"⚠️ Falló Twitter: {e}")
            # Si falla, probamos el reintento con ID anti-duplicado
            if "403" in str(e):
                print("   🔄 Reintentando con ID único para evitar filtro de duplicados...")
                try:
                    full_text_unique = f"{full_text} 🤖{run_id}"
                    response = client.create_tweet(text=full_text_unique)
                    print(f"   ✅ Twitter Success (Intento 2)! ID: {response.data['id']}")
                except Exception as e2:
                    print(f"   ❌ Reintento fallido: {e2}")

    def post_to_linkedin(self, text, url):
        """Publica en LinkedIn."""
        text = self._clean_text(text) # Limpieza básica
        print(f"DTO - Posting to LinkedIn: {text[:50]}...")
        
        if not self.company_id:
            print("⚠️ BLOQUEADO LinkedIn: No se encontró LINKEDIN_COMPANY_ID.")
            return

        api_url = "https://api.linkedin.com/v2/ugcPosts"
        author = f"urn:li:organization:{self.company_id}"
        
        headers = {
            "Authorization": f"Bearer {self.linkedin_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        payload = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "originalUrl": url
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            print(f"✅ LinkedIn Success! Post ID: {response.json().get('id')}")
        except Exception as e:
            print(f"⚠️ Falló LinkedIn: {e}")

if __name__ == "__main__":
    pass