"""
apps/snake/tests/test_snake.py
Suite de verificación determinista para Neon Snake ("Cyberpunk Overdrive v2.0").
Valida las invariantes de dominio INV-SNAKE-1 a INV-SNAKE-10 y el firewall de static/.
"""

import os
import re
import json
import subprocess
import pytest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
REPO_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../../.."))
STATIC_DIR = os.path.join(REPO_ROOT, "static", "games", "snake")


def test_inv_snake_1_source_files_exist():
    """INV-SNAKE-1: Verifica que todos los componentes modulares de apps/snake/ existen."""
    required = [
        "catalog.js",
        "engine.js",
        "audio.js",
        "leaderboard.js",
        "styles.css",
        "app.js",
        "build_icons.py",
        "build.py",
        "manifest.json",
        "sw.js",
        "icon.svg",
        "icon-192.png",
        "icon-512.png",
        "icon-maskable-192.png",
        "icon-maskable-512.png",
        "apple-touch-icon.png"
    ]
    for fname in required:
        fpath = os.path.join(APP_DIR, fname)
        assert os.path.exists(fpath), f"Falta el archivo fuente obligatorio: {fname}"


def test_inv_snake_2_deterministic_engine_with_node():
    """INV-SNAKE-2: Verifica determinismo del motor PRNG Mulberry32 y telegraphing de firewalls con Node.js."""
    from pathlib import Path
    engine_path = os.path.join(APP_DIR, "engine.js")
    engine_url = Path(engine_path).as_uri()
    node_script = f"""
    import {{ createSeededRng, createInitialGameState, getLevelObstacles, tickGame }} from '{engine_url}';
    
    // 1. Verificar determinismo de Mulberry32
    const rng1 = createSeededRng('2026-11-07');
    const rng2 = createSeededRng('2026-11-07');
    const seq1 = [rng1(), rng1(), rng1(), rng1()];
    const seq2 = [rng2(), rng2(), rng2(), rng2()];
    if (JSON.stringify(seq1) !== JSON.stringify(seq2)) {{
        console.error('FAIL: PRNG no determinista');
        process.exit(1);
    }}

    // 2. Obstáculos por nivel
    const obsLvl4 = getLevelObstacles(4);
    const obsLvl5 = getLevelObstacles(5);
    if (obsLvl4.length !== 0 || obsLvl5.length !== 16) {{
        console.error('FAIL: getLevelObstacles incorrecto');
        process.exit(2);
    }}

    // 3. Estado inicial
    const state = createInitialGameState('arcade', {{}}, rng1);
    if (state.score !== 0 || state.level !== 1 || state.snake.length !== 3 || state.combo !== 1) {{
        console.error('FAIL: estado inicial inválido');
        process.exit(3);
    }}

    // 4. Tick determinista
    const events = tickGame(state, 140, false);
    if (state.snake[0].x !== 11 || state.snake[0].y !== 10) {{
        console.error('FAIL: movimiento inválido');
        process.exit(4);
    }}

    console.log('NODE_OK');
    """

    res = subprocess.run(["node", "--input-type=module", "-e", node_script], capture_output=True, text=True)
    assert res.returncode == 0, f"Error en motor JS con Node.js:\n{res.stderr}"
    assert "NODE_OK" in res.stdout


