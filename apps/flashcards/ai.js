// apps/flashcards/ai.js
// Cliente Google Gemini API BYOK (Batch Structured JSON con Fallback de Modelo)
// Datalaria Flashcards AI ("Mazo Mágico v2.0")

const PRIMARY_MODEL = 'gemini-2.5-flash';
const FALLBACK_MODEL = 'gemini-2.0-flash';

/**
 * Genera un conjunto completo de tarjetas flashcards mediante una única llamada Batch JSON a Gemini.
 * @param {Array<string>} termsList - Lista de palabras/conceptos introducidos por el usuario.
 * @param {string} generationMode - Modo (ej: 'translate_en', 'translate_es', 'define_es', etc.)
 * @param {string} apiKey - Clave de Google AI Studio del usuario.
 * @returns {Promise<{success: boolean, cards?: Array<{front: string, back: string, phonetic: string, hint: string}>, error?: string}>}
 */
export async function generateBatchDeckWithGemini(termsList, generationMode, apiKey) {
  if (!apiKey || typeof apiKey !== 'string' || apiKey.trim().length < 10) {
    return {
      success: false,
      error: 'Por favor, introduce una API Key válida de Google Gemini (AI Studio).'
    };
  }

  const cleanTerms = termsList
    .map(t => (typeof t === 'string' ? t.trim() : ''))
    .filter(Boolean);

  if (cleanTerms.length === 0) {
    return {
      success: false,
      error: 'No se encontraron términos para generar.'
    };
  }

  const [action, lang] = (generationMode || 'translate_en').split('_');
  const langMap = {
    en: 'English',
    es: 'Spanish',
    fr: 'French',
    de: 'German',
    pt: 'Portuguese',
    it: 'Italian'
  };
  const targetLanguage = langMap[lang] || 'English';

  let systemInstruction = '';
  if (action === 'translate') {
    systemInstruction = `You are an expert bilingual educational tutor. Given a list of terms, translate each term to ${targetLanguage}.
For each term, provide:
1. "front": The original input term.
2. "back": The accurate and natural translation in ${targetLanguage}.
3. "phonetic": A clear phonetic pronunciation guide (IPA or intuitive syllabic transcription, e.g., "/dʒɔɪnts/").
4. "hint": A short pedagogical hint or mnemonic in Spanish (max 12 words) to help remember the concept.`;
  } else {
    // Action: define
    systemInstruction = `You are an expert educational tutor. Given a list of terms, provide a single, short, and crystal-clear definition in ${targetLanguage} suitable for active recall flashcards.
For each term, provide:
1. "front": The original input term.
2. "back": A concise, pedagogical definition (max 15 words) in ${targetLanguage}.
3. "phonetic": A pronunciation hint or syllables.
4. "hint": A short mnemonic hint (max 10 words).`;
  }

  const promptText = `Generate flashcards for the following terms in valid JSON format.
Terms to process:
${cleanTerms.map((t, idx) => `${idx + 1}. ${t}`).join('\n')}

Output MUST be a single raw JSON array containing objects with keys: "front", "back", "phonetic", "hint". Do not include extra conversational text.`;

  // Intentar con modelo primario y luego fallback
  const modelsToTry = [PRIMARY_MODEL, FALLBACK_MODEL];
  let lastErrorMsg = '';

  for (const model of modelsToTry) {
    try {
      const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${encodeURIComponent(apiKey.trim())}`;
      
      const payload = {
        contents: [
          {
            role: 'user',
            parts: [{ text: `${systemInstruction}\n\n${promptText}` }]
          }
        ],
        generationConfig: {
          temperature: 0.2,
          responseMimeType: 'application/json'
        }
      };

      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        const msg = errorData?.error?.message || `HTTP ${res.status} ${res.statusText}`;
        lastErrorMsg = msg;
        // Si es 404 o problema de modelo, probar fallback
        if (res.status === 404 || res.status === 400) {
          continue;
        }
        return { success: false, error: `Error Gemini (${model}): ${msg}` };
      }

      const data = await res.json();
      const rawText = data?.candidates?.[0]?.content?.parts?.[0]?.text;
      if (!rawText) {
        throw new Error('Respuesta vacía del modelo Gemini.');
      }

      // Limpieza de posibles delimitadores markdown json
      let sanitizedJson = rawText.trim();
      if (sanitizedJson.startsWith('```json')) {
        sanitizedJson = sanitizedJson.replace(/^```json\s*/i, '').replace(/\s*```$/, '');
      } else if (sanitizedJson.startsWith('```')) {
        sanitizedJson = sanitizedJson.replace(/^```\s*/, '').replace(/\s*```$/, '');
      }

      const parsedArray = JSON.parse(sanitizedJson);
      if (!Array.isArray(parsedArray) || parsedArray.length === 0) {
        throw new Error('El modelo no devolvió una lista válida de tarjetas.');
      }

      const cleanCards = parsedArray.map(item => ({
        front: String(item.front || '').trim(),
        back: String(item.back || '').trim(),
        phonetic: String(item.phonetic || '').trim(),
        hint: String(item.hint || '').trim()
      })).filter(c => c.front && c.back);

      return {
        success: true,
        cards: cleanCards
      };

    } catch (err) {
      lastErrorMsg = err.message || String(err);
    }
  }

  return {
    success: false,
    error: `No se pudo conectar con la API de Gemini: ${lastErrorMsg}`
  };
}
