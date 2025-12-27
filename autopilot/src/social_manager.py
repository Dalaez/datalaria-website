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

    def post_to_linkedin(self, content):
        print(f"DTO - Posting to LinkedIn: {content[:50]}...")
        
        headers = {
            'Authorization': f'Bearer {self.linkedin_access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        try:
            # LOGICA HÍBRIDA: EMPRESA O PERSONAL
            company_id = os.getenv("LINKEDIN_COMPANY_ID")
            
            if company_id:
                # Opción A: Publicar como Empresa (Organization)
                print(f"🏢 Detectado Company ID: {company_id}. Intentando publicar como página...")
                author_urn = f"urn:li:organization:{company_id}"
            else:
                # Opción B: Publicar como Perfil Personal (Person)
                print("👤 No hay Company ID. Publicando como perfil personal...")
                user_info_url = "https://api.linkedin.com/v2/userinfo"
                response_user = requests.get(user_info_url, headers=headers)
                if response_user.status_code != 200:
                    raise Exception(f"Error fetching Profile: {response_user.text}")
                user_data = response_user.json()
                person_urn = user_data.get('sub')
                if not person_urn:
                    raise Exception("Could not find user URN (sub)")
                author_urn = f"urn:li:person:{person_urn}"
            
            # PASO 2: Publicar
            post_url = "https://api.linkedin.com/v2/ugcPosts"
            
            post_data = {
                "author": author_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            response_post = requests.post(post_url, headers=headers, json=post_data)
            
            if response_post.status_code == 201:
                print(f"✅ LinkedIn Success! Post ID: {response_post.json()['id']}")
                return response_post.json()['id']
            else:
                # Si falla aquí es probablemente por falta de permisos (w_organization_social)
                raise Exception(f"Status {response_post.status_code}: {response_post.text}")

        except Exception as e:
            print(f"❌ Error posting to LinkedIn: {str(e)}")
            return None

if __name__ == "__main__":
    print("--- TESTING SOCIAL MEDIA MANAGER ---")
    manager = SocialMediaManager()
    msg = "¡SISTEMA VERIFICADO! ✅ Datalaria Autopilot ahora tiene permiso OFICIAL para publicar en la Página de Empresa de LinkedIn y en X. La burocracia ha sido derrotada. 🤖👔 #BuildingInPublic #Python #Automation"
    
    # Prueba Twitter
    manager.post_to_twitter(msg)
    
    # Prueba LinkedIn
    manager.post_to_linkedin(msg)
    
    print("--- TEST COMPLETED ---")
