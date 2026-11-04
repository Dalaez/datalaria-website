# Especificación de Diseño UX/UI: [NOMBRE DE LA APLICACIÓN] (`[app-slug]`)

> **ID de Diseño:** `DESIGN-APP-[SLUG]`  
> **Spec Técnica Vinculada:** [`specs/apps/[app-slug]/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/)  
> **Agente Propietario:** [`04-ux-ui` (Diseñador UX/UI)](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md)  
> **Preset Estético Seleccionado:** `Executive Data-Dense | Minimal Utility | Consumer Playful | Editorial Knowledge | Mobile-First Field`

---

## 1. Dirección Estética y Psicología de Usuario

### 1.1 Perfil Visual del Usuario y Contexto de Uso
- **Quién lo usa y dónde:** [Ej. Director de Operaciones en portátil de 13"-16" durante comité semanal / Profesional autónomo desde móvil].
- **Sensación que debe transmitir en los primeros 3 segundos:** [Ej. Precisión ejecutiva C-Level, control instantáneo, cero fricción cognitiva].
- **Preset de Dirección Activo:**
  - [ ] **`Executive Data-Dense` (Estándar B2B Datalaria — LifeOps / Pulse):** Modo oscuro profundo (`#0b0f17` / `#0f172a`), bordes sutiles iluminados, alta densidad informativa sin ruido, KPIs con jerarquía clara.
  - [ ] **`Minimal Utility` (Herramientas rápidas y calculadoras):** Foco absoluto en el input principal y el resultado inmediato en 1 pantalla sin scroll.
  - [ ] **`Editorial Knowledge` (Lectura profunda, documentación interactiva):** Contraste tipográfico cálido, ancho de línea óptimo (`65–75ch`), navegación lateral limpia.
  - [ ] **`Consumer Playful` (Juegos, aprendizaje, hábitos):** Micro-interacciones expresivas, feedback gamificado y color vibrante controlado.
  - [ ] **`Mobile-First Field` (Uso en calle o móvil vertical):** Botones táctiles $\ge 44\times44\text{ px}$, navegación inferior al pulgar.

### 1.2 El «Momento Firma» (*Signature Wow Moment*)
> Toda aplicación diseñada con Datalaria Helix debe incluir **una (y solo una) micro-interacción o componente firma** que sorprenda positivamente al usuario y mejore la usabilidad real (nunca decoración gratuita).
- **Descripción del Momento Firma:** [Ej. Importación de CSV en 1 clic con diagnóstico instantáneo animado / Conmutador de vistas segmentado con transición fluida / Tarjeta de puntuación en vivo].

---

## 2. Sistema de Design Tokens (Variables CSS Canónicas)

> **Regla `INV-UX-1`:** Queda prohibido usar colores hexadecimales arbitrarios fuera de los tokens declarados en esta tabla.

### 2.1 Paleta Semántica de Color
| Token CSS | Valor (Dark Mode / Default) | Valor (Light Mode / Opcional) | Uso Semántico Exclusivo |
| :--- | :--- | :--- | :--- |
| `--bg-canvas` | `#0b0f17` | `#f8fafc` | Fondo principal de la aplicación |
| `--bg-surface` | `#111827` | `#ffffff` | Tarjetas, paneles, contenedores primarios |
| `--bg-elevated` | `#1e293b` | `#f1f5f9` | Modales, desplegables, cabeceras flotantes |
| `--text-primary` | `#f8fafc` | `#0f172a` | Títulos, cifras KPI y texto principal (Contraste $\ge 7:1$) |
| `--text-secondary` | `#94a3b8` | `#475569` | Etiquetas, subtítulos y metadatos (Contraste $\ge 4.5:1$) |
| `--accent-primary` | `#0ea5e9` | `#0284c7` | Acción primaria (CTA principal) y estado activo |
| `--accent-secondary` | `#8b5cf6` | `#7c3aed` | Destacados Pro / IA / Suite B2B |
| `--status-success` | `#10b981` | `#059669` | Confirmación, paridad completa, estado saludable |
| `--status-warning` | `#f59e0b` | `#d97706` | Avisos preventivos, caducidad próxima |
| `--status-danger` | `#ef4444` | `#dc2626` | Errores bloqueantes, alertas críticas |
| `--border-subtle` | `rgba(148, 163, 184, 0.15)` | `rgba(15, 23, 42, 0.12)` | Divisores y bordes de tarjetas |

### 2.2 Escala Tipográfica y Espaciado
- **Fuente de Títulos y KPIs (`--font-display`):** `'Outfit', system-ui, sans-serif` (Pesos `600`, `700`).
- **Fuente de Interfaz y Lectura (`--font-sans`):** `'Inter', system-ui, sans-serif` (Pesos `400`, `500`, `600`).
- **Fuente Monoespaciada / Datos (`--font-mono`):** `'JetBrains Mono', monospace` (`font-variant-numeric: tabular-nums` obligatorio en tablas de números).
- **Radios y Sombras:** `--radius-sm: 6px`, `--radius-md: 10px`, `--radius-lg: 14px`.

---

## 3. Arquitectura de Información y Presupuesto *Above-the-Fold*

1. **Shell Visual Datalaria (Constitución Art. 5.2):**
   - Cabecera compacta de **1 sola fila en escritorio** (`height <= 64px`) con enlace de retorno `← Datalaria`, identidad de la App, selector de idioma `ES | EN`, estado de modo (`Sandbox` / `Pro`) y **1 único botón CTA primario destacado**.
2. **Presupuesto Vertical *Above-the-Fold* (Portátil 1366×768 / 1440×900):**
   - La suma de cabecera + banners informativos no puede superar los **`130 px` verticales**, garantizando que los KPIs principales y el área de trabajo sean visibles sin hacer scroll.

---

## 4. Matriz de Estados de Interfaz (Cero Pantallas Muertas)

| Vista / Componente | Estado Vacío (*Empty State*) | Estado de Carga (*Loading*) | Estado de Error (*Graceful Fallback*) | Estado Poblado (*Ideal*) |
| :--- | :--- | :--- | :--- | :--- |
| **Área Principal** | Mensaje orientativo + botón `⚡ Cargar ejemplo en 1 clic` | Skeleton sutil sin saltos de layout (`CLS < 0.1`) | Banner no bloqueante con causa clara y opción de continuar en modo local | Tabla / Kanban / Gráfico con jerarquía visual limpia |

---

## 5. Checklist del Gate de Revisión UX/UI (Pre-QA)

Para que [`04-ux-ui`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md) otorgue el visto bueno (`UX_PASS`) antes del gate final de `11-qa-verifier`:
- [ ] **Responsive en 3 Viewports:** Sin desbordamiento horizontal indeseado en `390px` (móvil), `768px` (tablet) y `1440px` (escritorio). Tablas anchas con contenedor `overflow-x: auto` e indicador visual de scroll.
- [ ] **Contraste y Accesibilidad (WCAG 2.2 AA):** Contraste mínimo `4.5:1` en texto normal y `3:1` en componentes UI; navegación por teclado (`Tab`, `Escape` cierra modales) y atributos `aria-label` en botones de solo icono.
- [ ] **Fidelidad a Tokens:** Cero colores arbitrarios fuera de la paleta semántica y números alineados con `tabular-nums`.
- [ ] **Bilingüismo Visual:** Los textos en español (generalmente un 20–25 % más largos que en inglés) no rompen botones ni cabeceras en dos líneas.
- [ ] **Activo de Conversión Comercial:** Si la App tiene Kit asociado, existe captura compuesta real `1600×980 px` sin glifos rotos (`□`) para su ficha y catálogo.
