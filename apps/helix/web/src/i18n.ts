export type Language = 'es' | 'en';

export interface AgentInfo {
  id: string;
  name: string;
  cell: 'direction' | 'construction' | 'assurance' | 'delivery';
  icon: string;
  role: string;
  hasVeto: boolean;
}

export const SQUAD_AGENTS: AgentInfo[] = [
  { id: '01-orchestrator', name: 'Orquestador', cell: 'direction', icon: '🎯', role: 'Triaje determinista y entrega', hasVeto: false },
  { id: '02-product-analyst', name: 'Product Analyst', cell: 'direction', icon: '🧭', role: 'Entrevista y spec.md', hasVeto: false },
  { id: '03-architect', name: 'Arquitecto', cell: 'direction', icon: '🏛️', role: 'Constitución, ADR y módulos', hasVeto: false },
  { id: '04-ux-ui', name: 'Diseñador UX/UI', cell: 'construction', icon: '🎨', role: 'Tokens visuales y design.md', hasVeto: false },
  { id: '05-frontend', name: 'Frontend Lead', cell: 'construction', icon: '⚡', role: 'React 19, SPA y UI limpia', hasVeto: false },
  { id: '06-backend-data', name: 'Backend & Datos', cell: 'construction', icon: '🗄️', role: 'Python, Pydantic y SQL', hasVeto: false },
  { id: '07-apis-integrations', name: 'APIs & MCP', cell: 'construction', icon: '🔌', role: 'Conectores y webhooks', hasVeto: false },
  { id: '08-media-i18n', name: 'Media & i18n', cell: 'construction', icon: '🎬', role: 'Paridad bilingüe y docs', hasVeto: false },
  { id: '09-monetization', name: 'Monetización & PLG', cell: 'construction', icon: '💳', role: 'Checkout, precios y GA4', hasVeto: false },
  { id: '10-security-privacy', name: 'Seguridad & RLS', cell: 'assurance', icon: '🛡️', role: 'Aislamiento y secretos', hasVeto: true },
  { id: '11-qa-verifier', name: 'QA Verifier', cell: 'assurance', icon: '✅', role: 'Verification gates deterministas', hasVeto: true },
  { id: '12-release-devops', name: 'Release & DevOps', cell: 'delivery', icon: '🚀', role: 'Checkpoints, rollback y SemVer', hasVeto: false },
];

