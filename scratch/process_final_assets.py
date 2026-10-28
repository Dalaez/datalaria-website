import os
from PIL import Image, ImageDraw, ImageFont

DIR_ES = os.path.abspath("content/es/posts/app-lifeops_part6_analytics_dashboard_360")
DIR_EN = os.path.abspath("content/en/posts/app-lifeops_part6_analytics_dashboard_360")

# Source high-resolution Edge screenshots
RAW_ES = os.path.abspath("scratch/test_th_0.png")
RAW_EN = os.path.abspath("scratch/test_th_1.png")

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
    cards_y = 295
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
            dash_img = Image.open(dashboard_img_path).convert("RGBA")
            # Crop upper portion showing filter bar, sport category, and populated KPI cards
            dash_crop = dash_img.crop((0, 0, dash_img.width, min(dash_img.height, 580)))
            target_w = W - 200
            target_h = 240
            dash_crop = dash_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
            img.paste(dash_crop, (100, 445))
            draw.rounded_rectangle([100, 445, 100 + target_w, 445 + target_h], radius=12, outline=(255, 255, 255, 40), width=1)
        except Exception as e:
            print(f"Error loading dashboard image into cover: {e}")

    rgb_img = img.convert("RGB")
    rgb_img.save(path, quality=95)
    print(f"Created cover: {path} ({os.path.getsize(path)} bytes)")

def create_cloud_sync_banner_image(path, is_es=True):
    W, H = 1000, 320
    img = Image.new("RGBA", (W, H), (11, 15, 23, 255))
    draw = ImageDraw.Draw(img)

    # Ambient glow
    for r in range(250, 0, -5):
        alpha = int(25 * (1 - r / 250))
        draw.ellipse([500 - r, 160 - r, 500 + r, 160 + r], fill=(16, 185, 129, alpha))

    # Outer glass card
    draw.rounded_rectangle([30, 25, W - 30, H - 25], radius=20, fill=(15, 23, 42, 240), outline=(16, 185, 129, 120), width=2)

    # Spinner box
    draw.rounded_rectangle([60, 50, 110, 100], radius=12, fill=(16, 185, 129, 45), outline=(16, 185, 129, 140), width=1)
    draw.text((75, 62), "⟳", font=get_font(26, bold=True), fill=(52, 211, 153))

    # Title & timer
    timer_text = "12s"
    draw.rounded_rectangle([W - 140, 52, W - 60, 96], radius=10, fill=(17, 24, 39, 230), outline=(255, 255, 255, 30), width=1)
    draw.text((W - 120, 62), timer_text, font=get_font(20, bold=True), fill=(52, 211, 153))

    title = "Recuperando tus datos desde Supabase Cloud..." if is_es else "Retrieving your data from Supabase Cloud..."
    desc = (
        "El contenedor gratuito de Render estaba en reposo (Cold-Start) y se está activando (20-40s).\nTus datos están 100% seguros y aparecerán automáticamente en cuanto responda."
        if is_es else
        "The free-tier Render container was sleeping (Cold-Start) and is waking up (20-40s).\nYour data is 100% safe and will appear automatically as soon as it responds."
    )
    draw.text((130, 52), title, font=get_font(20, bold=True), fill=(249, 250, 251))
    draw.text((130, 84), desc, font=get_font(13, bold=False), fill=(156, 163, 175))

    # Progress bar track & fill
    bar_y = 155
    draw.rounded_rectangle([60, bar_y, W - 60, bar_y + 10], radius=5, fill=(31, 41, 55, 255))
    draw.rounded_rectangle([60, bar_y, int(60 + (W - 120) * 0.62), bar_y + 10], radius=5, fill=(16, 185, 129, 255))

    # 3 Steps checklist
    steps = [
        ("✓ " + ("Sesión autenticada (Supabase Auth)" if is_es else "Session authenticated (Supabase Auth)"), (16, 185, 129)),
        ("⟳ " + ("Activando motor API en Render (12s)" if is_es else "Waking up API engine on Render (12s)"), (6, 182, 212)),
        ("⏳ " + ("Hidratando actividades y analítica 360°" if is_es else "Hydrating activities & 360° analytics"), (156, 163, 175)),
    ]
    step_y = 195
    step_w = (W - 120) // 3
    for idx, (st, col) in enumerate(steps):
        sx = 60 + idx * step_w
        draw.text((sx, step_y), st, font=get_font(13, bold=True), fill=col)

    # Bottom pill note
    pill_text = (
        "💡 En visitas sucesivas, la caché Stale-While-Revalidate (SWR) carga estos datos en 0 ms sin esperar."
        if is_es else
        "💡 On return visits, Stale-While-Revalidate (SWR) cache loads these records in 0 ms instantly."
    )
    draw.rounded_rectangle([60, 240, W - 60, 285], radius=10, fill=(6, 182, 212, 25), outline=(6, 182, 212, 70), width=1)
    draw.text((80, 252), pill_text, font=get_font(12, bold=False), fill=(103, 232, 249))

    rgb_img = img.convert("RGB")
    rgb_img.save(path, quality=95)
    print(f"Created sync banner: {path} ({os.path.getsize(path)} bytes)")

