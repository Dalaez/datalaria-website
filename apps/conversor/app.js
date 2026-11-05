/**
 * apps/conversor/app.js
 * Interfaz y Controlador Reactivo del Engineering Workbench v2.0
 * Datalaria Helix — Single-Source-of-Truth
 */

import { PHYSICAL_CONSTANTS, CATEGORIES } from './catalog.js';
import {
  convertLinear,
  convertTemperature,
  convertRfPower,
  convertRfWavFreq,
  formatEngineeredNumber,
  processBatchText,
  WAVELENGTH_FACTORS,
  FREQ_FACTORS
} from './engine.js';

const I18N = {
  es: {
    backToPortal: '← Datalaria',
    appTitle: 'Conversor Pro',
    appSheet: '📋 Ficha de la App',
    guidePost: '📖 Guía Técnica',
    b2bKits: '📦 Kits B2B →',
    constantsLabel: 'Constantes CODATA:',
    viewCodataTable: 'Tabla completa',
    closeCodataTable: 'Cerrar tabla',
    injectBtn: 'Inyectar',
    injectedToast: 'Inyectada constante',
    inputLabel: 'Entrada',
    outputLabel: 'Resultado',
    swapTooltip: 'Invertir unidades (Atajo: X)',
    copyTooltip: 'Copiar (Atajo: C)',
    copiedFeedback: '✓ ¡Copiado!',
    shareTooltip: 'Compartir cálculo',
    linkCopied: '✓ Enlace copiado',
    precisionLabel: 'Precisión:',
    omniTitle: 'Omni-Matrix Multi-Escala',
    formulaTraceLabel: 'Fórmula Base SI:',
    historyTitle: 'Historial Reciente',
    clearHistory: 'Limpiar',
    collapseHistory: 'Plegar',
    expandHistory: 'Desplegar',
    scratchpadInputLabel: 'Datos de Entrada (Pega columnas de Excel o números multilínea):',
    scratchpadOutputLabel: 'Datos Convertidos / Formateados:',
    scratchpadTargetFormat: 'Formato numérico objetivo:',
    formatUS: 'US: Miles con coma (,), decimal con punto (.)',
    formatEU: 'EU: Miles con punto (.), decimal con coma (,)',
    enableUnitConversion: 'Convertir también magnitud física en cada fila',
    loadSampleBtn: '⚡ Cargar lote de ejemplo (1 clic)',
    copyOutputBtn: '📋 Copiar salida',
    downloadCsvBtn: '💾 Descargar CSV',
    footerMadeWith: 'Herramienta técnica de Datalaria · Precisión metrológica SI/CODATA 2022 · Cero dependencias externas.',
    scratchpadSample: `101325\n100000\n150000\n200000\n6894.757\n250000`
  },
  en: {
    backToPortal: '← Datalaria',
    appTitle: 'Converter Pro',
    appSheet: '📋 App Overview',
    guidePost: '📖 Technical Guide',
    b2bKits: '📦 B2B Kits →',
    constantsLabel: 'CODATA Constants:',
    viewCodataTable: 'Full Table',
    closeCodataTable: 'Close Table',
    injectBtn: 'Inject',
    injectedToast: 'Injected constant',
    inputLabel: 'Input Value',
    outputLabel: 'Converted Result',
    swapTooltip: 'Swap units (Shortcut: X)',
    copyTooltip: 'Copy (Shortcut: C)',
    copiedFeedback: '✓ Copied!',
    shareTooltip: 'Share calculation',
    linkCopied: '✓ Link copied',
    precisionLabel: 'Precision:',
    omniTitle: 'Multi-Scale Omni-Matrix',
    formulaTraceLabel: 'Canonical SI Formula:',
    historyTitle: 'Recent History',
    clearHistory: 'Clear',
    collapseHistory: 'Collapse',
    expandHistory: 'Expand',
    scratchpadInputLabel: 'Input Data (Paste Excel columns or multiline numbers):',
    scratchpadOutputLabel: 'Converted & Formatted Output:',
    scratchpadTargetFormat: 'Target number format:',
    formatUS: 'US: Thousands with comma (,), decimal with dot (.)',
    formatEU: 'EU: Thousands with dot (.), decimal with comma (,)',
    enableUnitConversion: 'Also convert physical unit for each row',
    loadSampleBtn: '⚡ Load sample batch (1-click)',
    copyOutputBtn: '📋 Copy output',
    downloadCsvBtn: '💾 Download CSV',
    footerMadeWith: 'Datalaria engineering toolkit · SI/CODATA 2022 metrological rigor · Zero external dependencies.',
    scratchpadSample: `101325\n100000\n150000\n200000\n6894.757\n250000`
  }
};

