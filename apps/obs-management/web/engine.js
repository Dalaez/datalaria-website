// apps/obs-management/web/engine.js
// El Músculo Determinista: Recorrido DAG BOM con guardia anti-ciclos (INV-OBS-4),
// Índice de Criticidad IEC 62402, Calculadora LTB vs. Rediseño FFF y Parser CSV 100 % local (INV-OBS-7).

export const LIFECYCLE_SCORE = Object.freeze({
  Obsolete: 100,
  EOL: 85,
  NRND: 55,
  Active: 10,
});

export const REQUIRED_CSV_COLUMNS = Object.freeze([
  'End_Product_SKU',
  'End_Product_Margin',
  'Assembly_PN',
  'Component_PN',
  'Quantity_per_Assembly',
  'Manufacturer',
  'Manufacturer_PN',
  'Lifecycle',
]);

export const SAMPLE_BOM_CSV = [
  'End_Product_SKU,End_Product_Margin,Assembly_PN,Component_PN,Quantity_per_Assembly,Manufacturer,Manufacturer_PN,Lifecycle',
  'DRONE-X1,12500.00,PCB-FLIGHT-01,CAP-001,4,Texas Instruments,TI-CAP-10U-50,EOL',
  'DRONE-X1,12500.00,PCB-FLIGHT-01,MCU-003,1,STMicroelectronics,STM32F405RGT6,NRND',
  'DRONE-X1,12500.00,MOTOR-ASSEMBLY-04,ESC-006,4,Hobbywing,XRotor-Micro-30A,Active',
  'SERVER-RACK-9,2950.00,PWR-SUPPLY-02,MCU-003,2,STMicroelectronics,STM32F405RGT6,EOL',
  'SERVER-RACK-9,2950.00,PWR-SUPPLY-02,MCU-003,2,NXP,MK20DX256VLH7,Obsolete',
  'SERVER-RACK-9,2950.00,PCB-MAIN-01,RAM-008,4,Samsung,M393A4K40CB2-CVF,Active',
  'LIDAR-SENSOR-PRO,18400.00,LASER-TUBE-01,LASER-012,2,Osram,SPL-PL90-3,EOL',
  'LIDAR-SENSOR-PRO,18400.00,PCB-SENSOR-05,CAP-001,6,Yageo,CC1206KKX7R9BB106,Active',
  'LIDAR-SENSOR-PRO,18400.00,PCB-SENSOR-05,MCU-003,1,STMicroelectronics,STM32F405RGT6,NRND',
].join('\n');

const BASE_PRODUCTS = [
  { sku: 'DRONE-X1', name: 'Autonomous Inspection Drone X1', gross_margin: 12500.0 },
  { sku: 'SERVER-RACK-9', name: 'Edge Telemetry Server Rack 9', gross_margin: 2950.0 },
  { sku: 'LIDAR-SENSOR-PRO', name: 'Industrial LiDAR Sensor Pro', gross_margin: 18400.0 },
];

const BASE_BOM_EDGES = [
  // Product -> Assembly
  { parent: 'DRONE-X1', parentType: 'product', child: 'PCB-FLIGHT-01', qty: 1 },
  { parent: 'DRONE-X1', parentType: 'product', child: 'MOTOR-ASSEMBLY-04', qty: 1 },
  { parent: 'SERVER-RACK-9', parentType: 'product', child: 'PCB-MAIN-01', qty: 1 },
  { parent: 'SERVER-RACK-9', parentType: 'product', child: 'PWR-SUPPLY-02', qty: 1 },
  { parent: 'LIDAR-SENSOR-PRO', parentType: 'product', child: 'PCB-SENSOR-05', qty: 1 },
  { parent: 'LIDAR-SENSOR-PRO', parentType: 'product', child: 'LASER-TUBE-01', qty: 1 },
  // Assembly -> Internal Component
  { parent: 'PCB-FLIGHT-01', parentType: 'assembly', child: 'CAP-001', qty: 4 },
  { parent: 'PCB-FLIGHT-01', parentType: 'assembly', child: 'MCU-003', qty: 1 },
  { parent: 'MOTOR-ASSEMBLY-04', parentType: 'assembly', child: 'ESC-006', qty: 4 },
  { parent: 'PCB-MAIN-01', parentType: 'assembly', child: 'RAM-008', qty: 4 },
  { parent: 'PWR-SUPPLY-02', parentType: 'assembly', child: 'MCU-003', qty: 2 },
  { parent: 'PCB-SENSOR-05', parentType: 'assembly', child: 'MCU-003', qty: 1 },
  { parent: 'PCB-SENSOR-05', parentType: 'assembly', child: 'CAP-001', qty: 6 },
  { parent: 'LASER-TUBE-01', parentType: 'assembly', child: 'LASER-012', qty: 2 },
];

