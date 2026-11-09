"""
Script: update_post_images.py
Sustituye los diagramas ASCII y Mermaid por imágenes PNG de alta resolución y añade la vista previa del paquete.
"""

import os

def update_es_post():
    path = "content/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/index.md"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    target_es = "{{< bundle-card"
    preview_block_es = """![Vista previa del Mega Bundle Suite 02: Toma de Decisiones & Priorización](preview-pack.png "Vista previa de los modelos analíticos, decks PPTX 16:9 y guías PDF de la Suite 02")
*Figura 4: Arsenal visual y matricial incluido en el Mega Bundle Suite 02: 6 modelos Excel/Sheets, 6 presentaciones ejecutivas PPTX 16:9 y 3 guías PDF.*

{{< bundle-card"""

    if "preview-pack.png" not in text and target_es in text:
        text = text.replace(target_es, preview_block_es, 1)
        print("[ES] Added preview-pack.png to Section 6")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    else:
        print("[ES] Section 6 already has preview-pack or target not found.")


def update_en_post():
    path = "content/en/posts/decision-making-prioritization-quantitative-framework/index.md"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    target_en = "{{< bundle-card"
    preview_block_en = """![Suite 02 Mega Bundle Preview: Quantitative Decision-Making & Prioritization](preview-pack.png "Preview of the analytical models, 16:9 PPTX decks, and PDF guides of Suite 02")
*Figure 4: Visual and financial workspace included in the Suite 02 Mega Bundle: 6 Excel/Sheets models, 6 executive 16:9 PPTX decks, and 3 PDF guides.*

{{< bundle-card"""

    if "preview-pack.png" not in text and target_en in text:
        text = text.replace(target_en, preview_block_en, 1)
        print("[EN] Added preview-pack.png to Section 6")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    else:
        print("[EN] Section 6 already has preview-pack or target not found.")


if __name__ == "__main__":
    update_es_post()
    update_en_post()