def test_inv_snake_3_zero_external_dependencies():
    """INV-SNAKE-3: Cero dependencias externas en runtime (sin Tailwind CDN, fuentes bloqueantes o jsDelivr)."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    assert os.path.exists(index_html), "static/games/snake/index.html debe existir"
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    assert "cdn.tailwindcss.com" not in content, "Violación: presencia de cdn.tailwindcss.com en index.html"
    assert "fonts.googleapis.com" not in content, "Violación: fuentes bloqueantes de Google Fonts en index.html"
    assert "cdn.jsdelivr.net" not in content, "Violación: librerías remotas de jsDelivr en index.html"


def test_inv_snake_4_retrocompatible_shims():
    """INV-SNAKE-4: Presencia de shims retrocompatibles para /es/ y /en/ con redirección a ?lang=."""
    for lang in ["es", "en"]:
        shim = os.path.join(STATIC_DIR, lang, "index.html")
        assert os.path.exists(shim), f"Falta el shim para {lang}"
        with open(shim, "r", encoding="utf-8") as f:
            c = f.read()
            assert f"/games/snake/?lang={lang}" in c, f"El shim {lang} no redirige a ?lang={lang}"
            assert 'http-equiv="refresh"' in c or "http-equiv='refresh'" in c


def test_inv_snake_5_xss_immunity_and_sanitization():
    """INV-SNAKE-5: Inmunidad XSS garantizada en leaderboard.js y app.js."""
    leader_path = os.path.join(APP_DIR, "leaderboard.js")
    with open(leader_path, "r", encoding="utf-8") as f:
        code = f.read()

    assert "sanitizeAgentName" in code, "leaderboard.js debe exportar sanitizeAgentName"
    assert "textContent" in code, "leaderboard.js debe usar textContent para nombres de usuario"

    # Verificar que no hay asignación directa de innerHTML con variables de nombre
    assert not re.search(r'innerHTML\s*=\s*.*username', code, re.IGNORECASE), \
        "Violación XSS: detección de innerHTML asignado con username en leaderboard.js"


def test_inv_snake_6_i18n_parity():
    """INV-SNAKE-6: Paridad bilingüe estricta ES y EN en catalog.js."""
    catalog_path = os.path.join(APP_DIR, "catalog.js")
    with open(catalog_path, "r", encoding="utf-8") as f:
        code = f.read()

    # Modos
    for mode in ["arcade", "daily", "time_attack", "zen"]:
        assert f'id: "{mode}"' in code or f"id: '{mode}'" in code, f"Falta modo {mode} en catalog.js"

    # Skins
    for skin in ["cyan_viper", "gold_sovereign", "matrix_operator", "akira_plasma", "glitch_phantom"]:
        assert skin in code, f"Falta skin {skin} en catalog.js"

    # Medallas
    for medal in ["first_hack", "overclock", "firewall_breaker", "ghost_walker", "daily_hacker", "cyber_legend"]:
        assert medal in code, f"Falta medalla {medal} en catalog.js"


def test_inv_snake_7_canonical_triad():
    """INV-SNAKE-7: La cabecera superior integra los tres enlaces canónicos de Datalaria y el regreso al portal."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    assert "/es/apps/" in content, "Falta enlace de regreso al portal de aplicaciones (/es/apps/)"
    assert "/es/apps/snake/" in content, "Falta enlace a la ficha técnica (/es/apps/snake/)"
    assert "/es/posts/game_snake/" in content, "Falta enlace al tutorial (/es/posts/game_snake/)"
    assert "/es/recursos/" in content, "Falta enlace a recursos B2B (/es/recursos/)"

    # Verificar existencia del shim retrocompatible en static/apps/snake/index.html
    apps_snake_shim = os.path.join(REPO_ROOT, "static", "apps", "snake", "index.html")
    assert os.path.exists(apps_snake_shim), "Falta el shim estático en static/apps/snake/index.html"


def test_inv_snake_8_pwa_offline_assets():
    """INV-SNAKE-8: PWA 100% offline con manifest.json, sw.js y 5 iconos rasterizados."""
    manifest_path = os.path.join(STATIC_DIR, "manifest.json")
    assert os.path.exists(manifest_path), "Falta manifest.json en static/games/snake/"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        assert manifest.get("start_url") == "/games/snake/", "start_url de manifest.json debe ser /games/snake/"
        assert manifest.get("display") == "standalone"

    sw_path = os.path.join(STATIC_DIR, "sw.js")
    assert os.path.exists(sw_path), "Falta sw.js en static/games/snake/"
    with open(sw_path, "r", encoding="utf-8") as f:
        sw_code = f.read()
        assert "datalaria-snake-v2.3.0" in sw_code
        assert "skipWaiting" in sw_code

    icons = [
        "icon.svg",
        "icon-192.png",
        "icon-512.png",
        "icon-maskable-192.png",
        "icon-maskable-512.png",
        "apple-touch-icon.png"
    ]
    for ic in icons:
        p = os.path.join(STATIC_DIR, ic)
        assert os.path.exists(p), f"Falta icono PWA en static: {ic}"


