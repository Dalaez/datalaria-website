"""
apps/maths/tests/test_maths_engine.py
Suite de verificación determinista para Matemáticas Interactivas (Ábaco Arcade v2.1.0).
Valida invariantes INV-MATHS-1 a INV-MATHS-9.
"""
import os
import re
import json
import pytest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATHS_APP_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../../static/apps/maths"))

def test_inv_maths_1_source_files_exist():
    """Verifica que todos los componentes modulares de apps/maths/ existen."""
    required = ["catalog.js", "engine.js", "audio.js", "app.js", "styles.css", "build.py", "manifest.json", "sw.js", "icon.svg"]
    for fname in required:
        fpath = os.path.join(MATHS_APP_DIR, fname)
        assert os.path.exists(fpath), f"Falta el archivo requerido {fname}"

def test_inv_maths_3_zero_external_dependencies():
    """INV-MATHS-3: Cero dependencias externas en runtime (sin Tailwind CDN ni Google Fonts)."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    assert os.path.exists(index_html), "static/apps/maths/index.html debe existir"
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    assert "cdn.tailwindcss.com" not in content, "Violación: presencia de cdn.tailwindcss.com"
    assert "fonts.googleapis.com" not in content, "Violación: presencia de fonts.googleapis.com"
    assert "fonts.gstatic.com" not in content, "Violación: presencia de fonts.gstatic.com"

def test_inv_maths_4_shims_and_zero_orphan_backups():
    """INV-MATHS-4: Presencia de shims retrocompatibles y eliminación de index_backup.html."""
    backup_file = os.path.join(STATIC_DIR, "index_backup.html")
    assert not os.path.exists(backup_file), "index_backup.html no debe existir en static/"

    for lang in ['es', 'en']:
        shim = os.path.join(STATIC_DIR, lang, "index.html")
        assert os.path.exists(shim), f"Falta el shim para {lang}"
        with open(shim, "r", encoding="utf-8") as f:
            c = f.read()
            assert f"/apps/maths/?lang={lang}" in c, f"El shim de {lang} no redirige correctamente"

def test_inv_maths_6_bilingual_parity():
    """INV-MATHS-6: Paridad total de claves i18n en catalog.js."""
    catalog_path = os.path.join(MATHS_APP_DIR, "catalog.js")
    with open(catalog_path, "r", encoding="utf-8") as f:
        code = f.read()

    for lvl in ['l1', 'l2', 'l3', 'l4', 'l5', 'l6']:
        assert f"id: '{lvl}'" in code, f"Falta el nivel {lvl}"

    for mode in ['zen', 'classic', 'time_attack']:
        assert f"id: '{mode}'" in code, f"Falta el modo {mode}"

    for medal in ['first_win', 'streak_5', 'streak_10', 'div_master', 'brain_power', 'time_hero']:
        assert f"id: '{medal}'" in code, f"Falta la medalla {medal}"

    for key in ['install_app', 'install_success', 'stats_reset_toast', 'correct_answer_is', 'next_question_btn']:
        assert f"{key}:" in code, f"Falta la clave i18n {key}"

def test_inv_maths_7_datalaria_shell_links():
    """INV-MATHS-7: Presencia de la Tríada Canónica de Enlaces en el HTML compilado."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    assert 'id="datalaria-back-link"' in content, "Falta botón ← Datalaria"
    assert 'id="link-spec"' in content, "Falta enlace a Ficha App"
    assert 'id="link-post"' in content, "Falta enlace a Historia IA"
    assert 'id="link-kits"' in content, "Falta enlace a Recursos"