def process_all():
    # Crop boundaries
    crop_dash_box = (240, 70, 1430, 1065)       # Full sport dashboard (header + filters + KPIs + charts)
    crop_filters_box = (240, 195, 1430, 405)    # Control filter bar with categories & subcategories
    crop_heatmap_box = (240, 1065, 1430, 1345)  # 16-week consistency heatmap

    # 1. Process Spanish Assets
    im_es = Image.open(RAW_ES)
    p_es_dash = os.path.join(DIR_ES, "lifeops_dashboard_360_analytics_es.png")
    im_es.crop(crop_dash_box).save(p_es_dash, quality=95)
    print(f"Saved: {p_es_dash} ({os.path.getsize(p_es_dash)} bytes)")

    p_es_filters = os.path.join(DIR_ES, "lifeops_analytics_filters_drilldown_es.png")
    im_es.crop(crop_filters_box).save(p_es_filters, quality=95)
    print(f"Saved: {p_es_filters} ({os.path.getsize(p_es_filters)} bytes)")

    p_es_heatmap = os.path.join(DIR_ES, "lifeops_consistency_heatmap_streaks_es.png")
    im_es.crop(crop_heatmap_box).save(p_es_heatmap, quality=95)
    print(f"Saved: {p_es_heatmap} ({os.path.getsize(p_es_heatmap)} bytes)")

    p_es_banner = os.path.join(DIR_ES, "lifeops_cloud_sync_banner_coldstart_es.png")
    create_cloud_sync_banner_image(p_es_banner, is_es=True)

    create_cover(
        os.path.join(DIR_ES, "cover.png"),
        "Dashboard 360° con Analítica Multidimensional",
        "Recharts, comparativas inter-periodo (Δ%) y mitigación de Cold-Starts",
        "Parte 6",
        p_es_dash
    )

    # 2. Process English Assets
    im_en = Image.open(RAW_EN)
    p_en_dash = os.path.join(DIR_EN, "lifeops_dashboard_360_analytics_en.png")
    im_en.crop(crop_dash_box).save(p_en_dash, quality=95)
    print(f"Saved: {p_en_dash} ({os.path.getsize(p_en_dash)} bytes)")

    p_en_filters = os.path.join(DIR_EN, "lifeops_analytics_filters_drilldown_en.png")
    im_en.crop(crop_filters_box).save(p_en_filters, quality=95)
    print(f"Saved: {p_en_filters} ({os.path.getsize(p_en_filters)} bytes)")

    p_en_heatmap = os.path.join(DIR_EN, "lifeops_consistency_heatmap_streaks_en.png")
    im_en.crop(crop_heatmap_box).save(p_en_heatmap, quality=95)
    print(f"Saved: {p_en_heatmap} ({os.path.getsize(p_en_heatmap)} bytes)")

    p_en_banner = os.path.join(DIR_EN, "lifeops_cloud_sync_banner_coldstart_en.png")
    create_cloud_sync_banner_image(p_en_banner, is_es=False)

    create_cover(
        os.path.join(DIR_EN, "cover.png"),
        "360° Multi-Dimensional Analytics Dashboard",
        "Recharts, period-over-period comparisons (Δ%) and Cold-Start mitigation",
        "Part 6",
        p_en_dash
    )

    print("\nAll assets successfully generated and replaced!")

if __name__ == "__main__":
    process_all()
