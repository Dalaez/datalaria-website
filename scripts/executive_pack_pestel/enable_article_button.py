#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
enable_article_button.py
========================
Habilita con precisión quirúrgica el botón de "Artículo técnico" / "Technical Article"
para la Matriz PESTEL en:
1. layouts/partials/recursos_catalog.html
   - Tarjeta HTML español
   - JSON KITS_DATA español
   - Tarjeta HTML inglés
   - JSON KITS_DATA inglés
2. content/es/recursos/_index.md
3. content/en/resources/_index.md
"""

def replace_exact(content, old_str, new_str, label=""):
    # Intentar primero con CRLF y luego con LF
    old_crlf = old_str.replace("\r\n", "\n").replace("\n", "\r\n")
    new_crlf = new_str.replace("\r\n", "\n").replace("\n", "\r\n")
    old_lf = old_str.replace("\r\n", "\n")
    new_lf = new_str.replace("\r\n", "\n")

    if old_crlf in content:
        content = content.replace(old_crlf, new_crlf, 1)
        print(f"[OK] {label} (CRLF matched)")
        return content, True
    elif old_lf in content:
        content = content.replace(old_lf, new_lf, 1)
        print(f"[OK] {label} (LF matched)")
        return content, True
    else:
        print(f"[ERROR] {label} NOT FOUND")
        return content, False

def main():
    # 1. layouts/partials/recursos_catalog.html
    p_cat = "layouts/partials/recursos_catalog.html"
    with open(p_cat, "r", encoding="utf-8") as f:
        cat_content = f.read()

    # 1.1 Tarjeta estática ES
    old_es_card = """<button type="button" class="btn-kit-info" onclick="openModal('pack-pestel')">
Detalles ℹ️
</button>
<span class="btn-kit-info btn-disabled" title="Artículo técnico próximamente">Artículo próximamente</span>
<a href="https://datalaria.lemonsqueezy.com/checkout/buy/17a0781c-8001-47df-9cdd-25923041e1de?embed=1" class="btn-kit-buy lemonsqueezy-button">Descargar →</a>"""

    new_es_card = """<button type="button" class="btn-kit-info" onclick="openModal('pack-pestel')">
Detalles ℹ️
</button>
<a href="/es/posts/matriz-pestel-cuantitativa/" class="btn-kit-info" title="Leer artículo técnico">Artículo técnico 📖</a>
<a href="https://datalaria.lemonsqueezy.com/checkout/buy/17a0781c-8001-47df-9cdd-25923041e1de?embed=1" class="btn-kit-buy lemonsqueezy-button">Descargar →</a>"""

    cat_content, ok1 = replace_exact(cat_content, old_es_card, new_es_card, "ES Static Card")

    # 1.2 JSON KITS_DATA ES
    old_es_js = """"id": "pack-pestel",
    "title": "Matriz PESTEL con Severidad & Volatilidad",
    "topic": "estrategia",
    "topicLabel": "Estrategia MBA",
    "status": "available",
    "statusLabel": "🟢 DISPONIBLE • Riesgo Macro",
    "price": "5€",
    "origPrice": "19€",
    "icon": "🌐",
    "delivs": [
      "Excel .xlsx + Sheets",
      "PowerPoint 16:9",
      "Guía PDF"
    ],
    "desc": "Evaluación de 6 factores macro con índice de impacto compuesto y mapa térmico de riesgos regulatorios y macroeconómicos.",
    "features": [
      "Evaluación ponderada de factores Políticos, Económicos, Sociales, Tecnológicos, Ecológicos y Legales",
      "Mapa de calor automático con semáforo de alerta temprana",
      "Slide PPTX con matriz de incertidumbre para comités directivos",
      "Guía PDF de anticipación estratégica y escenarios"
    ],
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/17a0781c-8001-47df-9cdd-25923041e1de?embed=1",
    "guideUrl": null,
    "previewImg": "/images/recursos/PESTEL.png" """

    # Remove trailing space if any
    old_es_js = old_es_js.strip()
    new_es_js = old_es_js.replace('"guideUrl": null,', '"guideUrl": "/es/posts/matriz-pestel-cuantitativa/",')
    cat_content, ok2 = replace_exact(cat_content, old_es_js, new_es_js, "ES JS KITS_DATA")

    # 1.3 Tarjeta estática EN
    old_en_card = """<button type="button" class="btn-kit-info" onclick="openModal('pack-pestel')">
Details ℹ️
</button>
<span class="btn-kit-info btn-disabled" title="Technical article coming soon">Article coming soon</span>
<a href="https://datalaria.lemonsqueezy.com/checkout/buy/17a0781c-8001-47df-9cdd-25923041e1de?embed=1" class="btn-kit-buy lemonsqueezy-button">Download →</a>"""

    new_en_card = """<button type="button" class="btn-kit-info" onclick="openModal('pack-pestel')">
