"""
apps/reading/build.py
Empaquetador estático para la aplicación Lector Arcade v1.0.0 (Reading).
Genera static/apps/reading/index.html (SPA autocontenida sin CDNs),
sincroniza manifest.json, sw.js, 6 iconos SVG/PNG y los 2 shims retrocompatibles es/ y en/.
"""
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../static/apps/reading"))


def build():
    print("Iniciando build de Lector Arcade v1.0.0...")

    with open(os.path.join(BASE_DIR, "styles.css"), "r", encoding="utf-8") as f:
        styles_css = f.read()
    with open(os.path.join(BASE_DIR, "catalog.js"), "r", encoding="utf-8") as f:
        catalog_js = f.read()
    with open(os.path.join(BASE_DIR, "engine.js"), "r", encoding="utf-8") as f:
        engine_js = f.read()
    with open(os.path.join(BASE_DIR, "audio.js"), "r", encoding="utf-8") as f:
        audio_js = f.read()
    with open(os.path.join(BASE_DIR, "app.js"), "r", encoding="utf-8") as f:
        app_js = f.read()

    html_content = f"""<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Lector Arcade — Aprendizaje de Lectura (Datalaria)</title>
  <meta name="theme-color" content="#0284c7">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <link rel="manifest" href="/apps/reading/manifest.json">
  <link rel="icon" type="image/svg+xml" href="/apps/reading/icon.svg">
  <link rel="alternate icon" type="image/png" href="/apps/reading/icon-192.png">
  <link rel="apple-touch-icon" href="/apps/reading/apple-touch-icon.png">
  <script>
    // Script Anti-FOUC para tema visual instantáneo (INV-READ-9)
    (function() {{
      try {{
        var savedTheme = localStorage.getItem('pref-theme');
        if (savedTheme === 'dark' || (!savedTheme && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
          document.documentElement.setAttribute('data-theme', 'dark');
        }} else {{
          document.documentElement.setAttribute('data-theme', 'light');
        }}
      }} catch (e) {{}}
    }})();
  </script>
  <style>
{styles_css}
  </style>
</head>
<body>
  <header class="datalaria-shell">
    <div class="shell-left">
      <a id="datalaria-back-link" href="/es/apps/" class="btn-arcade">← Datalaria</a>
      <a href="/apps/reading/" class="shell-brand">
        <span>📖</span>
        <span id="shell-app-title">Lector Arcade</span>
      </a>
      <button id="btn-check-update" type="button" class="shell-badge" title="Buscar actualizaciones (v1.0.0)">v1.0.0</button>
    </div>

    <div class="shell-right">
      <button id="btn-install-pwa" type="button" class="btn-arcade btn-arcade-install" style="display: none;" title="Instalar en pantalla de inicio">
        <span>📲</span> <span id="label-install-btn">Instalar App</span>
      </button>
      <button id="sound-btn" type="button" class="btn-arcade" title="Sonido (M)">🔊</button>
      <button id="theme-btn" type="button" class="btn-arcade" title="Tema (T)">☀️/🌙</button>
      <button id="lang-btn" type="button" class="btn-arcade" style="font-weight: 700;">🇪🇸 ES</button>
      <a id="link-spec" href="/es/apps/reading/" class="btn-arcade">📋 Ficha App</a>
      <a id="link-post" href="/es/posts/" class="btn-arcade">📖 Historia IA</a>
      <a id="link-kits" href="/es/recursos/" class="btn-arcade btn-arcade-primary">📦 Recursos</a>
    </div>
  </header>

  <!-- Selector de Perfiles Familiares Multi-Jugador (INV-READ-11) -->
  <div id="profile-bar" class="profile-bar"></div>

  <nav class="tabs-nav" id="tabs-nav"></nav>

  <main class="container">
    <div id="tab-content"></div>
  </main>

  <!-- Contenedor global de Toasts -->
  <div id="toast-container" class="toast-container"></div>

  <script>
{catalog_js}
{engine_js}
{audio_js}
{app_js}
  </script>
</body>
</html>
"""

    os.makedirs(STATIC_DIR, exist_ok=True)
    out_index = os.path.join(STATIC_DIR, "index.html")
    with open(out_index, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generado {out_index} ({len(html_content)} bytes)")

    pwa_files = [
        "manifest.json",
        "sw.js",
        "icon.svg",
        "icon-192.png",
        "icon-512.png",
        "icon-maskable-192.png",
        "icon-maskable-512.png",
        "apple-touch-icon.png",
    ]
    for pwa_file in pwa_files:
        src = os.path.join(BASE_DIR, pwa_file)
        dst = os.path.join(STATIC_DIR, pwa_file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copiado PWA asset {pwa_file} a static/apps/reading/")

    backup_path = os.path.join(STATIC_DIR, "index_backup.html")
    if os.path.exists(backup_path):
        os.remove(backup_path)
        print(f"Eliminado archivo huérfano {backup_path}")

    shim_template = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=/apps/reading/?lang={lang}">
  <title>Redireccionando...</title>
  <script>
    window.location.replace('/apps/reading/?lang={lang}');
  </script>
</head>
<body>
  <p>Redirigiendo a <a href="/apps/reading/?lang={lang}">Lector Arcade v1.0.0</a>...</p>
</body>
</html>
"""
    for l_code in ["es", "en"]:
        shim_dir = os.path.join(STATIC_DIR, l_code)
        os.makedirs(shim_dir, exist_ok=True)
        shim_file = os.path.join(shim_dir, "index.html")
        with open(shim_file, "w", encoding="utf-8") as f:
            f.write(shim_template.format(lang=l_code))
        print(f"Generado shim retrocompatible {shim_file}")

    print("Build de Lector Arcade completado con éxito.")


if __name__ == "__main__":
    build()
