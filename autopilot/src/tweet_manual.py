"""
tweet_manual.py - Script para publicar manualmente tweets con imágenes.

Uso:
    python tweet_manual.py "Texto del tweet" "https://url.com" --image "ruta/imagen.png"
    
Ejemplo:
    python tweet_manual.py "¡Nuevo post sobre Netflix! 🎬" "https://datalaria.com/es/posts/netflix/" --image "C:/path/to/netflix.png"

Nota: La imagen se sube directamente a Twitter (no usa Twitter Cards de Open Graph).
"""

import os
import sys
import io
import argparse
import tweepy
from dotenv import load_dotenv

# Forzar UTF-8 en Windows para soportar emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Cargar .env desde el directorio autopilot
load_dotenv()


def get_twitter_clients():
    """Inicializa y retorna el cliente v2 y API v1.1 de Twitter."""
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_secret]):
        print("❌ ERROR: Faltan credenciales de Twitter en el archivo .env")
        print("   Verifica: TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET")
        sys.exit(1)

    try:
        # Cliente v2 para crear tweets
        client_v2 = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        
        # API v1.1 para subir imágenes (media_upload)
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
        api_v1 = tweepy.API(auth)
        
        return client_v2, api_v1
    except Exception as e:
        print(f"❌ ERROR inicializando clientes Twitter: {e}")
        sys.exit(1)


def analyze_text(text, url=None):
    """Analiza el texto para detectar posibles problemas."""
    print("\n📊 ANÁLISIS DEL TEXTO:")
    print(f"   - Longitud texto: {len(text)} caracteres")
    
    # Contar emojis (aproximación: caracteres fuera del BMP o emojis comunes)
    emoji_count = sum(1 for c in text if ord(c) > 0xFFFF)
    print(f"   - Emojis detectados (aprox): ~{emoji_count} (cuentan x2 en Twitter)")
    
    # Longitud efectiva aproximada
    effective_len = len(text) + emoji_count
    print(f"   - Longitud efectiva: ~{effective_len} caracteres")
    
    # URL
    if url:
        print(f"   - URL: {url}")
        print(f"   - URL contará como: 23 caracteres (t.co)")
        total_effective = effective_len + 1 + 23  # espacio + URL
        print(f"   - TOTAL ESTIMADO: ~{total_effective} caracteres")
        
        if total_effective > 280:
            print("   ⚠️ ADVERTENCIA: Puede exceder los 280 caracteres de Twitter!")
    
    # Caracteres especiales problemáticos
    special_chars = ['"', '"', ''', ''', '—', '–']
    found_special = [c for c in special_chars if c in text]
    if found_special:
        print(f"   ⚠️ Caracteres especiales detectados: {found_special}")
    
    return effective_len


def compress_image_for_twitter(image_path, max_size_mb=4.5):
    """Comprime la imagen si excede el límite de Twitter (5MB).
    
    Retorna la ruta a la imagen (original si es pequeña, temporal si fue comprimida).
    """
    try:
        from PIL import Image
    except ImportError:
        print("   ⚠️ Pillow no instalado. Ejecuta: pip install Pillow")
        return image_path
    
    import tempfile
    
    file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
    print(f"   📏 Tamaño original: {file_size_mb:.2f} MB")
    
    if file_size_mb <= max_size_mb:
        return image_path
    
    print(f"   🔄 Comprimiendo imagen (límite Twitter: 5 MB)...")
    
    try:
        with Image.open(image_path) as img:
            # Convertir a RGB si es necesario (para RGBA/P)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Redimensionar si es muy grande
            max_dimension = 2048  # Twitter recomienda máximo 2048px
            if max(img.size) > max_dimension:
                ratio = max_dimension / max(img.size)
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                print(f"   📐 Redimensionada a: {new_size[0]}x{new_size[1]}")
            
            # Guardar como JPEG con compresión
            temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            # Ajustar calidad progresivamente hasta estar bajo el límite
            quality = 85
            while quality >= 20:
                img.save(temp_path, 'JPEG', quality=quality, optimize=True)
                new_size_mb = os.path.getsize(temp_path) / (1024 * 1024)
                
                if new_size_mb <= max_size_mb:
                    print(f"   ✅ Comprimida a: {new_size_mb:.2f} MB (calidad: {quality}%)")
                    return temp_path
                
                quality -= 10
            
            print(f"   ⚠️ No se pudo comprimir lo suficiente: {new_size_mb:.2f} MB")
            return temp_path
            
    except Exception as e:
        print(f"   ❌ Error comprimiendo: {e}")
        return image_path


