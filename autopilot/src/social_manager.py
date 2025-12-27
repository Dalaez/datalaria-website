import tweepy
import requests
import os
import json
from dotenv import load_dotenv
from pathlib import Path

# 1. CARGA ROBUSTA DEL .ENV
# Busca el .env subiendo niveles hasta encontrarlo, o asume que está en la carpeta padre de src
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class SocialMediaManager:
    def __init__(self):
        # Cargar credenciales
        self.twitter_api_key = os.getenv("TWITTER_API_KEY")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET")
        self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.twitter_access_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        
        self.linkedin_access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.linkedin_client_id = os.getenv("LINKEDIN_CLIENT_ID")

    def post_to_twitter(self, content):
        print(f"DTO - Posting to Twitter: {content[:50]}...")
        try:
            # Autenticación API v2
            client = tweepy.Client(
                consumer_key=self.twitter_api_key,
                consumer_secret=self.twitter_api_secret,
                access_token=self.twitter_access_token,
                access_token_secret=self.twitter_access_secret
            )
            
            response = client.create_tweet(text=content)
            print(f"✅ Twitter Success! Tweet ID: {response.data['id']}")
            return response.data['id']
            
        except Exception as e:
            print(f"❌ Error posting to Twitter: {str(e)}")
            return None

    def post_to_linkedin(self, text):
        """Publica SÓLO en la página de empresa. Si no hay ID, aborta."""
        url = "https://api.linkedin.com/v2/ugcPosts"
        
        # VERIFICACIÓN ESTRICTA
        if not self.company_id:
            print("⚠️ BLOQUEADO: No se encontró LINKEDIN_COMPANY_ID configurado.")
            print("   La publicación en perfil personal está desactivada por seguridad.")
            return # Salimos de la función sin hacer nada más

        # Si llegamos aquí, es porque HAY Company ID
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
            print(f"❌ Error posting to LinkedIn Company Page: {e}")
            if response is not None:
                print(f"Response Content: {response.text}")

if __name__ == "__main__":
    print("--- TESTING SOCIAL MEDIA MANAGER ---")
    manager = SocialMediaManager()
    msg = "¡SISTEMA VERIFICADO! ✅ Datalaria Autopilot ahora tiene permiso OFICIAL para publicar en la Página de Empresa de LinkedIn y en X. La burocracia ha sido derrotada. 🤖👔 #BuildingInPublic #Python #Automation"
    
    # Prueba Twitter
    manager.post_to_twitter(msg)
    
    # Prueba LinkedIn
    manager.post_to_linkedin(msg)
    
    print("--- TEST COMPLETED ---")
