# Especificación de Diseño UX/UI: Conversor de Unidades ("Engineering Workbench v2.0") (`conversor`)

> **ID de Diseño:** `DESIGN-APP-CONVERSOR`  
> **Spec Técnica Vinculada:** [`specs/apps/conversor/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/conversor/spec.md)  
> **Agente Propietario:** [`04-ux-ui` (Diseñador UX/UI)](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md)  
> **Preset Estético Seleccionado:** `Minimal Utility` hibridado con `Executive Data-Dense`

---

## 1. Dirección Estética y Psicología de Usuario

### 1.1 Perfil Visual del Usuario y Contexto de Uso
- **Quién lo usa y dónde:** Ingenieros de telecomunicaciones, industriales y de software, analistas cuantitativos, científicos y estudiantes técnicos trabajando en portátil de escritorio o tableta. Necesitan respuestas instantáneas en microsegundos, validación de fórmulas, cambio de separadores decimales entre herramientas (Excel US/EU, Python, MATLAB) y cero distracciones o banners publicitarios.
- **Sensación en los primeros 3 segundos:** Precisión quirúrgica de laboratorio, estética instrumental moderna ("Cockpit de ingeniería"), claridad visual sin fricción y confianza metrológica absoluta.
- **Preset de Dirección Activo:** `Minimal Utility` + `Executive Data-Dense` (Modo oscuro `#0b0f17`, tarjetas `#111827` con bordes sutiles `rgba(148, 163, 184, 0.15)`, acentos cian/azul `#0ea5e9` e índigo `#6366f1`, y tipografía monoespaciada para todos los valores numéricos).

### 1.2 El «Momento Firma» (*Signature Wow Moment*)
> **Omni-Matrix Multi-Escala + Batch Scratchpad en Tiempo Real:**  
> Al escribir un número en cualquier convertidor, la aplicación muestra instantáneamente una **Omni-Matrix** con la equivalencia simultánea en las 4 unidades más relevantes de la magnitud, junto con la traza de la fórmula SI paso a paso. Además, en la pestaña **Batch Scratchpad**, el usuario puede pegar columnas de miles de datos desde Excel y ver cómo se transforman y formatean al instante sin enviar un solo byte a ningún servidor.

---

## 2. Sistema de Design Tokens (Variables CSS Canónicas)

> **Invariante `INV-CONV-3`:** 100% CSS nativo sin dependencias externas (erradicación completa de `cdn.tailwindcss.com`).

### 2.1 Paleta Semántica de Color Dual (Dark Mode & Light Mode)
| Token CSS | Valor Dark (Canónico) | Valor Light (`data-theme="light"`) | Uso Semántico Exclusivo |
| :--- | :--- | :--- | :--- |
| `--bg-canvas` | `#0b0f17` | `#f8fafc` | Fondo principal de la aplicación y rejilla sutil |
| `--bg-surface` | `#111827` | `#ffffff` | Tarjetas de cálculo, paneles de control, contenedor activo |
| `--bg-elevated` | `#1e293b` | `#f1f5f9` | Desplegables, modales, píldoras activas, hover de tarjetas |
| `--bg-input` | `#151d2c` | `#ffffff` | Fondo de inputs numéricos y áreas de texto |
| `--bg-header` | `rgba(17, 24, 39, 0.88)` | `rgba(255, 255, 255, 0.92)` | Fondo translúcido con backdrop-filter de cabecera |
| `--bg-surface-subtle` | `rgba(30, 41, 59, 0.45)` | `rgba(241, 245, 249, 0.85)` | Contenedores auxiliares (Constantes, Omni-Matrix) |
| `--text-primary` | `#f8fafc` | `#0f172a` | Cifras de resultados, encabezados, títulos |
| `--text-secondary` | `#94a3b8` | `#334155` | Etiquetas de unidades, fórmulas, notas explicativas |
| `--text-muted` | `#64748b` | `#64748b` | Atajos, marcas secundarias, tooltips |
| `--accent-primary` | `#0ea5e9` | `#0284c7` | Píldora activa, foco de inputs, botón intercambiar `⇄` |
| `--accent-hover` | `#38bdf8` | `#0369a1` | Estado hover de botones primarios y acentos |
| `--accent-secondary` | `#8b5cf6` | `#7c3aed` | Acciones de lote (Batch Scratchpad) y constantes |
| `--status-success` | `#10b981` | `#059669` | Notificación de copiado al portapapeles (`✓ Copiado`) |
| `--border-subtle` | `rgba(148, 163, 184, 0.14)` | `rgba(100, 116, 139, 0.22)` | Bordes de tarjetas y divisiones |
| `--border-focus` | `#0ea5e9` | `#0284c7` | Anillo de enfoque accesible (WCAG 2.2 AA) |

### 2.2 Escala Tipográfica y Espaciado
- **Fuente de Títulos y Categorías (`--font-display`):** `'Outfit', system-ui, -apple-system, sans-serif` (Pesos `600`, `700`).
- **Fuente de Interfaz y Textos (`--font-sans`):** `'Inter', system-ui, -apple-system, sans-serif` (Pesos `400`, `500`).
- **Fuente de Números, Fórmulas y Datos (`--font-mono`):** `'JetBrains Mono', 'Fira Code', monospace` con `font-variant-numeric: tabular-nums` obligatorio.
- **Radios:** `--radius-sm: 6px`, `--radius-md: 10px`, `--radius-lg: 16px`.
- **Sombras:** `--shadow-card: 0 4px 20px rgba(0, 0, 0, 0.4)`, `--shadow-glow: 0 0 15px rgba(14, 165, 233, 0.25)`.

---

## 3. Arquitectura de Información y Presupuesto *Above-the-Fold*

1. **Shell Visual Datalaria (Constitución Art. 5.2 — Estándar Ecosistema Apps):**
   - Altura de cabecera: adaptativa (`56px` base, auto en móvil con wrap ergonómico).
   - Elementos alineados horizontalmente:
     - Izquierda: `← Datalaria` (enlace al catálogo general `/es/apps/` o `/en/apps/`) + Icono `🔄` + Título `Conversor Pro` + Badge `v2.0.0`.
     - Centro: Conmutador de vista rápida de categorías (Píldoras compactas o select en móvil).
     - Derecha (Tríada de Enlaces del Ecosistema):
       1. Botón selector de idioma `ES | EN`.
       2. Botón a la Ficha de la App (`📋 Ficha de la App` -> `/es/apps/conversor/` o `/en/apps/conversor/`) para consultar objetivos, tecnologías y roadmap evolutivo.
       3. Botón al Post Editorial (`📖 Guía Técnica` -> `/es/posts/app_conversor_unidades/` o `/en/posts/app_unit_converter/`).
       4. CTA sutil a recursos (`📦 Kits B2B →` -> `/es/recursos/` o `/en/resources/`).
2. **Distribución del Espacio de Trabajo:**
   - **Fila Superior:** Barra de categorías (7 pestañas: *Dimensión, Energía, Tiempo, Mecánica, Informática, Radiofrecuencia, Scratchpad Masivo*) + Barra de Constantes CODATA rápidas.
   - **Panel Central (Conversión Dual Directa):**
     - Columna Origen: Input con foco automático + Selector de unidad.
     - Botón central: `⇄ Invertir` accesible por teclado (atajo `X`).
     - Columna Destino: Display numérico destacado en `JetBrains Mono` con botón `Copiar` (atajo `C`) + Selector de unidad.
     - Barra de configuración: Precisión decimal (`Auto`, `2`, `4`, `6`, `8`, `Sci`) + Botón compartir cálculo con URL (`🔗`).
   - **Panel Inferior (Omni-Matrix):** 4 tarjetas con equivalencias instantáneas en unidades complementarias + Fórmula física explicativa en KaTeX/LaTeX legible.
   - **Modo Scratchpad Masivo (Pestaña 7):** Vista dividida en 2 paneles (Entrada multilínea ⇔ Salida convertida) con selector de formato (`US ⇔ EU`), selector de unidad física opcional y botón `⚡ Cargar ejemplo`.

---

## 4. Matriz de Estados de Interfaz (Cero Pantallas Muertas)

| Vista / Componente | Estado Vacío (*Empty State*) | Estado Activo / Poblado | Estado de Error (*Fallback*) | Feedback de Acción |
| :--- | :--- | :--- | :--- | :--- |
| **Conversor Principal** | Muestra valor por defecto `1` (o parámetro URL) listo para editar | Cálculo instantáneo en microsegundos | Si se introduce NaN o valor fuera de rango, muestra `--` en gris neutro sin romper | Botón copiar cambia a `✓ Copiado` en verde durante 1.8s |
| **Batch Scratchpad** | Textarea vacío con placeholder didáctico y botón `⚡ Cargar lote de ejemplo (1 clic)` | Columna formateada/convertida con contador de líneas procesadas | Si una línea contiene texto inválido, marca `[Entrada inválida en línea N]` sin abortar el resto | Botón de copiar todo o descargar CSV |
| **Constantes CODATA** | Selector desplegable con 8 constantes clave ($c, g_0, h, k_B, N_A, \varepsilon_0, R, e$) | Al pulsar una constante, se inyecta su valor exacto SI en el conversor activo | -- | Notificación sutil con símbolo y valor inyectado |

---

## 5. Checklist del Gate de Revisión UX/UI (Pre-QA)

- [x] **Responsive en 3 Viewports:** `390px` (móvil vertical apilado), `768px` (tablet dos columnas fluidas), `1440px` (pantalla ancha optimizada sin desbordamiento).
- [x] **Accesibilidad WCAG 2.2 AA:** Contraste mínimo `5.5:1` en texto y `3:1` en componentes UI; todos los inputs poseen `<label>` o `aria-label`; navegación 100% funcional por teclado (`Tab`, `Shift+Tab`, `Enter`, `X` para invertir, `C` para copiar).
- [x] **Cero Dependencias de Red Externas:** CSS nativo compilado dentro de la aplicación, sin peticiones bloqueantes a CDNs externos.
- [x] **Paridad Bilingüe Visual:** Los textos y abreviaturas en español e inglés mantienen la misma altura y no provocan saltos de línea indeseados.
