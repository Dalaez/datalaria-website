import os
from google import genai
from google.genai import types

def generate_social_copy(title, content, platform='twitter', lang='es'):
    """
    Genera texto con personalidades totalmente distintas para Twitter y LinkedIn.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ GEMINI_API_KEY no encontrada.")
        return None

    try:
        client = genai.Client(api_key=api_key)
        # Usamos el modelo fiable y gratuito
        model_name = 'gemini-3-flash-preview' 
        
        # Leemos más contexto para que la IA entienda bien el post
        content_snippet = content[:6000]

        # --- PERSONALIDAD 1: EL AGENTE DE TWITTER (Viral, Rápido, Hilos) ---
        if platform == 'twitter':
            if lang == 'en':
                sys_instruction = (
                    "You are a Viral Twitter Creator. Your goal is to get clicks and retweets.\n"
                    "Style: Punchy, controversial or intriguing hooks, short sentences.\n"
                    "Format: Use line breaks for readability. Use 1-2 relevant emojis.\n"
                    "Constraint: NEVER include the URL in the text (it is added automatically).\n"
                    "Length: Under 250 characters.\n"
                    "Tags: Include 2-3 trending hashtags."
                )
            else:
                sys_instruction = (
                    "Eres un Creador Viral en Twitter. Tu objetivo son los clics y retweets.\n"
                    "Estilo: Ganchos impactantes, frases cortas, preguntas directas.\n"
                    "Formato: Usa saltos de línea. Usa 1-2 emojis estratégicos.\n"
                    "Restricción: NUNCA incluyas la URL en el texto (se añade sola).\n"
                    "Longitud: Menos de 250 caracteres.\n"
                    "Tags: Incluye 2-3 hashtags tendencia."
                )

        # --- PERSONALIDAD 2: EL AGENTE DE LINKEDIN (Líder de Opinión, Reflexivo) ---
        elif platform == 'linkedin':
            if lang == 'en':
                sys_instruction = (
                    "You are a Tech Thought Leader on LinkedIn. Your goal is to build authority and engagement.\n"
                    "Style: Professional, storytelling, value-driven. Start with a strong 'hook' about a problem.\n"
                    "Structure:\n"
                    "1. The Hook (Problem or Insight).\n"
                    "2. The Context (Why this matters).\n"
                    "3. The Solution (What the article offers).\n"
                    "4. Call to Action (Invite to read).\n"
                    "Constraint: NEVER include the URL in the text.\n"
                    "Length: 400-800 characters (Micro-blogging style).\n"
                    "Tags: 3-5 professional hashtags at the bottom."
                )
            else:
                sys_instruction = (
                    "Eres un Líder de Opinión Tech en LinkedIn. Tu objetivo es generar autoridad y debate.\n"
                    "Estilo: Profesional, storytelling, aporte de valor. Empieza con un 'gancho' sobre un problema real.\n"
                    "Estructura:\n"
                    "1. El Gancho (Problema o Insight).\n"
                    "2. El Contexto (Por qué importa esto).\n"
                    "3. La Solución (Qué ofrece el artículo).\n"
                    "4. Llamada a la acción (Invita a leer/comentar).\n"
                    "Restricción: NUNCA incluyas la URL en el texto.\n"
                    "Longitud: 400-800 caracteres (Estilo micro-blogging).\n"
                    "Tags: 3-5 hashtags profesionales al final."
                )
        
        # PROMPT DE USUARIO (El contenido a procesar)
        user_prompt = f"Title: {title}\nContent: {content_snippet}"

        # LLAMADA A LA API
        response = client.models.generate_content(
            model=model_name,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction, # Inyectamos la personalidad aquí
                max_output_tokens=800,
                temperature=0.8 # Creatividad alta
            )
        )
        
        return response.text.strip()

    except Exception as e:
        print(f"❌ Error conectando con el Cerebro (Gemini): {e}")
        return None