def test_inv_maths_8_pwa_offline_resilience():
    """INV-MATHS-8: PWA 100% Offline con manifest.json, sw.js e iconos adaptativos."""
    manifest_path = os.path.join(STATIC_DIR, "manifest.json")
    sw_path = os.path.join(STATIC_DIR, "sw.js")
    icon_path = os.path.join(STATIC_DIR, "icon.svg")

    assert os.path.exists(manifest_path), "Falta static/apps/maths/manifest.json"
    assert os.path.exists(sw_path), "Falta static/apps/maths/sw.js"
    assert os.path.exists(icon_path), "Falta static/apps/maths/icon.svg"

    for icon_name in ["icon.svg", "icon-192.png", "icon-512.png", "icon-maskable-192.png", "icon-maskable-512.png", "apple-touch-icon.png"]:
        p = os.path.join(STATIC_DIR, icon_name)
        assert os.path.exists(p), f"Falta {icon_name} en static/apps/maths/"
        assert os.path.getsize(p) > 500, f"Icono {icon_name} corrupto o vacío"

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data.get("display") == "standalone", "PWA display debe ser standalone"
        assert data.get("start_url") == "/apps/maths/", "start_url inválido"
        maskables = [i for i in data.get("icons", []) if i.get("purpose") == "maskable"]
        assert len(maskables) >= 2, "Debe tener al menos 2 iconos maskables"
        for m in maskables:
            assert "datalaria_logo_transp.png" not in m["src"], "Icono maskable debe ser propio de Maths"
            assert "icon-maskable" in m["src"]

    with open(sw_path, "r", encoding="utf-8") as f:
        sw_code = f.read()
        assert "PRECACHE_ASSETS" in sw_code, "Falta lista de precaché en sw.js"
        assert "/apps/maths/index.html" in sw_code, "index.html no precacheado en sw.js"
        assert "icon-maskable-512.png" in sw_code
        assert "skipWaiting" in sw_code

    # Verificar enlace al manifest en index.html y botón de instalación
    with open(os.path.join(STATIC_DIR, "index.html"), "r", encoding="utf-8") as f:
        index_code = f.read()
        assert 'rel="manifest"' in index_code, "Falta rel=manifest en index.html"
        assert 'id="btn-install-pwa"' in index_code, "Falta botón #btn-install-pwa en cabecera"
        assert 'id="btn-check-update"' in index_code, "Falta botón #btn-check-update en cabecera"
        assert 'setupPwaUpdateFlow' in index_code, "Falta setupPwaUpdateFlow en app.js"
        assert 'apple-touch-icon.png' in index_code, "Falta apple-touch-icon en index.html"
        assert 'datalaria_logo_transp.png' not in index_code

def test_inv_maths_9_anti_fouc_and_persistence():
    """INV-MATHS-9: Persistencia de tema y micro-script anti-FOUC."""
    with open(os.path.join(STATIC_DIR, "index.html"), "r", encoding="utf-8") as f:
        content = f.read()
        assert "localStorage.getItem('pref-theme')" in content, "Falta script anti-FOUC para pref-theme en <head>"
        assert "toast-container" in content, "Falta contenedor para toasts interactivos"

