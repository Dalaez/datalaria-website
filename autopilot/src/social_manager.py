"""SocialMediaManager - Gestor omnicanal con política X/Twitter Coste 0 EUR."""

from __future__ import annotations

import json
import os
import re
import tempfile
from typing import Any, Dict, List, Optional, Union, Union

import requests
import tweepy
from dotenv import load_dotenv

from autopilot.src.models import (
    SocialPlatformX,
    build_x_web_intent_url,
    count_twitter_weighted_length,
)


class SocialMediaManager:
    """Gestiona publicación en X (Web Intent 0 EUR por defecto), LinkedIn y Dev.to."""

    def __init__(self) -> None:
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        load_dotenv(env_path)

        self.twitter_api_enabled = os.getenv("ENABLE_TWITTER_API", "false").lower() == "true"
        self.twitter_api_key = os.getenv("TWITTER_API_KEY")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET")
        self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

        self.linkedin_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.linkedin_client_id = os.getenv("LINKEDIN_CLIENT_ID")
        self.linkedin_client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
        self.linkedin_refresh_token = os.getenv("LINKEDIN_REFRESH_TOKEN")
        self.company_id = os.getenv("LINKEDIN_COMPANY_ID")

        self.devto_api_key = os.getenv("DEVTO_API_KEY")
        self.devto_org_id = os.getenv("DEVTO_ORG_ID")

        self.coderlegion_api_key = os.getenv("CODERLEGION_API_KEY")
        self.coderlegion_api_url = os.getenv(
            "CODERLEGION_API_URL", "https://coderlegion.com/api/v1/posts"
        )
        self.coderlegion_category_id = os.getenv("CODERLEGION_CATEGORY_ID")

        self.client_v2 = None
        self.api_v1 = None

        if self.twitter_api_enabled and self.twitter_api_key:
            try:
                self.client_v2 = tweepy.Client(
                    consumer_key=self.twitter_api_key,
                    consumer_secret=self.twitter_api_secret,
                    access_token=self.twitter_access_token,
                    access_token_secret=self.twitter_access_token_secret,
                )
                auth = tweepy.OAuth1UserHandler(
                    self.twitter_api_key,
                    self.twitter_api_secret,
                    self.twitter_access_token,
                    self.twitter_access_token_secret,
                )
                self.api_v1 = tweepy.API(auth)
            except Exception as exc:
                print(f"⚠️ Error inicializando Twitter clients: {exc}")

    def _clean_text(self, text: str) -> str:
        return " ".join((text or "").split())

    def _count_twitter_length(self, text: str) -> int:
        """Delega en el cálculo ponderado oficial compartido en autopilot.src.models."""
        return count_twitter_weighted_length(text)

    def _smart_truncate(self, text: str, url: str, max_length: int = 250) -> str:
        """Trunca el texto respetando longitud ponderada para incluir URL (23 chars t.co)."""
        cleaned = self._clean_text(text).rstrip(".…")
        target_len = max_length - (23 + 5)

        if self._count_twitter_length(cleaned) <= target_len:
            return f"{cleaned} {url}".strip()

        truncated = ""
        current_len = 0
        for word in cleaned.split():
            word_len = self._count_twitter_length(word)
            if current_len + word_len + 1 > target_len:
                break
            if truncated:
                truncated += " "
                current_len += 1
            truncated += word
            current_len += word_len
        return f"{truncated}... {url}".strip()

    def _compress_image(self, image_path: str, max_size_mb: float = 4.5) -> str:
        """Comprime la imagen si excede el límite de Twitter (5 MB)."""
        try:
            from PIL import Image
        except ImportError:
            print("   ⚠️ Pillow no instalado. Ejecuta: pip install Pillow")
            return image_path

        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
        print(f"   📏 Tamaño original: {file_size_mb:.2f} MB")
        if file_size_mb <= max_size_mb:
            return image_path

        print("   🔄 Comprimiendo imagen (límite Twitter: 5 MB)...")
        try:
            with Image.open(image_path) as img:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                max_dimension = 2048
                if max(img.size) > max_dimension:
                    ratio = max_dimension / max(img.size)
                    new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)

                temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                temp_path = temp_file.name
                temp_file.close()

                quality = 85
                while quality >= 20:
                    img.save(temp_path, "JPEG", quality=quality, optimize=True)
                    if os.path.getsize(temp_path) / (1024 * 1024) <= max_size_mb:
                        return temp_path
                    quality -= 10
                return temp_path
        except Exception as exc:
            print(f"   ❌ Error comprimiendo: {exc}")
            return image_path

    def prepare_x_zero_cost(
        self,
        x_pack_or_text: Union[SocialPlatformX, str],
        post_url: str,
        hashtags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Genera e imprime paquete X/Twitter a coste 0 EUR/mes (Web Intent + hilo copiable)."""
        if isinstance(x_pack_or_text, SocialPlatformX):
            hook = x_pack_or_text.hook
            thread = list(x_pack_or_text.thread)
            tags = list(x_pack_or_text.hashtags or hashtags or [])
            intent_url = x_pack_or_text.web_intent_url or build_x_web_intent_url(hook, post_url, tags)
        else:
            hook = self._clean_text(str(x_pack_or_text))
            tags = list(hashtags or [])
            intent_url = build_x_web_intent_url(hook, post_url, tags)
            thread = [f"1/1 {hook} {post_url}".strip()]

        print("\n🐦 [X / TWITTER - MODO COSTE 0 EUR/MES]")
        print(f"   👉 1-Clic X Web Intent: {intent_url}")
        print("   🧵 Hilo listo para copiar:")
        for idx, tweet in enumerate(thread, start=1):
            print(f"      [{idx}/{len(thread)}] ({count_twitter_weighted_length(tweet)}/280) {tweet}")

        return {
            "mode": "zero_cost_intent",
            "hook": hook,
            "hashtags": tags,
            "web_intent_url": intent_url,
            "thread": thread,
        }

    def post_to_devto(
        self,
        title: str,
        content_markdown: str,
        canonical_url: str,
        main_image: Optional[str] = None,
        tags: Optional[List[str]] = None,
        description: Optional[str] = None,
        published: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """Publica el artículo completo en Dev.to con URL canónica y metadatos enriquecidos."""
        print(f"DTO - Posting to Dev.to: '{title}'...")
        if not self.devto_api_key:
            print("⚠️ BLOQUEADO Dev.to: Faltan credenciales (DEVTO_API_KEY).")
            return None

        api_url = "https://dev.to/api/articles"
        headers = {
            "api-key": self.devto_api_key,
            "Content-Type": "application/json",
        }
        article_data: Dict[str, Any] = {
            "title": title,
            "body_markdown": content_markdown,
            "published": published,
            "canonical_url": canonical_url,
        }
        if self.devto_org_id:
            article_data["organization_id"] = int(self.devto_org_id)
        if main_image:
            article_data["main_image"] = main_image
        if tags:
            article_data["tags"] = list(tags)
        if description:
            article_data["description"] = description

        try:
            response = requests.post(
                api_url,
                headers=headers,
                json={"article": article_data},
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
            print(f"✅ Dev.to Success! URL: {payload.get('url') if isinstance(payload, dict) else ''}")
            return payload if isinstance(payload, dict) else {}
        except requests.exceptions.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else "?"
            preview = (exc.response.text or "")[:250] if exc.response is not None else ""
            print(f"⚠️ Falló Dev.to (HTTP {status_code}): {preview}")
            return None
        except Exception as exc:
            print(f"⚠️ Falló Dev.to: {exc}")
            return None

    def post_to_coderlegion(
        self,
        title: str,
        content_markdown: str,
        canonical_url: str,
        cover_image_url: Optional[str] = None,
        tags: Optional[List[str]] = None,
        description: Optional[str] = None,
        category_id: Optional[Union[str, int]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Publica el artículo en CoderLegion (/api/v1/posts) usando X-API-Key y source_url."""
        print(f"CLG - Posting to CoderLegion: '{title}'...")
        if not self.coderlegion_api_key:
            print("⚠️ BLOQUEADO CoderLegion: Faltan credenciales (CODERLEGION_API_KEY).")
            return None

        clean_source = (canonical_url or "").strip()
        if not clean_source.startswith("https://"):
            print("⛔ BLOQUEADO CoderLegion: source_url canónica HTTPS obligatoria (INV-AUTO-8).")
            return None

        headers = {
            "X-API-Key": self.coderlegion_api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload: Dict[str, Any] = {
            "title": title,
            "content": content_markdown,
            "source_url": clean_source,
            "tags": list(tags or []),
        }
        if cover_image_url:
            payload["cover_image_url"] = cover_image_url
        if description:
            payload["description"] = description

        raw_category = category_id if category_id is not None else self.coderlegion_category_id
        if raw_category is not None and str(raw_category).strip():
            cat_str = str(raw_category).strip()
            payload["category_id"] = int(cat_str) if cat_str.isdigit() else cat_str

        try:
            response = requests.post(
                self.coderlegion_api_url,
                headers=headers,
                json=payload,
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
            post_id = data.get("id") if isinstance(data, dict) else ""
            print(f"✅ CoderLegion Success! Post ID: {post_id}")
            return data if isinstance(data, dict) else {}
        except requests.exceptions.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else "?"
            preview = (exc.response.text or "")[:250] if exc.response is not None else ""
            print(f"⚠️ Falló CoderLegion (HTTP {status_code}): {preview}")
            return None
        except Exception as exc:
            print(f"⚠️ Falló CoderLegion: {exc}")
            return None

    def post_to_twitter(
        self,
        text: str,
        url: str,
        image_path: Optional[str] = None,
        x_pack: Optional[SocialPlatformX] = None,
    ) -> Dict[str, Any]:
        """Publica en X vía Web Intent coste 0 EUR por defecto (solo usa Tweepy si ENABLE_TWITTER_API=true)."""
        if not self.twitter_api_enabled:
            return self.prepare_x_zero_cost(x_pack or text, post_url=url)

        if not self.client_v2:
            print("⚠️ ENABLE_TWITTER_API=true pero faltan credenciales; emitiendo X Web Intent 0 EUR.")
            return self.prepare_x_zero_cost(x_pack or text, post_url=url)

        full_text = self._smart_truncate(text, url)
        twitter_length = self._count_twitter_length(full_text)
        print(f"DTO - Posting to Twitter ({twitter_length} weighted chars): {full_text[:100]}...")

        media_ids = None
        if image_path and self.api_v1 and os.path.exists(image_path):
            try:
                final_path = self._compress_image(image_path)
                media = self.api_v1.media_upload(filename=final_path)
                media_ids = [media.media_id]
                if final_path != image_path and os.path.exists(final_path):
                    os.remove(final_path)
            except Exception as exc:
                print(f"   ⚠️ Error subiendo imagen: {exc}")

        try:
            if media_ids:
                response = self.client_v2.create_tweet(text=full_text, media_ids=media_ids)
            else:
                response = self.client_v2.create_tweet(text=full_text)
            print(f"✅ Twitter Success! Tweet ID: {response.data['id']}")
            return {"mode": "twitter_api_v2", "tweet_id": response.data.get("id")}
        except tweepy.errors.TweepyException as exc:
            print(f"⚠️ Falló Twitter API ({exc}); fallback a X Web Intent coste 0 EUR:")
            return self.prepare_x_zero_cost(x_pack or text, post_url=url)

    def _refresh_linkedin_token(self) -> bool:
        """Renueva el access token de LinkedIn usando el refresh token."""
        if not self.linkedin_refresh_token:
            print("   ❌ No hay LINKEDIN_REFRESH_TOKEN.")
            return False
        if not self.linkedin_client_id or not self.linkedin_client_secret:
            print("   ❌ Faltan LINKEDIN_CLIENT_ID o LINKEDIN_CLIENT_SECRET.")
            return False

        print("   🔄 Renovando token de LinkedIn...")
        try:
            response = requests.post(
                "https://www.linkedin.com/oauth/v2/accessToken",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.linkedin_refresh_token,
                    "client_id": self.linkedin_client_id,
                    "client_secret": self.linkedin_client_secret,
                },
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
            new_token = data.get("access_token")
            new_refresh = data.get("refresh_token")
            if not new_token:
                print("   ❌ La respuesta de LinkedIn no incluyó un nuevo access_token.")
                return False

            self.linkedin_token = new_token
            if new_refresh:
                self.linkedin_refresh_token = new_refresh

            self._update_env_file("LINKEDIN_ACCESS_TOKEN", new_token)
            if new_refresh:
                self._update_env_file("LINKEDIN_REFRESH_TOKEN", new_refresh)
            self._save_refreshed_tokens(new_token, new_refresh)
            print(f"   ✅ Token renovado (expira en {data.get('expires_in', '?')}s).")
            return True
        except Exception as exc:
            print(f"   ❌ Error renovando token: {exc}")
            return False

    def _update_env_file(self, key: str, value: str) -> None:
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        if not os.path.exists(env_path):
            return

        with open(env_path, "r", encoding="utf-8") as fh:
            content = fh.read()

        pattern = rf"^{re.escape(key)}=.*$"
        replacement = f"{key}={value}"
        new_content, count = re.subn(pattern, replacement, content, flags=re.MULTILINE)
        if count == 0:
            new_content = content.rstrip() + f"\n{replacement}\n"

        with open(env_path, "w", encoding="utf-8") as fh:
            fh.write(new_content)

    def _save_refreshed_tokens(self, access_token: str, refresh_token: Optional[str] = None) -> None:
        token_data: Dict[str, str] = {"access_token": access_token}
        if refresh_token:
            token_data["refresh_token"] = refresh_token
        tokens_file = os.path.join(os.getcwd(), ".linkedin_new_tokens.json")
        try:
            with open(tokens_file, "w", encoding="utf-8") as fh:
                json.dump(token_data, fh)
            print("   📝 Nuevos tokens guardados para persistir en CI.")
        except Exception as exc:
            print(f"   ⚠️ No se pudieron guardar tokens para CI: {exc}")

    def post_to_linkedin(self, text: str, url: str) -> None:
        """Publica en LinkedIn preservando saltos de línea Broetry y renovando token en 401."""
        cleaned_text = (text or "").strip()
        print(f"DTO - Posting to LinkedIn: {cleaned_text[:50]}...")

        if not self.company_id:
            print("⚠️ BLOQUEADO LinkedIn: No se encontró LINKEDIN_COMPANY_ID.")
            return

        api_url = "https://api.linkedin.com/v2/ugcPosts"
        author = f"urn:li:organization:{self.company_id}"

        for attempt in range(2):
            headers = {
                "Authorization": f"Bearer {self.linkedin_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
            }
            payload = {
                "author": author,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": cleaned_text},
                        "shareMediaCategory": "ARTICLE",
                        "media": [{"status": "READY", "originalUrl": url}],
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
            }
            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=15)
                response.raise_for_status()
                print(f"✅ LinkedIn Success! Post ID: {response.json().get('id')}")
                return
            except requests.exceptions.HTTPError as exc:
                if response.status_code == 401 and attempt == 0:
                    print("   ⚠️ Token expirado (401). Intentando renovar...")
                    if self._refresh_linkedin_token():
                        continue
                    print("⚠️ Falló LinkedIn: No se pudo renovar el token.")
                    return
                print(f"⚠️ Falló LinkedIn: {exc}")
                return
            except Exception as exc:
                print(f"⚠️ Falló LinkedIn: {exc}")
                return


if __name__ == "__main__":
    pass
