// apps/obs-management/web/app.js
// Controlador Executive Risk Cockpit v2.0 (Zero-CDN, Cero innerHTML, Modern Web Guidance).
import { CHECKOUT_URLS, I18N, PORTAL_ROUTES, formatEur, formatInt, interpolate } from './i18n.js';
import {
  PRESET_SCENARIOS,
  SAMPLE_BOM_CSV,
  cloneCatalog,
  computeLtbVsFff,
  evaluateCatalogRisk,
  extractMpnFromPdnText,
  parseBomCsv,
  traverseBomUpward,
} from './engine.js';

const SVG_NS = 'http://www.w3.org/2000/svg';
const collator = new Intl.Collator(undefined, { numeric: true, sensitivity: 'base' });
const prefersReducedMotion = () => window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const state = {
  lang: 'es',
  theme: 'dark',
  view: 'cockpit',
  scenarioId: 'drone-capacitor',
  isLive: false,
  catalog: cloneCatalog(PRESET_SCENARIOS['drone-capacitor'].catalog),
  metrics: null,
  focusMpn: PRESET_SCENARIOS['drone-capacitor'].focusMpn,
  logFilter: 'ALL',
  sortCol: 2,
  sortDir: 'descending',
  timers: [],
};

function t(key, vars) {
  const dict = I18N[state.lang] || I18N.es;
  const raw = dict[key] ?? I18N.es[key] ?? key;
  return vars ? interpolate(raw, vars) : raw;
}

function trackEvent(eventName, params = {}) {
  const payload = { ...params, app_slug: 'obs-management', language: state.lang, transport_type: 'beacon' };
  try {
    if (typeof window.gtag === 'function') window.gtag('event', eventName, payload);
    if (Array.isArray(window.dataLayer)) window.dataLayer.push({ event: eventName, ...payload });
  } catch { /* non-blocking */ }
}

function detectInitialLang() {
  const sp = new URLSearchParams(window.location.search);
  const q = (sp.get('lang') || '').toLowerCase();
  if (q === 'es' || q === 'en') return q;
  try {
    const saved = localStorage.getItem('obs_radar_lang');
    if (saved === 'es' || saved === 'en') return saved;
  } catch { /* storage restricted */ }
  if (document.referrer && /\/en(\/|$)/i.test(document.referrer)) return 'en';
  return (navigator.language || '').toLowerCase().startsWith('es') ? 'es' : 'en';
}

function detectInitialTheme() {
  try {
    const saved = localStorage.getItem('obs_radar_theme');
    if (saved === 'dark' || saved === 'light') return saved;
  } catch { /* ignore */ }
  return 'dark';
}

function syncUrlParams() {
  try {
    const u = new URL(window.location.href);
    u.searchParams.set('lang', state.lang);
    u.searchParams.set('view', state.view);
    u.searchParams.set('scenario', state.scenarioId);
    window.history.replaceState({}, '', u.toString());
  } catch { /* ignore */ }
}

function applyTheme() {
  document.documentElement.setAttribute('data-theme', state.theme);
  const metaScheme = document.querySelector('meta[name="color-scheme"]');
  if (metaScheme) metaScheme.setAttribute('content', state.theme);
  try { localStorage.setItem('obs_radar_theme', state.theme); } catch { /* ignore */ }
}

function applyTranslations() {
  document.documentElement.lang = state.lang;
  document.title = t('pageTitle');
  const routes = PORTAL_ROUTES[state.lang] || PORTAL_ROUTES.es;

  document.getElementById('linkBackCatalog').href = routes.appsCatalog;
  document.getElementById('linkTechSheet').href = routes.appSheet;
  document.getElementById('linkSeries').href = routes.seriesStart;
  document.getElementById('linkCatalog').href = routes.resources;

  const langBtn = document.getElementById('btnLangToggle');
  langBtn.textContent = state.lang === 'es' ? 'EN' : 'ES';
  langBtn.setAttribute('aria-label', t('langToggleAria'));
  document.getElementById('btnThemeToggle').setAttribute('aria-label', t('themeToggleAria'));

  for (const el of document.querySelectorAll('[data-i18n]')) {
    el.textContent = t(el.dataset.i18n);
  }
  document.getElementById('simPdnText').placeholder = t('simPdnPlaceholder');

  const table = document.getElementById('riskTable');
  table.style.setProperty('--label-2', JSON.stringify(t('colMpn')));
  table.style.setProperty('--label-3', JSON.stringify(t('colCrit')));
  table.style.setProperty('--label-4', JSON.stringify(t('colMargin')));
  table.style.setProperty('--label-5', JSON.stringify(t('colStatus')));

  document.getElementById('modeText').textContent = state.isLive ? t('statusLive') : t('statusSandbox');
}

