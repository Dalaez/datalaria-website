// apps/snake/catalog.js
// Catálogo de Modos, Skins, Medallas, Perfiles y Diccionario i18n
// Datalaria Neon Snake ("Cyberpunk Overdrive v2.0")

export const GRID_SIZE = 20;

export const MODES = {
  arcade: {
    id: "arcade",
    icon: "🕹️",
    name: { es: "Arcade Overdrive", en: "Arcade Overdrive" },
    desc: {
      es: "10 niveles de velocidad creciente, firewalls dinámicos y ranking global.",
      en: "10 progressive speed levels, dynamic firewalls, and global leaderboard."
    },
    hasLevels: true,
    hasWalls: true,
    hasTimer: false,
    durationSec: null
  },
  daily: {
    id: "daily",
    icon: "📅",
    name: { es: "Reto Diario", en: "Daily Challenge" },
    desc: {
      es: "Misma cuadrícula y secuencia a nivel mundial por fecha. ¡Compite por el récord!",
      en: "Same global seed and sequence by date. Compete for the world high score!"
    },
    hasLevels: true,
    hasWalls: true,
    hasTimer: false,
    durationSec: null
  },
  time_attack: {
    id: "time_attack",
    icon: "⏱️",
    name: { es: "Contrarreloj 90s", en: "Time Attack 90s" },
    desc: {
      es: "Bordes abiertos. Chocar no te mata, te resta 5s y segmentos. Núcleos dorados dan +4s.",
      en: "Open borders. Crashing trims tail and -5s instead of death. Golden cores grant +4s."
    },
    hasLevels: false,
    hasWalls: false,
    hasTimer: true,
    durationSec: 90
  },
  zen: {
    id: "zen",
    icon: "🧘",
    name: { es: "Zen Cyber-Chill", en: "Zen Cyber-Chill" },
    desc: {
      es: "Sin firewalls, bordes envolventes infinitos y velocidad relajada constante.",
      en: "No firewalls, wrap-around borders, and constant relaxed speed."
    },
    hasLevels: false,
    hasWalls: false,
    hasTimer: false,
    durationSec: null
  }
};

export const NODES = {
  data: {
    id: "data",
    type: "food",
    color: "#00f0ff",
    glow: "#00f0ff",
    symbol: "◆",
    basePoints: 10,
    durationTicks: null,
    effectDesc: { es: "Datos estándar (+puntos según nivel)", en: "Standard data (+points scaled by level)" }
  },
  golden: {
    id: "golden",
    type: "powerup",
    color: "#ffe600",
    glow: "#ffe600",
    symbol: "★",
    basePoints: 50,
    lifespanSec: 6.0,
    durationTicks: null,
    effectDesc: { es: "Núcleo Dorado: +50 pts x combo y +2 al multiplicador", en: "Golden Core: +50 pts x combo and +2 to multiplier" }
  },
  cryo: {
    id: "cryo",
    type: "powerup",
    color: "#38bdf8",
    glow: "#0284c7",
    symbol: "❄",
    basePoints: 20,
    lifespanSec: 7.0,
    durationSec: 5.0,
    effectDesc: { es: "Cryo-Pulse: ralentiza la serpiente un 30% durante 5s", en: "Cryo-Pulse: slows snake by 30% for 5s" }
  },
  ghost: {
    id: "ghost",
    type: "powerup",
    color: "#10b981",
    glow: "#059669",
    symbol: "👻",
    basePoints: 25,
    lifespanSec: 7.0,
    durationSec: 6.0,
    effectDesc: { es: "Ghost Protocol: atraviesa paredes y colas durante 6s", en: "Ghost Protocol: pass through walls & tail for 6s" }
  }
};

