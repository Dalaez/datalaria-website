/**
 * Motor determinista de Triaje, Puntuación de Spec y Generador de Artefactos SDD.
 * Réplica idéntica client-side de las invariantes de ops/helix/cli.py.
 */

import { Language } from './i18n';

export interface ProjectState {
  slug: string;
  name: string;
  problem: string;
  targetUser: string;
  selectedNonGoals: string[];
  customNonGoals: string;
  surfaces: string[];
  designPreset: string;
  invariants: string[];
  customInvariants: string;
  gateCommand: string;
  estimatedFiles: number;
}

export const SURFACE_BUILDER_MAP: Record<string, string> = {
  docs: '08-media-i18n',
  ui: '04-ux-ui',
  frontend: '05-frontend',
  backend: '06-backend-data',
  data_sql: '06-backend-data',
  apis: '07-apis-integrations',
  media_i18n: '08-media-i18n',
  monetization: '09-monetization',
  auth_security: '06-backend-data',
};

export const DEFAULT_EXAMPLES: Record<string, ProjectState> = {
  static: {
    slug: 'mortgage-calculator',
    name: 'Simulador Hipotecario & Préstamos Pro',
    problem: 'Los compradores de vivienda necesitan comparar escenarios de hipotecas fijas vs variables con amortización anticipada sin introducir datos en portales bancarios con publicidad.',
    targetUser: 'Compradores particulares y asesores inmobiliarios independientes.',
    selectedNonGoals: [
      'Cero llamadas a APIs de pago o servicios cerrados en el cliente',
      'No almacenar credenciales ni datos privados sin cifrado',
    ],
    customNonGoals: 'No requiere servidor backend; opera 100% en memoria del navegador.',
    surfaces: ['ui', 'frontend', 'docs'],
    designPreset: 'Minimal Utility (Foco en 1 pantalla)',
    invariants: [
      'INV-MORT-1: Tiempo de respuesta del slider de cálculo < 16ms (60 FPS)',
      'INV-MORT-2: Cero recargas de página para simular amortizaciones',
      'INV-MORT-3: Precisión de redondeo financiero normalizada a 2 decimales',
    ],
    customInvariants: '',
    gateCommand: 'npm run lint && npm run test && npm run build',
    estimatedFiles: 3,
  },
  saas: {
    slug: 'b2b-billing-hub',
    name: 'Portal Multi-Tenant de Facturación B2B',
    problem: 'Las micro-empresas pierden horas emitiendo facturas recurrentes y conciliando cobros por falta de un panel multi-inquilino simple y seguro.',
    targetUser: 'Equipos de administración y autónomos B2B.',
    selectedNonGoals: [
      'Cero llamadas a APIs de pago o servicios cerrados en el cliente',
      'No almacenar credenciales ni datos privados sin cifrado',
      'Prohibido reescribir la arquitectura sin aprobación formal de spec',
    ],
    customNonGoals: 'No implementar contabilidad completa; solo facturación y cobros.',
    surfaces: ['ui', 'frontend', 'backend', 'data_sql', 'auth_security', 'monetization'],
    designPreset: 'Executive Data-Dense (#0b0f17 — Estándar B2B)',
    invariants: [
      'INV-BILL-1: Tablas protegidas obligatoriamente con ENABLE ROW LEVEL SECURITY',
      'INV-BILL-2: Claves privadas de pasarela aisladas en serverless, nunca en cliente',
      'INV-BILL-3: Cero mezcla de datos entre tenants (auth.uid() = tenant_id)',
    ],
    customInvariants: '',
    gateCommand: 'pytest tests/ -v && npm run lint && npm run build',
    estimatedFiles: 8,
  },
  quant: {
    slug: 'portfolio-risk-engine',
    name: 'Motor Cuantitativo de Riesgo de Portafolios',
    problem: 'Analistas financieros necesitan calcular VaR paramétrico y simulaciones Monte Carlo reproducibles con modelos matemáticos auditables y sin hojas de cálculo opacas.',
    targetUser: 'Analistas de riesgo, family offices y gestores de fondos cuantitativos.',
    selectedNonGoals: [
      'Cero llamadas a APIs de pago o servicios cerrados en el cliente',
      'Prohibido reescribir la arquitectura sin aprobación formal de spec',
    ],
    customNonGoals: 'No ejecutar trading en vivo; solo simulación y métricas de riesgo.',
    surfaces: ['backend', 'docs'],
    designPreset: 'Executive Data-Dense (#0b0f17 — Estándar B2B)',
    invariants: [
      'INV-RISK-1: Todos los modelos validados al 100% con Pydantic v2 BaseModel',
      'INV-RISK-2: Funciones matemáticas puras deterministas con semilla fija',
      'INV-RISK-3: Cero pérdida de precisión en operaciones de coma flotante',
    ],
    customInvariants: '',
    gateCommand: 'python -m pytest tests/ -v',
    estimatedFiles: 4,
  },
  margin: {
    slug: 'margin-guard',
    name: 'MarginGuard B2B — Simulador de Pricing & Breakeven',
    problem: 'Directores comerciales y consultores de estrategia necesitan calcular el volumen adicional necesario para compensar descuentos y evitar la destrucción irreversible de margen EBITDA.',
    targetUser: 'Directores comerciales, comités de precios y consultores de estrategia B2B.',
    selectedNonGoals: [
      'Cero llamadas a APIs de pago o servicios cerrados en el cliente',
      'No almacenar credenciales ni datos privados sin cifrado',
      'Prohibido reescribir la arquitectura sin aprobación formal de spec',
    ],
    customNonGoals: 'Cero backend, bases de datos o servicios cloud externos (100% client-side en navegador).',
    surfaces: ['ui', 'frontend', 'backend', 'docs'],
    designPreset: 'Minimal Utility (Foco en 1 pantalla)',
    invariants: [
      'INV-MARGIN-1: Incremento de volumen breakeven delta_V = d / (m - d) para d < m',
      'INV-MARGIN-2: Zona de destrucción de valor si d >= m (value_destruction_zone: true, volumen null)',
      'INV-MARGIN-3: Ejecución 100% autónoma en navegador local sin llamadas de red',
      'INV-MARGIN-4: Paridad bilingüe ES/EN y tiempo de recálculo < 16ms en sliders',
    ],
    customInvariants: '',
    gateCommand: 'python -m pytest engine.py -v && npm run lint',
    estimatedFiles: 4,
  },
};

