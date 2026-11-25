# -*- coding: utf-8 -*-
"""ops/obs_kit/build_post_visuals.py — Portadas 1200x630, preview-pack.png y diagrama ADR-028 para OBS-5."""

from __future__ import annotations

import shutil
from pathlib import Path
from PIL import Image, ImageDraw

from ops.obs_kit.visuals_builder import (
    AMBER,
    BG_DARK,
    BORDER_DARK,
    CARD_DARK,
    CYAN,
    EMERALD,
    MUTED,
    VIOLET,
    WHITE,
    _draw_badge,
    _draw_radar_icon,
    _get_font,
    build_store_cover,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
ES_DIR = REPO_ROOT / "content" / "es" / "posts" / "obs_parte8_simulador_ltb_v2"
EN_DIR = REPO_ROOT / "content" / "en" / "posts" / "obs_part8_ltb_simulator_v2"
PKG_DIR = REPO_ROOT / "packages" / "obs_kit"


def build_lifecycle_relay_png(lang: str, output_path: Path) -> Path:
    """Genera el diagrama PNG de respaldo ADR-028 para {{< mermaid image='obs_lifecycle_relay.png' >}}."""
    w, h = 1440, 520
    img = Image.new("RGB", (w, h), BG_DARK)
    draw = ImageDraw.Draw(img)

    f_head = _get_font(22, bold=True)
    f_box_t = _get_font(19, bold=True)
    f_box_b = _get_font(15, bold=False)
    f_badge = _get_font(14, bold=True)

    title = (
        "EL RELEVO MATEMÁTICO EN EL CICLO DE VIDA DEL COMPONENTE (CERO SOLAPAMIENTO)"
        if lang == "es"
        else "THE TWO-STAGE COMPONENT LIFECYCLE RELAY (ZERO OVERLAP)"
    )
    draw.text((48, 28), title, fill=WHITE, font=f_head)

    # Box 1: Phase 1 Maturity (pack-stock)
    draw.rounded_rectangle([48, 86, 468, 466], radius=16, fill=CARD_DARK, outline=EMERALD, width=3)
    _draw_badge(draw, 72, 112, "FASE 1 · MADUREZ (FLUJO CONTINUO)" if lang == "es" else "PHASE 1 · MATURITY (CONTINUOUS FLOW)", EMERALD, BG_DARK, f_badge)
    b1_title = "Calculadora Stock Seguridad & ROP\n(pack-stock · 7 € / Suite 03)" if lang == "es" else "Safety Stock & ROP Calculator\n(pack-stock · €7 / Suite 03)"
    draw.text((72, 162), b1_title, fill=WHITE, font=f_box_t)
    b1_lines = (
        [
            "• Proveedor Activo (pedidos recurrentes)",
            "• Estándar APICS / ASCM & MIT CTL",
            "• Convolución Demanda + Lead Time (SS3)",
            "• Umbral Punto de Pedido (ROP = d·L + SS3)",
            "• Lote Económico de Wilson (EOQ)",
            "• Protege servicio 98% y libera Working Capital",
        ]
        if lang == "es"
        else [
            "• Active vendor (recurring monthly orders)",
            "• APICS / ASCM & MIT CTL Standard",
            "• Demand & Lead-Time Convolution (SS3)",
            "• Dynamic Reorder Point (ROP = d·L + SS3)",
            "• Wilson Economic Order Quantity (EOQ)",
            "• Secures 98% fill rate & unlocks Working Capital",
        ]
    )
    ly = 236
    for ln in b1_lines:
        draw.text((72, ly), ln, fill=MUTED, font=f_box_b)
        ly += 34

    # Arrow 1 -> Trigger
    draw.line([468, 276, 540, 276], fill=AMBER, width=4)
    draw.polygon([(540, 276), (526, 268), (526, 284)], fill=AMBER)

    # Center Trigger: PCN / PDN / EOL
    draw.rounded_rectangle([544, 168, 896, 384], radius=16, fill=(38, 28, 15), outline=AMBER, width=3)
    _draw_badge(draw, 574, 194, "DISRUPCIÓN DE CICLO DE VIDA" if lang == "es" else "LIFECYCLE DISRUPTION EVENT", AMBER, BG_DARK, f_badge)
    trig_txt = (
        "Aviso PCN / PDN / EOL\n(Fabricante cierra línea)\n\nACCION INMEDIATA:\nCONGELAR EL ROP AUTOMÁTICO"
        if lang == "es"
        else "PCN / PDN / EOL Notice\n(Vendor closes prod line)\n\nIMMEDIATE RULE:\nFREEZE RECURRING ROP"
    )
    draw.text((574, 240), trig_txt, fill=WHITE, font=f_box_b)

    # Arrow Trigger -> Phase 2
    draw.line([896, 276, 968, 276], fill=CYAN, width=4)
    draw.polygon([(968, 276), (954, 268), (954, 284)], fill=CYAN)

    # Box 2: Phase 2 EOL (Agentic Radar v2.0 + pack-obs)
    draw.rounded_rectangle([972, 86, 1392, 466], radius=16, fill=CARD_DARK, outline=CYAN, width=3)
    _draw_badge(draw, 996, 112, "FASE 2 · FIN DE VIDA (CRISIS BOM)" if lang == "es" else "PHASE 2 · END-OF-LIFE (BOM CRISIS)", CYAN, BG_DARK, f_badge)
    b2_title = "Agentic Radar v2.0 + Kit IEC 62402\n(obs-management + pack-obs · 19 €)" if lang == "es" else "Agentic Radar v2.0 + IEC 62402 Kit\n(obs-management + pack-obs · €19)"
    draw.text((996, 162), b2_title, fill=WHITE, font=f_box_t)
    b2_lines = (
        [
            "• Proveedor cierra (sin futuros pedidos)",
            "• Estándar Internacional IEC 62402",
            "• Explosión Grafo BOM (MPN -> AML -> SKU)",
            "• Colchón puente único SS_LTB (H meses)",
            "• Decisión CAPEX: LTB (WACC) vs. Rediseño FFF",
            "• Blindaje P&L y Blueprint obs_radar RLS",
        ]
        if lang == "es"
        else [
            "• Line shutting down (no future reorders)",
            "• International IEC 62402 Standard",
            "• Multilevel BOM DAG (MPN -> AML -> SKU)",
            "• One-shot bridge buffer SS_LTB (H months)",
            "• CAPEX Verdict: LTB (WACC) vs. FFF Redesign",
            "• P&L protection & obs_radar RLS Blueprint",
        ]
    )
    ly = 236
    for ln in b2_lines:
        draw.text((996, ly), ln, fill=MUTED, font=f_box_b)
        ly += 34

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, format="PNG", optimize=True)
    return output_path


