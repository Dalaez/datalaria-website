import os
import sys
import frontmatter
from pathlib import Path

# Add the parent directory to sys.path to resolve imports from src
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from src.social_manager import SocialMediaManager
from src import brain

def load_post_content(file_path):
    """Lee el archivo markdown y extrae metadatos calculando la URL correcta por idioma."""
    if not os.path.exists(file_path):
        print(f"❌ El archivo no existe: {file_path}")
        sys.exit(1)
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            
            norm_path = file_path.replace('\\', '/')
            lang = "es" # Default
            if "/es/" in norm_path:
                lang = "es"
            elif "/en/" in norm_path:
                lang = "en"
            
            filename = os.path.basename(file_path)
            if filename.lower() == 'index.md':
                slug = os.path.basename(os.path.dirname(file_path))
            else:
                slug = filename.replace('.md', '')
            
            base_url = "https://datalaria.com"
            if lang:
                url = f"{base_url}/{lang}/posts/{slug}/"
            else:
                url = f"{base_url}/posts/{slug}/"
            
            social_override = post.metadata.get('social_text', None)

            return {
                "title": post.metadata.get('title', 'Sin título'),
                "url": url,
                "content": post.content,
                "social_text": social_override,
                "lang": lang
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
    
    # --- GENERACIÓN DE CONTENIDO ---
    
    twitter_text = ""
    linkedin_text = ""

    # Opción 1: Override Manual (El humano manda)
    if post_data.get('social_text'):
        print("✍️ Texto manual detectado. Usando el mismo para ambas redes.")
        twitter_text = post_data['social_text']
        linkedin_text = post_data['social_text']
        
    # Opción 2: Los Agentes de IA trabajan
    else:
        print(f"🧠 Invocando a los Agentes Creativos ({post_data['lang']})...")
        
        # 1. Llamada al Agente Twitter
        print("   🐦 Agente Twitter escribiendo...")
        twitter_gen = brain.generate_social_copy(
            post_data['title'], post_data['content'], platform='twitter', lang=post_data['lang']
        )
        if twitter_gen:
            twitter_text = twitter_gen
        else:
            twitter_text = f"🚀 Nuevo post: {post_data['title']} #Datalaria"

        # 2. Llamada al Agente LinkedIn
        print("   💼 Agente LinkedIn escribiendo...")
        linkedin_gen = brain.generate_social_copy(
            post_data['title'], post_data['content'], platform='linkedin', lang=post_data['lang']
        )
        if linkedin_gen:
            linkedin_text = linkedin_gen
        else:
            linkedin_text = f"🚀 Nuevo artículo recomendado: {post_data['title']}. #DataEngineering"

    # --- MOSTRAR RESULTADOS Y PUBLICAR ---

    dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
    
    if dry_run:
        print("\n🚧 --- DRY RUN MODE (Preview) --- 🚧")
        print("\n🐦 [TWITTER AGENT OUTPUT]:")
        print(twitter_text)
        print("\n💼 [LINKEDIN AGENT OUTPUT]:")
        print(linkedin_text)
        print(f"\n🔗 URL Adjunta: {post_url}")
        print("---------------------------------------")
        sys.exit(0)

    print("\n🚀 --- LIVE MODE (Posting to Social Media) --- 🚀")
    manager = SocialMediaManager()
    
    # Publicar en Twitter
    try:
        manager.post_to_twitter(text=twitter_text, url=post_url)
    except Exception as e:
        print(f"⚠️ Falló Twitter: {e}")
        
    # Publicar en LinkedIn
    try:
        # manager.post_to_linkedin(text=linkedin_text, url=post_url)
        print(f"⚠️ No publicado en Linkedin por duplicado: {e}")
    except Exception as e:
        print(f"⚠️ Falló LinkedIn: {e}")
    
    print("\n✅ Orquestación finalizada.")

if __name__ == "__main__":
    main()