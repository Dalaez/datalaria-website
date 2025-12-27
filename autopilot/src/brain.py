import os
import google.generativeai as genai

def generate_social_copy(title, content, lang='es'):
    """
    Usa Google Gemini para generar un texto atractivo para redes sociales.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ GEMINI_API_KEY no encontrada. Usando plantilla por defecto.")
        return None

    try:
        # Configurar Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') # Modelo rápido y económico

        # Limitar el contenido para no exceder tokens (primeros 3000 caracteres)
        content_snippet = content[:3000]

        # Prompt Engineering según idioma
        if lang == 'en':
            prompt = (
                f"You are an expert Social Media Manager for a Tech Blog called 'Datalaria'. "
                f"Write a short, engaging LinkedIn/Twitter post to promote this new article.\n"
                f"Title: {title}\n"
                f"Content snippet: {content_snippet}\n\n"
                f"Rules:\n"
                f"- Maximum 240 characters.\n"
                f"- Use an enthusiastic but professional tone.\n"
                f"- Do NOT include the URL (it will be added automatically).\n"
                f"- Include 2-3 relevant hashtags at the end.\n"
                f"- Output ONLY the text of the post."
            )
        else:
            prompt = (
                f"Eres un experto Social Media Manager para el blog técnico 'Datalaria'. "
                f"Escribe un post corto y atractivo para LinkedIn/Twitter promocionando este artículo.\n"
                f"Título: {title}\n"
                f"Fragmento del contenido: {content_snippet}\n\n"
                f"Reglas:\n"
                f"- Máximo 240 caracteres.\n"
                f"- Tono entusiasta pero profesional.\n"
                f"- NO incluyas la URL (el sistema la añade automáticamente).\n"
                f"- Incluye 2-3 hashtags relevantes al final.\n"
                f"- Devuelve SOLO el texto del post."
            )

        # Llamada a la API
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"❌ Error conectando con el Cerebro (Gemini): {e}")
        return None