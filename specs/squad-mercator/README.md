# 💰 Datalaria Mercator — Escuadrón de Revenue, Marca & Distribución (`specs/squad-mercator/`)

> **Fuente Única de Verdad (`ADR-034` / `INV-OS-2`):** Este directorio contiene las definiciones canónicas (`AGENT_SPEC`) de los **4 roles núcleo (Estadio 1)** de **Datalaria Mercator**. Sus adaptadores (`.agents/squad-mercator/`, `.claude/agents/M0*.md`, `.cursor/rules/mercator-squad.mdc`) se compilan automáticamente con `python -m ops.helix.build_adapters`.

---

## 1. Principio Rector: Ingresos Pasivos, Cero Bloat y Veto Reutilizado
1. **Misión:** Convertir la excelencia técnica de **Helix** y la autoridad editorial de **Scriba** en **marca reconocible, audiencia fidelizada e ingresos pasivos recurrentes** bajo coste fijo `0 €/mes` (`specs/STRATEGY.md`).
2. **Carga Bajo Demanda (`INV-HELIX-2` / `INV-MERCATOR-2`):** `M01-revenue-orchestrator` aplica [`triage-mercator-rubric.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-mercator/triage-mercator-rubric.md), emite la tarjeta `TRIAGE MERCATOR` de 6 líneas y convoca solo a los especialistas necesarios.
3. **Separación Construcción vs. Verificación sin Duplicar QA (`INV-HELIX-1` / `INV-OS-2`):** Ningún agente de Mercator tiene poder de veto ni aprueba su propio trabajo. Toda entrega pasa por los vetos ya consolidados:
   - Cambios web, checkout, telemetría o datos privados → **`10-security-privacy`** (`SECURITY_PASS`) + **`11-qa-verifier`** (`QA_PASS`).
   - Copys comerciales, emails Brevo o textos externos → **`E07-editorial-qa`** (`EDITORIAL_QA_PASS`).

---

## 2. Catálogo de los 4 Agentes Núcleo (Estadio 1: `0 → 500 €/mes`)

| ID | Icono y Rol | Célula | Misión Principal | ¿Código Prod? | ¿Veto? |
| :--- | :--- | :---: | :--- | :-: | :-: |
| [`M01-revenue-orchestrator`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-mercator/M01-revenue-orchestrator.md) | 💰 **Orquestador de Revenue & Marca** | `direction` | Triaje `TRIAGE MERCATOR`, coordinación con `00`/`01`/`E01`, custodia temporal de `specs/_brand.md` y priorización comercial. | ❌ No | ❌ No |
| [`M02-cro-pricing-revops`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-mercator/M02-cro-pricing-revops.md) | 💎 **Arquitecto CRO, Pricing & RevOps** | `construction` | Líder del Guild de Monetización: Lemon Squeezy API, CRO de `/recursos/` y landings, bundles, licencias B2B (`99–249 €`) y afiliados. | ✅ Sí | ❌ No |
| [`M03-lifecycle-retention`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-mercator/M03-lifecycle-retention.md) | 🔁 **Arquitecto de Lifecycle & Brevo Evergreen** | `construction` | Secuencias automatizadas Brevo 24/7 (Bienvenida segmentada, Waitlist Helix, Post-compra + Testimonio D+7 + Cross-sell D+14). | ✅ Sí | ❌ No |
| [`M04-distribution-marketplaces`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-mercator/M04-distribution-marketplaces.md) | 🚀 **Especialista en Distribución Externa & Marketplaces** | `construction` | Captación fuera del blog: Product Hunt, Show HN, Reddit nicho, directorios IA, marketplaces complementarios y crecimiento LinkedIn Empresa. | ✅ Sí | ❌ No |

> **Escalado Programado (Estadio 2 — al cruzar `500 €/mes` sostenidos):** Se desbloquearán `M05-brand-positioning` (asumiendo la custodia de `_brand.md`) y `M06-customer-success` (soporte automatizado y bucle VoC hacia `02-product-analyst`).
