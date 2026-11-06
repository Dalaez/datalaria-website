// apps/flashcards/engine.js
// Motor Lógico: Parser/Exportador CSV RFC-4180, Cajas Leitner, Quiz Distractors y Spelling Helper
// Datalaria Flashcards AI ("Mazo Mágico v2.0")

/**
 * Parsea un contenido CSV / TSV cumpliendo con RFC-4180 (soporte para comillas y saltos).
 * @param {string} text - Contenido en texto crudo del fichero CSV.
 * @returns {Array<{front: string, back: string, phonetic?: string, hint?: string}>}
 */
export function parseCSV(text) {
  if (!text || typeof text !== 'string') return [];
  
  const clean = text.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  const rows = [];
  let currentRow = [];
  let currentField = '';
  let inQuotes = false;

  // Detección automática de delimitador preponderante fuera de comillas (, ; o \t)
  const firstLine = clean.split('\n')[0] || '';
  let delimiter = ',';
  const commaCount = (firstLine.match(/,/g) || []).length;
  const semiCount = (firstLine.match(/;/g) || []).length;
  const tabCount = (firstLine.match(/\t/g) || []).length;
  if (semiCount > commaCount && semiCount > tabCount) delimiter = ';';
  else if (tabCount > commaCount && tabCount > semiCount) delimiter = '\t';

  for (let i = 0; i < clean.length; i++) {
    const char = clean[i];
    const nextChar = clean[i + 1];

    if (inQuotes) {
      if (char === '"' && nextChar === '"') {
        currentField += '"';
        i++; // Saltar comilla escapada
      } else if (char === '"') {
        inQuotes = false;
      } else {
        currentField += char;
      }
    } else {
      if (char === '"') {
        inQuotes = true;
      } else if (char === delimiter) {
        currentRow.push(currentField.trim());
        currentField = '';
      } else if (char === '\n') {
        currentRow.push(currentField.trim());
        if (currentRow.some(f => f.length > 0)) {
          rows.push(currentRow);
        }
        currentRow = [];
        currentField = '';
      } else {
        currentField += char;
      }
    }
  }

  if (currentField.length > 0 || currentRow.length > 0) {
    currentRow.push(currentField.trim());
    if (currentRow.some(f => f.length > 0)) {
      rows.push(currentRow);
    }
  }

  if (rows.length === 0) return [];

  // Detección y filtrado de cabecera si incluye palabras clave
  let startIndex = 0;
  const headerCandidate = rows[0].map(c => c.toLowerCase());
  if (
    headerCandidate.some(h =>
      h.includes('término') || h.includes('termino') ||
      h.includes('term') || h.includes('pregunta') ||
      h.includes('front') || h.includes('word')
    )
  ) {
    startIndex = 1;
  }

  const cards = [];
  for (let r = startIndex; r < rows.length; r++) {
    const cols = rows[r];
    if (!cols || cols.length === 0) continue;
    const front = cols[0] ? cols[0].trim() : '';
    const back = cols[1] ? cols[1].trim() : '';
    const phonetic = cols[2] ? cols[2].trim() : '';
    const hint = cols[3] ? cols[3].trim() : '';

    if (front && back) {
      cards.push({
        front,
        back,
        ...(phonetic ? { phonetic } : {}),
        ...(hint ? { hint } : {})
      });
    }
  }

  return cards;
}

/**
 * Serializa un mazo de tarjetas a formato CSV estándar RFC-4180.
 * @param {Array<{front: string, back: string, phonetic?: string, hint?: string}>} cards
 * @returns {string} Contenido CSV seguro con comillas escapadas
 */
export function exportCSV(cards) {
  if (!Array.isArray(cards) || cards.length === 0) {
    return 'Term,Definition/Translation,Phonetic,Hint\r\n';
  }

  const escapeField = (val) => {
    if (val === undefined || val === null) return '""';
    const str = String(val);
    if (str.includes(',') || str.includes(';') || str.includes('"') || str.includes('\n')) {
      return `"${str.replace(/"/g, '""')}"`;
    }
    return str;
  };

  const lines = ['Term,Definition/Translation,Phonetic,Hint'];
  for (const card of cards) {
    const f = escapeField(card.front);
    const b = escapeField(card.back);
    const p = escapeField(card.phonetic || '');
    const h = escapeField(card.hint || '');
    lines.push(`${f},${b},${p},${h}`);
  }

  return lines.join('\r\n') + '\r\n';
}

