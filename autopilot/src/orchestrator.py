import os
import sys
import frontmatter
from pathlib import Path
import re

# Add the parent directory to sys.path to resolve imports from src
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from src.social_manager import SocialMediaManager
from src import brain

def str_to_bool(value):
    """Convierte strings de entorno 'true', 'false', '1', '0' a booleano."""
    return str(value).lower() in ("yes", "true", "t", "1")

def resolve_image_urls(content, file_path):
    """
    Reemplaza rutas relativas de imágenes por URLs absolutas de GitHub Raw.
    Dev.to no puede leer imágenes locales (./img.png), necesita una URL pública.
    
    Ejemplo transf: 
    ![Alt](image.png) -> ![Alt](https://raw.githubusercontent.com/Dalaez/datalaria-website/main/content/es/posts/mi-post/image.png)
    """
    # 1. Base URL de Raw GitHub
    # ATENCIÓN: Asumimos que la estructura en GitHub es idéntica a la local.
    github_base = "https://raw.githubusercontent.com/Dalaez/datalaria-website/main"
    
    # 2. Calcular la ruta relativa del directorio del post
    # file_path = content/es/posts/X/index.md -> dir_path = content/es/posts/X
    # Debemos normalizar separadores a /
    normalized_path = file_path.replace('\\', '/')
    dir_path = os.path.dirname(normalized_path)
    
    def replacer(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        
        # Si ya es http, no tocamos
        if img_path.startswith("http"):
            return match.group(0)
            
        # Si es ruta relativa (empieza por ./ o nombre directo)
        clean_img_path = img_path.lstrip("./")
        
        # Construimos la URL absoluta
        # github_base + / + dir_path + / + clean_img_path
        abs_url = f"{github_base}/{dir_path}/{clean_img_path}"
        
        return f"![{alt_text}]({abs_url})"
        
    # Regex para capturar ![Alt](path)
    # Group 1: Alt, Group 2: Path
    pattern = r'!\[(.*?)\]\((.*?)\)'
    
    new_content = re.sub(pattern, replacer, content)
    return new_content

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

    # --- LEER INTERRUPTORES DE ENTORNO (Por defecto TRUE) ---
    enable_twitter = str_to_bool(os.getenv("ENABLE_TWITTER", "true"))
    enable_linkedin = str_to_bool(os.getenv("ENABLE_LINKEDIN", "true"))
    enable_devto = str_to_bool(os.getenv("ENABLE_DEVTO", "false")) # Default false for safety
    
    # --- GENERACIÓN DE CONTENIDO ---
    
    twitter_text = ""
    linkedin_text = ""

    # Opción 1: Override Manual
    if post_data.get('social_text'):
        print("✍️ Texto manual detectado.")
        twitter_text = post_data['social_text']
        linkedin_text = post_data['social_text']
        
    # Opción 2: IA
    else:
        print(f"🧠 Invocando a los Agentes Creativos ({post_data['lang']})...")
        
        # 1. Agente Twitter (Solo si está activado)
        if enable_twitter:
            print("   🐦 Agente Twitter escribiendo...")
            twitter_gen = brain.generate_social_copy(
                post_data['title'], post_data['content'], platform='twitter', lang=post_data['lang']
            )
            twitter_text = twitter_gen if twitter_gen else f"🚀 Nuevo post: {post_data['title']} #Datalaria"
        else:
            print("   🚫 Agente Twitter DESACTIVADO por configuración.")

        # 2. Agente LinkedIn (Solo si está activado)
        if enable_linkedin:
            print("   💼 Agente LinkedIn escribiendo...")
            linkedin_gen = brain.generate_social_copy(
                post_data['title'], post_data['content'], platform='linkedin', lang=post_data['lang']
            )
            linkedin_text = linkedin_gen if linkedin_gen else f"🚀 Nuevo artículo recomendado: {post_data['title']}. #DataEngineering"
        else:
            print("   🚫 Agente LinkedIn DESACTIVADO por configuración.")

    # --- RESOLUCIÓN DE IMAGEN LOCAL ---
    # Buscamos la imagen para subirla nativamente a Twitter (y opcionalmente a Dev.to si no usara URL)
    local_image_path = None
    
    # 1. Mirar si hay 'cover' (PaperMod)
    # Puede ser un dict {image: "..."} o directamente un string si el usuario se equivocó
    cover_meta = post_data.get('cover', {})
    image_filename = None
    
    if isinstance(cover_meta, dict):
        image_filename = cover_meta.get('image')
    elif isinstance(cover_meta, str):
        # Fallback por si alguien pone cover: "imagen.png"
        image_filename = cover_meta
        
    # 2. Si no, mirar 'image' (compatible)
    if not image_filename:
        image_filename = post_data.get('image')
        
    if image_filename:
        # Asumimos que la imagen está AL LADO del markdown (Page Bundle)
        # o en static/images si empieza por /
        
        if image_filename.startswith("/"):
            # Ruta absoluta desde la raíz del sitio (habitual en /static)
            # Datalaria root = parent_dir (autopilot) -> parent (datalaria)??
            # parent_dir = datalaria/autopilot/.. = datalaria/
            # Pero orchestrator está en src.
            # current_dir = src
            # parent_dir = autopilot
            # root_dir = autopilot/.. = datalaria
            root_dir = parent_dir.parent
            local_image_path = os.path.join(root_dir, "static", image_filename.lstrip("/"))
        else:
            # Ruta relativa al post (Page Bundle)
            post_dir = os.path.dirname(os.path.abspath(file_path))
            local_image_path = os.path.join(post_dir, image_filename)
            
        if not os.path.exists(local_image_path):
            print(f"⚠️ Imagen referenciada no encontrada en disco: {local_image_path}")
            local_image_path = None
        else:
            print(f"📸 Imagen local detectada: {local_image_path}")

    # --- PUBLICACIÓN ---

    dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
    
    if dry_run:
        print("\n🚧 --- DRY RUN MODE (Preview) --- 🚧")
        if enable_twitter:
            print(f"\n🐦 [TWITTER]:\n{twitter_text}")
            if local_image_path:
                print(f"   [Image]: {local_image_path}")
        if enable_linkedin:
            print(f"\n💼 [LINKEDIN]:\n{linkedin_text}")
        if enable_devto:
            print(f"\n🦄 [DEV.TO]:\n(Original Markdown Content will be published)")
            # Preview de URLs
            preview_content = resolve_image_urls(post_data['content'][:500], file_path)
            print(f"   Sample Processing: {preview_content}...")
        
        print(f"\n🔗 URL: {post_url}")
        sys.exit(0)

    print("\n🚀 --- LIVE MODE (Posting to Social Media) --- 🚀")
    manager = SocialMediaManager()
    
    # 1. Publicar en Twitter
    if enable_twitter:
        try:
            # Pasamos local_image_path si existe
            manager.post_to_twitter(text=twitter_text, url=post_url, image_path=local_image_path)
        except Exception as e:
            print(f"⚠️ Falló Twitter: {e}")
    else:
        print("🔕 Twitter omitido (ENABLE_TWITTER=false)")
        
    # 2. Publicar en LinkedIn    
    if enable_linkedin:
        try:
            manager.post_to_linkedin(text=linkedin_text, url=post_url)
        except Exception as e:
            print(f"⚠️ Falló LinkedIn: {e}")
    else:
        print("🔕 LinkedIn omitido (ENABLE_LINKEDIN=false)")

    # 3. Publicar en Dev.to
    if enable_devto:
        try:
            # Procesar imágenes para que sean URLs absolutas
            print("🦄 Procesando imágenes para Dev.to...")
            processed_content = resolve_image_urls(post_data['content'], file_path)
            
            manager.post_to_devto(
                title=post_data['title'], 
                content_markdown=processed_content, 
                canonical_url=post_url
            )
        except Exception as e:
            print(f"⚠️ Falló Dev.to: {e}")
    else:
        print("🔕 Dev.to omitido (ENABLE_DEVTO=false)")
    
    print("\n✅ Orquestación finalizada.")

if __name__ == "__main__":
    main()