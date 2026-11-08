// apps/snake/app.js
// Controlador Reactivo, Loop de Renderizado 60 FPS, Juice, PWA y Cyber-Card PNG
// Datalaria Neon Snake ("Cyberpunk Overdrive v2.0")

import {
  GRID_SIZE,
  MODES,
  NODES,
  SKINS,
  MEDALS,
  PROFILES,
  t,
  getSkin,
  getMode
} from "./catalog.js";

import {
  createSeededRng,
  createInitialGameState,
  queueInput,
  tickGame,
  generateDailySummary
} from "./engine.js";

import {
  initAudio,
  playSound,
  isMuted,
  toggleMute
} from "./audio.js";

import {
  fetchTopScores,
  saveScore,
  flushOfflineQueue,
  renderRankingListSafe,
  sanitizeAgentName
} from "./leaderboard.js";

// --- ESTADO GLOBAL DE LA APLICACIÓN ---
let currentLang = "es";
let currentTheme = "neon";
let currentProfileId = "hacker1";
let selectedModeId = "arcade";
let currentTab = "play";

let gameState = null;
let isBoostActive = false;
let isLoopRunning = false;
let animationFrameId = null;
let lastTimestamp = 0;
let dropAccumulator = 0;

// Sistema de Partículas y Juice
let particles = [];
let shakeTimer = 0;
let shakeMagnitude = 0;

// Canvas y Medidas
let canvas = null;
let ctx = null;
let TILE_SIZE = 20;

// PWA Deferred Prompt y Variables de Ciclo de Vida
let deferredInstallPrompt = null;
let isStandalone = false;
let swRefreshing = false;
let swRegistration = null;

// Ergonomía Móvil, Hit-Stop & Cuenta Atrás (INV-SNAKE-14)
let dpadEnabled = true;
try {
  const savedDpad = localStorage.getItem("datalaria_snake_dpad");
  if (savedDpad !== null) dpadEnabled = savedDpad !== "false";
} catch (e) {}

let isHitStop = false;
let hitStopPos = null;
let isCountdownActive = false;
let countdownText = "";
let countdownTimerId = null;

// Disparador de Vibración Háptica Nativa
function triggerHaptic(type) {
  if (isMuted()) return;
  if (typeof navigator === "undefined" || !navigator.vibrate) return;
  try {
    if (type === "eat") {
      navigator.vibrate(15);
    } else if (type === "levelup") {
      navigator.vibrate([30, 40, 30]);
    } else if (type === "crash") {
      navigator.vibrate(80);
    }
  } catch (e) {}
}

// --- GESTIÓN DE PERFILES Y ESTADÍSTICAS LOCALES ---
function getProfileStorageKey(profileId) {
  return `datalaria_snake_v2_stats_${profileId}`;
}

function loadProfileStats(profileId) {
  const defaultProf = PROFILES.find(p => p.id === profileId) || PROFILES[0];
  const defaults = {
    agentName: defaultProf.defaultAgent,
    highScore: 0,
    maxCombo: 1,
    maxLevel: 1,
    totalNodes: 0,
    dailyCompleted: 0,
    equippedSkin: "cyan_viper",
    unlockedSkins: ["cyan_viper"],
    medals: []
  };

  try {
    const raw = localStorage.getItem(getProfileStorageKey(profileId));
    if (raw) return { ...defaults, ...JSON.parse(raw) };
  } catch (e) {}
  return defaults;
}

function saveProfileStats(profileId, stats) {
  try {
    localStorage.setItem(getProfileStorageKey(profileId), JSON.stringify(stats));
  } catch (e) {}
}

let activeStats = loadProfileStats(currentProfileId);

// --- COMPROBACIÓN DE DESBLOQUEO DE SKINS Y MEDALLAS ---
function checkUnlocks(stats) {
  let anyNewSkin = false;
  let anyNewMedal = false;

  // 1. Skins
  Object.values(SKINS).forEach(skin => {
    if (!stats.unlockedSkins.includes(skin.id)) {
      if (skin.checkUnlock && skin.checkUnlock(stats)) {
        stats.unlockedSkins.push(skin.id);
        anyNewSkin = true;
        showToast(`${t("toast_skin_unlocked", currentLang)}: ${skin.name[currentLang]}`);
      }
    }
  });

  // 2. Medallas
  const unlockMedal = (id) => {
    if (!stats.medals.includes(id)) {
      stats.medals.push(id);
      anyNewMedal = true;
      playSound("record");
      showToast(`${t("toast_medal_unlocked", currentLang)}: ${MEDALS[id].name[currentLang]}`);
    }
  };

  if (stats.totalNodes >= 1) unlockMedal("first_hack");
  if (stats.maxCombo >= 5) unlockMedal("overclock");
  if (stats.maxLevel >= 5) unlockMedal("firewall_breaker");
  if (stats.dailyCompleted >= 1) unlockMedal("daily_hacker");
  if (stats.highScore >= 1500) unlockMedal("cyber_legend");

  stats.medalsCount = stats.medals.length;

  if (anyNewSkin || anyNewMedal) {
    saveProfileStats(currentProfileId, stats);
  }
}

// --- PARTÍCULAS VISUALES ---
class CyberParticle {
  constructor(x, y, color) {
    this.x = x;
    this.y = y;
    this.color = color;
    this.vx = (Math.random() - 0.5) * 8;
    this.vy = (Math.random() - 0.5) * 8;
    this.life = 1.0;
    this.decay = Math.random() * 0.04 + 0.02;
    this.size = Math.random() * 4 + 2;
  }
  update() {
    this.x += this.vx;
    this.y += this.vy;
    this.life -= this.decay;
  }
  draw(context) {
    context.save();
    context.globalAlpha = Math.max(0, this.life);
    context.fillStyle = this.color;
    context.shadowBlur = 8;
    context.shadowColor = this.color;
    context.beginPath();
    context.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    context.fill();
    context.restore();
  }
}

function spawnParticles(gridX, gridY, color = "#00f0ff", count = 10) {
  const px = gridX * TILE_SIZE + TILE_SIZE / 2;
  const py = gridY * TILE_SIZE + TILE_SIZE / 2;
  for (let i = 0; i < count; i++) {
    particles.push(new CyberParticle(px, py, color));
  }
}

function triggerScreenShake(magnitude = 6, durationMs = 180) {
  shakeMagnitude = magnitude;
  shakeTimer = durationMs;
}

