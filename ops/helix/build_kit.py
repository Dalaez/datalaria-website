"""
ops/helix/build_kit.py
----------------------
Empaquetador Comercial Maestro de Datalaria Helix (Hito 6.8).
Especificación: SPEC-APP-HELIX (specs/apps/helix/spec.md & plan_hito_6_8_ejecucion_flash.md).

Genera de manera determinista:
  1. Guía Ejecutiva PDF A4 (GUIA_EJECUTIVA_HELIX_SDD.pdf) con PyMuPDF (fitz).
  2. Starter Kit (Datalaria_Helix_Starter_Kit.zip · 9 €) en 3 carpetas numeradas.
  3. Core Kit (Datalaria_Helix_Core_Kit.zip y kit-datalaria-helix-core-v1.0.0.zip · 19 €/39 €)
     en 5 carpetas con los 12 agentes, 3 blueprints, CLI helix.py y 2 casos de estudio.
  4. Previews de catálogo de alta resolución (1600x980 px) y portadas cover.png (1200x750 px).
  5. Sincronización automática con packages/00_DISTRIBUCION_LEMONSQUEEZY/.
"""

from __future__ import annotations

import io
import os
import sys
import shutil
import zipfile
import hashlib
from pathlib import Path
from typing import List, Tuple, Optional

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

PACKAGES_HELIX_DIR = ROOT_DIR / "packages" / "helix"
LEMON_DIST_DIR = ROOT_DIR / "packages" / "00_DISTRIBUCION_LEMONSQUEEZY"
PDF_GUIDE_PATH = PACKAGES_HELIX_DIR / "GUIA_EJECUTIVA_HELIX_SDD.pdf"
STARTER_ZIP_PATH = PACKAGES_HELIX_DIR / "Datalaria_Helix_Starter_Kit.zip"
CORE_ZIP_PATH = PACKAGES_HELIX_DIR / "Datalaria_Helix_Core_Kit.zip"
CORE_VERSIONED_ZIP_PATH = PACKAGES_HELIX_DIR / "kit-datalaria-helix-core-v1.0.0.zip"

from ops.helix.build_core_kit import build_core_kit


