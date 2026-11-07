"""
ops/helix/build_series_covers.py
---------------------------------
Generador determinista de las 10 portadas conceptuales oficiales (1200x630 px)
para la serie editorial de 5 artículos bilingües de Datalaria Helix (Partes 1 a 5, ES y EN).

Especificación: Hito 6.9 (plan_hito_6_9_ejecucion_flash.md).
"""

from pathlib import Path
from typing import Dict, Any, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
WIDTH = 1200
HEIGHT = 630

POSTS_CONFIG: List[Dict[str, Any]] = [
    {
        "part": 1,
        "slug_es": "helix-parte1-especificacion-adn-escuadron-12-agentes",
        "slug_en": "helix-part1-spec-dna-12-agent-engineering-squad",
        "tag_es": "PARTE 1/5 · ARQUITECTURA AGÉNTICA",
        "tag_en": "PART 1/5 · AGENTIC ARCHITECTURE",
        "title_es": "La Especificación es el ADN de tu App",
        "title_en": "The Specification is your App's DNA",
        "sub_es": "Escuadrón Canónico de 12 Agentes · Separación de Poderes & Veto Vinculante",
        "sub_en": "Canonical 12-Agent Squad · Separation of Powers & Binding Veto",
        "pillars_es": [
            ("Vibe Coding", "Colapso a las 48h", "Amnesia de contexto y deriva"),
            ("SDD Framework", "La Spec es la Ley", "Invariantes y contratos formales"),
            ("Escuadrón 12 Roles", "4 Células Expertas", "Dirección, Construcción, Veto y Entrega"),
            ("Garantía de Calidad", "Veto Vinculante", "Seguridad y QA independientes"),
        ],
        "pillars_en": [
            ("Vibe Coding", "48h Collapse", "Context drift & regression"),
            ("SDD Framework", "The Spec is Law", "Invariants & formal contracts"),
            ("12-Agent Squad", "4 Expert Cells", "Direction, Construction, Veto & Delivery"),
            ("Quality Assurance", "Binding Veto Power", "Independent Security and QA"),
        ],
        "accent": (56, 189, 248),  # Cian
    },
    {
        "part": 2,
        "slug_es": "helix-parte2-triaje-determinista-adaptadores-antigravity-claude-cursor",
        "slug_en": "helix-part2-deterministic-triage-adapters-antigravity-claude-cursor",
        "tag_es": "PARTE 2/5 · GOBERNANZA DE CONTEXTO",
        "tag_en": "PART 2/5 · CONTEXT GOVERNANCE",
        "title_es": "Triaje Determinista XS–XL y Adaptadores",
        "title_en": "Deterministic XS–XL Triage & Adapters",
        "sub_es": "-87% de Context Spend · Google Antigravity, Claude Code, Cursor & Codex",
        "sub_en": "-87% Context Spend · Google Antigravity, Claude Code, Cursor & Codex",
        "pillars_es": [
            ("Triaje Determinista", "Tallas XS a XL", "Algoritmo estricto por archivos y superficies"),
            ("Ahorro de Tokens", "~87% menos coste", "140k -> 18.5k tokens cargando bajo demanda"),
            ("Disparadores TRG", "Seguridad Activa", "TRG-SEC, TRG-UX, TRG-I18N innegociables"),
            ("Compilador Multi-Tool", "26 Adaptadores", "Sincronizados desde una única spec"),
        ],
        "pillars_en": [
            ("Deterministic Triage", "XS to XL Sizing", "Strict algorithm by files and surfaces"),
            ("Token Savings", "~87% less spend", "140k -> 18.5k tokens via on-demand loading"),
            ("Mandatory Triggers", "Active Security", "TRG-SEC, TRG-UX, TRG-I18N non-negotiable"),
            ("Multi-Tool Compiler", "26 Adapters", "Synchronized from a single source spec"),
        ],
        "accent": (168, 85, 247),  # Púrpura
    },
    {
        "part": 3,
        "slug_es": "helix-parte3-cli-python-cero-dependencias-spec-score-rollback",
        "slug_en": "helix-part3-zero-dependency-python-cli-spec-score-rollback",
        "tag_es": "PARTE 3/5 · MÚSCULO DETERMINISTA",
        "tag_en": "PART 3/5 · DETERMINISTIC ENGINE",
        "title_es": "CLI helix.py: SpecQualityScore y Rollback",
        "title_en": "Zero-Dep helix.py CLI: SpecScore & Rollback",
        "sub_es": "0 Dependencias Externas · 7 Subcomandos · Marcha Atrás Automática al 2º Fallo",
        "sub_en": "0 External Dependencies · 7 Subcommands · Automatic 2-Failure Rollback",
        "pillars_es": [
            ("Python Stdlib >= 3.10", "0 Dependencias", "Ejecución universal en Win / macOS / Linux"),
            ("SpecQualityScore", "100 / 100 Puntos", "Auditoría formal matemática de 5 pilares"),
            ("Git Checkpoints", "Puntos de Restauración", "Tags automáticos antes de cada cambio"),
            ("Rollback al 2º Fallo", "INV-HELIX-7", "Marcha atrás determinista e informe de auditoría"),
        ],
        "pillars_en": [
            ("Python Stdlib >= 3.10", "0 Dependencies", "Universal run on Win / macOS / Linux"),
            ("SpecQualityScore", "100 / 100 Score", "5-pillar formal mathematical audit"),
            ("Git Checkpoints", "Restoration Points", "Automatic tags preceding every task"),
            ("2-Failure Rollback", "INV-HELIX-7", "Deterministic rollback & audit log report"),
        ],
        "accent": (16, 185, 129),  # Esmeralda
    },
    {
        "part": 4,
        "slug_es": "helix-parte4-sandbox-react-spec-builder-zip-client-side",
        "slug_en": "helix-part4-react-sandbox-spec-builder-client-side-zip",
        "tag_es": "PARTE 4/5 · SANDBOX INTERACTIVO",
        "tag_en": "PART 4/5 · INTERACTIVE SANDBOX",
        "title_es": "Sandbox Web React 19: Modo A+B y PKZIP",
        "title_en": "React 19 Web Sandbox: Mode A+B & PKZIP",
        "sub_es": "Entrevista Guiada en < 16ms · Empaquetado ZIP en Memoria · Mega-Prompt Multi-Agente",
        "sub_en": "Guided Interview in < 16ms · In-Memory ZIP Bundling · Multi-Agent Mega-Prompt",
        "pillars_es": [
            ("Modo A: Spec Builder", "Generador de Specs", "Entrevista determinista en 5 pilares guiados"),
            ("ZIP en Navegador", "zipBuilder.ts", "PKZIP STORE + CRC32 nativo sin backend"),
            ("Modo B: Mega-Prompt", "Cero API Key", "Prompt multi-agente copiable en 1 clic"),
            ("Cockpit Agéntico", "Activos vs Banquillo", "Visualización en vivo de las 4 células"),
        ],
        "pillars_en": [
            ("Mode A: Spec Builder", "Spec Generator", "Deterministic 5-pillar guided interview"),
            ("In-Browser ZIP", "zipBuilder.ts", "Native PKZIP STORE + CRC32 zero-backend"),
            ("Mode B: Mega-Prompt", "Zero API Key", "Multi-agent prompt copyable in 1 click"),
            ("Agentic Cockpit", "Active vs Benched", "Live visualization across the 4 cells"),
        ],
        "accent": (245, 158, 11),  # Ámbar
    },
    {
        "part": 5,
        "slug_es": "helix-parte5-casos-reales-operacion-crisol-pulse-marginguard-kits",
        "slug_en": "helix-part5-real-case-studies-pulse-crisol-marginguard-kits",
        "tag_es": "PARTE 5/5 · EVIDENCIA Y ENTREGABLES",
        "tag_en": "PART 5/5 · EVIDENCE & DELIVERABLES",
        "title_es": "Casos Reales de Estudio y Kits de Lanzamiento",
        "title_en": "Real Case Studies & Commercial Launch Kits",
        "sub_es": "Operación Crisol (Pulse) + MarginGuard B2B (Veto QA) · Starter 9€ & Core Kit 19€",
        "sub_en": "Operation Crisol (Pulse) + MarginGuard B2B (QA Veto) · Starter 9€ & Core Kit 19€",
        "pillars_es": [
            ("Caso #1: Pulse", "Operación Crisol", "Auditoría formal de app real por 12 agentes"),
            ("Caso #2: MarginGuard", "Veto QA Vinculante", "Rechazo de QA ante división/0 -> INV-MARGIN-2"),
            ("Starter Kit (9 €)", "Cimientos SDD", "3 carpetas + Guía PDF + 2 agentes esenciales"),
            ("Core Kit (19 € / 39 €)", "Ecosistema Completo", "5 carpetas + 12 agentes + CLI + 3 blueprints"),
        ],
        "pillars_en": [
            ("Case #1: Pulse", "Operation Crisol", "Formal audit of real app by 12 agents"),
            ("Case #2: MarginGuard", "Binding QA Veto", "QA reject on division/0 -> INV-MARGIN-2"),
            ("Starter Kit (9 €)", "SDD Foundations", "3 folders + PDF Guide + 2 essential agents"),
            ("Core Kit (19 € / 39 €)", "Complete System", "5 folders + 12 agents + CLI + 3 blueprints"),
        ],
        "accent": (239, 68, 68),  # Coral / Rojo
    },
]