function setView(viewName) {
  const valid = ['cockpit', 'simulator', 'ltb'];
  state.view = valid.includes(viewName) ? viewName : 'cockpit';
  for (const v of valid) {
    document.getElementById(`panel-${v}`).classList.toggle('hidden', v !== state.view);
  }
  for (const btn of document.querySelectorAll('.tab-btn[data-view]')) {
    btn.setAttribute('aria-selected', String(btn.dataset.view === state.view));
  }
  if (state.view === 'simulator') renderBomGraph();
  if (state.view === 'ltb') renderLtbResult();
  syncUrlParams();
  trackEvent('obs_view_change', { view: state.view });
}

function populateMpnSelect() {
  const sel = document.getElementById('simMpnSelect');
  const mpns = Object.values(state.catalog.mpns);
  const opts = mpns.map((m) => {
    const o = document.createElement('option');
    o.value = m.mpn;
    o.textContent = `${m.mpn} — ${m.manufacturer} (${m.lifecycle})`;
    if (m.mpn === state.focusMpn) o.selected = true;
    return o;
  });
  sel.replaceChildren(...opts);
  if (!state.catalog.mpns[state.focusMpn] && mpns.length) state.focusMpn = mpns[0].mpn;
}

function populateLtbInputs(cfg) {
  if (!cfg) return;
  document.getElementById('inDemand').value = cfg.monthly_demand;
  document.getElementById('inCv').value = cfg.demand_cv;
  document.getElementById('inRedesign').value = cfg.redesign_months;
  document.getElementById('inLead').value = cfg.lead_time_months;
  document.getElementById('inStock').value = cfg.current_stock_units;
  document.getElementById('inPriceLtb').value = cfg.ltb_unit_price_eur;
  document.getElementById('inPriceFff').value = cfg.fff_unit_price_eur;
  document.getElementById('inNre').value = cfg.redesign_nre_eur;
  document.getElementById('inWacc').value = Math.round((cfg.annual_holding_wacc_rate ?? 0.28) * 100);
  document.getElementById('inMargin').value = cfg.monthly_margin_at_risk_eur;
  document.getElementById('inZ').value = String(cfg.service_level_z ?? 2.054);
}

function renderKpis(metrics) {
  document.getElementById('kpiTotalRisk').textContent = formatEur(metrics.total_risk_eur, state.lang);
  document.getElementById('kpiAlerts').textContent = formatInt(metrics.active_alerts, state.lang);
  document.getElementById('kpiSkus').textContent = formatInt(metrics.blocked_skus_count, state.lang);
  document.getElementById('kpiLtbCap').textContent = formatEur(metrics.estimated_ltb_capital_eur, state.lang);
}

function createStatusBadge(status) {
  const span = document.createElement('span');
  const cls =
    status.includes('CRITICAL')
      ? 'status-critical'
      : status.includes('EVALUATING')
        ? 'status-evaluating'
        : 'status-monitored';
  span.className = `status-badge ${cls}`;
  span.textContent = status;
  return span;
}

function renderTable(metrics) {
  const tbody = document.getElementById('skuTableBody');
  const emptyEl = document.getElementById('tableEmptyState');
  const tableEl = document.getElementById('riskTable');

  if (!metrics.affected_skus || metrics.affected_skus.length === 0) {
    tbody.replaceChildren();
    tableEl.classList.add('hidden');
    emptyEl.classList.remove('hidden');
    return;
  }

  tableEl.classList.remove('hidden');
  emptyEl.classList.add('hidden');

  const rows = metrics.affected_skus.map((item) => {
    const tr = document.createElement('tr');
    tr.tabIndex = 0;
    tr.addEventListener('click', () => {
      state.focusMpn = item.trigger_mpn;
      populateMpnSelect();
      setView('simulator');
    });
    tr.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        state.focusMpn = item.trigger_mpn;
        populateMpnSelect();
        setView('simulator');
      }
    });

    const th = document.createElement('th');
    th.scope = 'row';
    th.dataset.value = item.sku;
    th.textContent = item.sku;

    const tdMpn = document.createElement('td');
    tdMpn.className = 'mono';
    tdMpn.dataset.value = item.trigger_mpn;
    tdMpn.textContent = item.trigger_mpn;

    const tdCrit = document.createElement('td');
    tdCrit.dataset.value = String(item.criticality_score ?? 0);
    const meter = document.createElement('div');
    meter.className = 'crit-meter';
    const scoreTxt = document.createElement('span');
    scoreTxt.textContent = String(item.criticality_score ?? 0);
    const bar = document.createElement('span');
    bar.className = 'crit-bar';
    const fill = document.createElement('span');
    fill.className = 'crit-fill';
    const sc = Number(item.criticality_score ?? 0);
    fill.style.width = `${Math.min(100, Math.max(0, sc))}%`;
    fill.style.background = sc >= 75 ? 'var(--status-danger)' : sc >= 45 ? 'var(--status-warning)' : 'var(--status-success)';
    bar.appendChild(fill);
    meter.append(scoreTxt, bar);
    tdCrit.appendChild(meter);

    const tdMargin = document.createElement('td');
    tdMargin.className = 'num-cell';
    tdMargin.dataset.value = String(item.margin_at_risk);
    tdMargin.textContent = formatEur(item.margin_at_risk, state.lang);

    const tdStatus = document.createElement('td');
    tdStatus.dataset.value = item.status;
    tdStatus.appendChild(createStatusBadge(item.status));

    tr.append(th, tdMpn, tdCrit, tdMargin, tdStatus);
    return tr;
  });

  tbody.replaceChildren(...rows);
  applyCurrentSort(false);
}