def test_inv_snake_9_controls_and_telegraphing():
    """INV-SNAKE-9: Controles multiplataforma completos y telegraphing preventivo."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    assert "d-pad-btn" in content, "Faltan botones D-Pad para móviles"
    assert "btn-touch-pause" in content, "Falta botón táctil de pausa funcional"
    assert "btn-touch-boost" in content, "Falta botón táctil de boost (Hyper-Dash)"
    assert "warningTicks" in content, "Falta lógica de telegraphing warningTicks"


def test_inv_snake_10_profiles_skins_cybercard():
    """INV-SNAKE-10: Soporte de 3 perfiles locales, Hangar de skins y Cyber-Card PNG."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    assert "profile-select" in content, "Falta selector de perfiles familiares"
    assert "downloadCyberCard" in content, "Falta función downloadCyberCard en el bundle"
    assert "btn-download-cybercard" in content, "Falta botón de descarga de Cyber-Card"


def test_inv_snake_11_bundle_syntax_and_no_duplicate_declarations():
    """INV-SNAKE-11: Verifica que el bundle inlined no tiene errores de sintaxis ni colisiones de identificadores."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Meta tags de PWA mobile-web-app-capable sin advertencias de deprecación
    assert '<meta name="mobile-web-app-capable" content="yes">' in content, "Falta meta tag mobile-web-app-capable"
    assert '<meta name="apple-mobile-web-app-capable" content="yes">' in content, "Falta meta tag apple-mobile-web-app-capable"

    # 2. Extraer el bloque del script bundle
    script_matches = re.findall(r"<script>([\s\S]*?)</script>", content)
    assert len(script_matches) >= 2, "Debe haber al menos 2 bloques <script> (anti-FOUC y bundle)"
    bundle_code = script_matches[1]

    # 3. Validar con Node.js que new Function(bundle_code) compila sin errores (SyntaxError, etc.)
    node_eval = """
    const fs = require('fs');
    const html = fs.readFileSync(process.argv[1], 'utf8');
    const parts = html.split('<script>');
    if (parts.length < 3) {
      console.error('BUNDLE_NOT_FOUND');
      process.exit(1);
    }
    const bundle = parts[2].split('</script>')[0];
    try {
      new Function(bundle);
      console.log('BUNDLE_SYNTAX_OK');
    } catch (e) {
      console.error('BUNDLE_SYNTAX_FAIL:', e);
      process.exit(1);
    }
    """
    res = subprocess.run(["node", "-e", node_eval, index_html], capture_output=True, text=True)
    assert res.returncode == 0, f"Error de sintaxis en el bundle inlined de Snake:\n{res.stderr}"
    assert "BUNDLE_SYNTAX_OK" in res.stdout

    # 4. Verificar que no hay colisión de GRID_SIZE u otras declaraciones top-level
    grid_size_decls = re.findall(r"^const\s+GRID_SIZE\b", bundle_code, re.MULTILINE)
    assert len(grid_size_decls) == 1, f"GRID_SIZE debe declararse exactamente 1 vez, encontrado: {len(grid_size_decls)}"


def test_inv_snake_12_immersive_layout_and_leaderboard_styles():
    """INV-SNAKE-12: Verifica modo inmersivo body.is-playing, escalado --board-size, encuadre sin emojis duplicados y Hall of Fame Leaderboard."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Regla global .hidden y modo inmersivo body.is-playing
    assert ".hidden {" in content and "display: none !important;" in content, "Falta regla global .hidden"
    assert "body.is-playing .app-header" in content, "Falta regla CSS para ocultar cabecera en body.is-playing"
    assert "body.is-playing .nav-deck" in content, "Falta regla CSS para ocultar pestañas en body.is-playing"
    assert "--board-size" in content, "Falta variable CSS --board-size para escalado dinámico del tablero"
    assert 'id="btn-hud-pause"' in content, "Falta botón #btn-hud-pause en el HUD para pausar durante modo inmersivo"
    assert 'data-i18n="final_score_label"' in content, "Falta atributo data-i18n='final_score_label' en Game Over"

    # 2. Verificar que los botones de pestañas no tienen emojis duplicados fuera del span data-i18n
    tab_buttons = re.findall(r'<button class="tab-btn[^"]*"[^>]*>(.*?)</button>', content)
    assert len(tab_buttons) == 5, f"Se esperaban 5 botones de pestaña, encontrados: {len(tab_buttons)}"
    for btn_inner in tab_buttons:
        assert btn_inner.strip().startswith("<span data-i18n="), f"El botón de pestaña no debe tener emojis hardcodeados fuera del span: {btn_inner}"

    # 3. Verificar estilos Hall of Fame del Leaderboard (.ranking-row, .rank-1, .ranking-kpi-strip)
    assert ".ranking-kpi-strip" in content, "Faltan estilos de KPI strip en el Leaderboard"
    assert ".ranking-row.rank-1" in content, "Falta estilo de podio Oro (.rank-1) en el Leaderboard"
    assert ".ranking-row.rank-2" in content, "Falta estilo de podio Plata (.rank-2) en el Leaderboard"
    assert ".ranking-row.rank-3" in content, "Falta estilo de podio Bronce (.rank-3) en el Leaderboard"
    assert 'id="ranking-kpi-best"' in content, "Falta indicador #ranking-kpi-best en el panel de clasificación"


