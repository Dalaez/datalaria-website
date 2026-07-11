"""
linkedin_manual.py - Script para publicar manualmente en LinkedIn con formato.

Uso:
    python linkedin_manual.py "Texto del post" "https://url.com"
    
Ejemplo con saltos de línea:
    python linkedin_manual.py "Primera línea

Segunda línea con espacio

🚀 Tercera línea con emoji" "https://datalaria.com/apps/weather/"

Nota: LinkedIn permite hasta 3,000 caracteres y preserva los saltos de línea.
"""

import os
import sys
import io
import argparse
import requests
from dotenv import load_dotenv

# Forzar UTF-8 en Windows para soportar emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Cargar .env desde el directorio autopilot
load_dotenv()


def get_linkedin_config():
    """Obtiene configuración de LinkedIn desde .env."""
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    company_id = os.getenv("LINKEDIN_COMPANY_ID")
    client_id = os.getenv("LINKEDIN_CLIENT_ID")
    client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
    refresh_token = os.getenv("LINKEDIN_REFRESH_TOKEN")
    
    if not token:
        print("❌ ERROR: Falta LINKEDIN_ACCESS_TOKEN en el archivo .env")
        sys.exit(1)
    
    if not company_id:
        print("❌ ERROR: Falta LINKEDIN_COMPANY_ID en el archivo .env")
        sys.exit(1)
    
    return {
        "token": token,
        "company_id": company_id,
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }


def analyze_text(text, url=None):
    """Analiza el texto para LinkedIn."""
    print("\n📊 ANÁLISIS DEL TEXTO:")
    print(f"   - Longitud texto: {len(text)} caracteres")
    
    # Contar líneas
    line_count = text.count('\n') + 1
    print(f"   - Número de líneas: {line_count}")
    
    # Contar emojis (aproximación)
    emoji_count = sum(1 for c in text if ord(c) > 0xFFFF)
    print(f"   - Emojis detectados: ~{emoji_count}")
    
    # URL
    if url:
        print(f"   - URL: {url}")
        total_len = len(text) + len(url) + 2  # espacio + salto
        print(f"   - TOTAL: {total_len} caracteres")
    else:
        print(f"   - TOTAL: {len(text)} caracteres")
    
    # Límite de LinkedIn
    if len(text) > 3000:
        print("   ⚠️ ADVERTENCIA: Excede los 3,000 caracteres de LinkedIn!")
    elif len(text) > 2500:
        print("   ⚠️ Nota: Texto largo, considera acortarlo para mejor engagement")
    
    return len(text)


def preview_post(text, url=None):
    """Muestra una vista previa del post."""
    print("\n💼 POST DE LINKEDIN A PUBLICAR:")
    print("=" * 60)
    print(text)
    if url:
        print(f"\n🔗 {url}")
    print("=" * 60)


