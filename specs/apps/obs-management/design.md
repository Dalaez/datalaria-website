# Especificación de Diseño UX/UI: Agentic Radar (`obs-management`)

> **ID de Diseño:** `DESIGN-APP-OBS-MANAGEMENT`  
> **Spec Técnica Vinculada:** [`specs/apps/obs-management/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/obs-management/spec.md) (`v2.0.0`)  
> **Agente Propietario:** 🎨 [`04-ux-ui` (Diseñador UX/UI)](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md)  
> **Skill Web de Referencia:** [`.agents/skills/modern-web-guidance/SKILL.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/.agents/skills/modern-web-guidance/SKILL.md) (`ADR-031`, política *Baseline Widely Available* + fallback ligero `<= 20` líneas para *Newly Available*)  
> **Preset Estético Seleccionado:** `Executive Data-Dense` (Centro de Mando de Riesgo de Cadena de Suministro IEC 62402)

---

## 1. Dirección Estética y Psicología de Usuario

### 1.1 Perfil Visual del Usuario y Contexto de Uso
- **Quién lo usa y dónde:**
  1. **Directores de Operaciones (COO / VP Supply Chain) y Directores Financieros (CFO)** en portátil (`1366×768` a `1920×1080`) durante comités de riesgo industrial, o en revisión ejecutiva rápida desde móvil (`390×844`).
  2. **Ingenieros de Componentes y Compras Técnicas** que evalúan avisos PDN/EOL, validan rutas críticas del grafo BOM y comparan financieramente *Last Time Buy (LTB)* frente a rediseño *Form-Fit-Function (FFF)*.
- **Sensación que debe transmitir en los primeros 3 segundos:** **Control ejecutivo inmediato, rigor industrial y precisión financiera C-Level** (estética de terminal analítica moderna estilo *Linear* / *Bloomberg Supply Chain*), donde el riesgo en euros, las alertas críticas y la ruta afectada se leen de un vistazo sin ruido visual ni sensación de prototipo estático (*Content-First*).
- **Preset de Dirección Activo:**
  - [x] **`Executive Data-Dense` (Estándar B2B Datalaria — LifeOps / Pulse / Weather):** Modo oscuro profundo por defecto (`#0b0f17` / `#111827`), bordes sutiles iluminados, cifras financieras alineadas con `tabular-nums` y soporte completo para alternar a Modo Claro de alto contraste (`color-scheme: dark light`).

### 1.2 El «Momento Firma» (*Signature Wow Moment*)
> Una única micro-interacción de alto valor funcional que convierte la demo en un simulador ejecutivo memorable en `< 3 s`.
- **Descripción del Momento Firma:** **Simulador Interactivo de Choque PDN/EOL + Grafo BOM Vivo en SVG (`< 16 ms`):**
  - El usuario puede elegir en **1 clic** entre 3 escenarios reales (*Crisis Capacitor `DRONE-X1`*, *Obsolescencia MCU `STM32` Multi-SKU*, *Parada Total de Línea `3 SKUs`*) o disparar una alerta EOL simulada sobre cualquier componente del catálogo.
  - Al instante (`< 16 ms`, sin recargar ni esperar servidores), los 4 KPIs recalculan el P&L y el capital LTB, la tabla ordenable destaca las filas afectadas y el **Visor SVG del Grafo BOM** ilumina en rojo/ámbar la cadena exacta de propagación `MPN → AML → Subensamblaje → SKU Final`, mientras la consola táctica reproduce las trazas de auditoría.

---

## 2. Sistema de Design Tokens y Primitivas Modern Web Guidance

> **Regla `INV-UX-1`:** Queda prohibido usar colores hexadecimales arbitrarios fuera de los tokens declarados en esta tabla.  
> **Regla `INV-UX-2` (Platform-First / `ADR-031`):** Cero librerías JS/CSS de terceros desde CDN (`INV-OBS-1`). Todos los overlays, tablas, scrollbars y formularios emplean primitivas nativas **Baseline** verificadas con `modern-web-guidance`.