def compute_sha256(file_path: Path) -> str:
    """Calcula el hash SHA-256 de un archivo binario."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


# ==============================================================================
# 1. GENERADOR DE LA GUÍA EJECUTIVA PDF (PyMuPDF - 4 Páginas A4)
# ==============================================================================

def draw_pdf_header_footer(page: fitz.Page, page_num: int, total_pages: int = 4) -> None:
    """Inserta cabecera y pie ejecutivos con líneas de diseño en páginas 2, 3 y 4."""
    if page_num == 1:
        return  # Portada limpia

    # Línea y título cabecera
    page.draw_rect(fitz.Rect(50, 40, 545, 41.5), color=(0.22, 0.74, 0.97), fill=(0.22, 0.74, 0.97))  # #38bdf8
    page.insert_text(
        fitz.Point(50, 35),
        "DATALARIA HELIX — SPEC-DRIVEN DEVELOPMENT & 12-AGENT SQUAD",
        fontsize=8,
        fontname="helv",
        color=(0.58, 0.64, 0.72),
    )
    page.insert_text(
        fitz.Point(440, 35),
        "MANUAL EJECUTIVO v1.0",
        fontsize=8,
        fontname="helv",
        color=(0.08, 0.65, 0.95),
    )

    # Pie de página
    page.draw_rect(fitz.Rect(50, 805, 545, 806), color=(0.2, 0.25, 0.33), fill=(0.2, 0.25, 0.33))
    page.insert_text(
        fitz.Point(50, 818),
        "© 2026 Datalaria.com — Propiedad y Gobernanza de Ingenieria bajo SDD",
        fontsize=8,
        fontname="helv",
        color=(0.58, 0.64, 0.72),
    )
    page.insert_text(
        fitz.Point(510, 818),
        f"{page_num} / {total_pages}",
        fontsize=8,
        fontname="helv",
        color=(0.38, 0.44, 0.52),
    )


def build_helix_pdf_guide(output_path: Path = PDF_GUIDE_PATH) -> Path:
    """Genera el manual ejecutivo en PDF A4 de 4 páginas de Datalaria Helix."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()

    # --------------------------------------------------------------------------
    # PÁGINA 1: PORTADA EJECUTIVA DARK COCKPIT (#0b0f17)
    # --------------------------------------------------------------------------
    p1 = doc.new_page(width=595, height=842)
    # Fondo completo #0b0f17
    p1.draw_rect(fitz.Rect(0, 0, 595, 842), color=(0.043, 0.059, 0.09), fill=(0.043, 0.059, 0.09))

    # Acento superior cian (#38bdf8)
    p1.draw_rect(fitz.Rect(50, 60, 545, 64), color=(0.22, 0.74, 0.97), fill=(0.22, 0.74, 0.97))

    p1.insert_text(
        fitz.Point(50, 110),
        "DATALARIA ENGINEERING · OPERATIONS & APPLIED AI",
        fontsize=10,
        fontname="helv",
        color=(0.22, 0.74, 0.97),
    )

    p1.insert_text(
        fitz.Point(50, 155),
        "Datalaria Helix",
        fontsize=34,
        fontname="helv",
        color=(0.976, 0.98, 0.984),
    )

    p1.insert_text(
        fitz.Point(50, 190),
        "Spec-Driven Development & 12-Agent Engineering Squad",
        fontsize=18,
        fontname="helv",
        color=(0.612, 0.639, 0.686),
    )

    p1.insert_text(
        fitz.Point(50, 220),
        "Manual Maestro de Gobernanza Agentica, Triaje Determinista y Rollback",
        fontsize=12,
        fontname="helv",
        color=(0.22, 0.74, 0.97),
    )

    # Caja de Entregables Comerciales
    p1.draw_rect(fitz.Rect(50, 255, 545, 435), color=(0.067, 0.094, 0.153), fill=(0.067, 0.094, 0.153))
    p1.draw_rect(fitz.Rect(50, 255, 54, 435), color=(0.22, 0.74, 0.97), fill=(0.22, 0.74, 0.97))

    p1.insert_text(
        fitz.Point(70, 285),
        "ARQUITECTURA DEL ENTREGABLE B2B (EDICION COMERCIAL v1.0):",
        fontsize=11,
        fontname="helv",
        color=(0.976, 0.98, 0.984),
    )

    bullets = [
        ("01_Constitution_and_Memory:", "Constitucion v1.1.0, AGENTS.md, CLAUDE.md y memoria persistente."),
        ("02_Templates:", "Plantillas homologadas de spec.md, design.md y agent-spec.md."),
        ("03_Squad_12_Agents_and_Adapters:", "12 agentes canonicos + adaptadores Antigravity, Claude y Cursor."),
        ("04_Project_Blueprints:", "3 arquitecturas llave en mano (Calculadora JS, SaaS Supabase, Quant)."),
        ("05_Case_Studies_and_Docs:", "Operacion Crisol (Pulse) + MarginGuard B2B + CLI helix.py (0 dependencias)."),
    ]
    b_y = 315
    for b_title, b_desc in bullets:
        p1.insert_text(fitz.Point(70, b_y), b_title, fontsize=9.5, fontname="helv", color=(0.22, 0.74, 0.97))
        p1.insert_text(fitz.Point(260, b_y), b_desc, fontsize=8.5, fontname="helv", color=(0.898, 0.91, 0.922))
        b_y += 24

    # Caja izquierda: Comparativa TCO y Ahorro de Tokens
    p1.draw_rect(fitz.Rect(50, 460, 285, 600), color=(0.067, 0.094, 0.153), fill=(0.067, 0.094, 0.153))
    p1.insert_text(fitz.Point(65, 490), "COMPARATIVA TCO Y AHORRO DE TOKENS", fontsize=9, fontname="helv", color=(0.976, 0.98, 0.984))
    p1.insert_text(fitz.Point(65, 515), "- Vibe Coding tradicional: ~140.000 tokens / tarea", fontsize=8.5, fontname="helv", color=(0.937, 0.267, 0.267))
    p1.insert_text(fitz.Point(65, 535), "- Datalaria Helix SDD: ~18.500 tokens (~87% ahorro)", fontsize=8.5, fontname="helv", color=(0.22, 0.74, 0.97))
    p1.insert_text(fitz.Point(65, 555), "- Rollback en 1 comando: marcha atras determinista", fontsize=8.5, fontname="helv", color=(0.898, 0.91, 0.922))
    p1.insert_text(fitz.Point(65, 575), "- SpecQualityScore: evaluacion formal 0..100 puntos", fontsize=8.5, fontname="helv", color=(0.063, 0.725, 0.506))

    # Caja derecha: Compatibilidad Multi-Herramienta
    p1.draw_rect(fitz.Rect(305, 460, 545, 600), color=(0.067, 0.094, 0.153), fill=(0.067, 0.094, 0.153))
    p1.insert_text(fitz.Point(320, 490), "COMPATIBILIDAD MULTI-HERRAMIENTA", fontsize=9, fontname="helv", color=(0.976, 0.98, 0.984))
    p1.insert_text(fitz.Point(320, 515), "- Google Antigravity (Gemini 3.8 Flash & Argon)", fontsize=8.5, fontname="helv", color=(0.898, 0.91, 0.922))
    p1.insert_text(fitz.Point(320, 535), "- Anthropic Claude Code & Agentes Claude (.claude/)", fontsize=8.5, fontname="helv", color=(0.898, 0.91, 0.922))
    p1.insert_text(fitz.Point(320, 555), "- Cursor IDE (.cursor/rules/) & OpenAI Codex", fontsize=8.5, fontname="helv", color=(0.898, 0.91, 0.922))
    p1.insert_text(fitz.Point(320, 575), "- Python >= 3.10 (0 dependencias externas en CLI)", fontsize=8.5, fontname="helv", color=(0.22, 0.74, 0.97))

    # Pie portada
    p1.insert_text(fitz.Point(50, 750), "Desarrollado y gobernado bajo el framework Spec-Driven Development (SDD)", fontsize=9, fontname="helv", color=(0.612, 0.639, 0.686))
    p1.insert_text(fitz.Point(50, 768), "Datalaria Engineering — https://datalaria.com/apps/helix/", fontsize=9, fontname="helv", color=(0.22, 0.74, 0.97))

    # --------------------------------------------------------------------------
    # PÁGINA 2: EL ESCUADRÓN DE 12 AGENTES Y TRIAJE DETERMINISTA
    # --------------------------------------------------------------------------
    p2 = doc.new_page(width=595, height=842)
    draw_pdf_header_footer(p2, 2)

    p2.insert_text(fitz.Point(50, 75), "1. El Escuadron Canonico de 12 Agentes", fontsize=18, fontname="helv", color=(0.06, 0.1, 0.16))
    p2.insert_text(
        fitz.Point(50, 95),
        "Estructura modular en 4 celulas con separacion estricta de poderes y veto vinculante.",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.35, 0.42),
    )

    cells = [
        ("Celula 1: Direccion (01-03)", "01-orchestrator (Triaje XS-XL y Entrega), 02-product-analyst (Entrevista y spec.md), 03-architect (Constitucion, ADR y division modular)."),
        ("Celula 2: Construccion (04-09)", "04-ux-ui (Tokens visuales y design.md), 05-frontend (React 19 y UI limpia), 06-backend-data (Python y SQL), 07-apis-integrations (MCP y Webhooks), 08-media-i18n (Bilinguismo ES/EN), 09-monetization (PLG y Checkout)."),
        ("Celula 3: Garantia con Veto (10-11)", "10-security-privacy (Aislamiento RLS, secretos y firewall static/) y 11-qa-verifier (Gates automatizados deterministas). AMBOS POSEEN DERECHO A VETO VINCULANTE."),
        ("Celula 4: Entrega (12)", "12-release-devops (Checkpoints Git, empaquetado ZIP comercial, SemVer y ejecucion de Rollback al segundo fallo consecutivo)."),
    ]
    y_pos = 125
    for c_title, c_desc in cells:
        p2.draw_rect(fitz.Rect(50, y_pos, 545, y_pos + 46), color=(0.95, 0.96, 0.98), fill=(0.95, 0.96, 0.98))
        p2.draw_rect(fitz.Rect(50, y_pos, 54, y_pos + 46), color=(0.08, 0.65, 0.95), fill=(0.08, 0.65, 0.95))
        p2.insert_text(fitz.Point(65, y_pos + 16), c_title, fontsize=10, fontname="helv", color=(0.06, 0.1, 0.16))
        p2.insert_text(fitz.Point(65, y_pos + 33), c_desc, fontsize=8, fontname="helv", color=(0.28, 0.33, 0.39))
        y_pos += 52

    p2.insert_text(fitz.Point(50, 360), "2. Regla de Carga Bajo Demanda y Triaje Determinista (INV-HELIX-2)", fontsize=13, fontname="helv", color=(0.06, 0.1, 0.16))
    triage_rules = [
        ("Talla XS (1 archivo, 1 superficie):", "Solo se activan 01-orchestrator y 11-qa-verifier + 1 rol constructor especifico."),
        ("Talla S (2-3 archivos, 1 superficie):", "Activacion del constructor directo + 11-qa-verifier."),
        ("Talla M (2 superficies o >3 archivos):", "Se incorporan 03-architect y 12-release-devops para asegurar gobernanza."),
        ("Tallas L / XL (Cambios de contrato o App nueva):", "Convocatoria ampliada con 02-product-analyst y 04-ux-ui."),
        ("Disparadores Innegociables:", "TRG-SEC activa siempre a 10-security; TRG-UX activa a 04; TRG-QA aplica en toda tarea."),
    ]
    y_trg = 385
    for t_title, t_desc in triage_rules:
        p2.insert_text(fitz.Point(65, y_trg), t_title, fontsize=9, fontname="helv", color=(0.08, 0.65, 0.95))
        p2.insert_text(fitz.Point(230, y_trg), t_desc, fontsize=8, fontname="helv", color=(0.28, 0.33, 0.39))
        y_trg += 20

    # Cuadro destacado Anti-Bloat
    p2.draw_rect(fitz.Rect(50, 510, 545, 620), color=(0.92, 0.96, 0.99), fill=(0.92, 0.96, 0.99))
    p2.insert_text(fitz.Point(65, 535), "CONTROL ANTI-BLOAT Y LECCIONES DE FRICCION REAL (INV-HELIX-8):", fontsize=9.5, fontname="helv", color=(0.08, 0.45, 0.75))
    p2.insert_text(fitz.Point(65, 555), "• Tope estricto de <= 85 lineas por ficha canonica en specs/squad/*.md.", fontsize=8.5, fontname="helv", color=(0.18, 0.23, 0.28))
    p2.insert_text(fitz.Point(65, 575), "• Maximo 6 reglas en Seccion 6 procedentes de correcciones de usuario [USER-FIX] o entorno [ENV-FIX].", fontsize=8.5, fontname="helv", color=(0.18, 0.23, 0.28))
    p2.insert_text(fitz.Point(65, 595), "• Prohibido inyectar teoria general de IA; los radares tecnologicos se cargan bajo demanda (Lazy Loading).", fontsize=8.5, fontname="helv", color=(0.18, 0.23, 0.28))

    # --------------------------------------------------------------------------
    # PÁGINA 3: EL BUCLE SDD EN 5 PASOS, SPECQUALITYSCORE Y CLI HELIX
    # --------------------------------------------------------------------------
    p3 = doc.new_page(width=595, height=842)
    draw_pdf_header_footer(p3, 3)

    p3.insert_text(fitz.Point(50, 75), "3. El Bucle SDD en 5 Pasos y Motor SpecQualityScore", fontsize=18, fontname="helv", color=(0.06, 0.1, 0.16))
    p3.insert_text(
        fitz.Point(50, 95),
        "Ciclo atomico determinista: cada intervencion cuenta con checkpoint, spec y verification gate.",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.35, 0.42),
    )

    steps = [
        ("1. SYNC & TRIAGE", "01-orchestrator lee ROADMAP.md, evalua la rubrica y emite la Tarjeta de Triaje de 6 lineas."),
        ("2. SPEC & DESIGN", "02-product y 03-architect definen contratos, non-goals e invariantes antes de tocar codigo."),
        ("3. CHECKPOINT", "12-release fija el tag git sdd-checkpoint-pre-<id> garantizando capacidad de retorno."),
        ("4. BUILD", "Los roles constructores convocados (04 a 09) implementan la funcionalidad especificada."),
        ("5. ASSURANCE GATE", "10-security y 11-qa ejecutan comandos deterministas. Si hay 2 fallos: ROLLBACK inmediato."),
    ]
    y_step = 120
    for s_title, s_desc in steps:
        p3.draw_rect(fitz.Rect(50, y_step, 545, y_step + 38), color=(0.95, 0.96, 0.98), fill=(0.95, 0.96, 0.98))
        p3.draw_rect(fitz.Rect(50, y_step, 54, y_step + 38), color=(0.08, 0.65, 0.95), fill=(0.08, 0.65, 0.95))
        p3.insert_text(fitz.Point(65, y_step + 15), s_title, fontsize=9.5, fontname="helv", color=(0.06, 0.1, 0.16))
        p3.insert_text(fitz.Point(65, y_step + 29), s_desc, fontsize=8, fontname="helv", color=(0.28, 0.33, 0.39))
        y_step += 44

    p3.insert_text(fitz.Point(50, 370), "4. Puntuacion Formal SpecQualityScore (0..100) en 5 Pilares", fontsize=13, fontname="helv", color=(0.06, 0.1, 0.16))
    pilares = [
        ("Pilar 1: Problema y Contexto (+20 pts):", "Definicion clara del problema de negocio y perfil del usuario objetivo."),
        ("Pilar 2: Non-Goals Explicitos (+20 pts):", "Limites y prohibiciones tecnicas estrictas para neutralizar la deuda de vibe coding."),
        ("Pilar 3: Contratos Tipados (+20 pts):", "Esquemas JSON / Pydantic o tablas de base de datos declaradas formalmente."),
        ("Pilar 4: Invariantes INV-* (+20 pts):", "Al menos 3 invariantes de dominio formalmente etiquetadas."),
        ("Pilar 5: Verification Gate (+20 pts):", "Comando ejecutable determinista (pytest, npm test, oxlint) con salida 0."),
    ]
    y_pil = 395
    for p_title, p_desc in pilares:
        p3.insert_text(fitz.Point(65, y_pil), p_title, fontsize=9, fontname="helv", color=(0.08, 0.65, 0.95))
        p3.insert_text(fitz.Point(235, y_pil), p_desc, fontsize=8, fontname="helv", color=(0.28, 0.33, 0.39))
        y_pil += 18

    # Bloque CLI
    p3.draw_rect(fitz.Rect(50, 505, 545, 655), color=(0.067, 0.094, 0.153), fill=(0.067, 0.094, 0.153))
    p3.insert_text(fitz.Point(65, 528), "CLI HELIX MULTIPLATAFORMA (0 DEPENDENCIAS EXTERNAS · INV-HELIX-5):", fontsize=9.5, fontname="helv", color=(0.976, 0.98, 0.984))
    cli_commands = [
        "python helix.py status                                    # Estado de salud y auditoria de specs",
        "python helix.py triage --milestone 1.2 --files 3 --surfaces ui,frontend  # Tarjeta de 6 lineas",
        "python helix.py new-spec mi-app --with-design             # Andamiaje formal con SpecScore >= 80",
        "python helix.py checkpoint 1.2                            # Creacion de tag git sdd-checkpoint-*",
        "python helix.py verify --spec specs/apps/mi-app/spec.md   # Puntuacion de calidad y gates",
        "python helix.py rollback 1.2 --confirm                    # Marcha atras inmediata y registro en log",
    ]
    y_cli = 548
    for cmd in cli_commands:
        p3.insert_text(fitz.Point(65, y_cli), cmd, fontsize=7.5, fontname="courier", color=(0.22, 0.74, 0.97))
        y_cli += 17

    # --------------------------------------------------------------------------
    # PÁGINA 4: BLUEPRINTS DE PROYECTO Y CASOS DE ESTUDIO REALES
    # --------------------------------------------------------------------------
    p4 = doc.new_page(width=595, height=842)
    draw_pdf_header_footer(p4, 4)

    p4.insert_text(fitz.Point(50, 75), "4. Blueprints de Proyecto y Casos de Estudio Auditados", fontsize=18, fontname="helv", color=(0.06, 0.1, 0.16))
    p4.insert_text(
        fitz.Point(50, 95),
        "Patrones arquitectonicos probados listos para clonar y evidencia empirica de veto en accion.",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.35, 0.42),
    )

    blueprints = [
        ("Blueprint 01: Calculadora Estatica", "Aplicaciones web cliente autonomas, cero backend, sliders reactivos < 16ms y empaquetado optimizado."),
        ("Blueprint 02: React + Supabase RLS", "SaaS B2B con politicas PostgreSQL Row-Level Security estrictas y aislamiento multi-tenant por usuario."),
        ("Blueprint 03: Motor Cuantitativo Python", "Modelos analiticos financieros con Pydantic v2, precision estricta y suite determinista pytest."),
    ]
    y_bp = 125
    for b_title, b_desc in blueprints:
        p4.draw_rect(fitz.Rect(50, y_bp, 545, y_bp + 38), color=(0.95, 0.96, 0.98), fill=(0.95, 0.96, 0.98))
        p4.draw_rect(fitz.Rect(50, y_bp, 54, y_bp + 38), color=(0.08, 0.65, 0.95), fill=(0.08, 0.65, 0.95))
        p4.insert_text(fitz.Point(65, y_bp + 15), b_title, fontsize=9.5, fontname="helv", color=(0.06, 0.1, 0.16))
        p4.insert_text(fitz.Point(65, y_bp + 29), b_desc, fontsize=8, fontname="helv", color=(0.28, 0.33, 0.39))
        y_bp += 44

    # Casos de Estudio
    p4.insert_text(fitz.Point(50, 280), "Casos de Estudio Reales Auditados:", fontsize=13, fontname="helv", color=(0.06, 0.1, 0.16))

    p4.draw_rect(fitz.Rect(50, 305, 545, 385), color=(0.98, 0.98, 0.99), fill=(0.98, 0.98, 0.99))
    p4.insert_text(fitz.Point(65, 325), "Caso #1: Datalaria Pulse ('Operacion Crisol')", fontsize=10.5, fontname="helv", color=(0.08, 0.65, 0.95))
    p4.insert_text(fitz.Point(65, 342), "- Auditoria completa del producto comercial Datalaria Pulse ejecutada por los 12 agentes de Helix.", fontsize=8, fontname="helv", color=(0.28, 0.33, 0.39))
    p4.insert_text(fitz.Point(65, 357), "- Aislamiento estricto de metricas privadas (INV-PULSE-1..5), generador de guias PDF y suite pytest 30/30 verde.", fontsize=8, fontname="helv", color=(0.28, 0.33, 0.39))
    p4.insert_text(fitz.Point(65, 372), "- Verificacion de embargo comercial para el 18 de noviembre de 2026 sin comprometer seguridad.", fontsize=8, fontname="helv", color=(0.063, 0.725, 0.506))

    p4.draw_rect(fitz.Rect(50, 400, 545, 480), color=(0.98, 0.98, 0.99), fill=(0.98, 0.98, 0.99))
    p4.insert_text(fitz.Point(65, 420), "Caso #2: MarginGuard B2B (Profesional No-Dev + Veto Real de QA)", fontsize=10.5, fontname="helv", color=(0.08, 0.65, 0.95))
    p4.insert_text(fitz.Point(65, 437), "- Creacion de un simulador de breakeven ante descuentos comerciales: delta_V = d / (m - d).", fontsize=8, fontname="helv", color=(0.28, 0.33, 0.39))
    p4.insert_text(fitz.Point(65, 452), "- Veto de 11-qa-verifier (QA_REJECT): division por cero y volumen negativo ante d >= m interceptados.", fontsize=8, fontname="helv", color=(0.937, 0.267, 0.267))
    p4.insert_text(fitz.Point(65, 467), "- Resolucion con invariante INV-MARGIN-2 (value_destruction_zone: true) y release con SpecScore 100/100.", fontsize=8, fontname="helv", color=(0.063, 0.725, 0.506))

    # Contacto y enlaces
    p4.draw_rect(fitz.Rect(50, 505, 545, 620), color=(0.043, 0.059, 0.09), fill=(0.043, 0.059, 0.09))
    p4.insert_text(fitz.Point(65, 530), "SOPORTE, COMUNIDAD Y LICENCIA COMERCIAL:", fontsize=10, fontname="helv", color=(0.976, 0.98, 0.984))
    p4.insert_text(fitz.Point(65, 552), "• Web Oficial del Ecosistema: https://datalaria.com", fontsize=8.5, fontname="helv", color=(0.898, 0.91, 0.922))
    p4.insert_text(fitz.Point(65, 570), "• Sandbox Web Interactivo (Spec Builder): https://datalaria.com/apps/helix/", fontsize=8.5, fontname="helv", color=(0.22, 0.74, 0.97))
    p4.insert_text(fitz.Point(65, 588), "• Catalogo B2B y Recursos: https://datalaria.com/es/recursos/#software", fontsize=8.5, fontname="helv", color=(0.898, 0.91, 0.922))
    p4.insert_text(fitz.Point(65, 606), "• Email de Ingenieria y Soporte: contacto@datalaria.com / dalaez1@gmail.com", fontsize=8.5, fontname="helv", color=(0.22, 0.74, 0.97))

    doc.save(str(output_path))
    doc.close()
    kb_size = round(output_path.stat().st_size / 1024, 1)
    print(f"[HELIX PDF GUIDE] Generada exitosamente en {output_path} ({kb_size} KB)")
    return output_path


