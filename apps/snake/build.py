# apps/snake/build.py
# Compilador y Empaquetador Determinista Single-Source-of-Truth
# Datalaria Neon Snake ("Cyberpunk Overdrive v2.0")

import os
import re
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
STATIC_DEST = REPO_ROOT / "static" / "games" / "snake"

def strip_es_modules(code: str) -> str:
    """Elimina imports y convierte exports en declaraciones locales para inlining."""
    # Eliminar sentencias import ... from '...'; o import '...';
    code = re.sub(r"^\s*import\s+[^;]+;\s*$", "", code, flags=re.MULTILINE)
    # Eliminar exportaciones nombradas export { ... };
    code = re.sub(r"^\s*export\s*\{[^}]+\};\s*$", "", code, flags=re.MULTILINE)
    # Reemplazar export const/let/var/function/async function/class por su declaración normal
    code = re.sub(r"^\s*export\s+(const|let|var|function|async\s+function|class)\s+", r"\1 ", code, flags=re.MULTILINE)
    return code

def build():
    print(f"[build.py] Compilando Neon Snake v2.0 desde {BASE_DIR} hacia {STATIC_DEST}...")
    STATIC_DEST.mkdir(parents=True, exist_ok=True)

    # 1. Leer estilos y módulos JS
    with open(BASE_DIR / "styles.css", "r", encoding="utf-8") as f:
        styles_css = f.read()

    js_files = ["catalog.js", "engine.js", "audio.js", "leaderboard.js", "app.js"]
    bundled_parts = []
    for jf in js_files:
        with open(BASE_DIR / jf, "r", encoding="utf-8") as f:
            content = f.read()
            bundled_parts.append(f"// --- INLINE BUNDLE: {jf} ---\n" + strip_es_modules(content))

    bundled_js = "\n\n".join(bundled_parts)

    # 2. Generar index.html canónico inlined en static/games/snake/
    index_html_content = f"""<!DOCTYPE html>
<html lang="es" data-theme="neon">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Neon Snake · Cyberpunk Overdrive · Datalaria</title>
  <meta name="description" content="Arcade retro Cyberpunk del clásico Snake con ranking global en tiempo real y audio sintetizado.">
  <meta name="theme-color" content="#00f0ff">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <link rel="manifest" href="/games/snake/manifest.json">
  <link rel="icon" type="image/svg+xml" href="/games/snake/icon.svg">
  <link rel="alternate icon" type="image/png" href="/games/snake/icon-192.png">
  <link rel="apple-touch-icon" href="/games/snake/apple-touch-icon.png">
  <!-- Micro-script Anti-FOUC inyectado en <head> -->
  <script>
    (function() {{
      try {{
        var saved = localStorage.getItem('pref-theme') || 'neon';
        document.documentElement.setAttribute('data-theme', saved === 'crt' ? 'crt' : 'neon');
      }} catch (e) {{}}
    }})();
  </script>
  <style>
{styles_css}
  </style>
</head>
<body>
  <!-- Shell Superior Datalaria -->
  <header id="app-header" class="app-header">
    <div class="brand-section">
      <a id="btn-back-datalaria" href="/es/apps/" class="btn-back" data-i18n="back_portal">← Datalaria</a>
      <div class="app-title-group">
        <h1 class="cyber-font neon-text-cyan">🐍 Neon Snake</h1>
      </div>
      <button id="btn-check-update" class="version-badge" title="Comprobar actualización">v2.3.1</button>
    </div>

    <div class="header-controls">
      <!-- Selector de perfil familiar -->
      <select id="profile-select" class="profile-select">
        <option value="hacker1">👾 Hacker 1</option>
        <option value="hacker2">🤖 Hacker 2</option>
        <option value="pro">⚡ Pro</option>
      </select>

      <!-- Selector de idioma -->
      <button id="btn-lang-toggle" class="ctrl-btn" title="Cambiar idioma">ES | EN</button>

      <!-- Botón de sonido -->
      <button id="btn-mute" class="ctrl-btn" title="Silenciar / Activar sonido">🔊</button>

      <!-- Conmutador de tema Neón / CRT -->
      <button id="btn-theme-toggle" class="ctrl-btn" title="Tema Neón / CRT">🌆</button>

      <!-- Conmutador D-Pad / Modo Swipe -->
      <button id="btn-toggle-dpad" class="ctrl-btn dpad-toggle-btn" title="Alternar D-Pad / Modo Swipe">🎮 D-Pad: ON</button>

      <!-- Botón Instalar PWA -->
      <button id="btn-install-pwa" class="ctrl-btn hidden" style="border-color: var(--neon-cyan); color: var(--neon-cyan);" data-i18n="btn_install">📲 Instalar</button>
    </div>

    <div class="header-links">
      <a id="link-nav-sheet" href="/es/apps/snake/" class="link-pill" data-i18n="nav_sheet">📋 Ficha</a>
      <a id="link-nav-tutorial" href="/es/posts/game_snake/" class="link-pill" data-i18n="nav_tutorial">📖 Tutorial</a>
      <a id="link-nav-kits" href="/es/recursos/" class="link-pill" data-i18n="nav_kits">📦 Kits</a>
    </div>
  </header>

  <!-- Pestañas de Navegación (Deck) -->
  <nav class="nav-deck">
    <button class="tab-btn active" data-tab="play"><span data-i18n="tab_play">🕹️ Jugar</span></button>
    <button class="tab-btn" data-tab="ranking"><span data-i18n="tab_ranking">🏆 Ranking</span></button>
    <button class="tab-btn" data-tab="skins"><span data-i18n="tab_skins">🎨 Skins</span></button>
    <button class="tab-btn" data-tab="medals"><span data-i18n="tab_medals">🎖️ Medallas</span></button>
    <button class="tab-btn" data-tab="help"><span data-i18n="tab_help">❓ Controles</span></button>
  </nav>

  <main class="app-container">
    <!-- Vista Principal: Jugar -->
    <div id="game-view-wrapper" class="game-view-wrapper">
      <!-- HUD de Juego -->
      <div class="game-hud">
        <div class="hud-top-row">
          <div class="hud-item">
            <span class="hud-label" data-i18n="score_label">PUNTUACIÓN</span>
            <span id="hud-score" class="hud-value neon-text-cyan">0</span>
          </div>

          <div class="hud-center-group">
            <div id="hud-combo" class="combo-pill">🔥 x1</div>
            <button id="btn-hud-pause" class="btn-hud-pause" data-i18n="hud_pause_btn" title="Pausar / Mostrar menú (P)">⏸ Pausa</button>
          </div>

          <div class="hud-item" style="text-align: right;">
            <span class="hud-label" data-i18n="level_label">NIVEL</span>
            <span id="hud-level" class="hud-value neon-text-yellow">1/10</span>
          </div>
        </div>

        <!-- Barra de enfriamiento de combo -->
        <div class="combo-bar-container">
          <div id="combo-bar-fill" class="combo-bar-fill"></div>
        </div>
      </div>

      <!-- Canvas de Juego con Overlays -->
      <div id="game-canvas-wrapper" class="game-canvas-wrapper">
        <canvas id="gameCanvas"></canvas>

        <!-- Overlay: Pantalla de Inicio y Selector de Modo -->
        <div id="start-overlay" class="canvas-overlay">
          <div class="overlay-inner">
            <h2 class="overlay-title cyber-font neon-text-cyan">NEON SNAKE</h2>
            <p class="overlay-subtitle cyber-font" data-i18n="app_tagline">CYBERPUNK OVERDRIVE v2.1</p>

            <!-- Selector de Modo de Juego -->
            <div class="mode-selector">
              <div class="mode-card selected" data-mode="arcade">
                <div class="mode-card-title" data-i18n="mode_arcade_title">🕹️ Arcade</div>
                <div class="mode-card-desc" data-i18n="mode_arcade_short">10 niveles + Firewalls</div>
              </div>
              <div class="mode-card" data-mode="daily">
                <div class="mode-card-title" data-i18n="mode_daily_title">📅 Reto Diario</div>
                <div class="mode-card-desc" data-i18n="mode_daily_short">Semilla mundial hoy</div>
              </div>
              <div class="mode-card" data-mode="time_attack">
                <div class="mode-card-title" data-i18n="mode_time_title">⏱️ Contrarreloj</div>
                <div class="mode-card-desc" data-i18n="mode_time_short">90s · Bordes abiertos</div>
              </div>
              <div class="mode-card" data-mode="zen">
                <div class="mode-card-title" data-i18n="mode_zen_title">🧘 Zen Chill</div>
                <div class="mode-card-desc" data-i18n="mode_zen_short">Sin muros · Relajado</div>
              </div>
            </div>

            <!-- Input Nombre de Agente -->
            <input type="text" id="username-input" class="cyber-input" placeholder="ALIAS DE AGENTE (MÁX 12)" maxlength="12" value="Neo">

            <!-- Botones de Acción -->
            <div class="overlay-actions-stack">
              <button id="btn-start-game" class="btn-arcade-action" data-i18n="btn_start">INICIAR SISTEMA</button>
              <button id="btn-view-ranking-start" class="btn-arcade-action btn-arcade-neutral" data-i18n="btn_view_ranking">🏆 RANKING</button>
            </div>
          </div>
        </div>

        <!-- Overlay: Pausa -->
        <div id="pause-overlay" class="canvas-overlay hidden">
          <div class="overlay-inner">
            <h2 class="overlay-title cyber-font neon-text-yellow" data-i18n="paused_title">SISTEMA EN PAUSA</h2>
            <p class="overlay-subtitle" data-i18n="paused_hint">Pulsa P, Espacio o Reanudar para continuar</p>
            <div class="overlay-actions-stack">
              <button id="btn-resume-game" class="btn-arcade-action" data-i18n="btn_resume">REANUDAR</button>
              <button id="btn-restart-pause" class="btn-arcade-action btn-arcade-neutral" data-i18n="btn_retry">⚡ REINTENTAR</button>
            </div>
          </div>
        </div>

        <!-- Overlay: Game Over -->
        <div id="gameover-overlay" class="canvas-overlay hidden">
          <div class="overlay-inner">
            <div id="gameover-modal-body">
              <h2 id="gameover-title" class="overlay-title cyber-font neon-text-pink" data-i18n="game_over_title">SYSTEM FAILURE</h2>
              <p id="gameover-subtitle" class="overlay-subtitle" data-i18n="game_over_subtitle">Conexión terminada. Datos registrados.</p>

              <div class="gameover-score-box">
                <span class="gameover-score-label" data-i18n="final_score_label">PUNTUACIÓN FINAL</span>
                <div id="gameover-final-score" class="gameover-score-value">0</div>
              </div>

              <div class="overlay-actions-stack">
                <button id="btn-restart-game" class="btn-arcade-action" data-i18n="btn_retry">⚡ REINTENTAR</button>
                <div class="overlay-actions-row">
                  <button id="btn-download-cybercard" class="btn-arcade-action btn-arcade-secondary" data-i18n="btn_download_card">🎓 Cyber-Card (PNG)</button>
                  <button id="btn-view-ranking-gameover" class="btn-arcade-action btn-arcade-neutral" data-i18n="btn_view_ranking">🏆 RANKING</button>
                </div>
                <button id="btn-share-daily" class="btn-arcade-action btn-arcade-neutral hidden" data-i18n="btn_share_daily">📤 Compartir Reto</button>
                <div class="btn-inspect-wrap">
                  <button id="btn-inspect-board" class="btn-inspect-board"><span data-i18n="btn_inspect_board">👁️ Ver Tablero</span></button>
                </div>
              </div>
            </div>

            <!-- Barra de control flotante durante la Inspección de Tablero -->
            <div id="inspect-controls-bar" class="inspect-controls-bar hidden">
              <div class="inspect-hint-badge" data-i18n="inspect_hint">👁️ MODO INSPECCIÓN DE TABLERO</div>
              <div class="inspect-buttons-row">
                <button id="btn-inspect-retry" class="btn-arcade-action btn-inspect-retry" data-i18n="btn_retry">⚡ REINTENTAR</button>
                <button id="btn-inspect-close" class="btn-arcade-action btn-arcade-neutral btn-inspect-close" data-i18n="btn_restore_overlay">↩️ Menú</button>
              </div>
              <span class="inspect-tap-hint" data-i18n="inspect_tap_to_restore">Toca el tablero para volver</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Controles Táctiles para Móvil / Tablet -->
      <div id="touch-controls-deck" class="d-pad-container">
        <!-- Conmutador Táctil Ergonómico D-Pad vs Full-Swipe (INV-SNAKE-14) -->
        <div class="touch-mode-bar">
          <button id="btn-toggle-dpad-deck" class="btn-touch-mode-pill" type="button">
            <span id="dpad-deck-label" data-i18n="dpad_deck_mode_dpad">🎮 Controles: Cruceta (Toca para Swipe)</span>
          </button>
        </div>

        <!-- Área de Cruceta Virtual D-Pad -->
        <div class="d-pad-grid-wrapper">
          <div class="d-pad-grid">
            <div></div>
            <button class="d-pad-btn" data-dir="up">▲</button>
            <div></div>
            <button class="d-pad-btn" data-dir="left">◀</button>
            <button id="btn-touch-pause" class="d-pad-btn" style="border-color: rgba(255, 0, 122, 0.4); color: var(--neon-pink);">⏸</button>
            <button class="d-pad-btn" data-dir="right">▶</button>
            <div></div>
            <button class="d-pad-btn" data-dir="down">▼</button>
            <div></div>
          </div>

          <!-- Botón Hyper-Dash Boost D-Pad -->
          <button id="btn-touch-boost" class="btn-boost-touch">
            <span style="font-size: 1.4rem;">⚡</span>
            <span>BOOST</span>
          </button>
        </div>

        <!-- Cyber-Touchpad para Modo Swipe (sin D-Pad) -->
        <div id="swipe-touchpad-zone" class="swipe-touchpad-zone hidden">
          <div class="touchpad-visual">
            <span class="touchpad-icon">👆</span>
            <span class="touchpad-title" data-i18n="swipe_zone_title">ZONA TÁCTIL DE GESTOS</span>
            <span class="touchpad-sub" data-i18n="swipe_zone_sub">Desliza en cualquier dirección para girar</span>
          </div>
          <button id="btn-touch-boost-swipe" class="btn-boost-touch btn-boost-swipe">
            <span style="font-size: 1.3rem;">⚡</span>
            <span data-i18n="btn_boost_swipe">HYPER-DASH BOOST (x2 PUNTOS)</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Panel de Ranking (Cyberpunk Hall of Fame) -->
    <div id="ranking-panel" class="view-panel hidden">
      <div class="panel-header">
        <h3 class="panel-title" data-i18n="ranking_title">TOP CYBER AGENTS</h3>
        <button id="btn-refresh-ranking" class="ctrl-btn" title="Actualizar Ranking">🔄 Sync</button>
      </div>

      <div class="ranking-kpi-strip">
        <div class="ranking-kpi-card">
          <span class="ranking-kpi-label" data-i18n="ranking_your_best">MI RÉCORD</span>
          <span id="ranking-kpi-best" class="ranking-kpi-val">0 PTS</span>
        </div>
        <div class="ranking-kpi-card">
          <span class="ranking-kpi-label" data-i18n="ranking_max_combo">COMBO MÁX</span>
          <span id="ranking-kpi-combo" class="ranking-kpi-val" style="color: var(--neon-pink);">x1</span>
        </div>
        <div class="ranking-kpi-card">
          <span class="ranking-kpi-label" data-i18n="ranking_status">ESTADO RED</span>
          <span id="ranking-kpi-status" class="ranking-kpi-val" style="color: var(--neon-green);" data-i18n="ranking_online">🟢 ONLINE</span>
        </div>
      </div>

      <ol id="ranking-list" class="ranking-list">
        <li class="ranking-empty" data-i18n="ranking_loading">Conectando al servidor central...</li>
      </ol>
    </div>

    <!-- Panel de Skins Hangar -->
    <div id="skins-panel" class="view-panel hidden">
      <div class="panel-header">
        <h3 class="panel-title" data-i18n="skins_title">HANGAR DE CYBER-SKINS</h3>
      </div>
      <div id="skins-grid" class="skins-grid"></div>
    </div>

    <!-- Panel de Medallas -->
    <div id="medals-panel" class="view-panel hidden">
      <div class="panel-header">
        <h3 class="panel-title" data-i18n="medals_title">PASAPORTE DE MEDALLAS ARCADE</h3>
        <button id="btn-download-card-medals" class="ctrl-btn" style="border-color: var(--neon-cyan); color: var(--neon-cyan);" data-i18n="btn_download_card">🎓 Cyber-Card (PNG)</button>
      </div>
      <div id="medals-grid" class="medals-grid"></div>
    </div>

    <!-- Panel de Ayuda y Controles -->
    <div id="help-panel" class="view-panel hidden">
      <div class="panel-header">
        <h3 class="panel-title" data-i18n="help_title">SISTEMA DE CONTROL Y MECÁNICAS</h3>
      </div>
      <div class="help-grid">
        <div class="help-card">
          <h4 data-i18n="help_kb_title">🕹️ Controles de Teclado y Táctil</h4>
          <ul class="help-list">
            <li data-i18n="help_kb_move">Flechas / WASD / Swipe: Mover la serpiente en 4 direcciones.</li>
            <li data-i18n="help_kb_dash">Espacio / Shift / BOOST: Hyper-Dash (acelera y duplica puntos x2).</li>
            <li data-i18n="help_kb_pause">P / Esc / Botón Pausa: Pausar partida y mostrar barra superior.</li>
            <li data-i18n="help_kb_audio">M / T: Silenciar audio (M) o alternar Tema Neón / CRT 1982 (T).</li>
          </ul>
        </div>
        <div class="help-card">
          <h4 style="color: var(--neon-pink);" data-i18n="help_nodes_title">✨ Nodos Cibernéticos</h4>
          <ul class="help-list">
            <li data-i18n="help_node_data">◆ Datos Normales: +10 pts × nivel y recarga la barra de combo (4s).</li>
            <li data-i18n="help_node_gold">★ Núcleo Dorado: +50 pts × combo, dura 6 segundos y suma +2 al combo.</li>
            <li data-i18n="help_node_cryo">❄ Cryo-Pulse: Ralentiza la velocidad un 30% durante 5 segundos.</li>
            <li data-i18n="help_node_ghost">👻 Protocolo Fantasma: Atraviesa bordes, cola y firewalls durante 6s.</li>
          </ul>
        </div>
        <div class="help-card" style="grid-column: 1 / -1;">
          <h4 style="color: var(--neon-yellow);" data-i18n="help_fw_title">🛡️ Telegraphing de Firewalls</h4>
          <p class="help-list" data-i18n="help_fw_desc">A partir del Nivel 5, los firewalls parpadean en ámbar con aviso ⚠️ durante 3 ticks antes de volverse letales. ¡Nunca morirás por aparición instantánea!</p>
        </div>
      </div>
    </div>
  </main>

  <!-- PWA Update Banner -->
  <div id="pwa-update-banner" class="pwa-update-banner hidden">
    <span data-i18n="pwa_update_available">⚡ Nueva versión disponible</span>
    <button id="btn-apply-update" class="ctrl-btn" style="background: var(--neon-cyan); color: #05070d; font-weight: bold;" data-i18n="btn_pwa_update">Actualizar ahora</button>
  </div>

  <!-- Toast Container -->
  <div id="toast-container" class="toast-container"></div>

  <!-- Inlined Bundle JavaScript -->
  <script>
{bundled_js}
  </script>
</body>
</html>
"""

    with open(STATIC_DEST / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html_content)
    print("  -> Generado index.html canónico 100% inline con Anti-FOUC, PWA y bundle JS.")

    # 3. Copiar PWA assets e iconos a static/games/snake/
    pwa_files = [
        "manifest.json",
        "sw.js",
        "icon.svg",
        "icon-192.png",
        "icon-512.png",
        "icon-maskable-192.png",
        "icon-maskable-512.png",
        "apple-touch-icon.png"
    ]
    for filename in pwa_files:
        src = BASE_DIR / filename
        dst = STATIC_DEST / filename
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  -> Copiado activo PWA: {filename}")
        else:
            print(f"  [AVISO] Activo PWA no encontrado en origen: {filename}")

    # 4. Generar Shims de Redirección Retrocompatibles
    # Para /games/snake/es/ y /games/snake/en/
    shims = [
        ("es", "es"),
        ("en", "en")
    ]
    for folder, lang in shims:
        shim_dir = STATIC_DEST / folder
        shim_dir.mkdir(parents=True, exist_ok=True)
        shim_content = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=/games/snake/?lang={lang}">
  <title>Redireccionando a Neon Snake...</title>
