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

    def post_to_devto(self, title, content_markdown, canonical_url, main_image=None):
        """Publica el artículo completo en Dev.to con URL canónica."""
        print(f"DTO - Posting to Dev.to: '{title}'...")
        
        if not self.devto_api_key:
            print("⚠️ BLOQUEADO Dev.to: Faltan credenciales (DEVTO_API_KEY).")
            return

        api_url = "https://dev.to/api/articles"
        
        headers = {
            "api-key": self.devto_api_key,
            "Content-Type": "application/json"
        }

        # Construir payload
        article_data = {
            "title": title,
            "body_markdown": content_markdown,
            "published": True,
            "canonical_url": canonical_url
        }

        # Si hay Organization ID, lo añadimos
        if self.devto_org_id:
            article_data["organization_id"] = int(self.devto_org_id)

        # Si hay imagen de portada (opcional)
        if main_image:
            article_data["main_image"] = main_image

        payload = {"article": article_data}

        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            print(f"✅ Dev.to Success! URL: {response.json().get('url')}")
        except Exception as e:
            print(f"⚠️ Falló Dev.to: {e}")
            if 'response' in locals() and response is not None:
                print(f"   🔴 Dev.to Response: {response.text}")

    def post_to_twitter(self, text, url):
        """Publica en Twitter gestionando la longitud automáticamente."""
        # Usamos la función de truncado inteligente
        full_text = self._smart_truncate(text, url)
        
        print(f"DTO - Posting to Twitter ({len(full_text)} chars): {full_text}...")
        try:
            client = tweepy.Client(
                consumer_key=self.twitter_api_key,
                consumer_secret=self.twitter_api_secret,
                access_token=self.twitter_access_token,
                access_token_secret=self.twitter_access_token_secret
            )
            response = client.create_tweet(text=full_text)
            print(f"✅ Twitter Success! Tweet ID: {response.data['id']}")
        
        except tweepy.errors.TweepyException as e:
            print(f"⚠️ Falló Twitter (Tweepy Error): {e}")
            if hasattr(e, 'response') and e.response:
                print(f"   🔴 Response Status Code: {e.response.status_code}")
                # print(f"   🔴 Response Text: {e.response.text}") # A veces es muy largo o html
            if hasattr(e, 'api_codes') and e.api_codes:
                print(f"   🔴 API Error Codes: {e.api_codes}")
            
            # Common specific hints
            if "403" in str(e):
                print("   💡 PISTA 403: Forbidden. Puede ser:")
                print("      1. Credenciales incorrectas o sin permisos de escritura.")
                print("      2. Contenido duplicado (Twitter prohíbe repostear lo mismo seguido).")
                print("      3. Contenido demasiado largo.")
            if "401" in str(e):
                print("   💡 PISTA 401: Unauthorized. Revisa tus API KEYS y TOKENS.")

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