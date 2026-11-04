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
| [`01-orchestrator`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/01-orchestrator.md) | 🎯 **Orquestador / Delivery Lead** | Único interlocutor humano, triaje `XS–XL`, asignación de roles y custodia de `ROADMAP.md`. | Tarjeta de Triaje (6 líneas) + Puntero `ROADMAP.md` | ❌ No |
| [`02-product-analyst`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/02-product-analyst.md) | 🧭 **Product Analyst / PO** | Entrevista de negocio, definición de problema, usuario, *non-goals*, precios y embudo. | Sección 1 y criterios de negocio en `spec.md` | ❌ No |
| [`03-architect`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/03-architect.md) | 🏛️ **Arquitecto / Tech Lead** | Diseño de arquitectura mínima viable, contratos de datos, invariantes `INV-*` y ADRs. | `spec.md` (§2–§4), `DECISIONS.md` (`ADR-*`) | ❌ No |

### Célula 2: Diseño y Construcción (Ejecución Especializada)
| ID | Icono y Rol | Misión Principal | Entregable Clave | ¿Escribe Código Prod? |
| :--- | :--- | :--- | :--- | :-: |
| [`04-ux-ui`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md) | 🎨 **Diseñador UX/UI** | Dirección estética por preset, Design Tokens, flujos, estados de UI, *Wow Moment* y accesibilidad WCAG 2.2 AA. | `design.md` + Auditoría visual pre-QA | ⚠️ Solo CSS/Tokens/Assets |
| [`05-frontend`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/05-frontend.md) | ⚡ **Ingeniero Frontend** | Implementación de componentes React/TS/HTML/Hugo fieles a `design.md` y estado en cliente. | Código UI + `oxlint` y `vite build` en `0` | ✅ Sí (UI/Frontend) |
| [`06-backend-data`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/06-backend-data.md) | 🗄️ **Backend, Datos & Motor Cuantitativo** | Músculo matemático determinista (Python/Pydantic/Pandas/Excel), APIs FastAPI y esquemas SQL. | Motores `.py`, migraciones `.sql` y tests unitarios | ✅ Sí (Backend/Data) |
| [`07-apis-integrations`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/07-apis-integrations.md) | 🔌 **APIs, Integraciones & MCP** | Conectores externos (Brevo, GA4, GSC, Lemon Squeezy, Supabase, Power Query, MCP) con privilegio mínimo. | Clientes HTTP/ Serverless con *graceful degradation* | ✅ Sí (Integraciones) |
| [`08-media-i18n`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/08-media-i18n.md) | 🎬 **Media, Contenido, SEO & i18n** | Diccionarios bilingües ES/EN, artículos técnicos, portadas, capturas compuestas `1600×980`, guías PDF y SEO. | Posts ES/EN, `i18n/`, imágenes y manuales PDF | ✅ Sí (Contenido/i18n) |
| [`09-monetization`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/09-monetization.md) | 💳 **Monetización, Checkout & PLG** | Escalera Dual-Mode (Sandbox → Kit → Pro), tarjetas en `/recursos/`, Lemon Squeezy y telemetría GA4 de conversión. | `kits.yaml`, CTAs de conversión y eventos GA4 | ✅ Sí (Catálogo/PLG) |

### Célula 3: Garantía (Verificación Independiente con Derecho a Veto)
| ID | Icono y Rol | Misión Principal | Entregable Clave | ¿Derecho a Veto? |
| :--- | :--- | :--- | :--- | :-: |
| [`10-security-privacy`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/10-security-privacy.md) | 🛡️ **Seguridad, Privacidad & RLS** | Auditoría de secretos, políticas RLS por `user_id`, lista blanca de endpoints, RGPD y firewall de `/static/`. | Dictamen `SECURITY_PASS` / `SECURITY_REJECT` | ✅ **SÍ (Veto)** |
| [`11-qa-verifier`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/11-qa-verifier.md) | ✅ **QA Verifier** | Ejecución determinista de `pytest`, `oxlint`, `hugo --gc --minify` y comprobación punto por punto contra `spec.md`. | Veredicto `QA_PASS` / `QA_REJECT` con logs reales | ✅ **SÍ (Veto)** |

### Célula 4: Entrega (Release, Checkpoints y Memoria)
| ID | Icono y Rol | Misión Principal | Entregable Clave | ¿Escribe Código Prod? |
| :--- | :--- | :--- | :--- | :-: |
| [`12-release-devops`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/12-release-devops.md) | 🚀 **Release, Empaquetado & DevOps** | Tags `sdd-checkpoint-*`, empaquetado de `.zip` comerciales, versionado SemVer (`data/apps/*.yaml`), CI/CD y rollback. | Artefactos `.zip`, tags Git y changelog actualizado | ❌ Solo Ops/CI/Release |