def test_inv_maths_10_daily_seed_determinism():
    """INV-MATHS-10: Determinismo de Semilla en Reto Diario (Mulberry32)."""
    import subprocess
    import json

    # 1. Verificar presencia de componentes en el bundle
    with open(os.path.join(STATIC_DIR, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()
        assert "createSeededRng" in html, "Falta createSeededRng en el bundle compilado"
        assert "btn-share-result" in html, "Falta btn-share-result en el bundle compilado"
        assert "round-blocks-strip" in html, "Falta round-blocks-strip en el bundle compilado"
        assert "mistake-review-section" in html, "Falta mistake-review-section en el bundle compilado"

    # 2. Ejecutar prueba de determinismo con Node.js cargando engine.js
    node_script = """
    const fs = require('fs');
    const path = require('path');
    const engineCode = fs.readFileSync(path.join(process.cwd(), 'apps/maths/engine.js'), 'utf8');
    
    // Evaluar en contexto global simulando window.MathsEngine
    const window = {};
    eval(engineCode);
    const engine = window.MathsEngine;

    const seed = '2026-11-06_l3';
    
    // Generar secuencia 1
    const rng1 = engine.createSeededRng(seed);
    const seq1 = [];
    for (let i = 0; i < 10; i++) {
        seq1.push(engine.generateProblem('l3', 'es', rng1).display);
    }

    // Generar secuencia 2 con la misma semilla
    const rng2 = engine.createSeededRng(seed);
    const seq2 = [];
    for (let i = 0; i < 10; i++) {
        seq2.push(engine.generateProblem('l3', 'es', rng2).display);
    }

    // Generar secuencia 3 con diferente fecha
    const rng3 = engine.createSeededRng('2026-11-07_l3');
    const seq3 = [];
    for (let i = 0; i < 10; i++) {
        seq3.push(engine.generateProblem('l3', 'es', rng3).display);
    }

    console.log(JSON.stringify({
        match: JSON.stringify(seq1) === JSON.stringify(seq2),
        seq1,
        diff: JSON.stringify(seq1) !== JSON.stringify(seq3)
    }));
    """
    proc = subprocess.run(["node", "-e", node_script], capture_output=True, text=True)
    assert proc.returncode == 0, f"Error ejecutando node: {proc.stderr}"
    res = json.loads(proc.stdout.strip())
    assert res["match"] is True, f"Las secuencias generadas con la misma semilla no coinciden: {res}"
    assert res["diff"] is True, "Dos fechas distintas produjeron la misma secuencia (falta variabilidad)"
    assert len(res["seq1"]) == 10, "No se generaron exactamente 10 problemas"

def test_inv_maths_11_profiles_and_diploma():
    """INV-MATHS-11: Perfiles Familiares Multi-Jugador y Generador de Diploma Arcade PNG."""
    # 1. Verificar catálogo y perfiles
    with open(os.path.join(MATHS_APP_DIR, "catalog.js"), "r", encoding="utf-8") as f:
        catalog_code = f.read()
        assert "player_1" in catalog_code
        assert "player_2" in catalog_code
        assert "adult" in catalog_code
        assert "🦁" in catalog_code
        assert "🦊" in catalog_code
        assert "🦉" in catalog_code
        assert "download_diploma_btn" in catalog_code
        assert "diploma_card_title" in catalog_code

    # 2. Verificar presencia de componentes en el bundle compilado
    with open(os.path.join(STATIC_DIR, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()
        assert 'id="profile-bar"' in html, "Falta #profile-bar en el HTML compilado"
        assert 'profile-chip' in html, "Falta clase profile-chip en index.html"
        assert 'btn-arcade-diploma' in html, "Falta clase btn-arcade-diploma en index.html"
        assert 'downloadArcadeDiploma' in html, "Falta downloadArcadeDiploma en index.html"
        assert 'datalaria_maths_v2_stats_' in html, "Falta clave aislada por perfil en index.html"
        assert 'diploma-promo-card' in html, "Falta diploma-promo-card en index.html"

def test_inv_maths_12_generate_problem_null_rng_robustness():
    """Verifica que generateProblem es 100% inmune a rng=null, undefined o ausente en todos los niveles."""
    import subprocess
    import json

    node_script = """
    const fs = require('fs');
    const path = require('path');
    const engineCode = fs.readFileSync(path.join(process.cwd(), 'apps/maths/engine.js'), 'utf8');
    
    const window = {};
    eval(engineCode);
    const engine = window.MathsEngine;

    const levels = ['l1', 'l2', 'l3', 'l4', 'l5', 'l6'];
    const results = [];

    for (const lvl of levels) {
      // 1. Probar con null explícito (causa raíz del bug reportado)
      const pNull = engine.generateProblem(lvl, 'es', null);
      if (!pNull || !pNull.display) throw new Error(`Fallo con null en ${lvl}`);

      // 2. Probar con undefined
      const pUndef = engine.generateProblem(lvl, 'es', undefined);
      if (!pUndef || !pUndef.display) throw new Error(`Fallo con undefined en ${lvl}`);

      // 3. Probar sin 3er argumento
      const pNone = engine.generateProblem(lvl, 'es');
      if (!pNone || !pNone.display) throw new Error(`Fallo sin 3er arg en ${lvl}`);

      results.push({ lvl, ok: true });
    }

    console.log(JSON.stringify({ success: true, count: results.length }));
    """
    proc = subprocess.run(["node", "-e", node_script], capture_output=True, text=True)
    assert proc.returncode == 0, f"Fallo en robustez de engine: {proc.stderr}"
    res = json.loads(proc.stdout.strip())
    assert res["success"] is True
    assert res["count"] == 6