const BASE_AML = [
  { internal_pn: 'CAP-001', mpn: 'TI-CAP-10U-50', manufacturer: 'Texas Instruments', pref: 'Primary' },
  { internal_pn: 'CAP-001', mpn: 'CC1206KKX7R9BB106', manufacturer: 'Yageo', pref: 'Secondary' },
  { internal_pn: 'MCU-003', mpn: 'STM32F405RGT6', manufacturer: 'STMicroelectronics', pref: 'Primary' },
  { internal_pn: 'MCU-003', mpn: 'MK20DX256VLH7', manufacturer: 'NXP', pref: 'Secondary' },
  { internal_pn: 'ESC-006', mpn: 'XROTOR-MICRO-30A', manufacturer: 'Hobbywing', pref: 'Primary' },
  { internal_pn: 'RAM-008', mpn: 'M393A4K40CB2-CVF', manufacturer: 'Samsung', pref: 'Primary' },
  { internal_pn: 'LASER-012', mpn: 'SPL-PL90-3', manufacturer: 'Osram', pref: 'Primary' },
];

function buildScenarioCatalog(mpnOverrides, defaultLtb) {
  const mpnDefaults = {
    'TI-CAP-10U-50': { manufacturer: 'Texas Instruments', lifecycle: 'Active', unit_price_eur: 1.85, monthly_demand: 900 },
    'CC1206KKX7R9BB106': { manufacturer: 'Yageo', lifecycle: 'Active', unit_price_eur: 1.4, monthly_demand: 900 },
    'STM32F405RGT6': { manufacturer: 'STMicroelectronics', lifecycle: 'Active', unit_price_eur: 8.4, monthly_demand: 420 },
    'MK20DX256VLH7': { manufacturer: 'NXP', lifecycle: 'Obsolete', unit_price_eur: 9.2, monthly_demand: 180 },
    'XROTOR-MICRO-30A': { manufacturer: 'Hobbywing', lifecycle: 'Active', unit_price_eur: 19.5, monthly_demand: 260 },
    'M393A4K40CB2-CVF': { manufacturer: 'Samsung', lifecycle: 'Active', unit_price_eur: 68.0, monthly_demand: 110 },
    'SPL-PL90-3': { manufacturer: 'Osram', lifecycle: 'Active', unit_price_eur: 42.0, monthly_demand: 150 },
  };
  const mpns = {};
  for (const [k, v] of Object.entries(mpnDefaults)) {
    mpns[k] = { mpn: k, ...v, ...(mpnOverrides[k] || {}) };
  }
  return {
    products: BASE_PRODUCTS.map((p) => ({ ...p })),
    bomEdges: BASE_BOM_EDGES.map((e) => ({ ...e })),
    aml: BASE_AML.map((a) => ({ ...a })),
    mpns,
    defaultLtb,
  };
}

