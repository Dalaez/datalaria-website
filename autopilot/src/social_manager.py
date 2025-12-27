import os
import requests
import tweepy
from dotenv import load_dotenv

class SocialMediaManager:
    def __init__(self):
        # Carga variables si estás en local (.env). En GitHub Actions las coge del entorno.
        load_dotenv()
        
        # Twitter Credentials
        self.twitter_api_key = os.getenv("TWITTER_API_KEY")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET")
        self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        
        # LinkedIn Credentials
        self.linkedin_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        # --- AQUÍ ESTABA EL ERROR ---
        # Necesitamos inicializar esta variable para usarla luego en self.company_id
        self.company_id = os.getenv("LINKEDIN_COMPANY_ID") 

    def post_to_twitter(self, text):
        try:
            client = tweepy.Client(
                consumer_key=self.twitter_api_key,
                consumer_secret=self.twitter_api_secret,
                access_token=self.twitter_access_token,
                access_token_secret=self.twitter_access_token_secret
            )
            response = client.create_tweet(text=text)
            print(f"✅ Twitter Success! Tweet ID: {response.data['id']}")
            return response
        except Exception as e:
            print(f"❌ Error posting to Twitter: {e}")

    def post_to_linkedin(self, text):
        """Publica SÓLO en la página de empresa. Si no hay ID, aborta."""
        url = "https://api.linkedin.com/v2/ugcPosts"
        
        # 1. VERIFICACIÓN DE SEGURIDAD
        if not self.company_id:
            print("⚠️ BLOQUEADO: No se encontró LINKEDIN_COMPANY_ID configurado.")
            print("   La publicación se ha cancelado para evitar usar el perfil personal.")
            return

        # 2. Publicación Corporativa
        print(f"🏢 Publicando en Página de Empresa (ID: {self.company_id})...")
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
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            print(f"✅ LinkedIn Success! Post ID: {response.json().get('id')}")
        except Exception as e:
            print(f"❌ Error posting to LinkedIn: {e}")
            if 'response' in locals() and response is not None:
                print(f"Response Content: {response.text}")

if __name__ == "__main__":
    # Prueba rápida local
    manager = SocialMediaManager()
    print("Iniciando prueba de SocialManager...")
    # manager.post_to_twitter("Prueba Twitter") # Descomentar para probar