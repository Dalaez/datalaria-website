import os
import requests
import tweepy
from dotenv import load_dotenv

class SocialMediaManager:
    def __init__(self):
        load_dotenv()
        # Twitter Credentials
        self.twitter_api_key = os.getenv("TWITTER_API_KEY")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET")
        self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        # LinkedIn Credentials
        self.linkedin_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.company_id = os.getenv("LINKEDIN_COMPANY_ID")

    def post_to_twitter(self, text, url):
        """Publica en Twitter concatenando texto y URL."""
        print(f"DTO - Posting to Twitter: {text[:50]}...")
        try:
            client = tweepy.Client(
                consumer_key=self.twitter_api_key,
                consumer_secret=self.twitter_api_secret,
                access_token=self.twitter_access_token,
                access_token_secret=self.twitter_access_token_secret
            )
            # Twitter es listo, solo necesita el texto unido
            full_text = f"{text}\n\n{url}"
            response = client.create_tweet(text=full_text)
            print(f"✅ Twitter Success! Tweet ID: {response.data['id']}")
        except Exception as e:
            print(f"⚠️ Falló Twitter: {e}")

    def post_to_linkedin(self, text, url):
        """Publica en LinkedIn Empresa como un 'Artículo' para generar la tarjeta visual."""
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
        
        # --- AQUÍ ESTÁ LA MAGIA PARA LA IMAGEN ---
        payload = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    # 1. El texto de introducción va aquí
                    "shareCommentary": {
                        "text": text
                    },
                    # 2. Cambiamos NONE por ARTICLE
                    "shareMediaCategory": "ARTICLE",
                    # 3. Le decimos cuál es la URL original para que saque la imagen
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