def _get_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    """Carga fuente TrueType del sistema con fallback seguro."""
    candidates = [
        "seguisb.ttf" if bold else "segoeui.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _draw_dna_helix_icon(draw: ImageDraw.ImageDraw, x: float, y: float, w: float, h: float, color=(56, 189, 248), stroke_width: int = 2):
    """Dibuja un icono estilizado de doble hélice de ADN."""
    import math
    steps = 14
    points_a = []
    points_b = []
    for i in range(steps + 1):
        t = i / steps
        py = y + t * h
        wave = math.sin(t * math.pi * 2.5) * (w / 2.2)
        px_a = x + (w / 2) + wave
        px_b = x + (w / 2) - wave
        points_a.append((px_a, py))
        points_b.append((px_b, py))

    # Conectores transversales
    for i in range(1, steps, 2):
        draw.line([points_a[i], points_b[i]], fill=(color[0], color[1], color[2], 120), width=1)

    # Hebras helicoidales
    for i in range(len(points_a) - 1):
        draw.line([points_a[i], points_a[i + 1]], fill=color, width=stroke_width)
        draw.line([points_b[i], points_b[i + 1]], fill=color, width=stroke_width)


def create_series_cover(item: Dict[str, Any], lang: str = "es") -> Image.Image:
    """Genera la imagen conceptual oficial (1200x630 px) para un artículo de la serie Helix."""
    part_num = item["part"]
    accent = item["accent"]
    is_es = (lang == "es")

    tag_text = item["tag_es"] if is_es else item["tag_en"]
    title_text = item["title_es"] if is_es else item["title_en"]
    sub_text = item["sub_es"] if is_es else item["sub_en"]
    pillars = item["pillars_es"] if is_es else item["pillars_en"]

    # 1. Lienzo Base con gradiente vertical oscuro (#0b0f17 -> #0f172a)
    img = Image.new("RGBA", (WIDTH, HEIGHT), (11, 15, 23, 255))
    c_top = (11, 15, 23)
    c_bot = (15, 23, 42)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(c_top[0] + (c_bot[0] - c_top[0]) * ratio)
        g = int(c_top[1] + (c_bot[1] - c_top[1]) * ratio)
        b = int(c_top[2] + (c_bot[2] - c_top[2]) * ratio)
        line_draw = ImageDraw.Draw(img)
        line_draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

    # 2. Resplandores atmosféricos de fondo (Glows temáticos)
    glow_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)

    # Glow principal del acento (centro-superior)
    glow_draw.ellipse([400, -80, 800, 280], fill=(accent[0], accent[1], accent[2], 26))
    # Glow cian superior izquierdo para el badge de serie
    glow_draw.ellipse([20, 20, 360, 160], fill=(56, 189, 248, 22))
    # Glow secundario azul profundo inferior derecho
    glow_draw.ellipse([880, 260, 1260, 640], fill=(37, 99, 235, 20))

    glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(55))
    img = Image.alpha_composite(img, glow_overlay)
    draw = ImageDraw.Draw(img)

    # 3. Malla técnica blueprint ejecutiva (40x40 px)
    grid_color = (20, 30, 48, 140)
    for x in range(0, WIDTH, 40):
        draw.line([(x, 0), (x, HEIGHT)], fill=grid_color)
    for y in range(0, HEIGHT, 40):
        draw.line([(0, y), (WIDTH, y)], fill=grid_color)

    # Micro-cruces en intersecciones (cada 160 px)
    cross_color = (51, 65, 85, 200)
    for cx in range(80, WIDTH, 160):
        for cy in range(80, HEIGHT, 160):
            draw.line([(cx - 3, cy), (cx + 3, cy)], fill=cross_color)
            draw.line([(cx, cy - 3), (cx, cy + 3)], fill=cross_color)

    # 4. Insignia Frosted Glass superior izquierda (Badge de Serie 1/5 .. 5/5)
    bx, by, bw, bh = 60, 42, 90, 40
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8, fill=(15, 23, 42, 230), outline=(56, 189, 248, 220), width=1)
    # Dibujar icono ADN
    _draw_dna_helix_icon(draw, bx + 10, by + 8, 16, 24, color=(56, 189, 248, 255), stroke_width=2)
    # Separador vertical
    draw.line([(bx + 38, by + 8), (bx + 38, by + bh - 8)], fill=(71, 85, 105, 200), width=1)
    # Texto de parte (ej: 1/5)
    font_badge_num = _get_font(13, bold=True)
    draw.text((bx + 46, by + 11), f"{part_num}/5", fill=(244, 114, 182), font=font_badge_num)

    # Tag de la entrega (junto al badge)
    font_tag = _get_font(12, bold=True)
    draw.rounded_rectangle([bx + bw + 14, by + 4, bx + bw + 14 + len(tag_text) * 8 + 20, by + bh - 4], radius=6, fill=(17, 24, 39, 220), outline=(accent[0], accent[1], accent[2], 160), width=1)
    draw.text((bx + bw + 24, by + 11), tag_text, fill=accent, font=font_tag)

    # Brand Pill superior derecha
    brand_text = "DATALARIA HELIX · SPEC-DRIVEN DEVELOPMENT OS"
    font_brand = _get_font(11, bold=True)
    draw.text((WIDTH - 420, by + 12), brand_text, fill=(148, 163, 184), font=font_brand)

    # 5. Título Principal y Subtítulo
    font_title = _get_font(30, bold=True)
    font_sub = _get_font(15, bold=False)

    draw.text((60, 115), title_text, fill=(249, 250, 251), font=font_title)
    draw.text((60, 172), sub_text, fill=(203, 213, 225), font=font_sub)

    # 6. Cuadrícula de 4 Tarjetas de Pilares Técnicos (2x2)
    card_w = 520
    card_h = 100
    positions = [
        (60, 230),
        (620, 230),
        (60, 350),
        (620, 350),
    ]

    font_pillar_title = _get_font(14, bold=True)
    font_pillar_sub = _get_font(15, bold=True)
    font_pillar_desc = _get_font(12, bold=False)

    for idx, (p_title, p_sub, p_desc) in enumerate(pillars):
        px, py = positions[idx]
        # Fondo de tarjeta oscuro con borde sutil
        draw.rounded_rectangle([px, py, px + card_w, py + card_h], radius=8, fill=(17, 24, 39, 230), outline=(51, 65, 85, 220), width=1)
        # Línea de acento a la izquierda
        draw.rounded_rectangle([px, py, px + 4, py + card_h], radius=2, fill=accent)

        draw.text((px + 20, py + 14), p_title.upper(), fill=accent, font=font_pillar_title)
        draw.text((px + 20, py + 38), p_sub, fill=(241, 245, 249), font=font_pillar_sub)
        draw.text((px + 20, py + 68), p_desc, fill=(148, 163, 184), font=font_pillar_desc)

    # 7. Franja Inferior Ejecutiva con Métricas Clave
    draw.rounded_rectangle([60, 480, 1140, 580], radius=10, fill=(15, 23, 42, 240), outline=(56, 189, 248, 160), width=1)

    kpi_items = [
        ("SpecQualityScore", "100 / 100", "Auditoría formal 5 pilares" if is_es else "5-pillar formal audit"),
        ("Ahorro de Contexto" if is_es else "Context Savings", "~87%", "Carga bajo demanda" if is_es else "On-demand role loading"),
        ("CLI Python Puro" if is_es else "Pure Python CLI", "0 Deps", "helix.py stdlib >= 3.10"),
        ("Lanzamiento" if is_es else "Release Model", "Enero 2027" if is_es else "January 2027", "Starter 9€ · Core 19€"),
    ]

    for k_idx, (k_top, k_main, k_sub) in enumerate(kpi_items):
        kx = 85 + k_idx * 265
        draw.text((kx, 498), k_top, fill=(148, 163, 184), font=_get_font(12, bold=False))
        draw.text((kx, 518), k_main, fill=(56, 189, 248), font=_get_font(22, bold=True))
        draw.text((kx, 550), k_sub, fill=(203, 213, 225), font=_get_font(11, bold=False))

    # Pie institucional
    footer_text = "Datalaria Engineering · https://datalaria.com/apps/helix/"
    font_footer = _get_font(11, bold=False)
    draw.text((60, 598), footer_text, fill=(100, 116, 139), font=font_footer)

    return img.convert("RGB")


