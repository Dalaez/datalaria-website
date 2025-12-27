import os
import sys
import frontmatter
from pathlib import Path

# Add the parent directory to sys.path to resolve imports from src
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from src.social_manager import SocialMediaManager

def load_post_content(file_path):
    """Lee el archivo markdown y extrae metadatos calculando la URL correcta por idioma."""
    if not os.path.exists(file_path):
        print(f"❌ El archivo no existe: {file_path}")
        sys.exit(1)
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            
            # 1. Normalizar rutas para evitar problemas entre Windows/Linux
            norm_path = file_path.replace('\\', '/')
            
            # 2. Detectar Idioma basado en la carpeta
            lang = "es" # Default
            if "/es/" in norm_path:
                lang = "es"
            elif "/en/" in norm_path:
                lang = "en"
            
            # 3. Detectar Slug (nombre del post)
            filename = os.path.basename(file_path)
            # Si el archivo se llama 'index.md', el slug es el nombre de la carpeta padre
            if filename.lower() == 'index.md':
                slug = os.path.basename(os.path.dirname(file_path))
            else:
                slug = filename.replace('.md', '')
            
            # 4. Construir URL correcta
            # Estructura: https://datalaria.com/{lang}/posts/{slug}/
            base_url = "https://datalaria.com"
            # Asumimos que si es español /es/ explícito o inglés /en/ explícito lo ponemos
            # Si tu web usa /posts/ para default, ajusta aquí. Por seguridad usamos el lang detectado.
            if lang:
                url = f"{base_url}/{lang}/posts/{slug}/"
            else:
                url = f"{base_url}/posts/{slug}/"
            
            # 5. Extraer Override Manual si existe
            social_override = post.metadata.get('social_text', None)

            return {
                "title": post.metadata.get('title', 'Sin título'),
                "url": url,
                "content": post.content,
                "social_text": social_override,
                "lang": lang # <--- DEVOLVEMOS EL IDIOMA DETECTADO
            }
    except Exception as e:
        print(f"❌ Error leyendo el archivo {file_path}: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("❌ Uso: python orchestrator.py <ruta_al_post.md>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    print(f"🔍 Analizando archivo: {file_path}")
    
    post_data = load_post_content(file_path)
    if not post_data:
        sys.exit(1)
        
    print(f"📄 Post cargado: '{post_data['title']}' ({post_data['lang']})")
    
    post_url = post_data['url']
    print(f"🔗 URL Calculada: {post_url}")
    
    # LÓGICA DE GENERACIÓN DE TEXTO
    if post_data.get('social_text'):
        # 1. Prioridad: Texto Manual en Frontmatter
        print("✍️ Texto manual detectado en Frontmatter. Omitiendo generación por IA.")
        social_base_text = post_data['social_text']
    else:
        # 2. Fallback: Generación Automática MULTILINGÜE
        print(f"🌍 Idioma detectado: {post_data['lang']}")
        
        if post_data['lang'] == 'en':
            social_base_text = f"🚀 New article on Datalaria: {post_data['title']}\n\n#DataEngineering #Python #Automation #Tech"
        else:
            social_base_text = f"🚀 Nuevo artículo en Datalaria: {post_data['title']}\n\n#DataEngineering #Python #Automation #Tech"
    
    # Verificar Modo DRY_RUN
    dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
    
    if dry_run:
        print("\n🚧 --- DRY RUN MODE (No posting) --- 🚧")
        print(f"📄 Texto Base: {social_base_text}")
        print(f"🔗 URL Adjunta: {post_url}")
        print("---------------------------------------")
        sys.exit(0)

    # Si NO es Dry Run, ejecutamos los posts reales
    print("\n🚀 --- LIVE MODE (Posting to Social Media) --- 🚀")
    manager = SocialMediaManager()
    
    # 1. Twitter
    try:
        manager.post_to_twitter(text=social_base_text, url=post_url)
    except Exception as e:
        print(f"⚠️ Falló Twitter, pero continuamos: {e}")
        
    # 2. LinkedIn
    try:
        manager.post_to_linkedin(text=social_base_text, url=post_url)
    except Exception as e:
        print(f"⚠️ Falló LinkedIn: {e}")
    
    print("\n✅ Orquestación finalizada.")

if __name__ == "__main__":
    main()