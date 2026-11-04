# Especificación de Diseño y Experiencia de Usuario (`design.md`) — Datalaria Pulse

> **App / Módulo:** `pulse`  
> **Spec Técnica Vinculada:** [`specs/apps/pulse/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/pulse/spec.md) (`SPEC-APP-PULSE` v1.1.0)  
> **Agente Responsable:** [`04-ux-ui`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md)  
> **Preset Estético Seleccionado:** `B2B Executive Dark Cockpit`

---

## 1. Intención Estética y *Signature Wow Moment*

### 1.1 Dirección Visual y Personalidad
- **Arquetipo Visual:** Cabina de mando ejecutiva oscura de alta densidad informativa (*Content Ops Cockpit*), inspirada en Linear y Bloomberg Terminal, con acentos neón semánticos que distinguen el inventario publicado (esmeralda), el roadmap programado (cyan) y el patrimonio léxico/IA (violeta).
- **Sensación al abrir la aplicación (primeros 3 segundos):** Control instantáneo sobre 140+ activos editoriales bilingües con latencia cero, navegación de retorno clara al portal (`← Datalaria`) y acceso en 1 clic tanto al importador de Notion en memoria como al Modo Demo Cloud.

### 1.2 El *"Signature Wow Moment"* (Elemento Diferencial Obligatorio)
1. **Importador y Diagnóstico Instantáneo de Notion en 1 Clic (Client-Side Sandbox):**
   - Dentro del modal *"Previsualizador en Memoria de CSV de Notion"*, el visitante que no tenga un archivo `.csv` a mano puede pulsar **`⚡ Probar con CSV de Notion de ejemplo (1 clic)`**.
   - En `< 100 ms`, la aplicación procesa un lote realista de artículos, puebla las 5 vistas y despliega una **Tarjeta de Diagnóstico Ejecutivo** (*activos analizados, brechas de paridad ES/EN detectadas y borradores listos para migrar*) conectada directamente con el CTA del **Datalaria Pulse Kit (19€)**.
2. **Avance Rápido de Fase en 1 Clic en el Tablero Kanban (`→`):**
   - En las tarjetas de ideas locales, Cloud o Demo dentro del Kanban, un botón de acción rápida permite avanzar el activo a la siguiente columna (`idea → draft → review → scheduled → published`) sin abrir el modal de edición.

---

## 2. Paleta de Colores y Tokens Semánticos (CSS Custom Properties)

```css
:root {
  /* Superficies (Dark Mode Ejecutivo por Defecto) */
  --bg-primary: #0b0f17;
  --bg-elevated: #111827;
  --bg-glass: rgba(17, 24, 39, 0.82);
  --border-subtle: rgba(148, 163, 184, 0.16);
  --border-focus: #10b981;

  /* Tipografía y Jerarquía de Texto */
  --text-primary: #f9fafb;
  --text-secondary: #9ca3af;
  --text-muted: #6b7280;

  /* Acentos de Marca y Acción */
  --accent-primary: #10b981;
  --accent-primary-hover: #059669;
  --accent-secondary: #06b6d4;
  --accent-violet: #8b5cf6;

  /* Estados Semánticos */
  --status-success: #10b981;
  --status-warning: #f59e0b;
  --status-danger: #ef4444;
  --status-info: #06b6d4;
}
```

- **Ratios de Contraste Verificados (WCAG 2.2 AA):**
  - `--text-primary` (`#f9fafb`) sobre `--bg-primary` (`#0b0f17`): **18.4 : 1** (Supera AAA $\ge 7.0:1$).
  - `--text-secondary` (`#9ca3af`) sobre `--bg-elevated` (`#111827`): **6.8 : 1** (Supera AA $\ge 4.5:1$).
  - `--accent-primary` (`#10b981`) sobre `--bg-primary` (`#0b0f17`): **8.1 : 1** (Supera AA $\ge 4.5:1$).

---

## 3. Sistema Tipográfico y Escala Modular

| Uso | Familia Tipográfica | Peso (`font-weight`) | Tamaño (`rem` / `px`) | `line-height` | Reglas Especiales |
| :--- | :--- | :-: | :-: | :-: | :--- |
| **Display / Hero KPI** | `'Outfit', sans-serif` | `700`–`800` | `1.85rem` (`29.6px`) | `1.15` | `font-variant-numeric: tabular-nums` |
| **Títulos de Sección (H2/H3)** | `'Outfit', sans-serif` | `600`–`700` | `1.20rem` (`19.2px`) | `1.25` | Tracking `-0.02em` |
| **Cuerpo de Interfaz (UI Body)** | `'Inter', system-ui, sans-serif` | `400`–`500` | `0.875rem` (`14px`) | `1.50` | Lectura limpia en tablas |
| **Datos Cuantitativos / Tablas** | `'JetBrains Mono', monospace` | `500`–`700` | `0.8125rem` (`13px`) | `1.40` | Obligatorio `tabular-nums` |

---

## 4. Arquitectura de Layout, Espaciado y Shell Datalaria

- **Shell Obligatorio Datalaria (Constitución Art. 5.2):**
  1. Enlace de retorno **`← Datalaria`** integrado a la izquierda del bloque de marca en `.pulse-header`, apuntando a `/es/` o `/en/` según el idioma activo.
  2. Selector bilingüe **`ES` / `EN`** persistido en `localStorage` y sincronizado con `?lang=es|en`.
  3. CTA de conversión contextual **`Descargar Kit (19€) ⚡`** apuntando dinámicamente a `/es/recursos/#pack-pulse` (ES) o `/en/resources/#pack-pulse` (EN) con telemetría GA4 (`begin_checkout_kit`).
- **Higiene del *Above-the-Fold* (`UX-02`):**
  - El botón de refresco HTTP se presenta de forma compacta y el aviso informativo de modo escaparate puede ocultarse con `×` para maximizar el área visible de los Macro KPIs en pantallas de 13"–14".

---

## 5. Estados de Interfaz y Micro-interacciones

| Componente / Vista | Estado Vacío (*Empty State*) | Estado de Carga (*Loading*) | Estado de Error (*Error*) | Estado de Éxito (*Success*) |
| :--- | :--- | :--- | :--- | :--- |
| **Tabla Ejecutiva / Kanban** | Mensaje contextual con botón para limpiar filtros o cargar datos de ejemplo | Icono `RefreshCw` con animación `.spin-animation` | Fallback limpio al snapshot estático local | Actualización reactiva instantánea |
| **Importador CSV Notion** | Zona drag & drop + botón **`⚡ Probar con CSV de ejemplo (1 clic)`** | Lectura `FileReader` en memoria (`<50ms`) | Aviso si el CSV no contiene filas válidas | Tarjeta de Diagnóstico Ejecutivo + CTA al Kit |
| **Auth / Demo Cloud** | Acceso 1 clic a `demo@datalaria.com` o login propio | Botón deshabilitado con estado `Iniciando...` | Mensaje de error acotado en rojo semántico | Píldora `DEMO` / `PRO` activa en cabecera |

---

## 6. Criterios de Verificación Visual (`11-qa-verifier`)

- [x] Cero estilos rotos; compilación limpia con `oxlint` y `vite build`.
- [x] Enlace `← Datalaria` presente y funcional en ES y EN.
- [x] Soporte verificado de `?lang=en|es` y `?demo=true` (en query string y hash `#/?demo=true`).
- [x] Los 3 botones de compra del Kit enlazan a `/es/recursos/#pack-pulse` en español y a `/en/resources/#pack-pulse` en inglés.
