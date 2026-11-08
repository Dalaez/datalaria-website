# 🎯 Rúbrica Determinista de Triaje Editorial y Enrutado (`triage-editorial-rubric.md`)

> **Propietario:** [`E01-editorial-orchestrator`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-editorial/E01-editorial-orchestrator.md)  
> **Invariantes vinculadas:** `INV-HELIX-1`, `INV-HELIX-2`, `INV-SCRIBA-1`, `INV-SCRIBA-2`

---

## 1. Matriz de Dimensionamiento Editorial por Talla (`XS` a `XL`)

Antes de modificar cualquier artículo, plantilla social o programar campañas, el **Coordinador Editorial** clasifica la tarea en una de las 5 tallas según el alcance ($P$ posts afectados, $C$ canales de distribución y $\Delta_{\text{content}}$ impacto estratégico):

| Talla | Criterio Objetivo Determinista | Roles Convocados (Alineación) | Máx. Fichas en Contexto | Ejemplo Real en Datalaria |
| :-: | :--- | :--- | :-: | :--- |
| **`XS`** | $P = 1$ archivo post · Corrección tipográfica, ajuste de enlace o actualización menor de metadata | `E01-editorial-orchestrator` + `E04-bilingual-seo-editor` + `E07-editorial-qa` | **3** | Corregir una errata en un post o actualizar un enlace roto. |
| **`S`** | $P = 1$ post existente · Preparación de `social_pack.yaml` o campaña de Newsletter Brevo 2.0 | `E01` + `E05-content-monetizer` o `E06-social-syndicator` + `E07` + `E08-autopilot-dispatcher` | **4** | Generar el hilo de X, post de LinkedIn y campaña Brevo para un post ya redactado. |
| **`M`** | $P = 2$ archivos (`ES ⇔ EN`) · Redacción completa de 1 nuevo artículo bilingüe con portada y syndication pack | `E01` + `E03-technical-writer` + `E04` + `E05` + `E06` + `E07` + `E08` | **5–7** | Redactar un post técnico bilingüe con diagrama Mermaid, CTAs y paquete social completo. |
| **`L`** | Auditoría integral post-actualización GA4+GSC con `impact_analyzer.py`, optimización de 3+ posts o serie vinculada a App | `E01` + `E02-seo-impact-strategist` + `E04` + `E05` + `E07` + `E08` | **5–6** | Reporte mensual de impacto SEO/GA4 y reescritura de 3 títulos para ganar CTR orgánico. |
| **`XL`** | Serie editorial pilar completa (5 posts bilingües = 10 entregas) conectada a producto Helix/Pulse | Dividir en **$N$ tareas de talla `M` o `L`** coordinando con `01-orchestrator` (Helix). | Secuencial hito a hito | Lanzamiento editorial de una Suite o serie de 5 capítulos (ej. serie Helix o serie Pulse). |

---

## 2. Disparadores Automáticos Innegociables (`Mandatory Triggers`)

La presencia de cualquiera de estas condiciones activa obligatoriamente al especialista correspondiente:

| ID Trigger | Condición Detectada | Agente Activado Obligatoriamente | Acción Requerida |
| :--- | :--- | :--- | :--- |
| **`TRG-SEO`** | Análisis de métricas GA4/GSC, ajuste de títulos, meta-descriptions, categorías o auditoría de impacto | 📈 [`E02-seo-impact-strategist`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-editorial/E02-seo-impact-strategist.md) | Dictamen analítico, cálculo de ROI y propuestas de optimización de CTR. |
| **`TRG-I18N-POST`** | Creación o edición de artículos en `content/{es,en}/posts/` o diccionarios i18n | 🌐 [`E04-bilingual-seo-editor`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-editorial/E04-bilingual-seo-editor.md) | Verificación de paridad estricta `ES ⇔ EN` y checklist SEO On-Page (100/100). |
| **`TRG-BREVO`** | Creación o modificación de campañas de email o plantillas HTML de Newsletter | 💰 [`E05-content-monetizer`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-editorial/E05-content-monetizer.md) | Validación de ratio texto/imagen > 80%, caja de valor 60s y asunto sin prefijo robótico. |
| **`TRG-SOCIAL`** | Preparación o edición de copys para X/Twitter, LinkedIn, Dev.to o CoderLegion | 📣 [`E06-social-syndicator`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-editorial/E06-social-syndicator.md) | Generación de `social_pack.yaml`, hilos de X coste 0€ y artículos con `canonical_url`. |
| **`TRG-EDIT-QA`** | **Toda tarea** editorial o de sindicación social (`XS` a `XL`) | ✅ [`E07-editorial-qa`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-editorial/E07-editorial-qa.md) | Auditoría punto por punto determinista con derecho a veto (`EDITORIAL_QA_PASS`). |

---

## 3. Formato Canónico de la Tarjeta de Triaje Editorial (6 Líneas)

Todo turno editorial comienza publicando este bloque compacto:

```text
TRIAGE SCRIBA · Tarea <ID> · Talla: <XS|S|M|L|XL>
Superficies afectadas: <content_es | content_en | seo_metadata | newsletter_brevo | social_syndication | pulse_index>
Roles activados (<N> de 8): <iconos y nombres de los agentes convocados>
Roles en banquillo: <agentes no requeridos en esta tarea>
Verification Gate: <comandos exactos con código de salida 0>
Presupuesto y Gobernanza: Máx. 2 intentos por gate · Checkpoint <tag Git> · Aprobación humana previa: <SÍ|NO>
```
