import re

def update_recursos_catalog():
    path = 'layouts/partials/recursos_catalog.html'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read().replace('\r\n', '\n')

    # 1. ES Static HTML for suite-ctx-btn-box
    es_static_old = """          <div id="suite-ctx-btn-box">
            <a href="#" id="suite-ctx-btn" class="btn-suite-buy-full lemonsqueezy-button">
              Obtener Bundle Suite →
            </a>
          </div>"""

    es_static_new = """          <div id="suite-ctx-btn-box">
            <div class="kit-btns-group" style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
              <button type="button" class="btn-kit-info" onclick="openModal('suite-01')">
                Detalles ℹ️
              </button>
              <a href="/es/posts/estrategia-corporativa-mba-framework-cuantitativo/" class="btn-kit-info" title="Leer artículo técnico">
                Artículo técnico 📖
              </a>
              <a href="https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd?embed=1" class="btn-kit-buy lemonsqueezy-button" title="Descargar Suite Completa (.ZIP)">
                Descargar →
              </a>
            </div>
          </div>"""

    assert es_static_old in text, "Could not find ES static HTML"
    text = text.replace(es_static_old, es_static_new, 1)
    print("ES Static HTML updated!")

    # 2. EN Static HTML for suite-ctx-btn-box
    en_static_old = """          <div id="suite-ctx-btn-box">
            <a href="#" id="suite-ctx-btn" class="btn-suite-buy-full lemonsqueezy-button">
              Buy Suite Bundle →
            </a>
          </div>"""

    en_static_new = """          <div id="suite-ctx-btn-box">
            <div class="kit-btns-group" style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
              <button type="button" class="btn-kit-info" onclick="openModal('suite-01')">
                Details ℹ️
              </button>
              <a href="/en/posts/corporate-strategy-mba-quantitative-framework/" class="btn-kit-info" title="Read technical article">
                Technical article 📖
              </a>
              <a href="https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd?embed=1" class="btn-kit-buy lemonsqueezy-button" title="Download Complete Suite (.ZIP)">
                Download →
              </a>
            </div>
          </div>"""

    assert en_static_old in text, "Could not find EN static HTML"
    text = text.replace(en_static_old, en_static_new, 1)
    print("EN Static HTML updated!")

    # 3. ES JS setTopic
    es_js_old = """        const btnBox = document.getElementById('suite-ctx-btn-box');
        if (suite.available) {
          btnBox.innerHTML = `
            <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
              <button type="button" class="btn-kit-info" onclick="openModal('${suite.id}')" style="padding: 7px 11px; font-size: 12px;">
                Detalles ℹ️
              </button>
              ${suite.guideUrl 
                ? `<a href="${suite.guideUrl}" class="btn-kit-info" style="padding: 7px 11px; font-size: 12px;" title="Leer artículo técnico">Artículo técnico 📖</a>` 
                : `<span class="btn-kit-info btn-disabled" style="padding: 7px 11px; font-size: 12px;" title="Artículo técnico próximamente">Artículo próximamente</span>`
              }
              <a href="${suite.checkoutUrl}" class="btn-suite-buy-full lemonsqueezy-button">Obtener Bundle Suite • ${suite.price} →</a>
            </div>
          `;
        } else {
          btnBox.innerHTML = `<span class="badge-suite-soon" style="padding: 8px 14px; font-size: 12px;">Próximamente</span>`;
        }"""

    es_js_new = """        const btnBox = document.getElementById('suite-ctx-btn-box');
        const isAvailable = (suite.status === 'available' || suite.available === true);
        if (isAvailable) {
          btnBox.innerHTML = `
            <div class="kit-btns-group" style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
              <button type="button" class="btn-kit-info" onclick="openModal('${suite.id}')">
                Detalles ℹ️
              </button>
              ${suite.guideUrl 
                ? `<a href="${suite.guideUrl}" class="btn-kit-info" title="Leer artículo técnico">Artículo técnico 📖</a>` 
                : `<span class="btn-kit-info btn-disabled" title="Artículo técnico próximamente">Artículo próximamente</span>`
              }
              <a href="${suite.checkoutUrl}" class="btn-kit-buy lemonsqueezy-button" title="Descargar Suite Completa (.ZIP)">Descargar →</a>
            </div>
          `;
        } else {
          btnBox.innerHTML = `<span class="badge-suite-soon" style="padding: 8px 14px; font-size: 12px;">Próximamente</span>`;
        }"""

    assert es_js_old in text, "Could not find ES JS snippet"
    text = text.replace(es_js_old, es_js_new, 1)
    print("ES JS updated!")

    # 4. EN JS setTopic
    en_js_old = """        const btnBox = document.getElementById('suite-ctx-btn-box');
        if (suite.available) {
          btnBox.innerHTML = `
            <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
              <button type="button" class="btn-kit-info" onclick="openModal('${suite.id}')" style="padding: 7px 11px; font-size: 12px;">
                Details ℹ️
              </button>
              ${suite.guideUrl 
                ? `<a href="${suite.guideUrl}" class="btn-kit-info" style="padding: 7px 11px; font-size: 12px;" title="Read technical article">Technical Article 📖</a>` 
                : `<span class="btn-kit-info btn-disabled" style="padding: 7px 11px; font-size: 12px;" title="Technical article coming soon">Article coming soon</span>`
              }
              <a href="${suite.checkoutUrl}" class="btn-suite-buy-full lemonsqueezy-button">Buy Suite Bundle • ${suite.price} →</a>
            </div>
          `;
        } else {
          btnBox.innerHTML = `<span class="badge-suite-soon" style="padding: 8px 14px; font-size: 12px;">Coming Soon</span>`;
        }"""

    en_js_new = """        const btnBox = document.getElementById('suite-ctx-btn-box');
        const isAvailable = (suite.status === 'available' || suite.available === true);
        if (isAvailable) {
          btnBox.innerHTML = `
            <div class="kit-btns-group" style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
              <button type="button" class="btn-kit-info" onclick="openModal('${suite.id}')">
                Details ℹ️
              </button>
              ${suite.guideUrl 
                ? `<a href="${suite.guideUrl}" class="btn-kit-info" title="Read technical article">Technical article 📖</a>` 
                : `<span class="btn-kit-info btn-disabled" title="Technical article coming soon">Article coming soon</span>`
              }
              <a href="${suite.checkoutUrl}" class="btn-kit-buy lemonsqueezy-button" title="Download Complete Suite (.ZIP)">Download →</a>
            </div>
          `;
        } else {
          btnBox.innerHTML = `<span class="badge-suite-soon" style="padding: 8px 14px; font-size: 12px;">Coming Soon</span>`;
        }"""

    assert en_js_old in text, "Could not find EN JS snippet"
    text = text.replace(en_js_old, en_js_new, 1)
    print("EN JS updated!")

    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print("layouts/partials/recursos_catalog.html updated successfully!")

if __name__ == '__main__':
    update_recursos_catalog()
