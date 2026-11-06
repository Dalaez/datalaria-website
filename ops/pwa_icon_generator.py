"""
ops/pwa_icon_generator.py
Generador determinista de iconos PWA rasterizados (PNG estándar y maskable)
para aplicaciones del ecosistema Datalaria.
Soporta Chrome y Edge headless con escalado bicúbico/Lanczos via Pillow.
"""
import os
import sys
import tempfile
import subprocess
from pathlib import Path
from PIL import Image

def find_browser_binary():
    candidates = [
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    raise RuntimeError("No se encontró Google Chrome ni Microsoft Edge para renderizado headless de iconos PWA.")

def render_svg_to_png(browser_path, svg_content, output_png_512, bg_color="00000000"):
    temp_dir = tempfile.gettempdir()
    html_file = os.path.join(temp_dir, f"pwa_icon_render_{os.getpid()}_{hash(svg_content) % 100000}.html")
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 512px; height: 512px; overflow: hidden; background: transparent; }}
  svg {{ width: 512px; height: 512px; display: block; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)
        
    cmd = [
        browser_path,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--default-background-color={bg_color}",
        f"--screenshot={output_png_512}",
        "--window-size=512,512",
        f"file:///{html_file.replace(os.sep, '/')}"
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        if os.path.exists(html_file):
            try:
                os.remove(html_file)
            except OSError:
                pass

def generate_app_pwa_icons(app_dir, static_dir, standard_svg, maskable_svg):
    browser = find_browser_binary()
    app_path = Path(app_dir)
    static_path = Path(static_dir)
    app_path.mkdir(parents=True, exist_ok=True)
    static_path.mkdir(parents=True, exist_ok=True)
    
    temp_dir = tempfile.gettempdir()
    tmp_std_512 = os.path.join(temp_dir, f"tmp_std_512_{app_path.name}.png")
    tmp_msk_512 = os.path.join(temp_dir, f"tmp_msk_512_{app_path.name}.png")
    
    # 1. Renderizar Standard 512x512
    render_svg_to_png(browser, standard_svg, tmp_std_512, bg_color="00000000")
    with Image.open(tmp_std_512) as img_std_512:
        img_std_512.load()
        # Guardar 512x512 standard
        img_std_512.save(app_path / "icon-512.png", format="PNG", optimize=True)
        img_std_512.save(static_path / "icon-512.png", format="PNG", optimize=True)
        
        # 192x192 standard
        img_192 = img_std_512.resize((192, 192), Image.Resampling.LANCZOS)
        img_192.save(app_path / "icon-192.png", format="PNG", optimize=True)
        img_192.save(static_path / "icon-192.png", format="PNG", optimize=True)
        
        # Apple touch icon 180x180
        img_apple = img_std_512.resize((180, 180), Image.Resampling.LANCZOS)
        img_apple.save(app_path / "apple-touch-icon.png", format="PNG", optimize=True)
        img_apple.save(static_path / "apple-touch-icon.png", format="PNG", optimize=True)
        
    if os.path.exists(tmp_std_512):
        try: os.remove(tmp_std_512)
        except OSError: pass

    # 2. Renderizar Maskable 512x512 (Fondo full-bleed para recortador adaptativo de Android)
    render_svg_to_png(browser, maskable_svg, tmp_msk_512, bg_color="00000000")
    with Image.open(tmp_msk_512) as img_msk_512:
        img_msk_512.load()
        # Guardar 512x512 maskable
        img_msk_512.save(app_path / "icon-maskable-512.png", format="PNG", optimize=True)
        img_msk_512.save(static_path / "icon-maskable-512.png", format="PNG", optimize=True)
        
        # 192x192 maskable
        img_msk_192 = img_msk_512.resize((192, 192), Image.Resampling.LANCZOS)
        img_msk_192.save(app_path / "icon-maskable-192.png", format="PNG", optimize=True)
        img_msk_192.save(static_path / "icon-maskable-192.png", format="PNG", optimize=True)

    if os.path.exists(tmp_msk_512):
        try: os.remove(tmp_msk_512)
        except OSError: pass

    print(f"[OK] Iconos PWA generados con éxito para '{app_path.name}':")
    print(f"     - icon-192.png, icon-512.png (any)")
    print(f"     - icon-maskable-192.png, icon-maskable-512.png (maskable Android)")
    print(f"     - apple-touch-icon.png (iOS 180x180)")

if __name__ == "__main__":
    print("Módulo generador de iconos PWA Datalaria cargado.")