# ==============================================================================
# 2. GENERADOR DEL STARTER KIT (9 € · 3 Carpetas Numeradas)
# ==============================================================================

def _render_starter_readme() -> str:
    return """# Datalaria Helix Starter Kit — Commercial Release v1.0.0 (9 €)

> **The Essential Foundation for Spec-Driven AI Development.**

This starter kit provides the core principles of Spec-Driven Development (SDD),
the executive PDF playbook, fundamental templates, and the two primary leadership
agents to eliminate context rot and hallucinated architectures.

## Package Structure:
- `01_Executive_Playbook/`: Complete executive PDF handbook (A4), Quickstart guides in English and Spanish, and the No-CLI parity guide.
- `02_Starter_Templates/`: Universal constitution v1.1.0, AGENTS.md, CLAUDE.md, ROADMAP.md, DECISIONS.md, and production templates for specs and designs.
- `03_Essential_2_Agents/`: Canonical specs and ready-to-use adapters for `01-orchestrator` (deterministic triage) and `02-product-analyst` (interview to spec).

## License:
Commercial Single User License — Datalaria (c) 2026. See `LICENSE.txt`.
To unlock the full 12-agent squad, 3 project blueprints, CLI `helix.py`, and real-world case studies, upgrade to **Datalaria Helix Core Kit**.
"""


