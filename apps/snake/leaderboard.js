// apps/snake/leaderboard.js
// Conector Seguro y Resiliente a Supabase PostgREST + Cola Offline + Anti-XSS
// Datalaria Neon Snake ("Cyberpunk Overdrive v2.0")

const SUPABASE_URL = "https://wxwnbzmbzztegcdzrxbg.supabase.co";
const SUPABASE_KEY = "sb_publishable_hAEvRnntjRnk11ps4n1yVw__PwZYoSy";

const CACHE_KEY = "datalaria_snake_cached_ranking";
const QUEUE_KEY = "datalaria_snake_offline_queue";

/**
 * Sanitiza un alias de agente evitando cualquier inyección de código o desbordamiento.
 * @param {string} rawName
 * @returns {string}
 */
export function sanitizeAgentName(rawName) {
  if (!rawName || typeof rawName !== "string") return "Agente 007";
  // Eliminar etiquetas HTML y caracteres potencialmente peligrosos
  const clean = rawName
    .replace(/<[^>]*>/g, "")
    .replace(/[^\w\s\-\.]/gi, "")
    .trim()
    .slice(0, 12);
  return clean || "Agente 007";
}

/**
 * Obtiene el ranking de mejores puntuaciones desde Supabase con fallback a caché local.
 * @param {number} limit
 * @returns {Promise<{scores: Array<{username: string, score: number}>, fromCache: boolean}>}
 */
export async function fetchTopScores(limit = 20) {
  // 1. Intentar sincronizar cola de puntuaciones offline pendientes
  flushOfflineQueue().catch(() => {});

  const endpoint = `${SUPABASE_URL}/rest/v1/snake_scores?select=username,score,created_at&order=score.desc&limit=${limit}`;

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4500);

    const res = await fetch(endpoint, {
      method: "GET",
      headers: {
        "apikey": SUPABASE_KEY,
        "Authorization": `Bearer ${SUPABASE_KEY}`,
        "Content-Type": "application/json"
      },
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    const data = await res.json();
    const sanitizedList = (data || []).map(entry => ({
      username: sanitizeAgentName(entry.username),
      score: Number(entry.score) || 0
    }));

    // Actualizar caché local
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify(sanitizedList));
    } catch (e) {}

    return { scores: sanitizedList, fromCache: false };
  } catch (err) {
    console.warn("[leaderboard.js] Error consultando Supabase, cargando caché local:", err);
    let cached = [];
    try {
      const raw = localStorage.getItem(CACHE_KEY);
      if (raw) cached = JSON.parse(raw);
    } catch (e) {}
    return { scores: cached, fromCache: true };
  }
}

/**
 * Guarda una puntuación en Supabase. Si está offline, la encola localmente.
 * @param {string} agentName
 * @param {number} score
 * @returns {Promise<{success: boolean, queued: boolean}>}
 */
export async function saveScore(agentName, score) {
  const safeName = sanitizeAgentName(agentName);
  const numericScore = Math.floor(Math.max(0, Number(score) || 0));

  const endpoint = `${SUPABASE_URL}/rest/v1/snake_scores`;
  const payload = [{ username: safeName, score: numericScore }];

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4500);

    const res = await fetch(endpoint, {
      method: "POST",
      headers: {
        "apikey": SUPABASE_KEY,
        "Authorization": `Bearer ${SUPABASE_KEY}`,
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
      },
      body: JSON.stringify(payload),
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return { success: true, queued: false };
  } catch (err) {
    console.warn("[leaderboard.js] No se pudo guardar online, encolando localmente:", err);
    enqueueScoreLocally(safeName, numericScore);
    return { success: true, queued: true };
  }
}

/**
 * Encola una puntuación en localStorage para sincronizarla cuando vuelva la red
 * e inyecta optimistamente el récord en la caché local del ranking (INV-SNAKE-13).
 */
export function enqueueScoreLocally(username, score) {
  try {
    const raw = localStorage.getItem(QUEUE_KEY);
    const queue = raw ? JSON.parse(raw) : [];
    queue.push({ username, score, timestamp: Date.now() });
    localStorage.setItem(QUEUE_KEY, JSON.stringify(queue.slice(-10))); // Máx 10 en cola

    // Inyección optimista en la caché local del ranking
    let cached = [];
    const cachedRaw = localStorage.getItem(CACHE_KEY);
    if (cachedRaw) {
      try { cached = JSON.parse(cachedRaw); } catch (e) { cached = []; }
    }
    cached.push({ username, score, pendingSync: true });
    cached.sort((a, b) => (Number(b.score) || 0) - (Number(a.score) || 0));
    localStorage.setItem(CACHE_KEY, JSON.stringify(cached.slice(0, 20)));
  } catch (e) {}
}

