# Especificación de Diseño UX/UI: Lector Arcade / Reader Arcade (`reading`)

> **ID de Diseño:** `DESIGN-APP-READING`  
> **Spec Técnica Vinculada:** [`specs/apps/reading/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/reading/spec.md)  
> **Versión de Diseño:** `v1.0.0` (Comunalidad directa con `DESIGN-APP-MATHS v2.3`)  
> **Agente Propietario:** [`04-ux-ui` (Diseñador UX/UI)](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md)  
> **Preset Estético Seleccionado:** `Consumer Playful` (Datalaria Arcade Academy)  
> **Aislamiento de Excepción:** Esta especificación aplica un estilo lúdico e informal adaptado a niños y familias internacionales, sin alterar el estándar `Executive Data-Dense` de las apps B2B de Datalaria.

---

## 1. Dirección Estética y Psicología de Usuario

### 1.1 Perfil Visual del Usuario y Contexto de Uso
- **Quién lo usa y dónde:** Niños de 4 a 11 años practicando lectura inicial y fluidez verbal en tablets táctiles, móviles o PC en casa o colegio, acompañados opcionalmente por padres/tutores.
- **Sensación en los primeros 3 segundos:** Entorno acogedor, alegre, táctil y libre de frustración (hermano directo de **Ábaco Arcade** `apps/maths/`), con tipografía amplia de alta legibilidad infantil, tarjetas con relieve 3D y feedback positivo inmediato.
- **Preset de Dirección Activo:** `Consumer Playful` con dos temas cromáticos alternables anti-FOUC (`pref-theme`):
  - **`Daylight Arcade` (Tema Claro por defecto):** Fondo lavanda/cielo suave (`#f0f4ff`), tarjetas blancas con borde limpio y sombras suaves.
  - **`Cosmic Night` (Tema Oscuro):** Fondo azul noche (`#0b1120`), tarjetas `#1e293b` con alto contraste y protección ocular nocturna.

### 1.2 El «Momento Firma» (*Signature Wow Moment*) Dual
> **Mesa de Mezclas Silábica (`💡 Aprender`) + Cronómetro Lector Split con Teclado Táctil 3D y Confeti (`🎮 Jugar`):**  
> - **En Aprender:** Tocar cualquier consonante despliega en vivo sus combinaciones vocálicas (`MA · ME · MI · MO · MU`) codificadas por color, con pronunciación en velocidad normal (`1.0x`) o **Modo Tortuga (`0.65x`)** y cambio instantáneo entre **MAYÚSCULAS (`AA`)** y **minúsculas (`Aa`)**.  
> - **En Jugar:** El cronómetro corre con suavidad mientras el alumno lee o completa las letras faltantes en el teclado táctil 3D, **se congela instantáneamente** al completar la palabra/frase o pulsar **`✅ ¡Leído!`**, calcula sus **Palabras por Minuto (PPM)** y celebra con sonido 8-bit y lluvia de confeti física.

---

## 2. Sistema de Design Tokens (Variables CSS Canónicas)

> **Invariante `INV-READ-3`:** 100% CSS nativo sin dependencias externas ni CDNs (`cdn.tailwindcss.com` o `fonts.googleapis.com` prohibidos).

### 2.1 Paleta Semántica de Color (Heredada de `DESIGN-APP-MATHS` + Tokens Fonéticos)

```css
:root {
  /* Daylight Arcade (Light Mode - Default) */
  --bg-canvas: #f0f4ff;
  --bg-surface: #ffffff;
  --bg-elevated: #f8faff;
  --bg-inset: #eef2ff;
  --text-primary: #1e1b4b;
  --text-secondary: #475569;
  --text-muted: #64748b;
  --border-card: #e2e8f0;
  --border-strong: #cbd5e1;

  /* Acentos Arcade Base (Paridad Maths) */
  --op-add: #0ea5e9;
  --op-add-shadow: #0284c7;
  --op-mul: #10b981;
  --op-mul-shadow: #059669;
  --op-div: #8b5cf6;
  --op-div-shadow: #7c3aed;
  --status-success: #10b981;
  --status-error: #f43f5e;
  --status-warning: #f59e0b;
  --accent-combo: #ff007a;

  /* Tokens Semánticos de Lectura y Sílabas */
  --syl-a: #0284c7;
  --syl-b: #e11d48;
  --syl-complex: #7c3aed;
  --vowel-bg: rgba(16, 185, 129, 0.14);
  --consonant-bg: rgba(14, 165, 233, 0.12);

  /* Relieve 3D y Geometría */
  --btn-3d-shadow: 0 4px 0 var(--border-strong);
  --btn-3d-active: translateY(3px);
  --radius-sm: 8px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-pill: 9999px;
}

[data-theme="dark"] {
  /* Cosmic Night (Dark Mode) */
  --bg-canvas: #0b1120;
  --bg-surface: #1e293b;
  --bg-elevated: #334155;
  --bg-inset: #0f172a;
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --border-card: #334155;
  --border-strong: #475569;
  --syl-a: #38bdf8;
  --syl-b: #fb7185;
  --syl-complex: #a78bfa;
}
```

### 2.2 Tipografía y Ergonomía de Lectura
- **Display y Palabras Protagonistas:** `'Outfit', system-ui, -apple-system, sans-serif` (Pesos `700`, `800`, formas abiertas con clara distinción entre `I`, `l`, `b`, `d`, `p`, `q`).
- **Frases de 2 y 3 Líneas (`--reading-max-width: 44ch`, `--reading-line-height: 1.65`):** `'Inter', system-ui, -apple-system, sans-serif` con espaciado generoso de letras (`letter-spacing: 0.02em`) para evitar apelotonamiento visual (*crowding*) en primeros lectores.
- **Cronómetro, Puntos y PPM:** `'JetBrains Mono', monospace` (`font-variant-numeric: tabular-nums`).
- **Controles Pedagógicos Transversales (Píldoras Compactas):**
  - Toggle de Caja: **`AA MAYÚS`** / **`Aa minús`** (aplica `.case-upper` en palabras y sílabas).
  - Toggle Silábico: **`🎨 Sílabas`** (alterna `--syl-a` y `--syl-b` en los bloques de la palabra).

---

## 3. Arquitectura de Información y Presupuesto *Above-the-Fold*

1. **Shell Visual Datalaria (`height <= 60px` en escritorio):**
   - Izquierda: `← Datalaria` (`/es/apps/` o `/en/apps/`) + Icono `📖` + Título `Lector Arcade / Reader Arcade` + Badge `#btn-check-update` (`v1.0.0`).
   - Derecha: `#btn-install-pwa`, `#sound-btn` (`🔊/🔇`), `#theme-btn` (`☀️/🌙`), `#lang-btn` (`🇪🇸 ES / 🇬🇧 EN`), `#link-spec` (`📋 Ficha App`), `#link-post` (`📖 Post`), `#link-kits` (`📦 Recursos`).
2. **Selector de Perfiles Familiares (`#profile-bar`):**
   - Chips interactivos (`🦁 Lector 1`, `🦊 Lector 2`, `🦉 Tutor/Adulto`) cargando estadísticas aisladas al instante.
3. **Navegación de 3 Pestañas (`#tabs-nav`):**
   - **`🎮 Jugar`** · **`💡 Aprender`** · **`🏆 Logros`**.

### 3.1 Ergonomía Táctil del Tablero de Lectura
- **Teclado Alfabético/Silábico Táctil 3D (`.alpha-pad`):** En Nivel 3 (*Letras Faltantes*), muestra únicamente 8–10 teclas grandes (`.alpha-btn`, tamaño mínimo `52×52 px`) con las letras necesarias y distractores fonéticos, evitando que el teclado nativo de iOS/Android tape la pantalla.
- **Botón Principal de Cierre Lector (`.btn-read-done`):** Botón dominante verde esmeralda de alto contraste (`min-height: 56px`, ancho cómodo `>= 220px`) **`✅ ¡Leído!`** accesible también con `Espacio` o `Enter`.
- **Cronómetro Split en Vivo (`.stopwatch-pill`):** Chip en `tabular-nums` (`⏱️ 00:03.4`) visible en modo `stopwatch` y `daily`; al detenerse cambia brevemente a verde mostrando el tiempo final y **PPM**.

---

## 4. Especificación del Diploma Arcade PNG (`1200×800`)

- Idéntico en estructura ceremonial a `downloadArcadeDiploma()` de `apps/maths/app.js`:
  - Lienzo `<canvas>` 2D `1200×800 px` con fondo marfil pergamino y doble orla dorada.
  - Encabezado: `DATALARIA LECTOR ARCADE • ACADEMIA DE LECTURA` / `DIPLOMA OF HONOR IN READING & FLUENCY`.
  - Bloque de perfil (avatar + nombre + título), 3 tarjetas KPI (**Récord Máximo**, **Récord PPM / WPM**, **Medallas**), fila de 6 medallas, sello circular oficial `DATALARIA VERIFIED` y descarga directa `diploma_lector_arcade_<perfil>_<fecha>.png`.

---

## 5. Matriz de Estados de Interfaz (Cero Pantallas Muertas)

| Vista / Componente | Estado Vacío / Inicial | Estado Activo / Jugando | Estado de Feedback / Micro-Check | Estado Final |
| :--- | :--- | :--- | :--- | :--- |
| **Tablero `Jugar`** | Grid de 6 Niveles + 4 Modos + Botón gigante `¡A Jugar! 🚀` | Palabra/Frase + Toggles `AA/Aa` & `🎨 Sílabas` + Cronómetro + Botón `✅ ¡Leído!` o `.alpha-pad` | Banner animado (`¡Genial! ⭐ +pts · 74 PPM`) o paso breve de **Micro-Check (3 opciones)** con reloj ya congelado | Confeti, puntuación, PPM máxima, tira Wordle (`🟩💡🟥`), Compartir, Repaso de Fallos y Diploma PNG |
| **Pista Visual (`💡`)** | Oculta por defecto (`H`) | Despliega sílabas coloreadas, puntos de palmada (`● ● ●`), primera letra o imagen en `l4` | -- | Se oculta al avanzar a la siguiente ronda |
| **Pestaña `Aprender`** | 4 selectores de bloque con Módulo 1 abierto por defecto | Cuadrícula interactiva de letras, **Mesa de Mezclas `C+V`**, complejas o frases con audio `1.0x`/`0.65x` | Resaltado visual de la ficha pulsada durante la reproducción TTS | -- |
| **Pestaña `Logros`** | 0 medallas en escala de grises con pista de desbloqueo | Medallas doradas desbloqueadas + tarjeta de **Récord PPM** + botón Diploma PNG | Toast flotante al desbloquear medalla o reiniciar stats | -- |

---

## 6. Checklist del Gate de Revisión UX/UI (Pre-QA)

- [ ] **Responsive en 3 Viewports:** Cero desbordamiento horizontal en `390px` (móvil), `768px` (tablet) y `1440px` (escritorio).
- [ ] **Ergonomía Táctil Infantil:** Todas las fichas de letras, sílabas, opciones de micro-check y `.alpha-btn` miden $\ge 48\times48\text{ px}$ (objetivo `52×52 px` en `.alpha-btn`).
- [ ] **Accesibilidad WCAG 2.2 AA:** Contraste mínimo `4.5:1` en textos (`Daylight` y `Cosmic Night`) y `3:1` en controles; soporte de teclado físico (`T`, `M`, `H`, `Espacio`, `Enter`, `A-Z`, `Ñ`, `Backspace`).
- [ ] **Cero CDNs Externos y Cero Glifos Rotos:** Todo CSS e iconos locales; `cover.png` `1200×750` dentro de Safe Zone `[145px, 1055px]`.
- [ ] **Paridad Bilingüe Visual (`ES ⇔ EN`):** Textos en español (~25% más extensos) probados sin romper cabecera ni botones de pestañas.