/**
 * Genera 4 opciones para el Modo Quiz: 1 correcta y 3 distractores aleatorios.
 * @param {object} currentCard - Tarjeta activa.
 * @param {Array<object>} deck - Baraja completa para extraer distractores.
 * @returns {Array<{text: string, isCorrect: boolean}>}
 */
export function generateQuizOptions(currentCard, deck) {
  if (!currentCard) return [];
  const correctText = currentCard.back;
  
  // Extraer posibles respuestas distintas a la correcta
  const otherOptions = deck
    .map(c => c.back)
    .filter(b => b && b.toLowerCase() !== correctText.toLowerCase());

  // Mezclar alternativas
  const shuffledOthers = [...otherOptions].sort(() => 0.5 - Math.random());
  const selectedDistractors = shuffledOthers.slice(0, 3);

  // Fallbacks si el mazo tiene menos de 4 cartas
  const fallbacks = [
    'Ninguna de las anteriores',
    'Concepto en proceso de consolidación',
    'Definición alternativa no aplicable'
  ];
  while (selectedDistractors.length < 3) {
    const fb = fallbacks[selectedDistractors.length] || `Alternativa ${selectedDistractors.length + 1}`;
    selectedDistractors.push(fb);
  }

  const options = [
    { text: correctText, isCorrect: true },
    ...selectedDistractors.map(d => ({ text: d, isCorrect: false }))
  ];

  // Mezclar las 4 opciones finales
  return options.sort(() => 0.5 - Math.random());
}

/**
 * Normaliza una cadena para comparaciones ortográficas flexibles en Modo Spelling.
 * @param {string} str 
 * @returns {string}
 */
export function normalizeAnswer(str) {
  if (!str) return '';
  return str
    .trim()
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Quita tildes para tolerancia ortográfica
    .replace(/[.,/#!$%^&*;:{}=\-_`~()?"']/g, '') // Quita signos
    .replace(/\s+/g, ' ');
}

/**
 * Valida si la respuesta escrita coincide con la definición objetivo.
 * @param {string} userAttempt 
 * @param {string} targetBack 
 * @returns {boolean}
 */
export function validateSpelling(userAttempt, targetBack) {
  if (!userAttempt || !targetBack) return false;
  const cleanUser = normalizeAnswer(userAttempt);
  const cleanTarget = normalizeAnswer(targetBack);
  
  // Acierto exacto
  if (cleanUser === cleanTarget) return true;

  // Tolerancia para respuestas con alternativas como "Joint / Joints" o "Avergonzado / Incómodo"
  const alternatives = targetBack.split(/[/;,()]/).map(normalizeAnswer).filter(Boolean);
  return alternatives.includes(cleanUser);
}

/**
 * Genera la máscara de pista para el Modo Spelling revelando N caracteres.
 * @param {string} targetBack - Texto objetivo.
 * @param {number} revealedCount - Cuántas letras se desvelan.
 * @returns {string} Ej: "J o i _ _ _"
 */
export function getSpellingMask(targetBack, revealedCount = 1) {
  if (!targetBack) return '';
  const chars = targetBack.split('');
  let revealedSoFar = 0;

  return chars.map((char) => {
    if (char === ' ' || char === '/' || char === '(' || char === ')' || char === '-') {
      return char;
    }
    if (revealedSoFar < revealedCount) {
      revealedSoFar++;
      return char;
    }
    return '_';
  }).join(' ');
}

/**
 * Calcula el puntaje y porcentaje de dominio Leitner de un mazo.
 * @param {object} masteryState - Mapa de cardId/front -> 'repeat' | 'good' | 'mastered'
 * @param {number} totalCards 
 * @returns {{ score: number, masteredCount: number, percent: number }}
 */
export function calculateDeckMastery(masteryState, totalCards) {
  if (!masteryState || totalCards <= 0) {
    return { score: 0, masteredCount: 0, percent: 0 };
  }
  let score = 0;
  let masteredCount = 0;

  for (const status of Object.values(masteryState)) {
    if (status === 'mastered') {
      score += 3;
      masteredCount++;
    } else if (status === 'good') {
      score += 2;
    }
  }

  const percent = Math.min(100, Math.round((masteredCount / totalCards) * 100));
  return { score, masteredCount, percent };
}
