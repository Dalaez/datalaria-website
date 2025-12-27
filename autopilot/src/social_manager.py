import os
import requests
import tweepy
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

    def _smart_truncate(self, text, url, max_length=280):
        """
        Corta el texto si excede el límite de Twitter, reservando espacio para la URL.
        Twitter considera que cualquier URL ocupa 23 caracteres.
        """
        url_length = 23 # Longitud fija de URL en Twitter (t.co)
        # Espacio disponible para texto = 280 - URL - 1 espacio - 3 puntos suspensivos
        available_chars = max_length - url_length - 4 
        
        if len(text) <= available_chars:
            return f"{text} {url}"
        
        # Si es muy largo, cortamos y añadimos '...'
        truncated_text = text[:available_chars] + "..."
        print(f"✂️ Texto demasiado largo ({len(text)} chars). Cortado a: '{truncated_text}'")
        return f"{truncated_text} {url}"

    def post_to_twitter(self, text, url):
        """Publica en Twitter gestionando la longitud automáticamente."""
        # Usamos la función de truncado inteligente
        full_text = self._smart_truncate(text, url)
        
        print(f"DTO - Posting to Twitter: {full_text[:50]}...")
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
            # Si es un error 403, damos una pista extra en el log
            if "403" in str(e):
                print("   💡 PISTA: Si dice 'Forbidden', regenera tus Access Tokens en dev.twitter.com con permisos Read/Write.")

    def post_to_linkedin(self, text, url):
        """Publica en LinkedIn Empresa como un 'Artículo'."""
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
            if 'response' in locals() and response is not None:
                 print(f"LinkedIn Response info: {response.text}")

if __name__ == "__main__":
    pass