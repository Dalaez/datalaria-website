import os
from google import genai
from google.genai import types

def generate_social_copy(title, content, lang='es'):
    """
    Usa el nuevo SDK de Google GenAI para generar texto.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ GEMINI_API_KEY no encontrada. Usando plantilla por defecto.")
        return None

    try:
        # Configurar Cliente con la nueva librería
        client = genai.Client(api_key=api_key)
        
        # --- AQUÍ ES DONDE ELIGES EL MODELO ---
        # Usa 'gemini-3-flash-preview' (o el nombre exacto que veas en la doc)
        model_name = 'gemini-3-flash-preview'
        # Limitar contenido
        content_snippet = content[:3000]

        # Prompt Engineering
        if lang == 'en':
            prompt_text = (
                f"You are an expert Social Media Manager for a Tech Blog called 'Datalaria'. "
                f"Write a short, engaging LinkedIn/Twitter post to promote this new article.\n"
                f"Title: {title}\n"
                f"Content snippet: {content_snippet}\n\n"
                f"Rules:\n"
                f"- Maximum 240 characters.\n"
                f"- Use an enthusiastic but professional tone.\n"
                f"- Do NOT include the URL.\n"
                f"- Include 2-3 relevant hashtags.\n"
                f"- Output ONLY the text of the post."
            )
        else:
            prompt_text = (
                f"Eres un experto Social Media Manager para el blog técnico 'Datalaria'. "
                f"Escribe un post corto y atractivo para LinkedIn/Twitter promocionando este artículo.\n"
                f"Título: {title}\n"
                f"Fragmento del contenido: {content_snippet}\n\n"
                f"Reglas:\n"
                f"- Máximo 240 caracteres.\n"
                f"- Tono entusiasta pero profesional.\n"
                f"- NO incluyas la URL.\n"
                f"- Incluye 2-3 hashtags relevantes.\n"
                f"- Devuelve SOLO el texto del post."
            )

        # Llamada a la API con la nueva sintaxis v2
        response = client.models.generate_content(
            model=model_name,
            contents=prompt_text,
            config=types.GenerateContentConfig(
                max_output_tokens=300,
                temperature=0.7
            )
        )
        
        return response.text.strip()

    except Exception as e:
        print(f"❌ Error conectando con el Cerebro (Gemini): {e}")
        return None