def _render_starter_license() -> str:
    return """DATALARIA HELIX STARTER KIT — COMMERCIAL SINGLE USER LICENSE
Copyright (c) 2026 Datalaria. All rights reserved.

Permission is hereby granted to the licensee to use this software and associated
documentation files for commercial and personal software engineering projects.

Redistribution, sublicensing, or resale of the core framework materials,
templates, or agent specs as a standalone commercial template is strictly prohibited.
"""


def build_starter_kit(output_zip: Path = STARTER_ZIP_PATH) -> Path:
    """Construye y empaqueta el Starter Kit comercial en 3 carpetas numeradas."""
    print("[STARTER KIT] Construyendo estructura comercial en 3 carpetas...")
    staging_dir = PACKAGES_HELIX_DIR / "starter_kit_staging"
    if staging_dir.exists():
        shutil.rmtree(staging_dir, ignore_errors=True)
    staging_dir.mkdir(parents=True, exist_ok=True)

    # 1. 01_Executive_Playbook/
    dir_01 = staging_dir / "01_Executive_Playbook"
    dir_01.mkdir(parents=True, exist_ok=True)
    if not PDF_GUIDE_PATH.exists():
        build_helix_pdf_guide()
    shutil.copy2(PDF_GUIDE_PATH, dir_01 / "GUIA_EJECUTIVA_HELIX_SDD.pdf")

    core_kit_dir = PACKAGES_HELIX_DIR / "core_kit"
    docs_src = core_kit_dir / "05_Case_Studies_and_Docs"
    for doc_name in ["QUICKSTART_HELIX_CORE_ES.md", "QUICKSTART_HELIX_CORE_EN.md", "NO_CLI_PARITY_GUIDE.md"]:
        src_f = docs_src / doc_name
        dest_name = doc_name.replace("_CORE", "")
        if src_f.exists():
            shutil.copy2(src_f, dir_01 / dest_name)

    # 2. 02_Starter_Templates/
    dir_02 = staging_dir / "02_Starter_Templates"
    dir_02.mkdir(parents=True, exist_ok=True)
    templates_01_src = core_kit_dir / "01_Constitution_and_Memory"
    if templates_01_src.exists():
        for tf in ["AGENTS.md", "CLAUDE.md"]:
            if (templates_01_src / tf).exists():
                shutil.copy2(templates_01_src / tf, dir_02 / tf)
        if (templates_01_src / "specs").exists():
            shutil.copytree(templates_01_src / "specs", dir_02 / "specs", dirs_exist_ok=True)

    templates_02_src = core_kit_dir / "02_Templates"
    if templates_02_src.exists():
        shutil.copytree(templates_02_src, dir_02 / "specs" / "_templates", dirs_exist_ok=True)

    # 3. 03_Essential_2_Agents/
    dir_03 = staging_dir / "03_Essential_2_Agents"
    dir_03.mkdir(parents=True, exist_ok=True)
    squad_specs_target = dir_03 / "specs" / "squad"
    squad_specs_target.mkdir(parents=True, exist_ok=True)

    squad_src = ROOT_DIR / "specs" / "squad"
    for sf in ["README.md", "triage-rubric.md", "01-orchestrator.md", "02-product-analyst.md"]:
        if (squad_src / sf).exists():
            shutil.copy2(squad_src / sf, squad_specs_target / sf)

    # Adaptadores solo para 01 y 02
    for tool_dir in [".agents", ".claude"]:
        src_d = ROOT_DIR / tool_dir / "agents" if tool_dir == ".claude" else ROOT_DIR / tool_dir / "squad"
        tgt_d = dir_03 / tool_dir / "agents" if tool_dir == ".claude" else dir_03 / tool_dir / "squad"
        tgt_d.mkdir(parents=True, exist_ok=True)
        for af in ["01-orchestrator.md", "02-product-analyst.md"]:
            if (src_d / af).exists():
                shutil.copy2(src_d / af, tgt_d / af)

    # Raíz
    (staging_dir / "README.md").write_text(_render_starter_readme(), encoding="utf-8")
    (staging_dir / "LICENSE.txt").write_text(_render_starter_license(), encoding="utf-8")

    # Empaquetar ZIP
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in staging_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(staging_dir)
                zf.write(file_path, arcname)

    # Verificar integridad del ZIP
    with zipfile.ZipFile(output_zip, "r") as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"Error de integridad en Starter ZIP: {bad}")

    # Sincronizar en 00_DISTRIBUCION_LEMONSQUEEZY/
    LEMON_DIST_DIR.mkdir(parents=True, exist_ok=True)
    lemon_starter = LEMON_DIST_DIR / output_zip.name
    shutil.copy2(output_zip, lemon_starter)

    # Limpiar staging
    shutil.rmtree(staging_dir, ignore_errors=True)

    size_kb = round(output_zip.stat().st_size / 1024, 1)
    sha = compute_sha256(output_zip)
    print(f"[STARTER KIT] Generado: {output_zip} ({size_kb} KB, SHA-256: {sha[:12]}...)")
    return output_zip