function applyCurrentSort(announce = true) {
  const table = document.getElementById('riskTable');
  const tbody = document.getElementById('skuTableBody');
  const headers = [...table.tHead.rows[0].cells];
  const th = headers[state.sortCol];
  if (!th || tbody.rows.length === 0) return;

  for (const h of headers) h.removeAttribute('aria-sort');
  th.setAttribute('aria-sort', state.sortDir);

  const type = th.dataset.type || 'text';
  const factor = state.sortDir === 'ascending' ? 1 : -1;
  const rows = [...tbody.rows];
  const getVal = (r) => r.cells[state.sortCol].dataset.value ?? r.cells[state.sortCol].textContent.trim();

  rows.sort((a, b) =>
    factor * (type === 'number' ? Number(getVal(a)) - Number(getVal(b)) : collator.compare(getVal(a), getVal(b))),
  );

  // Move existing <tr> nodes without rebuilding tbody (modern-web-guidance: sortable-table)
  for (const row of rows) {
    if (typeof tbody.moveBefore === 'function') tbody.moveBefore(row, null);
    else tbody.appendChild(row);
  }

  if (announce) {
    const colLabel = th.querySelector('span')?.textContent?.trim() || '';
    document.getElementById('tableStatus').textContent = t('sortAnnounce', {
      col: colLabel,
      dir: state.sortDir === 'ascending' ? t('dirAsc') : t('dirDesc'),
      count: rows.length,
    });
  }
}

function renderConsole(logs, animate = true) {
  const box = document.getElementById('telemetryConsole');
  for (const id of state.timers) clearTimeout(id);
  state.timers = [];
  box.replaceChildren();

  const filtered = (logs || []).filter((line) => state.logFilter === 'ALL' || line.includes(`[${state.logFilter}]`));
  const immediate = !animate || prefersReducedMotion();

  const appendLine = (entry) => {
    const div = document.createElement('div');
    div.className = 'log-line';
    if (entry.includes('[Alert]')) div.classList.add('alert');
    else if (entry.includes('[BOM/SQL]') || entry.includes('[Supabase')) div.classList.add('sql');
    div.textContent = `> ${entry}`;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
  };

  if (immediate) {
    for (const entry of filtered) appendLine(entry);
    return;
  }

  filtered.forEach((entry, idx) => {
    const timer = setTimeout(() => appendLine(entry), idx * 180);
    state.timers.push(timer);
  });
}

function svgEl(tag, attrs = {}, text = null) {
  const el = document.createElementNS(SVG_NS, tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, String(v));
  if (text !== null) el.textContent = text;
  return el;
}

