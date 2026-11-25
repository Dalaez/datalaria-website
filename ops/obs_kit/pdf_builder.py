# -*- coding: utf-8 -*-
"""ops/obs_kit/pdf_builder.py — Playbook Ejecutivo PDF Vectorial de 5 páginas A4 (ES y EN).

Cumple b2b-kit-factory SKILL:
- Exactamente 5 páginas A4 (595 x 842 pt) con geometría segura (x0=40, x1=555).
- Fuentes TrueType UTF-8 (Segoe UI / DejaVu Sans) y gráficos vectoriales con page.new_shape().
- Cero glifos rotos / tofu (□) ni emojis crudos.
- Incluye metodología IEC 62402, protocolo PCN/PDN, matemática LTB vs. FFF + congelación ROP,
  diagrama vectorial de ciclo de vida y matriz comparativa pack-stock (7 €) vs. pack-obs (19 €).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF

PAGE_W = 595.0
PAGE_H = 842.0
X0 = 40.0
X1 = 555.0
CONTENT_W = X1 - X0

# Paleta Executive Data-Dense (design.md)
DARK_BG = (0.043, 0.059, 0.090)       # #0b0f17
DARK_CARD = (0.067, 0.094, 0.153)     # #111827
DARK_BORDER = (0.145, 0.200, 0.298)   # #25334c
CYAN = (0.055, 0.647, 0.914)          # #0ea5e9
VIOLET = (0.545, 0.361, 0.965)        # #8b5cf6
EMERALD = (0.063, 0.725, 0.506)       # #10b981
AMBER = (0.961, 0.620, 0.043)         # #f59e0b
ROSE = (0.937, 0.267, 0.267)          # #ef4444
WHITE = (1.0, 1.0, 1.0)
TEXT_LIGHT = (0.973, 0.980, 0.988)    # #f8fafc
TEXT_MUTED_DARK = (0.796, 0.835, 0.882)
SLATE_900 = (0.059, 0.090, 0.165)     # #0f172a
SLATE_700 = (0.200, 0.255, 0.333)     # #334155
SLATE_500 = (0.392, 0.455, 0.545)     # #64748b
CARD_LIGHT = (0.973, 0.980, 0.988)    # #f8fafc
BORDER_LIGHT = (0.859, 0.898, 0.941)  # #dbe5f0
CYAN_BG = (0.878, 0.949, 0.996)       # #e0f2fe
VIOLET_BG = (0.929, 0.914, 0.996)     # #ede9fe
AMBER_BG = (0.996, 0.953, 0.780)      # #fef3c7
ROSE_BG = (0.996, 0.886, 0.886)       # #fee2e2
EMERALD_BG = (0.820, 0.980, 0.898)    # #d1fae5


@dataclass(frozen=True)
class FontBundle:
    regular: str
    bold: str
    mono: str


def _resolve_ttf() -> tuple[Optional[Path], Optional[Path], Optional[Path]]:
    reg_c = [
        Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
    ]
    bold_c = [
        Path("C:/Windows/Fonts/segoeuib.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
    ]
    mono_c = [
        Path("C:/Windows/Fonts/consola.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"),
    ]
    reg = next((p for p in reg_c if p.exists()), None)
    bold = next((p for p in bold_c if p.exists()), reg)
    mono = next((p for p in mono_c if p.exists()), reg)
    return reg, bold, mono


def _register_fonts(page: fitz.Page) -> FontBundle:
    reg, bold, mono = _resolve_ttf()
    if reg and bold and mono:
        page.insert_font(fontname="dl_reg", fontfile=str(reg))
        page.insert_font(fontname="dl_bold", fontfile=str(bold))
        page.insert_font(fontname="dl_mono", fontfile=str(mono))
        return FontBundle("dl_reg", "dl_bold", "dl_mono")
    return FontBundle("helv", "hebo", "cour")


def _draw_radar_logo(page: fitz.Page, cx: float, cy: float, r: float) -> None:
    shape = page.new_shape()
    shape.draw_circle((cx, cy), r)
    shape.finish(color=DARK_BORDER, fill=DARK_CARD, width=1.4)
    shape.draw_circle((cx, cy), r * 0.68)
    shape.finish(color=CYAN, width=0.9)
    shape.draw_circle((cx, cy), r * 0.34)
    shape.finish(color=VIOLET, width=0.9)
    shape.draw_line((cx - r, cy), (cx + r, cy))
    shape.draw_line((cx, cy - r), (cx, cy + r))
    shape.finish(color=DARK_BORDER, width=0.7)
    shape.draw_line((cx, cy), (cx + r * 0.72, cy - r * 0.64))
    shape.finish(color=TEXT_LIGHT, width=1.6)
    shape.draw_circle((cx + r * 0.45, cy - r * 0.25), 3.6)
    shape.finish(color=AMBER, fill=AMBER)
    shape.draw_circle((cx - r * 0.38, cy + r * 0.32), 2.8)
    shape.finish(color=EMERALD, fill=EMERALD)
    shape.draw_circle((cx, cy), 3.2)
    shape.finish(color=CYAN, fill=WHITE, width=1.2)
    shape.commit()


def _draw_header_footer(page: fitz.Page, fb: FontBundle, page_num: int, total: int, kicker: str, footer_txt: str) -> None:
    shape = page.new_shape()
    shape.draw_rect(fitz.Rect(0, 0, PAGE_W, 44))
    shape.finish(fill=DARK_BG, color=DARK_BG)
    shape.draw_line((X0, 44), (X1, 44))
    shape.finish(color=CYAN, width=1.5)
    shape.draw_line((X0, PAGE_H - 36), (X1, PAGE_H - 36))
    shape.finish(color=BORDER_LIGHT, width=0.8)
    shape.commit()

    page.insert_text((X0, 27), "DATALARIA · AGENTIC RADAR v2.0", fontname=fb.bold, fontsize=9, color=CYAN)
    page.insert_textbox(
        fitz.Rect(240, 16, X1, 34), kicker, fontname=fb.regular, fontsize=8.5, color=TEXT_MUTED_DARK, align=fitz.TEXT_ALIGN_RIGHT
    )
    page.insert_text((X0, PAGE_H - 20), footer_txt, fontname=fb.regular, fontsize=8, color=SLATE_500)
    page.insert_textbox(
        fitz.Rect(420, PAGE_H - 30, X1, PAGE_H - 12),
        f"{page_num} / {total}",
        fontname=fb.bold,
        fontsize=8.5,
        color=SLATE_700,
        align=fitz.TEXT_ALIGN_RIGHT,
    )


def _draw_card(
    page: fitz.Page, rect: fitz.Rect, fill: tuple[float, float, float], border: tuple[float, float, float], radius: float = 0.08
) -> None:
    shape = page.new_shape()
    shape.draw_rect(rect)
    shape.finish(fill=fill, color=border, width=0.9)
    shape.commit()


def _copy_dict(lang: str) -> dict:
    if lang == "es":
        return {
            "badge": "EXECUTIVE PLAYBOOK · ESTÁNDAR IEC 62402 & JEDEC J-STD-048",
            "cover_title": "Gestión de Obsolescencia,\nRiesgo BOM & Decisión\nLast Time Buy (LTB)",
            "cover_sub": (
                "Protocolo cuantitativo C-Level (COO / CFO / Component Engineering) para neutralizar "
                "notificaciones PCN/PDN/EOL, recorrer grafos BOM multinivel y decidir con rigor matemático "
                "entre compra puente Last Time Buy (LTB) o Rediseño Form-Fit-Function (FFF)."
            ),
            "cover_kpis": [
                ("MOTOR EXCEL 5 HOJAS", "Sin macros VBA · Dual ES/EN"),
                ("NORMA INTERNACIONAL", "IEC 62402 · Criticidad 0-100"),
                ("STARTER BLUEPRINT", "PostgreSQL obs_radar + Python"),
            ],
            "cover_meta": "Datalaria Executive Kits · Edicion v2.0.0 · Publicacion oficial: 09 Dic 2026 · datalaria.com",
            "footer": "Datalaria · IEC 62402 Obsolescence, BOM Risk & LTB Decision Kit (v2.0.0)",
            "p2_kicker": "SECCION 1 · METODOLOGIA IEC 62402 & GRAFO BOM",
            "p2_h1": "1. Erradicando el 'Cisne Negro': Explosión DAG de BOM y Criticidad IEC 62402",
            "p2_intro": (
                "En fabricacion electronica, aeroespacial e industrial, un unico condensador o microcontrolador "
                "de 2 EUR discontinuado sin aviso bloquea lineas de ensamblaje con decenas o cientos de miles de euros "
                "en margen bruto P&L comprometido. Este kit sustituye hojas aisladas por un recorrido determinista "
                "ascendente de listas de materiales (BOM) libre de ciclos infinitos."
            ),
            "p2_dag_title": "FLUJO DE PROPAGACION ASCENDENTE EN GRAFO BOM (MPN -> SKU FINAL)",
            "p2_dag_nodes": ["1. Aviso PCN/PDN\n(MPN Fabricante)", "2. Revision AML\n(Fuentes Alt.)", "3. Subensamblaje\n(PCB / Modulo)", "4. SKU Final\n(Margen P&L EUR)"],
            "p2_rubric_title": "Matriz Cuantitativa de Criticidad IEC 62402 (Escala 0 a 100 puntos)",
            "p2_rubric": [
                ("Fuente Unica AML (0–40 pts)", "0 alternativos cualificados = 40 pts · 1 alternativo = 20 pts · >=2 alternativos = 5 pts."),
                ("Urgencia de Ciclo de Vida (0–35 pts)", "Obsolete = 35 pts · EOL = 30 pts · PDN = 22 pts · NRND = 12 pts · Active = 0 pts."),
                ("Exposicion de Lead Time (0–15 pts)", ">=24 semanas = 15 pts · 12–23 semanas = 10 pts · <12 semanas = 4 pts."),
                ("Impacto Financiero P&L (0–10 pts)", ">=150.000 EUR/ano = 10 pts · 50.000–149.999 EUR = 6 pts · <50.000 EUR = 2 pts."),
            ],
            "p2_tiers_title": "Reglas de Accion Directivas y Desacoplo del Punto de Pedido (ROP)",
            "p2_tiers": [
                ("70 – 100 pts · CRITICAL LTB REQUIRED", "CONGELAR ROP recurrente de inmediato. Activar simulacion LTB vs. FFF y bloquear presupuesto CAPEX.", ROSE_BG, ROSE),
                ("40 – 69 pts · DUAL-SOURCE / QUALIFY", "Revisar stock de seguridad y acelerar homologacion de segunda fuente en AML antes de cierre de fabrica.", AMBER_BG, AMBER),
                ("0 – 39 pts · MONITOR (FASE MADUREZ)", "Mantener aprovisionamiento continuo estocastico APICS (SS3 / ROP / EOQ mediante pack-stock).", EMERALD_BG, EMERALD),
            ],
            "p3_kicker": "SECCION 2 · MODELO FINANCIERO LTB VS. REDISENO FFF",
            "p3_h1": "2. Matematica de Decision CFO/COO: Last Time Buy (LTB) vs. Rediseno FFF",
            "p3_intro": (
                "Cuando el fabricante anuncia el fin de vida (PDN/EOL), las formulas clasicas de reposicion periodica "
                "dejan de ser validas porque no existiran mas pedidos en el futuro. La direccion afronta una eleccion "
                "de capital irreversible: inmovilizar tesoreria en una compra puente unica (LTB) o financiar ingenieria "
                "no recurrente (NRE) para redisenar la placa hacia un componente activo (FFF)."
            ),
            "p3_eq1_title": "A. Colchon Puente Unico tras Congelar el ROP (SS_LTB)",
            "p3_eq1_formula": "SS_LTB = ceil( Z * sigma_m * sqrt(H_meses) )   |   Q_LTB = ceil( H_meses * D_m + SS_LTB )",
            "p3_eq1_desc": "Absorbe la incertidumbre acumulada de demanda (sigma_m) durante todo el horizonte remanente H_meses sin opcion de reorden posterior.",
            "p3_eq2_title": "B. Coste Financiero Total del Last Time Buy (C_LTB)",
            "p3_eq2_formula": "C_LTB = (Q_LTB * P_LTB) * [ 1 + (WACC + h_merma) * (H_meses / 24) ]",
            "p3_eq2_desc": "Incorpora el desembolso inicial CAPEX mas el coste real de oportunidad del capital circulante (WACC) y merma/almacenaje sobre el stock medio.",
            "p3_eq3_title": "C. Coste Total del Rediseno Form-Fit-Function (C_FFF) y Equilibrio (T*)",
            "p3_eq3_formula": "C_FFF = NRE_Ing + Coste_Recert + Riesgo_Parada   |   T* = (NRE + Recert) / [ D_m * P_LTB * (1 + 0.5*(WACC+h)) ]",
            "p3_eq3_desc": "Si H_meses < T*, ejecutar LTB preserva caja; si H_meses > T* y C_FFF <= 0.92 * C_LTB, conviene redisenar o ejecutar un puente hibrido.",
            "p3_verdict_title": "Regla de Veredicto Determinista (Paridad Exacta Excel <-> Agentic Radar v2.0)",
            "p3_verdict_body": (
                "1) EXECUTE LTB: cuando C_LTB <= 0.92 * C_FFF (tipico en productos con certificacion medica/aeroespacial costosa o vida restante < 24 meses).\n"
                "2) REDESIGN FFF: cuando C_FFF <= 0.92 * C_LTB (productos flagship con > 36 meses de vida comercial remanente).\n"
                "3) HYBRID BRIDGE: en la banda de indiferencia (+/- 8%), comprar un LTB corto de 12 meses mientras ingenieria homologa el nuevo diseno."
            ),
            "p4_kicker": "SECCION 3 · COMPLEMENTARIEDAD PACK-STOCK VS. PACK-OBS",
            "p4_h1": "3. Sinergia Operativa: Stock de Seguridad (pack-stock) vs. Obsolescencia (pack-obs)",
            "p4_intro": (
                "Uno de los errores mas caros en Supply Chain es intentar gestionar avisos de discontinuacion EOL con "
                "hojas de punto de pedido estandar, o aplicar compras LTB masivas a referencias activas. Ambos kits de "
                "Datalaria forman un circuito complementario sin solapamiento a lo largo del ciclo de vida del componente."
            ),
            "p4_phase1_t": "FASE 1 · MADUREZ (FLUJO CONTINUO)",
            "p4_phase1_b": "pack-stock (7 EUR · Suite 03)\nProveedor activo · Pedidos mensuales\nEst. APICS: SS3, ROP y Wilson EOQ",
            "p4_trig": "AVISO PCN / PDN / EOL\n¡Congelar ROP!",
            "p4_phase2_t": "FASE 2 · FIN DE VIDA (CRISIS BOM)",
            "p4_phase2_b": "pack-obs (19 EUR · Agentic Radar)\nFabrica cierra · Compra puente unica\nEst. IEC 62402: BOM DAG + LTB vs. FFF",
            "p4_table_headers": ["Dimensión", "pack-stock (Stock & ROP · 7 €)", "pack-obs (IEC 62402 LTB · 19 €)"],
            "p4_rows": [
                ("Estado Proveedor", "Activo: admite pedidos recurrentes cada mes.", "En cierre (PDN/EOL): ultima oportunidad de compra."),
                ("Norma Tecnica", "APICS / ASCM & MIT CTL (Revision continua s,Q).", "IEC 62402 & JEDEC J-STD-048 (Obsolescencia)."),
                ("Nivel de Analisis", "SKU individual y almacen central.", "Grafo BOM multinivel (MPN -> AML -> Sub -> SKU)."),
                ("Decision Directiva", "Colchon mensual y lote optimo sin roturas.", "Margen P&L amenazado y CAPEX LTB vs. Rediseno."),
                ("Entregables ZIP", "Excel 35 SKUs + PPTX 16:9 + Guia PDF 5 pags.", "Excel Dual 5 hojas + Blueprint SQL/Python + PDF."),
            ],
            "p5_kicker": "SECCION 4 · DESPLIEGUE Y STARTER BLUEPRINT TECNICO",
            "p5_h1": "4. Plan de Implementacion en 5 Pasos & Arquitectura Starter Blueprint",
            "p5_steps": [
                ("Paso 1 · Inventario BOM & AML (Hoja 01)", "Carga tus referencias criticas en 01_BOM_AML_EXPLORER o usa la plantilla CSV incluida (datalaria_bom_industrial_template.csv)."),
                ("Paso 2 · Auditoria Visual en Agentic Radar v2.0", "Importa tu CSV 100% localmente en datalaria.com/apps/obs-management/ (privacidad total en navegador, cero subida a servidores) para ver el grafo SVG."),
                ("Paso 3 · Priorizacion IEC 62402 (Hoja 02)", "Filtra los componentes >= 70 puntos (CRITICAL LTB REQUIRED) y congela su reposicion automatica ROP en tu ERP."),
                ("Paso 4 · Defensa Financiera ante CFO (Hojas 03 y 05)", "Ajusta WACC, merma y NRE en 03_LTB_VS_FFF_SIMULATOR y exporta el Dashboard C-Level para aprobacion de CAPEX."),
                ("Paso 5 · Automatizacion Continua (Carpeta 03 Blueprint)", "Despliega el esquema PostgreSQL obs_radar con Row-Level Security (RLS) y el motor puro bom_engine.py para ingesta automatica de webhooks PDN."),
            ],
            "p5_box_title": "CONTENIDO AUDITADO DEL PAQUETE .ZIP (VERIFICACION SHA-256)",
            "p5_box_body": (
                "• 01_EXCEL_MOTOR_BOM_LTB/: Libros ES y EN (.xlsx, 5 hojas, 0 macros VBA, tablas nativas y grafico C-Level).\n"
                "• 02_PLAYBOOK_EJECUTIVO_PDF/: Guias vectoriales A4 de 5 paginas en Espanol e Ingles.\n"
                "• 03_STARTER_BLUEPRINT_TECNICO/: obs_radar_supabase_schema.sql (RLS), bom_engine.py, models.py, env.example y plantilla CSV.\n"
                "• SHA256_MANIFEST.txt + LICENSE.txt: Licencia comercial B2B para uso interno de equipo y verificacion criptografica."
            ),
        }
    return {
        "badge": "EXECUTIVE PLAYBOOK · IEC 62402 & JEDEC J-STD-048 STANDARD",
        "cover_title": "Obsolescence Management,\nBOM Risk & Last Time Buy\n(LTB) Decision Playbook",
        "cover_sub": (
            "Boardroom-grade quantitative protocol (COO / CFO / Component Engineering) to neutralize "
            "PCN/PDN/EOL notices, traverse multilevel BOM graphs without cycles, and decide with exact math "
            "between Last Time Buy (LTB) bridge stock and Form-Fit-Function (FFF) Redesign."
        ),
        "cover_kpis": [
            ("5-SHEET EXCEL ENGINE", "Zero VBA Macros · Dual ES/EN"),
            ("GLOBAL STANDARD", "IEC 62402 · 0-100 Criticality"),
            ("STARTER BLUEPRINT", "PostgreSQL obs_radar + Python"),
        ],
        "cover_meta": "Datalaria Executive Kits · Edition v2.0.0 · Official Release: Dec 09, 2026 · datalaria.com",
        "footer": "Datalaria · IEC 62402 Obsolescence, BOM Risk & LTB Decision Kit (v2.0.0)",
        "p2_kicker": "SECTION 1 · IEC 62402 METHODOLOGY & BOM GRAPH",
        "p2_h1": "1. Eradicating the 'Black Swan': Multilevel BOM DAG & IEC 62402 Criticality",
        "p2_intro": (
            "In electronics, aerospace, and industrial manufacturing, a single discontinued EUR 2 capacitor or "
            "microcontroller can halt assembly lines and put hundreds of thousands of euros in annual P&L gross "
            "margin at risk. This kit replaces disconnected spreadsheets with deterministic upward Bill of "
            "Materials (BOM) graph traversal protected against infinite cycles."
        ),
        "p2_dag_title": "UPWARD BOM GRAPH PROPAGATION FLOW (MPN -> END SKU)",
        "p2_dag_nodes": ["1. PCN/PDN Notice\n(Vendor MPN)", "2. AML Audit\n(Alt. Sources)", "3. Sub-Assembly\n(PCB / Module)", "4. Final SKU\n(P&L Margin EUR)"],
        "p2_rubric_title": "Quantitative IEC 62402 Criticality Matrix (0 to 100 Point Scale)",
        "p2_rubric": [
            ("Single-Source AML Risk (0–40 pts)", "0 qualified alternates = 40 pts · 1 alternate = 20 pts · >=2 alternates = 5 pts."),
            ("Lifecycle Urgency (0–35 pts)", "Obsolete = 35 pts · EOL = 30 pts · PDN = 22 pts · NRND = 12 pts · Active = 0 pts."),
            ("Lead-Time Exposure (0–15 pts)", ">=24 weeks = 15 pts · 12–23 weeks = 10 pts · <12 weeks = 4 pts."),
            ("Financial P&L Impact (0–10 pts)", ">=150,000 EUR/yr = 10 pts · 50,000–149,999 EUR = 6 pts · <50,000 EUR = 2 pts."),
        ],
        "p2_tiers_title": "Executive Action Tiers & Reorder Point (ROP) Decoupling Rules",
        "p2_tiers": [
            ("70 – 100 pts · CRITICAL LTB REQUIRED", "FREEZE recurring ROP immediately. Run LTB vs. FFF financial model and ring-fence CAPEX budget.", ROSE_BG, ROSE),
            ("40 – 69 pts · DUAL-SOURCE / QUALIFY", "Audit safety stock exposure and accelerate AML second-source qualification ahead of factory cutoff.", AMBER_BG, AMBER),
            ("0 – 39 pts · MONITOR (MATURITY PHASE)", "Maintain continuous stochastic APICS replenishment (SS3 / ROP / EOQ governed via pack-stock).", EMERALD_BG, EMERALD),
        ],
        "p3_kicker": "SECTION 2 · LTB VS. FFF REDESIGN FINANCIAL MODEL",
        "p3_h1": "2. CFO / COO Decision Math: Last Time Buy (LTB) vs. FFF Redesign",
        "p3_intro": (
            "Once a vendor issues an End-of-Life (PDN/EOL) notice, standard recurring reorder formulas collapse "
            "because no future replenishment orders will exist. Leadership faces an irreversible capital allocation "
            "choice: lock working capital in a one-shot bridge buy (LTB) or fund Non-Recurring Engineering (NRE) "
            "to redesign and recertify the assembly toward an active component (FFF)."
        ),
        "p3_eq1_title": "A. One-Shot Bridge Buffer After Freezing ROP (SS_LTB)",
        "p3_eq1_formula": "SS_LTB = ceil( Z * sigma_m * sqrt(H_months) )   |   Q_LTB = ceil( H_months * D_m + SS_LTB )",
        "p3_eq1_desc": "Absorbs cumulative demand uncertainty (sigma_m) across the entire remaining horizon H_months with zero future reorder option.",
        "p3_eq2_title": "B. Total Financial Cost of Last Time Buy (C_LTB)",
        "p3_eq2_formula": "C_LTB = (Q_LTB * P_LTB) * [ 1 + (WACC + h_decay) * (H_months / 24) ]",
        "p3_eq2_desc": "Captures upfront CAPEX cash outlay plus true working-capital opportunity cost (WACC) and holding/decay expense on average inventory.",
        "p3_eq3_title": "C. Total FFF Redesign Cost (C_FFF) & Break-Even Horizon (T*)",
        "p3_eq3_formula": "C_FFF = NRE_Eng + Recert_Cost + Stoppage_Risk   |   T* = (NRE + Recert) / [ D_m * P_LTB * (1 + 0.5*(WACC+h)) ]",
        "p3_eq3_desc": "If H_months < T*, executing LTB preserves cash; if H_months > T* and C_FFF <= 0.92 * C_LTB, redesign or execute a hybrid bridge.",
        "p3_verdict_title": "Deterministic Verdict Rule (Exact Parity Excel <-> Agentic Radar v2.0)",
        "p3_verdict_body": (
            "1) EXECUTE LTB: when C_LTB <= 0.92 * C_FFF (typical for heavily regulated medical/aerospace SKUs or remaining life < 24 months).\n"
            "2) REDESIGN FFF: when C_FFF <= 0.92 * C_LTB (flagship assemblies with > 36 months of remaining commercial lifecycle).\n"
            "3) HYBRID BRIDGE: within the +/- 8% indifference band, execute a 12-month LTB bridge while engineering qualifies the new design."
        ),
        "p4_kicker": "SECTION 3 · COMPLEMENTARITY PACK-STOCK VS. PACK-OBS",
        "p4_h1": "3. Operational Synergy: Safety Stock (pack-stock) vs. Obsolescence (pack-obs)",
        "p4_intro": (
            "A costly supply-chain mistake is trying to handle EOL discontinuations using recurring reorder sheets, "
            "or applying bulk LTB buys to active parts. Both Datalaria kits form a seamless, zero-overlap two-stage "
            "lifecycle control loop protecting both working capital and manufacturing continuity."
        ),
        "p4_phase1_t": "PHASE 1 · MATURITY (CONTINUOUS FLOW)",
        "p4_phase1_b": "pack-stock (EUR 7 · Suite 03)\nActive vendor · Monthly replenishment\nAPICS Std: SS3, ROP & Wilson EOQ",
        "p4_trig": "PCN / PDN / EOL NOTICE\nFreeze ROP!",
        "p4_phase2_t": "PHASE 2 · END-OF-LIFE (BOM CRISIS)",
        "p4_phase2_b": "pack-obs (EUR 19 · Agentic Radar)\nLine shuts down · One-shot bridge\nIEC 62402: BOM DAG + LTB vs. FFF",
        "p4_table_headers": ["Dimension", "pack-stock (Safety Stock · €7)", "pack-obs (IEC 62402 LTB · €19)"],
        "p4_rows": [
            ("Vendor Status", "Active: accepts recurring monthly orders.", "Closing (PDN/EOL): last chance to buy or redesign."),
            ("Global Standard", "APICS / ASCM & MIT CTL (Continuous s,Q).", "IEC 62402 & JEDEC J-STD-048 (Obsolescence)."),
            ("Analysis Scope", "Individual SKU & central warehouse.", "Multilevel BOM graph (MPN -> AML -> Sub -> SKU)."),
            ("Core Decision", "Monthly buffer & optimal lot without stockouts.", "Threatened P&L margin & CAPEX LTB vs. Redesign."),
            ("ZIP Deliverables", "35-SKU Excel + 16:9 PPTX + 5-page PDF Guide.", "5-sheet Dual Excel + SQL/Python Blueprint + PDF."),
        ],
        "p5_kicker": "SECTION 4 · DEPLOYMENT & TECHNICAL STARTER BLUEPRINT",
        "p5_h1": "4. Five-Step Rollout Plan & Technical Starter Blueprint",
        "p5_steps": [
            ("Step 1 · BOM & AML Baseline (Sheet 01)", "Load critical components into 01_BOM_AML_EXPLORER or adapt the included CSV template (datalaria_bom_industrial_template.csv)."),
            ("Step 2 · Visual BOM Audit in Agentic Radar v2.0", "Import your CSV 100% locally at datalaria.com/apps/obs-management/ (zero server upload, browser-only privacy) to inspect the SVG graph."),
            ("Step 3 · IEC 62402 Triage (Sheet 02)", "Filter components scoring >= 70 (CRITICAL LTB REQUIRED) and immediately freeze automated ERP ROP replenishment."),
            ("Step 4 · CFO / COO Boardroom Defense (Sheets 03 & 05)", "Tune WACC, decay, and NRE assumptions in 03_LTB_VS_FFF_SIMULATOR and present the C-Level Dashboard for CAPEX sign-off."),
            ("Step 5 · Continuous Automation (Folder 03 Blueprint)", "Deploy the obs_radar PostgreSQL schema with Row-Level Security (RLS) and pure bom_engine.py for automated PDN webhook ingestion."),
        ],
        "p5_box_title": "AUDITED .ZIP PACKAGE CONTENTS (SHA-256 VERIFIED)",
        "p5_box_body": (
            "• 01_EXCEL_MOTOR_BOM_LTB/: Dual ES & EN Workbooks (.xlsx, 5 sheets, 0 VBA macros, native tables & C-Level chart).\n"
            "• 02_PLAYBOOK_EJECUTIVO_PDF/: 5-page A4 vector executive guides in both Spanish and English.\n"
            "• 03_STARTER_BLUEPRINT_TECNICO/: obs_radar_supabase_schema.sql (RLS), bom_engine.py, models.py, env.example & CSV template.\n"
            "• SHA256_MANIFEST.txt + LICENSE.txt: Commercial internal-team B2B license & cryptographic integrity manifest."
        ),
    }


def build_pdf_playbook(lang: str, output_path: Path) -> Path:
    """Genera el Playbook Ejecutivo PDF vectorial de exactamente 5 páginas A4 sin glifos rotos."""
    assert lang in ("es", "en")
    c = _copy_dict(lang)
    doc = fitz.open()

    # ==================================================================
    # PAGE 1: EXECUTIVE DARK COVER
    # ==================================================================
    p1 = doc.new_page(width=PAGE_W, height=PAGE_H)
    fb = _register_fonts(p1)
    sh = p1.new_shape()
    sh.draw_rect(fitz.Rect(0, 0, PAGE_W, PAGE_H))
    sh.finish(fill=DARK_BG, color=DARK_BG)
    sh.draw_rect(fitz.Rect(0, 0, PAGE_W, 8))
    sh.finish(fill=CYAN, color=CYAN)
    sh.draw_rect(fitz.Rect(X0, 62, 360, 84))
    sh.finish(fill=DARK_CARD, color=CYAN, width=1.0)
    sh.commit()

    p1.insert_text((X0 + 12, 77), c["badge"], fontname=fb.bold, fontsize=8.5, color=CYAN)
    _draw_radar_logo(p1, X1 - 48, 128, 42)

    p1.insert_textbox(fitz.Rect(X0, 118, 445, 290), c["cover_title"], fontname=fb.bold, fontsize=30, color=TEXT_LIGHT, lineheight=1.18)
    p1.insert_textbox(fitz.Rect(X0, 308, X1, 415), c["cover_sub"], fontname=fb.regular, fontsize=11.5, color=TEXT_MUTED_DARK, lineheight=1.45)

    # 3 KPI Cards on Cover
    card_w = (CONTENT_W - 24) / 3.0
    for idx, (kt, ks) in enumerate(c["cover_kpis"]):
        rx0 = X0 + idx * (card_w + 12)
        rect = fitz.Rect(rx0, 445, rx0 + card_w, 535)
        _draw_card(p1, rect, DARK_CARD, CYAN if idx == 0 else (VIOLET if idx == 1 else EMERALD))
        p1.insert_textbox(fitz.Rect(rx0 + 12, 460, rx0 + card_w - 12, 492), kt, fontname=fb.bold, fontsize=9.5, color=CYAN if idx == 0 else TEXT_LIGHT)
        p1.insert_textbox(fitz.Rect(rx0 + 12, 494, rx0 + card_w - 12, 528), ks, fontname=fb.regular, fontsize=9, color=TEXT_MUTED_DARK)

    # Visual mini architecture strip on cover
    strip = fitz.Rect(X0, 570, X1, 695)
    _draw_card(p1, strip, DARK_CARD, DARK_BORDER)
    p1.insert_text((X0 + 16, 594), "DUAL-MODE ARCHITECTURE: EXCEL 5-SHEET ENGINE + AGENTIC RADAR v2.0 + OBS_RADAR RLS", fontname=fb.bold, fontsize=8.5, color=VIOLET)
    p1.insert_textbox(
        fitz.Rect(X0 + 16, 608, X1 - 16, 684),
        "01_BOM_AML_EXPLORER  ->  02_IEC62402_CRITICALITY  ->  03_LTB_VS_FFF_SIMULATOR  ->  04_MITIGATION_ROADMAP  ->  05_EXECUTIVE_DASHBOARD\n\n"
        "Zero-VBA .xlsx  |  100% Local Browser CSV Parser  |  PostgreSQL obs_radar Schema (RLS)  |  Exact Math Parity (< 0.01 EUR)",
        fontname=fb.mono,
        fontsize=8.2,
        color=TEXT_MUTED_DARK,
        lineheight=1.35,
    )

    p1.insert_textbox(fitz.Rect(X0, PAGE_H - 58, X1, PAGE_H - 28), c["cover_meta"], fontname=fb.regular, fontsize=8.5, color=TEXT_MUTED_DARK)

    # ==================================================================
    # PAGE 2: IEC 62402 METHODOLOGY & BOM DAG
    # ==================================================================
    p2 = doc.new_page(width=PAGE_W, height=PAGE_H)
    fb = _register_fonts(p2)
    _draw_header_footer(p2, fb, 2, 5, c["p2_kicker"], c["footer"])

    p2.insert_textbox(fitz.Rect(X0, 62, X1, 108), c["p2_h1"], fontname=fb.bold, fontsize=16, color=SLATE_900)
    p2.insert_textbox(fitz.Rect(X0, 110, X1, 182), c["p2_intro"], fontname=fb.regular, fontsize=10, color=SLATE_700, lineheight=1.4)

    # Vector DAG Diagram (4 connected boxes)
    _draw_card(p2, fitz.Rect(X0, 192, X1, 300), CARD_LIGHT, BORDER_LIGHT)
    p2.insert_text((X0 + 14, 212), c["p2_dag_title"], fontname=fb.bold, fontsize=9, color=SLATE_900)
    node_w = 104.0
    gap = 21.0
    start_x = X0 + 14
    node_colors = [ROSE_BG, AMBER_BG, CYAN_BG, VIOLET_BG]
    node_borders = [ROSE, AMBER, CYAN, VIOLET]
    sh2 = p2.new_shape()
    for i, label in enumerate(c["p2_dag_nodes"]):
        nx0 = start_x + i * (node_w + gap)
        rect = fitz.Rect(nx0, 226, nx0 + node_w, 284)
        sh2.draw_rect(rect)
        sh2.finish(fill=node_colors[i], color=node_borders[i], width=1.1)
        if i < 3:
            ax0 = nx0 + node_w + 2
            ax1 = nx0 + node_w + gap - 3
            ay = 255
            sh2.draw_line((ax0, ay), (ax1, ay))
            sh2.draw_line((ax1 - 5, ay - 4), (ax1, ay))
            sh2.draw_line((ax1 - 5, ay + 4), (ax1, ay))
            sh2.finish(color=SLATE_500, width=1.2)
    sh2.commit()
    for i, label in enumerate(c["p2_dag_nodes"]):
        nx0 = start_x + i * (node_w + gap)
        p2.insert_textbox(fitz.Rect(nx0 + 4, 236, nx0 + node_w - 4, 278), label, fontname=fb.bold, fontsize=8.3, color=SLATE_900, align=fitz.TEXT_ALIGN_CENTER)

    # Rubric
    p2.insert_text((X0, 330), c["p2_rubric_title"], fontname=fb.bold, fontsize=12, color=SLATE_900)
    y = 344.0
    for idx, (rt, rd) in enumerate(c["p2_rubric"]):
        _draw_card(p2, fitz.Rect(X0, y, X1, y + 46), CARD_LIGHT if idx % 2 == 0 else WHITE, BORDER_LIGHT)
        p2.insert_text((X0 + 12, y + 18), rt, fontname=fb.bold, fontsize=9.5, color=SLATE_900)
        p2.insert_textbox(fitz.Rect(X0 + 12, y + 23, X1 - 12, y + 44), rd, fontname=fb.regular, fontsize=8.8, color=SLATE_700)
        y += 52.0

    # Action Tiers
    p2.insert_text((X0, 574), c["p2_tiers_title"], fontname=fb.bold, fontsize=12, color=SLATE_900)
    ty = 588.0
    for tt, td, tbg, tbd in c["p2_tiers"]:
        _draw_card(p2, fitz.Rect(X0, ty, X1, ty + 58), tbg, tbd)
        p2.insert_text((X0 + 14, ty + 20), tt, fontname=fb.bold, fontsize=9.8, color=SLATE_900)
        p2.insert_textbox(fitz.Rect(X0 + 14, ty + 26, X1 - 14, ty + 54), td, fontname=fb.regular, fontsize=9, color=SLATE_700, lineheight=1.25)
        ty += 66.0

    # ==================================================================
    # PAGE 3: FINANCIAL MATH (LTB VS. FFF & FREEZING ROP)
    # ==================================================================
    p3 = doc.new_page(width=PAGE_W, height=PAGE_H)
    fb = _register_fonts(p3)
    _draw_header_footer(p3, fb, 3, 5, c["p3_kicker"], c["footer"])

    p3.insert_textbox(fitz.Rect(X0, 62, X1, 108), c["p3_h1"], fontname=fb.bold, fontsize=16, color=SLATE_900)
    p3.insert_textbox(fitz.Rect(X0, 110, X1, 184), c["p3_intro"], fontname=fb.regular, fontsize=10, color=SLATE_700, lineheight=1.4)

    eq_blocks = [
        (c["p3_eq1_title"], c["p3_eq1_formula"], c["p3_eq1_desc"], CYAN_BG, CYAN),
        (c["p3_eq2_title"], c["p3_eq2_formula"], c["p3_eq2_desc"], VIOLET_BG, VIOLET),
        (c["p3_eq3_title"], c["p3_eq3_formula"], c["p3_eq3_desc"], AMBER_BG, AMBER),
    ]
    ey = 196.0
    for et, ef, ed, ebg, ebd in eq_blocks:
        _draw_card(p3, fitz.Rect(X0, ey, X1, ey + 114), CARD_LIGHT, BORDER_LIGHT)
        p3.insert_text((X0 + 14, ey + 22), et, fontname=fb.bold, fontsize=10.5, color=SLATE_900)
        _draw_card(p3, fitz.Rect(X0 + 14, ey + 30, X1 - 14, ey + 64), ebg, ebd)
        p3.insert_textbox(fitz.Rect(X0 + 22, ey + 40, X1 - 22, ey + 62), ef, fontname=fb.mono, fontsize=8.8, color=SLATE_900)
        p3.insert_textbox(fitz.Rect(X0 + 14, ey + 70, X1 - 14, ey + 108), ed, fontname=fb.regular, fontsize=9.2, color=SLATE_700, lineheight=1.32)
        ey += 126.0

    # Verdict box
    _draw_card(p3, fitz.Rect(X0, 588, X1, 760), DARK_BG, CYAN)
    p3.insert_text((X0 + 16, 614), c["p3_verdict_title"], fontname=fb.bold, fontsize=11, color=CYAN)
    p3.insert_textbox(fitz.Rect(X0 + 16, 628, X1 - 16, 748), c["p3_verdict_body"], fontname=fb.regular, fontsize=9.6, color=TEXT_LIGHT, lineheight=1.55)

    # ==================================================================
    # PAGE 4: OPERATIONAL SYNERGY (PACK-STOCK VS. PACK-OBS)
    # ==================================================================
    p4 = doc.new_page(width=PAGE_W, height=PAGE_H)
    fb = _register_fonts(p4)
    _draw_header_footer(p4, fb, 4, 5, c["p4_kicker"], c["footer"])

    p4.insert_textbox(fitz.Rect(X0, 62, X1, 108), c["p4_h1"], fontname=fb.bold, fontsize=15.5, color=SLATE_900)
    p4.insert_textbox(fitz.Rect(X0, 110, X1, 180), c["p4_intro"], fontname=fb.regular, fontsize=10, color=SLATE_700, lineheight=1.4)

    # 2-Phase Lifecycle Vector Diagram
    _draw_card(p4, fitz.Rect(X0, 194, X0 + 185, 314), EMERALD_BG, EMERALD)
    p4.insert_textbox(fitz.Rect(X0 + 10, 204, X0 + 175, 232), c["p4_phase1_t"], fontname=fb.bold, fontsize=8.8, color=SLATE_900, align=fitz.TEXT_ALIGN_CENTER)
    p4.insert_textbox(fitz.Rect(X0 + 10, 238, X0 + 175, 306), c["p4_phase1_b"], fontname=fb.regular, fontsize=8.8, color=SLATE_700, align=fitz.TEXT_ALIGN_CENTER, lineheight=1.35)

    _draw_card(p4, fitz.Rect(X0 + 205, 224, X0 + 310, 286), AMBER_BG, AMBER)
    p4.insert_textbox(fitz.Rect(X0 + 210, 234, X0 + 305, 280), c["p4_trig"], fontname=fb.bold, fontsize=8.5, color=SLATE_900, align=fitz.TEXT_ALIGN_CENTER, lineheight=1.3)

    _draw_card(p4, fitz.Rect(X0 + 330, 194, X1, 314), VIOLET_BG, VIOLET)
    p4.insert_textbox(fitz.Rect(X0 + 340, 204, X1 - 10, 232), c["p4_phase2_t"], fontname=fb.bold, fontsize=8.8, color=SLATE_900, align=fitz.TEXT_ALIGN_CENTER)
    p4.insert_textbox(fitz.Rect(X0 + 340, 238, X1 - 10, 306), c["p4_phase2_b"], fontname=fb.regular, fontsize=8.8, color=SLATE_700, align=fitz.TEXT_ALIGN_CENTER, lineheight=1.35)

    sh4 = p4.new_shape()
    sh4.draw_line((X0 + 185, 255), (X0 + 204, 255))
    sh4.draw_line((X0 + 310, 255), (X0 + 329, 255))
    sh4.finish(color=SLATE_900, width=1.6)
    sh4.commit()

    # Comparison Table (Anti-Confusion Matrix)
    col_x = [X0, X0 + 105, X0 + 310, X1]
    ty = 342.0
    _draw_card(p4, fitz.Rect(col_x[0], ty, col_x[3], ty + 32), DARK_BG, DARK_BG)
    for idx_h, htxt in enumerate(c["p4_table_headers"]):
        p4.insert_textbox(fitz.Rect(col_x[idx_h] + 6, ty + 8, col_x[idx_h + 1] - 6, ty + 28), htxt, fontname=fb.bold, fontsize=8.5, color=WHITE)
    ty += 32.0
    for idx_r, (d0, d1, d2) in enumerate(c["p4_rows"]):
        row_h = 56.0
        bg_row = CARD_LIGHT if idx_r % 2 == 0 else WHITE
        _draw_card(p4, fitz.Rect(col_x[0], ty, col_x[1], ty + row_h), bg_row, BORDER_LIGHT)
        _draw_card(p4, fitz.Rect(col_x[1], ty, col_x[2], ty + row_h), CYAN_BG if idx_r % 2 == 0 else WHITE, BORDER_LIGHT)
        _draw_card(p4, fitz.Rect(col_x[2], ty, col_x[3], ty + row_h), VIOLET_BG if idx_r % 2 == 0 else WHITE, BORDER_LIGHT)
        p4.insert_textbox(fitz.Rect(col_x[0] + 6, ty + 12, col_x[1] - 6, ty + row_h - 6), d0, fontname=fb.bold, fontsize=8.8, color=SLATE_900)
        p4.insert_textbox(fitz.Rect(col_x[1] + 8, ty + 12, col_x[2] - 8, ty + row_h - 6), d1, fontname=fb.regular, fontsize=8.8, color=SLATE_700, lineheight=1.3)
        p4.insert_textbox(fitz.Rect(col_x[2] + 8, ty + 12, col_x[3] - 8, ty + row_h - 6), d2, fontname=fb.bold if idx_r == 4 else fb.regular, fontsize=8.8, color=SLATE_900, lineheight=1.3)
        ty += row_h

    # ==================================================================
    # PAGE 5: 5-STEP DEPLOYMENT & STARTER BLUEPRINT
    # ==================================================================
    p5 = doc.new_page(width=PAGE_W, height=PAGE_H)
    fb = _register_fonts(p5)
    _draw_header_footer(p5, fb, 5, 5, c["p5_kicker"], c["footer"])

    p5.insert_textbox(fitz.Rect(X0, 62, X1, 108), c["p5_h1"], fontname=fb.bold, fontsize=16, color=SLATE_900)

    sy = 122.0
    for idx, (st, sb) in enumerate(c["p5_steps"]):
        _draw_card(p5, fitz.Rect(X0, sy, X1, sy + 78), CARD_LIGHT if idx % 2 == 0 else WHITE, BORDER_LIGHT)
        badge_sh = p5.new_shape()
        badge_sh.draw_circle((X0 + 24, sy + 39), 13)
        badge_sh.finish(fill=DARK_BG, color=CYAN, width=1.2)
        badge_sh.commit()
        p5.insert_textbox(fitz.Rect(X0 + 11, sy + 31, X0 + 37, sy + 49), str(idx + 1), fontname=fb.bold, fontsize=10.5, color=WHITE, align=fitz.TEXT_ALIGN_CENTER)
        p5.insert_text((X0 + 48, sy + 24), st, fontname=fb.bold, fontsize=10.2, color=SLATE_900)
        p5.insert_textbox(fitz.Rect(X0 + 48, sy + 32, X1 - 14, sy + 72), sb, fontname=fb.regular, fontsize=9.2, color=SLATE_700, lineheight=1.32)
        sy += 88.0

    # Audited ZIP Box
    _draw_card(p5, fitz.Rect(X0, 582, X1, 764), DARK_BG, EMERALD)
    p5.insert_text((X0 + 16, 608), c["p5_box_title"], fontname=fb.bold, fontsize=10.5, color=EMERALD)
    p5.insert_textbox(fitz.Rect(X0 + 16, 624, X1 - 16, 752), c["p5_box_body"], fontname=fb.regular, fontsize=9.2, color=TEXT_LIGHT, lineheight=1.55)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    doc.close()
    return output_path