export interface TriageResult {
  size: 'XS' | 'S' | 'M' | 'L' | 'XL';
  activeAgents: string[];
  benchedAgents: string[];
  cardLines: string[];
  gate: string;
}

export function calculateTriage(state: ProjectState): TriageResult {
  const surfaces = state.surfaces.length > 0 ? state.surfaces : ['docs'];
  const files = Math.max(1, state.estimatedFiles || 1);

  // 1. Talla
  let size: 'XS' | 'S' | 'M' | 'L' | 'XL' = 'XS';
  if (surfaces.length >= 4 || files >= 8) {
    size = 'L';
  } else if (surfaces.length >= 2 || files > 3) {
    size = 'M';
  } else if (files > 1) {
    size = 'S';
  }

  // 2. Selección de agentes
  const activeSet = new Set<string>(['01-orchestrator', '11-qa-verifier']);

  for (const s of surfaces) {
    if (SURFACE_BUILDER_MAP[s]) {
      activeSet.add(SURFACE_BUILDER_MAP[s]);
    }
  }

  if (size === 'M' || size === 'L' || size === 'XL') {
    activeSet.add('03-architect');
    activeSet.add('12-release-devops');
  }
  if (size === 'L' || size === 'XL') {
    activeSet.add('02-product-analyst');
    activeSet.add('04-ux-ui');
  }

  // Disparadores innegociables
  if (surfaces.some((s) => ['auth_security', 'data_sql', 'monetization'].includes(s))) {
    activeSet.add('10-security-privacy');
  }
  if (surfaces.some((s) => ['ui', 'frontend'].includes(s))) {
    activeSet.add('04-ux-ui');
  }
  if (surfaces.includes('media_i18n')) {
    activeSet.add('08-media-i18n');
  }
  if (surfaces.includes('monetization')) {
    activeSet.add('09-monetization');
  }

  const allAgentIds = [
    '01-orchestrator', '02-product-analyst', '03-architect', '04-ux-ui',
    '05-frontend', '06-backend-data', '07-apis-integrations', '08-media-i18n',
    '09-monetization', '10-security-privacy', '11-qa-verifier', '12-release-devops',
  ];

  const activeAgents = allAgentIds.filter((id) => activeSet.has(id));
  const benchedAgents = allAgentIds.filter((id) => !activeSet.has(id));

  const surfacesStr = surfaces.join(', ');
  const activeStr = activeAgents.join(', ');
  const benchedStr = benchedAgents.length ? benchedAgents.join(', ') : 'Ninguno (Escuadrón Completo)';
  const gate = state.gateCommand || 'python -m pytest && npm run build';
  const approval = size === 'L' || size === 'XL' ? 'SÍ' : 'NO';

  const cardLines = [
    `TRIAGE HELIX · Hito 1.0 · Talla: ${size}`,
    `Superficies afectadas: ${surfacesStr}`,
    `Roles activados (${activeAgents.length} de 12): ${activeStr}`,
    `Roles en banquillo: ${benchedStr}`,
    `Verification Gate: ${gate}`,
    `Presupuesto y Gobernanza: Máx. 2 intentos por gate · Checkpoint sdd-checkpoint-pre-1.0 · Aprobación humana previa: ${approval}`,
  ];

  return {
    size,
    activeAgents,
    benchedAgents,
    cardLines,
    gate,
  };
}

