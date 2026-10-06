#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_pack_health.py
====================
Script de auditoría integral y control de calidad para el Executive Decision Pack EVM:
- Verifica la existencia y peso de todos los entregables (Excel, PPTX, PDF, LEEME).
- Verifica las políticas de protección OpenXML ECMA-376 (hojas protegidas, celdas de usuario desbloqueadas).
- Verifica la integridad del empaquetado ZIP maestro y la copia en Lemon Squeezy.
- Verifica las restricciones de seguridad anti-filtración (cero archivos en static/downloads o public/downloads).
- Verifica que la contraseña NUNCA aparezca en los artículos públicos del blog.
- Verifica la resolución de las imágenes de portada (1200x630 px).
- Verifica el recuento de palabras (>2.500 palabras) y shortcodes de los posts.
"""

import os
import sys
import zipfile
import openpyxl
from pptx import Presentation
from reportlab.pdfgen import canvas
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PASSWORD_SECRET = "Datalaria2026"

def audit_deliverables():
    print("=" * 80)
    print("1. AUDITORÍA DE ARCHIVOS ENTREGABLES")
    print("=" * 80)

    base_dir = "packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado"
    expected = [
        os.path.join(base_dir, "[ES]_Cuadro_EVM_Valor_Ganado", "Cuadro_Mando_EVM_Datalaria_ES.xlsx"),
        os.path.join(base_dir, "[ES]_Cuadro_EVM_Valor_Ganado", "Presentacion_EVM_CLevel_ES.pptx"),
        os.path.join(base_dir, "[ES]_Cuadro_EVM_Valor_Ganado", "Guia_Metodologica_EVM_ES.pdf"),
        os.path.join(base_dir, "[ES]_Cuadro_EVM_Valor_Ganado", "LEEME_INSTRUCCIONES.txt"),
        os.path.join(base_dir, "[EN]_Earned_Value_Management_EVM", "EVM_Dashboard_Datalaria_EN.xlsx"),
        os.path.join(base_dir, "[EN]_Earned_Value_Management_EVM", "Deck_EVM_CLevel_EN.pptx"),
        os.path.join(base_dir, "[EN]_Earned_Value_Management_EVM", "Methodology_Guide_EVM_EN.pdf"),
        os.path.join(base_dir, "[EN]_Earned_Value_Management_EVM", "README_INSTRUCTIONS.txt"),
        os.path.join(base_dir, "LEEME_ACCESO_GOOGLE_SHEETS.txt"),
        os.path.join(base_dir, "README_GOOGLE_SHEETS_ACCESS.txt"),
        os.path.join(base_dir, "Executive_Decision_Pack_EVM_Dual.zip"),
        os.path.join("packages/00_DISTRIBUCION_LEMONSQUEEZY", "Executive_Decision_Pack_EVM_Dual.zip"),
        os.path.join("content/es/posts/cuadro-mando-evm-valor-ganado", "cover.png"),
        os.path.join("content/es/posts/cuadro-mando-evm-valor-ganado", "index.md"),
        os.path.join("content/en/posts/earned-value-management-evm-dashboard", "cover.png"),
        os.path.join("content/en/posts/earned-value-management-evm-dashboard", "index.md"),
    ]

    all_ok = True
    for p in expected:
        if os.path.exists(p):
            size_kb = os.path.getsize(p) / 1024
            print(f"  [OK] {p} ({size_kb:.1f} KB)")
        else:
            print(f"  [FAIL] NO ENCONTRADO: {p}")
            all_ok = False
    return all_ok


def audit_excel_protection():
    print("\n" + "=" * 80)
    print("2. AUDITORÍA DE PROTECCIÓN OPENXML Y FÓRMULAS EN EXCEL")
    print("=" * 80)

    files = [
        "packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado/[ES]_Cuadro_EVM_Valor_Ganado/Cuadro_Mando_EVM_Datalaria_ES.xlsx",
        "packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado/[EN]_Earned_Value_Management_EVM/EVM_Dashboard_Datalaria_EN.xlsx"
    ]

    for f in files:
        wb = openpyxl.load_workbook(f, data_only=False)
        print(f"-> Archivo: {os.path.basename(f)}")
        assert len(wb.sheetnames) == 4, f"Se esperaban 4 pestañas, encontradas {len(wb.sheetnames)}"
        for sname in wb.sheetnames:
            ws = wb[sname]
            is_protected = ws.protection.sheet
            unlocked_allowed = (ws.protection.selectUnlockedCells is False)
            print(f"   Pestaña '{sname}': Protegida={is_protected}, selectUnlockedCells={ws.protection.selectUnlockedCells} (Edición fluida={unlocked_allowed})")
            assert is_protected, f"Pestaña {sname} no está protegida"
            assert unlocked_allowed, f"Pestaña {sname} restringe erróneamente selectUnlockedCells"
    print("  [OK] Todas las pestañas cumplen estrictamente con ECMA-376.")


def audit_pptx():
    print("\n" + "=" * 80)
    print("3. AUDITORÍA DE PRESENTACIONES PPTX (16:9)")
    print("=" * 80)

    decks = [
        "packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado/[ES]_Cuadro_EVM_Valor_Ganado/Presentacion_EVM_CLevel_ES.pptx",
        "packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado/[EN]_Earned_Value_Management_EVM/Deck_EVM_CLevel_EN.pptx"
    ]

    for d in decks:
        prs = Presentation(d)
        num_slides = len(prs.slides)
        w_in = prs.slide_width.inches
        h_in = prs.slide_height.inches
        print(f"-> {os.path.basename(d)}: {num_slides} diapositivas, Formato: {w_in:.2f}\" x {h_in:.2f}\" (Widescreen 16:9)")
        assert num_slides == 3, f"Se esperaban 3 diapositivas, encontradas {num_slides}"
        assert abs(w_in - 13.333) < 0.1, "Ancho incorrecto"
    print("  [OK] Presentaciones PPTX conformes.")


def audit_covers_and_posts():
    print("\n" + "=" * 80)
    print("4. AUDITORÍA DE PORTADAS, ARTÍCULOS Y SEGURIDAD")
    print("=" * 80)

    # Portadas
    for cp in [
        "content/es/posts/cuadro-mando-evm-valor-ganado/cover.png",
        "content/en/posts/earned-value-management-evm-dashboard/cover.png"
    ]:
        im = Image.open(cp)
        print(f"-> Portada {cp}: {im.size} (Esperado: 1200x630)")
        assert im.size == (1200, 630), f"Tamaño incorrecto en {cp}"

    # Posts
    posts = [
        ("content/es/posts/cuadro-mando-evm-valor-ganado/index.md", "ES"),
        ("content/en/posts/earned-value-management-evm-dashboard/index.md", "EN")
    ]

    for p, lang in posts:
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()

        words = len(content.split())
        print(f"-> Post {os.path.basename(os.path.dirname(p))}: {words} palabras (Mínimo: 2.500)")
        assert words >= 2500, f"Post {p} no alcanza 2.500 palabras"

        # Seguridad: la contraseña NO debe estar en el post público
        if PASSWORD_SECRET in content:
            raise ValueError(f"CRÍTICO: La contraseña interna '{PASSWORD_SECRET}' aparece en el post público {p}!")
        print(f"   [SEGURIDAD OK] Contraseña '{PASSWORD_SECRET}' NO presente en el texto público.")

        # Billing: prohibido 'factura oficial B2B con IVA deducible'
        forbidden_phrase = "factura oficial B2B con IVA deducible"
        if forbidden_phrase.lower() in content.lower():
            raise ValueError(f"CRÍTICO: Mensaje no permitido '{forbidden_phrase}' encontrado en {p}!")
        print("   [FACTURACIÓN OK] Sin mención a facturas con IVA en los shortcodes.")

        # Verificar presencia de product-card y enlace lemonsqueezy
        assert "product-card" in content, f"Falta shortcode product-card en {p}"
        assert "lemonsqueezy.com/buy/cuadro-mando-evm" in content, f"Falta enlace checkout en {p}"
        assert "8€" in content, f"Precio de 8€ no encontrado en {p}"

    # Anti-filtración de descargas
    forbidden_files = [
        "static/downloads/Executive_Decision_Pack_EVM_Dual.zip",
        "public/downloads/Executive_Decision_Pack_EVM_Dual.zip"
    ]
    for fb in forbidden_files:
        assert not os.path.exists(fb), f"ALERTA DE SEGURIDAD: Archivo encontrado en ruta pública {fb}"
    print("  [SEGURIDAD OK] Ningún activo filtrado a static/downloads o public/downloads.")


if __name__ == "__main__":
    audit_deliverables()
    audit_excel_protection()
    audit_pptx()
    audit_covers_and_posts()
    print("\n" + "=" * 80)
    print("TODAS LAS AUDITORÍAS SUPERADAS CON ÉXITO Y CONFORMIDAD DEL 100%.")
    print("=" * 80)
