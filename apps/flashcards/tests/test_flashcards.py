"""
apps/flashcards/tests/test_flashcards.py
Suite de verificación determinista para Flashcards AI ("Mazo Mágico v2.0").
Valida las invariantes de dominio INV-FLASH-1 a INV-FLASH-9.
"""

import os
import re
import json
import pytest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
REPO_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../../.."))
STATIC_DIR = os.path.join(REPO_ROOT, "static", "apps", "flashcards")


def test_inv_flash_1_source_files_exist():
    """INV-FLASH-1: Verifica que todos los componentes modulares de apps/flashcards/ existen."""
    required = [
        "catalog.js",
        "engine.js",
        "ai.js",
        "audio.js",
        "styles.css",
        "app.js",
        "icon.svg",
        "manifest.json",
        "sw.js",
        "build.py"
    ]
    for fname in required:
        fpath = os.path.join(APP_DIR, fname)
        assert os.path.exists(fpath), f"Falta el archivo fuente obligatorio: {fname}"


def test_inv_flash_2_speech_and_gemini_batch():
    """INV-FLASH-2: Verifica síntesis Web Speech API y endpoint Gemini actualizado en batch JSON."""
    audio_path = os.path.join(APP_DIR, "audio.js")
    with open(audio_path, "r", encoding="utf-8") as f:
        audio_code = f.read()

    assert "speechSynthesis" in audio_code, "Falta integración con Web Speech API en audio.js"
    assert "SpeechSynthesisUtterance" in audio_code, "Falta SpeechSynthesisUtterance en audio.js"
    assert "0.75" in audio_code, "Falta soporte para velocidad modo tortuga (0.75x) en audio.js"

    ai_path = os.path.join(APP_DIR, "ai.js")
    with open(ai_path, "r", encoding="utf-8") as f:
        ai_code = f.read()

    assert "gemini-2.5-flash" in ai_code, "ai.js debe utilizar gemini-2.5-flash como modelo primario"
    assert "gemini-2.5-flash-preview-05-20" not in ai_code, "ai.js no debe utilizar preview expirado de mayo 2025"
    assert "responseMimeType: 'application/json'" in ai_code or 'responseMimeType: "application/json"' in ai_code, \
        "ai.js debe solicitar JSON estructurado nativo"


def test_inv_flash_3_zero_external_dependencies():
    """INV-FLASH-3: Cero dependencias externas en runtime (sin Tailwind CDN ni Giphy externos)."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    assert os.path.exists(index_html), "static/apps/flashcards/index.html debe existir"
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    assert "cdn.tailwindcss.com" not in content, "Violación: presencia de cdn.tailwindcss.com en index.html"
    assert "media.giphy.com" not in content, "Violación: presencia de GIFs externos de Giphy en index.html"
    assert "fonts.googleapis.com" not in content, "Violación: fuentes bloqueantes de Google Fonts en index.html"


def test_inv_flash_4_shims_and_templates():
    """INV-FLASH-4: Presencia de shims retrocompatibles con charset UTF-8 y plantillas CSV."""
    for lang in ['es', 'en']:
        shim = os.path.join(STATIC_DIR, lang, "index.html")
        assert os.path.exists(shim), f"Falta el shim para {lang}"
        with open(shim, "r", encoding="utf-8") as f:
            c = f.read()
            assert f"/apps/flashcards/?lang={lang}" in c, f"El shim {lang} no redirige a ?lang={lang}"
            assert 'charset="UTF-8"' in c or "charset='UTF-8'" in c or 'charset="utf-8"' in c, \
                f"El shim {lang} tiene un charset incorrecto (posible residuo UTF-g)"
            assert "UTF-g" not in c, f"Corrupción UTF-g detectada en shim {lang}"

    # Plantillas CSV
    csv_es = os.path.join(STATIC_DIR, "es", "plantilla_flashcards.csv")
    csv_en = os.path.join(STATIC_DIR, "en", "flashcards_template.csv")
    assert os.path.exists(csv_es), "Falta plantilla_flashcards.csv en static/apps/flashcards/es/"
    assert os.path.exists(csv_en), "Falta flashcards_template.csv en static/apps/flashcards/en/"
    assert os.path.getsize(csv_es) > 20, "Plantilla CSV en español vacía"
    assert os.path.getsize(csv_en) > 20, "Plantilla CSV en inglés vacía"


def test_inv_flash_5_firewall_static():
    """INV-FLASH-5: Firewall estricto de static/ (cero archivos .py, .env, .git o temporales)."""
    violations = []
    for root, _, files in os.walk(STATIC_DIR):
        for f in files:
            if f.endswith((".py", ".env", ".sql", ".pyc", ".ipynb")):
                violations.append(os.path.join(root, f))
    assert not violations, f"Violación del firewall estricto de static/: {violations}"


def test_inv_flash_6_bilingual_parity():
    """INV-FLASH-6: Paridad total bilingüe en los 6 mazos y en el diccionario i18n."""
    catalog_path = os.path.join(APP_DIR, "catalog.js")
    with open(catalog_path, "r", encoding="utf-8") as f:
        code = f.read()

    # 6 mazos obligatorios
    expected_decks = ['body_science', 'space_nature', 'world_capitals', 'business_english', 'ai_concepts', 'mba_strategy']
    for deck_id in expected_decks:
        assert f"id: '{deck_id}'" in code, f"Falta el mazo {deck_id} en catalog.js"

    # 3 modos de estudio
    for mode in ['flip', 'quiz', 'spelling']:
        assert f"id: '{mode}'" in code, f"Falta el modo de estudio {mode} en catalog.js"

    # Claves esenciales en ambos idiomas
    assert "es: {" in code and "en: {" in code, "Falta bloque bilingüe i18n en catalog.js"
    for key in ['appTitle', 'tabStudy', 'tabCreator', 'tabStats', 'btnStartStudy', 'speakSlow', 'summaryMastered']:
        assert f"{key}:" in code, f"Falta la clave i18n {key} en catalog.js"


def test_inv_flash_7_shell_and_html_elements():
    """INV-FLASH-7: Presencia de los contenedores institucionales, Toasts, Canvas y bundle inline."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    assert 'id="app-header"' in content, "Falta header institucional #app-header"
    assert 'id="nav-deck"' in content, "Falta barra de navegación #nav-deck"
    assert 'id="app-container"' in content, "Falta contenedor principal #app-container"
    assert 'id="confetti-canvas"' in content, "Falta canvas de confeti #confetti-canvas"
    assert 'id="toast-container"' in content, "Falta contenedor flotante #toast-container"
    assert 'btn-check-update' in content, "Falta soporte de botón interactivo #btn-check-update"
    assert 'btn-install-pwa' in content, "Falta botón multi-plataforma #btn-install-pwa"
    assert 'class FlashcardsApp' in content, "El bundle de JS debe estar incrustado inline en index.html"
    assert '<script type="module" src="./app.js">' not in content, "No deben existir scripts modulares externos sueltos"