def build_all_series_covers() -> List[Path]:
    """Genera las 10 portadas de la serie oficial Datalaria Helix."""
    print("================================================================================")
    print("      GENERADOR DE PORTADAS CONCEPTUALES DATALARIA HELIX (HITO 6.9)")
    print("================================================================================")
    generated: List[Path] = []

    for item in POSTS_CONFIG:
        part = item["part"]

        # Portada ES
        dir_es = ROOT_DIR / "content" / "es" / "posts" / item["slug_es"]
        dir_es.mkdir(parents=True, exist_ok=True)
        path_es = dir_es / "cover.png"
        img_es = create_series_cover(item, lang="es")
        img_es.save(path_es, format="PNG", optimize=True)
        kb_es = round(path_es.stat().st_size / 1024, 1)
        print(f"[COVER ES] Parte {part}/5: {path_es} ({kb_es} KB)")
        generated.append(path_es)

        # Portada EN
        dir_en = ROOT_DIR / "content" / "en" / "posts" / item["slug_en"]
        dir_en.mkdir(parents=True, exist_ok=True)
        path_en = dir_en / "cover.png"
        img_en = create_series_cover(item, lang="en")
        img_en.save(path_en, format="PNG", optimize=True)
        kb_en = round(path_en.stat().st_size / 1024, 1)
        print(f"[COVER EN] Part {part}/5:  {path_en} ({kb_en} KB)")
        generated.append(path_en)

    print(f"\n[OK] Generadas exitosamente {len(generated)} portadas oficiales (1200x630 px).")
    return generated


def main() -> None:
    build_all_series_covers()


if __name__ == "__main__":
    main()
