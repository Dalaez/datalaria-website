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
        # Usamos un modelo estable para evitar warnings de 'thoughts'
        model_name = 'gemini-3-flash-preview' 
        
        # Leemos más contexto
        content_snippet = content[:6000]

        # --- PERSONALIDAD 1: AGENTE TWITTER ---
        if platform == 'twitter':
            if lang == 'en':
                sys_instruction = (
                    "You are a Viral Twitter Creator. Your goal is to get clicks and retweets.\n"
                    "Style: Punchy, controversial or intriguing hooks.\n"
                    "Format: Short lines. Use 1-2 emojis.\n"
                    "CRITICAL: Never include the URL. FINISH YOUR SENTENCES.\n"
                    "Length: Keep it under 280 characters.\n"
                    "Tags: 2-3 trending hashtags."
                )
            else:
                sys_instruction = (
                    "Eres un Creador Viral en Twitter. Tu objetivo son los clics.\n"
                    "Estilo: Ganchos impactantes, frases cortas.\n"
                    "Formato: Saltos de línea. 1-2 emojis.\n"
                    "CRÍTICO: NO incluyas la URL. TERMINA LAS FRASES.\n"
                    "Longitud: Menos de 280 caracteres.\n"
                    "Tags: 2-3 hashtags tendencia."
                )

        # --- PERSONALIDAD 2: AGENTE LINKEDIN ---
        elif platform == 'linkedin':
            if lang == 'en':
                sys_instruction = (
                    "You are a Tech Thought Leader on LinkedIn.\n"
                    "Style: Professional storytelling. Start with a hook.\n"
                    "Structure: Hook -> Insight -> Value -> Call to Action.\n"
                    "CRITICAL: Never include the URL. Ensure the post is complete.\n"
                    "Length: 400-900 characters.\n"
                    "Tags: 3-5 professional hashtags."
                )
            else:
                sys_instruction = (
                    "Eres un Líder de Opinión Tech en LinkedIn.\n"
                    "Estilo: Storytelling profesional. Empieza con un gancho.\n"
                    "Estructura: Gancho -> Insight -> Valor -> Llamada a la acción.\n"
                    "CRÍTICO: NO incluyas la URL. Asegúrate de que el texto está completo y cerrado.\n"
                    "Longitud: 400-900 caracteres.\n"
                    "Tags: 3-5 hashtags profesionales."
                )
        
        user_prompt = f"Title: {title}\nContent: {content_snippet}"

        # LLAMADA A LA API
        response = client.models.generate_content(
            model=model_name,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                max_output_tokens=2000,  # 🔥 SUBIMOS A 2000 PARA EVITAR CORTES
                temperature=0.8
            )
        )
        
        return response.text.strip()

    except Exception as e:
        print(f"❌ Error conectando con el Cerebro (Gemini): {e}")
        return None