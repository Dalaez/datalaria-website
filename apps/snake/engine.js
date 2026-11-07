// apps/snake/engine.js
// Motor Determinista de Cuadrícula, Colisiones, Power-ups, Combo y PRNG
// Datalaria Neon Snake ("Cyberpunk Overdrive v2.0")

import { GRID_SIZE } from "./catalog.js";
export { GRID_SIZE };

/**
 * Generador pseudoaleatorio determinista Mulberry32 a partir de una semilla string.
 * @param {string} seedStr
 * @returns {() => number}
 */
export function createSeededRng(seedStr) {
  let hash = 0;
  const str = String(seedStr || "datalaria-snake-daily");
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash |= 0;
  }
  let a = (hash ^ 0xdeadbeef) >>> 0;
  return function () {
    let t = (a += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * Genera la lista de obstáculos fijos para cada nivel en el modo Arcade.
 * @param {number} level
 * @returns {Array<{x: number, y: number}>}
 */
export function getLevelObstacles(level) {
  const obs = [];
  if (level < 5) return obs;
  const add = (x, y) => obs.push({ x, y });

  if (level === 5) {
    for (let i = 2; i < 6; i++) {
      add(i, 2);
      add(i, GRID_SIZE - 3);
      add(GRID_SIZE - 1 - i, 2);
      add(GRID_SIZE - 1 - i, GRID_SIZE - 3);
    }
  } else if (level === 6) {
    for (let i = 6; i < 14; i++) {
      add(i, 9);
      add(i, 10);
    }
  } else if (level === 7) {
    for (let x = 4; x < 8; x++) {
      for (let y = 4; y < 8; y++) add(x, y);
    }
    for (let x = 12; x < 16; x++) {
      for (let y = 12; y < 16; y++) add(x, y);
    }
  } else {
    for (let i = 0; i < GRID_SIZE; i++) {
      if (i % 3 !== 0) {
        add(i, 0);
        add(i, GRID_SIZE - 1);
        add(0, i);
        add(GRID_SIZE - 1, i);
      }
    }
    if (level >= 9) {
      add(5, 5); add(5, 14); add(14, 5); add(14, 14);
    }
  }
  return obs;
}

/**
 * Inicializa el estado del juego para un modo específico.
 */
export function createInitialGameState(modeId = "arcade", options = {}, rng = Math.random) {
  const state = {
    mode: modeId,
    snake: [
      { x: 10, y: 10 },
      { x: 9, y: 10 },
      { x: 8, y: 10 }
    ],
    direction: { x: 1, y: 0 },
    nextDirection: { x: 1, y: 0 },
    inputQueue: [],
    score: 0,
    level: 1,
    baseSpeedMs: 140,
    tickIntervalMs: 140,
    timeRemainingSec: modeId === "time_attack" ? 90 : null,
    totalTimeElapsedSec: 0,
    isGameOver: false,
    isPaused: false,
    
    // Combo System
    combo: 1,
    maxCombo: 1,
    comboTimerSec: 0,
    COMBO_MAX_TIME_SEC: 4.0,

    // Nodos y Power-ups
    food: { x: 15, y: 10, type: "data", lifespanSec: null },
    activePowerups: {
      cryoSec: 0,
      ghostSec: 0
    },
    foodEatenCount: 0,
    
    // Obstáculos con Telegraphing
    obstacles: [], // { x, y, warningTicks: number }
    
    // Eventos del tick para feedback auditivo / visual
    events: [],
    
    // Generador aleatorio inyectado
    rng: rng
  };

  placeFood(state, rng);
  return state;
}

/**
 * Coloca comida o power-up en una celda vacía.
 */
export function placeFood(state, rng = Math.random) {
  const isOccupied = (x, y) => {
    if (state.snake.some(s => s.x === x && s.y === y)) return true;
    if (state.obstacles.some(o => o.x === x && o.y === y && o.warningTicks <= 0)) return true;
    return false;
  };

  let candidate = null;
  let attempts = 0;
  while (!candidate && attempts < 200) {
    attempts++;
    const x = Math.floor(rng() * GRID_SIZE);
    const y = Math.floor(rng() * GRID_SIZE);
    if (!isOccupied(x, y)) {
      candidate = { x, y };
    }
  }

  if (!candidate) {
    candidate = { x: 0, y: 0 };
  }

  // Determinar tipo de nodo
  // Cada 5 comidas garantizamos un Golden Core si no hay powerup activo
  let type = "data";
  const roll = rng();

  if (state.foodEatenCount > 0 && state.foodEatenCount % 5 === 0) {
    type = "golden";
  } else if (roll < 0.12 && state.level >= 2) {
    type = "cryo";
  } else if (roll < 0.22 && state.level >= 3) {
    type = "ghost";
  }

  state.food = {
    x: candidate.x,
    y: candidate.y,
    type: type,
    lifespanSec: type === "golden" ? 6.0 : (type === "cryo" || type === "ghost" ? 7.0 : null)
  };
}

/**
 * Introduce una nueva dirección en la cola de comandos de entrada.
 */
export function queueInput(state, newDir) {
  if (state.isGameOver || state.isPaused) return;
  if (!newDir || (newDir.x === 0 && newDir.y === 0)) return;

  const lastDir = state.inputQueue.length > 0
    ? state.inputQueue[state.inputQueue.length - 1]
    : state.direction;

  // Evitar marcha atrás instantánea
  if (newDir.x !== -lastDir.x || newDir.y !== -lastDir.y) {
    if (state.inputQueue.length < 2) {
      state.inputQueue.push(newDir);
    }
  }
}

/**
 * Añade obstáculos con advertencia (telegraphing) de nivel.
 */
export function addLevelObstaclesWithTelegraph(state, newLevel) {
  const newObsCoords = getLevelObstacles(newLevel);
  // Filtrar para no poner obstáculos donde ya está la serpiente o su cabeza inmediata
  const head = state.snake[0];
  const safeCoords = newObsCoords.filter(coord => {
    const onSnake = state.snake.some(s => s.x === coord.x && s.y === coord.y);
    const onFood = state.food && state.food.x === coord.x && state.food.y === coord.y;
    const isHeadNear = Math.abs(coord.x - head.x) <= 1 && Math.abs(coord.y - head.y) <= 1;
    return !onSnake && !onFood && !isHeadNear;
  });

  // Añadir con advertencia de 3 ticks (parpadeo seguro)
  safeCoords.forEach(c => {
    const exists = state.obstacles.some(o => o.x === c.x && o.y === c.y);
    if (!exists) {
      state.obstacles.push({ x: c.x, y: c.y, warningTicks: 3 });
    }
  });
}

/**
 * Ejecuta un paso del reloj del juego (tick).
 * @param {object} state
 * @param {number} deltaTimeMs
 * @param {boolean} isBoostActive
 * @returns {object} eventos ocurridos en el tick
 */
export function tickGame(state, deltaTimeMs = 140, isBoostActive = false) {
  state.events = [];
  if (state.isGameOver || state.isPaused) return state.events;

  const dtSec = deltaTimeMs / 1000;
  state.totalTimeElapsedSec += dtSec;

  // Actualizar temporizador en modo Contrarreloj
  if (state.mode === "time_attack") {
    state.timeRemainingSec = Math.max(0, state.timeRemainingSec - dtSec);
    if (state.timeRemainingSec <= 0) {
      state.isGameOver = true;
      state.events.push({ type: "game_over", reason: "timeout" });
      return state.events;
    }
  }

  // Actualizar Combo
  if (state.comboTimerSec > 0) {
    state.comboTimerSec = Math.max(0, state.comboTimerSec - dtSec);
    if (state.comboTimerSec === 0 && state.combo > 1) {
      state.combo = 1;
      state.events.push({ type: "combo_reset" });
    }
  }

  // Actualizar Power-ups activos
  if (state.activePowerups.cryoSec > 0) {
    state.activePowerups.cryoSec = Math.max(0, state.activePowerups.cryoSec - dtSec);
  }
  if (state.activePowerups.ghostSec > 0) {
    state.activePowerups.ghostSec = Math.max(0, state.activePowerups.ghostSec - dtSec);
  }

  // Actualizar vida útil de comida temporal
  if (state.food && state.food.lifespanSec !== null) {
    state.food.lifespanSec -= dtSec;
    if (state.food.lifespanSec <= 0) {
      placeFood(state, state.rng);
      state.events.push({ type: "food_expired" });
    }
  }

  // Actualizar telegraphing de obstáculos
  state.obstacles.forEach(o => {
    if (o.warningTicks > 0) {
      o.warningTicks -= 1;
      if (o.warningTicks === 0) {
        state.events.push({ type: "firewall_active", x: o.x, y: o.y });
      }
    }
  });

  // Procesar siguiente dirección de la cola
  if (state.inputQueue.length > 0) {
    const nextDir = state.inputQueue.shift();
    if (nextDir.x !== -state.direction.x || nextDir.y !== -state.direction.y) {
      state.direction = nextDir;
    }
  }

  // Calcular nueva posición de la cabeza
  let newHead = {
    x: state.snake[0].x + state.direction.x,
    y: state.snake[0].y + state.direction.y
  };

  const isGhostActive = state.activePowerups.ghostSec > 0;
  const isWrapAround = isGhostActive || state.mode === "zen" || state.mode === "time_attack";

  // Tratamiento de bordes perimetrales
  if (isWrapAround) {
    newHead.x = (newHead.x + GRID_SIZE) % GRID_SIZE;
    newHead.y = (newHead.y + GRID_SIZE) % GRID_SIZE;
    if (isGhostActive && (newHead.x === 0 || newHead.x === GRID_SIZE - 1 || newHead.y === 0 || newHead.y === GRID_SIZE - 1)) {
      state.events.push({ type: "ghost_warp" });
    }
  } else {
    if (newHead.x < 0 || newHead.x >= GRID_SIZE || newHead.y < 0 || newHead.y >= GRID_SIZE) {
      state.isGameOver = true;
      state.events.push({ type: "game_over", reason: "wall_hit", crashPos: { ...state.snake[0] } });
      return state.events;
    }
  }

  // Detección de auto-mordedura (bypassed si ghost)
  const selfHitIndex = state.snake.findIndex((s, idx) => idx > 0 && s.x === newHead.x && s.y === newHead.y);
  if (selfHitIndex !== -1 && !isGhostActive) {
    if (state.mode === "time_attack") {
      // En contrarreloj, recortar cola y penalizar tiempo
      state.snake = state.snake.slice(0, Math.max(3, selfHitIndex));
      state.timeRemainingSec = Math.max(0, state.timeRemainingSec - 5);
      state.combo = 1;
      state.events.push({ type: "tail_trimmed", penaltySec: 5 });
    } else {
      state.isGameOver = true;
      state.events.push({ type: "game_over", reason: "self_hit", crashPos: { ...newHead } });
      return state.events;
    }
  }

  // Detección de colisión con obstáculos (bypassed si ghost o si sigue en warning)
  const hitObstacle = state.obstacles.find(o => o.x === newHead.x && o.y === newHead.y && o.warningTicks <= 0);
  if (hitObstacle && !isGhostActive) {
    if (state.mode === "time_attack") {
      state.timeRemainingSec = Math.max(0, state.timeRemainingSec - 5);
      state.combo = 1;
      state.events.push({ type: "obstacle_hit_penalty", penaltySec: 5 });
    } else {
      state.isGameOver = true;
      state.events.push({ type: "game_over", reason: "obstacle_hit", crashPos: { ...newHead } });
      return state.events;
    }
  } else if (hitObstacle && isGhostActive) {
    state.events.push({ type: "ghost_through_wall" });
  }

  // Mover serpiente
  state.snake.unshift(newHead);

  // Comprobar comida o power-up
  if (state.food && newHead.x === state.food.x && newHead.y === state.food.y) {
    const eatenType = state.food.type;
    state.foodEatenCount += 1;

    // Calcular puntos con Combo y Dash
    const boostMultiplier = isBoostActive ? 2 : 1;
    let earnedPoints = 10 * state.level * boostMultiplier * state.combo;

    if (eatenType === "golden") {
      earnedPoints = 50 * state.combo * boostMultiplier;
      state.combo = Math.min(8, state.combo + 2);
      if (state.mode === "time_attack") {
        state.timeRemainingSec += 4.0;
      }
      state.events.push({ type: "eat_golden", points: earnedPoints });
    } else if (eatenType === "cryo") {
      earnedPoints = 20 * state.combo * boostMultiplier;
      state.activePowerups.cryoSec = 5.0;
      state.combo = Math.min(8, state.combo + 1);
      state.events.push({ type: "eat_cryo", points: earnedPoints });
    } else if (eatenType === "ghost") {
      earnedPoints = 25 * state.combo * boostMultiplier;
      state.activePowerups.ghostSec = 6.0;
      state.combo = Math.min(8, state.combo + 1);
      state.events.push({ type: "eat_ghost", points: earnedPoints });
    } else {
      // Nodo normal
      state.combo = Math.min(8, state.combo + 1);
      state.events.push({ type: "eat_data", points: earnedPoints });
    }

    state.comboTimerSec = state.COMBO_MAX_TIME_SEC;
    if (state.combo > state.maxCombo) {
      state.maxCombo = state.combo;
    }

    state.score += earnedPoints;

    // Progresión de nivel en modo Arcade y Daily
    if (state.mode === "arcade" || state.mode === "daily") {
      const nextLevel = Math.min(10, Math.floor(state.score / 75) + 1);
      if (nextLevel > state.level) {
        state.level = nextLevel;
        state.events.push({ type: "level_up", newLevel: state.level });
        if (state.mode === "arcade") {
          addLevelObstaclesWithTelegraph(state, state.level);
        }
      }
    }

    // Reponer comida
    placeFood(state, state.rng);
  } else {
    // Si no comió, quitar el segmento de la cola
    state.snake.pop();
  }

  // Ajustar velocidad según nivel y powerup cryo
  let baseSpeed = Math.max(55, 140 - (state.level * 9));
  if (state.activePowerups.cryoSec > 0) {
    baseSpeed = Math.floor(baseSpeed * 1.35); // Ralentiza un 35%
  }
  if (isBoostActive) {
    baseSpeed = Math.max(35, Math.floor(baseSpeed * 0.5)); // Duplica velocidad efectiva
  }
  state.tickIntervalMs = baseSpeed;

  return state.events;
}

/**
 * Genera el resumen visual de emojis para compartir el Reto Diario.
 */
export function generateDailySummary(dateStr, score, level, maxCombo, events = []) {
  const blocks = [];
  // Mapear eventos a emojis
  for (let i = 0; i < Math.min(10, events.length); i++) {
    const ev = events[i];
    if (ev.type === "eat_golden") blocks.push("🟡");
    else if (ev.type === "eat_cryo") blocks.push("❄️");
    else if (ev.type === "eat_ghost") blocks.push("👻");
    else if (ev.type === "eat_data") blocks.push("🟩");
  }
  if (blocks.length < 5) {
    blocks.push("🟩", "🟩", "🟡", "🟦");
  }
  const gridLine = blocks.slice(0, 10).join("");
  return `🐍 Neon Snake Daily #${dateStr}\n🏆 ${score} pts | Nivel ${level} | Max Combo x${maxCombo}\n${gridLine}\nhttps://datalaria.com/games/snake/`;
}
