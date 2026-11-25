# 🎯 Rúbrica Determinista de Triaje Comercial y Crecimiento (`triage-mercator-rubric.md`)

> **Propietario:** [`M01-revenue-orchestrator`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-mercator/M01-revenue-orchestrator.md)  
> **Invariantes vinculadas:** `INV-HELIX-1`, `INV-HELIX-2`, `INV-OS-2`, `INV-MERCATOR-1`, `INV-MERCATOR-2`

---

## 1. Matriz de Dimensionamiento Comercial por Talla (`XS` a `XL`)

Antes de ejecutar cualquier cambio de precios, CRO, automatización Brevo o campaña externa, el **Orquestador de Revenue** clasifica la iniciativa según superficies comerciales afectadas ($S$) e impacto en embudo ($\Delta_{\text{rev}}$):

| Talla | Criterio Objetivo Determinista | Roles Convocados (Mercator + Veto Reutilizado) | Máx. Fichas | Ejemplo Real en Datalaria |
| :-: | :--- | :--- | :-: | :--- |
| **`XS`** | 1 archivo · Ajuste puntual de copy CTA, cupón o texto en un flujo existente | `M01` + 1 especialista (`M02`/`M03`/`M04`) + veto (`E07` o `11-qa`) | **3** | Ajustar el texto del cupón de cross-sell en un email post-compra. |
| **`S`** | 1 superficie comercial (`cro_pricing`, `lifecycle_brevo` o `external_dist`) sin cambio estructural | `M01` + 1 especialista + veto correspondiente (`10`/`11`/`E07`) | **3–4** | Preparar el playbook de lanzamiento en Reddit/HN para `pack-obs`. |
| **`M`** | 2 superficies combinadas o auditoría CRO de `/recursos/` + ajuste de oferta | `M01` + 2 especialistas + veto (`10-security-privacy`, `11-qa-verifier`, `E07`) | **4–5** | Optimizar `/recursos/` con FAQ `<details>` y bloque comparativo de ahorro. |
| **`L`** | Sprint comercial completo pre-lanzamiento o nueva palanca de ingresos (Licencias B2B + Brevo + Launch Pack) | `M01` + `M02` + `M03` + `M04` + vetos (`10`, `11`, `E07`) | **5–6** | Primer Sprint Comercial de Mercator para `pack-obs` (9 Dic) y `Helix` (19 Ene). |
| **`XL`** | Cambio de modelo de precios global, nuevo tier SaaS/MRR o campaña anual | Escalar a `00-chief-orchestrator` y dividir en **$N$ hitos `M`/`L`** coordinados con `01` y `E01`. | Secuencial | Lanzamiento comercial de `Datalaria Helix` + Licencias Equipo B2B. |

---

## 2. Disparadores Automáticos Innegociables (`Mandatory Triggers`)

| ID Trigger | Condición Detectada | Agente Activado Obligatoriamente | Acción Requerida |
| :--- | :--- | :--- | :--- |
| **`TRG-CRO`** | Cambios en `/recursos/`, precios, bundles, licencias B2B, Lemon Squeezy o `sync_revenue.py` | 💎 [`M02-cro-pricing-revops`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-mercator/M02-cro-pricing-revops.md) | Coherencia de escalera `€`, embargo `INV-AUTO-6` y telemetría sin PII (`INV-PULSE-13`). |
| **`TRG-LIFECYCLE`** | Flujos automáticos Brevo, secuencias de bienvenida, waitlist o emails post-compra | 🔁 [`M03-lifecycle-retention`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-mercator/M03-lifecycle-retention.md) | Secuencia evergreen coste `0 €`, anti-spam `> 80%` texto y segmentación por vertical. |
| **`TRG-EXT-DIST`** | Product Hunt, Show HN, Reddit, directorios IA, marketplaces o crecimiento LinkedIn Empresa | 🚀 [`M04-distribution-marketplaces`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-mercator/M04-distribution-marketplaces.md) | Playbook nativo EN-first sin spam, UTMs `ADR-033` y respeto a embargos. |
| **`TRG-VETO-TECH`** | Cualquier cambio de código, templates Hugo, APIs, `.gitignore` o datos privados | 🛡️ `10-security-privacy` + ✅ `11-qa-verifier` | Veredictos independientes `SECURITY_PASS` y `QA_PASS`. |
| **`TRG-VETO-COPY`** | Cualquier copy público, email Brevo o lanzamiento externo | ✅ `E07-editorial-qa` | Veredicto independiente `EDITORIAL_QA_PASS` (paridad ES/EN y anti-spam). |

---

## 3. Formato Canónico de la Tarjeta de Triaje Comercial (6 Líneas)

```text
TRIAGE MERCATOR · Campaña <ID> · Talla: <XS|S|M|L|XL>
Superficies afectadas: <cro_pricing | lifecycle_brevo | external_dist | brand_positioning | revenue_telemetry>
Roles activados (<N> de 4): <iconos y nombres de los agentes Mercator convocados> + Veto: <10/11/E07>
Roles en banquillo: <agentes Mercator no requeridos>
Verification Gate: <comandos exactos con código de salida 0>
Presupuesto y Gobernanza: Máx. 2 intentos por gate · Checkpoint <tag Git> · Aprobación humana previa: <SÍ|NO>
```
