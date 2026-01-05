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

    def _count_twitter_length(self, text):
        """Cuenta la longitud real del texto para Twitter (emojis cuentan x2)."""
        length = 0
        for char in text:
            # Caracteres fuera del BMP (emojis, etc.) cuentan como 2
            if ord(char) > 0xFFFF:
                length += 2
            else:
                length += 1
        return length

    def _smart_truncate(self, text, url, max_length=250):
        """Trunca el texto de forma inteligente para Twitter (280 chars max)."""
        # 1. Limpieza básica
        text = self._clean_text(text)
        
        # 2. Eliminar "..." existentes al final (pueden venir del generador IA)
        text = text.rstrip('.')
        if text.endswith('…'):
            text = text[:-1]
        
        # 3. Calcular espacio disponible
        # Twitter acorta URLs a 23 caracteres. +1 espacio. +4 para "... "
        url_length = 23
        reserved_chars = url_length + 5  # " ... " + URL
        target_len = max_length - reserved_chars
        
        # 4. Verificar longitud ponderada (emojis = 2)
        twitter_len = self._count_twitter_length(text)
        
        if twitter_len <= target_len:
            return f"{text} {url}"
        
        # 5. Truncar respetando palabras y emojis
        truncated = ""
        current_len = 0
        
        for word in text.split():
            word_len = self._count_twitter_length(word)
            if current_len + word_len + 1 > target_len:  # +1 por espacio
                break
            if truncated:
                truncated += " "
                current_len += 1
            truncated += word
            current_len += word_len
        
        return f"{truncated}... {url}"

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

    def post_to_twitter(self, text, url, image_path=None):
        """Publica en Twitter gestionando la longitud automáticamente.
        
        Args:
            text: Texto del tweet
            url: URL a incluir
            image_path: Ruta opcional a imagen local para subir con el tweet
        """
        if not self.client_v2:
            print("⚠️ Twitter no configurado (Faltan credenciales o error init).")
            return

        full_text = self._smart_truncate(text, url)
        twitter_length = self._count_twitter_length(full_text)
        print(f"DTO - Posting to Twitter ({twitter_length} weighted chars, {len(full_text)} raw): {full_text[:100]}...")
        
        # Subir imagen si existe
        media_ids = None
        if image_path and self.api_v1:
            import os
            if os.path.exists(image_path):
                try:
                    print(f"📸 Subiendo imagen: {image_path}")
                    media = self.api_v1.media_upload(filename=image_path)
                    media_ids = [media.media_id]
                    print(f"   ✅ Imagen subida. Media ID: {media.media_id}")
                except Exception as e:
                    print(f"   ⚠️ Error subiendo imagen: {e}")
            else:
                print(f"⚠️ Imagen no encontrada: {image_path}")
        
        try:
            if media_ids:
                response = self.client_v2.create_tweet(text=full_text, media_ids=media_ids)
            else:
                response = self.client_v2.create_tweet(text=full_text)
            print(f"✅ Twitter Success! Tweet ID: {response.data['id']}")
        
        except tweepy.errors.TweepyException as e:
            # Enhanced Debugging
            print(f"⚠️ Falló Twitter (Tweepy Error): {e}")
            print(f"   🔍 Debug Info: {type(e)}")
            
            if hasattr(e, 'response') and e.response:
                print(f"   🔴 Status Code: {e.response.status_code}")
                try: 
                   error_json = e.response.json()
                   print(f"   🔴 Response JSON: {error_json}")
                   if 'detail' in error_json:
                       print(f"   🔴 Detail: {error_json['detail']}")
                except:
                   print(f"   🔴 Response Text: {e.response.text}")
            
            if hasattr(e, 'api_messages'):
                print(f"   🔴 API Messages: {e.api_messages}")
            
            if "403" in str(e):
                print("   💡 PISTA 403: Forbidden. Puede ser:")
                print("      1. Contenido duplicado (intenta texto diferente).")
                print("      2. Credenciales sin permisos de escritura (regenera tokens).")
                print("      3. Rate limit alcanzado.")
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