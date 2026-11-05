# Especificación de Diseño UX/UI: Datalaria Helix Spec Builder (`helix`)

> **ID de Diseño:** `DESIGN-APP-HELIX`  
> **Spec Técnica Vinculada:** [`specs/apps/helix/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/helix/spec.md)  
> **Agente Propietario:** [`04-ux-ui` (Diseñador UX/UI)](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md)  
> **Preset Estético Seleccionado:** `Executive Data-Dense` (AI Engineering Cockpit)

---

## 1. Dirección Estética y Psicología de Usuario

### 1.1 Perfil Visual del Usuario y Contexto de Uso
- **Quién lo usa y dónde:** Consultores B2B, Tech Leads, PMs, analistas financieros y profesionales no desarrolladores que quieren estructurar su software con IA sin caer en el *vibe debt*. Lo usan desde portátiles (13" a 16") y monitores de sobremesa.
- **Sensación en los primeros 3 segundos:** Control de ingeniería absoluto, rigor C-Level, cero humo de marketing, diagnóstico inmediato y claridad cristalina sobre cómo orquestar agentes.
- **Preset de Dirección Activo:**
  - **`Executive Data-Dense` (AI Engineering Cockpit):** Modo oscuro profundo (`#0b0f17`), paneles semitransparentes con bordes sutiles iluminados (`#1e293b`), indicadores de estado en color esmeralda (`#10b981`), ámbar (`#f59e0b`), coral (`#ef4444`) e índigo (`#6366f1`).

### 1.2 El «Momento Firma» (*Signature Wow Moment*)
> **El Cockpit Reactivo de Triaje y Diagnóstico en Vivo:** Al responder a cualquiera de los 5 pasos de la entrevista o al hacer clic en uno de los 3 botones de demostración (`⚡ Cargar ejemplo`), el **indicador circular de `SpecQualityScore` (`0..100`)**, el medidor de **Riesgo de `Vibe-Debt`**, la **Tarjeta `TRIAGE HELIX` de 6 líneas canónicas** y la **Matriz de las 4 Células (12 Agentes: Activos vs. Banquillo)** se recalculan instantáneamente en `< 16ms`, generando en memoria los 5 archivos SDD listos para descargar en `.zip` o copiar en Mega-Prompt.

---

## 2. Sistema de Design Tokens (Variables CSS Canónicas)

### 2.1 Paleta Semántica de Color
| Token CSS | Valor (Dark Default) | Uso Semántico Exclusivo |
| :--- | :--- | :--- |
| `--bg-canvas` | `#0b0f17` | Fondo principal de la aplicación |
| `--bg-surface` | `#111827` | Paneles, tarjetas y contenedores de cockpit |
| `--bg-elevated` | `#1e293b` | Modales, previsualizaciones de código y menús |
| `--text-primary` | `#f8fafc` | Títulos, métricas numéricas y texto principal |
| `--text-secondary` | `#94a3b8` | Subtítulos, labels y explicaciones de agentes |
| `--accent-primary` | `#6366f1` | Índigo de acción primaria (CTA de descarga/copiado) |
| `--accent-teal` | `#0d9488` | Acento secundario y badges de agentes de construcción |
| `--status-success` | `#10b981` | Score >= 80, tests en verde y agentes convocados |
| `--status-warning` | `#f59e0b` | Avisos de omisión de Non-Goals o dependencias |
| `--status-danger` | `#ef4444` | Alto riesgo de Vibe Debt o veto de seguridad/QA |
| `--border-subtle` | `rgba(148, 163, 184, 0.12)` | Delimitadores y bordes de paneles |

### 2.2 Escala Tipográfica y Espaciado
- **Cabeceras (`--font-display`):** `'Outfit', system-ui, sans-serif` (600, 700).
- **Cuerpo (`--font-sans`):** `'Inter', system-ui, sans-serif` (400, 500, 600).
- **Código y Métricas (`--font-mono`):** `'JetBrains Mono', monospace` (`tabular-nums`).
- **Radios:** `--radius-sm: 6px`, `--radius-md: 10px`, `--radius-lg: 14px`.

---

## 3. Arquitectura de Información y Presupuesto *Above-the-Fold*

1. **Cabecera Ejecutiva (`height <= 60px`):**
   - Retorno al portal `← Datalaria` (dinámico `/es/` o `/en/`), logotipo Helix, selector de idioma `ES | EN`, botón de demostración rápida en 1 clic y CTA de acceso a Helix Core Kit (Waitlist 19 €).
2. **Layout Bipolar de Alto Rendimiento (2 Columnas en Escritorio):**
   - **Columna Izquierda (Asistente Guiado SDD — 5 Pilares de 20 pts):**
     1. Identidad, Problema y Usuario objetivo.
     2. Alcance Negativo y Non-Goals.
     3. Superficies técnicas afectadas (docs, ui, frontend, backend, apis, monetization, auth_security).
     4. Invariantes innegociables `INV-*`.
     5. Verification Gates y Rollback.
   - **Columna Derecha (Cockpit de Diagnóstico y Artefactos en 4 Pestañas):**
     - Score Gauge `0..100` y Nivel de Vibe-Debt permanente.
     - Pestaña 1: Cuadrícula del Escuadrón (12 Agentes: Convocados vs. Banquillo).
     - Pestaña 2: Modo A — Generador de Kit SDD (`AGENTS.md`, `_constitution.md`, `spec.md`, `design.md`, `ROADMAP.md`) y descarga `.zip` en cliente.
     - Pestaña 3: Modo B — Mega-Prompt SDD copiable en 1 clic.
     - Pestaña 4: Escalera de Valor (Sandbox vs Starter vs Core Kit).
3. **Accesibilidad WCAG 2.2 AA:**
   - Contraste `>= 4.5:1` en todos los textos.
   - Soporte de teclado (tabulación y cierre con `Escape`).
   - Cero dependencias externas en el cálculo de métricas (`INV-HELIX-6`).
