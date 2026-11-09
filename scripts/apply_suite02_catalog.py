import os

path = "layouts/partials/recursos_catalog.html"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. ES Quick Grid suite-02 button
old_es_btn = """            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-02')">
              Detalles ℹ️
            </button>
            <span class="btn-kit-info btn-disabled" onclick="event.stopPropagation()" title="Artículo técnico próximamente">
              Artículo próximamente
            </span>"""

new_es_btn = """            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-02')">
              Detalles ℹ️
            </button>
            <a href="/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/" class="btn-kit-info" onclick="event.stopPropagation()" title="Leer artículo técnico">
              Artículo técnico 📖
            </a>"""

assert old_es_btn in text, "Could not find old_es_btn"
text = text.replace(old_es_btn, new_es_btn, 1)

# 2. ES SUITES_CONFIG suite-02
old_es_config = """"checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d?embed=1",
    "guideUrl": "",
    "previewImg": ""
  },"""

new_es_config = """"checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d?embed=1",
    "guideUrl": "/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/",
    "previewImg": "/images/recursos/suite-02-preview-es.png"
  },"""

assert old_es_config in text, "Could not find old_es_config"
text = text.replace(old_es_config, new_es_config, 1)

# 3. EN Quick Grid suite-02 button
old_en_btn = """            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-02')">
              Details ℹ️
            </button>
            <span class="btn-kit-info btn-disabled" onclick="event.stopPropagation()" title="Technical article coming soon">
              Article coming soon
            </span>"""

new_en_btn = """            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-02')">
              Details ℹ️
            </button>
            <a href="/en/posts/decision-making-prioritization-quantitative-framework/" class="btn-kit-info" onclick="event.stopPropagation()" title="Read technical article">
              Technical article 📖
            </a>"""

assert old_en_btn in text, "Could not find old_en_btn"
text = text.replace(old_en_btn, new_en_btn, 1)

# 4. EN SUITES_CONFIG suite-02
old_en_config = """"checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d?embed=1",
    "guideUrl": "",
    "previewImg": ""
  },
  "operaciones": {"""

new_en_config = """"checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d?embed=1",
    "guideUrl": "/en/posts/decision-making-prioritization-quantitative-framework/",
    "previewImg": "/images/recursos/suite-02-preview-en.png"
  },
  "operaciones": {"""

assert old_en_config in text, "Could not find old_en_config"
text = text.replace(old_en_config, new_en_config, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] recursos_catalog.html successfully updated for Suite 02!")