function renderBomGraph() {
  const wrap = document.getElementById('bomGraphWrap');
  const result = traverseBomUpward(state.catalog, state.focusMpn);
  document.getElementById('simCycleBadge').classList.toggle('hidden', !result.cycleDetected);
  document.getElementById('selectedNodeInfo').textContent = `${result.mpn} (${result.lifecycle})`;
  document.getElementById('selectedNodeAlts').textContent = String(result.altSourcesCount);

  if (result.paths.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'empty-state';
    empty.textContent = t('simGraphEmpty');
    wrap.replaceChildren(empty);
    return;
  }

  const colNodes = [
    [{ id: result.mpn, sub: result.lifecycle, type: 'mpn', danger: result.lifecycle !== 'Active' }],
    [...new Set(result.paths.map((p) => p.internalPn))].map((id) => ({ id, sub: `AML alt: ${result.altSourcesCount}`, type: 'aml', danger: result.altSourcesCount === 0 })),
    [...new Set(result.paths.flatMap((p) => p.assemblies))].map((id) => ({ id, sub: 'Sub-Assembly', type: 'asm', danger: true })),
    [...new Map(result.paths.map((p) => [p.sku, p])).values()].map((p) => ({
      id: p.sku,
      sub: formatEur(p.grossMargin, state.lang),
      type: 'sku',
      danger: true,
    })),
  ];

  const colTitles = [t('colHeaderMpn'), t('colHeaderAml'), t('colHeaderAsm'), t('colHeaderSku')];
  const colX = [16, 206, 396, 586];
  const boxW = 160;
  const boxH = 52;
  const maxRows = Math.max(...colNodes.map((c) => c.length));
  const svgH = Math.max(210, 62 + maxRows * 74);
  const svg = svgEl('svg', { class: 'bom-svg', viewBox: `0 0 762 ${svgH}`, role: 'img', 'aria-label': t('simGraphTitle') });

  const positions = new Map();
  colTitles.forEach((label, cIdx) => {
    svg.appendChild(svgEl('text', { x: colX[cIdx], y: 22, fill: 'var(--text-secondary)', 'font-size': '11', 'font-weight': '700' }, label.toUpperCase()));
    const nodes = colNodes[cIdx];
    const startY = 44 + ((maxRows - nodes.length) * 36);
    nodes.forEach((n, rIdx) => {
      positions.set(`${cIdx}:${n.id}`, { x: colX[cIdx], y: startY + rIdx * 72, node: n });
    });
  });

  // Draw edges
  const drawn = new Set();
  const drawEdge = (k1, k2) => {
    const ek = `${k1}->${k2}`;
    if (drawn.has(ek)) return;
    drawn.add(ek);
    const p1 = positions.get(k1);
    const p2 = positions.get(k2);
    if (!p1 || !p2) return;
    const x1 = p1.x + boxW;
    const y1 = p1.y + boxH / 2;
    const x2 = p2.x;
    const y2 = p2.y + boxH / 2;
    const mx = (x1 + x2) / 2;
    const stroke = result.lifecycle === 'Active' ? 'var(--status-success)' : 'var(--status-danger)';
    svg.appendChild(svgEl('path', { d: `M${x1} ${y1} C${mx} ${y1}, ${mx} ${y2}, ${x2} ${y2}`, fill: 'none', stroke, 'stroke-width': '2', 'stroke-opacity': '0.8' }));
  };

  for (const p of result.paths) {
    drawEdge(`0:${p.mpn}`, `1:${p.internalPn}`);
    const asm = p.assemblies[0];
    if (asm) {
      drawEdge(`1:${p.internalPn}`, `2:${asm}`);
      drawEdge(`2:${asm}`, `3:${p.sku}`);
    }
  }

  // Draw interactive nodes
  for (const pos of positions.values()) {
    const g = svgEl('g', { class: 'bom-node', tabindex: '0', role: 'button', 'aria-label': `${pos.node.id} ${pos.node.sub}` });
    const stroke = pos.node.danger && result.lifecycle !== 'Active' ? 'var(--status-danger)' : 'var(--accent-primary)';
    g.appendChild(svgEl('rect', { x: pos.x, y: pos.y, width: boxW, height: boxH, rx: 8, fill: 'var(--bg-elevated)', stroke, 'stroke-width': '1.5' }));
    g.appendChild(svgEl('text', { x: pos.x + 10, y: pos.y + 21, fill: 'var(--text-primary)', 'font-size': '11.5', 'font-weight': '700', class: 'mono' }, pos.node.id.slice(0, 18)));
    g.appendChild(svgEl('text', { x: pos.x + 10, y: pos.y + 39, fill: 'var(--text-secondary)', 'font-size': '10.5', class: 'mono' }, pos.node.sub.slice(0, 22)));
    const selectNode = () => {
      document.getElementById('selectedNodeInfo').textContent = `${pos.node.id} — ${pos.node.sub}`;
    };
    g.addEventListener('click', selectNode);
    g.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectNode(); }
    });
    svg.appendChild(g);
  }

  wrap.replaceChildren(svg);
}

function renderLtbResult() {
  const form = document.getElementById('ltbForm');
  let valid = true;
  for (const inp of form.querySelectorAll('input[required]')) {
    const errEl = document.getElementById(inp.getAttribute('aria-describedby'));
    const ok = inp.checkValidity();
    inp.setAttribute('aria-invalid', String(!ok));
    if (errEl) errEl.textContent = ok ? '' : t('ltbInvalidMsg');
    if (!ok) valid = false;
  }
  if (!valid) return;

  const res = computeLtbVsFff({
    monthly_demand: Number(document.getElementById('inDemand').value),
    demand_cv: Number(document.getElementById('inCv').value),
    redesign_months: Number(document.getElementById('inRedesign').value),
    lead_time_months: Number(document.getElementById('inLead').value),
    current_stock_units: Number(document.getElementById('inStock').value),
    ltb_unit_price_eur: Number(document.getElementById('inPriceLtb').value),
    fff_unit_price_eur: Number(document.getElementById('inPriceFff').value),
    redesign_nre_eur: Number(document.getElementById('inNre').value),
    annual_holding_wacc_rate: Number(document.getElementById('inWacc').value) / 100,
    monthly_margin_at_risk_eur: Number(document.getElementById('inMargin').value),
    service_level_z: Number(document.getElementById('inZ').value),
  });
  if (!res) return;

  const verdictKey =
    res.verdict === 'EXECUTE_LTB'
      ? 'verdictExecuteLtb'
      : res.verdict === 'REDESIGN_FFF'
        ? 'verdictRedesignFff'
        : 'verdictHybrid';

  document.getElementById('ltbVerdictTitle').textContent = t(verdictKey);
  document.getElementById('ltbSavingsVal').textContent = formatEur(res.savings_eur, state.lang);
  document.getElementById('ltbGapNote').textContent = res.stock_gap_months > 0 ? t('verdictGapNote', { gap: res.stock_gap_months }) : '';
  document.getElementById('resLtbCostVal').textContent = formatEur(res.ltb_total_cost_eur, state.lang);
  document.getElementById('resFffCostVal').textContent = formatEur(res.fff_total_cost_eur, state.lang);
  document.getElementById('resWcVal').textContent = formatEur(res.ltb_working_capital_eur, state.lang);
  document.getElementById('resSsVal').textContent = `${formatInt(res.safety_stock_units, state.lang)} ${t('unitUds')}`;
  document.getElementById('resOrderVal').textContent = `${formatInt(res.ltb_order_qty, state.lang)} ${t('unitUds')}`;
  document.getElementById('resBeVal').textContent =
    res.breakeven_months !== null ? `${res.breakeven_months} ${t('resMonthsUnit')}` : t('resNoBreakeven');
}

