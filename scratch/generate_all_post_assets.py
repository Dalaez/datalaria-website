import os
import shutil
import subprocess
import time
import socketserver
import threading
from http.server import SimpleHTTPRequestHandler
from PIL import Image, ImageDraw, ImageFont

PORT = 5177
STATIC_DIR = os.path.abspath("static/apps/lifeops")
DIR_ES = os.path.abspath("content/es/posts/app-lifeops_part6_analytics_dashboard_360")
DIR_EN = os.path.abspath("content/en/posts/app-lifeops_part6_analytics_dashboard_360")

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)
    def log_message(self, format, *args):
        pass

socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", PORT), Handler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()
print(f"HTTP Server started on port {PORT}")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
user_dir = os.path.abspath("temp_edge_post_assets")

def capture_url(url, out_path, window_size="1440,1400"):
    cmd = [
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--window-size={window_size}",
        "--virtual-time-budget=6000",
        f"--user-data-dir={user_dir}",
        f"--screenshot={out_path}",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Edge error on {url}:", res.stderr)
    else:
        print(f"Captured {out_path} ({os.path.getsize(out_path)} bytes)")

def get_font(size, bold=False):
    font_names = [
        "C:\\Windows\\Fonts\\segoeui.ttf" if not bold else "C:\\Windows\\Fonts\\segoeuib.ttf",
        "C:\\Windows\\Fonts\\arial.ttf" if not bold else "C:\\Windows\\Fonts\\arialbd.ttf"
    ]
    for fn in font_names:
        if os.path.exists(fn):
            try:
                return ImageFont.truetype(fn, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_cover(path, title_text, subtitle_text, part_text, dashboard_img_path):
    W, H = 1200, 750
    img = Image.new("RGBA", (W, H), (11, 15, 23, 255))
    draw = ImageDraw.Draw(img)

    # Ambient radial gradients
    for r in range(450, 0, -5):
        alpha = int(35 * (1 - r / 450))
        draw.ellipse([800 - r, -100 - r, 800 + r, -100 + r], fill=(16, 185, 129, alpha))
        draw.ellipse([150 - r, 750 - r, 150 + r, 750 + r], fill=(6, 182, 212, alpha))
        draw.ellipse([1100 - r, 700 - r, 1100 + r, 700 + r], fill=(139, 92, 246, alpha))

    # Grid lines subtle pattern
    for x in range(0, W, 60):
        draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 6))
    for y in range(0, H, 60):
        draw.line([(0, y), (W, y)], fill=(255, 255, 255, 6))

    # Glass container border
    draw.rounded_rectangle([60, 60, W - 60, H - 60], radius=24, fill=(17, 24, 39, 180), outline=(255, 255, 255, 30), width=2)

    # Pill badge
    badge_font = get_font(18, bold=True)
    draw.rounded_rectangle([100, 100, 360, 140], radius=12, fill=(16, 185, 129, 45), outline=(16, 185, 129, 120), width=1)
    draw.text((120, 108), f"🚀  LIFEOPS  ·  {part_text.upper()}", font=badge_font, fill=(52, 211, 153))

    # Main title
    title_font = get_font(40, bold=True)
    draw.text((100, 170), title_text, font=title_font, fill=(249, 250, 251))

    # Subtitle
    sub_font = get_font(21, bold=False)
    draw.text((100, 235), subtitle_text, font=sub_font, fill=(156, 163, 175))

    # Mini Preview Cards below
    cards_y = 300
    card_w = 230
    card_h = 125
    kpis = [
        ("Periodo Dinámico", "7D · 30D · Año", "Semana / Mes / YTD", (16, 185, 129)),
        ("Comparativa Inter-Periodo", "+33% vs. anterior", "Cálculo Δ% determinista", (6, 182, 212)),
        ("Drill-Down 360°", "Deporte / Libros / Cine", "Running, Gym, Series, Kanban", (139, 92, 246)),
        ("Mitigación Cold-Start", "Caché SWR (0 ms)", "Banner de carga en 1er plano", (245, 158, 11)),
    ] if "Parte" in part_text else [
        ("Dynamic Window", "7D · 30D · Year", "Week / Month / YTD", (16, 185, 129)),
        ("Period-over-Period", "+33% vs. previous", "Deterministic Δ% math", (6, 182, 212)),
        ("360° Drill-Down", "Sport / Books / Cinema", "Running, Gym, Series, Kanban", (139, 92, 246)),
        ("Cold-Start Shield", "SWR Cache (0 ms)", "Foreground progress banner", (245, 158, 11)),
    ]

    for idx, (label, val, sub, col) in enumerate(kpis):
        cx = 100 + idx * (card_w + 20)
        draw.rounded_rectangle([cx, cards_y, cx + card_w, cards_y + card_h], radius=16, fill=(15, 23, 42, 220), outline=(col[0], col[1], col[2], 90), width=1)
        draw.text((cx + 16, cards_y + 16), label, font=get_font(13, bold=True), fill=(156, 163, 175))
        draw.text((cx + 16, cards_y + 44), val, font=get_font(17, bold=True), fill=col)
        draw.text((cx + 16, cards_y + 86), sub, font=get_font(12, bold=False), fill=(107, 114, 128))

    # Bottom mockup strip of the POPULATED dashboard screenshot
    if os.path.exists(dashboard_img_path):
        try:
            user_img = Image.open(dashboard_img_path).convert("RGBA")
            # Crop upper portion showing filter bar and KPI cards
            user_crop = user_img.crop((0, 0, user_img.width, min(user_img.height, 550)))
            target_w = W - 200
            target_h = 220
            user_crop = user_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
            img.paste(user_crop, (100, 455))
            draw.rounded_rectangle([100, 455, 100 + target_w, 455 + target_h], radius=12, outline=(255, 255, 255, 40), width=1)
        except Exception as e:
            print(f"Error loading dashboard image into cover: {e}")

    rgb_img = img.convert("RGB")
    rgb_img.save(path, quality=95)
    print(f"Created cover: {path}")