# ==============================================================================
# 3. GENERADOR DEL CORE KIT (19 € / 39 € · 5 Carpetas + CLI + 2 Casos)
# ==============================================================================

def build_full_core_kit() -> Tuple[Path, Path]:
    """Genera la estructura de Core Kit, inyecta la Guía PDF y empaqueta ambos ZIPs."""
    print("[CORE KIT] Compilando Core Kit completo...")
    if not PDF_GUIDE_PATH.exists():
        build_helix_pdf_guide()

    # 1. Compilar directorio core_kit
    core_dir = build_core_kit(source_root=ROOT_DIR)

    # 2. Inyectar GUIA_EJECUTIVA_HELIX_SDD.pdf en 05_Case_Studies_and_Docs/
    dest_pdf = core_dir / "05_Case_Studies_and_Docs" / "GUIA_EJECUTIVA_HELIX_SDD.pdf"
    shutil.copy2(PDF_GUIDE_PATH, dest_pdf)

    # 3. Empaquetar kit-datalaria-helix-core-v1.0.0.zip y Datalaria_Helix_Core_Kit.zip
    for zpath in [CORE_VERSIONED_ZIP_PATH, CORE_ZIP_PATH]:
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in core_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(core_dir)
                    zf.write(file_path, arcname)

        with zipfile.ZipFile(zpath, "r") as zf:
            bad = zf.testzip()
            if bad:
                raise RuntimeError(f"Error de integridad en Core ZIP {zpath.name}: {bad}")

        # Copiar a Lemon Squeezy
        LEMON_DIST_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(zpath, LEMON_DIST_DIR / zpath.name)

        size_kb = round(zpath.stat().st_size / 1024, 1)
        sha = compute_sha256(zpath)
        print(f"[CORE KIT] Generado: {zpath} ({size_kb} KB, SHA-256: {sha[:12]}...)")

    return CORE_VERSIONED_ZIP_PATH, CORE_ZIP_PATH


