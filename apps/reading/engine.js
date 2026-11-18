// apps/reading/engine.js - Motor determinista de lectura, PRNG por semilla, PPM/WPM, evaluación ortográfica (Ñ !== N) y pistas visuales
(function(window) {
  'use strict';

  const SENTINEL_N_TILDE = '\u0001';

  /**
   * Generador pseudoaleatorio determinista por semilla (PRNG Mulberry32).
   * Idéntico al motor de apps/maths/engine.js para paridad en Reto Diario.
   */
  function createSeededRng(seedStr) {
    const str = String(seedStr === null || seedStr === undefined ? '' : seedStr);
    let h = 2166136261 >>> 0;
    for (let i = 0; i < str.length; i++) {
      h = Math.imul(h ^ str.charCodeAt(i), 16777619);
    }
    return function() {
      h += 0x6D2B79F5;
      let t = Math.imul(h ^ (h >>> 15), 1 | h);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  /**
   * Escape HTML estricto para inmunidad XSS (INV-READ-5).
   */
  function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  /**
   * Normaliza cadenas preservando estrictamente la letra Ñ/ñ distinta de N/n (INV-READ-12).
   * Tolera tildes opcionales (Á->A, É->E, Í->I, Ó->O, Ú->U, Ü->U) e insensibilidad a mayúsculas.
   */
  function normalizeAnswer(str) {
    if (str === null || str === undefined) return '';
    const raw = String(str);
    // Proteger Ñ/ñ en NFC antes de descomposición NFD
    const precomposed = typeof raw.normalize === 'function' ? raw.normalize('NFC') : raw;
    const withSentinel = precomposed.replace(/[Ññ]/g, SENTINEL_N_TILDE);
    const stripped = typeof withSentinel.normalize === 'function'
      ? withSentinel.normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      : withSentinel;
    return stripped
      .replace(/\u0001/g, 'Ñ')
      .toUpperCase()
      .trim();
  }

  /**
   * Normaliza un único carácter preservando Ñ distinta de N (INV-READ-12).
   */
  function normalizeChar(ch) {
    if (ch === null || ch === undefined) return '';
    const norm = normalizeAnswer(String(ch));
    return norm.length > 0 ? norm.charAt(0) : '';
  }

  /**
   * Calcula Palabras Por Minuto (PPM / WPM) de forma pura y determinista (INV-READ-2).
   * Cláusula de guarda anti-división por cero: elapsedSec = Math.max(0.4, elapsedMs / 1000).
   * Techo de seguridad: 350 PPM.
   */
  function computeWpm(wordCount, elapsedMs) {
    if (typeof wordCount !== 'number' || isNaN(wordCount) || wordCount <= 0) {
      return 0;
    }
    const ms = (typeof elapsedMs === 'number' && !isNaN(elapsedMs) && elapsedMs > 0) ? elapsedMs : 0;
    const elapsedSec = Math.max(0.4, ms / 1000);
    return Math.min(350, Math.round((wordCount * 60) / elapsedSec));
  }

  /**
   * Calcula puntuación determinista de la ronda según Spec §4.1.
   */
  function computeRoundScore(params) {
    const opts = params || {};
    const mode = opts.mode || 'normal';
    const streak = (typeof opts.streak === 'number' && !isNaN(opts.streak) && opts.streak >= 0) ? opts.streak : 0;
    const usedHint = Boolean(opts.usedHint);
    const elapsedMs = (typeof opts.elapsedMs === 'number' && !isNaN(opts.elapsedMs) && opts.elapsedMs >= 0) ? opts.elapsedMs : 0;
    const targetSec = (typeof opts.targetSec === 'number' && !isNaN(opts.targetSec) && opts.targetSec > 0) ? opts.targetSec : 10;

    const base = 100;
    const speedBonus = (mode === 'stopwatch' || mode === 'daily')
      ? Math.round(Math.max(0, targetSec - (elapsedMs / 1000)) * 12)
      : 0;
    const multiplier = streak >= 5 ? 3 : (streak >= 3 ? 2 : 1);
    const cleanBonus = usedHint ? 0 : 20;

    return Math.round((base + speedBonus) * multiplier) + cleanBonus;
  }

  function shuffleArray(arr, rng) {
    const f = (typeof rng === 'function') ? rng : Math.random;
    const copy = arr.slice();
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(f() * (i + 1));
      const tmp = copy[i];
      copy[i] = copy[j];
      copy[j] = tmp;
    }
    return copy;
  }

  function pickRandom(arr, rng) {
    const f = (typeof rng === 'function') ? rng : Math.random;
    return arr[Math.floor(f() * arr.length)];
  }

  // Registro ligero solo para llamadas sin PRNG externo (para evitar repeticiones inmediatas en modo libre)
  const lastUnseededByPool = {};

  function getCatalog() {
    if (window && window.READING_CATALOG) {
      return window.READING_CATALOG;
    }
    if (typeof globalThis !== 'undefined' && globalThis.READING_CATALOG) {
      return globalThis.READING_CATALOG;
    }
    throw new Error('READING_CATALOG is not loaded.');
  }

  function selectPoolItem(pool, poolKey, rng, recentIds) {
    if (!Array.isArray(pool) || pool.length === 0) {
      throw new Error(`Empty bank for pool ${poolKey}`);
    }
    let candidates = pool;
    if (Array.isArray(recentIds) && recentIds.length > 0 && pool.length > recentIds.length) {
      const excluded = new Set(recentIds);
      const filtered = pool.filter(item => !excluded.has(item.id));
      if (filtered.length > 0) {
        candidates = filtered;
      }
    } else if (typeof rng !== 'function' && pool.length > 1 && lastUnseededByPool[poolKey]) {
      const filtered = pool.filter(item => item.id !== lastUnseededByPool[poolKey]);
      if (filtered.length > 0) {
        candidates = filtered;
      }
    }

    const picked = pickRandom(candidates, rng);
    if (typeof rng !== 'function') {
      lastUnseededByPool[poolKey] = picked.id;
    }
    return picked;
  }

  /**
   * Construye el teclado alfabético táctil (8-10 teclas sin duplicados) para Nivel l3.
   */
  function buildKeyboardChars(word, missingIndices, lang, rng) {
    const seen = new Set();
    const chars = [];

    // 1. Añadir letras esperadas obligatorias
    for (const idx of missingIndices) {
      const ch = normalizeChar(word.charAt(idx));
      if (ch && !seen.has(ch)) {
        seen.add(ch);
        chars.push(ch);
      }
    }

    // 2. Completar con distractores fonéticos hasta 9 teclas (rango 8-10)
    const distractorAlphabet = lang === 'es'
      ? ['A', 'E', 'I', 'O', 'U', 'L', 'M', 'P', 'S', 'T', 'D', 'N', 'R', 'C', 'B', 'F', 'G', 'Ñ', 'V', 'Z']
      : ['A', 'E', 'I', 'O', 'U', 'B', 'C', 'D', 'F', 'G', 'H', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'W', 'K'];

    // Si la palabra contiene N en español y falta, priorizar Ñ como distractor didáctico
    if (lang === 'es' && seen.has('N') && !seen.has('Ñ')) {
      seen.add('Ñ');
      chars.push('Ñ');
    } else if (lang === 'es' && seen.has('Ñ') && !seen.has('N')) {
      seen.add('N');
      chars.push('N');
    }

    const shuffledAlphabet = shuffleArray(distractorAlphabet, rng);
    const targetSize = Math.min(10, Math.max(8, chars.length + 6, 9));

    for (const ch of shuffledAlphabet) {
      if (chars.length >= targetSize) break;
      if (!seen.has(ch)) {
        seen.add(ch);
        chars.push(ch);
      }
    }

    return shuffleArray(chars, rng);
  }

  /**
   * Genera un reto de lectura determinista para el nivel y lengua dados.
   * Totalmente tolerante a rng = null / undefined.
   */
  function generateChallenge(levelId, lang = 'es', rng = null, recentIds = null) {
    const safeLang = (lang === 'en') ? 'en' : 'es';
    const validLevels = ['l1', 'l2', 'l3', 'l4', 'l5', 'l6'];
    const safeLevel = validLevels.includes(levelId) ? levelId : 'l1';
    const safeRng = (typeof rng === 'function') ? rng : Math.random;
    const catalog = getCatalog();

    if (safeLevel === 'l1') {
      const pool = catalog.wordBank[safeLang].l1;
      const item = selectPoolItem(pool, `${safeLang}_l1`, rng, recentIds);
      const rawChoices = [
        { id: 'c_correct', label: item.target, isCorrect: true },
        ...item.distractors.slice(0, 3).map((d, idx) => ({
          id: `c_dist_${idx}`,
          label: d,
          isCorrect: false
        }))
      ];
      return {
        id: item.id,
        levelId: 'l1',
        lang: safeLang,
        kind: 'choice',
        prompt: item.target,
        anchorWord: item.anchorWord,
        emoji: item.emoji,
        syllables: [item.target],
        wordCount: 1,
        choices: shuffleArray(rawChoices, safeRng)
      };
    }

    if (safeLevel === 'l2') {
      const pool = catalog.wordBank[safeLang].l2;
      const item = selectPoolItem(pool, `${safeLang}_l2`, rng, recentIds);
      const rawChoices = [
        { id: 'c_correct', label: item.word, isCorrect: true },
        ...item.distractors.slice(0, 3).map((d, idx) => ({
          id: `c_dist_${idx}`,
          label: d,
          isCorrect: false
        }))
      ];
      return {
        id: item.id,
        levelId: 'l2',
        lang: safeLang,
        kind: 'choice',
        prompt: item.word,
        syllables: item.syllables.slice(),
        emoji: item.emoji,
        wordCount: 1,
        choices: shuffleArray(rawChoices, safeRng)
      };
    }

    if (safeLevel === 'l3') {
      const pool = catalog.wordBank[safeLang].l3;
      const item = selectPoolItem(pool, `${safeLang}_l3`, rng, recentIds);
      const sortedIndices = item.missingIndices.slice().sort((a, b) => a - b);
      const maskedSlots = sortedIndices.map(idx => ({
        index: idx,
        expected: item.word.charAt(idx)
      }));
      const keyboardChars = buildKeyboardChars(item.word, sortedIndices, safeLang, safeRng);

      return {
        id: item.id,
        levelId: 'l3',
        lang: safeLang,
        kind: 'fill_letters',
        prompt: item.word,
        syllables: item.syllables.slice(),
        emoji: item.emoji,
        wordCount: 1,
        missingIndices: sortedIndices,
        maskedSlots,
        keyboardChars
      };
    }

    if (safeLevel === 'l4') {
      const pool = catalog.wordBank[safeLang].l4;
      const item = selectPoolItem(pool, `${safeLang}_l4`, rng, recentIds);
      const options = shuffleArray(
        item.microCheck.options.map(o => ({
          icon: o.emoji || o.icon || '',
          emoji: o.emoji || o.icon || '',
          label: o.label,
          isCorrect: Boolean(o.isCorrect)
        })),
        safeRng
      );
      return {
        id: item.id,
        levelId: 'l4',
        lang: safeLang,
        kind: 'read_check',
        prompt: item.word,
        syllables: item.syllables.slice(),
        emoji: item.emoji,
        wordCount: 1,
        microCheck: {
          question: item.microCheck.question,
          options
        }
      };
    }

    // l5 y l6
    const sPool = catalog.sentenceBank[safeLang][safeLevel];
    const sItem = selectPoolItem(sPool, `${safeLang}_${safeLevel}`, rng, recentIds);
    const sOptions = shuffleArray(
      sItem.microCheck.options.map(o => ({
        icon: o.icon || o.emoji || '',
        emoji: o.icon || o.emoji || '',
        label: o.label,
        isCorrect: Boolean(o.isCorrect)
      })),
      safeRng
    );

    return {
      id: sItem.id,
      levelId: safeLevel,
      lang: safeLang,
      kind: 'read_check',
      prompt: sItem.lines.join(' '),
      lines: sItem.lines.slice(),
      wordCount: sItem.wordCount,
      microCheck: {
        question: sItem.microCheck.question,
        options: sOptions
      }
    };
  }

  /**
   * Evalúa estrictamente la respuesta del usuario para los 3 modos de entrada:
   * - 'choice' (l1, l2)
   * - 'fill_letters' (l3)
   * - 'read_check' (l4, l5, l6)
   */
  function evaluateChallenge(challenge, userInput, lang = 'es') {
    if (!challenge) {
      return { isCorrect: false, correctDisplay: '', userDisplay: '' };
    }

    if (challenge.kind === 'choice') {
      let userStr = '';
      if (userInput !== null && userInput !== undefined) {
        if (typeof userInput === 'object') {
          userStr = String(userInput.label !== undefined ? userInput.label : (userInput.value || ''));
        } else {
          userStr = String(userInput);
        }
      }
      const isCorrect = normalizeAnswer(userStr) === normalizeAnswer(challenge.prompt);
      return {
        isCorrect,
        expected: challenge.prompt,
        correctDisplay: challenge.prompt,
        userDisplay: userStr
      };
    }

    if (challenge.kind === 'fill_letters') {
      let builtWord = '';
      if (Array.isArray(userInput)) {
        const chars = challenge.prompt.split('');
        const slots = challenge.maskedSlots || [];
        for (let i = 0; i < slots.length; i++) {
          const slot = slots[i];
          const fill = (userInput[i] !== null && userInput[i] !== undefined) ? String(userInput[i]) : '_';
          chars[slot.index] = fill;
        }
        builtWord = chars.join('');
      } else if (userInput && typeof userInput === 'object') {
        if (Array.isArray(userInput.slots)) {
          return evaluateChallenge(challenge, userInput.slots, lang);
        }
        builtWord = String(userInput.word || userInput.value || '');
      } else if (userInput !== null && userInput !== undefined) {
        builtWord = String(userInput);
      }

      const isCorrect = normalizeAnswer(builtWord) === normalizeAnswer(challenge.prompt);
      return {
        isCorrect,
        expected: challenge.prompt,
        correctDisplay: challenge.prompt,
        userDisplay: builtWord
      };
    }

    // 'read_check' (l4, l5, l6)
    const mc = challenge.microCheck || { options: [] };
    const options = mc.options || [];
    const correctOpt = options.find(o => o.isCorrect === true);
    const correctDisplay = correctOpt
      ? `${correctOpt.icon || correctOpt.emoji || ''} ${correctOpt.label}`.trim()
      : challenge.prompt;

    let selectedOpt = null;
    let userDisplay = '';

    if (typeof userInput === 'number' && options[userInput]) {
      selectedOpt = options[userInput];
    } else if (userInput && typeof userInput === 'object') {
      if (typeof userInput.index === 'number' && options[userInput.index]) {
        selectedOpt = options[userInput.index];
      } else if (userInput.label !== undefined) {
        const targetNorm = normalizeAnswer(userInput.label);
        selectedOpt = options.find(o => normalizeAnswer(o.label) === targetNorm) || userInput;
      }
    } else if (typeof userInput === 'string') {
      const targetNorm = normalizeAnswer(userInput);
      selectedOpt = options.find(o => normalizeAnswer(o.label) === targetNorm);
      userDisplay = userInput;
    }

    const isCorrect = Boolean(selectedOpt && selectedOpt.isCorrect === true);
    if (selectedOpt && selectedOpt.label) {
      userDisplay = `${selectedOpt.icon || selectedOpt.emoji || ''} ${selectedOpt.label}`.trim();
    }

    return {
      isCorrect,
      expected: correctOpt ? correctOpt.label : '',
      correctDisplay,
      userDisplay
    };
  }

  /**
   * Renderiza sílabas seguras con escape HTML estricto, alternando 2 colores (--syl-a / --syl-b)
   * y generando puntos de golpeteo silábico (●).
   */
  function renderSyllableTokens(syllables, colorize = true) {
    const list = Array.isArray(syllables)
      ? syllables
      : (syllables ? [String(syllables)] : []);
    if (list.length === 0) return '';

    const tokensHtml = list.map((syl, idx) => {
      const safeSyl = escapeHtml(syl);
      const cls = colorize
        ? (idx % 2 === 0 ? 'syl-token syl-a' : 'syl-token syl-b')
        : 'syl-token';
      return `<span class="${cls}">${safeSyl}</span>`;
    }).join('<span class="syl-dot" aria-hidden="true">·</span>');

    const clapsHtml = list
      .map(() => '<span class="clap-dot" aria-hidden="true">●</span>')
      .join(' ');

    return `<div class="syllable-tokens-wrap">` +
      `<div class="syllable-row">${tokensHtml}</div>` +
      `<div class="clap-dots-row" aria-hidden="true">${clapsHtml}</div>` +
      `</div>`;
  }

  /**
   * Genera HTML seguro (anti-XSS) para la pista visual didáctica de cada nivel.
   */
  function renderVisualHint(challenge, lang = 'es') {
    const safeLang = (lang === 'en') ? 'en' : 'es';
    if (!challenge) {
      const emptyMsg = safeLang === 'en'
        ? '💡 Read syllable by syllable at your own pace!'
        : '💡 ¡Lee sílaba a sílaba con calma!';
      return `<div class="visual-hint-box">${escapeHtml(emptyMsg)}</div>`;
    }

    if (challenge.levelId === 'l1') {
      const safeEmoji = escapeHtml(challenge.emoji || '');
      const safeAnchor = escapeHtml(challenge.anchorWord || challenge.prompt || '');
      const safeTarget = escapeHtml(challenge.prompt || '');
      const tipLabel = safeLang === 'en' ? 'Starts with:' : 'Empieza por:';
      return `<div class="visual-hint-box">` +
        `<span class="hint-emoji">${safeEmoji}</span>` +
        `<span class="hint-text">${escapeHtml(tipLabel)} <strong class="syl-a">${safeTarget}</strong> (${safeAnchor})</span>` +
        `</div>`;
    }

    if (challenge.levelId === 'l2' || challenge.levelId === 'l3') {
      const sylHtml = renderSyllableTokens(challenge.syllables || [challenge.prompt], true);
      const clapsCount = (challenge.syllables && challenge.syllables.length) || 1;
      const clueLabel = safeLang === 'en'
        ? `${clapsCount} syllable${clapsCount > 1 ? 's' : ''} · Starts with "${escapeHtml((challenge.prompt || '').charAt(0))}"`
        : `${clapsCount} sílaba${clapsCount > 1 ? 's' : ''} · Empieza por "${escapeHtml((challenge.prompt || '').charAt(0))}"`;
      return `<div class="visual-hint-box">${sylHtml}<div class="hint-caption">${clueLabel}</div></div>`;
    }

    if (challenge.levelId === 'l4') {
      const sylHtml = renderSyllableTokens(challenge.syllables || [challenge.prompt], true);
      const safeEmoji = escapeHtml(challenge.emoji || '');
      const clueLabel = safeLang === 'en' ? 'Visual clue unlocked:' : 'Pista visual desbloqueada:';
      return `<div class="visual-hint-box">` +
        `<div class="hint-caption">${escapeHtml(clueLabel)} <span class="hint-emoji">${safeEmoji}</span></div>` +
        `${sylHtml}` +
        `</div>`;
    }

    // l5 y l6: Pista de entonación y pausas
    const tipText = safeLang === 'en'
      ? '💡 Pause briefly at commas (,) and breathe cleanly at periods (.). Notice ? and ! tone changes.'
      : '💡 Haz una pausa breve en las comas (,) y respira en los puntos (.). Marca bien los signos ¿? y ¡!.';
    return `<div class="visual-hint-box"><div class="hint-caption">${escapeHtml(tipText)}</div></div>`;
  }

  const ReadingEngine = {
    createSeededRng,
    escapeHtml,
    normalizeAnswer,
    normalizeChar,
    computeWpm,
    computeRoundScore,
    generateChallenge,
    evaluateChallenge,
    renderSyllableTokens,
    renderVisualHint
  };

  window.ReadingEngine = ReadingEngine;
})(window);
