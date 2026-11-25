# Especificación de Diseño UX/UI: [NOMBRE DE LA APLICACIÓN] (`[app-slug]`)

> **ID de Diseño:** `DESIGN-APP-[SLUG]`  
> **Spec Técnica Vinculada:** [`specs/apps/[app-slug]/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/)  
> **Agente Propietario:** [`04-ux-ui` (Diseñador UX/UI)](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md)  
> **Skill Web de Referencia:** [`.agents/skills/modern-web-guidance/SKILL.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/.agents/skills/modern-web-guidance/SKILL.md) (`ADR-031`, política *Baseline Widely Available* + fallback ligero `<= 20` líneas para *Newly Available*)  
> **Preset Estético Seleccionado:** `Executive Data-Dense | Minimal Utility | Consumer Playful | Editorial Knowledge | Mobile-First Field`

---

## 1. Dirección Estética y Psicología de Usuario

### 1.1 Perfil Visual del Usuario y Contexto de Uso
- **Quién lo usa y dónde:** [Ej. Director de Operaciones en portátil de 13"-16" durante comité semanal / Profesional autónomo desde móvil].
- **Sensación que debe transmitir en los primeros 3 segundos:** [Ej. Precisión ejecutiva C-Level, control instantáneo, cero fricción cognitiva, *Content-First*].
- **Preset de Dirección Activo:**
  - [ ] **`Executive Data-Dense` (Estándar B2B Datalaria — LifeOps / Pulse):** Modo oscuro profundo (`#0b0f17` / `#0f172a`), bordes sutiles iluminados, alta densidad informativa sin ruido, KPIs con jerarquía clara.
  - [ ] **`Minimal Utility` (Herramientas rápidas y calculadoras):** Foco absoluto en el input principal y el resultado inmediato en 1 pantalla sin scroll.
  - [ ] **`Editorial Knowledge` (Lectura profunda, documentación interactiva):** Contraste tipográfico cálido, ancho de línea óptimo (`65–75ch`), navegación lateral limpia.
  - [ ] **`Consumer Playful` (Juegos, aprendizaje, hábitos):** Micro-interacciones expresivas, feedback gamificado y color vibrante controlado.
  - [ ] **`Mobile-First Field` (Uso en calle o móvil vertical):** Botones táctiles $\ge 44\times44\text{ px}$, navegación inferior al pulgar con `env(safe-area-inset-bottom)`.

### 1.2 El «Momento Firma» (*Signature Wow Moment*)
> Toda aplicación diseñada con Datalaria Helix debe incluir **una (y solo una) micro-interacción o componente firma** que sorprenda positivamente al usuario y mejore la usabilidad real (nunca decoración gratuita).
- **Descripción del Momento Firma:** [Ej. Importación de CSV en 1 clic con diagnóstico instantáneo animado / Conmutador de vistas con View Transition suave / Tarjeta de puntuación en vivo].

---

## 2. Sistema de Design Tokens y Primitivas Modern Web Guidance

> **Regla `INV-UX-1`:** Queda prohibido usar colores hexadecimales arbitrarios fuera de los tokens declarados en esta tabla.  
> **Regla `INV-UX-2` (Platform-First / `ADR-031`):** Antes de introducir librerías JS para modales, tooltips, popovers, selects o animaciones, consultar `.agents/skills/modern-web-guidance/SKILL.md` y emplear primitivas nativas Baseline (`<dialog>`, Popover API, CSS Anchor Positioning, `@container`, `subgrid`, `:has()`, `:user-invalid`, `oklch()`/`light-dark()`, `text-wrap: balance`, View Transitions con `@supports` y `prefers-reduced-motion`).

### 2.1 Paleta Semántica de Color (`color-scheme: dark light`)
| Token CSS | Valor (Dark Mode / Default) | Valor (Light Mode / Opcional) | Uso Semántico Exclusivo |
| :--- | :--- | :--- | :--- |
| `--bg-canvas` | `#0b0f17` | `#f8fafc` | Fondo principal de la aplicación |
| `--bg-surface` | `#111827` | `#ffffff` | Tarjetas, paneles, contenedores primarios |
| `--bg-elevated` | `#1e293b` | `#f1f5f9` | Modales (`<dialog>`), popovers, cabeceras flotantes |
| `--text-primary` | `#f8fafc` | `#0f172a` | Títulos, cifras KPI y texto principal (Contraste $\ge 7:1$) |
| `--text-secondary` | `#94a3b8` | `#475569` | Etiquetas, subtítulos y metadatos (Contraste $\ge 4.5:1$) |
| `--accent-primary` | `#0ea5e9` | `#0284c7` | Acción primaria (CTA principal) y estado activo |
| `--accent-secondary` | `#8b5cf6` | `#7c3aed` | Destacados Pro / IA / Suite B2B |
| `--status-success` | `#10b981` | `#059669` | Confirmación, paridad completa, estado saludable |
| `--status-warning` | `#f59e0b` | `#d97706` | Avisos preventivos, caducidad próxima |
| `--status-danger` | `#ef4444` | `#dc2626` | Errores bloqueantes, alertas críticas |
| `--border-subtle` | `rgba(148, 163, 184, 0.15)` | `rgba(15, 23, 42, 0.12)` | Divisores y bordes de tarjetas |

