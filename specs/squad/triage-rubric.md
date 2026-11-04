# 🎯 Rúbrica Determinista de Triaje y Enrutado (`triage-rubric.md`)

> **Propietario:** [`01-orchestrator`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/01-orchestrator.md)  
> **Invariantes vinculadas:** `INV-HELIX-1`, `INV-HELIX-2`, `INV-HELIX-3`, `INV-HELIX-7`

---

## 1. Matriz de Dimensionamiento por Talla (`XS` a `XL`)

Antes de modificar cualquier archivo del repositorio, el **Orquestador** clasifica la tarea en una de las 5 tallas deterministas según el número de archivos afectados ($F$), las superficies técnicas tocadas ($S$) y el impacto en contratos ($\Delta_{\text{spec}}$):

| Talla | Criterio Objetivo Determinista | Roles Convocados (Alineación) | Máx. Fichas `AGENT_SPEC` en Contexto | Ejemplo Real en Datalaria |
| :-: | :--- | :--- | :-: | :--- |
| **`XS`** | $F = 1$ archivo · $1$ sola superficie no sensible · Sin cambio en `spec.md` ni esquemas de datos | `01-orchestrator` + `1 Constructor` (`05`, `06` u `08`) + `11-qa-verifier` | **2–3** | Corregir una errata tipográfica o ajustar un color dentro de un token existente. |
| **`S`** | $1 \le F \le 3$ archivos · $1$ superficie · Sin cambio de arquitectura ni nuevas tablas/endpoints | `01-orchestrator` + `1–2 Constructores` (+ disparadores si aplican) + `11-qa-verifier` | **3–4** | Añadir un filtro rápido por fecha en una tabla React o un nuevo test en `pytest`. |
| **`M`** | $F > 3$ archivos **o** $2$ superficies combinadas **o** ajuste menor de contrato existente | `01-orchestrator` + `03-architect` + `2–3 Constructores` + `10-security-privacy` (si aplica) + `11-qa-verifier` + `12-release-devops` | **4–6** | Integrar el formulario de Waitlist con Brevo en posts y catálogo (Hito 6.0). |
| **`L`** | Nueva funcionalidad completa que crea o modifica sustancialmente una `spec.md` o el modelo de negocio | `01-orchestrator` + `02-product-analyst` + `03-architect` + `04-ux-ui` + `Constructores` + `10-security-privacy` + `11-qa-verifier` + `12-release-devops` | **6–9** *(secuenciados por fase)* | Auditoría y robustecimiento integral de Datalaria Pulse y su Kit ZIP (Hito 6.3). |
| **`XL`** | Aplicación nueva desde cero o épica multi-módulo | **Prohibido ejecutar de golpe.** `01-orchestrator` + `02-product-analyst` + `03-architect` dividen la épica en **$N$ hitos atómicos de talla `M` o `L`** en `ROADMAP.md`. | Secuencial hito a hito | Lanzamiento completo del producto Datalaria Helix (Hitos 6.0 a 6.9). |

---

## 2. Disparadores Automáticos Innegociables (`Mandatory Triggers` — `INV-HELIX-3`)

Independientemente de que una tarea sea de talla `XS` o `S`, la presencia de cualquiera de las siguientes condiciones **fuerza automáticamente** la activación del especialista correspondiente:

| ID Trigger | Condición Detectada en los Archivos Afectados | Agente Activado Obligatoriamente | Acción Requerida antes del Cierre |
| :--- | :--- | :--- | :--- |
| **`TRG-SEC`** | Se toca autenticación, Supabase RLS, `.env`, variables de entorno, funciones serverless (`netlify/functions/`), pagos o cualquier archivo bajo `/static/` | 🛡️ [`10-security-privacy`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/10-security-privacy.md) | Auditoría de secretos, listas blancas, aislamiento RLS y firewall de `/static/` (`SECURITY_PASS`). |
| **`TRG-UX`** | Se crea o modifica interfaz visual visible por el usuario (`.tsx`, `.html`, `.css`, modales, tarjetas o layouts) | 🎨 [`04-ux-ui`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md) | Validación contra `design.md`, jerarquía visual, modo oscuro, estados vacíos/error y contraste WCAG 2.2 AA. |
| **`TRG-I18N`** | Se crean o editan artículos (`content/{es,en}/`), diccionarios de traducción (`i18n`), metadatos (`data/apps/*.yaml`) o kits (`data/pulse/kits.yaml`) | 🎬 [`08-media-i18n`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/08-media-i18n.md) | Verificación de paridad estricta `ES ⇔ EN` y ejecución de `build_index` + `publish_public` de Datalaria Pulse. |
| **`TRG-MON`** | Se modifican precios, enlaces de Lemon Squeezy, CTAs de compra/waitlist, `/recursos/` o eventos `gtag` / `dataLayer` | 💳 [`09-monetization`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/09-monetization.md) | Comprobación de coherencia de precios, ausencia de enlaces muertos/`mailto:` y emisión de telemetría GA4. |
| **`TRG-QA`** | **Cualquier tarea** que modifique el repositorio (`XS`, `S`, `M`, `L`) | ✅ [`11-qa-verifier`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/11-qa-verifier.md) | Ejecución de los comandos deterministas del Gate con código de salida `0` (`QA_PASS`). |

---

## 3. Formato Canónico de la Tarjeta de Triaje (6 Líneas)

Todo hito o intervención comienza mostrando este bloque compacto:

```text
TRIAGE HELIX · Hito <ID> · Talla: <XS|S|M|L|XL>
Superficies afectadas: <lista separada por comas>
Roles activados (<N> de 12): <iconos y nombres de los agentes convocados>
Roles en banquillo: <agentes no requeridos en esta tarea>
Verification Gate: <comandos exactos con código de salida 0>
Presupuesto y Gobernanza: Máx. 2 intentos por gate · Checkpoint <tag Git> · Aprobación humana previa: <SÍ|NO>
```

---

## 4. Protocolo de Traspaso (*Handoff*) y Escalado

1. **Contrato de Handoff entre Constructores y Garantía:**
   Cuando los agentes constructores terminan su implementación, entregan a `10-security-privacy` y `11-qa-verifier` una lista explícita de:
   - Archivos creados o modificados.
   - Invariantes `INV-*` afectadas.
   - Comandos ejecutados preliminarmente.
2. **Protocolo de Veto y Reintento (Máximo 2 Intentos):**
   - Si `10-security-privacy` o `11-qa-verifier` emiten `REJECT`, devuelven el control al constructor específico indicando la línea y el test fallido.
   - Si tras el **2.º intento** el Verification Gate sigue fallando, se activa inmediatamente `12-release-devops` para ejecutar **Rollback al Checkpoint (`INV-HELIX-7`)** y el Orquestador informa al usuario humano sin improvisar parches a ciegas.
3. **Escalado de Talla en Caliente (*Scope Creep Guard*):**
   - Si durante una tarea `S` el constructor descubre que necesita tocar más de 3 archivos o modificar un contrato de datos, **debe detenerse y devolver el control a `01-orchestrator`** para re-emitir la Tarjeta de Triaje como `M` o `L` (solicitando aprobación humana si cambia el alcance funcional).
