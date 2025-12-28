import os
import tweepy
import requests
import time
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
        return " ".join(text.split())

    def _smart_truncate(self, text, url, max_length=230):
        text = self._clean_text(text)
        url_length = 23
        available_chars = max_length - url_length - 5 
        
        if len(text) <= available_chars:
            return f"{text} {url}"
        
        truncated_text = text[:available_chars] + "..."
        return f"{truncated_text} {url}"

    def post_to_twitter(self, text, url):
        """
        Publica en Twitter usando 'Warm-up': valida credenciales primero para establecer sesión
        y evitar el bloqueo WAF directo en el POST.
        """
        clean_text = self._smart_truncate(text, url)
        
        max_retries = 3
        base_delay = 5 

        client = tweepy.Client(
            consumer_key=self.twitter_api_key,
            consumer_secret=self.twitter_api_secret,
            access_token=self.twitter_access_token,
            access_token_secret=self.twitter_access_token_secret
        )

        print(f"DTO - Posting to Twitter ({len(clean_text)} chars): {clean_text}")

        for attempt in range(1, max_retries + 1):
            try:
                # --- WARM-UP 🔥 ---
                # Hacemos una petición de lectura ligera antes de intentar escribir.
                # Esto a veces 'bypassea' la pantalla de 'Just a moment...' al validar la sesión.
                if attempt == 1:
                    print("   🔍 Verificando sesión (Warm-up)...")
                    me = client.get_me()
                    print(f"   ✅ Sesión activa como @{me.data.username}")
                    time.sleep(2) # Pausa corta de cortesía
                # ------------------

                response = client.create_tweet(text=clean_text)
                print(f"✅ Twitter Success! Tweet ID: {response.data['id']}")
                return

            except tweepy.errors.TweepyException as e:
                print(f"⚠️ Falló Twitter (Intento {attempt}/{max_retries}): {e}")
                
                if hasattr(e, 'response') and e.response is not None:
                    # Imprimir solo un poco del error para no llenar la pantalla de HTML
                    error_msg = e.response.text[:100].replace('\n', ' ')
                    print(f"   🔎 RAW SERVER MSG: {error_msg}...")

                if attempt == max_retries:
                    print("❌ Se agotaron los intentos en Twitter.")
                    return 

                wait_time = base_delay * attempt 
                print(f"   ⏳ Esperando {wait_time}s para reintentar...")
                time.sleep(wait_time)

    def post_to_linkedin(self, text, url):
        """Publica en LinkedIn."""
        text = self._clean_text(text)
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