function renderAll(animateLogs = true) {
  state.metrics = evaluateCatalogRisk(state.catalog);
  renderKpis(state.metrics);
  renderTable(state.metrics);
  renderConsole(state.metrics.agent_logs, animateLogs);
  populateMpnSelect();
  if (state.view === 'simulator') renderBomGraph();
  renderLtbResult();
}

function loadScenario(scenarioId) {
  const preset = PRESET_SCENARIOS[scenarioId] || PRESET_SCENARIOS['drone-capacitor'];
  state.scenarioId = preset.id;
  state.isLive = false;
  state.catalog = cloneCatalog(preset.catalog);
  state.focusMpn = preset.focusMpn;
  populateLtbInputs(preset.catalog.defaultLtb);

  for (const pill of document.querySelectorAll('.preset-pill[data-scenario]')) {
    const active = pill.dataset.scenario === state.scenarioId;
    pill.classList.toggle('active', active);
    pill.setAttribute('aria-pressed', String(active));
  }
  document.getElementById('modeText').textContent = t('statusSandbox');
  renderAll(true);
  syncUrlParams();
  trackEvent('obs_scenario_select', { scenario: state.scenarioId });
}

function downloadBlob(content, filename, mime) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function exportReportCsv() {
  const header = 'SKU,Trigger_MPN,IEC_62402_Score,Margin_at_Risk_EUR,Alt_Sources,Status';
  const rows = (state.metrics?.affected_skus || []).map((r) =>
    [r.sku, r.trigger_mpn, r.criticality_score, r.margin_at_risk.toFixed(2), r.alt_sources_count, `"${r.status}"`].join(','),
  );
  downloadBlob([header, ...rows].join('\n'), `agentic-radar-${state.scenarioId}.csv`, 'text/csv;charset=utf-8');
  trackEvent('obs_export', { format: 'csv', scenario: state.scenarioId });
}

function exportReportJson() {
  downloadBlob(JSON.stringify({ scenario: state.scenarioId, ...state.metrics }, null, 2), `agentic-radar-${state.scenarioId}.json`, 'application/json');
  trackEvent('obs_export', { format: 'json', scenario: state.scenarioId });
}