### 2.1 Paleta Semántica de Color (`color-scheme: dark light`)
| Token CSS | Valor (Dark Mode / Default) | Valor (Light Mode / Opcional) | Uso Semántico Exclusivo |
| :--- | :--- | :--- | :--- |
| `--bg-canvas` | `#0b0f17` | `#f8fafc` | Fondo principal de la aplicación |
| `--bg-surface` | `#111827` | `#ffffff` | Tarjetas KPI, tabla de ensamblajes, visor BOM y calculadora LTB |
| `--bg-elevated` | `#1e293b` | `#f1f5f9` | Modales `<dialog>`, popovers, barra de pestañas y controles activos |
| `--bg-terminal` | `#060a12` | `#0f172a` | Fondo de la consola táctica de telemetría CrewAI (contraste `>= 9:1`) |
| `--text-primary` | `#f8fafc` | `#0f172a` | Títulos, cifras KPI principales y encabezados (Contraste `>= 7:1`) |
| `--text-secondary` | `#94a3b8` | `#475569` | Etiquetas, subtítulos, metadatos de tabla (Contraste `>= 4.5:1`) |
| `--accent-primary` | `#0ea5e9` | `#0284c7` | Pestaña activa, foco, nodos seleccionados y acción primaria |
| `--accent-secondary` | `#8b5cf6` | `#7c3aed` | Destacados Agente IA / CrewAI y puente a Suites Ejecutivas B2B |
| `--status-success` | `#10b981` | `#059669` | Estado Sandbox/Live nominal, componente `Active`, ahorro confirmado |
| `--status-warning` | `#f59e0b` | `#d97706` | `EVALUATING INVENTORY`, estado `NRND`, estrategia híbrida |
| `--status-danger` | `#ef4444` | `#dc2626` | `CRITICAL LTB REQUIRED`, `EOL`/`Obsolete`, margen P&L en riesgo |
| `--border-subtle` | `rgba(148, 163, 184, 0.16)` | `rgba(15, 23, 42, 0.12)` | Divisores de tarjetas, filas de tabla y bordes de inputs |

### 2.2 Escala Tipográfica, Layout y Espaciado
- **Fuente de Títulos y KPIs (`--font-display`):** `'Outfit', system-ui, -apple-system, 'Segoe UI', sans-serif` (Pesos `600`, `700`; `text-wrap: balance` en `h1`–`h3`; sin bloqueo CDN: pila de sistema limpia o `@font-face` local si se incluye, garantizando `FOIT = 0`).
- **Fuente de Interfaz (`--font-sans`):** `'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif` (Pesos `400`, `500`, `600`; tamaños estrictamente en `rem` para respetar la escala de texto del SO).
- **Fuente Monoespaciada / Cifras (`--font-mono`):** `'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` con **`font-variant-numeric: tabular-nums`** obligatorio en KPIs, importes en €, códigos MPN/SKU, puntuaciones IEC 62402 y tabla.
- **Layout Responsivo y Radios:** `@container` en tarjetas KPI y `.table-wrapper`, `scrollbar-gutter: stable`, `--radius-sm: 6px`, `--radius-md: 10px`, `--radius-lg: 14px`.

### 2.3 Primitivas Nativas Seleccionadas y Fallbacks (`Modern Web Guidance`)
| Patrón UI | Primitiva Nativa Elegida | Soporte Baseline & Fallback (`<= 20` líneas si *Newly Available*) | Guía `modern-web-guidance` Consultada |
| :--- | :--- | :--- | :--- |
| **Modal Importar CSV / Exportar PNG** | `<dialog>` + `showModal()` + `<form method="dialog">` + `dialog:modal { overscroll-behavior: contain; }` + `dialog::backdrop { overflow: hidden; overscroll-behavior: contain; }` (sin `role="dialog"` ni `aria-modal` manual; reset `dialog.returnValue = ''` en `close`). | Widely Available. Para `closedby="any"` (Limited en Safari), fallback de `<= 12` líneas con `pointerdown`/`pointerup` sobre `getBoundingClientRect()` si `!('closedBy' in HTMLDialogElement.prototype)`. | `dialog` |
| **Tooltips de Fórmulas IEC 62402 / Menú Opciones** | `popover="auto"` + `popovertarget` (en elemento semántico, no `<dialog>`), estilizado con `:is(:popover-open, .\:popover-open)`. | Newly Available (Baseline Ene 2025). Degradación progresiva con toggle de atributo `hidden` (`<= 12` líneas) si `!Object.hasOwn(HTMLElement.prototype, 'popover')`. | `dialog` (Rule 3) |
| **Tabla de Ensamblajes Impactados** | `<div class="table-wrapper" tabindex="0" role="region" aria-labelledby="...">` con `container-type: inline-size`, `position: sticky` en `thead`/`tbody th`, y transformación apilada en `@container (width < 600px)` con `::before` y `var(--label-n)`. | Widely Available (`@container` + `position: sticky`). | `responsive-table` |
| **Ordenación de Columnas en Tabla** | `<button type="button">` dentro de `<th scope="col" data-type="number|text">`, `aria-sort="ascending|descending"` exclusivo en la columna activa, `Intl.Collator` + `data-value` numérico crudo, reordenación de `<tr>` existentes sin re-renderizar `<tbody>` ni usar `innerHTML`, anuncio en un único `<div role="status">` oculto visualmente (`clip-path: inset(50%)`). | Click listener estándar en botones de cabecera (equivale funcionalmente a Invoker Commands sin polyfill externo); `appendChild` en orden como fallback de `moveBefore()` (Limited en Safari). | `sortable-table` |
| **Scrollbars de Consola CrewAI y Tabla** | `scrollbar-width: thin` + `scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)` (contraste thumb `>= 3:1`). | Bloque `@supports not (scrollbar-color: auto)` con reset `scrollbar-width: auto` y fallback `::-webkit-scrollbar` (10 líneas), evitando el fallo de `legacy-scan`. | `customize-scrollbar-color-and-thickness` |
| **Validación Formularios (Simulador LTB / PDN)** | `:user-invalid` + `aria-invalid` sincronizado + `aria-describedby` hacia mensaje de error accesible. | Widely Available (feedback únicamente tras interacción del usuario). | `forms`, `accessibility` |
| **Sanitización DOM y Sonda API Local** | Construcción 100 % con `document.createElement` + `textContent` + `.replaceChildren()` (cero `innerHTML`); `AbortSignal.timeout(800)` en `fetch()`. | Widely Available (`replaceChildren`, `AbortSignal.timeout`). | `sanitize-untrusted-html`, `trusted-types`, `js` |