# ==============================================================================
# 4. GENERADOR DE ACTIVOS VISUALES (Previews 1600x980 y Cores 1200x750)
# ==============================================================================

def _get_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    """Carga fuente con fallbacks seguros en Windows y Linux."""
    font_names = [
        "seguisb.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
    ]
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _render_pdf_page_to_image(pdf_path: Path, page_num: int, target_height: int) -> Image.Image:
    """Renderiza una página de PDF a imagen PIL con antialiasing y nitidez."""
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    zoom = (target_height / page.rect.height) * 1.5
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    aspect = img.width / img.height
    target_width = int(target_height * aspect)
    res = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    doc.close()
    return res


def _add_drop_shadow(base_img: Image.Image, element: Image.Image, x: int, y: int, shadow_offset: int = 14, border_color=(56, 189, 248)):
    """Pega un elemento con sombra paralela suave y borde decorativo."""
    shadow_box = Image.new("RGBA", (element.width + shadow_offset * 2, element.height + shadow_offset * 2), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_box)
    sdraw.rectangle(
        [shadow_offset, shadow_offset, shadow_box.width - 2, shadow_box.height - 2],
        fill=(0, 0, 0, 160)
    )
    base_img.paste(shadow_box, (x - shadow_offset // 2, y - shadow_offset // 2), mask=shadow_box)

    elem_border = element.copy().convert("RGBA")
    edraw = ImageDraw.Draw(elem_border)
    edraw.rectangle([0, 0, elem_border.width - 1, elem_border.height - 1], outline=border_color, width=2)
    base_img.paste(elem_border, (x, y))


def build_helix_preview(lang: str = "es") -> Path:
    """Genera la imagen preview de alta resolución (1600x980 px) para catálogo y modales."""
    out_dir = ROOT_DIR / "static" / "images" / "recursos"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"helix-preview-{lang}.png"

    width, height = 1600, 980
    img = Image.new("RGB", (width, height), color="#0b0f17")
    draw = ImageDraw.Draw(img)

    # Rejilla ejecutiva y degradado suave
    for y in range(0, height, 70):
        draw.line([(0, y), (width, y)], fill=(17, 24, 39), width=1)
    for x in range(0, width, 100):
        draw.line([(x, 0), (x, height)], fill=(17, 24, 39), width=1)

    draw.rectangle([16, 16, width - 17, height - 17], outline=(30, 41, 59), width=2)
    draw.rectangle([20, 20, width - 21, height - 21], outline=(56, 189, 248), width=1)

    f_badge = _get_font(18, bold=True)
    f_title = _get_font(44, bold=True)
    f_sub = _get_font(22, bold=False)
    f_item_title = _get_font(21, bold=True)
    f_item_desc = _get_font(15, bold=False)
    f_kpi_num = _get_font(30, bold=True)
    f_kpi_lbl = _get_font(13, bold=False)
    f_price_badge = _get_font(24, bold=True)

    if lang == "es":
        badge_text = "SISTEMA SDD B2B · ESCUADRON 12 AGENTES · 19€ EARLY-BIRD"
        title_text = "Datalaria Helix SDD Kit"
        sub_text = "Gobernanza Agéntica, Triaje Determinista, 3 Blueprints y Rollback en 1 Clic"
        features = [
            ("01. Escuadrón de 12 Agentes IA", "4 células especializadas con veto vinculante en Seguridad y QA (INV-HELIX-1)"),
            ("02. Adaptadores Multi-Herramienta", "Soporte agnóstico para Antigravity (.agents/), Claude (.claude/) y Cursor (.cursor/)"),
            ("03. 3 Blueprints de Arquitectura", "Calculadora Estática JS, SaaS React+Supabase RLS y Motor Cuantitativo Python"),
            ("04. CLI helix.py (0 dependencias)", "Subcomandos init, triage, new-spec, checkpoint, verify y rollback en Python estándar"),
        ]
        kpi_items = [
            ("19€", "Lanzamiento Early-Bird"),
            ("12 Roles", "Escuadrón Coordinado"),
            ("-87%", "Gasto de Tokens vs Vibe"),
            ("100/100", "SpecQualityScore Auditado"),
        ]
        footer_left = "datalaria.com/es/recursos/#software · Compatible con Antigravity, Claude, Cursor & Codex"
        footer_right = "Lanzamiento Oficial Enero 2027 · Reserva Early-Bird"
    else:
        badge_text = "B2B SDD SYSTEM · 12-AGENT AI SQUAD · 19€ EARLY-BIRD"
        title_text = "Datalaria Helix SDD Kit"
        sub_text = "Agentic Governance, Deterministic Triage, 3 Blueprints & 1-Click Rollback"
        features = [
            ("01. 12-Agent AI Engineering Squad", "4 specialized cells with binding veto in Security and QA (INV-HELIX-1)"),
            ("02. Multi-Tool Precompiled Adapters", "Agnostic support for Antigravity (.agents/), Claude (.claude/) & Cursor (.cursor/)"),
            ("03. 3 Production Project Blueprints", "Client-Side Static Calculator, React+Supabase SaaS, and Python Quant Engine"),
            ("04. Zero-Dependency CLI helix.py", "Pure Python CLI for init, triage, new-spec, checkpoint, verify, and rollback"),
        ]
        kpi_items = [
            ("19€", "Early-Bird Launch Price"),
            ("12 Roles", "Coordinated Squad"),
            ("-87%", "Token Spend vs Vibe"),
            ("100/100", "Audited SpecQualityScore"),
        ]
        footer_left = "datalaria.com/en/resources/#software · Compatible with Antigravity, Claude, Cursor & Codex"
        footer_right = "Official Launch January 2027 · Reserve Early-Bird"

    # Header / Badge
    draw.rounded_rectangle([70, 60, 720, 96], radius=8, fill=(14, 165, 233, 30), outline=(56, 189, 248), width=1)
    draw.text((88, 68), badge_text, fill=(56, 189, 248), font=f_badge)

    draw.text((70, 118), title_text, fill=(249, 250, 251), font=f_title)
    draw.text((70, 178), sub_text, fill=(156, 163, 175), font=f_sub)

    # 4 Features
    y_start = 245
    for i, (feat_title, feat_desc) in enumerate(features):
        box_y = y_start + i * 92
        draw.rounded_rectangle([70, box_y, 790, box_y + 78], radius=8, fill=(17, 24, 39), outline=(51, 65, 85), width=1)
        draw.rounded_rectangle([86, box_y + 14, 114, box_y + 42], radius=6, fill=(14, 165, 233), outline=(2, 132, 199))
        draw.text((94, box_y + 18), "✓", fill=(255, 255, 255), font=f_badge)
        draw.text((130, box_y + 14), feat_title, fill=(249, 250, 251), font=f_item_title)
        draw.text((130, box_y + 44), feat_desc, fill=(156, 163, 175), font=f_item_desc)

    # 4 KPIs
    kpi_y = 645
    for k_idx, (num, lbl) in enumerate(kpi_items):
        kx = 70 + k_idx * 185
        draw.rounded_rectangle([kx, kpi_y, kx + 172, kpi_y + 86], radius=8, fill=(15, 23, 42), outline=(56, 189, 248), width=1)
        draw.text((kx + 14, kpi_y + 12), num, fill=(56, 189, 248), font=f_kpi_num)
        draw.text((kx + 14, kpi_y + 52), lbl, fill=(148, 163, 184), font=f_kpi_lbl)

    # Price Badge
    draw.rounded_rectangle([70, 755, 450, 815], radius=10, fill=(14, 165, 233), outline=(2, 132, 199), width=2)
    draw.text((88, 772), "⚡ 19€  ·  EARLY-BIRD (PVP: 39€)", fill=(11, 15, 23), font=f_price_badge)

    # Render PDF Pages
    if PDF_GUIDE_PATH.exists():
        try:
            p1_img = _render_pdf_page_to_image(PDF_GUIDE_PATH, 0, target_height=650)
            p2_img = _render_pdf_page_to_image(PDF_GUIDE_PATH, 1, target_height=560)

            _add_drop_shadow(img, p2_img, x=1090, y=140, shadow_offset=18, border_color=(147, 51, 234))
            _add_drop_shadow(img, p1_img, x=840, y=110, shadow_offset=22, border_color=(56, 189, 248))

            draw.rounded_rectangle([1080, 780, 1520, 825], radius=8, fill=(17, 24, 39), outline=(56, 189, 248), width=1)
            draw.text((1100, 792), "📄 GUIA_EJECUTIVA_HELIX_SDD.pdf (4 Pag. A4)", fill=(249, 250, 251), font=f_badge)
        except Exception as e:
            print(f"[WARN] Error renderizando PDF en preview: {e}")

    # Footer
    f_footer = _get_font(15, bold=False)
    draw.line([(70, 890), (width - 70, 890)], fill=(51, 65, 85), width=1)
    draw.text((70, 915), footer_left, fill=(148, 163, 184), font=f_footer)
    draw.text((width - 440, 915), footer_right, fill=(56, 189, 248), font=f_footer)

    img.save(out_path, format="PNG", optimize=True)
    kb = round(out_path.stat().st_size / 1024, 1)
    print(f"[PREVIEW] Generada imagen {out_path.name} ({width}x{height} px, {kb} KB)")
    return out_path


def build_helix_app_cover(lang: str = "es") -> Path:
    """Genera la portada 16:10 (1200x750 px) para content/{es,en}/apps/helix/cover.png."""
    out_path = ROOT_DIR / "content" / lang / "apps" / "helix" / "cover.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    width, height = 1200, 750
    img = Image.new("RGB", (width, height), color="#0b0f17")
    draw = ImageDraw.Draw(img)

    for y in range(0, height, 50):
        draw.line([(0, y), (width, y)], fill=(17, 24, 39), width=1)
    for x in range(0, width, 80):
        draw.line([(x, 0), (x, height)], fill=(17, 24, 39), width=1)

    draw.rectangle([12, 12, width - 13, height - 13], outline=(30, 41, 59), width=2)
    draw.rectangle([16, 16, width - 17, height - 17], outline=(56, 189, 248), width=1)

    f_badge = _get_font(16, bold=True)
    f_title = _get_font(42, bold=True)
    f_sub = _get_font(20, bold=False)
    f_card_title = _get_font(18, bold=True)
    f_card_desc = _get_font(14, bold=False)

    badge_text = "DATALARIA HELIX · SPEC-DRIVEN DEVELOPMENT OS" if lang == "en" else "DATALARIA HELIX · SISTEMA OPERATIVO SDD"
    title_text = "Helix 12-Agent Engineering Squad" if lang == "en" else "Escuadrón de 12 Agentes Helix"
    sub_text = "The spec is your app's DNA; AI agents merely express it" if lang == "en" else "La spec es el ADN de tu app; los agentes solo la expresan"

    draw.rounded_rectangle([60, 50, 580, 85], radius=6, fill=(14, 165, 233, 30), outline=(56, 189, 248), width=1)
    draw.text((76, 58), badge_text, fill=(56, 189, 248), font=f_badge)
    draw.text((60, 105), title_text, fill=(249, 250, 251), font=f_title)
    draw.text((60, 160), sub_text, fill=(156, 163, 175), font=f_sub)

    # 4 Células Cards en cuadrícula 2x2
    cells_data = [
        ("🎯 CÉLULA 1: DIRECCIÓN", "Orquestador (Triaje XS-XL), Product Analyst y Arquitecto.", 60, 220),
        ("⚡ CÉLULA 2: CONSTRUCCIÓN", "UX/UI, Frontend, Backend, APIs, Media e i18n, Monetización.", 620, 220),
        ("🛡️ CÉLULA 3: GARANTÍA (VETO)", "Seguridad y QA Verifier con veto vinculante innegociable.", 60, 360),
        ("🚀 CÉLULA 4: ENTREGA", "Release DevOps, Checkpoints, SemVer y Rollback en 1 clic.", 620, 360),
    ]
    for c_title, c_desc, cx, cy in cells_data:
        draw.rounded_rectangle([cx, cy, cx + 520, cy + 115], radius=8, fill=(17, 24, 39), outline=(51, 65, 85), width=1)
        draw.text((cx + 20, cy + 18), c_title, fill=(56, 189, 248), font=f_card_title)
        draw.text((cx + 20, cy + 54), c_desc, fill=(203, 213, 225), font=f_card_desc)

    # Franja inferior con métricas clave
    draw.rounded_rectangle([60, 510, 1140, 680], radius=10, fill=(15, 23, 42), outline=(56, 189, 248), width=1)
    kpis = [
        ("SpecQualityScore", "100 / 100", "Auditoría formal 5 pilares"),
        ("Ahorro de Contexto", "~87%", "Carga bajo demanda INV-HELIX-2"),
        ("CLI sin dependencias", "helix.py", "Python estándar >= 3.10"),
        ("Disponibilidad", "Dual-Mode", "Sandbox Gratis + Kits Lemon Squeezy"),
    ]
    for k_idx, (k_top, k_main, k_sub) in enumerate(kpis):
        kx = 85 + k_idx * 265
        draw.text((kx, 530), k_top, fill=(148, 163, 184), font=_get_font(13, bold=False))
        draw.text((kx, 555), k_main, fill=(56, 189, 248), font=_get_font(26, bold=True))
        draw.text((kx, 600), k_sub, fill=(203, 213, 225), font=_get_font(12, bold=False))

    img.save(out_path, format="PNG", optimize=True)
    kb = round(out_path.stat().st_size / 1024, 1)
    print(f"[COVER] Generada portada {out_path} ({width}x{height} px, {kb} KB)")
    return out_path


def build_helix_visual_assets() -> None:
    """Compila las previsualizaciones de catálogo y portadas de fichas de Helix."""
    print("[VISUAL ASSETS] Generando previews 1600x980 px y portadas 1200x750 px...")
    build_helix_preview("es")
    build_helix_preview("en")
    build_helix_app_cover("es")
    build_helix_app_cover("en")


# ==============================================================================
# 5. ENTRY POINT PRINCIPAL
# ==============================================================================

def main() -> int:
    try:
        print("=" * 80)
        print("          CONSTRUCTOR COMERCIAL DE DATALARIA HELIX (HITO 6.8)")
        print("=" * 80)

        # 1. Guía PDF
        pdf_path = build_helix_pdf_guide()

        # 2. Starter Kit
        starter_zip = build_starter_kit()

        # 3. Core Kit
        versioned_zip, core_zip = build_full_core_kit()

        # 4. Activos Visuales
        build_helix_visual_assets()

        print("\n" + "=" * 80)
        print("[OK] EMPAQUETADO COMERCIAL HELIX COMPLETADO CON ÉXITO")
        print(f"  - Guía PDF:     {pdf_path.resolve()}")
        print(f"  - Starter Kit:  {starter_zip.resolve()}")
        print(f"  - Core Kit:     {core_zip.resolve()}")
        print(f"  - Core Version: {versioned_zip.resolve()}")
        print(f"  - Distribución: {LEMON_DIST_DIR.resolve()}")
        print("=" * 80)
        return 0
    except Exception as exc:
        print(f"\n[ERROR BUILD KIT] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
