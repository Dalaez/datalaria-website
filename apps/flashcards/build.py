# apps/flashcards/build.py
# Compilador y Empaquetador Determinista Single-Source-of-Truth
# Datalaria Flashcards AI ("Mazo Mágico v2.1.0")

import os
import re
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
STATIC_DEST = REPO_ROOT / "static" / "apps" / "flashcards"

def strip_es_modules(code: str) -> str:
    """Elimina imports y convierte exports en declaraciones locales para inlining."""
    # Eliminar sentencias import ... from '...'; o import '...';
    code = re.sub(r"^\s*import\s+[^;]+;\s*$", "", code, flags=re.MULTILINE)
    # Reemplazar export const/let/var/function/async function/class por su declaración normal
    code = re.sub(r"^\s*export\s+(const|let|var|function|async\s+function|class)\s+", r"\1 ", code, flags=re.MULTILINE)
    return code

def build():
    print(f"[build.py] Compilando Flashcards AI v2.1.0 desde {BASE_DIR} hacia {STATIC_DEST}...")
    STATIC_DEST.mkdir(parents=True, exist_ok=True)

    # 1. Leer estilos y módulos JS
    with open(BASE_DIR / "styles.css", "r", encoding="utf-8") as f:
        styles_css = f.read()

    js_files = ["catalog.js", "engine.js", "ai.js", "audio.js", "app.js"]
    bundled_parts = []
    for jf in js_files:
        with open(BASE_DIR / jf, "r", encoding="utf-8") as f:
            content = f.read()
            bundled_parts.append(f"// --- INLINE BUNDLE: {jf} ---\n" + strip_es_modules(content))

    bundled_js = "\n\n".join(bundled_parts)

    # 2. Generar index.html canónico inlined
    index_html_content = f"""<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Flashcards Mágico · Datalaria</title>
  <meta name="description" content="Estudio activo bilingüe, pronunciación fonética por voz y generador con IA.">
  <meta name="theme-color" content="#8b5cf6">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <link rel="manifest" href="/apps/flashcards/manifest.json">
  <link rel="icon" type="image/svg+xml" href="/apps/flashcards/icon.svg">
  <link rel="alternate icon" type="image/png" href="/apps/flashcards/icon-192.png">
  <link rel="apple-touch-icon" href="/apps/flashcards/apple-touch-icon.png">
  <!-- Micro-script Anti-FOUC inyectado en <head> -->
  <script>
    (function() {{
      try {{
        const saved = localStorage.getItem('pref-theme') ||
          (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', saved);
      }} catch (e) {{}}
    }})();
  </script>
  <style>
{styles_css}
  </style>
</head>
<body>
  <header id="app-header" class="app-header"></header>
  <nav id="nav-deck" class="nav-deck"></nav>
  <main id="app-container" class="app-container"></main>
  <canvas id="confetti-canvas"></canvas>
  <div id="toast-container" class="toast-container"></div>
  <footer class="app-footer">
    <p>Datalaria Flashcards AI · Una herramienta educativa abierta para niños y adultos</p>
  </footer>

  <script>
{bundled_js}
  </script>
</body>
</html>
"""

    with open(STATIC_DEST / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html_content)
    print("  -> Generado index.html canónico 100% inline con Anti-FOUC, #toast-container y bundle JS.")

    # 3. Copiar PWA assets e iconos a static/apps/flashcards/
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
            print(f"  -> Copiado asset {filename}")
        else:
            print(f"  -> [AVISO] Asset no encontrado: {src}")

    # 4. Limpiar módulos .js y .css sueltos de static/apps/flashcards/
    loose_files = ["catalog.js", "engine.js", "ai.js", "audio.js", "styles.css", "app.js"]
    for filename in loose_files:
        target = STATIC_DEST / filename
        if target.exists():
            target.unlink()
            print(f"  -> Limpiado archivo suelto {filename} de static/")

    # 5. Shims de redirección SEO retrocompatibles en es/ y en/
    shim_es_dir = STATIC_DEST / "es"
    shim_en_dir = STATIC_DEST / "en"
    shim_es_dir.mkdir(parents=True, exist_ok=True)
    shim_en_dir.mkdir(parents=True, exist_ok=True)

    shim_es_html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Redirigiendo a Flashcards Mágico...</title>
  <meta http-equiv="refresh" content="0; url=/apps/flashcards/?lang=es">
  <link rel="canonical" href="https://datalaria.com/apps/flashcards/?lang=es">
</head>
<body>
  <p>Redirigiendo a la versión actualizada de Flashcards... Si no eres redirigido, <a href="/apps/flashcards/?lang=es">pulsa aquí</a>.</p>
</body>
</html>
"""
    with open(shim_es_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(shim_es_html)

    shim_en_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Redirecting to Magic Flashcards...</title>
  <meta http-equiv="refresh" content="0; url=/apps/flashcards/?lang=en">
  <link rel="canonical" href="https://datalaria.com/apps/flashcards/?lang=en">
</head>
<body>
  <p>Redirecting to the updated Magic Flashcards app... If not redirected, <a href="/apps/flashcards/?lang=en">click here</a>.</p>
</body>
</html>
"""
    with open(shim_en_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(shim_en_html)

    # 6. Asegurar plantillas CSV descargables en es/ y en/
    csv_es_content = "Término,Definición/Traducción,Fonética,Pista\nArticulación,Joint,/dʒɔɪnt/,Unión de dos huesos\nColumna vertebral,Spinal column,/ˈspaɪ.nəl ˈkɒl.əm/,Eje central\nCráneo,Skull,/skʌl/,Protege el cerebro\nCostillas,Ribs,/rɪbz/,Protegen el tórax\n"
    with open(shim_es_dir / "plantilla_flashcards.csv", "w", encoding="utf-8") as f:
        f.write(csv_es_content)

    csv_en_content = "Term,Definition/Translation,Phonetic,Hint\nJoint,Articulación,/dʒɔɪnt/,Connection between bones\nSpinal column,Columna vertebral,/ˈspaɪ.nəl ˈkɒl.əm/,Central axis\nSkull,Cráneo,/skʌl/,Protects the brain\nRibs,Costillas,/rɪbz/,Protects the chest\n"
    with open(shim_en_dir / "flashcards_template.csv", "w", encoding="utf-8") as f:
        f.write(csv_en_content)

    print("  -> Shims SEO retrocompatibles y plantillas CSV sincronizadas.")
    print("Build completado con éxito.")

if __name__ == "__main__":
    build()
