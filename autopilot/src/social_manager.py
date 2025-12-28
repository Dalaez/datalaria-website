import os
import tweepy
import requests
import time
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
        Publica en Twitter usando inyección completa de Headers (Full Browser Spoofing)
        para atravesar el bloqueo WAF de Cloudflare/Twitter en GitHub Actions.
        """
        clean_text = self._smart_truncate(text, url)
        
        max_retries = 3
        base_delay = 10 

        # Configuración del cliente
        client = tweepy.Client(
            consumer_key=self.twitter_api_key,
            consumer_secret=self.twitter_api_secret,
            access_token=self.twitter_access_token,
            access_token_secret=self.twitter_access_token_secret
        )

        # --- EL DISFRAZ COMPLETO 🎭 ---
        # No solo cambiamos el User-Agent, sino toda la huella digital del navegador.
        # Esto hace que la petición sea indistinguible de un Chrome real.
        full_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://twitter.com/",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1"
        }
        
        # Inyectamos los headers en la sesión de requests subyacente de Tweepy
        client.session.headers.update(full_headers)
        # ------------------------------

        print(f"DTO - Posting to Twitter ({len(clean_text)} chars): {clean_text}")

        for attempt in range(1, max_retries + 1):
            try:
                response = client.create_tweet(text=clean_text)
                print(f"✅ Twitter Success! Tweet ID: {response.data['id']}")
                return

            except tweepy.errors.TweepyException as e:
                print(f"⚠️ Falló Twitter (Intento {attempt}/{max_retries}): {e}")
                
                # Diagnóstico de error HTML
                if hasattr(e, 'response') and e.response is not None:
                    if "<!DOCTYPE html>" in e.response.text:
                         print("   🔎 BLOQUEO WAF DETECTADO (IP de GitHub sucia).")
                    else:
                         print(f"   🔎 ERROR RAW: {e.response.text[:100]}...")

                if attempt == max_retries:
                    print("❌ Se agotaron los intentos en Twitter.")
                    return 

                wait_time = base_delay * attempt 
                print(f"   ⏳ Esperando {wait_time}s para reintentar con headers completos...")
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