def main() -> None:
    ES_DIR.mkdir(parents=True, exist_ok=True)
    EN_DIR.mkdir(parents=True, exist_ok=True)

    pdf_es = PKG_DIR / "Playbook_Ejecutivo_IEC62402_LTB_ES.pdf"
    pdf_en = PKG_DIR / "Executive_Playbook_IEC62402_LTB_EN.pdf"
    cov_es = REPO_ROOT / "content" / "es" / "apps" / "obs-management" / "cover.png"
    cov_en = REPO_ROOT / "content" / "en" / "apps" / "obs-management" / "cover.png"

    # 1. Portadas 1200x630 Safe Zone para ambos posts
    build_store_cover("es", 1200, 630, pdf_es, cov_es, ES_DIR / "cover.png")
    build_store_cover("en", 1200, 630, pdf_en, cov_en, EN_DIR / "cover.png")

    # 2. Copia real de preview-pack.png (1600x980) desde static/images/recursos/
    shutil.copy2(REPO_ROOT / "static" / "images" / "recursos" / "obs-preview-es.png", ES_DIR / "preview-pack.png")
    shutil.copy2(REPO_ROOT / "static" / "images" / "recursos" / "obs-preview-en.png", EN_DIR / "preview-pack.png")

    # 3. Diagrama PNG de respaldo ADR-028
    build_lifecycle_relay_png("es", ES_DIR / "obs_lifecycle_relay.png")
    build_lifecycle_relay_png("en", EN_DIR / "obs_lifecycle_relay.png")

    print("OK: Portadas 1200x630, preview-pack.png y obs_lifecycle_relay.png generados para ES y EN.")


if __name__ == "__main__":
    main()
