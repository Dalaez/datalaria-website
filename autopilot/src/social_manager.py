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
        self.devto_api_key = os.getenv("DEVTO_API_KEY")
        self.devto_org_id = os.getenv("DEVTO_ORG_ID")

        # Configurar Tweepy Client (v2) - Para postear tweets
        self.client_v2 = None
        # Configurar Tweepy API (v1.1) - Para subir imágenes (media_upload)
        self.api_v1 = None

        if self.twitter_api_key:
            try:
                # Client v2
                self.client_v2 = tweepy.Client(
                    consumer_key=self.twitter_api_key,
                    consumer_secret=self.twitter_api_secret,
                    access_token=self.twitter_access_token,
                    access_token_secret=self.twitter_access_token_secret
                )
                
                # API v1.1 (Auth OAuth1UserHandler)
                auth = tweepy.OAuth1UserHandler(
                    self.twitter_api_key, self.twitter_api_secret,
                    self.twitter_access_token, self.twitter_access_token_secret
                )
                self.api_v1 = tweepy.API(auth)
            except Exception as e:
                print(f"⚠️ Error inicializando Twitter clients: {e}")

    def _clean_text(self, text):
        return " ".join(text.split())

    def _smart_truncate(self, text, url, max_length=230):
        # NOTA: Para Twitter seguimos limpiando espacios extra, pero
        # podríamos relajarlo si quisiéramos saltos de línea en Twitter también.
        text = self._clean_text(text)
        url_length = 23
        available_chars = max_length - url_length - 5 
        
        if len(text) <= available_chars:
            return f"{text} {url}"
        
        truncated_text = text[:available_chars] + "..."
        return f"{truncated_text} {url}"

    # ... post_to_devto ...

    def post_to_twitter(self, text, url):
        """Publica en Twitter gestionando la longitud automáticamente."""
        if not self.client_v2:
            print("⚠️ Twitter no configurado (Faltan credenciales o error init).")
            return

        full_text = self._smart_truncate(text, url)
        print(f"DTO - Posting to Twitter ({len(full_text)} chars): {full_text}...")
        
        try:
            response = self.client_v2.create_tweet(text=full_text)    
            print(f"✅ Twitter Success! Tweet ID: {response.data['id']}")
        
        except tweepy.errors.TweepyException as e:
            # Enhanced Debugging
            print(f"⚠️ Falló Twitter (Tweepy Error): {e}")
            print(f"   🔍 Debug Info: {type(e)}")
            
            if hasattr(e, 'response') and e.response:
                print(f"   🔴 Status Code: {e.response.status_code}")
                # Intentar leer cuerpo JSON si existe
                try: 
                   print(f"   🔴 Response JSON: {e.response.json()}")
                except:
                   print(f"   🔴 Response Text: {e.response.text}") # Descomentado para debug granular
            
            if hasattr(e, 'api_messages'):
                print(f"   🔴 API Messages: {e.api_messages}")

            # Fallback: Intentar solo texto si falló con imagen
            if media_ids:
                print("   🔄 Intentando FALLBACK (Solo Texto) por si la imagen causó el error...")
                try:
                    response = self.client_v2.create_tweet(text=full_text)
                    print(f"✅ Twitter Fallback Success! (Solo Texto). Tweet ID: {response.data['id']}")
                    return # Salimos con éxito parcial
                except Exception as e_fallback:
                    print(f"   ⚠️ El fallback también falló: {e_fallback}")
            
            if "403" in str(e):
                print("   💡 PISTA 403: Forbidden. Puede ser:")
                print("      1. Credenciales incorrectas o sin permisos de escritura.")
                print("      2. Contenido duplicado.")
                print("      3. Contenido demasiado largo.")
            if "401" in str(e):
                print("   💡 PISTA 401: Unauthorized. Revisa tus API KEYS y TOKENS.")

    def post_to_linkedin(self, text, url):
        """Publica en LinkedIn."""
        # CORRECCIÓN: NO usamos _clean_text aquí para respetar los saltos de línea
        # text = self._clean_text(text) <-- ELIMINADO
        
        # Solo hacemos un strip() básico por si acaso
        text = text.strip()
        
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