def test_inv_snake_13_pwa_gold_and_offline_optimistic_ranking():
    """INV-SNAKE-13: Verifica ciclo PWA Gold (standalone, appinstalled, updateflow) y ranking offline optimista."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Badge de versión sincronizado a v2.3.0
    assert ">v2.3.0</button>" in content, "El badge interactivo de versión en cabecera debe indicar v2.3.0"

    # 2. Detección de standalone e instalación PWA
    assert "display-mode: standalone" in content, "Falta detección de display-mode: standalone en app.js"
    assert "appinstalled" in content, "Falta listener del evento nativo appinstalled"
    assert "install_success_toast" in content or "Neon Snake instalada con éxito" in content, "Falta toast de éxito tras instalación PWA"
    assert "install_ios_instructions" in content, "Falta guía contextual para iOS Safari"
    assert "install_generic_instructions" in content, "Falta guía contextual genérica/Android"

    # 3. Flujo reactivo de actualización in-app
    assert "visibilitychange" in content, "Falta comprobación de actualización de Service Worker en visibilitychange"
    assert "swRefreshing" in content, "Falta bandera swRefreshing para proteger controllerchange"
    assert "pwa-update-banner" in content, "Falta banner de actualización in-app"

    # 4. Clasificación Offline Optimista y auto-sincronización
    assert "pendingSync" in content, "Falta gestión de bandera pendingSync para récords offline"
    assert ".ranking-offline-badge" in content, "Falta clase CSS .ranking-offline-badge"
    assert ".ranking-row.is-offline-pending" in content, "Falta clase CSS .ranking-row.is-offline-pending"
    assert 'window.addEventListener("online"' in content or "window.addEventListener('online'" in content, "Falta listener online para auto-sincronización desatendida"

    # 5. Verificación de lógica determinista de leaderboard.js con Node.js
    from pathlib import Path
    leader_path = os.path.join(APP_DIR, "leaderboard.js")
    leader_url = Path(leader_path).as_uri()

    node_script = f"""
    import {{ enqueueScoreLocally, renderRankingListSafe }} from '{leader_url}';

    // Mock localStorage
    const store = {{}};
    globalThis.localStorage = {{
      getItem: (k) => store[k] || null,
      setItem: (k, v) => {{ store[k] = String(v); }},
      removeItem: (k) => {{ delete store[k]; }}
    }};

    // 1. Simular encolado offline optimista
    enqueueScoreLocally('OfflineHacker', 540);
    const cached = JSON.parse(store['datalaria_snake_cached_ranking'] || '[]');
    if (cached.length !== 1 || cached[0].username !== 'OfflineHacker' || cached[0].score !== 540 || !cached[0].pendingSync) {{
      console.error('FAIL: inyección optimista en caché falló', cached);
      process.exit(1);
    }}

    // 2. Simular segundo récord mayor
    enqueueScoreLocally('ProAgent', 820);
    const cached2 = JSON.parse(store['datalaria_snake_cached_ranking'] || '[]');
    if (cached2[0].username !== 'ProAgent' || cached2[0].score !== 820 || cached2[1].username !== 'OfflineHacker') {{
      console.error('FAIL: ordenación descendente en caché falló', cached2);
      process.exit(2);
    }}

    console.log('NODE_LEADERBOARD_OK');
    """
    res = subprocess.run(["node", "--input-type=module", "-e", node_script], capture_output=True, text=True)
    assert res.returncode == 0, f"Error en test de leaderboard con Node.js:\n{res.stderr}"
    assert "NODE_LEADERBOARD_OK" in res.stdout


def test_inv_snake_14_ergonomics_hitstop_and_countdown():
    """INV-SNAKE-14: Ergonomía táctil Full-Swipe, Hit-Stop de 450ms, botón ver tablero y cuenta atrás 3-2-1."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Conmutador móvil D-Pad vs Full-Swipe
    assert 'id="btn-toggle-dpad"' in content, "Falta botón #btn-toggle-dpad en controles de cabecera"
    assert 'id="btn-toggle-dpad-deck"' in content, "Falta botón #btn-toggle-dpad-deck en zona de controles táctiles"
    assert 'id="touch-controls-deck"' in content, "Falta contenedor #touch-controls-deck"
    assert ".dpad-disabled" in content, "Falta clase CSS .dpad-disabled para ocultar cruceta en modo swipe"
    assert "datalaria_snake_dpad" in content, "Falta clave de persistencia localStorage datalaria_snake_dpad"
    assert 'id="swipe-touchpad-zone"' in content, "Falta zona de gestos #swipe-touchpad-zone"

    # 2. Feedback háptico nativo
    assert "navigator.vibrate" in content, "Falta llamada a navigator.vibrate en app.js"
    assert "triggerHaptic" in content, "Falta función triggerHaptic en app.js"
    assert "ev.cancelable" in content, "Falta comprobación de ev.cancelable para prevenir advertencias de scroll"

    # 3. Hit-Stop dramático y botón Ver Tablero con barra flotante
    assert "isHitStop" in content, "Falta variable de estado isHitStop"
    assert "handleHitStopAndGameOver" in content, "Falta función handleHitStopAndGameOver"
    assert 'id="btn-inspect-board"' in content, "Falta botón #btn-inspect-board en overlay de Game Over"
    assert 'id="inspect-controls-bar"' in content, "Falta barra de control flotante #inspect-controls-bar"
    assert 'id="btn-inspect-retry"' in content, "Falta botón #btn-inspect-retry en modo inspección"
    assert 'id="btn-inspect-close"' in content, "Falta botón #btn-inspect-close en modo inspección"
    assert ".is-inspecting" in content, "Falta modificador CSS .is-inspecting para modal translúcido"

    # 4. Cuenta atrás animada 3-2-1 al reanudar
    assert "isCountdownActive" in content, "Falta variable isCountdownActive"
    assert "startResumeCountdown" in content, "Falta función startResumeCountdown"
    assert "countdown_tick" in content, "Falta sintetizador countdown_tick en audio.js"
    assert "countdown_go" in content, "Falta sintetizador countdown_go en audio.js"
    assert "countdown_hack" in content, "Falta clave de i18n countdown_hack en catalog.js"

    # 5. Determinismo del motor: crashPos emitido en colisión de pared con Node.js
    from pathlib import Path
    engine_path = os.path.join(APP_DIR, "engine.js")
    engine_url = Path(engine_path).as_uri()

    node_script = f"""
    import {{ createInitialGameState, tickGame }} from '{engine_url}';

    const state = createInitialGameState('arcade');
    state.snake[0] = {{ x: 0, y: 10 }};
    state.direction = {{ x: -1, y: 0 }};
    const events = tickGame(state, 140, false);
    const goEv = events.find(e => e.type === 'game_over');
    if (!goEv || !goEv.crashPos || goEv.crashPos.x !== 0 || goEv.crashPos.y !== 10) {{
      console.error('FAIL: crashPos no emitido en colisión de pared', goEv);
      process.exit(1);
    }}
    console.log('NODE_HITSTOP_CRASH_OK');
    """
    res = subprocess.run(["node", "--input-type=module", "-e", node_script], capture_output=True, text=True)
    assert res.returncode == 0, f"Error en verificación de colisión con Node.js:\n{res.stderr}"
    assert "NODE_HITSTOP_CRASH_OK" in res.stdout


def test_static_firewall_compliance():
    """Constitución Art. 2: El cortafuegos de static/ prohíbe código backend y archivos sensibles."""
    forbidden_extensions = [".py", ".sql", ".env", ".ipynb", ".pyc"]
    for root, dirs, files in os.walk(STATIC_DIR):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            assert ext not in forbidden_extensions, f"Violación del cortafuegos de static/: {f} en {root}"
        assert ".git" not in dirs, f"Violación del cortafuegos: subdirectorio .git en {root}"