def run():
    try:
        # Step 1: Capture Raw screenshots
        raw_es_sport = os.path.abspath("scratch/raw_es_sport.png")
        raw_es_360 = os.path.abspath("scratch/raw_es_360.png")
        raw_es_banner = os.path.abspath("scratch/raw_es_banner.png")

        raw_en_sport = os.path.abspath("scratch/raw_en_sport.png")
        raw_en_360 = os.path.abspath("scratch/raw_en_360.png")
        raw_en_banner = os.path.abspath("scratch/raw_en_banner.png")

        capture_url(f"http://localhost:{PORT}/#/?mock=true&lang=es&cat=sport&subcat=running", raw_es_sport)
        capture_url(f"http://localhost:{PORT}/#/?mock=true&lang=es", raw_es_360)
        capture_url(f"http://localhost:{PORT}/#/?mock=true&lang=es&banner=true&sec=12", raw_es_banner)

        capture_url(f"http://localhost:{PORT}/#/?mock=true&lang=en&cat=sport&subcat=running", raw_en_sport)
        capture_url(f"http://localhost:{PORT}/#/?mock=true&lang=en", raw_en_360)
        capture_url(f"http://localhost:{PORT}/#/?mock=true&lang=en&banner=true&sec=12", raw_en_banner)

        # Step 2: Crop and save target assets
        # Common Coordinates
        crop_dash_box = (240, 70, 1430, 1065)       # Full sport dashboard (header + filters + KPIs + charts)
        crop_filters_box = (240, 195, 1430, 405)    # Control filter bar with categories & subcategories
        crop_heatmap_box = (240, 1065, 1430, 1345)  # 16-week consistency heatmap
        crop_banner_box = (240, 195, 1430, 395)     # Foreground cloud sync banner (renders at top when banner=true)

        # ── Spanish Assets ──
        img_es_sport = Image.open(raw_es_sport)
        img_es_360 = Image.open(raw_es_360)
        img_es_banner = Image.open(raw_es_banner)

        p_es_dash = os.path.join(DIR_ES, "lifeops_dashboard_360_analytics_es.png")
        img_es_sport.crop(crop_dash_box).save(p_es_dash, quality=95)
        print("Saved:", p_es_dash)

        p_es_filters = os.path.join(DIR_ES, "lifeops_analytics_filters_drilldown_es.png")
        img_es_sport.crop(crop_filters_box).save(p_es_filters, quality=95)
        print("Saved:", p_es_filters)

        p_es_heatmap = os.path.join(DIR_ES, "lifeops_consistency_heatmap_streaks_es.png")
        img_es_sport.crop(crop_heatmap_box).save(p_es_heatmap, quality=95)
        print("Saved:", p_es_heatmap)

        p_es_banner = os.path.join(DIR_ES, "lifeops_cloud_sync_banner_coldstart_es.png")
        img_es_banner.crop(crop_banner_box).save(p_es_banner, quality=95)
        print("Saved:", p_es_banner)

        create_cover(
            os.path.join(DIR_ES, "cover.png"),
            "Dashboard 360° con Analítica Multidimensional",
            "Recharts, comparativas inter-periodo (Δ%) y mitigación de Cold-Starts",
            "Parte 6",
            p_es_dash
        )

        # ── English Assets ──
        img_en_sport = Image.open(raw_en_sport)
        img_en_360 = Image.open(raw_en_360)
        img_en_banner = Image.open(raw_en_banner)

        p_en_dash = os.path.join(DIR_EN, "lifeops_dashboard_360_analytics_en.png")
        img_en_sport.crop(crop_dash_box).save(p_en_dash, quality=95)
        print("Saved:", p_en_dash)

        p_en_filters = os.path.join(DIR_EN, "lifeops_analytics_filters_drilldown_en.png")
        img_en_sport.crop(crop_filters_box).save(p_en_filters, quality=95)
        print("Saved:", p_en_filters)

        p_en_heatmap = os.path.join(DIR_EN, "lifeops_consistency_heatmap_streaks_en.png")
        img_en_sport.crop(crop_heatmap_box).save(p_en_heatmap, quality=95)
        print("Saved:", p_en_heatmap)

        p_en_banner = os.path.join(DIR_EN, "lifeops_cloud_sync_banner_coldstart_en.png")
        img_en_banner.crop(crop_banner_box).save(p_en_banner, quality=95)
        print("Saved:", p_en_banner)

        create_cover(
            os.path.join(DIR_EN, "cover.png"),
            "360° Multi-Dimensional Analytics Dashboard",
            "Recharts, period-over-period comparisons (Δ%) and Cold-Start mitigation",
            "Part 6",
            p_en_dash
        )

        print("\nAll assets successfully generated and overwritten!")

    finally:
        httpd.shutdown()
        httpd.server_close()
        print("HTTP server closed.")

if __name__ == "__main__":
    run()