export const SKINS = {
  cyan_viper: {
    id: "cyan_viper",
    name: { es: "Cyan Viper", en: "Cyan Viper" },
    desc: { es: "Skin clásica de neón cibernético.", en: "Classic cyber neon skin." },
    headColor: "#00f0ff",
    bodyColor: "#008888",
    eyeColor: "#ffffff",
    glowColor: "#00f0ff",
    unlockedByDefault: true,
    reqDesc: { es: "Desbloqueada", en: "Unlocked" }
  },
  gold_sovereign: {
    id: "gold_sovereign",
    name: { es: "Gold Sovereign", en: "Gold Sovereign" },
    desc: { es: "Piel dorada de alta frecuencia.", en: "High frequency golden alloy." },
    headColor: "#ffe600",
    bodyColor: "#b39b00",
    eyeColor: "#ffffff",
    glowColor: "#ffe600",
    unlockedByDefault: false,
    reqDesc: { es: "Alcanza 500 puntos en cualquier modo", en: "Score 500 points in any mode" },
    checkUnlock: (stats) => (stats.highScore || 0) >= 500
  },
  matrix_operator: {
    id: "matrix_operator",
    name: { es: "Matrix Operator", en: "Matrix Operator" },
    desc: { es: "Código verde fósforo terminal 1999.", en: "Phosphor green terminal code 1999." },
    headColor: "#00ff66",
    bodyColor: "#007722",
    eyeColor: "#ccffdd",
    glowColor: "#00ff66",
    unlockedByDefault: false,
    reqDesc: { es: "Alcanza el Nivel 5 en modo Arcade", en: "Reach Level 5 in Arcade mode" },
    checkUnlock: (stats) => (stats.maxLevel || 1) >= 5
  },
  akira_plasma: {
    id: "akira_plasma",
    name: { es: "Akira Plasma", en: "Akira Plasma" },
    desc: { es: "Furia carmesí de sobrecarga cuántica.", en: "Crimson quantum overdrive fury." },
    headColor: "#ff007a",
    bodyColor: "#990033",
    eyeColor: "#ffffff",
    glowColor: "#ff007a",
    unlockedByDefault: false,
    reqDesc: { es: "Logra un Combo x5 activo", en: "Achieve an active x5 Combo" },
    checkUnlock: (stats) => (stats.maxCombo || 1) >= 5
  },
  glitch_phantom: {
    id: "glitch_phantom",
    name: { es: "Glitch Phantom", en: "Glitch Phantom" },
    desc: { es: "Anomalía cuántica espectral multidimensional.", en: "Spectral multidimensional quantum anomaly." },
    headColor: "#a855f7",
    bodyColor: "#581c87",
    eyeColor: "#00f0ff",
    glowColor: "#c084fc",
    unlockedByDefault: false,
    reqDesc: { es: "Completa un Reto Diario o 4 medallas", en: "Complete a Daily Challenge or 4 medals" },
    checkUnlock: (stats) => (stats.dailyCompleted || 0) >= 1 || (stats.medalsCount || 0) >= 4
  }
};

export const MEDALS = {
  first_hack: {
    id: "first_hack",
    icon: "⚡",
    name: { es: "Primer Hack", en: "First Hack" },
    desc: { es: "Consume tu primer nodo de datos.", en: "Consume your first data node." }
  },
  overclock: {
    id: "overclock",
    icon: "🔥",
    name: { es: "Maestro Overclock", en: "Overclock Master" },
    desc: { es: "Alcanza un combo multiplicador x5.", en: "Reach a x5 combo multiplier." }
  },
  firewall_breaker: {
    id: "firewall_breaker",
    icon: "🛡️",
    name: { es: "Rompe-Muros", en: "Firewall Breaker" },
    desc: { es: "Supera el Nivel 5 en el modo Arcade.", en: "Survive Level 5 in Arcade mode." }
  },
  ghost_walker: {
    id: "ghost_walker",
    icon: "👻",
    name: { es: "Protocolo Fantasma", en: "Ghost Protocol" },
    desc: { es: "Atraviesa un muro en modo fantasma.", en: "Pass through a wall while in ghost mode." }
  },
  daily_hacker: {
    id: "daily_hacker",
    icon: "📅",
    name: { es: "Hacker Cotidiano", en: "Daily Hacker" },
    desc: { es: "Completa una partida del Reto Diario.", en: "Complete a Daily Challenge match." }
  },
  cyber_legend: {
    id: "cyber_legend",
    icon: "👑",
    name: { es: "Leyenda Cyberpunk", en: "Cyber Legend" },
    desc: { es: "Supera los 1.500 puntos en una partida.", en: "Score over 1,500 points in a single match." }
  }
};

export const PROFILES = [
  { id: "hacker1", name: "👾 Hacker 1", defaultAgent: "Neo" },
  { id: "hacker2", name: "🤖 Hacker 2", defaultAgent: "Trinity" },
  { id: "pro", name: "⚡ Pro", defaultAgent: "Morpheus" }
];