export const PRESET_SCENARIOS = Object.freeze({
  'drone-capacitor': {
    id: 'drone-capacitor',
    catalog: buildScenarioCatalog(
      {
        'TI-CAP-10U-50': { lifecycle: 'EOL' },
        'CC1206KKX7R9BB106': { lifecycle: 'EOL' },
        'STM32F405RGT6': { lifecycle: 'NRND' },
      },
      {
        monthly_demand: 900,
        demand_cv: 0.22,
        redesign_months: 6,
        lead_time_months: 2,
        current_stock_units: 1200,
        ltb_unit_price_eur: 2.15,
        fff_unit_price_eur: 1.55,
        redesign_nre_eur: 14500,
        annual_holding_wacc_rate: 0.28,
        monthly_margin_at_risk_eur: 12500,
        service_level_z: 2.054,
      },
    ),
    focusMpn: 'TI-CAP-10U-50',
  },
  'mcu-multi-sku': {
    id: 'mcu-multi-sku',
    catalog: buildScenarioCatalog(
      {
        'STM32F405RGT6': { lifecycle: 'EOL' },
        'MK20DX256VLH7': { lifecycle: 'Obsolete' },
      },
      {
        monthly_demand: 420,
        demand_cv: 0.25,
        redesign_months: 9,
        lead_time_months: 3,
        current_stock_units: 600,
        ltb_unit_price_eur: 9.8,
        fff_unit_price_eur: 7.2,
        redesign_nre_eur: 32000,
        annual_holding_wacc_rate: 0.28,
        monthly_margin_at_risk_eur: 33850,
        service_level_z: 2.054,
      },
    ),
    focusMpn: 'STM32F405RGT6',
  },
  'full-line-halt': {
    id: 'full-line-halt',
    catalog: buildScenarioCatalog(
      {
        'TI-CAP-10U-50': { lifecycle: 'Obsolete' },
        'CC1206KKX7R9BB106': { lifecycle: 'EOL' },
        'STM32F405RGT6': { lifecycle: 'EOL' },
        'MK20DX256VLH7': { lifecycle: 'Obsolete' },
        'SPL-PL90-3': { lifecycle: 'EOL' },
      },
      {
        monthly_demand: 150,
        demand_cv: 0.18,
        redesign_months: 11,
        lead_time_months: 3,
        current_stock_units: 180,
        ltb_unit_price_eur: 46.0,
        fff_unit_price_eur: 38.0,
        redesign_nre_eur: 48000,
        annual_holding_wacc_rate: 0.30,
        monthly_margin_at_risk_eur: 18400,
        service_level_z: 2.326,
      },
    ),
    focusMpn: 'SPL-PL90-3',
  },
});

export function cloneCatalog(catalog) {
  return {
    products: catalog.products.map((p) => ({ ...p })),
    bomEdges: catalog.bomEdges.map((e) => ({ ...e })),
    aml: catalog.aml.map((a) => ({ ...a })),
    mpns: Object.fromEntries(Object.entries(catalog.mpns).map(([k, v]) => [k, { ...v }])),
    defaultLtb: catalog.defaultLtb ? { ...catalog.defaultLtb } : null,
  };
}

export function computeCriticality(lifecycle, altSourcesCount, marginAtRisk, refMargin = 15000) {
  const sLife = LIFECYCLE_SCORE[lifecycle] ?? 10;
  const sAml = altSourcesCount <= 0 ? 100 : altSourcesCount === 1 ? 50 : 15;
  const denom = Math.max(15000, Number(refMargin) || 15000);
  const sMargin = Math.min(100, (100 * Math.max(0, Number(marginAtRisk) || 0)) / denom);
  const score = Math.min(100, Math.round(0.40 * sLife + 0.35 * sAml + 0.25 * sMargin));
  const status =
    score >= 75
      ? 'CRITICAL LTB REQUIRED'
      : score >= 45
        ? 'EVALUATING INVENTORY'
        : 'MONITORED';
  return { score, status };
}

