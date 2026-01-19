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
    
    if not token:
        print("❌ ERROR: Falta LINKEDIN_ACCESS_TOKEN en el archivo .env")
        sys.exit(1)
    
    if not company_id:
        print("❌ ERROR: Falta LINKEDIN_COMPANY_ID en el archivo .env")
        sys.exit(1)
    
    return token, company_id


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


def post_to_linkedin(text, url, dry_run=False):
    """Publica en LinkedIn usando la API."""
    
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
    token, company_id = get_linkedin_config()
    
    api_url = "https://api.linkedin.com/v2/ugcPosts"
    author = f"urn:li:organization:{company_id}"
    
    headers = {
        "Authorization": f"Bearer {token}",
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
        
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ ERROR HTTP: {e}")
        print(f"   Status: {response.status_code}")
        try:
            error_detail = response.json()
            print(f"   Detalle: {error_detail}")
        except:
            print(f"   Response: {response.text}")
        
        if response.status_code == 401:
            print("\n💡 El token de LinkedIn puede haber expirado. Genera uno nuevo en LinkedIn Developer Portal.")
        elif response.status_code == 403:
            print("\n💡 Permisos insuficientes. Verifica los scopes del token.")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


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
