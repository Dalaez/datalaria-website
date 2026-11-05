"""
apps/maths/build.py
Empaquetador estático para la aplicación Ábaco Arcade v2.1.0 (Maths).
Genera static/apps/maths/index.html, sincroniza manifest.json, sw.js, icon.svg y los 2 shims retrocompatibles.
"""
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../static/apps/maths"))

def build():
    print("Iniciando build de Maths v2.1.0...")
    
    # Leer componentes
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

    # Template HTML con PWA manifest y script Anti-FOUC
    html_content = f"""<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Ábaco Arcade — Matemáticas Lúdicas (Datalaria)</title>
  <meta name="theme-color" content="#0ea5e9">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <link rel="manifest" href="/apps/maths/manifest.json">
  <link rel="icon" type="image/svg+xml" href="/apps/maths/icon.svg">
  <script>
    // Script Anti-FOUC para tema visual instantáneo
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
      <a href="/apps/maths/" class="shell-brand">
        <span>🧮</span>
        <span id="shell-app-title">Ábaco Arcade</span>
        <span class="shell-badge">v2.1.0</span>
      </a>
    </div>

    <div class="shell-right">
      <button id="btn-install-pwa" class="btn-arcade btn-arcade-install" style="display: none;" title="Instalar en pantalla de inicio">
        <span>📲</span> <span id="label-install-btn">Instalar</span>
      </button>
      <button id="sound-btn" class="btn-arcade" title="Sonido (M)">🔊</button>
      <button id="theme-btn" class="btn-arcade" title="Tema (T)">☀️/🌙</button>
      <button id="lang-btn" class="btn-arcade" style="font-weight: 700;">🇪🇸 ES</button>
      <a id="link-spec" href="/es/apps/maths/" class="btn-arcade">📋 Ficha App</a>
      <a id="link-post" href="/es/posts/founderz-programando-chatGPT/" class="btn-arcade">📖 Historia IA</a>
      <a id="link-kits" href="/es/recursos/" class="btn-arcade btn-arcade-primary">📦 Recursos</a>
    </div>
  </header>

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

    # Copiar PWA assets a static/apps/maths/
    for pwa_file in ["manifest.json", "sw.js", "icon.svg"]:
        src = os.path.join(BASE_DIR, pwa_file)
        dst = os.path.join(STATIC_DIR, pwa_file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copiado PWA asset {pwa_file} a static/apps/maths/")

    # Eliminar index_backup.html huérfano si existe
    backup_path = os.path.join(STATIC_DIR, "index_backup.html")
    if os.path.exists(backup_path):
        os.remove(backup_path)
        print(f"Eliminado archivo huérfano {backup_path}")

    # Generar Shims Retrocompatibles
    shim_template = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=/apps/maths/?lang={lang}">
  <title>Redireccionando...</title>
  <script>
    window.location.replace('/apps/maths/?lang={lang}');
  </script>
</head>
<body>
  <p>Redirigiendo a <a href="/apps/maths/?lang={lang}">Ábaco Arcade v2.1</a>...</p>
</body>
</html>
"""
    for l in ['es', 'en']:
        shim_dir = os.path.join(STATIC_DIR, l)
        os.makedirs(shim_dir, exist_ok=True)
        shim_file = os.path.join(shim_dir, "index.html")
        with open(shim_file, "w", encoding="utf-8") as f:
            f.write(shim_template.format(lang=l))
        print(f"Generado shim retrocompatible {shim_file}")

    print("Build completado con éxito.")

if __name__ == "__main__":
    build()