export function traverseBomUpward(catalog, targetMpn) {
  const mpnClean = String(targetMpn || '').trim().toUpperCase();
  const productMap = new Map(catalog.products.map((p) => [p.sku.toUpperCase(), p]));
  const parentIndex = new Map();
  for (const edge of catalog.bomEdges) {
    const child = String(edge.child).toUpperCase();
    if (!parentIndex.has(child)) parentIndex.set(child, []);
    parentIndex.get(child).push(edge);
  }

  const amlMatches = catalog.aml.filter((a) => String(a.mpn).toUpperCase() === mpnClean);
  const internalPns = [...new Set(amlMatches.map((a) => String(a.internal_pn).toUpperCase()))];
  const mpnInfo = catalog.mpns[mpnClean] || { mpn: mpnClean, lifecycle: 'EOL', manufacturer: 'Unknown', unit_price_eur: 5, monthly_demand: 200 };

  let minAltActive = internalPns.length ? Infinity : 0;
  for (const ipn of internalPns) {
    const alts = catalog.aml.filter((a) => {
      const aMpn = String(a.mpn).toUpperCase();
      if (String(a.internal_pn).toUpperCase() !== ipn || aMpn === mpnClean) return false;
      const st = catalog.mpns[aMpn]?.lifecycle || 'Active';
      return st === 'Active';
    });
    minAltActive = Math.min(minAltActive, alts.length);
  }
  const altSourcesCount = Number.isFinite(minAltActive) ? minAltActive : 0;

  const affectedMap = new Map();
  const paths = [];
  let cycleDetected = false;

  function dfs(nodeId, chain, visited) {
    const edges = parentIndex.get(nodeId) || [];
    for (const edge of edges) {
      const parentId = String(edge.parent).toUpperCase();
      if (visited.has(parentId)) {
        cycleDetected = true;
        continue;
      }
      const nextChain = [...chain, parentId];
      if (edge.parentType === 'product' || productMap.has(parentId)) {
        const prod = productMap.get(parentId);
        if (prod) {
          paths.push({
            mpn: mpnClean,
            internalPn: chain[0],
            assemblies: chain.slice(1),
            sku: prod.sku,
            grossMargin: Number(prod.gross_margin),
          });
          if (!affectedMap.has(prod.sku)) {
            affectedMap.set(prod.sku, {
              sku: prod.sku,
              name: prod.name || prod.sku,
              margin_at_risk: Number(prod.gross_margin),
              assembly_path: chain.slice(1),
            });
          }
        }
      } else {
        const nextVisited = new Set(visited);
        nextVisited.add(parentId);
        dfs(parentId, nextChain, nextVisited);
      }
    }
  }

  for (const ipn of internalPns) {
    dfs(ipn, [ipn], new Set([ipn]));
  }

  const maxCatalogMargin = Math.max(15000, ...catalog.products.map((p) => Number(p.gross_margin) || 0));
  const affectedSkus = [...affectedMap.values()].map((item) => {
    const crit = computeCriticality(mpnInfo.lifecycle, altSourcesCount, item.margin_at_risk, maxCatalogMargin);
    return {
      sku: item.sku,
      trigger_mpn: mpnClean,
      assembly_path: item.assembly_path,
      margin_at_risk: item.margin_at_risk,
      criticality_score: crit.score,
      alt_sources_count: altSourcesCount,
      status: crit.status,
    };
  });

  const totalRiskEur = affectedSkus.reduce((acc, s) => acc + s.margin_at_risk, 0);
  return {
    mpn: mpnClean,
    lifecycle: mpnInfo.lifecycle,
    manufacturer: mpnInfo.manufacturer,
    internalPns,
    altSourcesCount,
    affectedSkus,
    paths,
    totalRiskEur,
    cycleDetected,
  };
}

export function evaluateCatalogRisk(catalog) {
  const flaggedMpns = Object.values(catalog.mpns).filter(
    (m) => m.lifecycle === 'EOL' || m.lifecycle === 'Obsolete' || m.lifecycle === 'NRND',
  );
  const eolCount = flaggedMpns.filter((m) => m.lifecycle === 'EOL' || m.lifecycle === 'Obsolete').length;

  const skuUniqueMargin = new Map();
  const rows = [];
  const logs = [];
  let cycleDetected = false;
  let estimatedLtbCapitalEur = 0;

  let sec = 2;
  const ts = () => {
    const s = String(sec % 60).padStart(2, '0');
    const m = String(31 + Math.floor(sec / 60)).padStart(2, '0');
    sec += 3;
    return `18:${m}:${s}`;
  };

  for (const m of flaggedMpns) {
    const tr = traverseBomUpward(catalog, m.mpn);
    if (tr.cycleDetected) cycleDetected = true;
    const isHardEol = m.lifecycle === 'EOL' || m.lifecycle === 'Obsolete';

    if (tr.affectedSkus.length > 0 && isHardEol) {
      const demand = Number(m.monthly_demand) || 300;
      const price = Number(m.unit_price_eur) || 5.0;
      estimatedLtbCapitalEur += Math.round(demand * 7.5 * price);
    }

    if (isHardEol) {
      logs.push(`[${ts()}] [Webhook] PDN/EOL alert received: ${m.mpn} (${m.manufacturer}, ${m.lifecycle}).`);
      logs.push(`[${ts()}] [CrewAI] Semantic MPN verified -> ${m.mpn}. Calling deterministic bom_engine.`);
    }

    for (const item of tr.affectedSkus) {
      rows.push(item);
      if (isHardEol) {
        skuUniqueMargin.set(item.sku, Math.max(skuUniqueMargin.get(item.sku) || 0, item.margin_at_risk));
        logs.push(
          `[${ts()}] [BOM/SQL] DAG path ${tr.internalPns[0] || 'N/A'} -> ${item.assembly_path.join(' -> ')} -> ${item.sku}. IEC=${item.criticality_score}.`,
        );
      }
    }

    if (isHardEol && tr.affectedSkus.length > 0) {
      logs.push(
        `[${ts()}] [Alert] ${m.mpn} exposes ${tr.totalRiskEur.toFixed(2)} EUR across ${tr.affectedSkus.length} SKU(s). Alt AML=${tr.altSourcesCount}.`,
      );
    }
  }

  // Sort rows by criticality descending, then margin descending
  rows.sort((a, b) => b.criticality_score - a.criticality_score || b.margin_at_risk - a.margin_at_risk);
  const totalRiskEur = [...skuUniqueMargin.values()].reduce((a, b) => a + b, 0);

  if (logs.length === 0) {
    logs.push('[18:31:00] [CrewAI] Catalog scan complete. Zero critical EOL/Obsolete triggers active.');
  } else {
    logs.push(`[${ts()}] [CrewAI] Risk consolidation complete. Deduplicated P&L exposure: ${totalRiskEur.toFixed(2)} EUR.`);
  }

  return {
    total_risk_eur: Number(totalRiskEur.toFixed(2)),
    active_alerts: eolCount,
    blocked_skus_count: skuUniqueMargin.size,
    estimated_ltb_capital_eur: Number(estimatedLtbCapitalEur.toFixed(2)),
    affected_skus: rows,
    agent_logs: logs,
    cycle_detected: cycleDetected,
  };
}