---

## 3. Arquitectura de Información y Presupuesto *Above-the-Fold*

### 3.1 Shell Visual Datalaria (Cabecera Focus Mode en 1 Sola Fila)
- **Altura estricta:** `<= 64 px` en escritorio (`>= 768 px`) y `<= 56 px` en móvil (`390 px`, `flex-wrap: nowrap` con menú compacto o colapso limpio, `0` desbordamiento horizontal).
- **Máximo 4 agrupaciones lógicas en `<header>`:**
  1. **Identidad & Retorno:** Enlace `← Datalaria` (localizado a `/es/apps/` o `/en/apps/`) + marca `Agentic Radar` con icono SVG inline (`viewBox`, cero emojis rotos).
  2. **Conmutador de 3 Vistas (`role="tablist"`):**
     - `Cockpit` (KPIs + Tabla Ordenable + Consola CrewAI)
     - `Simulador BOM` (Inyector PDN + Grafo SVG interactivo `MPN → AML → Assembly → SKU`)
     - `LTB vs. FFF` (Calculadora financiera + puente APICS Stock de Seguridad)
  3. **Estado Dual-Mode:** Píldora compacta `● SANDBOX` / `● LIVE` (sin `animate-ping` cuando `prefers-reduced-motion: reduce`).
  4. **Controles de Utilidad + 1 CTA Primario:** Selector `ES | EN`, toggle tema `Dark | Light`, botón `Ficha ↗` (localizado) y botón CTA primario `Importar CSV` (abre `<dialog>`).

### 3.2 Presupuesto Vertical *Above-the-Fold* (`1366×768` / `1440×900`)
- Cabecera (`<= 64 px`) + Barra compacta de 3 Escenarios Preset en 1 clic (`<= 48 px`) = **`<= 112 px`** (cumple holgadamente el techo de `130 px`).
- Los **4 KPIs ejecutivos** y las primeras filas de la **Tabla de Ensamblajes Impactados** (o el Grafo BOM) quedan 100 % visibles en el primer pantallazo sin hacer scroll.

### 3.3 Navegación Móvil (`<= 768 px`)
- En móvil (`390×844`), las 3 vistas pasan a una barra de pestañas fija inferior o barra segmentada con objetivos táctiles `>= 44×44 px` y `padding-bottom: max(8px, env(safe-area-inset-bottom))`.
- Las tarjetas KPI se apilan en rejilla `2×2` compacta y la tabla activa su transformación `@container (width < 600px)` a tarjetas legibles sin scroll horizontal de página (`scrollWidth === clientWidth`).

---

## 4. Matriz de Estados de Interfaz (Cero Pantallas Muertas)