// --- TOAST NOTIFICATIONS ---
export function showToast(message, duration = 3000) {
  const container = document.getElementById("toast-container");
  if (!container) return;
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(-10px)";
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// --- MODO JUEGO INMERSIVO Y ESCALADO DETERMINISTA DEL TABLERO ---
function setFocusPlayingMode(playing) {
  if (typeof document === "undefined") return;
  document.body.classList.toggle("is-playing", Boolean(playing));
  resizeCanvas();
  if (typeof requestAnimationFrame === "function") {
    requestAnimationFrame(resizeCanvas);
  }
}

function updateDpadUI() {
  const deck = document.getElementById("touch-controls-deck");
  if (deck) {
    deck.classList.toggle("dpad-disabled", !dpadEnabled);
  }
  const btn = document.getElementById("btn-toggle-dpad");
  if (btn) {
    btn.textContent = dpadEnabled ? t("btn_toggle_dpad_on", currentLang) : t("btn_toggle_dpad_off", currentLang);
  }
  const deckLabel = document.getElementById("dpad-deck-label");
  if (deckLabel) {
    deckLabel.textContent = dpadEnabled ? t("dpad_deck_mode_dpad", currentLang) : t("dpad_deck_mode_swipe", currentLang);
  }
  const swipeZone = document.getElementById("swipe-touchpad-zone");
  if (swipeZone) {
    swipeZone.classList.toggle("hidden", dpadEnabled);
  }
  resizeCanvas();
}

function resizeCanvas() {
  const wrapper = document.getElementById("game-canvas-wrapper");
  if (!wrapper || !canvas) return;

  const winW = window.innerWidth || 800;
  const winH = window.innerHeight || 700;
  const isTouchDevice = (typeof window !== "undefined") && (
    ("ontouchstart" in window) ||
    (navigator.maxTouchPoints > 0) ||
    (window.matchMedia && window.matchMedia("(pointer: coarse)").matches)
  );
  const showTouchControls = isTouchDevice || document.body.classList.contains("force-touch-controls") || winW < 1024;
  const isPlaying = document.body.classList.contains("is-playing");

  // Ancho disponible descontando márgenes mínimos laterales (máx 720px en escritorio/tablet)
  const isSmallMobile = winW < 600;
  const marginSide = isSmallMobile ? 8 : 24;
  const availW = Math.min(winW - marginSide, 720);

  // Espacio vertical reservado para HUD y controles táctiles / cabecera
  let reservedH;
  if (showTouchControls) {
    const touchAllowance = dpadEnabled ? 150 : 80;
    reservedH = isPlaying ? (60 + touchAllowance) : (180 + touchAllowance);
  } else {
    reservedH = isPlaying ? 85 : 180;
  }

  const minFloor = isSmallMobile ? 260 : 340;
  const availH = Math.max(minFloor, winH - reservedH);
  const rawSize = Math.min(availW, availH);

  // En móvil/tablet aprovechamos todo el espacio útil disponible de forma proporcional
  const boardSize = Math.max(260, Math.round(rawSize));

  document.documentElement.style.setProperty("--board-size", `${boardSize}px`);
  canvas.width = boardSize;
  canvas.height = boardSize;
  TILE_SIZE = boardSize / GRID_SIZE;
}

function drawGame() {
  if (!ctx || !canvas) return;

  ctx.save();

  // Screen shake
  if (shakeTimer > 0) {
    const offsetX = (Math.random() - 0.5) * shakeMagnitude;
    const offsetY = (Math.random() - 0.5) * shakeMagnitude;
    ctx.translate(offsetX, offsetY);
  }

  // Fondo
  ctx.fillStyle = currentTheme === "crt" ? "#020b04" : "#05070d";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Rejilla de fondo
  const gridColor = currentTheme === "crt" ? "rgba(0, 255, 102, 0.08)" : "rgba(0, 240, 255, 0.06)";
  ctx.strokeStyle = gridColor;
  ctx.lineWidth = 1;
  for (let i = 0; i <= GRID_SIZE; i++) {
    ctx.beginPath();
    ctx.moveTo(i * TILE_SIZE, 0);
    ctx.lineTo(i * TILE_SIZE, canvas.height);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(0, i * TILE_SIZE);
    ctx.lineTo(canvas.width, i * TILE_SIZE);
    ctx.stroke();
  }

  if (!gameState) {
    ctx.restore();
    return;
  }

  // 1. Obstáculos / Firewalls con Telegraphing
  gameState.obstacles.forEach(obs => {
    const x = obs.x * TILE_SIZE;
    const y = obs.y * TILE_SIZE;

    if (obs.warningTicks > 0) {
      // TELEGRAPHING: Aviso preventivo en ámbar parpadeante
      const flash = Math.floor(Date.now() / 150) % 2 === 0;
      ctx.strokeStyle = flash ? "#ffe600" : "rgba(255, 230, 0, 0.3)";
      ctx.lineWidth = 2;
      ctx.strokeRect(x + 2, y + 2, TILE_SIZE - 4, TILE_SIZE - 4);
      ctx.fillStyle = "#ffe600";
      ctx.font = `${Math.floor(TILE_SIZE * 0.65)}px sans-serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText("⚠️", x + TILE_SIZE / 2, y + TILE_SIZE / 2);
    } else {
      // Firewall activo y letal en rojo resplandeciente
      ctx.fillStyle = currentTheme === "crt" ? "#ff4444" : "#ff0033";
      ctx.shadowBlur = 10;
      ctx.shadowColor = "#ff0033";
      ctx.fillRect(x + 1, y + 1, TILE_SIZE - 2, TILE_SIZE - 2);
      ctx.shadowBlur = 0;

      // Núcleo de datos interno del firewall
      ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
      ctx.fillRect(x + TILE_SIZE * 0.3, y + TILE_SIZE * 0.3, TILE_SIZE * 0.4, TILE_SIZE * 0.4);
    }
  });

  // 2. Comida y Power-ups
  if (gameState.food) {
    const fx = gameState.food.x * TILE_SIZE + TILE_SIZE / 2;
    const fy = gameState.food.y * TILE_SIZE + TILE_SIZE / 2;
    const nodeDef = NODES[gameState.food.type] || NODES.data;

    // Pulso animado
    const pulse = Math.sin(Date.now() / 120) * 2;
    const radius = Math.max(3, (TILE_SIZE * 0.35) + pulse);

    ctx.save();
    ctx.shadowBlur = 16;
    ctx.shadowColor = nodeDef.glow;
    ctx.fillStyle = nodeDef.color;
    ctx.beginPath();
    ctx.arc(fx, fy, radius, 0, Math.PI * 2);
    ctx.fill();

    // Símbolo del nodo
    ctx.fillStyle = "#ffffff";
    ctx.font = `bold ${Math.floor(TILE_SIZE * 0.55)}px var(--font-cyber)`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(nodeDef.symbol, fx, fy);
    ctx.restore();
  }

  // 3. Serpiente con Skin equipada
  const equippedSkin = getSkin(activeStats.equippedSkin);
  const isGhostActive = gameState.activePowerups.ghostSec > 0;

  // Estela de la serpiente
  if (gameState.snake.length > 1) {
    ctx.beginPath();
    ctx.strokeStyle = equippedSkin.bodyColor;
    ctx.lineWidth = 3;
    const startX = gameState.snake[0].x * TILE_SIZE + TILE_SIZE / 2;
    const startY = gameState.snake[0].y * TILE_SIZE + TILE_SIZE / 2;
    ctx.moveTo(startX, startY);
    for (let i = 1; i < gameState.snake.length; i++) {
      ctx.lineTo(
        gameState.snake[i].x * TILE_SIZE + TILE_SIZE / 2,
        gameState.snake[i].y * TILE_SIZE + TILE_SIZE / 2
      );
    }
    ctx.stroke();
  }

  // Segmentos del cuerpo
  gameState.snake.forEach((segment, idx) => {
    const cx = segment.x * TILE_SIZE + TILE_SIZE / 2;
    const cy = segment.y * TILE_SIZE + TILE_SIZE / 2;

    ctx.save();
    if (isGhostActive) {
      ctx.globalAlpha = 0.55 + Math.sin(Date.now() / 80) * 0.2;
    }

    if (idx === 0) {
      // Cabeza direccional con ojos
      ctx.translate(cx, cy);
      const angle = Math.atan2(gameState.direction.y, gameState.direction.x);
      ctx.rotate(angle);

      ctx.fillStyle = equippedSkin.headColor;
      ctx.shadowBlur = isBoostActive ? 22 : 14;
      ctx.shadowColor = equippedSkin.glowColor;

      // Forma triangular aerodinámica
      ctx.beginPath();
      ctx.moveTo(TILE_SIZE * 0.48, 0);
      ctx.lineTo(-TILE_SIZE * 0.36, -TILE_SIZE * 0.36);
      ctx.lineTo(-TILE_SIZE * 0.2, 0);
      ctx.lineTo(-TILE_SIZE * 0.36, TILE_SIZE * 0.36);
      ctx.closePath();
      ctx.fill();

      // Ojos cibernéticos
      ctx.fillStyle = equippedSkin.eyeColor;
      ctx.beginPath();
      ctx.arc(TILE_SIZE * 0.1, -TILE_SIZE * 0.16, 2.5, 0, Math.PI * 2);
      ctx.arc(TILE_SIZE * 0.1, TILE_SIZE * 0.16, 2.5, 0, Math.PI * 2);
      ctx.fill();
    } else {
      // Segmentos del cuerpo con disminución progresiva hacia la cola
      const ratio = 1 - (idx / (gameState.snake.length + 6));
      const radius = (TILE_SIZE / 2 - 2) * Math.max(0.55, ratio);

      ctx.fillStyle = equippedSkin.bodyColor;
      ctx.beginPath();
      ctx.arc(cx, cy, radius, 0, Math.PI * 2);
      ctx.fill();

      // Núcleo brillante
      ctx.fillStyle = equippedSkin.headColor;
      ctx.beginPath();
      ctx.arc(cx, cy, radius * 0.35, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  });

  // 4. Partículas
  particles.forEach(p => p.draw(ctx));

  // 5. Destello dramático de impacto (Hit-Stop - INV-SNAKE-14)
  if (isHitStop && hitStopPos) {
    ctx.save();
    ctx.fillStyle = "rgba(255, 0, 122, 0.75)";
    ctx.shadowBlur = 24;
    ctx.shadowColor = "#ff007a";
    ctx.fillRect(hitStopPos.x * TILE_SIZE - 4, hitStopPos.y * TILE_SIZE - 4, TILE_SIZE + 8, TILE_SIZE + 8);
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 3;
    ctx.strokeRect(hitStopPos.x * TILE_SIZE - 6, hitStopPos.y * TILE_SIZE - 6, TILE_SIZE + 12, TILE_SIZE + 12);
    ctx.restore();
  }

  // 6. Cuenta atrás animada 3 - 2 - 1 - HACK!
  if (isCountdownActive && countdownText) {
    ctx.save();
    ctx.fillStyle = "rgba(5, 7, 13, 0.55)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.font = `bold ${Math.floor(canvas.width * 0.2)}px 'Orbitron', monospace`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    const isHack = countdownText.includes("HACK") || countdownText.includes("¡");
    ctx.fillStyle = isHack ? "#ffe600" : "#00f0ff";
    ctx.shadowColor = isHack ? "#ffe600" : "#00f0ff";
    ctx.shadowBlur = 30;

    ctx.fillText(countdownText, canvas.width / 2, canvas.height / 2);
    ctx.restore();
  }

  ctx.restore();
}

// --- ACTUALIZACIÓN DE HUD Y ESTADOS ---
function updateHUD() {
  if (!gameState) return;

  const scoreEl = document.getElementById("hud-score");
  const levelEl = document.getElementById("hud-level");
  const timeEl = document.getElementById("hud-time");
  const comboEl = document.getElementById("hud-combo");
  const comboBar = document.getElementById("combo-bar-fill");

  if (scoreEl) scoreEl.textContent = gameState.score.toLocaleString();
  if (levelEl) {
    if (gameState.mode === "time_attack") {
      levelEl.textContent = "⏱️ 90s";
    } else {
      levelEl.textContent = `${gameState.level}/10`;
    }
  }

  if (timeEl) {
    if (gameState.mode === "time_attack") {
      timeEl.textContent = `${Math.ceil(gameState.timeRemainingSec)}s`;
    } else {
      timeEl.textContent = `${Math.floor(gameState.totalTimeElapsedSec)}s`;
    }
  }

  if (comboEl) {
    comboEl.textContent = `🔥 x${gameState.combo}`;
  }

  if (comboBar) {
    const pct = (gameState.comboTimerSec / gameState.COMBO_MAX_TIME_SEC) * 100;
    comboBar.style.width = `${Math.max(0, Math.min(100, pct))}%`;
  }
}

// --- BUCLE PRINCIPAL DE JUEGO (GAME LOOP) ---
function gameLoop(timestamp) {
  if (!lastTimestamp) lastTimestamp = timestamp;
  const delta = timestamp - lastTimestamp;
  lastTimestamp = timestamp;

  // Actualizar partículas
  particles.forEach((p, idx) => {
    p.update();
    if (p.life <= 0) particles.splice(idx, 1);
  });

  // Screen shake decay
  if (shakeTimer > 0) {
    shakeTimer = Math.max(0, shakeTimer - delta);
  }

  if (gameState && !gameState.isGameOver && !gameState.isPaused) {
    dropAccumulator += delta;
    if (dropAccumulator >= gameState.tickIntervalMs) {
      dropAccumulator = 0;
      const events = tickGame(gameState, gameState.tickIntervalMs, isBoostActive);

      // Procesar eventos sonoros y partículas
      events.forEach(ev => {
        if (ev.type === "eat_data") {
          playSound("eat", { combo: gameState.combo });
          triggerHaptic("eat");
          spawnParticles(gameState.snake[0].x, gameState.snake[0].y, "#00f0ff", 8);
          activeStats.totalNodes += 1;
        } else if (ev.type === "eat_golden") {
          playSound("golden");
          triggerHaptic("eat");
          spawnParticles(gameState.snake[0].x, gameState.snake[0].y, "#ffe600", 16);
          triggerScreenShake(4, 120);
          activeStats.totalNodes += 1;
        } else if (ev.type === "eat_cryo") {
          playSound("cryo");
          triggerHaptic("eat");
          spawnParticles(gameState.snake[0].x, gameState.snake[0].y, "#38bdf8", 12);
          activeStats.totalNodes += 1;
        } else if (ev.type === "eat_ghost") {
          playSound("ghost");
          triggerHaptic("eat");
          spawnParticles(gameState.snake[0].x, gameState.snake[0].y, "#10b981", 12);
          activeStats.totalNodes += 1;
        } else if (ev.type === "level_up") {
          playSound("levelup");
          triggerHaptic("levelup");
          showToast(`🚀 ${t("level_label", currentLang)} ${ev.newLevel}!`);
          triggerScreenShake(5, 160);
        } else if (ev.type === "game_over") {
          handleHitStopAndGameOver(ev.crashPos || gameState.snake[0]);
        }
      });

      // Actualizar récord en memoria de perfil
      if (gameState.score > activeStats.highScore) {
        activeStats.highScore = gameState.score;
      }
      if (gameState.maxCombo > activeStats.maxCombo) {
        activeStats.maxCombo = gameState.maxCombo;
      }
      if (gameState.level > activeStats.maxLevel) {
        activeStats.maxLevel = gameState.level;
      }

      checkUnlocks(activeStats);
      updateHUD();
    }
  }

  drawGame();
  animationFrameId = requestAnimationFrame(gameLoop);
}

// --- HIT-STOP DE COLISIÓN (INV-SNAKE-14) ---
function handleHitStopAndGameOver(crashPos) {
  playSound("die");
  triggerHaptic("crash");
  triggerScreenShake(14, 400);

  isHitStop = true;
  hitStopPos = crashPos ? { ...crashPos } : { ...gameState.snake[0] };
  gameState.isPaused = true;

  // Pausa dramática de 450 ms reteniendo el fotograma antes de desplegar el modal
  setTimeout(() => {
    isHitStop = false;
    hitStopPos = null;
    handleGameOver();
  }, 450);
}

// --- GESTIÓN DE GAME OVER ASÍNCRONO SEGURO ---
async function handleGameOver() {
  setFocusPlayingMode(false);

  const overlay = document.getElementById("gameover-overlay");
  const title = document.getElementById("gameover-title");
  const subtitle = document.getElementById("gameover-subtitle");
  const scoreDisplay = document.getElementById("gameover-final-score");
  const shareDailyBtn = document.getElementById("btn-share-daily");

  if (title) title.textContent = t("game_over_title", currentLang);
  if (subtitle) subtitle.textContent = t("saving_score", currentLang);
  if (scoreDisplay) scoreDisplay.textContent = gameState.score.toLocaleString();
  if (shareDailyBtn) shareDailyBtn.classList.toggle("hidden", gameState.mode !== "daily");

  if (overlay) {
    overlay.classList.remove("is-inspecting");
    overlay.classList.remove("hidden");
  }

  const inspectSpan = document.querySelector("#btn-inspect-board span");
  if (inspectSpan) inspectSpan.textContent = t("btn_inspect_board", currentLang);

  // Si es modo Daily y no se había marcado completado
  if (gameState.mode === "daily") {
    activeStats.dailyCompleted = (activeStats.dailyCompleted || 0) + 1;
  }

  saveProfileStats(currentProfileId, activeStats);

  // Guardar puntuación en Supabase con cliente fetch seguro
  const res = await saveScore(activeStats.agentName, gameState.score);
  if (subtitle) {
    if (res.queued) {
      subtitle.textContent = t("score_offline_queued", currentLang);
    } else {
      subtitle.textContent = t("score_saved", currentLang);
    }
  }
}

// --- GENERADOR DE CYBER-CARD EN ALTA RESOLUCIÓN (PNG) ---
export function downloadCyberCard() {
  showToast(t("card_generating", currentLang));

  const offCanvas = document.createElement("canvas");
  offCanvas.width = 1200;
  offCanvas.height = 630;
  const octx = offCanvas.getContext("2d");

  // 1. Fondo degradado Cyberpunk
  const bgGrad = octx.createLinearGradient(0, 0, 1200, 630);
  bgGrad.addColorStop(0, "#05070d");
  bgGrad.addColorStop(0.5, "#0b1224");
  bgGrad.addColorStop(1, "#120820");
  octx.fillStyle = bgGrad;
  octx.fillRect(0, 0, 1200, 630);

  // 2. Rejilla cibernética
  octx.strokeStyle = "rgba(0, 240, 255, 0.08)";
  octx.lineWidth = 1;
  for (let x = 0; x <= 1200; x += 40) {
    octx.beginPath(); octx.moveTo(x, 0); octx.lineTo(x, 630); octx.stroke();
  }
  for (let y = 0; y <= 630; y += 40) {
    octx.beginPath(); octx.moveTo(0, y); octx.lineTo(1200, y); octx.stroke();
  }

  // 3. Orla doble Neón
  octx.strokeStyle = "#00f0ff";
  octx.lineWidth = 3;
  octx.strokeRect(30, 30, 1140, 570);
  octx.strokeStyle = "rgba(255, 0, 122, 0.5)";
  octx.lineWidth = 1;
  octx.strokeRect(38, 38, 1124, 554);

  // 4. Encabezados
  octx.fillStyle = "#00f0ff";
  octx.font = "bold 24px 'Orbitron', 'Courier New', monospace";
  octx.fillText("DATALARIA CYBER-ARCADE NETWORK", 70, 85);

  octx.fillStyle = "#ffffff";
  octx.font = "bold 46px 'Orbitron', 'Courier New', monospace";
  octx.fillText("NEON SNAKE: CYBER-AGENT RECORD", 70, 145);

  // 5. Datos del Agente
  const safeName = sanitizeAgentName(activeStats.agentName);
  octx.fillStyle = "#ffe600";
  octx.font = "bold 32px 'JetBrains Mono', monospace";
  octx.fillText(`AGENTE: ${safeName}`, 70, 220);

  const equippedSkin = getSkin(activeStats.equippedSkin);
  octx.fillStyle = "#94a3b8";
  octx.font = "22px 'Inter', sans-serif";
  octx.fillText(`Skin Activa: ${equippedSkin.name[currentLang]}`, 70, 260);

  // 6. Tarjetas de Estadísticas (KPIs)
  const drawStatBox = (x, y, label, val, color) => {
    octx.fillStyle = "rgba(18, 24, 43, 0.8)";
    octx.strokeStyle = color;
    octx.lineWidth = 1.5;
    octx.fillRect(x, y, 220, 110);
    octx.strokeRect(x, y, 220, 110);

    octx.fillStyle = "#94a3b8";
    octx.font = "14px 'Orbitron', monospace";
    octx.fillText(label, x + 20, y + 36);

    octx.fillStyle = color;
    octx.font = "bold 34px 'JetBrains Mono', monospace";
    octx.fillText(val, x + 20, y + 84);
  };

  drawStatBox(70, 310, "RÉCORD PUNTOS", activeStats.highScore.toLocaleString(), "#00f0ff");
  drawStatBox(310, 310, "MAX COMBO", `x${activeStats.maxCombo}`, "#ff007a");
  drawStatBox(550, 310, "NIVEL MÁXIMO", `${activeStats.maxLevel}`, "#ffe600");
  drawStatBox(790, 310, "NODOS DATOS", `${activeStats.totalNodes}`, "#00ff66");

  // 7. Medallas conseguidas
  octx.fillStyle = "#f0f6fc";
  octx.font = "bold 18px 'Inter', sans-serif";
  octx.fillText("Medallas Desbloqueadas:", 70, 470);

  const medalEmojis = activeStats.medals.map(m => MEDALS[m]?.icon || "⭐").join(" ");
  octx.font = "28px sans-serif";
  octx.fillText(medalEmojis || "Ninguna todavía (¡sigue hackeando!)", 70, 515);

  // 8. Sello Oficial Datalaria Arcade
  octx.save();
  octx.translate(1040, 480);
  octx.strokeStyle = "#00f0ff";
  octx.lineWidth = 2;
  octx.beginPath();
  octx.arc(0, 0, 55, 0, Math.PI * 2);
  octx.stroke();

  octx.fillStyle = "#00f0ff";
  octx.font = "bold 10px 'Orbitron', monospace";
  octx.textAlign = "center";
  octx.fillText("DATALARIA", 0, -15);
  octx.fillText("VERIFIED", 0, 5);
  octx.fillText("EXCELLENCE", 0, 22);
  octx.restore();

  // Fecha
  octx.fillStyle = "#64748b";
  octx.font = "16px 'JetBrains Mono', monospace";
  octx.textAlign = "left";
  octx.fillText(`Emisión: ${new Date().toISOString().split("T")[0]} · datalaria.com/games/snake/`, 70, 575);

  // Descarga directa
  const dataUrl = offCanvas.toDataURL("image/png");
  const link = document.createElement("a");
  link.download = `cyber_agent_${safeName.toLowerCase().replace(/\s+/g, "_")}_record.png`;
  link.href = dataUrl;
  link.click();
  showToast(t("card_downloaded", currentLang));
}

// --- INICIALIZACIÓN Y CONTROLADORES ---
export function initGameApp() {
  canvas = document.getElementById("gameCanvas");
  if (canvas) {
    ctx = canvas.getContext("2d");
  }

  // Detectar idioma desde URL, localStorage o navegador
  const params = new URLSearchParams(window.location.search);
  const langParam = params.get("lang");
  if (langParam === "es" || langParam === "en") {
    currentLang = langParam;
  } else {
    currentLang = (navigator.language || "").startsWith("en") ? "en" : "es";
  }

  // Detectar tema
  try {
    const savedTheme = localStorage.getItem("pref-theme") || "neon";
    currentTheme = savedTheme === "crt" ? "crt" : "neon";
    document.documentElement.setAttribute("data-theme", currentTheme);
  } catch (e) {}

  initAudio();
  setupUI();
  setupEventListeners();
  resizeCanvas();

  // Iniciar Loop
  if (!isLoopRunning) {
    isLoopRunning = true;
    lastTimestamp = performance.now();
    animationFrameId = requestAnimationFrame(gameLoop);
  }

  // Registrar Service Worker PWA
  setupPWA();
}

function startNewGame() {
  if (countdownTimerId) {
    clearInterval(countdownTimerId);
    countdownTimerId = null;
  }
  isCountdownActive = false;
  countdownText = "";
  isHitStop = false;
  hitStopPos = null;

  const nameInput = document.getElementById("username-input");
  if (nameInput) {
    const entered = sanitizeAgentName(nameInput.value);
    activeStats.agentName = entered;
    saveProfileStats(currentProfileId, activeStats);
  }

  let rng = Math.random;
  if (selectedModeId === "daily") {
    const today = new Date().toISOString().split("T")[0];
    rng = createSeededRng(today);
  }

  gameState = createInitialGameState(selectedModeId, {}, rng);

  // Ocultar overlays y activar modo inmersivo maximizado
  document.getElementById("start-overlay")?.classList.add("hidden");
  const goOv = document.getElementById("gameover-overlay");
  if (goOv) {
    goOv.classList.remove("is-inspecting");
    goOv.classList.add("hidden");
  }
  document.getElementById("pause-overlay")?.classList.add("hidden");

  setFocusPlayingMode(true);
  updateHUD();
}

// --- VISTAS Y PESTAÑAS ---
function switchTab(tabId) {
  currentTab = tabId;

  // Si salimos de la pestaña Jugar mientras hay partida activa, pausar y mostrar barra
  if (tabId !== "play") {
    if (gameState && !gameState.isGameOver && !gameState.isPaused) {
      gameState.isPaused = true;
      document.getElementById("pause-overlay")?.classList.remove("hidden");
    }
    setFocusPlayingMode(false);
  } else {
    const activelyPlaying = Boolean(gameState && !gameState.isGameOver && !gameState.isPaused);
    setFocusPlayingMode(activelyPlaying);
  }

  // Actualizar botones del deck
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.tab === tabId);
  });

  // Mostrar / Ocultar paneles
  const playWrapper = document.getElementById("game-view-wrapper");
  const rankingPanel = document.getElementById("ranking-panel");
  const skinsPanel = document.getElementById("skins-panel");
  const medalsPanel = document.getElementById("medals-panel");
  const helpPanel = document.getElementById("help-panel");

  if (playWrapper) playWrapper.classList.toggle("hidden", tabId !== "play");
  if (rankingPanel) rankingPanel.classList.toggle("hidden", tabId !== "ranking");
  if (skinsPanel) skinsPanel.classList.toggle("hidden", tabId !== "skins");
  if (medalsPanel) medalsPanel.classList.toggle("hidden", tabId !== "medals");
  if (helpPanel) helpPanel.classList.toggle("hidden", tabId !== "help");

  if (tabId === "ranking") loadAndRenderRanking();
  if (tabId === "skins") renderSkinsHangar();
  if (tabId === "medals") renderMedalsView();
}

// --- RENDERIZADO DEL HANGAR DE SKINS ---
function renderSkinsHangar() {
  const container = document.getElementById("skins-grid");
  if (!container) return;
  container.innerHTML = "";

  Object.values(SKINS).forEach(skin => {
    const card = document.createElement("div");
    card.className = "skin-card";
    const isEquipped = activeStats.equippedSkin === skin.id;
    const isUnlocked = activeStats.unlockedSkins.includes(skin.id);

    if (isEquipped) card.classList.add("equipped");

    // Mini Canvas de Preview
    const pCanvas = document.createElement("canvas");
    pCanvas.className = "skin-preview-canvas";
    pCanvas.width = 64;
    pCanvas.height = 64;
    const pctx = pCanvas.getContext("2d");

    // Dibujar preview de la skin
    pctx.fillStyle = "#0c101d";
    pctx.fillRect(0, 0, 64, 64);
    pctx.fillStyle = skin.bodyColor;
    pctx.beginPath(); pctx.arc(20, 32, 8, 0, Math.PI * 2); pctx.fill();
    pctx.beginPath(); pctx.arc(33, 32, 9, 0, Math.PI * 2); pctx.fill();

    pctx.fillStyle = skin.headColor;
    pctx.shadowBlur = 8; pctx.shadowColor = skin.glowColor;
    pctx.beginPath(); pctx.arc(46, 32, 10, 0, Math.PI * 2); pctx.fill();
    pctx.shadowBlur = 0;

    card.appendChild(pCanvas);

    const nameEl = document.createElement("h4");
    nameEl.className = "skin-name";
    nameEl.textContent = skin.name[currentLang];
    card.appendChild(nameEl);

    const descEl = document.createElement("p");
    descEl.className = "skin-desc";
    descEl.textContent = skin.desc[currentLang];
    card.appendChild(descEl);

    if (isEquipped) {
      const tag = document.createElement("span");
      tag.className = "skin-status-tag";
      tag.textContent = t("skins_equipped", currentLang);
      card.appendChild(tag);
    } else if (isUnlocked) {
      const btn = document.createElement("button");
      btn.className = "ctrl-btn skin-equip-btn";
      btn.textContent = t("skins_equip_btn", currentLang);
      btn.onclick = () => {
        activeStats.equippedSkin = skin.id;
        saveProfileStats(currentProfileId, activeStats);
        renderSkinsHangar();
        showToast(`${t("skins_equipped", currentLang)}: ${skin.name[currentLang]}`);
      };
      card.appendChild(btn);
    } else {
      const reqEl = document.createElement("span");
      reqEl.className = "skin-req-tag";
      reqEl.textContent = `🔒 ${skin.reqDesc[currentLang]}`;
      card.appendChild(reqEl);
    }

    container.appendChild(card);
  });
}

// --- RENDERIZADO DE MEDALLAS ---
function renderMedalsView() {
  const container = document.getElementById("medals-grid");
  if (!container) return;
  container.innerHTML = "";

  Object.values(MEDALS).forEach(medal => {
    const isUnlocked = activeStats.medals.includes(medal.id);
    const card = document.createElement("div");
    card.className = `medal-card ${isUnlocked ? "unlocked" : "locked"}`;

    const icon = document.createElement("div");
    icon.className = "medal-icon";
    icon.textContent = medal.icon;
    card.appendChild(icon);

    const info = document.createElement("div");
    info.className = "medal-info";

    const title = document.createElement("h4");
    title.textContent = medal.name[currentLang];
    info.appendChild(title);

    const desc = document.createElement("p");
    desc.textContent = medal.desc[currentLang];
    info.appendChild(desc);

    card.appendChild(info);
    container.appendChild(card);
  });
}

// --- CARGA Y RENDERIZADO DEL RANKING ---
async function loadAndRenderRanking() {
  const listEl = document.getElementById("ranking-list");
  if (!listEl) return;

  // Actualizar KPIs personales en la cabecera del Ranking
  const bestEl = document.getElementById("ranking-kpi-best");
  const comboEl = document.getElementById("ranking-kpi-combo");
  const statusEl = document.getElementById("ranking-kpi-status");
  if (bestEl) bestEl.textContent = `${(activeStats.highScore || 0).toLocaleString()} PTS`;
  if (comboEl) comboEl.textContent = `x${activeStats.maxCombo || 1}`;

  listEl.innerHTML = `<li class="ranking-empty">${t("ranking_loading", currentLang)}</li>`;

  const { scores, fromCache } = await fetchTopScores(20);
  if (statusEl) {
    statusEl.textContent = fromCache ? "💾 CACHE" : t("ranking_online", currentLang);
  }
  renderRankingListSafe(listEl, scores, activeStats.agentName, t("ranking_you_badge", currentLang), t("ranking_offline_badge", currentLang));
}

// --- SETUP DE LA UI Y TEXTOS I18N ---
function setupUI() {
  // Traducir todos los elementos marcados con data-i18n
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.dataset.i18n;
    el.textContent = t(key, currentLang);
  });

  // Actualizar inputs y placeholders
  const nameInput = document.getElementById("username-input");
  if (nameInput) {
    nameInput.placeholder = t("agent_name_placeholder", currentLang);
    nameInput.value = activeStats.agentName || "Neo";
  }

  // Actualizar botón de sonido
  const muteBtn = document.getElementById("btn-mute");
  if (muteBtn) {
    muteBtn.textContent = isMuted() ? "🔇" : "🔊";
  }

  // Actualizar selector de perfiles
  const profSelect = document.getElementById("profile-select");
  if (profSelect) {
    profSelect.value = currentProfileId;
  }

  // Actualizar enlaces canónicos de cabecera con el idioma activo
  const backBtn = document.getElementById("btn-back-datalaria") || document.querySelector(".btn-back");
  if (backBtn) backBtn.href = `/${currentLang}/apps/`;

  const sheetLink = document.getElementById("link-nav-sheet");
  if (sheetLink) sheetLink.href = `/${currentLang}/apps/snake/`;

  const tutorialLink = document.getElementById("link-nav-tutorial");
  if (tutorialLink) tutorialLink.href = `/${currentLang}/posts/game_snake/`;

  const kitsLink = document.getElementById("link-nav-kits");
  if (kitsLink) kitsLink.href = currentLang === "en" ? "/en/resources/" : "/es/recursos/";

  // Actualizar estado del botón D-Pad (INV-SNAKE-14)
  updateDpadUI();
}

// --- CONFIGURACIÓN DE EVENT LISTENERS ---
function setupEventListeners() {
  window.addEventListener("resize", resizeCanvas);

  // Selector de perfiles familiares
  const profSelect = document.getElementById("profile-select");
  if (profSelect) {
    profSelect.addEventListener("change", (e) => {
      currentProfileId = e.target.value;
      activeStats = loadProfileStats(currentProfileId);
      setupUI();
      if (currentTab === "ranking") loadAndRenderRanking();
      if (currentTab === "skins") renderSkinsHangar();
      if (currentTab === "medals") renderMedalsView();
      showToast(`Perfil: ${activeStats.agentName}`);
    });
  }

  // Selector de idioma ES / EN
  const langToggle = document.getElementById("btn-lang-toggle");
  if (langToggle) {
    langToggle.addEventListener("click", () => {
      currentLang = currentLang === "es" ? "en" : "es";
      setupUI();
      if (currentTab === "ranking") loadAndRenderRanking();
      if (currentTab === "skins") renderSkinsHangar();
      if (currentTab === "medals") renderMedalsView();
    });
  }

  // Conmutador de Sonido Mute
  const muteBtn = document.getElementById("btn-mute");
  if (muteBtn) {
    muteBtn.addEventListener("click", () => {
      const muted = toggleMute();
      muteBtn.textContent = muted ? "🔇" : "🔊";
      showToast(muted ? "Audio Silenciado" : "Audio Activado");
    });
  }

  // Conmutador de Tema Neón / CRT
  const themeBtn = document.getElementById("btn-theme-toggle");
  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      currentTheme = currentTheme === "neon" ? "crt" : "neon";
      document.documentElement.setAttribute("data-theme", currentTheme);
      try { localStorage.setItem("pref-theme", currentTheme); } catch (e) {}
      showToast(`Tema: ${currentTheme.toUpperCase()}`);
    });
  }

  // Conmutador Táctil Ergonómico D-Pad vs Full-Swipe (INV-SNAKE-14)
  const toggleDpadMode = () => {
    dpadEnabled = !dpadEnabled;
    try { localStorage.setItem("datalaria_snake_dpad", dpadEnabled ? "true" : "false"); } catch (e) {}
    updateDpadUI();
    showToast(dpadEnabled ? t("toast_dpad_enabled", currentLang) : t("toast_swipe_mode", currentLang));
  };
  document.getElementById("btn-toggle-dpad")?.addEventListener("click", toggleDpadMode);
  document.getElementById("btn-toggle-dpad-deck")?.addEventListener("click", toggleDpadMode);

  // Inspección de Tablero en Game Over (INV-SNAKE-14)
  const toggleInspectBoard = (forceState) => {
    const goOverlay = document.getElementById("gameover-overlay");
    if (!goOverlay) return;
    const isInspecting = typeof forceState === "boolean" ? forceState : !goOverlay.classList.contains("is-inspecting");
    goOverlay.classList.toggle("is-inspecting", isInspecting);
    const inspectBtn = document.getElementById("btn-inspect-board");
    if (inspectBtn) {
      inspectBtn.textContent = isInspecting ? t("btn_restore_overlay", currentLang) : t("btn_inspect_board", currentLang);
    }
    // En modo inspección mantenemos ocultos cabecera y nav para no recortar el tablero
    if (isInspecting) {
      document.body.classList.add("is-playing");
    } else {
      document.body.classList.remove("is-playing");
    }
    resizeCanvas();
  };

  document.getElementById("btn-inspect-board")?.addEventListener("click", () => toggleInspectBoard());
  document.getElementById("btn-inspect-close")?.addEventListener("click", () => toggleInspectBoard(false));
  document.getElementById("btn-inspect-retry")?.addEventListener("click", () => {
    toggleInspectBoard(false);
    startNewGame();
  });
  document.getElementById("gameover-overlay")?.addEventListener("click", (e) => {
    const goOverlay = document.getElementById("gameover-overlay");
    if (goOverlay && goOverlay.classList.contains("is-inspecting") && !e.target.closest("button")) {
      toggleInspectBoard(false);
    }
  });

  // Pestañas del Deck
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });

  // Selector de modos en pantalla de Start
  document.querySelectorAll(".mode-card").forEach(card => {
    card.addEventListener("click", () => {
      document.querySelectorAll(".mode-card").forEach(c => c.classList.remove("selected"));
      card.classList.add("selected");
      selectedModeId = card.dataset.mode;
    });
  });

  // Botones Iniciar / Reiniciar / Reanudar / Pausar
  document.getElementById("btn-start-game")?.addEventListener("click", startNewGame);
  document.getElementById("btn-restart-game")?.addEventListener("click", startNewGame);
  document.getElementById("btn-restart-pause")?.addEventListener("click", startNewGame);
  document.getElementById("btn-hud-pause")?.addEventListener("click", togglePause);
  document.getElementById("btn-refresh-ranking")?.addEventListener("click", loadAndRenderRanking);

  document.getElementById("btn-resume-game")?.addEventListener("click", () => {
    startResumeCountdown();
  });

  // Botón Ver Ranking desde Start / GameOver
  const openRanking = () => switchTab("ranking");
  document.getElementById("btn-view-ranking-start")?.addEventListener("click", openRanking);
  document.getElementById("btn-view-ranking-gameover")?.addEventListener("click", openRanking);

  // Botón Descargar Cyber-Card (PNG)
  document.getElementById("btn-download-cybercard")?.addEventListener("click", downloadCyberCard);
  document.getElementById("btn-download-card-medals")?.addEventListener("click", downloadCyberCard);

  // Botón Compartir Reto Diario
  document.getElementById("btn-share-daily")?.addEventListener("click", () => {
    if (!gameState) return;
    const today = new Date().toISOString().split("T")[0];
    const text = generateDailySummary(today, gameState.score, gameState.level, gameState.maxCombo, gameState.events);
    navigator.clipboard.writeText(text).then(() => {
      showToast(t("daily_copied", currentLang));
    }).catch(() => {
      showToast(t("daily_copied", currentLang));
    });
  });

  // Controles de Teclado
  window.addEventListener("keydown", (e) => {
    if (isCountdownActive || isHitStop) return;

    if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "].includes(e.key)) {
      if (currentTab === "play" && document.activeElement?.id !== "username-input") {
        e.preventDefault();
      }
    }

    if (document.activeElement?.id === "username-input") {
      if (e.key === "Enter") startNewGame();
      return;
    }

    if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") {
      if (gameState) queueInput(gameState, { x: 0, y: -1 });
    } else if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") {
      if (gameState) queueInput(gameState, { x: 0, y: 1 });
    } else if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") {
      if (gameState) queueInput(gameState, { x: -1, y: 0 });
    } else if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") {
      if (gameState) queueInput(gameState, { x: 1, y: 0 });
    } else if (e.key === " " || e.key === "Shift") {
      if (gameState && gameState.isPaused) {
        togglePause();
      } else {
        // Hyper-Dash
        isBoostActive = true;
        playSound("dash");
      }
    } else if (e.key === "p" || e.key === "P" || e.key === "Escape") {
      togglePause();
    } else if (e.key === "m" || e.key === "M") {
      const muted = toggleMute();
      const mb = document.getElementById("btn-mute");
      if (mb) mb.textContent = muted ? "🔇" : "🔊";
    } else if (e.key === "t" || e.key === "T") {
      currentTheme = currentTheme === "neon" ? "crt" : "neon";
      document.documentElement.setAttribute("data-theme", currentTheme);
    }
  });

  window.addEventListener("keyup", (e) => {
    if (e.key === " " || e.key === "Shift") {
      isBoostActive = false;
    }
  });

  // Controles Táctiles: D-Pad en Pantalla
  document.querySelectorAll(".d-pad-btn[data-dir]").forEach(btn => {
    const handleDir = (ev) => {
      if (ev && ev.cancelable) ev.preventDefault();
      if (!gameState || isCountdownActive || isHitStop) return;
      const d = btn.dataset.dir;
      if (d === "up") queueInput(gameState, { x: 0, y: -1 });
      else if (d === "down") queueInput(gameState, { x: 0, y: 1 });
      else if (d === "left") queueInput(gameState, { x: -1, y: 0 });
      else if (d === "right") queueInput(gameState, { x: 1, y: 0 });
    };
    btn.addEventListener("touchstart", handleDir, { passive: false });
    btn.addEventListener("mousedown", handleDir);
  });

  // Botón Pausa táctil funcional
  document.getElementById("btn-touch-pause")?.addEventListener("click", togglePause);

  // Botones Boost táctil (Hyper-Dash): Soporte para botón en D-Pad y botón en Swipe Touchpad
  const bindBoostTouch = (el) => {
    if (!el) return;
    const startBoost = (ev) => {
      if (ev && ev.cancelable) ev.preventDefault();
      isBoostActive = true;
      playSound("dash");
    };
    const endBoost = (ev) => {
      if (ev && ev.cancelable) ev.preventDefault();
      isBoostActive = false;
    };
    el.addEventListener("touchstart", startBoost, { passive: false });
    el.addEventListener("touchend", endBoost, { passive: false });
    el.addEventListener("mousedown", startBoost);
    el.addEventListener("mouseup", endBoost);
    el.addEventListener("mouseleave", endBoost);
  };
  bindBoostTouch(document.getElementById("btn-touch-boost"));
  bindBoostTouch(document.getElementById("btn-touch-boost-swipe"));

  // Gestos Swipe sobre el Canvas y sobre la Zona Touchpad
  let touchStartX = 0;
  let touchStartY = 0;
  const handleTouchStart = (e) => {
    touchStartX = e.changedTouches[0].screenX;
    touchStartY = e.changedTouches[0].screenY;
  };
  const handleTouchEnd = (e) => {
    if (!gameState || isCountdownActive || isHitStop) return;
    const dx = e.changedTouches[0].screenX - touchStartX;
    const dy = e.changedTouches[0].screenY - touchStartY;
    if (Math.abs(dx) > Math.abs(dy)) {
      if (Math.abs(dx) > 25) {
        queueInput(gameState, dx > 0 ? { x: 1, y: 0 } : { x: -1, y: 0 });
      }
    } else {
      if (Math.abs(dy) > 25) {
        queueInput(gameState, dy > 0 ? { x: 0, y: 1 } : { x: 0, y: -1 });
      }
    }
  };

  canvas?.addEventListener("touchstart", handleTouchStart, { passive: true });
  canvas?.addEventListener("touchmove", (e) => {
    if (e.cancelable) e.preventDefault();
  }, { passive: false });
  canvas?.addEventListener("touchend", handleTouchEnd, { passive: true });

  const touchpadZone = document.getElementById("swipe-touchpad-zone");
  touchpadZone?.addEventListener("touchstart", handleTouchStart, { passive: true });
  touchpadZone?.addEventListener("touchmove", (e) => {
    if (e.cancelable) e.preventDefault();
  }, { passive: false });
  touchpadZone?.addEventListener("touchend", handleTouchEnd, { passive: true });

  // Prevenir gestos nativos de pull-to-refresh y navegación accidental al deslizar (INV-SNAKE-15)
  window.addEventListener("touchmove", (e) => {
    if (document.body.classList.contains("is-playing")) {
      if (e.cancelable) e.preventDefault();
    }
  }, { passive: false });
}

function startResumeCountdown() {
  if (!gameState || gameState.isGameOver) return;
  const overlay = document.getElementById("pause-overlay");
  if (overlay) overlay.classList.add("hidden");

  if (countdownTimerId) clearInterval(countdownTimerId);
  isCountdownActive = true;
  setFocusPlayingMode(true);

  let step = 3;
  countdownText = "3";
  playSound("countdown_tick");
  drawGame();

  countdownTimerId = setInterval(() => {
    step--;
    if (step > 0) {
      countdownText = String(step);
      playSound("countdown_tick");
      drawGame();
    } else if (step === 0) {
      countdownText = t("countdown_hack", currentLang);
      playSound("countdown_go");
      drawGame();
    } else {
      clearInterval(countdownTimerId);
      countdownTimerId = null;
      isCountdownActive = false;
      countdownText = "";
      if (gameState) gameState.isPaused = false;
      lastTickTime = performance.now();
      drawGame();
    }
  }, 380);
}

function togglePause() {
  if (!gameState || gameState.isGameOver || isHitStop) return;
  if (isCountdownActive) {
    if (countdownTimerId) clearInterval(countdownTimerId);
    countdownTimerId = null;
    isCountdownActive = false;
    countdownText = "";
    gameState.isPaused = true;
    document.getElementById("pause-overlay")?.classList.remove("hidden");
    setFocusPlayingMode(false);
    return;
  }
  if (gameState.isPaused) {
    startResumeCountdown();
  } else {
    gameState.isPaused = true;
    const overlay = document.getElementById("pause-overlay");
    if (overlay) overlay.classList.remove("hidden");
    setFocusPlayingMode(false);
  }
}

// --- CICLO PWA & ACTUALIZACIÓN IN-APP (INV-SNAKE-8 & INV-SNAKE-13) ---
function setupPWA() {
  if (typeof window !== "undefined") {
    isStandalone = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
  }

  const btnInstall = document.getElementById("btn-install-pwa");
  if (btnInstall && isStandalone) {
    btnInstall.classList.add("hidden");
  }

  // Capturar prompt nativo de instalación
  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredInstallPrompt = e;
    if (btnInstall && !isStandalone) {
      btnInstall.classList.remove("hidden");
    }
  });

  // Evento appinstalled nativo
  window.addEventListener("appinstalled", () => {
    deferredInstallPrompt = null;
    isStandalone = true;
    if (btnInstall) btnInstall.classList.add("hidden");
    showToast(t("install_success_toast", currentLang));
  });

  if (btnInstall) {
    btnInstall.addEventListener("click", async () => {
      if (deferredInstallPrompt) {
        deferredInstallPrompt.prompt();
        try {
          const choice = await deferredInstallPrompt.userChoice;
          if (choice && choice.outcome === "accepted") {
            btnInstall.classList.add("hidden");
            showToast(t("install_success_toast", currentLang));
          }
        } catch (e) {}
        deferredInstallPrompt = null;
      } else {
        const isIos = /iphone|ipad|ipod/.test(window.navigator.userAgent.toLowerCase()) && !window.MSStream;
        if (isIos) {
          showToast(t("install_ios_instructions", currentLang));
        } else {
          showToast(t("install_generic_instructions", currentLang));
        }
      }
    });
  }

  // Registrar Service Worker
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/games/snake/sw.js").then(reg => {
      swRegistration = reg;

      // 1. Si ya hay un worker esperando activación
      if (reg.waiting && navigator.serviceWorker.controller) {
        document.getElementById("pwa-update-banner")?.classList.remove("hidden");
      }

      // 2. Si se detecta un nuevo worker descargándose
      reg.addEventListener("updatefound", () => {
        const newWorker = reg.installing;
        if (!newWorker) return;
        newWorker.addEventListener("statechange", () => {
          if (newWorker.state === "installed" && navigator.serviceWorker.controller) {
            document.getElementById("pwa-update-banner")?.classList.remove("hidden");
          }
        });
      });
    }).catch(() => {});

    // Revalidar actualizaciones cuando la pestaña vuelve a enfocarse
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "visible" && swRegistration) {
        swRegistration.update().catch(() => {});
      }
    });

    // Botón interactivo de versión en cabecera (#btn-check-update)
    const checkBtn = document.getElementById("btn-check-update");
    if (checkBtn) {
      checkBtn.addEventListener("click", async () => {
        showToast(t("checking_updates", currentLang));
        try {
          const reg = swRegistration || await navigator.serviceWorker.getRegistration();
          if (reg) {
            if (reg.waiting) {
              document.getElementById("pwa-update-banner")?.classList.remove("hidden");
              return;
            }
            await reg.update();
            if (reg.waiting || reg.installing) {
              showToast(t("pwa_update_available", currentLang));
              document.getElementById("pwa-update-banner")?.classList.remove("hidden");
            } else {
              showToast(t("already_latest", currentLang));
            }
          } else {
            showToast(t("already_latest", currentLang));
          }
        } catch (e) {
          showToast(t("already_latest", currentLang));
        }
      });
    }

    // Botón de actualización en caliente del banner
    document.getElementById("btn-apply-update")?.addEventListener("click", () => {
      const reg = swRegistration;
      if (reg && reg.waiting) {
        reg.waiting.postMessage({ action: "skipWaiting" });
      } else {
        navigator.serviceWorker.getRegistration().then(activeReg => {
          if (activeReg && activeReg.waiting) {
            activeReg.waiting.postMessage({ action: "skipWaiting" });
          }
        });
      }
    });

    navigator.serviceWorker.addEventListener("controllerchange", () => {
      if (!swRefreshing) {
        swRefreshing = true;
        window.location.reload();
      }
    });
  }

  // Listener para sincronización desatendida cuando vuelve Internet (INV-SNAKE-13)
  window.addEventListener("online", async () => {
    try {
      const res = await flushOfflineQueue();
      if (res && res.flushed > 0) {
        showToast(t("offline_scores_synced", currentLang));
        if (currentTab === "ranking") {
          loadAndRenderRanking();
        }
      }
    } catch (e) {}
  });
}

// Iniciar aplicación al cargar
if (typeof window !== "undefined") {
  window.addEventListener("DOMContentLoaded", initGameApp);
}
