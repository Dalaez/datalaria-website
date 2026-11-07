# Especificación de Diseño UX/UI: Neon Snake ("Cyberpunk Overdrive v2.3") (`snake`)

> **ID de Diseño:** `DESIGN-APP-SNAKE`  
> **Spec Técnica Vinculada:** [`specs/apps/snake/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/snake/spec.md)  
> **Versión de Diseño:** `v2.3.0` (Ergonomía Táctil Full-Swipe, Vibración Háptica, Hit-Stop e Inspección de Tablero)  
> **Agente Propietario:** [`04-ux-ui` (Diseñador UX/UI)](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md)  
> **Preset Estético Seleccionado:** `Arcade Cyberpunk Neon` (Datalaria Retro Arcade Deck)  
> **Aislamiento de Excepción (`[SCOPE-ISOLATION: ARCADE-GAME]`):** Esta especificación aplica un estilo estético Cyberpunk de alto contraste, brillos de neón (`box-shadow` / `text-shadow` bloom), tipografía arcade de ciencia ficción, animaciones de glitch/screen-shake y mecánicas de gamificación adictiva concebidas exclusivamente para este videojuego arcade por instrucción explícita del usuario. Estas reglas de diseño y tokens lúdicos **no persisten ni contaminan los estándares de diseño corporativo o herramientas ejecutivas B2B de Datalaria**.

---

## 1. Dirección Estética y Psicología de Usuario

### 1.1 Perfil Visual del Usuario y Contexto de Uso
- **Quién lo usa y dónde:** Jugadores casuales, desarrolladores y visitantes del portal Datalaria buscando una experiencia arcade inmersiva, frenética y estimulante en móvil, tablet o PC.
- **Sensación en los primeros 3 segundos:** Inmersión cibernética instantánea estilo *Tron / Cyberpunk 2077 / Hotline Miami*, ganas inmediatas de pulsar "Iniciar Sistema", sensación de alta tecnología retrofuturista con audio sintetizado 8-bit analógico y cero latencia de carga.
- **Preset de Dirección Activo:** `Arcade Cyberpunk Neon` con dos temas cromáticos alternables:
  - **🌆 `Neon Cyberpunk` (Tema Principal Neón):** Fondo negro azabache (`#05070d`), rejilla cian tenue con pulso reactivo, sombras de neón fucsia (`#ff007a`), cian (`#00f0ff`), amarillo neón (`#ffe600`) y verde matrix (`#00ff66`).
  - **📺 `Retro Phosphor CRT` (Tema Fósforo Verde 1982):** Emulación de monitor CRT monocromo fósforo verde (`#00ff66`) con líneas de escaneo (*scanlines* CSS sutiles), tinte de curvatura arcade y alto contraste nostálgico.

### 1.2 El «Momento Firma» (*Signature Wow Moment*)
> **Combo Overclock + Hyper-Dash Visual + Screen Shake Glitch + Tarjeta Coleccionable PNG:**  
> - **En partida:** Al encadenar capturas antes de que expire la barra de 4s de Combo, el borde del canvas y el HUD entran en modo *Overclock* (`🔥 x2, x3, x5, x8`), las notas del sintetizador Web Audio ascienden en arpegio mayor, y al activar el *Hyper-Dash* (`Espacio` / `Shift` / `⚡ BOOST`), la serpiente proyecta una estela luminosa de alta velocidad ganando doble puntuación.
> - **En Game Over:** Animación sutil de choque (*screen shake* y glitch RGB), guardado asíncrono seguro en el ranking y botón en 1 clic para generar y descargar la **«Cyber-Agent Record Card» en PNG** (1200×630 px) con su skin, nivel, combo récord y sello oficial de verificación de Datalaria.

---

## 2. Sistema de Design Tokens (Variables CSS Canónicas)

> **Invariante `INV-SNAKE-3`:** 100% CSS nativo sin dependencias externas (cero `cdn.tailwindcss.com` ni fuentes web bloqueantes).

### 2.1 Paleta Semántica de Color

```css
:root {
  /* Neon Cyberpunk (Default Theme) */
  --bg-deep: #05070d;
  --bg-surface: #0c101d;
  --bg-card: #12182b;
  --border-neon: #00f0ff;
  --border-dim: #1e293b;
  --text-main: #f0f6fc;
  --text-muted: #94a3b8;

  /* Colores Neón Funcionales */
  --neon-cyan: #00f0ff;
  --neon-pink: #ff007a;
  --neon-yellow: #ffe600;
  --neon-green: #00ff66;
  --neon-red: #ff3344;
  --neon-purple: #a855f7;

  /* Nodos y Power-ups */
  --node-data: #00f0ff;
  --node-golden: #ffe600;
  --node-cryo: #38bdf8;
  --node-ghost: #10b981;

  /* Resplandores y Glows */
  --glow-cyan: 0 0 12px rgba(0, 240, 255, 0.6);
  --glow-pink: 0 0 12px rgba(255, 0, 122, 0.6);
  --glow-yellow: 0 0 12px rgba(255, 230, 0, 0.7);

  /* Botones Arcade 3D */
  --btn-arcade-border: 1px solid var(--neon-cyan);
  --btn-arcade-shadow: 0 4px 0 #0088aa;
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-pill: 9999px;
}

[data-theme="crt"] {
  /* Retro Phosphor CRT Theme */
  --bg-deep: #020b04;
  --bg-surface: #041608;
  --bg-card: #08210e;
  --border-neon: #00ff66;
  --border-dim: #0a3314;
  --text-main: #b8ffcc;
  --text-muted: #52a36b;

  --neon-cyan: #00ff66;
  --neon-pink: #33ff88;
  --neon-yellow: #88ffaa;
  --neon-green: #00ff66;
  --neon-red: #ff4444;
  --neon-purple: #00cc55;

  --glow-cyan: 0 0 10px rgba(0, 255, 102, 0.5);
  --glow-pink: 0 0 10px rgba(0, 255, 102, 0.5);
  --glow-yellow: 0 0 10px rgba(0, 255, 102, 0.5);
}
```

### 2.2 Tipografía y Ergonomía
- **Títulos y Contadores Arcade:** `'Orbitron', 'Courier New', monospace, sans-serif` (peso 700/800, espaciado `letter-spacing: 2px`).
- **Textos y Botones:** `'Inter', system-ui, -apple-system, sans-serif` (peso 500/600).
- **HUD y Puntuaciones:** `'JetBrains Mono', monospace` (`font-variant-numeric: tabular-nums`).

---

## 3. Arquitectura de Información, Presupuesto Above-the-Fold y Modo Inmersivo (`v2.2.0`)

1. **Shell Superior de Datalaria (Visible en Menú, Pausa, Game Over y Pestañas):**
   - Botón `← Datalaria` hacia `/{lang}/apps/` + Icono `🐍` + Título `Neon Snake` + Badge interactivo `#btn-check-update` (`v2.3.0`).
   - Selector de Perfil Familiar (`👾 Hacker 1` / `🤖 Hacker 2` / `⚡ Pro`), selector bilingüe `ES | EN`, botón de audio `🔊 / 🔇`, conmutador de tema `🌆 / 📺`, conmutador `🎮 D-Pad / 👆 Swipe` y botón de instalación inteligente `#btn-install-pwa`.
   - Tríada de enlaces: `📋 Ficha`, `📖 Tutorial`, `📦 Kits`.
2. **Modo Juego Inmersivo Maximizado (`body.is-playing`) y Modo Móvil Full-Swipe:**
   - Al iniciar una partida activa (`!isPaused && !isGameOver`), el `<body>` adquiere la clase `.is-playing`, ocultando automáticamente `#app-header` y `.nav-deck` para entregar el **100% del alto útil de pantalla (`100dvh`)** al tablero y los controles.
   - **Modo Swipe Puro:** Los jugadores móviles pueden desactivar la cruceta virtual mediante `#btn-toggle-dpad`. El panel de controles táctiles oculta el D-Pad (`.touch-controls-deck.dpad-disabled`) dejando únicamente un botón de Hyper-Dash compacto, y `resizeCanvas()` recalcula el lienzo ganando hasta **160 px extra** de altura útil para un tablero gigante.
   - El `.game-hud` incorpora un botón directo **`⏸ Pausa / Menú`** (`#btn-hud-pause`) accesible con 1 clic o pulsando `P` / `Escape`, que pausa la partida y restaura instantáneamente la cabecera completa y las pestañas.
3. **Pausa Dramática (*Hit-Stop* 450 ms) e Inspección de Tablero (`#btn-inspect-board`):**
   - Al chocar, el juego congela el fotograma durante 450 ms con destello estroboscópico en la casilla del impacto y vibración háptica de 80 ms antes de desplegar el modal de Game Over.
   - En `#gameover-overlay`, el botón `#btn-inspect-board` (`👁️ Ver Tablero`) permite atenuar la opacidad del modal al 15% para que el jugador pueda revisar visualmente la jugada y la causa del choque antes de reiniciar.
4. **Cuenta Atrás Animada `3 - 2 - 1 - HACK!` al Reanudar:**
   - Al reanudar desde pausa, se muestra una cuenta atrás superpuesta en el Canvas (`3`, `2`, `1`, `HACK!`) acompañada de pulsos sintetizados 8-bit (`440 Hz` y `880 Hz`), garantizando que el usuario esté preparado antes de que la serpiente vuelva a avanzar.
5. **Pestañas del Juego y Hall of Fame Leaderboard con Ranking Offline Optimista:**
   - **🕹️ Jugar:** Selector de 4 modos 100% bilingüe + Tablero Canvas 60 FPS + D-Pad táctil ergonómico / Swipe + botón `⚡ BOOST`.
   - **🏆 Leaderboard (Cyberpunk Hall of Fame):** Barra superior de KPIs personales (`Mi Récord`, `Combo Máx`, `Estado Red`) seguida de tarjetas `.ranking-row` con medallas diferenciadas para el Podio Top 3 (Oro `#1`, Plata `#2`, Bronce `#3`), indicador `TÚ / YOU` para el jugador activo, badge `⏳ OFFLINE` y borde discontinuo en entradas pendientes de sincronización (`.is-offline-pending`), y tipografía monoespaciada `tabular-nums`.
   - **🎨 Hangar Skins & 🎖️ Medallas:** Tarjetas interactivas con estado equipado/desbloqueado y descarga directa de `🎓 Cyber-Card (PNG)`.

---

## 4. Matriz de Estados de Interfaz (Cero Pantallas Muertas)

| Componente | Estado Vacío / Inactivo | Estado Activo / En Partida | Estado de Feedback | Estado Final (Game Over) |
| :--- | :--- | :--- | :--- | :--- |
| **Tablero Canvas** | Pantalla de inicio con demo animada de fondo | Serpiente en movimiento con rejilla reactiva y partículas | Flash de combo, aviso de firewall ámbar y texto flotante `+pts` | Screen-shake leve, overlay con puntuación, medallas y botones |
| **Ranking** | Indicador de conexión o récords locales en caché | Lista ordenada con badges de posición (#1 oro, #2 plata, #3 bronce) | Indicador `Guardando en la red...` o `⏳ Guardado offline` | Resaltado del agente actual con borde cian brillante y badge `⏳ OFFLINE` si está pendiente |
| **Skins** | Siluetas bloqueadas con candado y objetivo claro | Skin seleccionada con borde de neón y efecto de pulso | Notificación toast: `🔓 ¡Nueva Skin desbloqueada!` | Previsualización renderizada en tarjeta PNG |

---

## 5. Checklist del Gate de Revisión UX/UI (Pre-QA)

- [x] **Adaptabilidad Multidispositivo:** Optimizado para smartphones (`360px`–`420px`), tablets (`768px`) y desktop (`1080p`–`1440p`).
- [x] **Controles Táctiles de Alta Precisión:** Botones D-Pad con área de impacto $\ge 52\times52\text{ px}$ + soporte de gestos táctiles *Swipe* en el Canvas.
- [x] **Accesibilidad WCAG 2.2 AA:** Contraste $\ge 4.5:1$ en todos los textos sobre fondos oscuros, soporte total de teclado (`WASD`, `Flechas`, `Espacio`, `P`, `M`, `T`, `1-4`).
- [x] **Cero CDNs Externos:** Todo el CSS, iconos SVG y sintetizador de audio cargan al 100% de manera local y offline.