| Vista / Componente | Estado Vacío (*Empty State*) | Estado de Carga (*Loading*) | Estado de Error (*Graceful Fallback*) | Estado Poblado (*Ideal*) |
| :--- | :--- | :--- | :--- | :--- |
| **Cockpit / Tabla BOM** | Si el usuario limpia el filtro o sube un CSV sin MPNs en riesgo: mensaje explicativo + botón `⚡ Cargar escenario industrial (1 clic)`. | Skeleton con altura reservada (`min-height` fija, `CLS < 0.1`) durante el sondeo inicial `<= 800 ms` en `localhost` (en CDN estático renderiza en `0 ms`). | **Nunca** muestra `> OFFLINE` ni disfraza un error de vacío. Si falla la API local o el CSV tiene columnas faltantes, muestra banner recuperable `role="alert"` con columnas esperadas y botón `Continuar con Sandbox`. | 4 KPIs `tabular-nums`, tabla ordenable con badges IEC 62402 y consola CrewAI con filtro y replay. |
| **Grafo SVG BOM (Vista 2)** | Mensaje *"Selecciona o inyecta un MPN para trazar el árbol de impacto"* + 3 botones de escenario. | Transición instantánea (`< 16 ms`) sin spinner bloqueante. | Si el CSV importado contiene un ciclo en el grafo BOM, detiene la recursión de forma segura (`INV-OBS-4`) y muestra aviso visible `⚠️ Ciclo BOM detectado y aislado`. | Grafo vectorial SVG limpio de 4 columnas (`MPN → AML → Subensamblaje → SKU`) con nodos clicables y resaltado de ruta crítica. |
| **Calculadora LTB vs. FFF (Vista 3)** | Valores pre-cargados del componente seleccionado (nunca en blanco). | Recálculo en tiempo real al escribir (`input` event, `< 5 ms`). | Validación `:user-invalid` + `aria-invalid="true"` + texto de rango válido bajo el campo erróneo; congela el veredicto hasta corregir. | Tarjetas comparativas `TC_LTB` vs. `TC_FFF`, Capital Circulante, Break-Even, veredicto destacado y bloque PLG contextual a `pack-stock` (7 €) y `suite-03` (22 €). |
| **Modal Importar CSV (`<dialog>`)** | Zona drop/selector de archivo + botones `⚡ Probar con BOM de ejemplo (1 clic)` y `⬇ Descargar plantilla CSV`. | Feedback inmediato de filas leídas y sanitizadas. | Lista clara de columnas ausentes (`End_Product_SKU`, `End_Product_Margin`, `Assembly_PN`, `Component_PN`, `Manufacturer_PN`, `Lifecycle`) sin cerrar el modal. | Resumen de nodos importados (`X` SKUs, `Y` componentes, `Z` alertas EOL) y aplicación directa al Cockpit. |

---

## 5. Bloque PLG Contextual (Integración No Intrusiva)

- Ubicado al pie del Cockpit y de forma contextual bajo el veredicto de la Vista 3 (*LTB vs. FFF*), con estética coherente (`--bg-surface`, borde `--accent-secondary` sutil, cero banners intrusivos bloqueando la herramienta):
  - **Tarjeta Principal (Stock & LTB):** Conecta el cálculo de $SS_{\text{LTB}}$ con **`pack-stock` — Calculadora de Stock de Seguridad & ROP (`7 €`)** (`?embed=1`).
  - **Tarjeta Complementaria (Riesgo & Suite):** Enlaza a **`pack-amfe` (`7 €`)** y **`suite-03` — Pack Suite 3: Control Operativo (`22 €`, ahorro 35 %)** (`?embed=1`).
  - Todos los botones llevan clase compatible con checkout embebido Lemon Squeezy y disparan `gtag('event', 'obs_cta_click', { ..., transport_type: 'beacon' })`.

---

## 6. Checklist del Gate de Revisión UX/UI (Pre-QA para `OBS-2` y `OBS-4`)

Para que [`04-ux-ui`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md) emita `UX_PASS` antes del gate final de `11-qa-verifier`:

- [ ] **Modern Web Guidance & Zero-CDN (`INV-OBS-1`, `INV-OBS-3`):** Cero `cdn.tailwindcss.com`; `<dialog>` nativo sin `role="dialog"`/`aria-modal` manual; `responsive-table` + `sortable-table` sin reconstruir `<tbody>`; `scrollbar-color`/`scrollbar-width` con `@supports not`; `0` hallazgos en `modern-web-guidance legacy-scan`.
- [ ] **Focus Mode & Responsive (`390×844` / `768×1024` / `1440×900`):** Cabecera `<= 64 px` desktop y `<= 56 px` móvil; `scrollWidth === clientWidth` en ES y EN (+25 % longitud en español); controles táctiles `>= 44×44 px` y `env(safe-area-inset-bottom)` en barra móvil.
- [ ] **Accesibilidad WCAG 2.2 AA:** Contraste `>= 4.5:1` en todo texto (`>= 3:1` en bordes/scrollbars/iconos), `:focus-visible` nítido, `aria-live="polite"` / `role="status"` en resultados dinámicos, soporte explícito de `@media (prefers-reduced-motion: reduce)` deteniendo pulsos y transiciones, escala de texto en `rem`.
- [ ] **Fidelidad a Tokens y Cero Glifos Rotos:** Cero hexadecimales fuera de §2.1, `font-variant-numeric: tabular-nums` en todas las cifras, SVGs inline (`viewBox`) en iconos y grafo BOM (cero emojis tofu `□`), `CLS < 0.1`.
- [ ] **Portada Real (`OBS-4`):** `cover.png` (`1280×800`) generada sobre captura real del Cockpit v2.0 respetando Safe Zone `[145px, 1055px]`.
