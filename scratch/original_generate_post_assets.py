import os
import shutil
from PIL import Image, ImageDraw, ImageFont

USER_UPLOADED_IMG = r"C:\Users\dalae\.gemini\antigravity\brain\ea3c2d0a-c775-440f-8046-60bef6d1f525\.user_uploaded\media_1793086990165_a1a5ac07.png"
DIR_ES = r"content\es\posts\app-lifeops_part6_analytics_dashboard_360"
DIR_EN = r"content\en\posts\app-lifeops_part6_analytics_dashboard_360"

def get_font(size, bold=False):
    # Try system fonts on Windows
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

def create_cover(path, title_text, subtitle_text, part_text):
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
    title_font = get_font(42, bold=True)
    draw.text((100, 175), title_text, font=title_font, fill=(249, 250, 251))

    # Subtitle
    sub_font = get_font(22, bold=False)
    draw.text((100, 240), subtitle_text, font=sub_font, fill=(156, 163, 175))

    # Mini Preview Cards below
    cards_y = 310
    card_w = 230
    card_h = 130
    kpis = [
        ("Periodo Dinámico", "7D · 30D · Año", "Semana / Mes / YTD", (16, 185, 129)),
        ("Comparativa Inter-Periodo", "+33% vs. anterior", "Cálculo Δ% determinista", (6, 182, 212)),
        ("Drill-Down 360°", "Deporte / Libros / Cine", "Running, Gym, Series, Kanban", (139, 92, 246)),
        ("Mitigación Cold-Start", "Caché SWR (0 ms)", "Banner de carga en 1er plano", (245, 158, 11)),
    ]
    for idx, (label, val, sub, col) in enumerate(kpis):
        cx = 100 + idx * (card_w + 20)
        draw.rounded_rectangle([cx, cards_y, cx + card_w, cards_y + card_h], radius=16, fill=(15, 23, 42, 220), outline=(col[0], col[1], col[2], 90), width=1)
        draw.text((cx + 16, cards_y + 16), label, font=get_font(13, bold=True), fill=(156, 163, 175))
        draw.text((cx + 16, cards_y + 44), val, font=get_font(17, bold=True), fill=col)
        draw.text((cx + 16, cards_y + 88), sub, font=get_font(12, bold=False), fill=(107, 114, 128))

    # Bottom mockup strip of the dashboard screenshot
    if os.path.exists(USER_UPLOADED_IMG):
        try:
            user_img = Image.open(USER_UPLOADED_IMG).convert("RGBA")
            # Crop upper part of dashboard
            user_crop = user_img.crop((0, 60, user_img.width, min(user_img.height, 460)))
            target_w = W - 200
            target_h = 190
            user_crop = user_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
            img.paste(user_crop, (100, 470))
            draw.rounded_rectangle([100, 470, 100 + target_w, 470 + target_h], radius=12, outline=(255, 255, 255, 40), width=1)
        except Exception as e:
            print(f"Error loading user image: {e}")

    rgb_img = img.convert("RGB")
    rgb_img.save(path, quality=95)
    print(f"Created cover: {path}")

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
    print(f"Created sync banner: {path}")