Details ℹ️
</button>
<a href="/en/posts/quantitative-pestel-matrix/" class="btn-kit-info" title="Read technical article">Technical Article 📖</a>
<a href="https://datalaria.lemonsqueezy.com/checkout/buy/17a0781c-8001-47df-9cdd-25923041e1de?embed=1" class="btn-kit-buy lemonsqueezy-button">Download →</a>"""

    cat_content, ok3 = replace_exact(cat_content, old_en_card, new_en_card, "EN Static Card")

    # 1.4 JSON KITS_DATA EN
    old_en_js = """"id": "pack-pestel",
    "title": "PESTEL Matrix: Severity & Volatility",
    "topic": "estrategia",
    "topicLabel": "MBA Strategy",
    "status": "available",
    "statusLabel": "🟢 AVAILABLE • Macro Risk",
    "price": "5€",
    "origPrice": "19€",
    "icon": "🌐",
    "delivs": [
      "Excel .xlsx + Sheets",
      "PowerPoint 16:9",
      "PDF Guide"
    ],
    "desc": "Evaluation of 6 macro factors with composite impact index and regulatory/macroeconomic heat map.",
    "features": [
      "Weighted evaluation of Political, Economic, Social, Tech, Environmental & Legal factors",
      "Automated heat map with early warning traffic light indicators",
      "PPTX slide with uncertainty matrix for steering committees",
      "PDF guide on strategic foresight and scenario planning"
    ],
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/17a0781c-8001-47df-9cdd-25923041e1de?embed=1",
    "guideUrl": null,
    "previewImg": "/images/recursos/PESTEL.png" """

    old_en_js = old_en_js.strip()
    new_en_js = old_en_js.replace('"guideUrl": null,', '"guideUrl": "/en/posts/quantitative-pestel-matrix/",')
    cat_content, ok4 = replace_exact(cat_content, old_en_js, new_en_js, "EN JS KITS_DATA")

    with open(p_cat, "w", encoding="utf-8") as f:
        f.write(cat_content)

    # 2. content/es/recursos/_index.md
    p_es = "content/es/recursos/_index.md"
    with open(p_es, "r", encoding="utf-8") as f:
        es_md = f.read()

    old_es_md = """          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="openModal('pack-pestel')">
              Detalles ℹ️
            </button>
            <span class="btn-kit-info btn-disabled" style="opacity: 0.55; cursor: default; border-style: dashed;" title="Guía metodológica próximamente en el blog">Guía ⏳</span>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/17a0781c-8001-47df-9cdd-25923041e1de" class="btn-kit-buy lemonsqueezy-button">Descargar →</a>
          </div>"""

    new_es_md = """          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="openModal('pack-pestel')">
              Detalles ℹ️
            </button>
            <a href="/es/posts/matriz-pestel-cuantitativa/" class="btn-kit-info" title="Leer artículo técnico">Artículo técnico 📖</a>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/17a0781c-8001-47df-9cdd-25923041e1de" class="btn-kit-buy lemonsqueezy-button">Descargar →</a>
          </div>"""

    es_md, ok5 = replace_exact(es_md, old_es_md, new_es_md, "ES _index.md")
    with open(p_es, "w", encoding="utf-8") as f:
        f.write(es_md)

    # 3. content/en/resources/_index.md
    p_en = "content/en/resources/_index.md"
    with open(p_en, "r", encoding="utf-8") as f:
        en_md = f.read()

    old_en_md = """          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="openModal('pack-pestel')">
              Details ℹ️
            </button>
            <span class="btn-kit-info btn-disabled" style="opacity: 0.55; cursor: default; border-style: dashed;" title="Methodological guide coming soon on the blog">Guide ⏳</span>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/17a0781c-8001-47df-9cdd-25923041e1de" class="btn-kit-buy lemonsqueezy-button">Download →</a>
          </div>"""

    new_en_md = """          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="openModal('pack-pestel')">
              Details ℹ️
            </button>
            <a href="/en/posts/quantitative-pestel-matrix/" class="btn-kit-info" title="Read technical article">Technical Article 📖</a>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/17a0781c-8001-47df-9cdd-25923041e1de" class="btn-kit-buy lemonsqueezy-button">Download →</a>
          </div>"""

    en_md, ok6 = replace_exact(en_md, old_en_md, new_en_md, "EN _index.md")
    with open(p_en, "w", encoding="utf-8") as f:
        f.write(en_md)

    print(f"\nSummary: All 6 replacements successful? {all([ok1, ok2, ok3, ok4, ok5, ok6])}")

if __name__ == '__main__':
    main()