export interface SpecQualityResult {
  totalScore: number;
  pillars: {
    problem: number;
    nongoals: number;
    contracts: number;
    invariants: number;
    gates: number;
  };
  vibeDebtRisk: number;
  passed: boolean;
  recommendations: string[];
}

export function calculateSpecQuality(state: ProjectState): SpecQualityResult {
  let p1 = 0;
  const recs: string[] = [];

  // P1: Problema y Usuario (20)
  if (state.problem.trim().length >= 15) p1 += 10;
  else recs.push('Describe con mayor detalle el problema crítico (mín. 15 caracteres).');
  if (state.targetUser.trim().length >= 5) p1 += 10;
  else recs.push('Define quién es el usuario objetivo del sistema.');

  // P2: Non-Goals (20)
  let p2 = 0;
  const nonGoalsCount = state.selectedNonGoals.length + (state.customNonGoals.trim() ? 1 : 0);
  if (nonGoalsCount >= 2) p2 = 20;
  else if (nonGoalsCount === 1) {
    p2 = 10;
    recs.push('Añade al menos un Non-Goal adicional para blindar el alcance.');
  } else {
    recs.push('Define qué NO construirá el sistema para evitar Vibe Debt.');
  }

  // P3: Contratos & Arquitectura (20)
  let p3 = 0;
  if (state.surfaces.length >= 1) p3 += 10;
  if (state.designPreset.trim().length > 0) p3 += 10;

  // P4: Invariantes (20)
  let p4 = 0;
  const rawInvs = [
    ...state.invariants,
    ...state.customInvariants.split('\n').filter((l) => l.trim().length > 0),
  ];
  if (rawInvs.length >= 3) p4 = 20;
  else if (rawInvs.length >= 1) {
    p4 = 10;
    recs.push('Recomendado: declara al menos 3 invariantes formales INV-*.');
  } else {
    recs.push('Declara invariantes innegociables INV-* para dar poder de veto a QA y Seguridad.');
  }

  // P5: Verification Gates (20)
  let p5 = 0;
  if (state.gateCommand.trim().length >= 5) p5 += 10;
  if (/pytest|npm|oxlint|hugo|python|tsc|vitest|cargo/.test(state.gateCommand)) p5 += 10;
  else recs.push('Especifica un comando ejecutable concreto de verificación (ej. pytest, npm run build).');

  const totalScore = p1 + p2 + p3 + p4 + p5;
  const vibeDebtRisk = Math.max(0, 100 - totalScore);

  return {
    totalScore,
    pillars: { problem: p1, nongoals: p2, contracts: p3, invariants: p4, gates: p5 },
    vibeDebtRisk,
    passed: totalScore >= 70,
    recommendations: recs,
  };
}