export const TRANSLATIONS = {
  es: {
    backToDatalaria: '← Datalaria',
    tagline: 'La spec es el ADN de tu app; los agentes solo la expresan',
    cockpitTitle: 'Helix Spec Builder & 12-Agent Cockpit',
    earlyBirdBadge: 'Lanzamiento Enero 2027 · Waitlist 19 €',
    loadExampleLabel: '⚡ Cargar ejemplo:',
    exampleStatic: 'Calculadora Estática',
    exampleSaas: 'SaaS React + Supabase RLS',
    exampleQuant: 'Motor Cuantitativo Python',
    exampleMargin: 'Caso Real #2: MarginGuard B2B',

    // Pilares
    p1Title: '1. Identidad, Problema y Usuario',
    p1Slug: 'Slug del Proyecto (identificador kebab-case):',
    p1Name: 'Nombre Público de la Aplicación:',
    p1Problem: 'Problema Crítico que Resuelve:',
    p1User: 'Usuario Objetivo y Contexto de Negocio:',

    p2Title: '2. Alcance Negativo y Non-Goals (Anti-Vibe-Debt)',
    p2Help: 'Selecciona o redacta qué está terminantemente prohibido construir:',
    nonGoal1: 'Cero llamadas a APIs de pago o servicios cerrados en el cliente',
    nonGoal2: 'No almacenar credenciales ni datos privados sin cifrado',
    nonGoal3: 'Prohibido reescribir la arquitectura sin aprobación formal de spec',
    p2Custom: 'Otros Non-Goals específicos:',

    p3Title: '3. Arquitectura, Superficies y Diseño UX/UI',
    p3SurfacesHelp: 'Marca las superficies técnicas afectadas (determina el triaje de agentes):',
    surfaceDocs: 'Documentación / Guías',
    surfaceUi: 'Diseño UX / UI Tokens',
    surfaceFrontend: 'Código Frontend (React/Web)',
    surfaceBackend: 'Backend / Python / Lógica',
    surfaceDataSql: 'Base de Datos / SQL / RLS',
    surfaceApis: 'APIs Externas / Webhooks',
    surfaceMediaI18n: 'Bilingüismo i18n / Media',
    surfaceMonetization: 'Monetización / Checkout',
    surfaceAuthSecurity: 'Autenticación / Seguridad',
    p3Preset: 'Preset de Diseño Visual (design.md):',
    presetDataDense: 'Executive Data-Dense (#0b0f17 — Estándar B2B)',
    presetMinimal: 'Minimal Utility (Foco en 1 pantalla)',
    presetEditorial: 'Editorial Knowledge (Lectura y documentación)',
    presetPlayful: 'Consumer Playful (Interacciones vibrantes)',
    presetMobile: 'Mobile-First Field (Uso vertical táctil)',

    p4Title: '4. Invariantes Innegociables (INV-*)',
    p4Help: 'Invariantes formales que ningún agente puede violar (mínimo 3 recomendadas):',
    invPlaceholder: 'Escribe una invariante por línea, ej: INV-APP-1: Cero fugas de claves en static/',
    suggestInvariants: '+ Añadir 3 Invariantes Recomendadas',

    p5Title: '5. Verification Gates y Rollback',
    p5GateHelp: 'Comando automatizado que 11-qa-verifier ejecutará (debe salir con código 0):',
    p5FilesEstimated: 'Archivos aproximados a modificar:',

    // Cockpit
    scoreTitle: 'SpecQualityScore Determinista',
    vibeDebtRisk: 'Riesgo de Vibe-Debt:',
    vibeRiskLow: 'Bajo (Ingeniería Robusta)',
    vibeRiskMedium: 'Moderado (Faltan Contratos)',
    vibeRiskHigh: 'Crítico (Alto riesgo de colapso)',
    triageCardTitle: 'Tarjeta de Triaje Canónica (6 Líneas)',
    copyTriageCard: 'Copiar Tarjeta',
    copiedBadge: '¡Copiado!',

    // Tabs
    tabSquad: '👥 Escuadrón (12 Agentes)',
    tabModeA: '📦 Modo A: Kit SDD (.zip)',
    tabModeB: '⚡ Modo B: Mega-Prompt',
    tabPricing: '🚀 Escalar a Core Kit',

    squadActiveCount: 'Roles Convocados en Contexto',
    squadBenchedCount: 'En Banquillo (Ahorro de Tokens)',
    vetoBadge: 'VETO VINCULANTE',

    downloadZipBtn: '⬇️ Descargar Kit Inicial (.zip)',
    downloadZipHelp: 'Empaquetado 100% en memoria de tu navegador (AGENTS.md, _constitution.md, spec.md, design.md, ROADMAP.md). Cero envío de datos.',
    previewFile: 'Previsualizar archivo:',

    copyPromptBtn: '📋 Copiar Mega-Prompt en 1 Clic',
    promptHelp: 'Prompt multi-rol listo para pegar en cualquier chat de IA (Antigravity, Claude, ChatGPT, Gemini, Cursor) sin requerir API key.',

    pricingTitle: 'La Escalera de Valor de Datalaria Helix',
    planSandbox: 'Sandbox Web (Gratis)',
    planSandboxDesc: 'Generador de specs, simulador de triaje y exportador de Mega-Prompt client-side.',
    planStarter: 'Starter Kit (9 €)',
    planStarterDesc: 'Guía metodológica SDD en PDF HD + 2 agentes esenciales (Orquestador y Product Analyst).',
    planCore: 'Core Kit (19 € Early-Bird / 39 € PVP)',
    planCoreDesc: 'Escuadrón completo de 12 Agentes, CLI helix sin dependencias, 3 Blueprints y adaptadores para Antigravity, Claude, Cursor y Codex.',
    joinWaitlistTitle: 'Únete a la Lista de Espera Prioritaria (Early-Bird 19 €)',
    emailPlaceholder: 'tu.email@empresa.com',
    joinWaitlistBtn: 'Reservar con 50% de Descuento →',
    waitlistSuccess: '¡Registrado con éxito! Te avisaremos para el lanzamiento en enero.',
  },
  en: {
    backToDatalaria: '← Datalaria',
    tagline: 'The spec is your app\'s DNA; agents merely express it',
    cockpitTitle: 'Helix Spec Builder & 12-Agent Cockpit',
    earlyBirdBadge: 'January 2027 Launch · Waitlist 19 €',
    loadExampleLabel: '⚡ Load example:',
    exampleStatic: 'Static Calculator',
    exampleSaas: 'SaaS React + Supabase RLS',
    exampleQuant: 'Python Quant Engine',
    exampleMargin: 'Case Study #2: MarginGuard B2B',

    // Pillars
    p1Title: '1. Identity, Problem & User Context',
    p1Slug: 'Project Slug (kebab-case identifier):',
    p1Name: 'Application Public Name:',
    p1Problem: 'Critical Problem Solved:',
    p1User: 'Target User & Business Context:',

    p2Title: '2. Negative Scope & Non-Goals (Anti-Vibe-Debt)',
    p2Help: 'Select or write what is strictly forbidden to build:',
    nonGoal1: 'Zero paid API calls or locked third-party services on client-side',
    nonGoal2: 'Never store unencrypted credentials or private user data',
    nonGoal3: 'Forbidden to rewrite architecture without formal approved spec',
    p2Custom: 'Additional specific Non-Goals:',

    p3Title: '3. Architecture, Technical Surfaces & UX/UI',
    p3SurfacesHelp: 'Check technical surfaces touched (determines agent triage):',
    surfaceDocs: 'Documentation / Guides',
    surfaceUi: 'UX / UI Tokens',
    surfaceFrontend: 'Frontend Code (React/Web)',
    surfaceBackend: 'Backend / Python / Logic',
    surfaceDataSql: 'Database / SQL / RLS',
    surfaceApis: 'External APIs / Webhooks',
    surfaceMediaI18n: 'Bilingual i18n / Media',
    surfaceMonetization: 'Monetization / Checkout',
    surfaceAuthSecurity: 'Authentication / Security',
    p3Preset: 'Visual Design Preset (design.md):',
    presetDataDense: 'Executive Data-Dense (#0b0f17 — B2B Standard)',
    presetMinimal: 'Minimal Utility (Single screen focus)',
    presetEditorial: 'Editorial Knowledge (Deep reading & docs)',
    presetPlayful: 'Consumer Playful (Vibrant interactions)',
    presetMobile: 'Mobile-First Field (Touch vertical view)',

    p4Title: '4. Non-Negotiable Invariants (INV-*)',
    p4Help: 'Formal invariants no agent can ever bypass (3+ recommended):',
    invPlaceholder: 'One invariant per line, e.g.: INV-APP-1: Zero leaked keys in static/',
    suggestInvariants: '+ Add 3 Recommended Invariants',

    p5Title: '5. Verification Gates & Rollback',
    p5GateHelp: 'Automated command 11-qa-verifier will execute (must exit code 0):',
    p5FilesEstimated: 'Estimated files to touch:',

    // Cockpit
    scoreTitle: 'Deterministic SpecQualityScore',
    vibeDebtRisk: 'Vibe-Debt Risk:',
    vibeRiskLow: 'Low (Engineered & Robust)',
    vibeRiskMedium: 'Moderate (Missing Contracts)',
    vibeRiskHigh: 'Critical (High risk of breakage)',
    triageCardTitle: 'Canonical Triage Card (6 Lines)',
    copyTriageCard: 'Copy Card',
    copiedBadge: 'Copied!',

    // Tabs
    tabSquad: '👥 Squad (12 Agents)',
    tabModeA: '📦 Mode A: SDD Kit (.zip)',
    tabModeB: '⚡ Mode B: Mega-Prompt',
    tabPricing: '🚀 Upgrade to Core Kit',

    squadActiveCount: 'Active Roles in Context',
    squadBenchedCount: 'On Bench (Token Savings)',
    vetoBadge: 'BINDING VETO',

    downloadZipBtn: '⬇️ Download Starter Kit (.zip)',
    downloadZipHelp: 'Packaged 100% in your browser memory (AGENTS.md, _constitution.md, spec.md, design.md, ROADMAP.md). Zero data sent to servers.',
    previewFile: 'Preview file:',

    copyPromptBtn: '📋 Copy Mega-Prompt (1-Click)',
    promptHelp: 'Ready-to-paste multi-agent prompt for any AI chat (Antigravity, Claude, ChatGPT, Gemini, Cursor) without API keys.',

    pricingTitle: 'The Datalaria Helix Value Ladder',
    planSandbox: 'Web Sandbox (Free)',
    planSandboxDesc: 'Client-side spec builder, triage simulator, and Mega-Prompt exporter.',
    planStarter: 'Starter Kit (9 €)',
    planStarterDesc: 'SDD HD PDF methodology guide + 2 core agents (Orchestrator & Product Analyst).',
    planCore: 'Core Kit (19 € Early-Bird / 39 € Retail)',
    planCoreDesc: 'Full 12-Agent squad, zero-dependency helix CLI, 3 Blueprints, and pre-compiled adapters for Antigravity, Claude, Cursor & Codex.',
    joinWaitlistTitle: 'Join Priority Waitlist (Early-Bird 19 €)',
    emailPlaceholder: 'you@company.com',
    joinWaitlistBtn: 'Claim 50% Off Waitlist →',
    waitlistSuccess: 'Successfully registered! We will notify you for the January launch.',
  },
};