export function computeLtbVsFff(input) {
  const Dm = Number(input.monthly_demand);
  const cv = Number(input.demand_cv ?? 0.2);
  const Tr = Number(input.redesign_months);
  const Lm = Number(input.lead_time_months ?? 2);
  const I0 = Number(input.current_stock_units ?? 0);
  const Pltb = Number(input.ltb_unit_price_eur);
  const Pfff = Number(input.fff_unit_price_eur);
  const Nre = Number(input.redesign_nre_eur ?? 0);
  const wh = Number(input.annual_holding_wacc_rate ?? 0.28);
  const Mm = Number(input.monthly_margin_at_risk_eur ?? 0);
  const Z = Number(input.service_level_z ?? 2.054);

  if (!(Dm > 0 && Tr > 0 && Pltb > 0 && Pfff > 0 && cv >= 0 && cv <= 1 && Lm >= 0 && I0 >= 0 && Nre >= 0 && wh >= 0 && Mm >= 0)) {
    return null;
  }

  const horizon = Tr + Lm;
  const qBase = Dm * horizon;
  const ssLtb = Z * (cv * Dm) * Math.sqrt(horizon);
  const qLtb = Math.max(0, Math.ceil(qBase + ssLtb - I0));
  const wcLtb = qLtb * Pltb;
  const tcLtb = wcLtb * (1 + ((wh / 2) * (Tr / 12)));

  const tStock = I0 / Dm;
  const gapMonths = Math.max(0, Tr - tStock);
  const fffBaseOnly = Nre + qBase * Pfff;
  const tcFff = fffBaseOnly + gapMonths * Mm;

  let verdict = 'EXECUTE_LTB';
  if (gapMonths > 0 && fffBaseOnly < tcLtb) {
    verdict = 'HYBRID_BRIDGE';
  } else if (tcFff < tcLtb) {
    verdict = 'REDESIGN_FFF';
  }

  const savingsEur = Math.abs(tcLtb - tcFff);
  const breakevenMonths = Pltb > Pfff ? Number((Nre / (Dm * (Pltb - Pfff))).toFixed(1)) : null;

  return {
    safety_stock_units: Math.ceil(ssLtb),
    ltb_order_qty: qLtb,
    ltb_working_capital_eur: Number(wcLtb.toFixed(2)),
    ltb_total_cost_eur: Number(tcLtb.toFixed(2)),
    fff_total_cost_eur: Number(tcFff.toFixed(2)),
    stock_gap_months: Number(gapMonths.toFixed(1)),
    savings_eur: Number(savingsEur.toFixed(2)),
    breakeven_months: breakevenMonths,
    verdict,
  };
}

