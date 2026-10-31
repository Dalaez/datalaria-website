import re
import sys

def update_catalog_html():
    with open('layouts/partials/recursos_catalog.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Normalize CRLF to LF
    content = content.replace('\r\n', '\n')

    # 1. ES quick grid
    old_es_quick_grid = """    <!-- ACCESO RÁPIDO A SUITES INDIVIDUALES -->
    <div class="suites-quick-grid" id="suites-quick-grid">
      <!-- Suite 01 -->
      <div class="suite-mini-card" id="suite-01" onclick="setTopic('estrategia')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">🏛️</div>
          <div>
            <div class="suite-mini-title">Pack Suite 1: Estrategia MBA</div>
            <div class="suite-mini-desc">5 packs (DAFO, Porter, PESTEL, BCG, McKinsey)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <span class="suite-mini-price">19€</span>
          <a href="https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd?embed=1" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
            Comprar Suite →
          </a>
        </div>
      </div>

      <!-- Suite 02 -->
      <div class="suite-mini-card" id="suite-02" onclick="setTopic('decisiones')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">⚖️</div>
          <div>
            <div class="suite-mini-title">Pack Suite 2: Decisiones</div>
            <div class="suite-mini-desc">3 packs (DAR Veto, RICE/ICE, Business Case)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <span class="suite-mini-price">15€</span>
          <a href="https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d?embed=1" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
            Comprar Suite →
          </a>
        </div>
      </div>

      <!-- Suite 03 -->
      <div class="suite-mini-card" id="suite-03" onclick="setTopic('operaciones')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">⚙️</div>
          <div>
            <div class="suite-mini-title">Pack Suite 3: Control Operativo</div>
            <div class="suite-mini-desc">5 packs PMBOK (RACI, AMFE, PERT, EVM, Stock)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <span class="suite-mini-price">22€</span>
          <a href="https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a?embed=1" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
            Comprar Suite →
          </a>
        </div>
      </div>
    </div>"""

    new_es_quick_grid = """    <!-- ACCESO RÁPIDO A SUITES INDIVIDUALES -->
    <div class="suites-quick-grid" id="suites-quick-grid">
      <!-- Suite 01 -->
      <div class="suite-mini-card" id="suite-01" onclick="setTopic('estrategia')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">🏛️</div>
          <div>
            <div class="suite-mini-title">Pack Suite 1: Estrategia MBA</div>
            <div class="suite-mini-desc">5 packs (DAFO, Porter, PESTEL, BCG, McKinsey)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <div class="kit-pricing-box">
            <span class="suite-mini-price">19€</span>
            <span class="kit-price-orig">28€</span>
          </div>
          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-01')">
              Detalles ℹ️
            </button>
            <a href="/es/posts/estrategia-corporativa-mba-framework-cuantitativo/" class="btn-kit-info" onclick="event.stopPropagation()" title="Leer artículo técnico">
              Artículo técnico 📖
            </a>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd?embed=1" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
              Comprar Suite →
            </a>
          </div>
        </div>
      </div>

      <!-- Suite 02 -->
      <div class="suite-mini-card" id="suite-02" onclick="setTopic('decisiones')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">⚖️</div>
          <div>
            <div class="suite-mini-title">Pack Suite 2: Decisiones</div>
            <div class="suite-mini-desc">3 packs (DAR Veto, RICE/ICE, Business Case)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <div class="kit-pricing-box">
            <span class="suite-mini-price">15€</span>
            <span class="kit-price-orig">20€</span>
          </div>
          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-02')">
              Detalles ℹ️
            </button>
            <span class="btn-kit-info btn-disabled" onclick="event.stopPropagation()" title="Artículo técnico próximamente">
              Artículo próximamente
            </span>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d?embed=1" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
              Comprar Suite →
            </a>
          </div>
        </div>
      </div>

      <!-- Suite 03 -->
      <div class="suite-mini-card" id="suite-03" onclick="setTopic('operaciones')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">⚙️</div>
          <div>
            <div class="suite-mini-title">Pack Suite 3: Control Operativo</div>
            <div class="suite-mini-desc">5 packs PMBOK (RACI, AMFE, PERT, EVM, Stock)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <div class="kit-pricing-box">
            <span class="suite-mini-price">22€</span>
            <span class="kit-price-orig">34€</span>
          </div>
          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-03')">
              Detalles ℹ️
            </button>
            <span class="btn-kit-info btn-disabled" onclick="event.stopPropagation()" title="Artículo técnico próximamente">
              Artículo próximamente
            </span>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a?embed=1" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
              Comprar Suite →
            </a>
          </div>
        </div>
      </div>
    </div>"""

    assert old_es_quick_grid in content, "Error: old_es_quick_grid not found"
    content = content.replace(old_es_quick_grid, new_es_quick_grid, 1)

    # 2. EN quick grid
    old_en_quick_grid = """    <!-- ACCESO RÁPIDO A SUITES INDIVIDUALES -->
    <div class="suites-quick-grid" id="suites-quick-grid">
      <!-- Suite 01 -->
      <div class="suite-mini-card" id="suite-01" onclick="setTopic('estrategia')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">🏛️</div>
          <div>
            <div class="suite-mini-title">Suite 1: MBA Strategy Pack</div>
            <div class="suite-mini-desc">5 packs (SWOT, Porter, PESTEL, BCG, McKinsey)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <span class="suite-mini-price">19€</span>
          <a href="https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd?embed=1" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
            Buy Suite →
          </a>
        </div>
      </div>

      <!-- Suite 02 -->
      <div class="suite-mini-card" id="suite-02" onclick="setTopic('decisiones')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">⚖️</div>
          <div>
            <div class="suite-mini-title">Suite 2: Decisions Pack</div>
            <div class="suite-mini-desc">3 packs (DAR Veto, RICE/ICE, Business Case)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <span class="suite-mini-price">15€</span>
          <a href="https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d?embed=1" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
            Buy Suite →
          </a>
        </div>
      </div>

      <!-- Suite 03 -->
      <div class="suite-mini-card" id="suite-03" onclick="setTopic('operaciones')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">⚙️</div>
          <div>
            <div class="suite-mini-title">Suite 3: Operations Control</div>
            <div class="suite-mini-desc">5 packs PMBOK (RACI, FMEA, PERT, EVM, Safety Stock)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <span class="suite-mini-price">22€</span>
          <a href="https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a?embed=1" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
            Buy Suite →
          </a>
        </div>
      </div>
    </div>"""

    new_en_quick_grid = """    <!-- ACCESO RÁPIDO A SUITES INDIVIDUALES -->
    <div class="suites-quick-grid" id="suites-quick-grid">
      <!-- Suite 01 -->
      <div class="suite-mini-card" id="suite-01" onclick="setTopic('estrategia')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">🏛️</div>
          <div>
            <div class="suite-mini-title">Suite 1: MBA Strategy Pack</div>
            <div class="suite-mini-desc">5 packs (SWOT, Porter, PESTEL, BCG, McKinsey)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <div class="kit-pricing-box">
            <span class="suite-mini-price">19€</span>
            <span class="kit-price-orig">28€</span>
          </div>
          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-01')">
              Details ℹ️
            </button>
            <a href="/en/posts/corporate-strategy-mba-quantitative-framework/" class="btn-kit-info" onclick="event.stopPropagation()" title="Read technical article">
              Technical Article 📖
            </a>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd?embed=1" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
              Buy Suite →
            </a>
          </div>
        </div>
      </div>

      <!-- Suite 02 -->
      <div class="suite-mini-card" id="suite-02" onclick="setTopic('decisiones')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">⚖️</div>
          <div>
            <div class="suite-mini-title">Suite 2: Decisions Pack</div>
            <div class="suite-mini-desc">3 packs (DAR Veto, RICE/ICE, Business Case)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <div class="kit-pricing-box">
            <span class="suite-mini-price">15€</span>
            <span class="kit-price-orig">20€</span>
          </div>
          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-02')">
              Details ℹ️
            </button>
            <span class="btn-kit-info btn-disabled" onclick="event.stopPropagation()" title="Technical article coming soon">
              Article coming soon
            </span>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d?embed=1" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
              Buy Suite →
            </a>
          </div>
        </div>
      </div>

      <!-- Suite 03 -->
      <div class="suite-mini-card" id="suite-03" onclick="setTopic('operaciones')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">⚙️</div>
          <div>
            <div class="suite-mini-title">Suite 3: Operations Control</div>
            <div class="suite-mini-desc">5 packs PMBOK (RACI, FMEA, PERT, EVM, Safety Stock)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <div class="kit-pricing-box">
            <span class="suite-mini-price">22€</span>
            <span class="kit-price-orig">34€</span>
          </div>
          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-03')">
              Details ℹ️
            </button>
            <span class="btn-kit-info btn-disabled" onclick="event.stopPropagation()" title="Technical article coming soon">
              Article coming soon
            </span>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a?embed=1" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
              Buy Suite →
            </a>
          </div>
        </div>
      </div>
    </div>"""

    assert old_en_quick_grid in content, "Error: old_en_quick_grid not found"
    content = content.replace(old_en_quick_grid, new_en_quick_grid, 1)

    # 3. ES SUITES_CONFIG
    old_es_suites_config = """  const SUITES_CONFIG = {
  "estrategia": {
    "title": "Pack Suite 1: Estrategia Corporativa & MBA",
    "desc": "Incluye los 5 Executive Decision Packs: DAFO CAME, Porter, PESTEL, BCG y McKinsey con todos sus modelos matriciales y presentaciones ejecutivas.",
    "tag": "👑 Suite 01 Completa • Ahorro 32%",
    "icon": "🏛️",
    "price": "19€",
    "origPrice": "28€",
    "available": true,
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd?embed=1"
  },
  "decisiones": {
    "title": "Pack Suite 2: Toma de Decisiones & Priorización",
    "desc": "Las 3 herramientas indispensables para comités de inversión y PMs: Matriz DAR Criterios Veto, RICE & ICE Ágil y Business Case Financiero VAN/TIR.",
    "tag": "👑 Suite 02 Completa • Ahorro 25%",
    "icon": "⚖️",
    "price": "15€",
    "origPrice": "20€",
    "available": true,
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d?embed=1"
  },
  "operaciones": {
    "title": "Pack Suite 3: Control Operativo & PMBOK",
    "desc": "Los 5 Executive Packs para directores de operaciones y project managers: RACI, AMFE, PERT, EVM Curva S y Stock de Seguridad.",
    "tag": "👑 Suite 03 Completa • Ahorro 35%",
    "icon": "⚙️",
    "price": "22€",
    "origPrice": "34€",
    "available": true,
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a?embed=1"
  },
  "software": {
    "title": "Suite de Ingeniería: Software, IA & SDD",
    "desc": "Kits de especificación formal ejecutable, arquitectura de agentes y contratos tipados para erradicar la deuda técnica del vibe coding.",
    "tag": "🔒 Próximo Lanzamiento",
    "icon": "💻",
    "price": "Próximamente",
    "origPrice": "",
    "available": false,
    "checkoutUrl": "#"
  }
};"""

    new_es_suites_config = """  const SUITES_CONFIG = {
  "estrategia": {
    "id": "suite-01",
    "title": "Pack Suite 1: Estrategia Corporativa & MBA",
    "topic": "estrategia",
    "topicLabel": "Estrategia MBA",
    "status": "available",
    "statusLabel": "🟢 DISPONIBLE • Suite Completa (5 Packs)",
    "price": "19€",
    "origPrice": "28€",
    "icon": "🏛️",
    "tag": "👑 Suite 01 Completa • Ahorro 32%",
    "delivs": [
      "10 Modelos Excel + Sheets",
      "10 Decks PowerPoint 16:9",
      "5 Guías Metodológicas PDF"
    ],
    "desc": "Incluye los 5 Executive Decision Packs: DAFO CAME, Porter, PESTEL, BCG y McKinsey con todos sus modelos matriciales, presentaciones ejecutivas y guías metodológicas.",
    "features": [
      "Colección completa de 5 marcos analíticos: PESTEL, Porter, DAFO-CAME, BCG y McKinsey/GE",
      "10 plantillas automatizadas en Excel y Google Sheets con validaciones y gráficos dinámicos",
      "10 presentaciones ejecutivas en PowerPoint 16:9 con Action Titles listos para Consejo",
      "Guías metodológicas PDF completas con formulación matemática y casos empresariales integrados"
    ],
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd?embed=1",
    "guideUrl": "/es/posts/estrategia-corporativa-mba-framework-cuantitativo/",
    "previewImg": "/images/recursos/suite-01-preview-es.png"
  },
  "decisiones": {
    "id": "suite-02",
    "title": "Pack Suite 2: Toma de Decisiones & Priorización",
    "topic": "decisiones",
    "topicLabel": "Toma de Decisiones",
    "status": "available",
    "statusLabel": "🟢 DISPONIBLE • Suite Completa (3 Packs)",
    "price": "15€",
    "origPrice": "20€",
    "icon": "⚖️",
    "tag": "👑 Suite 02 Completa • Ahorro 25%",
    "delivs": [
      "6 Modelos Excel + Sheets",
      "6 Decks PowerPoint 16:9",
      "3 Guías Metodológicas PDF"
    ],
    "desc": "Las 3 herramientas indispensables para comités de inversión y PMs: Matriz DAR Criterios Veto, RICE & ICE Ágil y Business Case Financiero VAN/TIR.",
    "features": [
      "Matriz DAR con Criterios Veto para blindar decisiones críticas de comité",
      "Framework de priorización RICE & ICE con scoring normalizado y roadmap",
      "Business Case Financiero completo con proyección a 5 años, VAN, TIR y Payback",
      "Decks ejecutivos PowerPoint 16:9 y guías paso a paso"
    ],
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d?embed=1",
    "guideUrl": "",
    "previewImg": ""
  },
  "operaciones": {
    "id": "suite-03",
    "title": "Pack Suite 3: Control Operativo & PMBOK",
    "topic": "operaciones",
    "topicLabel": "Control Operativo",
    "status": "available",
    "statusLabel": "🟢 DISPONIBLE • Suite Completa (5 Packs)",
    "price": "22€",
    "origPrice": "34€",
    "icon": "⚙️",
    "tag": "👑 Suite 03 Completa • Ahorro 35%",
    "delivs": [
      "10 Modelos Excel + Sheets",
      "10 Decks PowerPoint 16:9",
      "5 Guías Metodológicas PDF"
    ],
    "desc": "Los 5 Executive Packs para directores de operaciones y project managers: RACI, AMFE, PERT, EVM Curva S y Stock de Seguridad.",
    "features": [
      "Matriz RACI con validación de singularidad (1 Accountable estricto por tarea)",
      "Análisis AMFE / FMEA con cálculo automático del Número de Prioridad de Riesgo (NPR)",
      "Estimación probabilística PERT con cálculo de ruta crítica y varianza",
      "EVM (Valor Ganado) con Curva S, CPI, SPI y previsión EAC / ETC",
      "Modelo de Stock de Seguridad con nivel de servicio, demanda estocástica y punto de pedido"
    ],
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a?embed=1",
    "guideUrl": "",
    "previewImg": ""
  },
  "software": {
    "id": "suite-sdd",
    "title": "Suite de Ingeniería: Software, IA & SDD",
    "topic": "software",
    "topicLabel": "Ingeniería de Software & IA",
    "status": "coming",
    "statusLabel": "🔒 PRÓXIMAMENTE",
    "price": "Próximamente",
    "origPrice": "",
    "icon": "💻",
    "tag": "🔒 Próximo Lanzamiento",
    "delivs": [
      "Especificaciones SDD",
      "Arquitectura de Agentes",
      "Contratos Tipados"
    ],
    "desc": "Kits de especificación formal ejecutable, arquitectura de agentes y contratos tipados para erradicar la deuda técnica del vibe coding.",
    "features": [
      "Framework integral Spec-Driven Development (SDD) para equipos humanos y agentes de IA",
      "Contratos de invariantes y esquemas de validación deterministas",
      "Prompts de arquitectura y memoria persistente para coding assistants",
      "Plantillas ejecutables para eliminar el vibe coding"
    ],
    "checkoutUrl": "#",
    "guideUrl": "",
    "previewImg": ""
  }
};"""

    assert old_es_suites_config in content, "Error: old_es_suites_config not found"
    content = content.replace(old_es_suites_config, new_es_suites_config, 1)

    # 4. EN SUITES_CONFIG
    old_en_suites_config = """  const SUITES_CONFIG = {
  "estrategia": {
    "title": "Suite 1: MBA Corporate Strategy",
    "desc": "Includes all 5 Executive Decision Packs: SWOT TOWS, Porter, PESTEL, BCG and McKinsey with all matrix models and executive slide decks.",
    "tag": "👑 Complete Suite 01 • 32% Off",
    "icon": "🏛️",
    "price": "19€",
    "origPrice": "28€",
    "available": true,
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd?embed=1"
  },
  "decisiones": {
    "title": "Suite 2: Decision Making & Prioritization",
    "desc": "The 3 indispensable tools for Investment Committees & PMs: DAR Veto Matrix, Agile RICE & ICE, and Financial Business Case NPV/IRR.",
    "tag": "👑 Complete Suite 02 • 25% Off",
    "icon": "⚖️",
    "price": "15€",
    "origPrice": "20€",
    "available": true,
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d?embed=1"
  },
  "operaciones": {
    "title": "Suite 3: Operational Control & PMBOK",
    "desc": "The 5 Executive Packs for Operations Directors & Project Managers: RACI, FMEA, PERT, EVM S-Curve, and Safety Stock.",
    "tag": "👑 Complete Suite 03 • 35% Off",
    "icon": "⚙️",
    "price": "22€",
    "origPrice": "34€",
    "available": true,
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a?embed=1"
  },
  "software": {
    "title": "Engineering Suite: Software, AI & SDD",
    "desc": "Executable formal specifications, agent architecture and typed contracts to eradicate technical debt from vibe coding.",
    "tag": "🔒 Coming Soon",
    "icon": "💻",
    "price": "Coming soon",
    "origPrice": "",
    "available": false,
    "checkoutUrl": "#"
  }
};"""

    new_en_suites_config = """  const SUITES_CONFIG = {
  "estrategia": {
    "id": "suite-01",
    "title": "Suite 1: MBA Corporate Strategy",
    "topic": "estrategia",
    "topicLabel": "MBA Strategy",
    "status": "available",
    "statusLabel": "🟢 AVAILABLE • Complete Suite (5 Packs)",
    "price": "19€",
    "origPrice": "28€",
    "icon": "🏛️",
    "tag": "👑 Complete Suite 01 • 32% Off",
    "delivs": [
      "10 Excel + Sheets Models",
      "10 PowerPoint 16:9 Decks",
      "5 Methodology PDF Guides"
    ],
    "desc": "Includes all 5 Executive Decision Packs: SWOT TOWS, Porter, PESTEL, BCG and McKinsey with all matrix models, executive slide decks, and methodology guides.",
    "features": [
      "Complete 5-framework collection: PESTEL, Porter, SWOT-TOWS, BCG and McKinsey/GE",
      "10 automated templates in Excel & Google Sheets with dynamic charting and error checks",
      "10 executive slide decks in PowerPoint 16:9 with boardroom-ready Action Titles",
      "Full PDF methodology guides with mathematical formulations and real enterprise case studies"
    ],
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd?embed=1",
    "guideUrl": "/en/posts/corporate-strategy-mba-quantitative-framework/",
    "previewImg": "/images/recursos/suite-01-preview-en.png"
  },
  "decisiones": {
    "id": "suite-02",
    "title": "Suite 2: Decision Making & Prioritization",
    "topic": "decisiones",
    "topicLabel": "Decision Making",
    "status": "available",
    "statusLabel": "🟢 AVAILABLE • Complete Suite (3 Packs)",
    "price": "15€",
    "origPrice": "20€",
    "icon": "⚖️",
    "tag": "👑 Complete Suite 02 • 25% Off",
    "delivs": [
      "6 Excel + Sheets Models",
      "6 PowerPoint 16:9 Decks",
      "3 Methodology PDF Guides"
    ],
    "desc": "The 3 indispensable tools for Investment Committees & PMs: DAR Veto Matrix, Agile RICE & ICE, and Financial Business Case NPV/IRR.",
    "features": [
      "DAR Decision Matrix with Veto criteria to safeguard boardroom signoffs",
      "RICE & ICE prioritization framework with normalized scoring and roadmap view",
      "Financial Business Case with 5-year cash-flow forecasting, NPV, IRR, and Payback",
      "Executive 16:9 slide decks and step-by-step implementation playbooks"
    ],
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d?embed=1",
    "guideUrl": "",
    "previewImg": ""
  },
  "operaciones": {
    "id": "suite-03",
    "title": "Suite 3: Operational Control & PMBOK",
    "topic": "operaciones",
    "topicLabel": "Operations Control",
    "status": "available",
    "statusLabel": "🟢 AVAILABLE • Complete Suite (5 Packs)",
    "price": "22€",
    "origPrice": "34€",
    "icon": "⚙️",
    "tag": "👑 Complete Suite 03 • 35% Off",
    "delivs": [
      "10 Excel + Sheets Models",
      "10 PowerPoint 16:9 Decks",
      "5 Methodology PDF Guides"
    ],
    "desc": "The 5 Executive Packs for Operations Directors & Project Managers: RACI, FMEA, PERT, EVM S-Curve, and Safety Stock.",
    "features": [
      "RACI Matrix with single-accountable governance validation",
      "FMEA Risk Matrix with automated Risk Priority Number (RPN) calculation",
      "PERT Probabilistic Estimation with critical path and variance formulas",
      "EVM (Earned Value Management) with S-Curve, CPI, SPI, and EAC forecasting",
      "Safety Stock Model with customer service levels, stochastic demand and reorder points"
    ],
    "checkoutUrl": "https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a?embed=1",
    "guideUrl": "",
    "previewImg": ""
  },
  "software": {
    "id": "suite-sdd",
    "title": "Engineering Suite: Software, AI & SDD",
    "topic": "software",
    "topicLabel": "Software Engineering & AI",
    "status": "coming",
    "statusLabel": "🔒 COMING SOON",
    "price": "Coming soon",
    "origPrice": "",
    "icon": "💻",
    "tag": "🔒 Coming Soon",
    "delivs": [
      "SDD Specifications",
      "Agent Architecture",
      "Typed Contracts"
    ],
    "desc": "Executable formal specifications, agent architecture and typed contracts to eradicate technical debt from vibe coding.",
    "features": [
      "Full Spec-Driven Development (SDD) framework for human developers and AI agents",
      "Deterministic invariant contracts and schema validation rules",
      "System prompt architecture and persistent memory playbooks for coding assistants",
      "Executable boilerplate templates to eliminate vibe coding debt"
    ],
    "checkoutUrl": "#",
    "guideUrl": "",
    "previewImg": ""
  }
};"""

    assert old_en_suites_config in content, "Error: old_en_suites_config not found"
    content = content.replace(old_en_suites_config, new_en_suites_config, 1)

    # 5. ES setTopic suite-ctx-btn-box
    old_es_set_topic_btn = """        const btnBox = document.getElementById('suite-ctx-btn-box');
        if (suite.available) {
          btnBox.innerHTML = `<a href="${suite.checkoutUrl}" class="btn-suite-buy-full lemonsqueezy-button">Obtener Bundle Suite • ` + suite.price + ` →</a>`;
        } else {
          btnBox.innerHTML = `<span class="badge-suite-soon" style="padding: 8px 14px; font-size: 12px;">Próximamente</span>`;
        }"""

    new_es_set_topic_btn = """        const btnBox = document.getElementById('suite-ctx-btn-box');
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

    assert old_es_set_topic_btn in content, "Error: old_es_set_topic_btn not found"
    content = content.replace(old_es_set_topic_btn, new_es_set_topic_btn, 1)

    # 6. EN setTopic suite-ctx-btn-box
    old_en_set_topic_btn = """        const btnBox = document.getElementById('suite-ctx-btn-box');
        if (suite.available) {
          btnBox.innerHTML = `<a href="${suite.checkoutUrl}" class="btn-suite-buy-full lemonsqueezy-button">Buy Suite Bundle • ` + suite.price + ` →</a>`;
        } else {
          btnBox.innerHTML = `<span class="badge-suite-soon" style="padding: 8px 14px; font-size: 12px;">Coming Soon</span>`;
        }"""

    new_en_set_topic_btn = """        const btnBox = document.getElementById('suite-ctx-btn-box');
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

    assert old_en_set_topic_btn in content, "Error: old_en_set_topic_btn not found"
    content = content.replace(old_en_set_topic_btn, new_en_set_topic_btn, 1)

    # 7. ES openModal
    old_es_open_modal = """  function openModal(kitId) {
    const kit = KITS_DATA.find(k => k.id === kitId);
    if (!kit) return;

    document.getElementById('modal-icon').textContent = kit.icon;
    document.getElementById('modal-title').textContent = kit.title;
    document.getElementById('modal-title').dataset.kitId = kit.id;
    document.getElementById('modal-cat').textContent = kit.topicLabel;
    document.getElementById('modal-desc').textContent = kit.desc;
    document.getElementById('modal-price').textContent = kit.price;

    renderModalPreview(kit, true);

    const delivsEl = document.getElementById('modal-delivs');
    delivsEl.innerHTML = kit.delivs.map(d => `<span class="deliv-chip" style="font-size: 12px; padding: 4px 8px;">${d}</span>`).join('');

    const featuresEl = document.getElementById('modal-features');
    featuresEl.innerHTML = kit.features.map(f => `
      <li>
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
        <span>${f}</span>
      </li>
    `).join('');

    const buyBtn = document.getElementById('modal-buy-link');
    if (kit.status === 'available') {
      buyBtn.href = kit.checkoutUrl;
      buyBtn.className = 'btn-kit-buy lemonsqueezy-button';
      buyBtn.textContent = `Descargar Kit • ` + kit.price;
      buyBtn.style.display = 'inline-flex';
    }"""

    new_es_open_modal = """  function openModal(kitId) {
    const kit = KITS_DATA.find(k => k.id === kitId) || Object.values(SUITES_CONFIG).find(s => s.id === kitId);
    if (!kit) return;

    document.getElementById('modal-icon').textContent = kit.icon;
    document.getElementById('modal-title').textContent = kit.title;
    document.getElementById('modal-title').dataset.kitId = kit.id;
    document.getElementById('modal-cat').textContent = kit.topicLabel;
    document.getElementById('modal-desc').textContent = kit.desc;
    document.getElementById('modal-price').textContent = kit.origPrice ? `${kit.price} (antes ${kit.origPrice})` : kit.price;

    renderModalPreview(kit, true);

    const delivsEl = document.getElementById('modal-delivs');
    delivsEl.innerHTML = kit.delivs.map(d => `<span class="deliv-chip" style="font-size: 12px; padding: 4px 8px;">${d}</span>`).join('');

    const featuresEl = document.getElementById('modal-features');
    featuresEl.innerHTML = kit.features.map(f => `
      <li>
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
        <span>${f}</span>
      </li>
    `).join('');

    const buyBtn = document.getElementById('modal-buy-link');
    if (kit.status === 'available') {
      buyBtn.href = kit.checkoutUrl;
      buyBtn.className = 'btn-kit-buy lemonsqueezy-button';
      buyBtn.textContent = kit.id.startsWith('suite') ? `Descargar Suite • ${kit.price}` : `Descargar Kit • ${kit.price}`;
      buyBtn.style.display = 'inline-flex';
    }"""

    assert old_es_open_modal in content, "Error: old_es_open_modal not found"
    content = content.replace(old_es_open_modal, new_es_open_modal, 1)

    # 8. EN openModal
    old_en_open_modal = """  function openModal(kitId) {
    const kit = KITS_DATA.find(k => k.id === kitId);
    if (!kit) return;

    document.getElementById('modal-icon').textContent = kit.icon;
    document.getElementById('modal-title').textContent = kit.title;
    document.getElementById('modal-cat').textContent = kit.topicLabel;
    document.getElementById('modal-desc').textContent = kit.desc;
    document.getElementById('modal-price').textContent = kit.price;

    renderModalPreview(kit, false);

    const delivsEl = document.getElementById('modal-delivs');
    delivsEl.innerHTML = kit.delivs.map(d => `<span class="deliv-chip" style="font-size: 12px; padding: 4px 8px;">${d}</span>`).join('');

    const featuresEl = document.getElementById('modal-features');
    featuresEl.innerHTML = kit.features.map(f => `
      <li>
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
        <span>${f}</span>
      </li>
    `).join('');

    const buyBtn = document.getElementById('modal-buy-link');
    if (kit.status === 'available') {
      buyBtn.href = kit.checkoutUrl;
      buyBtn.className = 'btn-kit-buy lemonsqueezy-button';
      buyBtn.textContent = `Download Pack • ` + kit.price;
      buyBtn.style.display = 'inline-flex';
    }"""

    new_en_open_modal = """  function openModal(kitId) {
    const kit = KITS_DATA.find(k => k.id === kitId) || Object.values(SUITES_CONFIG).find(s => s.id === kitId);
    if (!kit) return;

    document.getElementById('modal-icon').textContent = kit.icon;
    document.getElementById('modal-title').textContent = kit.title;
    document.getElementById('modal-cat').textContent = kit.topicLabel;
    document.getElementById('modal-desc').textContent = kit.desc;
    document.getElementById('modal-price').textContent = kit.origPrice ? `${kit.price} (was ${kit.origPrice})` : kit.price;

    renderModalPreview(kit, false);

    const delivsEl = document.getElementById('modal-delivs');
    delivsEl.innerHTML = kit.delivs.map(d => `<span class="deliv-chip" style="font-size: 12px; padding: 4px 8px;">${d}</span>`).join('');

    const featuresEl = document.getElementById('modal-features');
    featuresEl.innerHTML = kit.features.map(f => `
      <li>
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
        <span>${f}</span>
      </li>
    `).join('');

    const buyBtn = document.getElementById('modal-buy-link');
    if (kit.status === 'available') {
      buyBtn.href = kit.checkoutUrl;
      buyBtn.className = 'btn-kit-buy lemonsqueezy-button';
      buyBtn.textContent = kit.id.startsWith('suite') ? `Download Suite • ${kit.price}` : `Download Pack • ${kit.price}`;
      buyBtn.style.display = 'inline-flex';
    }"""

    assert old_en_open_modal in content, "Error: old_en_open_modal not found"
    content = content.replace(old_en_open_modal, new_en_open_modal, 1)

    with open('layouts/partials/recursos_catalog.html', 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print("layouts/partials/recursos_catalog.html updated successfully!")


def update_content_markdown_files():
    # Update content/es/recursos/_index.md and content/en/resources/_index.md
    with open('content/es/recursos/_index.md', 'r', encoding='utf-8') as f:
        es_md = f.read().replace('\r\n', '\n')

    # Regex search for suites-quick-grid
    quick_grid_pattern = r'(<div class="suites-quick-grid">.*?<!-- Suite 03 -->.*?</div>\s*</div>\s*</div>)'
    
    new_es_grid = """<div class="suites-quick-grid">
      <!-- Suite 01 -->
      <div class="suite-mini-card" id="suite-01" onclick="setTopic('estrategia')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">🏛️</div>
          <div>
            <div class="suite-mini-title">Pack Suite 1: Estrategia MBA</div>
            <div class="suite-mini-desc">5 packs (DAFO, Porter, PESTEL, BCG, McKinsey)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <div class="kit-pricing-box">
            <span class="suite-mini-price">19€</span>
            <span class="kit-price-orig">28€</span>
          </div>
          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-01')">
              Detalles ℹ️
            </button>
            <a href="/es/posts/estrategia-corporativa-mba-framework-cuantitativo/" class="btn-kit-info" onclick="event.stopPropagation()" title="Leer artículo técnico">
              Artículo técnico 📖
            </a>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
              Comprar Suite →
            </a>
          </div>
        </div>
      </div>

      <!-- Suite 02 -->
      <div class="suite-mini-card" id="suite-02" onclick="setTopic('decisiones')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">⚖️</div>
          <div>
            <div class="suite-mini-title">Pack Suite 2: Decisiones</div>
            <div class="suite-mini-desc">3 packs (DAR Veto, RICE/ICE, Business Case)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <div class="kit-pricing-box">
            <span class="suite-mini-price">15€</span>
            <span class="kit-price-orig">20€</span>
          </div>
          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-02')">
              Detalles ℹ️
            </button>
            <span class="btn-kit-info btn-disabled" onclick="event.stopPropagation()" title="Artículo técnico próximamente">
              Artículo próximamente
            </span>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
              Comprar Suite →
            </a>
          </div>
        </div>
      </div>

      <!-- Suite 03 -->
      <div class="suite-mini-card" id="suite-03" onclick="setTopic('operaciones')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">⚙️</div>
          <div>
            <div class="suite-mini-title">Pack Suite 3: Control Operativo</div>
            <div class="suite-mini-desc">5 packs PMBOK (RACI, AMFE, PERT, EVM, Stock)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <div class="kit-pricing-box">
            <span class="suite-mini-price">22€</span>
            <span class="kit-price-orig">34€</span>
          </div>
          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-03')">
              Detalles ℹ️
            </button>
            <span class="btn-kit-info btn-disabled" onclick="event.stopPropagation()" title="Artículo técnico próximamente">
              Artículo próximamente
            </span>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
              Comprar Suite →
            </a>
          </div>
        </div>
      </div>
    </div>"""

    match_es = re.search(quick_grid_pattern, es_md, re.DOTALL)
    if match_es:
        es_md = es_md[:match_es.start()] + new_es_grid + es_md[match_es.end():]
        with open('content/es/recursos/_index.md', 'w', encoding='utf-8', newline='\n') as f:
            f.write(es_md)
        print("content/es/recursos/_index.md updated successfully!")
    else:
        print("Warning: quick_grid_pattern not found in content/es/recursos/_index.md")

    # Now EN
    with open('content/en/resources/_index.md', 'r', encoding='utf-8') as f:
        en_md = f.read().replace('\r\n', '\n')

    new_en_grid = """<div class="suites-quick-grid">
      <!-- Suite 01 -->
      <div class="suite-mini-card" id="suite-01" onclick="setTopic('estrategia')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">🏛️</div>
          <div>
            <div class="suite-mini-title">Suite 1: MBA Strategy Pack</div>
            <div class="suite-mini-desc">5 packs (SWOT, Porter, PESTEL, BCG, McKinsey)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <div class="kit-pricing-box">
            <span class="suite-mini-price">19€</span>
            <span class="kit-price-orig">28€</span>
          </div>
          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-01')">
              Details ℹ️
            </button>
            <a href="/en/posts/corporate-strategy-mba-quantitative-framework/" class="btn-kit-info" onclick="event.stopPropagation()" title="Read technical article">
              Technical Article 📖
            </a>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
              Buy Suite →
            </a>
          </div>
        </div>
      </div>

      <!-- Suite 02 -->
      <div class="suite-mini-card" id="suite-02" onclick="setTopic('decisiones')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">⚖️</div>
          <div>
            <div class="suite-mini-title">Suite 2: Decisions Pack</div>
            <div class="suite-mini-desc">3 packs (DAR Veto, RICE/ICE, Business Case)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <div class="kit-pricing-box">
            <span class="suite-mini-price">15€</span>
            <span class="kit-price-orig">20€</span>
          </div>
          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-02')">
              Details ℹ️
            </button>
            <span class="btn-kit-info btn-disabled" onclick="event.stopPropagation()" title="Technical article coming soon">
              Article coming soon
            </span>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/4e2ca8b1-a6f9-43b7-851a-72c44d9bc13d" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
              Buy Suite →
            </a>
          </div>
        </div>
      </div>

      <!-- Suite 03 -->
      <div class="suite-mini-card" id="suite-03" onclick="setTopic('operaciones')">
        <div class="suite-mini-info">
          <div class="suite-mini-icon">⚙️</div>
          <div>
            <div class="suite-mini-title">Suite 3: Operations Control</div>
            <div class="suite-mini-desc">5 packs PMBOK (RACI, FMEA, PERT, EVM, Safety Stock)</div>
          </div>
        </div>
        <div class="suite-mini-action">
          <div class="kit-pricing-box">
            <span class="suite-mini-price">22€</span>
            <span class="kit-price-orig">34€</span>
          </div>
          <div class="kit-btns-group">
            <button type="button" class="btn-kit-info" onclick="event.stopPropagation(); openModal('suite-03')">
              Details ℹ️
            </button>
            <span class="btn-kit-info btn-disabled" onclick="event.stopPropagation()" title="Technical article coming soon">
              Article coming soon
            </span>
            <a href="https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a" class="btn-suite-buy-mini lemonsqueezy-button" onclick="event.stopPropagation()">
              Buy Suite →
            </a>
          </div>
        </div>
      </div>
    </div>"""

    match_en = re.search(quick_grid_pattern, en_md, re.DOTALL)
    if match_en:
        en_md = en_md[:match_en.start()] + new_en_grid + en_md[match_en.end():]
        with open('content/en/resources/_index.md', 'w', encoding='utf-8', newline='\n') as f:
            f.write(en_md)
        print("content/en/resources/_index.md updated successfully!")
    else:
        print("Warning: quick_grid_pattern not found in content/en/resources/_index.md")


def update_kits_yaml():
    with open('data/pulse/kits.yaml', 'r', encoding='utf-8') as f:
        yaml_content = f.read().replace('\r\n', '\n')

    # Update suite-01: add guide_url_es and guide_url_en
    old_suite_01 = """- id: suite-01
  slug: suite-1-estrategia-mba
  type: suite
  topic: estrategia
  status: available
  price: 19 €
  original_price: 29 €
  icon: 📊
  checkout_url: https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd
  title_es: 'Pack Suite 1: Estrategia MBA'
  title_en: 'Suite 1: MBA Strategy'
  description_es: 'Colección completa de 5 modelos de decisión estratégica: DAFO Cuantitativo,
    5 Fuerzas de Porter, PESTEL, BCG y McKinsey / GE.'
  description_en: 'Complete collection of 5 strategic decision models: Quantitative
    SWOT, Porter 5 Forces, PESTEL, BCG and McKinsey / GE.'
  included_kits:"""

    new_suite_01 = """- id: suite-01
  slug: suite-1-estrategia-mba
  type: suite
  topic: estrategia
  status: available
  price: 19 €
  original_price: 29 €
  icon: 🏛️
  checkout_url: https://datalaria.lemonsqueezy.com/checkout/buy/6afa0df4-fec1-4227-a183-9e5bcc738bdd
  title_es: 'Pack Suite 1: Estrategia MBA'
  title_en: 'Suite 1: MBA Strategy'
  description_es: 'Colección completa de 5 modelos de decisión estratégica: DAFO Cuantitativo,
    5 Fuerzas de Porter, PESTEL, BCG y McKinsey / GE.'
  description_en: 'Complete collection of 5 strategic decision models: Quantitative
    SWOT, Porter 5 Forces, PESTEL, BCG and McKinsey / GE.'
  guide_url_es: /es/posts/estrategia-corporativa-mba-framework-cuantitativo/
  guide_url_en: /en/posts/corporate-strategy-mba-quantitative-framework/
  included_kits:"""

    assert old_suite_01 in yaml_content, "Error: old_suite_01 not found"
    yaml_content = yaml_content.replace(old_suite_01, new_suite_01, 1)

    # Update pack-porter guide URLs
    old_porter = """  title_es: 5 Fuerzas de Porter Ponderadas
  description_es: Scoring cuantitativo por fuerza competitiva, gráfico Radar dinámico
    auto-generado y diagnóstico de foso defensivo (Moat).
  article_url_es: null
  guide_url_es: null
  title_en: Weighted Porter's 5 Forces
  category_en: MBA Strategy
  description_en: Quantitative scoring per competitive force, dynamic radar chart
    and defensible Economic Moat spread diagnostic.
  deliverables_en:
  - Excel .xlsx + Sheets
  - PowerPoint 16:9
  - PDF Guide
  features_en:
  - Numeric 0-to-10 scoring per market power dimension
  - Dynamic Radar chart exportable directly to executive slides
  - Fitted 16:9 PPTX slide with one-click chart container
  - Methodology guide covering barrier dynamics and industry rents
  article_url_en: null
  guide_url_en: null"""

    new_porter = """  title_es: 5 Fuerzas de Porter Ponderadas
  description_es: Scoring cuantitativo por fuerza competitiva, gráfico Radar dinámico
    auto-generado y diagnóstico de foso defensivo (Moat).
  article_url_es: null
  guide_url_es: /es/posts/5-fuerzas-porter-cuantitativas/
  title_en: Weighted Porter's 5 Forces
  category_en: MBA Strategy
  description_en: Quantitative scoring per competitive force, dynamic radar chart
    and defensible Economic Moat spread diagnostic.
  deliverables_en:
  - Excel .xlsx + Sheets
  - PowerPoint 16:9
  - PDF Guide
  features_en:
  - Numeric 0-to-10 scoring per market power dimension
  - Dynamic Radar chart exportable directly to executive slides
  - Fitted 16:9 PPTX slide with one-click chart container
  - Methodology guide covering barrier dynamics and industry rents
  article_url_en: null
  guide_url_en: /en/posts/quantitative-porter-5-forces/"""

    assert old_porter in yaml_content, "Error: old_porter not found"
    yaml_content = yaml_content.replace(old_porter, new_porter, 1)

    # Update pack-pestel guide URLs
    old_pestel = """  title_es: Matriz PESTEL con Severidad & Volatilidad
  description_es: Evaluación de 6 factores macro con índice de impacto compuesto y
    mapa térmico de riesgos regulatorios y macroeconómicos.
  article_url_es: null
  guide_url_es: null
  title_en: Quantitative PESTEL (Severity & Volatility)
  category_en: MBA Strategy
  description_en: Assessment of 6 macro factors with composite risk indices and early
    warning heatmaps for regulatory and economic shocks.
  deliverables_en:
  - Excel .xlsx + Sheets
  - PowerPoint 16:9
  - PDF Guide
  features_en:
  - Weighted evaluation across Political, Economic, Social, Tech, Ecological, and
    Legal drivers
  - Automated risk heatmap with early warning thresholds
  - 16:9 PPTX slide with uncertainty matrix for executive committees
  - PDF scenario planning and macro stress-testing guide
  article_url_en: null
  guide_url_en: null"""

    new_pestel = """  title_es: Matriz PESTEL con Severidad & Volatilidad
  description_es: Evaluación de 6 factores macro con índice de impacto compuesto y
    mapa térmico de riesgos regulatorios y macroeconómicos.
  article_url_es: null
  guide_url_es: /es/posts/matriz-pestel-cuantitativa/
  title_en: Quantitative PESTEL (Severity & Volatility)
  category_en: MBA Strategy
  description_en: Assessment of 6 macro factors with composite risk indices and early
    warning heatmaps for regulatory and economic shocks.
  deliverables_en:
  - Excel .xlsx + Sheets
  - PowerPoint 16:9
  - PDF Guide
  features_en:
  - Weighted evaluation across Political, Economic, Social, Tech, Ecological, and
    Legal drivers
  - Automated risk heatmap with early warning thresholds
  - 16:9 PPTX slide with uncertainty matrix for executive committees
  - PDF scenario planning and macro stress-testing guide
  article_url_en: null
  guide_url_en: /en/posts/quantitative-pestel-matrix/"""

    assert old_pestel in yaml_content, "Error: old_pestel not found"
    yaml_content = yaml_content.replace(old_pestel, new_pestel, 1)

    with open('data/pulse/kits.yaml', 'w', encoding='utf-8', newline='\n') as f:
        f.write(yaml_content)
    print("data/pulse/kits.yaml updated successfully!")

if __name__ == '__main__':
    update_catalog_html()
    update_content_markdown_files()
    update_kits_yaml()
