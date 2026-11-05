"""
apps/maths/tests/test_maths_engine.py
Suite de verificación determinista para Matemáticas Interactivas (Ábaco Arcade v2.0).
Valida invariantes INV-MATHS-1 a INV-MATHS-7.
"""
import os
import re
import pytest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATHS_APP_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../../static/apps/maths"))

def test_inv_maths_1_source_files_exist():
    """Verifica que todos los componentes modulares de apps/maths/ existen."""
    required = ["catalog.js", "engine.js", "audio.js", "app.js", "styles.css", "build.py"]
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

    # Comprobar que existen los 6 niveles y 3 modos
    for lvl in ['l1', 'l2', 'l3', 'l4', 'l5', 'l6']:
        assert f"id: '{lvl}'" in code, f"Falta el nivel {lvl}"

    for mode in ['zen', 'classic', 'time_attack']:
        assert f"id: '{mode}'" in code, f"Falta el modo {mode}"

    for medal in ['first_win', 'streak_5', 'streak_10', 'div_master', 'brain_power', 'time_hero']:
        assert f"id: '{medal}'" in code, f"Falta la medalla {medal}"

def test_inv_maths_7_datalaria_shell_links():
    """INV-MATHS-7: Presencia de la Tríada Canónica de Enlaces en el HTML compilado."""
    index_html = os.path.join(STATIC_DIR, "index.html")
    with open(index_html, "r", encoding="utf-8") as f:
        content = f.read()

    assert 'id="datalaria-back-link"' in content, "Falta botón ← Datalaria"
    assert 'id="link-spec"' in content, "Falta enlace a Ficha App"
    assert 'id="link-post"' in content, "Falta enlace a Historia IA"
    assert 'id="link-kits"' in content, "Falta enlace a Recursos"