export function extractMpnFromPdnText(text, knownMpns = []) {
  const upper = String(text || '').toUpperCase();
  for (const mpn of knownMpns) {
    if (upper.includes(mpn.toUpperCase())) return mpn.toUpperCase();
  }
  const m = upper.match(/(?:MPN|PART NUMBER|TARGET PART NUMBER)[:\s#-]+([A-Z0-9][A-Z0-9._-]{3,32})/);
  return m ? m[1] : null;
}

function splitCsvLine(line) {
  const out = [];
  let cur = '';
  let inQuotes = false;
  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') {
        cur += '"';
        i += 1;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === ',' && !inQuotes) {
      out.push(cur.trim());
      cur = '';
    } else {
      cur += ch;
    }
  }
  out.push(cur.trim());
  return out;
}

export function parseBomCsv(csvText) {
  const lines = String(csvText || '')
    .replace(/^\uFEFF/, '')
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter(Boolean);

  if (lines.length < 2) {
    return { ok: false, errorType: 'empty', missing: [] };
  }

  const headers = splitCsvLine(lines[0]);
  const missing = REQUIRED_CSV_COLUMNS.filter((c) => !headers.includes(c));
  if (missing.length > 0) {
    return { ok: false, errorType: 'missing', missing };
  }

  const idx = Object.fromEntries(headers.map((h, i) => [h, i]));
  const prodMap = new Map();
  const edgeSet = new Set();
  const bomEdges = [];
  const amlSet = new Set();
  const aml = [];
  const mpns = {};

  const validLifecycles = new Set(['Active', 'NRND', 'EOL', 'Obsolete']);

  for (let r = 1; r < lines.length; r += 1) {
    const cols = splitCsvLine(lines[r]);
    if (cols.length < REQUIRED_CSV_COLUMNS.length) continue;

    const sku = (cols[idx.End_Product_SKU] || '').trim().toUpperCase();
    const rawMargin = Number.parseFloat(cols[idx.End_Product_Margin]);
    const asm = (cols[idx.Assembly_PN] || '').trim().toUpperCase();
    const comp = (cols[idx.Component_PN] || '').trim().toUpperCase();
    const qty = Math.max(1, Number.parseInt(cols[idx.Quantity_per_Assembly], 10) || 1);
    const mfg = (cols[idx.Manufacturer] || 'Unknown').trim();
    const mpn = (cols[idx.Manufacturer_PN] || '').trim().toUpperCase();
    let life = (cols[idx.Lifecycle] || 'Active').trim();
    if (!validLifecycles.has(life)) life = 'Active';

    if (!sku || !asm || !comp || !mpn) continue;
    const grossMargin = Number.isFinite(rawMargin) && rawMargin > 1 ? rawMargin : Number.isFinite(rawMargin) ? rawMargin * 10000 : 5000;

    if (!prodMap.has(sku)) {
      prodMap.set(sku, { sku, name: `${sku} System`, gross_margin: grossMargin });
    }

    const e1Key = `${sku}|${asm}`;
    if (!edgeSet.has(e1Key)) {
      edgeSet.add(e1Key);
      bomEdges.push({ parent: sku, parentType: 'product', child: asm, qty: 1 });
    }
    const e2Key = `${asm}|${comp}`;
    if (!edgeSet.has(e2Key)) {
      edgeSet.add(e2Key);
      bomEdges.push({ parent: asm, parentType: 'assembly', child: comp, qty });
    }

    const amlKey = `${comp}|${mpn}`;
    if (!amlSet.has(amlKey)) {
      amlSet.add(amlKey);
      aml.push({ internal_pn: comp, mpn, manufacturer: mfg, pref: 'Primary' });
    }

    if (!mpns[mpn] || LIFECYCLE_SCORE[life] > LIFECYCLE_SCORE[mpns[mpn].lifecycle]) {
      mpns[mpn] = { mpn, manufacturer: mfg, lifecycle: life, unit_price_eur: 6.5, monthly_demand: 350 };
    }
  }

  if (prodMap.size === 0) {
    return { ok: false, errorType: 'empty', missing: [] };
  }

  const catalog = {
    products: [...prodMap.values()],
    bomEdges,
    aml,
    mpns,
    defaultLtb: PRESET_SCENARIOS['drone-capacitor'].catalog.defaultLtb,
  };
  const alerts = Object.values(mpns).filter((m) => m.lifecycle === 'EOL' || m.lifecycle === 'Obsolete').length;

  return {
    ok: true,
    catalog,
    stats: { skus: prodMap.size, comps: Object.keys(mpns).length, alerts },
  };
}
