# OPPORTUNITY_BACKLOG.md — Repositorio de Oportunidades y Mejoras Proactivas Helix

> **Gobernanza:** `ADR-019`, `ADR-031` e Invariante `INV-HELIX-8`.  
> **Propósito:** Canalizar las propuestas de mejora, nuevas tendencias y optimizaciones identificadas por los agentes de Helix durante las auditorías e hitos mayores.  
> **Aislamiento de Contexto:** Este documento **NUNCA** se inyecta en el prompt de tareas rutinarias para proteger el presupuesto de tokens y la atención del modelo. Se revisa exclusivamente a petición explícita del usuario o en hitos de planificación estratégica.

---

## 1. Criterio de Priorización RICE

Cada iniciativa se evalúa con la fórmula estándar RICE:
$$\text{Score RICE} = \frac{\text{Reach (Alcance: 1-10)} \times \text{Impact (Impacto: 0.5-3)} \times \text{Confidence (Confianza: 50\%-100\%)}}{\text{Effort (Esfuerzo: personas/días o turnos: 1-5)}}$$

---

## 2. Oportunidades por Dominio y Agente Proponente

### 2.1 Célula de Construcción: UX/UI (`04-ux-ui`)
- **OPP-UX-01: Micro-interacciones Nativas CSS (`@starting-style` / View Transitions) en Componentes de Entrada**
  - **Proponente:** `04-ux-ui`
  - **Descripción:** Sustituir animaciones pesadas de librerías JS por transiciones nativas CSS (`@starting-style`, `interpolate-size`, `prefers-reduced-motion`) en modales, sliders y tarjetas KPI para elevar la percepción ejecutiva sin peso extra.
  - **RICE:** Reach: 8 | Impact: 1.5 | Confidence: 90% | Effort: 1.5 $\rightarrow$ **Score: 7.2**
  - **Estado:** `TRIAL` (alineado con `ADR-031` Modern Web Guidance).

- **OPP-UX-02: Migración a Primitivas Nativas `<dialog>`, Popover y `@container` tras `legacy-scan`**
  - **Proponente:** `04-ux-ui` + `05-frontend` + `11-qa-verifier`
  - **Descripción:** Ejecutar `npx.cmd -y modern-web-guidance@latest legacy-scan` sobre `apps/lifeops/web`, `apps/pulse/web`, `apps/weather` y `layouts/partials/recursos_catalog.html` para modernizar formularios (`autocomplete`), scrollbars estándar CSS (`scrollbar-color`/`scrollbar-width`), métodos inmutables ES2023 (`.toSorted()`) y primitivas nativas.
  - **RICE:** Reach: 9 | Impact: 2.0 | Confidence: 90% | Effort: 2 $\rightarrow$ **Score: 8.1**
  - **Estado:** `ADOPTED` (`0` hallazgos `legacy-scan` verificados en `apps/lifeops/web`, `apps/pulse/web` y `layouts/partials/recursos_catalog.html`).

### 2.2 Célula de Construcción: Frontend, APIs y Arquitectura (`03-architect` + `05-frontend` + `07-apis-integrations`)
- **OPP-FE-01: Migración a Componentes de Tabla Virtualizados + `content-visibility: auto`**
  - **Proponente:** `05-frontend`
  - **Descripción:** Aplicar `content-visibility: auto` y `scheduler.yield()` (y virtualización si supera 1.000 filas) en inspectores analíticos para garantizar `INP < 200 ms` y 60 FPS constantes en móvil.
  - **RICE:** Reach: 6 | Impact: 2.0 | Confidence: 85% | Effort: 1.5 $\rightarrow$ **Score: 6.8**
  - **Estado:** `BACKLOG` (priorizar al escalar vistas de tabla densas).

- **OPP-FE-02: Motor Financiero/Climático Cliente en Parquet + DuckDB-Wasm**
  - **Proponente:** `03-architect`
  - **Descripción:** Consolidar la Etapa 2 de `ADR-021` (compactación Parquet + consultas analíticas locales en navegador vía DuckDB-Wasm) cuando el histórico supere ~550k registros, manteniendo coste fijo `0 €`.
  - **RICE:** Reach: 5 | Impact: 3.0 | Confidence: 75% | Effort: 4 $\rightarrow$ **Score: 2.81**
  - **Estado:** `ASSESS` (en radar tecnológico v2.0).

- **OPP-API-01: Exposición WebMCP en Sandboxes Datalaria (Helix, Pulse, Conversor)**
  - **Proponente:** `07-apis-integrations` + `05-frontend`
  - **Descripción:** Evaluar las guías `webmcp`, `agentic-forms` y `agentic-javascript-tools` de Modern Web Guidance para hacer que los sandboxes gratuitos de Datalaria sean invocables de forma declarativa por navegadores agénticos.
  - **RICE:** Reach: 7 | Impact: 2.0 | Confidence: 70% | Effort: 2 $\rightarrow$ **Score: 4.9**
  - **Estado:** `ASSESS (Origin Trial Gate #5117755740913664)` — `declarative-webmcp` y `document-modelcontext` evaluados como Chrome Origin Trial experimental; arquitectura en 2 capas diseñada para `/apps/helix/` (Capa 1 estándar hoy + Capa 2 Origin Trial tras opt-in explícito).

### 2.3 Célula de Construcción: Backend y Datos (`06-backend-data`)
- **OPP-BE-01: Plantillas Excel Blindadas con Protección de Fórmulas y Formatos Condicionales**
  - **Proponente:** `06-backend-data`
  - **Descripción:** Estandarizar en todos los generadores `openpyxl` de `ops/` protección de celdas de fórmulas, validaciones desplegables y formatos condicionales nativos sin macros bloqueadas.
  - **RICE:** Reach: 9 | Impact: 2.5 | Confidence: 95% | Effort: 2 $\rightarrow$ **Score: 10.68**
  - **Estado:** `ADOPTED` parcialmente (aplicado en Pulse y Lector Arcade R.11; extender a próximos Kits).

### 2.4 Célula de Monetización y Crecimiento (`09-monetization`)
- **OPP-MON-01: Bundle Dinámico con Descuento Progresivo en Lemon Squeezy**
  - **Proponente:** `09-monetization`
  - **Descripción:** Configurar en Lemon Squeezy un cupón cruzado para compradores del *Kit Datalaria Pulse* o *Kit Helix* que adquieran posteriormente otros Packs/Suites del catálogo.
  - **RICE:** Reach: 8 | Impact: 2.0 | Confidence: 80% | Effort: 1 $\rightarrow$ **Score: 12.8**
  - **Estado:** `READY` para activar tras consolidar lanzamientos de Pulse y Helix.

- **OPP-MON-02: Lead Magnet de Auditoría Rápida de Agentes (`verify_agent_constitution.py`)**
  - **Proponente:** `09-monetization`
  - **Descripción:** Publicar un script descargable gratuito de 1 archivo que audita repositorios externos contra `INV-HELIX-1..8` y `SpecQualityScore`, captando leads B2B para Helix Pro.
  - **RICE:** Reach: 9 | Impact: 2.5 | Confidence: 85% | Effort: 1.5 $\rightarrow$ **Score: 12.75**
  - **Estado:** `READY` para campaña de lanzamiento de Datalaria Helix (Enero 2027).

---

## 3. Protocolo de Transición hacia el ROADMAP

Cualquier oportunidad en estado `READY` o `APPROVED` solo se transfiere a [`specs/ROADMAP.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/ROADMAP.md) cuando el usuario da su aprobación explícita o cuando se planifica formalmente un nuevo Hito.