</head>
<body style="background:#05070d;color:#00f0ff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;">
  <p>Cargando Neon Snake Cyberpunk Overdrive...</p>
</body>
</html>
"""
        with open(shim_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(shim_content)
        print(f"  -> Generado shim retrocompatible en static/games/snake/{folder}/index.html (?lang={lang})")

    # 5. Generar shim retrocompatible para /apps/snake/ -> /es/apps/snake/
    apps_snake_dir = REPO_ROOT / "static" / "apps" / "snake"
    apps_snake_dir.mkdir(parents=True, exist_ok=True)
    apps_snake_shim = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Redirigiendo a la ficha de Neon Snake · Datalaria...</title>
  <script>
    (function() {
      try {
        var nav = navigator.language || navigator.userLanguage || 'es';
        var lang = nav.startsWith('en') ? 'en' : 'es';
        var saved = localStorage.getItem('pref-lang');
        if (saved === 'es' || saved === 'en') lang = saved;
        window.location.replace('/' + lang + '/apps/snake/');
      } catch(e) {
        window.location.replace('/es/apps/snake/');
      }
    })();
  </script>
  <meta http-equiv="refresh" content="0; url=/es/apps/snake/">
  <link rel="canonical" href="https://datalaria.com/es/apps/snake/">
</head>
<body style="background:#05070d;color:#00f0ff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;">
  <p>Redirigiendo a la ficha de Neon Snake... <a href="/es/apps/snake/" style="color:#00f0ff;">Pulsa aquí si no eres redirigido</a>.</p>
</body>
</html>
"""
    with open(apps_snake_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(apps_snake_shim)
    print("  -> Generado shim retrocompatible en static/apps/snake/index.html")

    print("[build.py] ¡Compilación finalizada con éxito!")

if __name__ == "__main__":
    build()