### 2.2 Escala Tipográfica, Layout y Espaciado
- **Fuente de Títulos y KPIs (`--font-display`):** `'Outfit', system-ui, sans-serif` (Pesos `600`, `700`; `text-wrap: balance` en encabezados).
- **Fuente de Interfaz y Lectura (`--font-sans`):** `'Inter', system-ui, sans-serif` (Pesos `400`, `500`, `600`; escala relativa en `rem` respetando ajustes del SO).
- **Fuente Monoespaciada / Datos (`--font-mono`):** `'JetBrains Mono', monospace` (`font-variant-numeric: tabular-nums` obligatorio en tablas de números).
- **Layout Responsivo y Radios:** Preferir `@container` en tarjetas/componentes reutilizables, `scrollbar-gutter: stable`, `--radius-sm: 6px`, `--radius-md: 10px`, `--radius-lg: 14px`.

### 2.3 Primitivas Nativas Seleccionadas y Fallbacks (`Modern Web Guidance`)
| Patrón UI | Primitiva Nativa Elegida | Soporte Baseline & Fallback (`<= 20` líneas si *Newly Available*) | Guía `modern-web-guidance` Consultada |
| :--- | :--- | :--- | :--- |
| **Modales / Confirmación** | `<dialog>` + `showModal()` + `::backdrop` | Widely Available (sin polyfill) | `dialog`, `light-dismiss-a-dialog` |
| **Tooltips / Menús** | Popover API (`popover="auto"`) + CSS Anchor Positioning | Fallback posicional simple vía `@supports not (anchor-name: --a)` | `position-aware-tooltips`, `viewport-aware-dropdowns` |
| **Validación Formularios** | `:user-invalid` + `aria-invalid` sincronizado | Widely Available (feedback solo tras interacción) | `accessible-error-announcement` |

---

## 3. Arquitectura de Información y Presupuesto *Above-the-Fold*

1. **Shell Visual Datalaria (Constitución Art. 5.2):**
   - Cabecera compacta de **1 sola fila en escritorio** (`height <= 64px`; móvil `<= 56px` con `flex-wrap` limpio y `0` desbordamiento horizontal) con enlace de retorno `← Datalaria`, identidad de la App, selector de idioma `ES | EN`, estado de modo (`Sandbox` / `Pro`) y **1 único botón CTA primario destacado**.
2. **Presupuesto Vertical *Above-the-Fold* (Portátil 1366×768 / 1440×900):**
   - La suma de cabecera + banners informativos no puede superar los **`130 px` verticales**, garantizando que los KPIs principales y el área de trabajo sean visibles sin hacer scroll (*Focus Mode*).

---

## 4. Matriz de Estados de Interfaz (Cero Pantallas Muertas)

| Vista / Componente | Estado Vacío (*Empty State*) | Estado de Carga (*Loading*) | Estado de Error (*Graceful Fallback*) | Estado Poblado (*Ideal*) |
| :--- | :--- | :--- | :--- | :--- |
| **Área Principal** | Mensaje orientativo + botón `⚡ Cargar ejemplo en 1 clic` | Skeleton sutil sin saltos de layout (`CLS < 0.1`) | Banner no bloqueante con causa clara y opción de reintentar/continuar en local (**nunca** disfrazado de estado vacío) | Tabla / Kanban / Gráfico con jerarquía visual limpia |

---

## 5. Checklist del Gate de Revisión UX/UI (Pre-QA)

Para que [`04-ux-ui`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md) otorgue el visto bueno (`UX_PASS`) antes del gate final de `11-qa-verifier`:
- [ ] **Modern Web Guidance & Baseline:** Guías relevantes consultadas en `.agents/skills/modern-web-guidance/SKILL.md`; primitivas nativas aplicadas (`<dialog>`, Popover, `@container`, `:user-invalid`) sin librerías redundantes.
- [ ] **Responsive y Móvil (`390px` / `768px` / `1440px`):** `scrollWidth == clientWidth` sin solapes; barras inferiores con `env(safe-area-inset-bottom)` y objetivos táctiles $\ge 44\times44\text{ px}$; tablas anchas en contenedor `overflow-x: auto`.
- [ ] **Accesibilidad (WCAG 2.2 AA) y Movimiento:** Contraste $\ge 4.5:1$ (`3:1` UI), `:focus-visible`, escala `rem`, cierre con `Escape`, `aria-label` en botones de icono y soporte explícito de `prefers-reduced-motion`.
- [ ] **Core Web Vitals y Fidelidad a Tokens:** Cero colores arbitrarios, `tabular-nums`, `width`/`height` en imágenes (`CLS < 0.1`), `INP` fluido y cero glifos rotos (`□`, usar SVGs inline).
- [ ] **Bilingüismo Visual y Conversión:** Textos en español (+20–25 % longitud) sin romper botones ni cabeceras; captura real `1600×980 px` si existe Kit asociado.