function exportExecutivePng() {
  const canvas = document.createElement('canvas');
  canvas.width = 1200;
  canvas.height = 630;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  ctx.fillStyle = '#0b0f17';
  ctx.fillRect(0, 0, 1200, 630);
  ctx.strokeStyle = '#0ea5e9';
  ctx.lineWidth = 4;
  ctx.strokeRect(24, 24, 1152, 582);

  ctx.fillStyle = '#0ea5e9';
  ctx.font = '700 18px system-ui, sans-serif';
  ctx.fillText('DATALARIA · AGENTIC RADAR v2.0', 60, 78);

  ctx.fillStyle = '#f8fafc';
  ctx.font = '700 34px system-ui, sans-serif';
  ctx.fillText(t('pngCardSubtitle'), 60, 126);

  const cards = [
    { l: t('kpiRiskLabel'), v: formatEur(state.metrics.total_risk_eur, state.lang), c: '#ef4444' },
    { l: t('kpiAlertsLabel'), v: String(state.metrics.active_alerts), c: '#f59e0b' },
    { l: t('kpiSkusLabel'), v: String(state.metrics.blocked_skus_count), c: '#f8fafc' },
    { l: t('kpiLtbLabel'), v: formatEur(state.metrics.estimated_ltb_capital_eur, state.lang), c: '#0ea5e9' },
  ];
  cards.forEach((card, i) => {
    const x = 60 + i * 274;
    ctx.fillStyle = '#111827';
    ctx.fillRect(x, 165, 254, 130);
    ctx.strokeStyle = 'rgba(148,163,184,0.25)';
    ctx.lineWidth = 1;
    ctx.strokeRect(x, 165, 254, 130);
    ctx.fillStyle = '#94a3b8';
    ctx.font = '600 14px system-ui, sans-serif';
    ctx.fillText(card.l.toUpperCase().slice(0, 24), x + 16, 200);
    ctx.fillStyle = card.c;
    ctx.font = '700 28px monospace';
    ctx.fillText(card.v, x + 16, 252);
  });

  ctx.fillStyle = '#111827';
  ctx.fillRect(60, 325, 1080, 220);
  ctx.fillStyle = '#94a3b8';
  ctx.font = '700 14px monospace';
  ctx.fillText('SKU                    MPN                   IEC62402   MARGIN EUR     STATUS', 84, 362);

  (state.metrics.affected_skus || []).slice(0, 4).forEach((row, idx) => {
    const y = 402 + idx * 36;
    ctx.fillStyle = '#f8fafc';
    ctx.font = '600 15px monospace';
    ctx.fillText(row.sku.padEnd(22, ' ').slice(0, 22), 84, y);
    ctx.fillStyle = '#94a3b8';
    ctx.fillText(row.trigger_mpn.padEnd(21, ' ').slice(0, 21), 282, y);
    ctx.fillStyle = row.criticality_score >= 75 ? '#ef4444' : '#f59e0b';
    ctx.fillText(`${row.criticality_score}/100`, 484, y);
    ctx.fillStyle = '#f8fafc';
    ctx.fillText(formatEur(row.margin_at_risk, state.lang), 584, y);
    ctx.fillText(row.status, 748, y);
  });

  ctx.fillStyle = '#94a3b8';
  ctx.font = '500 14px system-ui, sans-serif';
  ctx.fillText(t('pngCardFooter'), 60, 582);

  const a = document.createElement('a');
  a.href = canvas.toDataURL('image/png');
  a.download = `agentic-radar-${state.scenarioId}-1200x630.png`;
  a.click();
  trackEvent('obs_export', { format: 'png', scenario: state.scenarioId });
}

function handleCsvImport(csvText, source) {
  const feedback = document.getElementById('csvFeedback');
  const parsed = parseBomCsv(csvText);
  if (!parsed.ok) {
    feedback.style.color = 'var(--status-danger)';
    feedback.textContent =
      parsed.errorType === 'missing'
        ? t('csvErrMissing', { cols: parsed.missing.join(', ') })
        : t('csvErrEmpty');
    return;
  }
  state.catalog = parsed.catalog;
  state.scenarioId = 'custom-csv';
  state.isLive = false;
  const firstEol = Object.values(parsed.catalog.mpns).find((m) => m.lifecycle === 'EOL' || m.lifecycle === 'Obsolete');
  state.focusMpn = firstEol ? firstEol.mpn : Object.keys(parsed.catalog.mpns)[0];
  for (const pill of document.querySelectorAll('.preset-pill')) {
    pill.classList.remove('active');
    pill.setAttribute('aria-pressed', 'false');
  }
  renderAll(true);
  feedback.style.color = 'var(--status-success)';
  feedback.textContent = t('csvSuccess', parsed.stats);
  trackEvent('obs_csv_import', { source, skus: parsed.stats.skus, alerts: parsed.stats.alerts });
}

async function probeLocalLiveEngine() {
  const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  const sp = new URLSearchParams(window.location.search);
  const customApi = sp.get('api');
  if (!isLocal && !customApi) return;

  const targetUrl = customApi ? `${customApi.replace(/\/$/, '')}/api/v1/dashboard/risk-metrics` : 'http://127.0.0.1:8001/api/v1/dashboard/risk-metrics';
  try {
    const res = await fetch(targetUrl, { signal: AbortSignal.timeout(800) });
    if (!res.ok) return;
    const data = await res.json();
    if (data && Array.isArray(data.affected_skus)) {
      state.isLive = true;
      state.metrics = {
        total_risk_eur: Number(data.total_risk_eur || 0),
        active_alerts: Number(data.active_alerts || 0),
        blocked_skus_count: Number(data.blocked_skus_count ?? data.affected_skus.length),
        estimated_ltb_capital_eur: Number(data.estimated_ltb_capital_eur ?? data.total_risk_eur * 0.45),
        affected_skus: data.affected_skus.map((s) => ({
          sku: String(s.sku || ''),
          trigger_mpn: String(s.trigger_mpn || ''),
          margin_at_risk: Number(s.margin_at_risk || 0),
          criticality_score: Number(s.criticality_score ?? (String(s.status).includes('CRITICAL') ? 88 : 62)),
          alt_sources_count: Number(s.alt_sources_count ?? 0),
          status: String(s.status || 'MONITORED'),
        })),
        agent_logs: Array.isArray(data.agent_logs) ? data.agent_logs.map(String) : [],
      };
      document.getElementById('modeText').textContent = t('statusLive');
      renderKpis(state.metrics);
      renderTable(state.metrics);
      renderConsole(state.metrics.agent_logs, true);
    }
  } catch {
    // Seamless deterministic Sandbox fallback without console errors
  }
}

