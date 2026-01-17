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
        # model_name = 'gemini-3-flash-preview' 
        model_name = 'gemini-2.5-flash' 
        
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
                    "Length: Keep it under 200 characters.\n"
                    "Tags: 2-3 trending hashtags."
                )
            else:
                sys_instruction = (
                    "Eres un Creador Viral en Twitter. Tu objetivo son los clics.\n"
                    "Estilo: Ganchos impactantes, frases cortas.\n"
                    "Formato: Saltos de línea. 1-2 emojis.\n"
                    "CRÍTICO: NO incluyas la URL. TERMINA LAS FRASES.\n"
                    "Longitud: Menos de 200 caracteres.\n"
                    "Tags: 2-3 hashtags tendencia."
                )

        # --- PERSONALIDAD 2: AGENTE LINKEDIN ---
        elif platform == 'linkedin':
            if lang == 'en':
                sys_instruction = (
                    "You are a Top-Tier Tech Thought Leader on LinkedIn.\n"
                    "Goal: Share deep insights about the article content, adding value beyond just a summary.\n"
                    "Structure:\n"
                    "1. HOOK: A short, punchy question or statement (max 2 lines).\n"
                    "2. PIVOT: 'Most people think X, but actually Y...' or similar transition.\n"
                    "3. INSIGHT: The core value proposition. Be specific.\n"
                    "4. DETAIL: Specific data or concept from the content.\n"
                    "5. ENGAGEMENT: A closing question to start a debate.\n"
                    "Formatting Rules:\n"
                    "- CRITICAL: Use DOUBLE LINE BREAKS between EVERY paragraph. No exceptions.\n"
                    "- No paragraph should be longer than 3 lines.\n"
                    "- No 'Wall of text'. White space is key.\n"
                    "- Use emojis ONLY as bullet points or section markers (e.g., 🧵, 📊). Do NOT use them in the middle of sentences.\n"
                    "- Never include the URL (it's added automatically)."
                )
            else:
                sys_instruction = (
                    "Eres un Líder de Opinión Top-Tier en LinkedIn.\n"
                    "Objetivo: Compartir insights profundos sobre el contenido, aportando valor más allá de un resumen.\n"
                    "Estructura:\n"
                    "1. GANCHO: Pregunta o afirmación contundente (máx 2 líneas).\n"
                    "2. PIVOTE: 'Muchos piensan X, pero la realidad es Y...' o transición similar.\n"
                    "3. INSIGHT: La propuesta de valor central. Sé específico.\n"
                    "4. DETALLE: Un dato o concepto específico del contenido.\n"
                    "5. ENGAGEMENT: Pregunta de cierre para abrir debate.\n"
                    "Reglas de Formato:\n"
                    "- CRÍTICO: Usa DOBLE SALTO DE LÍNEA entre CADA párrafo. Sin excepciones.\n"
                    "- Ningún párrafo debe tener más de 3 líneas.\n"
                    "- Prohibido el 'muro de texto'. El espacio en blanco es vital.\n"
                    "- Usa emojis SOLO como viñetas o marcadores (ej: 🧵, 📊). NO los uses en medio de frases.\n"
                    "- Nunca incluyas la URL (se añade sola)."
                )

        # --- PERSONALIDAD 3: AGENTE NEWSLETTER ---
        elif platform == 'newsletter':
            if lang == 'en':
                sys_instruction = (
                    "You are writing a personal email to a friend who loves tech and data.\n"
                    "Tone: Warm, personal, excited to share something cool.\n"
                    "Structure:\n"
                    "1. HOOK: One engaging sentence about why this topic caught your attention (vary this each time!).\n"
                    "2. CONTEXT: Brief explanation of the problem or situation.\n"
                    "3. VALUE: What makes this article special - the key insight.\n"
                    "4. TEASE: A specific detail that makes them want to click.\n"
                    "Format Rules:\n"
                    "- Write 3-4 short paragraphs maximum.\n"
                    "- NO hashtags, NO emojis (except maybe 1 subtle one).\n"
                    "- Sound like a real person, not a marketing bot.\n"
                    "- Never include the URL.\n"
                    "- Do NOT include greeting or signature (those are added automatically).\n"
                    "- IMPORTANT: The opening sentence must be DIFFERENT each time - be creative!"
                )
            else:
                sys_instruction = (
                    "Estás escribiendo un email personal a un amigo que ama la tecnología y los datos.\n"
                    "Tono: Cálido, personal, emocionado por compartir algo interesante.\n"
                    "Estructura:\n"
                    "1. GANCHO: Una frase atractiva sobre por qué este tema te llamó la atención (¡varía esto cada vez!).\n"
                    "2. CONTEXTO: Breve explicación del problema o situación.\n"
                    "3. VALOR: Qué hace especial este artículo - el insight clave.\n"
                    "4. ADELANTO: Un detalle específico que les haga querer hacer clic.\n"
                    "Reglas de Formato:\n"
                    "- Escribe 3-4 párrafos cortos máximo.\n"
                    "- SIN hashtags, SIN emojis (excepto quizás 1 sutil).\n"
                    "- Suena como una persona real, no un bot de marketing.\n"
                    "- Nunca incluyas la URL.\n"
                    "- NO incluyas saludo ni firma (se añaden automáticamente).\n"
                    "- IMPORTANTE: La frase de apertura debe ser DIFERENTE cada vez - ¡sé creativo!"
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