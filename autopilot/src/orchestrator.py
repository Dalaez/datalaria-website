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
    """
    Lee un archivo Markdown, extrae el frontmatter y el contenido.
    Construye la URL basada en el nombre del archivo (slug).
    """
    path = Path(file_path)
    
    if not path.exists():
        print(f"❌ Error: El archivo {file_path} no existe.")
        return None

    try:
        post = frontmatter.load(file_path)
        
        # El slug es el nombre del archivo sin extensión
        slug = path.stem
        # Si el archivo es index.md, el slug debería ser el nombre de la carpeta padre
        if slug == 'index':
            slug = path.parent.name
            
        url = f"https://datalaria.com/posts/{slug}/"
        
        return {
            'title': post.get('title', 'Sin Título'),
            'url': url,
            'content': post.content,
            'metadata': post.metadata
        }
    except Exception as e:
        print(f"❌ Error leyendo el archivo: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("❌ Uso: python orchestrator.py <ruta_al_post.md>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    print(f"🔍 Analizando archivo: {file_path}")
    
    post_data = load_post_content(file_path)
    if not post_data:
        sys.exit(1)
        
    print(f"📄 Post cargado: '{post_data['title']}'")
    print(f"🔗 URL Calculada: {post_data['url']}")
    
    # Simulación del contenido generado por la IA (Por el momento hardcodeado o placeholder)
    # En una implementación real, aquí llamaríamos a la CrewAI con 'post_data['content']'
    social_text = f"Nuevo artículo publicado: {post_data['title']}. Léelo aquí: {post_data['url']} 🚀 #Datalaria #Tech"
    
    # Verificar Modo DRY_RUN
    dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
    
    if dry_run:
        print("\n🚧 --- DRY RUN MODE (No posting) --- 🚧")
        print(f"🐦 [Twitter Mock]: {social_text}")
        print(f"💼 [LinkedIn Mock]: {social_text}")
        print("---------------------------------------")
        sys.exit(0)

    # Si NO es Dry Run, ejecutamos los posts reales
    print("\n🚀 --- LIVE MODE (Posting to Social Media) --- 🚀")
    manager = SocialMediaManager()
    
    # 1. Twitter
    try:
        manager.post_to_twitter(social_text)
    except Exception as e:
        print(f"⚠️ Falló Twitter, pero continuamos: {e}")
        
    # 2. LinkedIn
    try:
        manager.post_to_linkedin(social_text)
    except Exception as e:
        print(f"⚠️ Falló LinkedIn: {e}")
    
    print("\n✅ Orquestación finalizada.")

if __name__ == "__main__":
    main()