function wireDialogFallbacks() {
  const dialog = document.getElementById('csvDialog');
  dialog.addEventListener('close', () => { dialog.returnValue = ''; });
  if (!('closedBy' in HTMLDialogElement.prototype)) {
    const outside = (e) => {
      const r = dialog.getBoundingClientRect();
      return e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom;
    };
    let downOut = false;
    dialog.addEventListener('pointerdown', (e) => { downOut = outside(e); });
    dialog.addEventListener('pointerup', (e) => { if (downOut && outside(e)) dialog.close(); });
  }
  if (!Object.hasOwn(HTMLElement.prototype, 'popover')) {
    const pop = document.getElementById('formulaPopover');
    pop.hidden = true;
    document.getElementById('btnFormula').addEventListener('click', () => { pop.hidden = !pop.hidden; });
  }
}

function bindEvents() {
  document.getElementById('btnLangToggle').addEventListener('click', () => {
    state.lang = state.lang === 'es' ? 'en' : 'es';
    try { localStorage.setItem('obs_radar_lang', state.lang); } catch { /* ignore */ }
    applyTranslations();
    renderAll(false);
    syncUrlParams();
  });

  document.getElementById('btnThemeToggle').addEventListener('click', () => {
    state.theme = state.theme === 'dark' ? 'light' : 'dark';
    applyTheme();
  });

  for (const btn of document.querySelectorAll('.tab-btn[data-view]')) {
    btn.addEventListener('click', () => setView(btn.dataset.view));
  }

  for (const pill of document.querySelectorAll('.preset-pill[data-scenario]')) {
    pill.addEventListener('click', () => loadScenario(pill.dataset.scenario));
  }

  for (const btn of document.querySelectorAll('.sort-btn[data-col]')) {
    btn.addEventListener('click', () => {
      const col = Number(btn.dataset.col);
      state.sortDir = state.sortCol === col && state.sortDir === 'ascending' ? 'descending' : 'ascending';
      state.sortCol = col;
      applyCurrentSort(true);
    });
  }

  for (const fp of document.querySelectorAll('.filter-pill[data-filter]')) {
    fp.addEventListener('click', () => {
      state.logFilter = fp.dataset.filter;
      for (const b of document.querySelectorAll('.filter-pill')) b.classList.toggle('active', b === fp);
      renderConsole(state.metrics?.agent_logs || [], false);
    });
  }

  document.getElementById('btnReplay').addEventListener('click', () => {
    renderConsole(state.metrics?.agent_logs || [], true);
    trackEvent('obs_replay_feed', { scenario: state.scenarioId });
  });

  document.getElementById('btnRestoreSample').addEventListener('click', () => loadScenario('drone-capacitor'));
  document.getElementById('btnDismissBanner').addEventListener('click', () => document.getElementById('statusBanner').classList.add('hidden'));

  document.getElementById('simMpnSelect').addEventListener('change', (e) => {
    state.focusMpn = e.target.value;
    renderBomGraph();
  });

  document.getElementById('simForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const rawPdn = document.getElementById('simPdnText').value.trim();
    const extracted = rawPdn ? extractMpnFromPdnText(rawPdn, Object.keys(state.catalog.mpns)) : null;
    const target = extracted && state.catalog.mpns[extracted] ? extracted : document.getElementById('simMpnSelect').value;
    const status = document.getElementById('simStatusSelect').value;
    if (state.catalog.mpns[target]) {
      state.catalog.mpns[target].lifecycle = status;
      state.focusMpn = target;
      renderAll(true);
      renderBomGraph();
      trackEvent('obs_pdn_inject', { mpn: target, status });
    }
  });

  document.getElementById('btnSimReset').addEventListener('click', () => loadScenario(state.scenarioId in PRESET_SCENARIOS ? state.scenarioId : 'drone-capacitor'));

  document.getElementById('btnJumpToLtb').addEventListener('click', () => {
    const tr = traverseBomUpward(state.catalog, state.focusMpn);
    const mInfo = state.catalog.mpns[state.focusMpn];
    if (mInfo) {
      document.getElementById('inDemand').value = mInfo.monthly_demand || 350;
      document.getElementById('inPriceLtb').value = Number((mInfo.unit_price_eur * 1.15).toFixed(2));
      document.getElementById('inPriceFff').value = Number((mInfo.unit_price_eur * 0.92).toFixed(2));
      document.getElementById('inMargin').value = Math.max(1000, Math.round(tr.totalRiskEur || 12500));
    }
    setView('ltb');
  });

  document.getElementById('ltbForm').addEventListener('input', () => {
    renderLtbResult();
    trackEvent('obs_ltb_calculate', { scenario: state.scenarioId });
  });

  // CSV Modal
  const dialog = document.getElementById('csvDialog');
  document.getElementById('btnOpenCsv').addEventListener('click', () => {
    document.getElementById('csvFeedback').textContent = '';
    dialog.showModal();
  });
  document.getElementById('csvFileInput').addEventListener('change', async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    handleCsvImport(text, 'local-file');
  });
  document.getElementById('btnCsvSample').addEventListener('click', () => handleCsvImport(SAMPLE_BOM_CSV, 'sample-1click'));
  document.getElementById('btnCsvTemplate').addEventListener('click', () => {
    downloadBlob(SAMPLE_BOM_CSV, 'datalaria-bom-template.csv', 'text/csv;charset=utf-8');
  });

  document.getElementById('btnExportCsv').addEventListener('click', exportReportCsv);
  document.getElementById('btnExportJson').addEventListener('click', exportReportJson);
  document.getElementById('btnExportPng').addEventListener('click', exportExecutivePng);

  // Kit IEC 62402 & Modo Pro B2B Modal (Brevo Waitlist, zero mailto:)
  const proDialog = document.getElementById('proKitDialog');
  const proBtn = document.getElementById('btnOpenProKit');
  const proForm = document.getElementById('proKitForm');
  if (proBtn && proDialog) {
    proBtn.addEventListener('click', () => {
      document.getElementById('proKitFeedback').textContent = '';
      proDialog.showModal();
      trackEvent('obs_pro_modal_open', { item_id: 'pack-obs', source: 'preset-bar' });
    });
  }
  if (proForm) {
    proForm.addEventListener('submit', async (ev) => {
      ev.preventDefault();
      const fb = document.getElementById('proKitFeedback');
      const submitBtn = document.getElementById('proKitSubmit');
      const nameVal = (document.getElementById('proKitName').value || '').trim();
      const emailVal = (document.getElementById('proKitEmail').value || '').trim();
      if (!nameVal || !emailVal.includes('@')) {
        fb.style.color = 'var(--status-danger)';
        fb.textContent = t('proKitErr');
        return;
      }
      submitBtn.disabled = true;
      fb.style.color = 'var(--text-secondary)';
      fb.textContent = t('proKitSending');
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      try {
        if (!isLocal) {
          const resp = await fetch('/.netlify/functions/subscribe', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify({ name: nameVal, email: emailVal, language: state.lang, list: 'newsletter' }),
            signal: AbortSignal.timeout(5000),
          });
          if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        }
        fb.style.color = 'var(--status-success)';
        fb.textContent = t('proKitSuccess');
        proForm.reset();
        trackEvent('obs_pro_waitlist_submit', { item_id: 'pack-obs', source: 'pro-modal' });
      } catch {
        fb.style.color = 'var(--status-danger)';
        fb.textContent = t('proKitErr');
      } finally {
        submitBtn.disabled = false;
      }
    });
  }

  for (const a of document.querySelectorAll('a[data-cta]')) {
    const key = a.dataset.cta === 'pack-stock' ? 'stock' : a.dataset.cta === 'pack-amfe' ? 'amfe' : 'suite03';
    a.href = CHECKOUT_URLS[key];
    a.addEventListener('click', () => {
      trackEvent('obs_cta_click', { item_id: a.dataset.cta, source: a.dataset.source || 'cockpit' });
    });
  }
}