export function generateSddFiles(
  state: ProjectState,
  lang: Language
): Array<{ name: string; content: string }> {
  const isEs = lang === 'es';
  const slug = state.slug || 'my-app';
  const name = state.name || (isEs ? 'Mi Aplicación SDD' : 'My SDD App');
  const triage = calculateTriage(state);
  const triageCard = triage.cardLines.join('\n');
  const allInvariants = [
    ...state.invariants,
    ...state.customInvariants.split('\n').filter((l) => l.trim().length > 0),
  ];
  const allNonGoals = [
    ...state.selectedNonGoals,
    ...(state.customNonGoals ? [state.customNonGoals] : []),
  ];

  const agentsMd = `# AGENTS.md — Sistema Operativo de Agentes de Ingeniería (${name})

> **Compatibilidad Universal:** Punto de entrada obligatorio para Antigravity, Claude Code, Cursor y GitHub Copilot.

---

## 1. PROTOCOLO DE ARRANQUE EN 3 PASOS
1. **Estado del Ecosistema:** Leer \`specs/ROADMAP.md\`.
2. **Reglas Inmutables:** Leer \`specs/_constitution.md\` (Artículos 1 al 9).
3. **Especificación Activa y Triaje:** Leer \`specs/apps/${slug}/spec.md\` y emitir la Tarjeta de Triaje.

---

## 2. BUCLE SDD ATÓMICO (INV-HELIX-1..8)
1. **Nadie verifica su propio trabajo (\`INV-HELIX-1\`):** Veto vinculado a QA y Seguridad.
2. **Triaje Bajo Demanda (\`INV-HELIX-2\`):** Cargar exclusivamente los roles activados.
3. **Control Anti-Bloat (\`INV-HELIX-8\`):** Fichas canónicas limitadas a 85 líneas.
`;

  const constitutionMd = `# CONSTITUCIÓN SDD — INVARIANTES DE INGENIERÍA v1.1.0

### Artículo 1: Fuente Única de Verdad (Spec-First)
Todo software comienza con una especificación formal. Prohibido crear código sin spec aprobada.

### Artículo 2: Topología y Límites Estrictos
El código de producción reside exclusivamente en directorios autorizados. Cero secretos en frontend.

### Artículo 3: Aislamiento de Datos y Secretos
Las variables de entorno residen en \`.env\`. Políticas RLS obligatorias en bases de datos multi-tenant.

### Artículo 4: Separación Inviolable de Construcción y Verificación
Ningún constructor aprueba su propio trabajo. Veto en 10-security-privacy y 11-qa-verifier.

### Artículo 5: Gates Deterministas y Rollback
Toda tarea supera comandos automatizados con código 0. Si falla 2 veces consecutivas, rollback automático.
`;

  const specMd = `# SPEC-APP-${slug.toUpperCase()}: ${name}

> **ID de Especificación:** \`SPEC-APP-${slug.toUpperCase()}\`  
> **Versión:** \`v0.1.0\`  
> **Estado:** \`APPROVED\`  
> **Preset Visual:** \`${state.designPreset}\`

---

## 1. Propósito y Contexto de Negocio
${state.problem}
- **Usuario Objetivo:** ${state.targetUser}

## 2. Límites y Prohibiciones (Non-Goals)
${allNonGoals.map((ng) => `- ❌ ${ng}`).join('\n')}

## 3. Arquitectura y Superficies Afectadas
- **Superficies:** ${state.surfaces.join(', ')}
- **Talla Estimada de Tareas:** \`${triage.size}\`

\`\`\`text
${triageCard}
\`\`\`

## 4. Invariantes Innegociables
${allInvariants.map((inv) => `- \`${inv}\``).join('\n')}

