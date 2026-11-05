"""apps/conversor/build.py
Compilador determinista del Conversor de Unidades v2.0.0
Genera static/apps/conversor/index.html y los 14 shims de retrocompatibilidad SEO.
Datalaria Helix — Single Source of Truth
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_DIR = REPO_ROOT / "apps" / "conversor"
STATIC_DIR = REPO_ROOT / "static" / "apps" / "conversor"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def generate_shim_html(target_url: str, title: str, lang: str) -> str:
    msg_es = "Redirigiendo al nuevo Conversor de Unidades v2.0..."
    msg_en = "Redirecting to the new Unit Converter v2.0..."
    msg = msg_es if lang == "es" else msg_en
    link_text = "Pulsa aquí si no eres redirigido" if lang == "es" else "Click here if not redirected"

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Datalaria</title>
    <meta http-equiv="refresh" content="0; url={target_url}">
    <link rel="canonical" href="https://datalaria.com{target_url}">
    <script>window.location.replace("{target_url}");</script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #0b0f17;
            color: #94a3b8;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            text-align: center;
        }}
        a {{ color: #0ea5e9; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div>
        <p>{msg}</p>
        <p><a href="{target_url}">{link_text}</a></p>
    </div>
</body>
</html>
"""


def build():
    print(f"[*] Construyendo Conversor v2.0.0 desde {SRC_DIR}...")
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    (STATIC_DIR / "es").mkdir(parents=True, exist_ok=True)
    (STATIC_DIR / "en").mkdir(parents=True, exist_ok=True)

    catalog_code = read_file(SRC_DIR / "catalog.js")
    engine_code = read_file(SRC_DIR / "engine.js")
    app_code = read_file(SRC_DIR / "app.js")
    css_code = read_file(SRC_DIR / "styles.css")

    # Inlining into index.html
    # To inline ES modules cleanly without import/export syntax clashes:
    # Remove 'export ' keywords from catalog.js and engine.js, and remove import statements in app.js
    clean_catalog = catalog_code.replace("export const ", "const ")
    clean_engine = (
        engine_code.replace("export const ", "const ")
        .replace("export function ", "function ")
    )
    clean_app = re.sub(r'import\s+{[^}]+}\s+from\s+[\'"][^\'"]+[\'"];?\n?', '', app_code)
    clean_app = clean_app.replace("export class UnitConverterApp", "class UnitConverterApp")

    index_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conversor Universal Pro — Engineering Workbench v2.1 | Datalaria</title>
    <meta name="description" content="Navaja suiza digital para conversiones científicas y técnicas en 6 disciplinas de ingeniería. Precisión SI/CODATA 2022, formato de separadores numéricos y batch scratchpad.">
    <link rel="canonical" href="https://datalaria.com/apps/conversor/">
    <link rel="manifest" href="/apps/conversor/manifest.json">
    <meta name="theme-color" content="#0b0f17" media="(prefers-color-scheme: dark)">
    <meta name="theme-color" content="#f8fafc" media="(prefers-color-scheme: light)">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Conversor Pro">
    <link rel="icon" type="image/svg+xml" href="/apps/conversor/icon.svg">
    <link rel="apple-touch-icon" href="/apps/conversor/datalaria_logo_transp.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@600;700&display=swap" rel="stylesheet">
    <style>
{css_code}
    </style>
    <script>
        (function() {{
            var saved = localStorage.getItem('pref-theme') || localStorage.getItem('datalaria_theme');
            var isDark = saved === 'dark' || (!saved && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) || !saved;
            var theme = isDark ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', theme);
            if (theme === 'dark') {{
                document.documentElement.classList.add('dark');
            }} else {{
                document.documentElement.classList.remove('dark');
            }}
        }})();
    </script>