def _update_env_file(key, value):
    """Actualiza una clave en el archivo .env del directorio autopilot."""
    import re
    
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    
    if not os.path.exists(env_path):
        print(f"   ⚠️ No se encontró .env en: {env_path}")
        return
    
    with open(env_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    pattern = rf"^{re.escape(key)}=.*$"
    replacement = f"{key}={value}"
    new_content, count = re.subn(pattern, replacement, content, flags=re.MULTILINE)
    
    if count == 0:
        new_content = content.rstrip() + f"\n{replacement}\n"
    
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(new_content)


def refresh_linkedin_token(config):
    """Renueva el access token de LinkedIn usando el refresh token.
    
    Returns:
        El nuevo token si se renovó, None en caso contrario.
    """
    if not config["refresh_token"]:
        print("   ❌ No hay LINKEDIN_REFRESH_TOKEN en .env.")
        return None
    
    if not config["client_id"] or not config["client_secret"]:
        print("   ❌ Faltan LINKEDIN_CLIENT_ID o LINKEDIN_CLIENT_SECRET en .env.")
        return None
    
    print("   🔄 Renovando token de LinkedIn...")
    
    try:
        response = requests.post(
            "https://www.linkedin.com/oauth/v2/accessToken",
            data={
                "grant_type": "refresh_token",
                "refresh_token": config["refresh_token"],
                "client_id": config["client_id"],
                "client_secret": config["client_secret"],
            }
        )
        response.raise_for_status()
        data = response.json()
        
        new_token = data.get("access_token")
        new_refresh = data.get("refresh_token")
        
        if not new_token:
            print("   ❌ La respuesta no incluyó un nuevo access_token.")
            return None
        
        # Actualizar .env
        _update_env_file("LINKEDIN_ACCESS_TOKEN", new_token)
        if new_refresh:
            _update_env_file("LINKEDIN_REFRESH_TOKEN", new_refresh)
            config["refresh_token"] = new_refresh
        
        config["token"] = new_token
        
        expires_in = data.get("expires_in", "?")
        print(f"   ✅ Token renovado (expira en {expires_in}s).")
        return new_token
        
    except Exception as e:
        print(f"   ❌ Error renovando token: {e}")
        return None


def post_to_linkedin(text, url, dry_run=False):
    """Publica en LinkedIn usando la API. Renueva el token automáticamente si expira."""
    
    preview_post(text, url)
    
    if dry_run:
        print("\n🚧 DRY RUN - No se publicará el post.")
        return
    
    # Confirmar antes de publicar
    confirm = input("\n¿Publicar este post en LinkedIn? (s/n): ").strip().lower()
    if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Publicación cancelada.")
        return
    
    # Obtener configuración
    config = get_linkedin_config()
    
    api_url = "https://api.linkedin.com/v2/ugcPosts"
    author = f"urn:li:organization:{config['company_id']}"
    
    for attempt in range(2):  # Máximo 2 intentos: original + retry tras refresh
        headers = {
            "Authorization": f"Bearer {config['token']}",
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
            print("\n📤 Publicando en LinkedIn...")
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            post_id = response.json().get('id', 'ID no disponible')
            print(f"\n✅ ¡ÉXITO! Post publicado en LinkedIn.")
            print(f"   Post ID: {post_id}")
            print(f"   Revisa tu página de empresa en LinkedIn para verlo.")
            return
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401 and attempt == 0:
                print(f"\n   ⚠️ Token expirado (401). Intentando renovar...")
                if refresh_linkedin_token(config):
                    print(f"   🔁 Reintentando publicación...")
                    continue
                else:
                    print(f"\n❌ No se pudo renovar el token. Genera uno nuevo manualmente.")
                    return
            
            print(f"\n❌ ERROR HTTP: {e}")
            print(f"   Status: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"   Detalle: {error_detail}")
            except:
                print(f"   Response: {response.text}")
            
            if response.status_code == 403:
                print("\n💡 Permisos insuficientes. Verifica los scopes del token.")
            return
                
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            return


def main():
    parser = argparse.ArgumentParser(
        description='Publicar en LinkedIn manualmente con formato.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python linkedin_manual.py "Mi texto aquí" "https://datalaria.com/post/"
  
  # Con saltos de línea (usa triple comillas en PowerShell):
  python linkedin_manual.py "Primera línea
  
  Segunda línea" "https://url.com"
  
  # Solo previsualizar:
  python linkedin_manual.py "Test" "https://url.com" --dry-run
        """
    )
    
    parser.add_argument('text', help='Texto del post (soporta saltos de línea)')
    parser.add_argument('url', help='URL del artículo/app a compartir')
    parser.add_argument('--dry-run', action='store_true', help='Solo analizar, no publicar')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("💼 DATALARIA - LINKEDIN MANUAL PUBLISHER")
    print("=" * 60)
    
    # Analizar texto
    analyze_text(args.text, args.url)
    
    # Publicar
    post_to_linkedin(args.text, args.url, args.dry_run)


if __name__ == "__main__":
    main()