def create_heatmap_graphic(path, is_es=True):
    W, H = 1000, 300
    img = Image.new("RGBA", (W, H), (11, 15, 23, 255))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([30, 20, W - 30, H - 20], radius=20, fill=(15, 23, 42, 240), outline=(255, 255, 255, 25), width=1)

    title = "🔥  " + ("Mapa de Consistencia Diaria (Últimas 16 Semanas — Estilo Strava/GitHub)" if is_es else "Daily Consistency Heatmap (Last 16 Weeks — Strava/GitHub Style)")
    draw.text((60, 42), title, font=get_font(18, bold=True), fill=(249, 250, 251))

    # Badges on right
    badges = [
        ("42", "Días activos" if is_es else "Active days", (16, 185, 129)),
        ("5d", "Racha actual" if is_es else "Current streak", (6, 182, 212)),
        ("14d", "Mejor racha" if is_es else "Best streak", (245, 158, 11)),
    ]
    bx = W - 420
    for val, lbl, col in badges:
        draw.rounded_rectangle([bx, 40, bx + 110, 72], radius=8, fill=(17, 24, 39, 220), outline=(col[0], col[1], col[2], 90), width=1)
        draw.text((bx + 10, 46), f"{val} {lbl[:3]}", font=get_font(12, bold=True), fill=col)
        bx += 120

    # Grid of 16 weeks x 7 days
    grid_x = 100
    grid_y = 105
    cell_size = 18
    gap = 6

    day_labels = ["Lun", "", "Mié", "", "Vie", "", "Dom"] if is_es else ["Mon", "", "Wed", "", "Fri", "", "Sun"]
    for d, dl in enumerate(day_labels):
        if dl:
            draw.text((60, grid_y + d * (cell_size + gap) + 2), dl, font=get_font(11, bold=False), fill=(107, 114, 128))

    # Palette levels
    colors = [
        (255, 255, 255, 14),   # level 0
        (16, 185, 129, 65),    # level 1
        (16, 185, 129, 120),   # level 2
        (16, 185, 129, 180),   # level 3
        (16, 185, 129, 255),   # level 4
    ]

    import random
    random.seed(42)

    for w in range(16):
        for d in range(7):
            cx = grid_x + w * (cell_size + gap)
            cy = grid_y + d * (cell_size + gap)
            lvl = random.choices([0, 1, 2, 3, 4], weights=[0.35, 0.2, 0.2, 0.15, 0.1])[0]
            draw.rounded_rectangle([cx, cy, cx + cell_size, cy + cell_size], radius=4, fill=colors[lvl], outline=(255, 255, 255, 20), width=1)

    # Footer scale
    scale_y = H - 55
    draw.text((60, scale_y), "DEPORTE → Running (Carrera)" if is_es else "SPORT → Running", font=get_font(12, bold=True), fill=(156, 163, 175))

    draw.text((W - 250, scale_y), "Menos" if is_es else "Less", font=get_font(11, bold=False), fill=(107, 114, 128))
    for idx, col in enumerate(colors):
        sx = W - 200 + idx * 18
        draw.rounded_rectangle([sx, scale_y - 2, sx + 14, scale_y + 12], radius=3, fill=col)
    draw.text((W - 100, scale_y), "Más" if is_es else "More", font=get_font(11, bold=False), fill=(107, 114, 128))

    rgb_img = img.convert("RGB")
    rgb_img.save(path, quality=95)
    print(f"Created heatmap: {path}")

def process_user_screenshots():
    if not os.path.exists(USER_UPLOADED_IMG):
        return
    u_img = Image.open(USER_UPLOADED_IMG)

    # 1. Full dashboard image
    u_img.save(os.path.join(DIR_ES, "lifeops_dashboard_360_analytics_es.png"))
    u_img.save(os.path.join(DIR_EN, "lifeops_dashboard_360_analytics_en.png"))

    # 2. Filter bar crop
    # Filter bar is approximately at y: 150 to 330
    w, h = u_img.size
    filter_crop = u_img.crop((40, 140, w - 40, min(h, 340)))
    filter_crop.save(os.path.join(DIR_ES, "lifeops_analytics_filters_drilldown_es.png"))
    filter_crop.save(os.path.join(DIR_EN, "lifeops_analytics_filters_drilldown_en.png"))
    print("Processed user screenshot crops.")

if __name__ == "__main__":
    create_cover(
        os.path.join(DIR_ES, "cover.png"),
        "Dashboard 360° con Analítica Multidimensional",
        "Recharts, comparativas inter-periodo (Δ%) y mitigación de Cold-Starts",
        "Parte 6"
    )
    create_cover(
        os.path.join(DIR_EN, "cover.png"),
        "360° Multi-Dimensional Analytics Dashboard",
        "Recharts, period-over-period comparisons (Δ%) and Cold-Start mitigation",
        "Part 6"
    )

    create_cloud_sync_banner_image(os.path.join(DIR_ES, "lifeops_cloud_sync_banner_coldstart_es.png"), is_es=True)
    create_cloud_sync_banner_image(os.path.join(DIR_EN, "lifeops_cloud_sync_banner_coldstart_en.png"), is_es=False)

    create_heatmap_graphic(os.path.join(DIR_ES, "lifeops_consistency_heatmap_streaks_es.png"), is_es=True)
    create_heatmap_graphic(os.path.join(DIR_EN, "lifeops_consistency_heatmap_streaks_en.png"), is_es=False)

    process_user_screenshots()
    print("All assets generated successfully!")