def test_inv_flash_8_pwa_offline_assets():
    """INV-FLASH-8: PWA 100% Offline con manifest.json, sw.js v2.1.0, suite de iconos maskable y PNGs."""
    manifest_path = os.path.join(STATIC_DIR, "manifest.json")
    sw_path = os.path.join(STATIC_DIR, "sw.js")
    icon_path = os.path.join(STATIC_DIR, "icon.svg")

    assert os.path.exists(manifest_path), "Falta static/apps/flashcards/manifest.json"
    assert os.path.exists(sw_path), "Falta static/apps/flashcards/sw.js"
    assert os.path.exists(icon_path), "Falta static/apps/flashcards/icon.svg"

    # Verificar suite de iconos PNG generados y optimizados
    expected_pngs = [
        "icon-192.png",
        "icon-512.png",
        "icon-maskable-192.png",
        "icon-maskable-512.png",
        "apple-touch-icon.png"
    ]
    for png in expected_pngs:
        png_path = os.path.join(STATIC_DIR, png)
        assert os.path.exists(png_path), f"Falta el icono PWA {png} en static/"
        assert os.path.getsize(png_path) > 500, f"El icono PWA {png} parece corrupto o vacío"

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data.get("display") == "standalone", "PWA display debe ser standalone"
        assert data.get("start_url") == "/apps/flashcards/", "start_url debe ser /apps/flashcards/"
        icons = data.get("icons", [])
        icon_srcs = [i.get("src") for i in icons]
        assert any("icon.svg" in s for s in icon_srcs), "El icono SVG debe estar en manifest.json"
        assert any("icon-maskable-192.png" in s for s in icon_srcs), "Falta icon-maskable-192.png en manifest.json"
        assert any("icon-maskable-512.png" in s for s in icon_srcs), "Falta icon-maskable-512.png en manifest.json"

    with open(sw_path, "r", encoding="utf-8") as f:
        sw_code = f.read()
        assert "datalaria-flashcards-v2.1.0" in sw_code, "sw.js debe definir la versión v2.1.0"
        assert "caches.open" in sw_code, "sw.js debe gestionar caché offline"
        assert "skipWaiting" in sw_code, "sw.js debe escuchar el mensaje skipWaiting"
        assert "icon-maskable-192.png" in sw_code, "sw.js debe precachear los iconos maskable"


def test_inv_flash_9_anti_fouc_script():
    """INV-FLASH-9: Micro-script en <head> para evitar parpadeo de tema (Anti-FOUC)."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    assert "pref-theme" in content, "Falta script anti-FOUC leyendo pref-theme en <head>"
    assert "data-theme" in content, "El script anti-FOUC debe configurar el atributo data-theme en <head>"