## 5. Verification Gates
- **Comando Obligatorio:** \`${state.gateCommand}\` (código de salida \`0\`).
`;

  const designMd = `# Especificación de Diseño UX/UI: ${name} (\`design.md\`)

> **Preset Estético:** \`${state.designPreset}\`  
> **Estándar:** WCAG 2.2 AA (Contraste >= 4.5:1)

## 1. Sistema de Tokens
- **Fondo Canvas:** \`#0b0f17\`
- **Superficie:** \`#111827\`
- **Acento Primario:** \`#6366f1\`
- **Tipografía:** \`Outfit\` (títulos), \`Inter\` (cuerpo), \`JetBrains Mono\` (métricas).

## 2. Signature Wow Moment
- Micro-interacción reactiva en < 16ms con feedback visual determinista.
`;

  const roadmapMd = `# ROADMAP.md — Hoja de Ruta y Memoria del Proyecto

## Puntero de Sesión Actual
- **Fase Activa:** Fase 1 — Inicialización del Ecosistema
- **Hito Actual:** Hito 1.0 — Arranque de ${name}
- **Último Checkpoint Verificado:** \`sdd-checkpoint-init\`

---

## Checklist de Hitos
- [x] **Hito 1.0: Especificación y Diseño Aprobados**
- [ ] **Hito 1.1: Construcción del Módulo Principal**
  - *Verification Gate:* \`${state.gateCommand}\`

---

## Registro de Bloqueos y Rollbacks (Audit Log)
| Fecha | Hito | Incidencia | Acción Tomada / Rollback | Checkpoint |
| :--- | :--- | :--- | :--- | :--- |
| - | - | Ningún bloqueo registrado | - | - |
`;

  return [
    { name: 'AGENTS.md', content: agentsMd },
    { name: 'specs/_constitution.md', content: constitutionMd },
    { name: `specs/apps/${slug}/spec.md`, content: specMd },
    { name: `specs/apps/${slug}/design.md`, content: designMd },
    { name: 'specs/ROADMAP.md', content: roadmapMd },
  ];
}

export function generateMegaPrompt(state: ProjectState, lang: Language): string {
  const isEs = lang === 'es';
  const name = state.name || (isEs ? 'Mi Aplicación SDD' : 'My SDD App');
  const triage = calculateTriage(state);
  const triageCard = triage.cardLines.join('\n');
  const allInvariants = [
    ...state.invariants,
    ...state.customInvariants.split('\n').filter((l) => l.trim().length > 0),
  ];

  return `### DIRECTIVA MAESTRA DE INGENIERÍA SDD (DATALARIA HELIX)
Actúa como el Coordinador (**01-orchestrator**) al mando del Escuadrón Datalaria Helix bajo la metodología **Spec-Driven Development (SDD)**.

---
#### 1. TARJETA DE TRIAJE OBLIGATORIA
\`\`\`text
${triageCard}
\`\`\`

---
#### 2. ESPECIFICACIÓN DEL PROYECTO
- **Aplicación:** ${name} (\`${state.slug}\`)
- **Problema Crítico:** ${state.problem}
- **Usuario Objetivo:** ${state.targetUser}
- **Preset de Diseño:** ${state.designPreset}

#### 3. LIMITACIONES (NON-GOALS)
${state.selectedNonGoals.map((ng) => `- ❌ ${ng}`).join('\n')}
${state.customNonGoals ? `- ❌ ${state.customNonGoals}` : ''}

#### 4. INVARIANTES INNEGOCIABLES (INV-*)
${allInvariants.map((inv) => `- \`${inv}\``).join('\n')}

#### 5. INSTRUCCIONES DE EJECUCIÓN
1. Convoca ÚNICAMENTE a los roles activados: ${triage.activeAgents.join(', ')}.
2. Mantén a los agentes en banquillo sin gastar tokens de contexto.
3. Al finalizar la fase de construcción, cede el turno a **11-qa-verifier** para validar el comando:
   \`${state.gateCommand}\` (código de salida 0).
4. Emite la tarjeta final **DEBRIEF HELIX** resumiendo conclusiones, riesgos y mejoras.
`;
}