const DIDACTIC_TEXTS = {
  dimension: {
    es: 'Todas las medidas lineales se normalizan al metro (m) según la definición oficial del BIPM (la distancia recorrida por la luz en el vacío en 1/299.792.458 s). Las áreas se computan en metros cuadrados (m²) y los volúmenes en metros cúbicos (m³), utilizando factores exactos para yardas, pulgadas y galones.',
    en: 'All spatial measurements are strictly normalized around the canonical meter (m) as defined by the BIPM (distance light travels in vacuum in 1/299,792,458 s). Surface areas derive to square meters (m²) and volume to cubic meters (m³), using exact legal factors for yards, feet, and gallons.'
  },
  energia: {
    es: 'El Julio (J) es la unidad base de energía del Sistema Internacional (1 J = 1 N·m = 1 W·s). La potencia se mide en Vatios (W = J/s). Para la temperatura se aplican transformaciones afines respecto al Kelvin (K).',
    en: 'The Joule (J) is the canonical SI unit for work and energy (1 J = 1 N·m = 1 W·s). Power is rated in Watts (W = J/s). Thermodynamic temperature transformations map affinely to and from the absolute Kelvin scale (K).'
  },
  tiempo: {
    es: 'El segundo (s) está definido por la frecuencia de transición hiperfina del cesio-133 (9.192.631.770 Hz). Todos los múltiplos estándar (minutos, horas, días y años julianos) se calculan con factores enteros deterministas.',
    en: 'The second (s) is fixed by the transition frequency of cesium-133 atoms (9,192,631,770 Hz). All standard intervals (minutes, hours, days, and Julian years) are computed deterministically.'
  },
  mecanica: {
    es: 'El Kilogramo (kg) es la unidad fundamental de masa fijada por la constante de Planck. El Newton (N = kg·m/s²) cuantifica la fuerza, y el Pascal (Pa = N/m²) la presión sobre superficies.',
    en: 'The Kilogram (kg) is the fundamental mass base defined via Planck’s constant. The Newton (N = kg·m/s²) quantifies force, and the Pascal (Pa = N/m²) gauges pressure across areas.'
  },
  informatica: {
    es: 'Diferenciamos estrictamente entre el estándar decimal SI (kB = 1000 B, MB = 10⁶ B) adoptado por fabricantes de discos y redes, y el estándar binario IEC 80000-13 (KiB = 1024 B, MiB = 1024² B) empleado por los sistemas operativos y memorias RAM.',
    en: 'We strictly distinguish between the decimal SI standard (kB = 1000 B, MB = 10⁶ B) used in network throughput and drive capacities, and the IEC 80000-13 binary standard (KiB = 1024 B, MiB = 1024² B) used by operating systems and memory.'
  },
  radiofrecuencia: {
    es: 'En el espectro electromagnético en el vacío, la frecuencia f y la longitud de onda λ están unidas de forma unívoca por la velocidad de la luz c: λ = c / f. La escala logarítmica dBm expresa potencia relativa a 1 milivatio: P(dBm) = 10·log₁₀(P/1mW).',
    en: 'In electromagnetic propagation through vacuum, frequency f and wavelength λ are inextricably linked by the speed of light c: λ = c / f. The logarithmic dBm metric gauges power relative to 1 milliwatt: P(dBm) = 10·log₁₀(P/1mW).'
  },
  scratchpad: {
    es: 'El Workbench Masivo permite limpiar columnas completas copiadas desde Excel o CSV. Puedes alternar el formato de separadores numéricos entre notación anglosajona (US) y europea (EU), y opcionalmente convertir unidades físicas fila por fila.',
    en: 'The Batch Workbench lets you sanitize and convert tabular columns pasted from Excel or CSV. Toggle thousands/decimal separators between US and EU notations, and optionally execute physical unit conversions row by row.'
  }
};

export class UnitConverterApp {
  constructor() {
    this.state = {
      lang: 'es',
      category: 'dimension',
      magnitude: 'length',
      fromUnit: 'm',
      toUnit: 'ft',
      inputValue: 1,
      precision: 'auto',
      // RF Special modes
      rfWavMode: 'freq_to_wav', // or 'wav_to_freq'
      rfWavFromUnit: 'mhz',
      rfWavToUnit: 'm',
      // Batch Scratchpad
      batchTargetFormat: 'eu',
      batchConvertUnits: false,
      batchUnitCategory: 'pressure',
      batchFromUnit: 'bar',
      batchToUnit: 'psi',
      history: [],
      historyCollapsed: false,
      codataTableOpen: false
    };
  }

  init() {
    this.readUrlParams();
    this.loadHistory();
    this.renderShell();
    this.renderCategoryNav();
    this.renderConstantsBar();
    this.bindEvents();
    this.updateView();
  }

  readUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const lang = params.get('lang');
    if (lang === 'en' || lang === 'es') {
      this.state.lang = lang;
    } else {
      const stored = localStorage.getItem('datalaria_lang');
      if (stored === 'en' || stored === 'es') this.state.lang = stored;
    }

    const cat = params.get('cat');
    if (cat && CATEGORIES[cat]) {
      this.state.category = cat;
      const mag = params.get('mag');
      if (mag && CATEGORIES[cat].magnitudes && CATEGORIES[cat].magnitudes[mag]) {
        this.state.magnitude = mag;
      } else if (CATEGORIES[cat].magnitudes) {
        this.state.magnitude = Object.keys(CATEGORIES[cat].magnitudes)[0];
      }
    }

    const val = params.get('val');
    if (val !== null && !isNaN(Number(val))) {
      this.state.inputValue = Number(val);
    }

    const from = params.get('from');
    const to = params.get('to');
    if (from) this.state.fromUnit = from;
    if (to) this.state.toUnit = to;