def upload_image(api_v1, image_path):
    """Sube una imagen a Twitter y retorna el media_id."""
    print(f"\n📸 Subiendo imagen: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"   ❌ ERROR: La imagen no existe en: {image_path}")
        return None
    
    # Comprimir si es necesario
    final_path = compress_image_for_twitter(image_path)
    
    try:
        media = api_v1.media_upload(filename=final_path)
        print(f"   ✅ Imagen subida. Media ID: {media.media_id}")
        
        # Limpiar archivo temporal si fue creado
        if final_path != image_path and os.path.exists(final_path):
            os.remove(final_path)
        
        return media.media_id
    except Exception as e:
        print(f"   ❌ ERROR subiendo imagen: {e}")
        
        # Limpiar archivo temporal si fue creado
        if final_path != image_path and os.path.exists(final_path):
            os.remove(final_path)
        
        return None


def post_tweet(text, url=None, image_path=None, dry_run=False):
    """Publica un tweet con el texto, URL e imagen dados."""
    
    # Construir tweet final
    if url:
        full_text = f"{text} {url}"
    else:
        full_text = text
    
    print("\n🐦 TWEET A PUBLICAR:")
    print("-" * 50)
    print(full_text)
    print("-" * 50)
    print(f"   Longitud final: {len(full_text)} caracteres")
    
    if image_path:
        print(f"   Imagen adjunta: {image_path}")
    
    if dry_run:
        print("\n🚧 DRY RUN - No se publicará el tweet.")
        return
    
    # Confirmar antes de publicar
    confirm = input("\n¿Publicar este tweet? (s/n): ").strip().lower()
    if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Publicación cancelada.")
        return
    
    # Obtener clientes
    client_v2, api_v1 = get_twitter_clients()
    
    # Subir imagen si existe
    media_ids = None
    if image_path:
        media_id = upload_image(api_v1, image_path)
        if media_id:
            media_ids = [media_id]
        else:
            print("   ⚠️ Continuando sin imagen...")
    
    try:
        print("\n📤 Enviando tweet...")
        
        if media_ids:
            response = client_v2.create_tweet(text=full_text, media_ids=media_ids)
        else:
            response = client_v2.create_tweet(text=full_text)
        
        if response.data:
            tweet_id = response.data['id']
            print(f"\n✅ ¡ÉXITO! Tweet publicado.")
            print(f"   Tweet ID: {tweet_id}")
            print(f"   URL: https://twitter.com/datalaria/status/{tweet_id}")
        else:
            print("⚠️ Respuesta extraña: no hay datos pero tampoco error.")
            
    except tweepy.errors.Forbidden as e:
        print(f"\n❌ ERROR 403 FORBIDDEN")
        print(f"   Mensaje: {e}")
        
        if hasattr(e, 'response') and e.response:
            print(f"   Status Code: {e.response.status_code}")
            try:
                error_json = e.response.json()
                print(f"   Response JSON: {error_json}")
                if 'detail' in error_json:
                    print(f"   Detalle: {error_json['detail']}")
                if 'errors' in error_json:
                    for err in error_json['errors']:
                        print(f"   Error: {err.get('message', err)}")
            except:
                print(f"   Response Text: {e.response.text}")
        
        print("\n💡 POSIBLES CAUSAS:")
        print("   1. Contenido duplicado (ya existe un tweet similar reciente)")
        print("   2. Permisos insuficientes (regenera tokens en Developer Portal)")
        print("   3. Rate limit alcanzado")
        print("   4. Contenido bloqueado por políticas de Twitter")
        
    except tweepy.errors.TweepyException as e:
        print(f"\n❌ ERROR TWEEPY: {type(e).__name__}")
        print(f"   {e}")
        
        if hasattr(e, 'response') and e.response:
            print(f"   Status: {e.response.status_code}")
            try:
                print(f"   Body: {e.response.json()}")
            except:
                print(f"   Body: {e.response.text}")


def main():
    parser = argparse.ArgumentParser(
        description='Publicar tweets manualmente con análisis detallado.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python tweet_manual.py "Mi texto aquí" "https://datalaria.com/post/"
  python tweet_manual.py "Solo texto sin URL"
  python tweet_manual.py "Con imagen" "https://url.com" --image "/ruta/imagen.png"
  python tweet_manual.py "Test" "https://url.com" --dry-run
        """
    )
    
    parser.add_argument('text', help='Texto del tweet')
    parser.add_argument('url', nargs='?', help='URL a incluir (opcional)')
    parser.add_argument('--image', '-i', help='Ruta a la imagen a adjuntar')
    parser.add_argument('--dry-run', action='store_true', help='Solo analizar, no publicar')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🐦 DATALARIA - TWEET MANUAL PUBLISHER")
    print("=" * 60)
    
    # Analizar texto
    analyze_text(args.text, args.url)
    
    # Verificar imagen
    if args.image:
        if os.path.exists(args.image):
            print(f"\n✅ Imagen encontrada: {args.image}")
        else:
            print(f"\n⚠️ ADVERTENCIA: Imagen no encontrada: {args.image}")
    
    # Publicar
    post_tweet(args.text, args.url, args.image, args.dry_run)


if __name__ == "__main__":
    main()