export const I18N = {
  es: {
    app_title: "Neon Snake",
    app_tagline: "Cyberpunk Overdrive Edition v2.3",
    back_portal: "← Datalaria",
    tab_play: "🕹️ Jugar",
    tab_ranking: "🏆 Ranking",
    tab_skins: "🎨 Skins",
    tab_medals: "🎖️ Medallas",
    tab_help: "❓ Controles",
    btn_install: "📲 Instalar",
    install_app_title: "Instalar Neon Snake en tu dispositivo (PWA)",
    install_success_toast: "✓ ¡Neon Snake instalada con éxito!",
    install_ios_instructions: "📲 En Safari iOS: pulsa Compartir (⎙) y elige \"Añadir a pantalla de inicio\"",
    install_generic_instructions: "📲 Pulsa el menú (⋮) del navegador y elige \"Instalar aplicación\" o \"Añadir a pantalla de inicio\"",
    btn_pwa_update: "🔄 Actualizar ahora",
    pwa_update_available: "⚡ Nueva versión v2.3 disponible",
    checking_updates: "🔍 Buscando actualizaciones...",
    already_latest: "✅ Tienes la versión más reciente (v2.3.0)",
    offline_scores_synced: "🌐 Puntuaciones offline sincronizadas con el mainframe",
    ranking_offline_badge: "⏳ OFFLINE",
    btn_toggle_dpad_on: "🎮 D-Pad: ON",
    btn_toggle_dpad_off: "👆 Swipe: ON",
    btn_inspect_board: "👁️ Ver Tablero",
    btn_restore_overlay: "↩️ Menú",
    inspect_hint: "👁️ MODO INSPECCIÓN DE TABLERO",
    inspect_tap_to_restore: "Pulsa en la pantalla para volver al menú",
    dpad_deck_mode_dpad: "🎮 Controles: Cruceta (Toca para Swipe)",
    dpad_deck_mode_swipe: "👆 Controles: Swipe (Toca para Cruceta)",
    swipe_zone_title: "ZONA TÁCTIL DE GESTOS",
    swipe_zone_sub: "Desliza en cualquier dirección para girar",
    btn_boost_swipe: "⚡ HYPER-DASH BOOST (x2 PUNTOS)",
    countdown_hack: "¡HACK!",
    toast_dpad_enabled: "🎮 D-Pad táctil activado",
    toast_swipe_mode: "👆 Modo Swipe activado (tablero maximizado)",
    score_label: "PUNTUACIÓN",
    final_score_label: "PUNTUACIÓN FINAL",
    level_label: "NIVEL",
    time_label: "TIEMPO",
    combo_label: "COMBO",
    hud_pause_btn: "⏸ Pausa",
    speed_boost_hint: "Mantén Espacio / Shift para Hyper-Dash (2x pts)",
    paused_title: "SISTEMA EN PAUSA",
    paused_hint: "Pulsa P, Espacio o Reanudar para continuar",
    btn_resume: "REANUDAR",
    btn_start: "INICIAR SISTEMA",
    btn_retry: "⚡ REINTENTAR",
    btn_view_ranking: "🏆 RANKING",
    btn_close: "CERRAR",
    btn_download_card: "🎓 Cyber-Card (PNG)",
    btn_share_daily: "📤 Compartir Reto",
    game_over_title: "SYSTEM FAILURE",
    game_over_subtitle: "Conexión terminada. Datos registrados.",
    agent_name_placeholder: "ALIAS DE AGENTE (MÁX 12)",
    saving_score: "Guardando puntuación en la red...",
    score_saved: "¡Puntuación sincronizada en el mainframe!",
    score_offline_queued: "Puntuación guardada localmente (modo offline)",
    ranking_title: "TOP CYBER AGENTS",
    ranking_your_best: "MI RÉCORD",
    ranking_max_combo: "COMBO MÁX",
    ranking_status: "ESTADO RED",
    ranking_online: "🟢 ONLINE",
    ranking_you_badge: "TÚ",
    ranking_global_tab: "🌐 Global Supabase",
    ranking_local_tab: "💾 Mis Récords",
    ranking_loading: "Conectando al servidor central...",
    ranking_empty: "Sin registros en la base de datos.",
    skins_title: "HANGAR DE CYBER-SKINS",
    skins_equipped: "EQUIPADA",
    skins_equip_btn: "EQUIPAR",
    skins_locked: "BLOQUEADA",
    medals_title: "PASAPORTE DE MEDALLAS ARCADE",
    medals_unlocked: "Desbloqueada",
    medals_locked: "Bloqueada",
    card_generating: "Generando Cyber-Card en alta resolución...",
    card_downloaded: "¡Cyber-Card descargada con éxito!",
    daily_copied: "¡Resumen del Reto Diario copiado al portapapeles!",
    toast_skin_unlocked: "🔓 ¡Nueva Skin desbloqueada!",
    toast_medal_unlocked: "🎖️ ¡Medalla desbloqueada!",
    nav_sheet: "📋 Ficha",
    nav_tutorial: "📖 Tutorial",
    nav_kits: "📦 Kits",
    theme_neon: "🌆 Neón",
    theme_crt: "📺 CRT 1982",
    mode_arcade_title: "🕹️ Arcade",
    mode_arcade_short: "10 niveles + Firewalls",
    mode_daily_title: "📅 Reto Diario",
    mode_daily_short: "Semilla mundial hoy",
    mode_time_title: "⏱️ Contrarreloj",
    mode_time_short: "90s · Bordes abiertos",
    mode_zen_title: "🧘 Zen Chill",
    mode_zen_short: "Sin muros · Relajado",
    help_title: "SISTEMA DE CONTROL Y MECÁNICAS",
    help_kb_title: "🕹️ Controles de Teclado y Táctil",
    help_kb_move: "Flechas / WASD / Swipe: Mover la serpiente en 4 direcciones.",
    help_kb_dash: "Espacio / Shift / BOOST: Hyper-Dash (acelera y duplica puntos x2).",
    help_kb_pause: "P / Esc / Botón Pausa: Pausar partida y mostrar barra superior.",
    help_kb_audio: "M / T: Silenciar audio (M) o alternar Tema Neón / CRT 1982 (T).",
    help_nodes_title: "✨ Nodos Cibernéticos",
    help_node_data: "◆ Datos Normales: +10 pts × nivel y recarga la barra de combo (4s).",
    help_node_gold: "★ Núcleo Dorado: +50 pts × combo, dura 6 segundos y suma +2 al combo.",
    help_node_cryo: "❄ Cryo-Pulse: Ralentiza la velocidad un 30% durante 5 segundos.",
    help_node_ghost: "👻 Protocolo Fantasma: Atraviesa bordes, cola y firewalls durante 6s.",
    help_fw_title: "🛡️ Telegraphing de Firewalls",
    help_fw_desc: "A partir del Nivel 5, los firewalls parpadean en ámbar con aviso ⚠️ durante 3 ticks antes de volverse letales. ¡Nunca morirás por aparición instantánea!"
  },
  en: {
    app_title: "Neon Snake",
    app_tagline: "Cyberpunk Overdrive Edition v2.3",
    back_portal: "← Datalaria",
    tab_play: "🕹️ Play",
    tab_ranking: "🏆 Leaderboard",
    tab_skins: "🎨 Skins",
    tab_medals: "🎖️ Medals",
    tab_help: "❓ Controls",
    btn_install: "📲 Install",
    install_app_title: "Install Neon Snake on your device (PWA)",
    install_success_toast: "✓ Neon Snake successfully installed!",
    install_ios_instructions: "📲 In Safari iOS: tap Share (⎙) and choose \"Add to Home Screen\"",
    install_generic_instructions: "📲 Tap browser menu (⋮) and select \"Install app\" or \"Add to Home Screen\"",
    btn_pwa_update: "🔄 Update now",
    pwa_update_available: "⚡ New version v2.3 available",
    checking_updates: "🔍 Checking for updates...",
    already_latest: "✅ You have the latest version (v2.3.0)",
    offline_scores_synced: "🌐 Offline scores synchronized with mainframe",
    ranking_offline_badge: "⏳ OFFLINE",
    btn_toggle_dpad_on: "🎮 D-Pad: ON",
    btn_toggle_dpad_off: "👆 Swipe: ON",
    btn_inspect_board: "👁️ View Board",
    btn_restore_overlay: "↩️ Menu",
    inspect_hint: "👁️ BOARD INSPECTION MODE",
    inspect_tap_to_restore: "Tap anywhere on screen to return to menu",
    dpad_deck_mode_dpad: "🎮 Controls: D-Pad (Tap for Swipe)",
    dpad_deck_mode_swipe: "👆 Controls: Swipe (Tap for D-Pad)",
    swipe_zone_title: "GESTURE TOUCHPAD ZONE",
    swipe_zone_sub: "Swipe in any direction to turn",
    btn_boost_swipe: "⚡ HYPER-DASH BOOST (x2 SCORE)",
    countdown_hack: "HACK!",
    toast_dpad_enabled: "🎮 Touch D-Pad enabled",
    toast_swipe_mode: "👆 Swipe mode active (board maximized)",
    score_label: "SCORE",
    final_score_label: "FINAL SCORE",
    level_label: "LEVEL",
    time_label: "TIME",
    combo_label: "COMBO",
    hud_pause_btn: "⏸ Pause",
    speed_boost_hint: "Hold Space / Shift for Hyper-Dash (2x pts)",
    paused_title: "SYSTEM PAUSED",
    paused_hint: "Press P, Space or Resume to continue",
    btn_resume: "RESUME",
    btn_start: "INIT SYSTEM",
    btn_retry: "⚡ RETRY",
    btn_view_ranking: "🏆 RANKING",
    btn_close: "CLOSE",
    btn_download_card: "🎓 Cyber-Card (PNG)",
    btn_share_daily: "📤 Share Daily",
    game_over_title: "SYSTEM FAILURE",
    game_over_subtitle: "Connection terminated. Data recorded.",
    agent_name_placeholder: "AGENT ALIAS (MAX 12)",
    saving_score: "Saving score to mainframe...",
    score_saved: "Score synchronized in mainframe!",
    score_offline_queued: "Score saved locally (offline mode)",
    ranking_title: "TOP CYBER AGENTS",
    ranking_your_best: "MY BEST",
    ranking_max_combo: "MAX COMBO",
    ranking_status: "NET STATUS",
    ranking_online: "🟢 ONLINE",
    ranking_you_badge: "YOU",
    ranking_global_tab: "🌐 Global Supabase",
    ranking_local_tab: "💾 My Records",
    ranking_loading: "Connecting to central mainframe...",
    ranking_empty: "No records found in database.",
    skins_title: "CYBER-SKINS HANGAR",
    skins_equipped: "EQUIPPED",
    skins_equip_btn: "EQUIP",
    skins_locked: "LOCKED",
    medals_title: "ARCADE MEDALS PASSPORT",
    medals_unlocked: "Unlocked",
    medals_locked: "Locked",
    card_generating: "Rendering high-res Cyber-Card...",
    card_downloaded: "Cyber-Card downloaded successfully!",
    daily_copied: "Daily Challenge summary copied to clipboard!",
    toast_skin_unlocked: "🔓 New Cyber-Skin unlocked!",
    toast_medal_unlocked: "🎖️ Medal unlocked!",
    nav_sheet: "📋 App Spec",
    nav_tutorial: "📖 Tutorial",
    nav_kits: "📦 Kits",
    theme_neon: "🌆 Neon",
    theme_crt: "📺 CRT 1982",
    mode_arcade_title: "🕹️ Arcade",
    mode_arcade_short: "10 levels + Firewalls",
    mode_daily_title: "📅 Daily Challenge",
    mode_daily_short: "Global daily seed",
    mode_time_title: "⏱️ Time Attack",
    mode_time_short: "90s · Open borders",
    mode_zen_title: "🧘 Zen Chill",
    mode_zen_short: "No walls · Chill",
    help_title: "CONTROL SYSTEM & MECHANICS",
    help_kb_title: "🕹️ Keyboard & Touch Controls",
    help_kb_move: "Arrows / WASD / Swipe: Move the snake in 4 directions.",
    help_kb_dash: "Space / Shift / BOOST: Hyper-Dash (accelerates & doubles points 2x).",
    help_kb_pause: "P / Esc / Pause Button: Pause match and reveal top navigation bar.",
    help_kb_audio: "M / T: Mute audio (M) or toggle Neon / 1982 CRT Theme (T).",
    help_nodes_title: "✨ Cybernetic Nodes",
    help_node_data: "◆ Standard Data: +10 pts × level and refills the 4s combo bar.",
    help_node_gold: "★ Golden Core: +50 pts × combo, lasts 6 seconds and adds +2 combo.",
    help_node_cryo: "❄ Cryo-Pulse: Slows movement speed by 30% for 5 seconds.",
    help_node_ghost: "👻 Ghost Protocol: Phase through borders, tail and firewalls for 6s.",
    help_fw_title: "🛡️ Firewall Telegraphing",
    help_fw_desc: "From Level 5 onwards, firewalls flash amber with a ⚠️ warning for 3 ticks before becoming lethal. Zero unfair deaths!"
  }
};

export function t(key, lang = "es") {
  const dict = I18N[lang] || I18N.es;
  return dict[key] || I18N.es[key] || key;
}

export function getSkin(id) {
  return SKINS[id] || SKINS.cyan_viper;
}

export function getMode(id) {
  return MODES[id] || MODES.arcade;
}