    const prec = params.get('prec');
    if (prec) this.state.precision = prec;
  }

  syncUrlParams() {
    const params = new URLSearchParams();
    params.set('lang', this.state.lang);
    params.set('cat', this.state.category);
    if (this.state.category !== 'scratchpad') {
      params.set('mag', this.state.magnitude);
      params.set('val', this.state.inputValue);
      params.set('from', this.state.fromUnit);
      params.set('to', this.state.toUnit);
      if (this.state.precision !== 'auto') {
        params.set('prec', this.state.precision);
      }
    }
    const newUrl = `${window.location.pathname}?${params.toString()}`;
    window.history.replaceState({}, '', newUrl);
  }

  setLanguage(lang) {
    if (this.state.lang === lang) return;
    this.state.lang = lang;
    localStorage.setItem('datalaria_lang', lang);
    this.renderShell();
    this.renderCategoryNav();
    this.renderConstantsBar();
    this.updateView();
    this.syncUrlParams();
  }

  renderShell() {
    const t = I18N[this.state.lang];
    const portalUrl = this.state.lang === 'en' ? '/en/apps/' : '/es/apps/';
    const appSheetUrl = this.state.lang === 'en' ? '/en/apps/conversor/' : '/es/apps/conversor/';
    const postUrl = this.state.lang === 'en' ? '/en/posts/app_unit_converter/' : '/es/posts/app_conversor_unidades/';
    const resourcesUrl = this.state.lang === 'en' ? '/en/resources/' : '/es/recursos/';

    const headerEl = document.getElementById('app-header');
    if (!headerEl) return;

    headerEl.innerHTML = `
      <div class="header-left">
        <a href="${portalUrl}" class="back-link" title="${t.backToPortal}">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 18l-6-6 6-6"/></svg>
          <span>Datalaria</span>
        </a>
        <div class="app-title-badge">
          <span>${t.appTitle}</span>
          <span class="version-chip">v2.0.0</span>
        </div>
      </div>
      <div class="header-right">
        <div class="lang-switch">
          <button class="lang-btn ${this.state.lang === 'es' ? 'active' : ''}" data-lang="es">ES</button>
          <button class="lang-btn ${this.state.lang === 'en' ? 'active' : ''}" data-lang="en">EN</button>
        </div>
        <a href="${appSheetUrl}" class="btn-ghost" title="${t.appSheet}">
          <span>${t.appSheet}</span>
        </a>
        <a href="${postUrl}" class="btn-ghost" title="${t.guidePost}">
          <span>${t.guidePost}</span>
        </a>
        <a href="${resourcesUrl}" class="btn-b2b" title="${t.b2bKits}">
          <span>${t.b2bKits}</span>
        </a>
      </div>
    `;

    headerEl.querySelectorAll('.lang-btn').forEach(btn => {
      btn.addEventListener('click', () => this.setLanguage(btn.dataset.lang));
    });
  }

  renderCategoryNav() {
    const navEl = document.getElementById('categories-nav');
    if (!navEl) return;
    const lang = this.state.lang;

    navEl.innerHTML = Object.values(CATEGORIES).map(cat => {
      const isActive = this.state.category === cat.id;
      const isScratchpad = cat.id === 'scratchpad';
      return `
        <button class="category-pill ${isActive ? 'active' : ''} ${isScratchpad ? 'scratchpad-pill' : ''}" data-cat="${cat.id}">
          <span>${cat.icon}</span>
          <span>${cat.title[lang]}</span>
        </button>
      `;
    }).join('');

    navEl.querySelectorAll('.category-pill').forEach(btn => {
      btn.addEventListener('click', () => {
        this.selectCategory(btn.dataset.cat);
      });
    });
  }

  renderConstantsBar() {
    const barEl = document.getElementById('constants-bar');
    if (!barEl) return;
    const t = I18N[this.state.lang];
    const lang = this.state.lang;
    const isOpen = this.state.codataTableOpen;

    barEl.innerHTML = `
      <div class="constants-header">
        <div class="constants-title-group">
          <span class="constants-badge">CODATA</span>
          <span class="constants-label">${t.constantsLabel}</span>
        </div>
        <div class="constants-chips-deck">
          ${PHYSICAL_CONSTANTS.map(c => `
            <button class="constant-micro-chip" data-val="${c.value}" data-symbol="${c.symbol}" data-unit="${c.unit}" title="${c.name[lang]}: ${formatEngineeredNumber(c.value, 'sci', lang)} ${c.unit} (${t.injectBtn})">
              <span class="chip-symbol">${c.symbol}</span>
            </button>
          `).join('')}
        </div>
        <button id="btn-toggle-codata-table" class="btn-codata-toggle ${isOpen ? 'active' : ''}" aria-expanded="${isOpen}">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
          <span>${isOpen ? t.closeCodataTable : t.viewCodataTable}</span>
          <span class="codata-toggle-arrow">${isOpen ? '▲' : '▼'}</span>
        </button>
      </div>

      <div id="codata-table-panel" class="codata-table-panel" style="${isOpen ? 'display: block;' : 'display: none;'}">
        <div class="codata-table-grid">
          ${PHYSICAL_CONSTANTS.map(c => `
            <div class="codata-card-row">
              <div class="codata-card-sym-badge">${c.symbol}</div>
              <div class="codata-card-body">
                <div class="codata-card-title">${c.name[lang]}</div>
                <div class="codata-card-val">${formatEngineeredNumber(c.value, 'sci', lang)} <span class="codata-card-unit">${c.unit}</span></div>
              </div>
              <button class="btn-codata-inject" data-val="${c.value}" data-symbol="${c.symbol}" data-unit="${c.unit}" title="${t.injectBtn}">
                ${t.injectBtn}
              </button>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    barEl.querySelectorAll('.constant-micro-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const val = Number(chip.dataset.val);
        const sym = chip.dataset.symbol;
        const unit = chip.dataset.unit || '';
        this.injectConstantValue(val, sym, unit);
      });
    });

    barEl.querySelectorAll('.btn-codata-inject').forEach(btn => {
      btn.addEventListener('click', () => {
        const val = Number(btn.dataset.val);
        const sym = btn.dataset.symbol;
        const unit = btn.dataset.unit || '';
        this.injectConstantValue(val, sym, unit);
      });
    });

    const toggleBtn = barEl.querySelector('#btn-toggle-codata-table');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        this.state.codataTableOpen = !this.state.codataTableOpen;
        this.renderConstantsBar();
      });
    }
  }

  injectConstantValue(val, sym, unit = '') {
    const t = I18N[this.state.lang];
    this.state.inputValue = val;
    const inputEl = document.getElementById('main-unit-input');
    if (inputEl) {
      inputEl.value = val;
      inputEl.focus();
    }
    this.calculateAndRender();
    this.syncUrlParams();
    this.showToast(`${t.injectedToast}: ${sym} = ${formatEngineeredNumber(val, 'sci', this.state.lang)} ${unit}`);
  }

  showToast(msg) {
    let toast = document.getElementById('workbench-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'workbench-toast';
      toast.className = 'workbench-toast';
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.classList.add('show');
    if (this._toastTimer) clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => {
      toast.classList.remove('show');
    }, 2200);
  }

  selectCategory(catId) {
    if (this.state.category === catId) return;
    this.state.category = catId;
    const cat = CATEGORIES[catId];
    if (cat.magnitudes) {
      this.state.magnitude = Object.keys(cat.magnitudes)[0];
      const mag = cat.magnitudes[this.state.magnitude];
      if (mag.units) {
        this.state.fromUnit = mag.defaultFrom || Object.keys(mag.units)[0];
        this.state.toUnit = mag.defaultTo || Object.keys(mag.units)[1] || Object.keys(mag.units)[0];
      }
    }
    this.renderCategoryNav();
    this.updateView();
    this.syncUrlParams();
  }

  selectMagnitude(magId) {
    if (this.state.magnitude === magId) return;
    this.state.magnitude = magId;
    const cat = CATEGORIES[this.state.category];
    const mag = cat.magnitudes[magId];
    if (mag.units) {
      this.state.fromUnit = mag.defaultFrom || Object.keys(mag.units)[0];
      this.state.toUnit = mag.defaultTo || Object.keys(mag.units)[1] || Object.keys(mag.units)[0];
    }
    this.updateView();
    this.syncUrlParams();
  }

  updateView() {
    const mainCard = document.getElementById('main-converter-card');
    const scratchpadCard = document.getElementById('scratchpad-card');
    const didacticCard = document.getElementById('didactic-card');

    if (this.state.category === 'scratchpad') {
      if (mainCard) mainCard.style.display = 'none';
      if (scratchpadCard) scratchpadCard.style.display = 'block';
      this.renderScratchpad();
    } else {
      if (scratchpadCard) scratchpadCard.style.display = 'none';
      if (mainCard) mainCard.style.display = 'block';
      this.renderConverterCard();
    }

    if (didacticCard) {
      const lang = this.state.lang;
      const text = DIDACTIC_TEXTS[this.state.category] ? DIDACTIC_TEXTS[this.state.category][lang] : '';
      didacticCard.innerHTML = `
        <h3 class="didactic-title">${CATEGORIES[this.state.category].icon} ${CATEGORIES[this.state.category].title[lang]}</h3>
        <p class="didactic-content">${text}</p>
      `;
    }

    this.renderHistory();
  }

  renderConverterCard() {
    const cardEl = document.getElementById('main-converter-card');
    if (!cardEl) return;
    const t = I18N[this.state.lang];
    const lang = this.state.lang;
    const cat = CATEGORIES[this.state.category];
    const mag = cat.magnitudes[this.state.magnitude];

    // Subcategories pill selector
    const subcats = Object.values(cat.magnitudes);
    const subcatsHtml = subcats.length > 1 ? `
      <div class="subcat-selector">
        ${subcats.map(s => `
          <button class="subcat-btn ${s.id === this.state.magnitude ? 'active' : ''}" data-mag="${s.id}">
            ${s.title[lang]}
          </button>
        `).join('')}
      </div>
    ` : `<div></div>`;

    let cockpitHtml = '';

    if (mag.isSpecialRfWav) {
      cockpitHtml = this.getRfWavCockpitHtml(t, lang);
    } else {
      cockpitHtml = this.getStandardCockpitHtml(mag, t, lang);
    }

    cardEl.innerHTML = `
      <div class="card-topbar">
        ${subcatsHtml}
        <div class="card-controls">
          <div class="precision-control">
            <span>${t.precisionLabel}</span>
            <select id="precision-select" class="select-compact">
              <option value="auto" ${this.state.precision === 'auto' ? 'selected' : ''}>Auto</option>
              <option value="2" ${this.state.precision === '2' ? 'selected' : ''}>2 dec</option>
              <option value="4" ${this.state.precision === '4' ? 'selected' : ''}>4 dec</option>
              <option value="6" ${this.state.precision === '6' ? 'selected' : ''}>6 dec</option>
              <option value="8" ${this.state.precision === '8' ? 'selected' : ''}>8 dec</option>
              <option value="sci" ${this.state.precision === 'sci' ? 'selected' : ''}>Sci (×10ⁿ)</option>
            </select>
          </div>
          <button id="btn-share" class="btn-action" title="${t.shareTooltip}">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
            <span>URL</span>
          </button>
        </div>
      </div>

      ${cockpitHtml}

      <div class="action-strip">
        <div class="action-buttons">
          <button id="btn-copy-result" class="btn-action" title="${t.copyTooltip}">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            <span id="copy-btn-text">${t.copyTooltip}</span>
          </button>
        </div>
        <div id="formula-trace-container" class="formula-trace">
          <!-- Live formula will populate here -->
        </div>
      </div>

      <div id="omni-matrix-container" class="omni-matrix-panel">
        <!-- Omni matrix will populate here -->
      </div>
    `;

    // Bind subcategory click
    cardEl.querySelectorAll('.subcat-btn').forEach(btn => {
      btn.addEventListener('click', () => this.selectMagnitude(btn.dataset.mag));
    });

    // Precision select
    const precSelect = cardEl.querySelector('#precision-select');
    if (precSelect) {
      precSelect.addEventListener('change', (e) => {
        this.state.precision = e.target.value;
        this.calculateAndRender();
        this.syncUrlParams();
      });
    }

    // Share button
    const shareBtn = cardEl.querySelector('#btn-share');
    if (shareBtn) {
      shareBtn.addEventListener('click', () => {
        this.syncUrlParams();
        navigator.clipboard.writeText(window.location.href).then(() => {
          shareBtn.innerHTML = `<span>${t.linkCopied}</span>`;
          setTimeout(() => {
            shareBtn.innerHTML = `
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
              <span>URL</span>
            `;
          }, 1800);
        });
      });
    }

    // Copy result button
    const copyBtn = cardEl.querySelector('#btn-copy-result');
    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        const outEl = document.getElementById('main-unit-output');
        if (outEl) {
          const text = outEl.textContent.trim();
          navigator.clipboard.writeText(text).then(() => {
            copyBtn.classList.add('copied');
            const btnText = cardEl.querySelector('#copy-btn-text');
            if (btnText) btnText.textContent = t.copiedFeedback;
            setTimeout(() => {
              copyBtn.classList.remove('copied');
              if (btnText) btnText.textContent = t.copyTooltip;
            }, 1800);
          });
        }
      });
    }

    this.bindConverterInputs();
    this.calculateAndRender();
  }

  getStandardCockpitHtml(mag, t, lang) {
    const units = Object.values(mag.units);
    return `
      <div class="cockpit-grid">
        <div class="unit-cell">
          <label class="cell-label" for="main-unit-input">
            <span>${t.inputLabel}</span>
          </label>
          <input type="number" id="main-unit-input" class="unit-input" value="${this.state.inputValue}" step="any">
          <select id="main-from-unit-select" class="unit-select">
            ${units.map(u => `<option value="${u.id}" ${u.id === this.state.fromUnit ? 'selected' : ''}>${u.name[lang]}</option>`).join('')}
          </select>
        </div>

        <div class="swap-btn-container">
          <button id="btn-swap-units" class="btn-swap" title="${t.swapTooltip}">
            ⇄
          </button>
        </div>

        <div class="unit-cell">
          <span class="cell-label">
            <span>${t.outputLabel}</span>
          </span>
          <div id="main-unit-output" class="unit-output">--</div>
          <select id="main-to-unit-select" class="unit-select">
            ${units.map(u => `<option value="${u.id}" ${u.id === this.state.toUnit ? 'selected' : ''}>${u.name[lang]}</option>`).join('')}
          </select>
        </div>
      </div>
    `;
  }

  getRfWavCockpitHtml(t, lang) {
    const isFreqToWav = this.state.rfWavMode === 'freq_to_wav';
    const freqUnits = Object.keys(FREQ_FACTORS);
    const wavUnits = Object.keys(WAVELENGTH_FACTORS);

    return `
      <div class="cockpit-grid">
        <div class="unit-cell">
          <label class="cell-label" for="main-unit-input">
            <span>${isFreqToWav ? 'Frecuencia (f)' : 'Longitud de Onda (λ)'}</span>
          </label>
          <input type="number" id="main-unit-input" class="unit-input" value="${this.state.inputValue}" step="any">
          <select id="rf-from-select" class="unit-select">
            ${(isFreqToWav ? freqUnits : wavUnits).map(u => `
              <option value="${u}" ${u === (isFreqToWav ? this.state.rfWavFromUnit : this.state.rfWavToUnit) ? 'selected' : ''}>${u.toUpperCase()}</option>
            `).join('')}
          </select>
        </div>

        <div class="swap-btn-container">
          <button id="btn-swap-rf-wav" class="btn-swap" title="${t.swapTooltip}">
            ⇄
          </button>
        </div>

        <div class="unit-cell">
          <span class="cell-label">
            <span>${isFreqToWav ? 'Longitud de Onda (λ = c/f)' : 'Frecuencia (f = c/λ)'}</span>
          </span>
          <div id="main-unit-output" class="unit-output">--</div>
          <select id="rf-to-select" class="unit-select">
            ${(isFreqToWav ? wavUnits : freqUnits).map(u => `
              <option value="${u}" ${u === (isFreqToWav ? this.state.rfWavToUnit : this.state.rfWavFromUnit) ? 'selected' : ''}>${u.toUpperCase()}</option>
            `).join('')}
          </select>
        </div>
      </div>
    `;
  }

  bindConverterInputs() {
    const inputEl = document.getElementById('main-unit-input');
    const fromSelect = document.getElementById('main-from-unit-select');
    const toSelect = document.getElementById('main-to-unit-select');
    const swapBtn = document.getElementById('btn-swap-units');

    if (inputEl) {
      inputEl.addEventListener('input', (e) => {
        this.state.inputValue = Number(e.target.value);
        this.calculateAndRender();
        this.syncUrlParams();
      });
    }

    if (fromSelect) {
      fromSelect.addEventListener('change', (e) => {
        this.state.fromUnit = e.target.value;
        this.calculateAndRender();
        this.syncUrlParams();
      });
    }

    if (toSelect) {
      toSelect.addEventListener('change', (e) => {
        this.state.toUnit = e.target.value;
        this.calculateAndRender();
        this.syncUrlParams();
      });
    }

    if (swapBtn) {
      swapBtn.addEventListener('click', () => {
        const temp = this.state.fromUnit;
        this.state.fromUnit = this.state.toUnit;
        this.state.toUnit = temp;
        if (fromSelect) fromSelect.value = this.state.fromUnit;
        if (toSelect) toSelect.value = this.state.toUnit;
        this.calculateAndRender();
        this.syncUrlParams();
      });
    }

    // Special RF λ-f binding
    const rfSwapBtn = document.getElementById('btn-swap-rf-wav');
    const rfFromSelect = document.getElementById('rf-from-select');
    const rfToSelect = document.getElementById('rf-to-select');

    if (rfSwapBtn) {
      rfSwapBtn.addEventListener('click', () => {
        this.state.rfWavMode = this.state.rfWavMode === 'freq_to_wav' ? 'wav_to_freq' : 'freq_to_wav';
        this.renderConverterCard();
      });
    }

    if (rfFromSelect) {
      rfFromSelect.addEventListener('change', (e) => {
        if (this.state.rfWavMode === 'freq_to_wav') this.state.rfWavFromUnit = e.target.value;
        else this.state.rfWavToUnit = e.target.value;
        this.calculateAndRender();
      });
    }

    if (rfToSelect) {
      rfToSelect.addEventListener('change', (e) => {
        if (this.state.rfWavMode === 'freq_to_wav') this.state.rfWavToUnit = e.target.value;
        else this.state.rfWavFromUnit = e.target.value;
        this.calculateAndRender();
      });
    }
  }

  calculateAndRender() {
    const outputEl = document.getElementById('main-unit-output');
    const traceEl = document.getElementById('formula-trace-container');
    const omniEl = document.getElementById('omni-matrix-container');
    if (!outputEl) return;

    const cat = CATEGORIES[this.state.category];
    const mag = cat.magnitudes[this.state.magnitude];
    const val = this.state.inputValue;
    const lang = this.state.lang;
    let result = NaN;
    let traceText = '';

    if (mag.isSpecialRfWav) {
      const mode = this.state.rfWavMode;
      const fromU = mode === 'freq_to_wav' ? this.state.rfWavFromUnit : this.state.rfWavToUnit;
      const toU = mode === 'freq_to_wav' ? this.state.rfWavToUnit : this.state.rfWavFromUnit;
      result = convertRfWavFreq(val, mode, fromU, toU);
      traceText = mode === 'freq_to_wav' ?
        `λ = c / f = 299.792.458 m/s ÷ (${val} ${fromU.toUpperCase()})` :
        `f = c / λ = 299.792.458 m/s ÷ (${val} ${fromU.toUpperCase()})`;
    } else if (mag.isSpecialRfPower) {
      result = convertRfPower(val, this.state.fromUnit, this.state.toUnit);
      traceText = `dBm ⇔ W/mW: P(mW) = 10^(dBm / 10)`;
    } else if (mag.isNonLinear && mag.id === 'temperature') {
      result = convertTemperature(val, this.state.fromUnit, this.state.toUnit);
      traceText = `T(${this.state.toUnit.toUpperCase()}) = escala(${this.state.fromUnit.toUpperCase()} ➔ K ➔ ${this.state.toUnit.toUpperCase()})`;
    } else {
      result = convertLinear(val, this.state.fromUnit, this.state.toUnit, mag.units);
      const fromU = mag.units[this.state.fromUnit];
      const toU = mag.units[this.state.toUnit];
      if (fromU && toU) {
        traceText = `${val} × ${fromU.factor} ${mag.baseUnit} ÷ ${toU.factor} = ${toU.symbol}`;
      }
    }

    const formatted = formatEngineeredNumber(result, this.state.precision, lang);
    outputEl.textContent = formatted;

    if (traceEl) {
      traceEl.innerHTML = `<strong>${I18N[lang].formulaTraceLabel}</strong> <span>${traceText}</span>`;
    }

    // Omni Matrix rendering
    if (omniEl && mag.units && !mag.isSpecialRfWav) {
      this.renderOmniMatrix(omniEl, val, mag, lang);
    } else if (omniEl) {
      omniEl.innerHTML = '';
    }

    // Save calculation to history
    this.saveCalculationToHistory(val, this.state.fromUnit, result, this.state.toUnit, mag);
  }

  renderOmniMatrix(container, val, mag, lang) {
    const t = I18N[lang];
    const allUnits = Object.values(mag.units);
    // Take 4 representative units different from current from/to
    const otherUnits = allUnits.filter(u => u.id !== this.state.fromUnit && u.id !== this.state.toUnit).slice(0, 4);

    if (otherUnits.length === 0) {
      container.innerHTML = '';
      return;
    }

    const cardsHtml = otherUnits.map(u => {
      let r = NaN;
      if (mag.isNonLinear && mag.id === 'temperature') {
        r = convertTemperature(val, this.state.fromUnit, u.id);
      } else if (mag.isSpecialRfPower) {
        r = convertRfPower(val, this.state.fromUnit, u.id);
      } else {
        r = convertLinear(val, this.state.fromUnit, u.id, mag.units);
      }
      return `
        <div class="omni-item">
          <span class="omni-item-label">${u.name[lang]}</span>
          <span class="omni-item-val">${formatEngineeredNumber(r, this.state.precision, lang)}</span>
        </div>
      `;
    }).join('');

    container.innerHTML = `
      <div class="omni-title">
        <span>${t.omniTitle}</span>
        <span>Equivalencias Simultáneas</span>
      </div>
      <div class="omni-grid">
        ${cardsHtml}
      </div>
    `;
  }

  renderScratchpad() {
    const cardEl = document.getElementById('scratchpad-card');
    if (!cardEl) return;
    const t = I18N[this.state.lang];
    const lang = this.state.lang;

    // Build categories options for optional batch unit conversion
    const availableCategories = Object.values(CATEGORIES).filter(c => c.magnitudes);

    cardEl.innerHTML = `
      <div class="converter-card">
        <h2 class="didactic-title" style="margin-bottom: 1rem;">📋 ${CATEGORIES.scratchpad.title[lang]}</h2>
        <div class="scratchpad-toolbar" style="margin-bottom: 1rem;">
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <label style="font-size:0.8rem; color:var(--text-secondary);">${t.scratchpadTargetFormat}</label>
            <select id="batch-format-select" class="select-compact">
              <option value="eu" ${this.state.batchTargetFormat === 'eu' ? 'selected' : ''}>EU (1.234,56)</option>
              <option value="us" ${this.state.batchTargetFormat === 'us' ? 'selected' : ''}>US (1,234.56)</option>
            </select>
          </div>

          <div style="display:flex; align-items:center; gap:0.5rem;">
            <input type="checkbox" id="batch-unit-toggle" ${this.state.batchConvertUnits ? 'checked' : ''}>
            <label for="batch-unit-toggle" style="font-size:0.8rem; color:var(--text-secondary); cursor:pointer;">
              ${t.enableUnitConversion}
            </label>
          </div>

          <button id="btn-batch-sample" class="btn-action">
            ${t.loadSampleBtn}
          </button>
        </div>

        <div id="batch-unit-selector-row" style="display: ${this.state.batchConvertUnits ? 'flex' : 'none'}; gap: 0.5rem; margin-bottom: 1rem; flex-wrap: wrap; background: var(--bg-canvas); padding: 0.75rem; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
          <select id="batch-category-select" class="select-compact">
            <option value="pressure">Presión (Mecánica)</option>
            <option value="length">Longitud (Dimensión)</option>
            <option value="mass">Masa (Mecánica)</option>
            <option value="energy">Energía</option>
            <option value="power">Potencia</option>
            <option value="storage_binary">Almacenamiento (IEC)</option>
          </select>
          <span style="font-size:0.8rem; color:var(--text-muted); align-self:center;">de</span>
          <select id="batch-from-select" class="select-compact"></select>
          <span style="font-size:0.8rem; color:var(--text-muted); align-self:center;">a</span>
          <select id="batch-to-select" class="select-compact"></select>
        </div>

        <div class="scratchpad-view">
          <div class="scratchpad-panel">
            <label class="cell-label" for="batch-input">${t.scratchpadInputLabel}</label>
            <textarea id="batch-input" class="scratchpad-textarea" placeholder="Pega números aquí, uno por línea..."></textarea>
          </div>
          <div class="scratchpad-panel">
            <label class="cell-label" for="batch-output">${t.scratchpadOutputLabel}</label>
            <textarea id="batch-output" class="scratchpad-textarea" readonly></textarea>
          </div>
        </div>

        <div class="scratchpad-toolbar" style="margin-top: 1rem;">
          <div style="font-size:0.8rem; color:var(--text-muted);" id="batch-status-text">0 líneas procesadas</div>
          <div style="display:flex; gap:0.5rem;">
            <button id="btn-batch-copy" class="btn-action">${t.copyOutputBtn}</button>
            <button id="btn-batch-csv" class="btn-action">${t.downloadCsvBtn}</button>
          </div>
        </div>
      </div>
    `;

    this.bindScratchpadEvents();
  }

  bindScratchpadEvents() {
    const inputEl = document.getElementById('batch-input');
    const outputEl = document.getElementById('batch-output');
    const formatSelect = document.getElementById('batch-format-select');
    const unitToggle = document.getElementById('batch-unit-toggle');
    const sampleBtn = document.getElementById('btn-batch-sample');
    const copyBtn = document.getElementById('btn-batch-copy');
    const csvBtn = document.getElementById('btn-batch-csv');
    const statusText = document.getElementById('batch-status-text');

    const updateBatch = () => {
      if (!inputEl || !outputEl) return;
      const text = inputEl.value;
      const res = processBatchText(text, {
        targetFormat: this.state.batchTargetFormat,
        convertUnits: this.state.batchConvertUnits,
        unitCategory: this.state.batchUnitCategory,
        fromUnit: this.state.batchFromUnit,
        toUnit: this.state.batchToUnit,
        precision: this.state.precision,
        categoriesCatalog: this.getFlattenedCatalog()
      });
      outputEl.value = res.output;
      if (statusText) {
        statusText.textContent = `${res.count} líneas procesadas (${res.errors} errores)`;
      }
    };

    if (inputEl) inputEl.addEventListener('input', updateBatch);

    if (formatSelect) {
      formatSelect.addEventListener('change', (e) => {
        this.state.batchTargetFormat = e.target.value;
        updateBatch();
      });
    }

    if (unitToggle) {
      unitToggle.addEventListener('change', (e) => {
        this.state.batchConvertUnits = e.target.checked;
        const row = document.getElementById('batch-unit-selector-row');
        if (row) row.style.display = e.target.checked ? 'flex' : 'none';
        this.populateBatchUnits();
        updateBatch();
      });
    }

    if (sampleBtn) {
      sampleBtn.addEventListener('click', () => {
        if (inputEl) {
          inputEl.value = I18N[this.state.lang].scratchpadSample;
          updateBatch();
        }
      });
    }

    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        if (outputEl && outputEl.value) {
          navigator.clipboard.writeText(outputEl.value).then(() => {
            copyBtn.textContent = I18N[this.state.lang].copiedFeedback;
            setTimeout(() => { copyBtn.textContent = I18N[this.state.lang].copyOutputBtn; }, 1800);
          });
        }
      });
    }

    if (csvBtn) {
      csvBtn.addEventListener('click', () => {
        if (outputEl && outputEl.value) {
          const blob = new Blob([outputEl.value], { type: 'text/csv;charset=utf-8;' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `datalaria_conversor_lote_${Date.now()}.csv`;
          a.click();
          URL.revokeObjectURL(url);
        }
      });
    }

    this.populateBatchUnits();
  }

  getFlattenedCatalog() {
    const flat = {};
    Object.values(CATEGORIES).forEach(c => {
      if (c.magnitudes) {
        Object.entries(c.magnitudes).forEach(([magKey, magObj]) => {
          flat[magKey] = magObj;
        });
      }
    });
    return flat;
  }

  populateBatchUnits() {
    const catSelect = document.getElementById('batch-category-select');
    const fromSelect = document.getElementById('batch-from-select');
    const toSelect = document.getElementById('batch-to-select');
    if (!catSelect || !fromSelect || !toSelect) return;

    const flat = this.getFlattenedCatalog();
    const currentMag = flat[this.state.batchUnitCategory];
    if (!currentMag || !currentMag.units) return;

    const units = Object.values(currentMag.units);
    const lang = this.state.lang;

    fromSelect.innerHTML = units.map(u => `<option value="${u.id}" ${u.id === this.state.batchFromUnit ? 'selected' : ''}>${u.name[lang]}</option>`).join('');
    toSelect.innerHTML = units.map(u => `<option value="${u.id}" ${u.id === this.state.batchToUnit ? 'selected' : ''}>${u.name[lang]}</option>`).join('');

    catSelect.value = this.state.batchUnitCategory;

    catSelect.onchange = (e) => {
      this.state.batchUnitCategory = e.target.value;
      const m = flat[e.target.value];
      if (m && m.units) {
        const uKeys = Object.keys(m.units);
        this.state.batchFromUnit = uKeys[0];
        this.state.batchToUnit = uKeys[1] || uKeys[0];
      }
      this.populateBatchUnits();
      const inEl = document.getElementById('batch-input');
      if (inEl) inEl.dispatchEvent(new Event('input'));
    };

    fromSelect.onchange = (e) => {
      this.state.batchFromUnit = e.target.value;
      const inEl = document.getElementById('batch-input');
      if (inEl) inEl.dispatchEvent(new Event('input'));
    };

    toSelect.onchange = (e) => {
      this.state.batchToUnit = e.target.value;
      const inEl = document.getElementById('batch-input');
      if (inEl) inEl.dispatchEvent(new Event('input'));
    };
  }

  saveCalculationToHistory(fromVal, fromUnit, toVal, toUnit, mag) {
    if (isNaN(toVal) || !isFinite(toVal)) return;
    const item = {
      fromVal,
      fromUnit,
      toVal: formatEngineeredNumber(toVal, 'auto', this.state.lang),
      toUnit,
      category: this.state.category,
      magnitude: this.state.magnitude,
      time: Date.now()
    };
    // Keep max 8 unique items
    const filtered = this.state.history.filter(h => !(h.fromUnit === fromUnit && h.toUnit === toUnit && h.fromVal === fromVal));
    filtered.unshift(item);
    this.state.history = filtered.slice(0, 8);
    localStorage.setItem('datalaria_conversor_hist', JSON.stringify(this.state.history));
    this.renderHistory();
  }

  loadHistory() {
    try {
      const data = localStorage.getItem('datalaria_conversor_hist');
      if (data) this.state.history = JSON.parse(data);
    } catch {
      this.state.history = [];
    }
  }

  renderHistory() {
    const stripEl = document.getElementById('history-strip');
    if (!stripEl) return;
    const t = I18N[this.state.lang];
    const lang = this.state.lang;

    if (this.state.history.length === 0) {
      stripEl.style.display = 'none';
      return;
    }

    stripEl.style.display = 'flex';
    const isCollapsed = this.state.historyCollapsed;

    stripEl.innerHTML = `
      <div class="history-header">
        <div class="history-title-group">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <span class="history-title">${t.historyTitle}</span>
          <span class="history-badge">${this.state.history.length}</span>
        </div>
        <div class="history-actions">
          <button id="btn-toggle-history" class="btn-history-toggle" title="${isCollapsed ? t.expandHistory : t.collapseHistory}">
            <span class="history-toggle-arrow">${isCollapsed ? '▶' : '▼'}</span>
            <span>${isCollapsed ? t.expandHistory : t.collapseHistory}</span>
          </button>
          <button id="btn-clear-history" class="btn-history-clear" title="${t.clearHistory}">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
            <span>${t.clearHistory}</span>
          </button>
        </div>
      </div>
      <div id="history-items-container" class="history-items-grid" style="${isCollapsed ? 'display: none;' : 'display: flex;'}">
        ${this.state.history.map((h, i) => `
          <button class="history-pill-card" data-idx="${i}" title="${h.fromVal} ${h.fromUnit} = ${h.toVal} ${h.toUnit}">
            <span class="hist-from">${h.fromVal} <small class="hist-unit">${h.fromUnit}</small></span>
            <span class="hist-arrow">➔</span>
            <span class="hist-to">${h.toVal} <small class="hist-unit">${h.toUnit}</small></span>
          </button>
        `).join('')}
      </div>
    `;

    const clearBtn = stripEl.querySelector('#btn-clear-history');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        this.state.history = [];
        localStorage.removeItem('datalaria_conversor_hist');
        this.renderHistory();
        this.showToast('✓ ' + (lang === 'es' ? 'Historial limpiado' : 'History cleared'));
      });
    }

    const toggleBtn = stripEl.querySelector('#btn-toggle-history');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        this.state.historyCollapsed = !this.state.historyCollapsed;
        this.renderHistory();
      });
    }

    stripEl.querySelectorAll('.history-pill-card').forEach(btn => {
      btn.addEventListener('click', () => {
        const item = this.state.history[Number(btn.dataset.idx)];
        if (item) {
          this.state.category = item.category;
          this.state.magnitude = item.magnitude;
          this.state.fromUnit = item.fromUnit;
          this.state.toUnit = item.toUnit;
          this.state.inputValue = item.fromVal;
          this.renderCategoryNav();
          this.updateView();
          this.syncUrlParams();
          this.showToast(`✓ ${item.fromVal} ${item.fromUnit} ➔ ${item.toVal} ${item.toUnit}`);
        }
      });
    });
  }

  bindEvents() {
    // Keyboard shortcuts
    window.addEventListener('keydown', (e) => {
      // Don't trigger if typing in textarea or input
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      if (e.key === 'x' || e.key === 'X') {
        const swapBtn = document.getElementById('btn-swap-units') || document.getElementById('btn-swap-rf-wav');
        if (swapBtn) swapBtn.click();
      } else if (e.key === 'c' || e.key === 'C') {
        const copyBtn = document.getElementById('btn-copy-result');
        if (copyBtn) copyBtn.click();
      }
    });
  }
}