/**
 * Envía las puntuaciones pendientes guardadas mientras no había conexión.
 * @returns {Promise<{flushed: number}>}
 */
export async function flushOfflineQueue() {
  try {
    const raw = localStorage.getItem(QUEUE_KEY);
    if (!raw) return { flushed: 0 };
    const queue = JSON.parse(raw);
    if (!queue.length) return { flushed: 0 };

    let flushedCount = 0;
    for (let i = 0; i < queue.length; i++) {
      const item = queue[i];
      try {
        const res = await fetch(`${SUPABASE_URL}/rest/v1/snake_scores`, {
          method: "POST",
          headers: {
            "apikey": SUPABASE_KEY,
            "Authorization": `Bearer ${SUPABASE_KEY}`,
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
          },
          body: JSON.stringify([{ username: item.username, score: item.score }])
        });
        if (res.ok) flushedCount++;
      } catch (e) {}
    }
    localStorage.removeItem(QUEUE_KEY);

    // Limpiar banderas pendingSync en la caché local
    try {
      const cachedRaw = localStorage.getItem(CACHE_KEY);
      if (cachedRaw) {
        const cached = JSON.parse(cachedRaw).map(entry => {
          const { pendingSync, ...rest } = entry;
          return rest;
        });
        localStorage.setItem(CACHE_KEY, JSON.stringify(cached));
      }
    } catch (e) {}

    console.log(`[leaderboard.js] Cola offline sincronizada con éxito (${flushedCount} puntuaciones).`);
    return { flushed: flushedCount };
  } catch (e) {
    return { flushed: 0 };
  }
}

/**
 * Renderizado seguro en el DOM garantizando INMUNIDAD XSS (INV-SNAKE-5).
 * Usa document.createElement y textContent, prohibiendo innerHTML con datos de usuario.
 */
export function renderRankingListSafe(containerEl, scores, currentAgentName, youBadgeText = "TÚ", offlineBadgeText = "⏳ OFFLINE") {
  if (!containerEl) return;
  containerEl.innerHTML = ""; // Limpiar contenedor de forma segura

  if (!scores || scores.length === 0) {
    const li = document.createElement("li");
    li.className = "ranking-empty";
    li.textContent = "Sin datos en la base de datos central.";
    containerEl.appendChild(li);
    return;
  }

  const safeCurrentName = sanitizeAgentName(currentAgentName);

  scores.forEach((entry, idx) => {
    const li = document.createElement("li");
    li.className = "ranking-row";
    if (idx === 0) li.classList.add("rank-1");
    else if (idx === 1) li.classList.add("rank-2");
    else if (idx === 2) li.classList.add("rank-3");

    const isCurrent = entry.username === safeCurrentName;
    if (isCurrent) {
      li.classList.add("is-current-agent");
    }

    if (entry.pendingSync) {
      li.classList.add("is-offline-pending");
    }

    // Columna izquierda: Posición + Icono medalla + Nombre
    const leftCol = document.createElement("div");
    leftCol.className = "ranking-left";

    const posSpan = document.createElement("span");
    posSpan.className = "ranking-pos";
    if (idx === 0) posSpan.textContent = "🥇 #1";
    else if (idx === 1) posSpan.textContent = "🥈 #2";
    else if (idx === 2) posSpan.textContent = "🥉 #3";
    else posSpan.textContent = `#${String(idx + 1).padStart(2, "0")}`;
    leftCol.appendChild(posSpan);

    const nameSpan = document.createElement("span");
    nameSpan.className = "ranking-name";
    nameSpan.textContent = entry.username; // XSS-SAFE: textContent
    leftCol.appendChild(nameSpan);

    if (isCurrent) {
      const youBadge = document.createElement("span");
      youBadge.className = "ranking-you-badge";
      youBadge.textContent = youBadgeText;
      leftCol.appendChild(youBadge);
    }

    if (entry.pendingSync) {
      const offlineBadge = document.createElement("span");
      offlineBadge.className = "ranking-offline-badge";
      offlineBadge.textContent = offlineBadgeText;
      leftCol.appendChild(offlineBadge);
    }

    // Columna derecha: Puntuación
    const scoreSpan = document.createElement("span");
    scoreSpan.className = "ranking-score";
    scoreSpan.textContent = `${Number(entry.score || 0).toLocaleString()} PTS`;

    li.appendChild(leftCol);
    li.appendChild(scoreSpan);
    containerEl.appendChild(li);
  });
}
