# 🧬 Datalaria Helix — Escuadrón de Ingeniería IA de 12 Agentes (`specs/squad/`)

> **Fuente Única de Verdad (`INV-HELIX-4`):** Este directorio contiene las definiciones canónicas (`AGENT_SPEC`) de los **12 roles especializados** de Datalaria Helix. Cualquier adaptador para herramientas específicas (`.agents/`, `.claude/agents/`, `.cursor/rules/`) se genera automáticamente desde estos archivos.

---

## 1. Principio Rector: Carga Bajo Demanda y Separación de Poderes

1. **Los 12 agentes son el banquillo, no la alineación simultánea (`INV-HELIX-2`):**
   - El **Orquestador (`01-orchestrator`)** evalúa cada solicitud con [`triage-rubric.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/triage-rubric.md) y activa **únicamente entre 2 y 4 agentes de media** para tareas cotidianas (`XS`, `S`, `M`).
   - En cada turno solo se leen en memoria las fichas `.md` de los agentes convocados en la **Tarjeta de Triaje**.
2. **Nadie verifica su propio trabajo (`INV-HELIX-1`):**
   - Los agentes de la **Célula de Diseño y Construcción (`04` a `09`)** tienen prohibido dar por cerrado un hito.
   - Todo cambio debe ser validado por la **Célula de Garantía (`10-security-privacy` y `11-qa-verifier`)** mediante comandos deterministas con código de salida `0`.

---

## 2. Catálogo de los 12 Agentes por Célula Operativa

### Célula 1: Dirección (Qué, Cómo y Quién)
| ID | Icono y Rol | Misión Principal | Entregable Clave | ¿Escribe Código Prod? |
| :--- | :--- | :--- | :--- | :-: |
| [`01-orchestrator`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/01-orchestrator.md) | 🎯 **Orquestador / Delivery Lead** | Único interlocutor humano, triaje `XS–XL`, enrutado de skills progresivas, federación con Scriba y custodia de `ROADMAP.md`. | Tarjeta de Triaje (6 líneas) + Puntero `ROADMAP.md` | ❌ No |
| [`02-product-analyst`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/02-product-analyst.md) | 🧭 **Product Analyst / PO** | Entrevista de negocio, problema, *non-goals*, divulgación progresiva, honestidad de datos y embudo Dual-Mode. | Sección 1 y criterios de negocio en `spec.md` | ❌ No |
| [`03-architect`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/03-architect.md) | 🏛️ **Arquitecto / Tech Lead** | Arquitectura Platform-First (Baseline), escalado coste 0 €, contratos paginados $O(page\_size)$, invariantes `INV-*` y ADRs. | `spec.md` (§2–§4), `DECISIONS.md` (`ADR-*`) | ❌ No |

### Célula 2: Diseño y Construcción (Ejecución Especializada)
| ID | Icono y Rol | Misión Principal | Entregable Clave | ¿Escribe Código Prod? |
| :--- | :--- | :--- | :--- | :-: |
| [`04-ux-ui`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md) | 🎨 **Diseñador UX/UI** | Dirección estética, Modern Web Guidance (Baseline CSS/HTML nativo), Design Tokens, Focus Mode móvil, *Wow Moment* y WCAG 2.2 AA. | `design.md` + Auditoría visual `UX_PASS` | ⚠️ Solo CSS/Tokens/Assets |
| [`05-frontend`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/05-frontend.md) | ⚡ **Ingeniero Frontend** | Implementación React 19/TS/Vanilla/Hugo fiel a `design.md`, Modern Web Guidance, Core Web Vitals (INP/LCP/CLS), PWA Gold y resiliencia móvil. | Código UI + `oxlint` y `build` en `0` | ✅ Sí (UI/Frontend) |
| [`06-backend-data`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/06-backend-data.md) | 🗄️ **Backend, Datos & Motor Cuantitativo** | Músculo matemático determinista (Python/Pydantic v2/Excel/PDF), APIs FastAPI paginadas, joins PostgREST embebidos y SQL RLS. | Motores `.py`, migraciones `.sql` y tests unitarios | ✅ Sí (Backend/Data) |
| [`07-apis-integrations`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/07-apis-integrations.md) | 🔌 **APIs, Integraciones & MCP** | Conectores externos, JWT local JWKS (`ECC P-256`), Power Query M, MCP y evaluación de WebMCP / Built-in Browser AI. | Clientes HTTP/Serverless con *graceful degradation* | ✅ Sí (Integraciones) |
| [`08-media-i18n`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/08-media-i18n.md) | 🎬 **Media, Contenido, SEO & i18n** | Paridad ES/EN, `data/apps/*.yaml`, capturas `1600×980`, SVGs inline sin glifos rotos, iconos PWA, PDFs y optimización media CWV. | Fichas, `i18n/`, imágenes, PDFs y sync Pulse | ✅ Sí (Contenido/i18n) |
| [`09-monetization`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/09-monetization.md) | 💳 **Monetización, Checkout & PLG** | Escalera Dual-Mode, `/recursos/`, Lemon Squeezy (`?embed=1`), respeto de embargos y telemetría GA4 no bloqueante (`beacon`). | `kits.yaml`, CTAs de conversión y eventos GA4 | ✅ Sí (Catálogo/PLG) |

### Célula 3: Garantía (Verificación Independiente con Derecho a Veto)
| ID | Icono y Rol | Misión Principal | Entregable Clave | ¿Derecho a Veto? |
| :--- | :--- | :--- | :--- | :-: |
| [`10-security-privacy`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/10-security-privacy.md) | 🛡️ **Seguridad, Privacidad & RLS** | Auditoría de secretos y cero credenciales demo (`INV-PULSE-10`), RLS/JWT `alg`, datasets públicos (`INV-PULSE-9`), Modern Web Security (XSS/CSP) y firewall `/static/`. | Dictamen `SECURITY_PASS` / `SECURITY_REJECT` | ✅ **SÍ (Veto)** |
| [`11-qa-verifier`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/11-qa-verifier.md) | ✅ **QA Verifier** | Gates deterministas (`pytest`, `oxlint`, `hugo`), **E2E Headless Desktop+Móvil**, `modern-web-guidance legacy-scan` y control de 2 intentos (`INV-HELIX-7`). | Veredicto `QA_PASS` / `QA_REJECT` con logs reales | ✅ **SÍ (Veto)** |

### Célula 4: Entrega (Release, Checkpoints y Memoria)
| ID | Icono y Rol | Misión Principal | Entregable Clave | ¿Escribe Código Prod? |
| :--- | :--- | :--- | :--- | :-: |
| [`12-release-devops`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/12-release-devops.md) | 🚀 **Release, Empaquetado & DevOps** | Checkpoints `sdd-checkpoint-*`, `.zip` con `SHA-256`, armonización SemVer multi-superficie (`yaml`+`spec`+`sw.js`), adaptadores, CI seguro y rollback quirúrgico. | Artefactos `.zip`, tags Git y changelog actualizado | ❌ Solo Ops/CI/Release |

---

## 3. Protocolo de Aprendizaje y Radar Tecnológico (`ADR-019` / `INV-HELIX-8`)

1. **Higiene de Contexto Anti-Bloat:** Las fichas `01` a `12` tienen un límite duro de **$\le 85$ líneas** y máximo **6 reglas en su Sección §6**.
2. **Lecciones por Fricción Real:** En §6 solo se registran correcciones explicitadas por el usuario (`[USER-FIX]`), soluciones a errores reales de entorno (`[ENV-FIX]`) o competencias adoptadas del radar (`[RADAR-SKILL]`).
3. **Memoria Templada Bajo Demanda:**
   - [`TECH_RADAR.yaml`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/TECH_RADAR.yaml): Clasificación oficial de tecnologías y prácticas en 4 anillos (`ADOPT`, `TRIAL`, `ASSESS`, `HOLD`).
   - [`OPPORTUNITY_BACKLOG.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/OPPORTUNITY_BACKLOG.md): Backlog priorizado RICE de propuestas proactivas de UX, arquitectura y monetización.
   - *Regla:* No se leen durante tareas rutinarias; solo se consultan bajo demanda expresa o en planificación `XL`.
4. **Cierre de Tarea con `DEBRIEF HELIX`:** Todo hito `M`, `L` o `XL` concluye con el informe estructurado del Orquestador (participación, aprendizajes, riesgos y propuestas de alto ROI).

---

## 4. Skills Progresivas de Workspace (`.agents/skills/` — `ADR-031`)

Para incorporar conocimiento técnico extenso y vivo (como guías oficiales de estándares web y patrones de arquitectura Datalaria) **sin inflar las fichas canónicas de $\le 85$ líneas**, Datalaria Helix adopta **Skills de Divulgación Progresiva** ubicadas en `.agents/skills/<nombre>/SKILL.md`:
- **[`modern-web-guidance`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/.agents/skills/modern-web-guidance/SKILL.md):** Integra **Google Chrome Modern Web Guidance 1.0** (`GoogleChrome/modern-web-guidance-src`, 209 guías cross-browser Chrome/Edge/Firefox/MDN + 52 reglas `legacy-scan`) con la política **Baseline** de Datalaria para `04-ux-ui`, `05-frontend`, `07-apis-integrations`, `10-security-privacy` y `11-qa-verifier`.
- **[`pwa-offline-arcade-builder`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/.agents/skills/pwa-offline-arcade-builder/SKILL.md):** Blueprint de arquitectura para PWAs monolíticas 100 % offline Zero-CDN, EdTech y simuladores Arcade (`conversor`, `maths`, `flashcards`, `snake`, `reading`, `weather`) para `04-ux-ui`, `05-frontend`, `08-media-i18n` y `11-qa-verifier`.
- **[`b2b-kit-factory`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/.agents/skills/b2b-kit-factory/SKILL.md):** Fábrica determinista de Kits B2B descargables (Excel `.xlsx` `openpyxl`, Guías Ejecutivas PDF A4 vectoriales `PyMuPDF` sin glifos `□`, previews reales `1600×980`, portadas `1200×750` Safe Zone `[145, 1055]`, ZIP numerado + `SHA-256` y embargo Lemon Squeezy) para `06-backend-data`, `08-media-i18n`, `09-monetization` y `12-release-devops`.
- **[`supabase-postgrest-rls-perf`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/.agents/skills/supabase-postgrest-rls-perf/SKILL.md):** Aislamiento multi-esquema PostgreSQL RLS en `datalaria-core`, verificación local JWKS ECC P-256 (`0.1 ms`), joins embebidos PostgREST, paginación server-side y resiliencia cliente SWR (`0 ms`) para `03-architect`, `06-backend-data`, `07-apis-integrations` y `10-security-privacy`.
- **Plugin `Chrome DevTools` (MCP en Antigravity):** Cierra el bucle *construir → verificar → diagnosticar* con skills bajo demanda: `a11y-debugging` (`04-ux-ui`/`11-qa-verifier`), `debug-optimize-lcp` + `memory-leak-debugging` + `chrome-devtools` (`05-frontend`/`11-qa-verifier`) y `cookie-debugging` (`10-security-privacy`).