function registerPwaServiceWorker() {
  const isLocalDev = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    && !new URLSearchParams(window.location.search).has('pwa_test');

  if ('serviceWorker' in navigator) {
    if (isLocalDev) {
      const hadController = Boolean(navigator.serviceWorker.controller);
      Promise.all([
        navigator.serviceWorker.getRegistrations()
          .then((regs) => Promise.all(regs.map((r) => r.unregister())))
          .catch(() => {}),
        ('caches' in window
          ? caches.keys().then((keys) =>
              Promise.all(keys.filter((k) => k.startsWith('obs-radar-')).map((k) => caches.delete(k))))
          : Promise.resolve()),
      ]).then(() => {
        if (hadController && !sessionStorage.getItem('obs_radar_sw_purged_v200')) {
          sessionStorage.setItem('obs_radar_sw_purged_v200', '1');
          window.location.reload();
        }
      });
    } else {
      const doRegisterSw = () => {
        navigator.serviceWorker.register('sw.js')
          .then((reg) => {
            reg.update().catch(() => {});
          })
          .catch((err) => console.warn('[PWA] Error SW:', err));
      };
      if (document.readyState !== 'loading') {
        doRegisterSw();
      } else {
        window.addEventListener('load', doRegisterSw, { once: true });
      }
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  state.lang = detectInitialLang();
  state.theme = detectInitialTheme();
  applyTheme();
  wireDialogFallbacks();
  bindEvents();
  registerPwaServiceWorker();

  const sp = new URLSearchParams(window.location.search);
  const initialScenario = sp.get('scenario') || 'drone-capacitor';
  const initialView = sp.get('view') || 'cockpit';

  applyTranslations();
  loadScenario(initialScenario);
  setView(initialView);
  trackEvent('obs_sandbox_view', { scenario: state.scenarioId, view: state.view });
  probeLocalLiveEngine();
});
