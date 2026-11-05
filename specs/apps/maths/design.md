# Especificación de Diseño UX/UI: Matemáticas Interactivas ("Ábaco Arcade v2.0") (`maths`)

> **ID de Diseño:** `DESIGN-APP-MATHS`  
> **Spec Técnica Vinculada:** [`specs/apps/maths/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/maths/spec.md)  
> **Agente Propietario:** [`04-ux-ui` (Diseñador UX/UI)](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md)  
> **Preset Estético Seleccionado:** `Consumer Playful` (Datalaria Arcade Academy)  
> **Aislamiento de Excepción:** Esta especificación aplica un estilo lúdico e informal adaptado para niños y adultos por instrucción explícita del usuario, sin que afecte ni persista en los estándares de las aplicaciones B2B de Datalaria.

---

## 1. Dirección Estética y Psicología de Usuario

### 1.1 Perfil Visual del Usuario y Contexto de Uso
- **Quién lo usa y dónde:** Niños de infantil y primaria (5 a 11 años) practicando en tablets táctiles o escritorios en casa/colegio, y jóvenes/adultos que buscan un reto lúdico de agilidad mental (entrenamiento de cálculo rápido, porcentajes, combinadas).
- **Sensación en los primeros 3 segundos:** Diversión inmediata, juego arcade moderno y acogedor (estilo *Duolingo / Kahoot!*), cero estrés ni formalismo corporativo rígido, y orgullo visual por los logros y rachas.
- **Preset de Dirección Activo:** `Consumer Playful` vibrante con dos temas cromáticos alternables:
  - **`Daylight Arcade` (Tema Claro por defecto):** Fondo degradado suave lavanda/cielo (`#f0f4ff`), tarjetas blancas flotantes con relieve 3D, sombras coloreadas y acentos vibrantes por operación.
  - **`Cosmic Night` (Tema Oscuro espacial):** Fondo azul noche profundo (`#0b1120`), tarjetas azul medianoche (`#1e293b`), destellos neón y estrellas para jugar cómodamente en entornos con poca luz.

### 1.2 El «Momento Firma» (*Signature Wow Moment*) Dual
> **Manipulador Visual Interactivo («Pista con Bloques/Estrellas») + Numpad Táctil 3D con Audio Sintetizado y Lluvia de Confeti:**  
> - **Para niños:** En cualquier momento (pantalla de aprender o pulsando `💡 Pista Visual`), la app materializa visualmente la operación matemática (agrupaciones de manzanas/estrellas en sumas y restas, matriz $N \times M$ en multiplicaciones, y reparto en cajas con resto resaltado en divisiones).
> - **Para todos:** Teclado numérico táctil 3D integrado en pantalla para responder a la velocidad del rayo en tablets sin que el teclado del sistema tape la interfaz, acompañado de notas musicales sintetizadas nativas (Web Audio API) y lluvia de confeti física al completar una ronda.

---

## 2. Sistema de Design Tokens (Variables CSS Canónicas)

> **Invariante `INV-MATHS-3`:** 100% CSS nativo sin dependencias externas (cero `cdn.tailwindcss.com` ni fuentes de terceros bloqueantes).

### 2.1 Paleta Semántica de Color

```css
:root {
  /* Daylight Arcade (Light Mode) */
  --bg-canvas: #f0f4ff;
  --bg-surface: #ffffff;
  --bg-elevated: #f8faff;
  --bg-inset: #eef2ff;
  --text-primary: #1e1b4b;
  --text-secondary: #475569;
  --text-muted: #64748b;
  --border-card: #e2e8f0;
  --border-strong: #cbd5e1;

  /* Colores Semánticos de Operaciones */
  --op-add: #0ea5e9;
  --op-add-shadow: #0284c7;
  --op-sub: #f59e0b;
  --op-sub-shadow: #d97706;
  --op-mul: #10b981;
  --op-mul-shadow: #059669;
  --op-div: #8b5cf6;
  --op-div-shadow: #7c3aed;
  --op-mixed: #ec4899;
  --op-mixed-shadow: #db2777;

  /* Estados y Feedback */
  --status-success: #10b981;
  --status-error: #f43f5e;
  --status-warning: #f59e0b;
  --accent-combo: #ff007a;

  /* Relieve 3D Arcade */
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
}
```

### 2.2 Tipografía y Ergonomía
- **Títulos y Botones:** `'Outfit', system-ui, -apple-system, sans-serif` (Pesos `700`, `800`, bordes redondeados).
- **Textos y Explicaciones:** `'Inter', system-ui, -apple-system, sans-serif` (Pesos `500`, `600`).
- **Números de Problemas y Numpad:** `'JetBrains Mono', monospace` (`font-variant-numeric: tabular-nums` para alineación limpia).

---

## 3. Arquitectura de Información y Presupuesto *Above-the-Fold*

1. **Shell Visual Datalaria (Lúdico pero Institucional):**
   - Altura de cabecera: adaptativa $\le 60\text{ px}$.
   - Izquierda: Botón `← Datalaria` hacia `/apps/` + Icono `🧮` + Título `Ábaco Arcade` + Badge `v2.0.0`.
   - Derecha: Selector `ES | EN`, Botón de Sonido `🔊 / 🔇`, Conmutador de Tema `☀️ / 🌙`, Enlace a Ficha `📋 Ficha`, Enlace a Post `📖 Historia IA`, y Botón `📦 Kits`.
2. **Pestañas Principales de la Aplicación:**
   - **🎮 Jugar (Arcade):** Configuración de nivel (1 a 6) y modo (Zen, Clásico 10, Contrarreloj 60s) ➔ Tablero de cálculo interactivo con Numpad y Pista Visual.
   - **💡 Aprender (Laboratorio Didáctico):** Explicación animada de las 4 operaciones y manipuladores visuales con ejemplos interactivos.
   - **🏆 Logros & Medallas:** Pasaporte con 6 medallas coleccionables y mejores récords guardados localmente.

---

## 4. Matriz de Estados de Interfaz (Cero Pantallas Muertas)

| Vista / Componente | Estado Vacío (*Empty State*) | Estado Activo / Jugando | Estado de Feedback | Estado Final |
| :--- | :--- | :--- | :--- | :--- |
| **Tablero de Juego** | Selector de nivel y modo listo con botón gigante `¡A Jugar! 🚀` | Expresión grande en pantalla + temporizador/modo + Numpad táctil activo | Notificación emergente animada (`¡Genial! ⭐ +puntos` o `¡Casi! Pista: ...`) | Modal resumen con trofeo, medallas ganadas, estadísticas y botón `Jugar de nuevo 🔁` |
| **Pista Visual** | Oculta para no saturar | Se despliega con animación suave mostrando cajas, manzanas o rejilla de multiplicar | -- | Se oculta automáticamente al pasar al siguiente reto |
| **Logros** | 0 medallas desbloqueadas con silueta en escala de grises y pista de cómo ganarlas | Medallas doradas vibrantes con fecha de desbloqueo y récord personal | -- | -- |

---

## 5. Checklist del Gate de Revisión UX/UI (Pre-QA)

- [x] **Adaptabilidad Multidispositivo:** Probado y optimizado para móvil vertical (`390px`), tablet apaisada/vertical (`768px`) y escritorio (`1440px`).
- [x] **Numpad en Pantalla Ergonómico:** Los botones tienen tamaño táctil $\ge 48\times48\text{ px}$ para evitar pulsaciones erróneas.
- [x] **Accesibilidad WCAG 2.2 AA:** Contraste superior a `4.5:1` en texto y `3:1` en elementos interactivos; soporte de teclado físico completo (`0-9`, `Backspace`, `Enter`, `Tab` para conmutar cociente/resto).
- [x] **Cero CDNs Externos:** Todo el CSS y la tipografía cargan de forma instantánea localmente sin bloqueos de red.