</head>
<body>
    <header id="app-header" class="app-header"></header>

    <main class="workbench-container">
        <nav id="categories-nav" class="categories-nav" aria-label="Categorías"></nav>

        <section id="constants-bar" class="constants-bar" aria-label="Constantes CODATA"></section>

        <!-- Conversor Estándar -->
        <section id="main-converter-card" class="converter-card" style="display: none;"></section>

        <!-- Batch Scratchpad -->
        <section id="scratchpad-card" style="display: none;"></section>

        <!-- Historial Reciente -->
        <section id="history-strip" class="history-strip" style="display: none;"></section>

        <!-- Sección Didáctica -->
        <article id="didactic-card" class="didactic-section"></article>
    </main>

    <footer class="app-footer">
        <p>Una herramienta de <a href="https://datalaria.com">Datalaria</a> · Precisión SI/CODATA 2022 · 100% Client-Side</p>
    </footer>

    <script type="module">
{clean_catalog}

{clean_engine}

{clean_app}

document.addEventListener('DOMContentLoaded', () => {{
    const app = new UnitConverterApp();
    app.init();
    window._datalariaConversorApp = app;
}});
    </script>
</body>
</html>
"""

    (STATIC_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"  [+] Generado static/apps/conversor/index.html ({len(index_html)} bytes)")

    # Shims retrocompatibles
    shims_es = [
        ("index.html", "/apps/conversor/?lang=es", "Conversor Universal Pro"),
        ("dimension.html", "/apps/conversor/?lang=es&cat=dimension", "Conversor de Dimensión"),
        ("energia.html", "/apps/conversor/?lang=es&cat=energia", "Conversor de Energía"),
        ("tiempo.html", "/apps/conversor/?lang=es&cat=tiempo", "Conversor de Tiempo"),
        ("mecanica.html", "/apps/conversor/?lang=es&cat=mecanica", "Conversor de Mecánica"),
        ("informatica.html", "/apps/conversor/?lang=es&cat=informatica", "Conversor de Informática"),
        ("radiofrecuencia.html", "/apps/conversor/?lang=es&cat=radiofrecuencia", "Conversor de Radiofrecuencia"),
    ]

    for filename, target, title in shims_es:
        shim_path = STATIC_DIR / "es" / filename
        shim_path.write_text(generate_shim_html(target, title, "es"), encoding="utf-8")
        print(f"  [+] Shim ES: {shim_path.relative_to(REPO_ROOT)} -> {target}")

    shims_en = [
        ("index.html", "/apps/conversor/?lang=en", "Universal Converter Pro"),
        ("dimension_en.html", "/apps/conversor/?lang=en&cat=dimension", "Dimension Converter"),
        ("energia_en.html", "/apps/conversor/?lang=en&cat=energia", "Energy Converter"),
        ("tiempo_en.html", "/apps/conversor/?lang=en&cat=tiempo", "Time Converter"),
        ("mecanica_en.html", "/apps/conversor/?lang=en&cat=mecanica", "Mechanics Converter"),
        ("informatica_en.html", "/apps/conversor/?lang=en&cat=informatica", "Data Converter"),
        ("radiofrecuencia_en.html", "/apps/conversor/?lang=en&cat=radiofrecuencia", "Radiofrequency Converter"),
    ]

    for filename, target, title in shims_en:
        shim_path = STATIC_DIR / "en" / filename
        shim_path.write_text(generate_shim_html(target, title, "en"), encoding="utf-8")
        print(f"  [+] Shim EN: {shim_path.relative_to(REPO_ROOT)} -> {target}")

    # PWA Assets
    for pwa_file in ["manifest.json", "sw.js", "icon.svg"]:
        src_pwa = SRC_DIR / pwa_file
        if src_pwa.exists():
            (STATIC_DIR / pwa_file).write_text(src_pwa.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"  [+] PWA Asset: static/apps/conversor/{pwa_file}")

    print("[OK] Build de Conversor v2.1.0 completado con exito.")


if __name__ == "__main__":
    build()
