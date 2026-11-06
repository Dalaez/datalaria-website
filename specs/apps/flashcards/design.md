# Especificación de Diseño UX/UI: Flashcards AI ("Mazo Mágico v2.1") (`flashcards`)

> **ID de Diseño:** `DESIGN-APP-FLASHCARDS`  
> **Spec Técnica Vinculada:** [`specs/apps/flashcards/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/flashcards/spec.md)  
> **Versión de Diseño:** `v2.1.0` (PWA Offline, Iconos Maskables, Botón Instalar Multi-Plataforma y Smart Update)  
> **Agente Propietario:** [`04-ux-ui` (Diseñador UX/UI)](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md)  
> **Preset Estético Seleccionado:** `Consumer Playful` (Datalaria Magic Academy Deck)  
> **Aislamiento de Excepción (`[SCOPE-ISOLATION]`):** Esta especificación aplica un estilo lúdico, informal y visualmente estimulante concebido para estudiantes niños (primaria/secundaria) y adultos (idiomas, conceptos técnicos, negocios), por instrucción explícita del usuario, sin que afecte ni persista en los estándares ejecutivos B2B de Datalaria.

---

## 1. Dirección Estética y Psicología de Usuario

### 1.1 Perfil Visual del Usuario y Contexto de Uso
- **Quién lo usa y dónde:**
  - **Niños y Jóvenes (6 a 16 años):** Estudiando vocabulario escolar, ciencias bilingües y geografía en tablets o PC, con necesidad de refuerzo auditivo inmediato, diversión y cero aburrimiento.
  - **Adultos y Profesionales:** Repasando inglés técnico, conceptos de Inteligencia Artificial, finanzas o preparando certificaciones mediante sesiones rápidas de 5 a 10 minutos.
- **Sensación en los primeros 3 segundos:** Motivación instantánea, aspecto de juego de cartas coleccionables mágicas (estilo *Duolingo / Pokémon TCG / Anki moderno*), cero frialdad burocrática y bienvenida interactiva con mazos pre-cargados listos para jugar sin configurar nada.
- **Preset de Dirección Activo:** `Consumer Playful` vibrante con dos temas cromáticos alternables:
  - **☀️ `Sunny Studio` (Tema Claro por defecto):** Fondo degradado suave azul cielo y lavanda (`#f4f7ff`), tarjetas blancas flotantes con relieve táctil 3D, sombras suaves de color, tipografía redondeada y acentos esmeralda/ámbar/violeta según dificultad.
  - **🌙 `Starlight Deck` (Tema Oscuro espacial):** Fondo azul noche profundo (`#0c1222`), tarjetas azul pizarra índigo (`#1e293b`), destellos neón cian/violeta y alto contraste para estudiar en la cama o por la noche sin fatiga visual.

### 1.2 El «Momento Firma» (*Signature Wow Moment*) Dual
> **Giro 3D Táctil + Voz Fonética Bilingüe en Vivo (`🔊 Normal 1.0x` / `🐢 Modo Tortuga 0.75x`) + 6 Mazos Curados en 1 Clic:**  
> - **Para niños y estudiantes de idiomas:** Al girar la tarjeta con una animación tridimensional ultrafluida (`transform: rotateY(180deg)`), un sintetizador fonético nativo pronuncia la palabra en el idioma exacto (`es`, `en`, `fr`, `de`, etc.), con opción de velocidad reducida (`🐢 0.75x`) para apreciar la pronunciación sílaba a sílaba y transcripción fonética visual simplificada.
> - **Para todos los públicos:** Cero pantallas vacías. Nada más entrar, el usuario puede pulsar sobre 6 mazos icónicos pre-cargados (Ciencias del Cuerpo Humano, Exploradores del Espacio, Capitales del Mundo, Business English, Conceptos de IA y Estrategia MBA) o importar/crear los suyos en segundos.

---

## 2. Sistema de Design Tokens (Variables CSS Canónicas)

> **Invariante `INV-FLASH-3`:** 100% CSS nativo sin dependencias externas (cero `cdn.tailwindcss.com`, cero fuentes de terceros bloqueantes y cero GIFs externos de Giphy).

### 2.1 Paleta Semántica de Color

```css
:root {
  /* Sunny Studio (Light Mode) */
  --bg-canvas: #f4f7ff;
  --bg-surface: #ffffff;
  --bg-elevated: #f8faff;
  --bg-inset: #eef2ff;
  --text-primary: #1e1b4b;
  --text-secondary: #475569;
  --text-muted: #64748b;
  --border-card: #e2e8f0;
  --border-strong: #cbd5e1;

  /* Colores de Cajas Leitner y Estados */
  --box-repeat: #f59e0b;      /* Repetir / Aprendiendo (Ámbar) */
  --box-repeat-bg: #fffbeb;
  --box-good: #0ea5e9;        /* Bien / Consolidando (Cielo) */
  --box-good-bg: #f0f9ff;
  --box-mastered: #10b981;    /* Dominada (Esmeralda) */
  --box-mastered-bg: #ecfdf5;
  --status-error: #ef4444;

  /* Acentos Mágicos & Gamificación */
  --magic-accent: #8b5cf6;
  --magic-gradient: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
  --gold-medal: #f59e0b;

  /* Banner de Actualización y Toasts */
  --banner-bg: #1e1b4b;
  --banner-text: #ffffff;
  --banner-accent: #38bdf8;

  /* Relieve 3D Arcade */
  --btn-3d-shadow: 0 4px 0 var(--border-strong);
  --btn-3d-active: translateY(3px);
  --radius-sm: 8px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-pill: 9999px;
}

[data-theme="dark"] {
  /* Starlight Deck (Dark Mode) */
  --bg-canvas: #0c1222;
  --bg-surface: #1e293b;
  --bg-elevated: #334155;
  --bg-inset: #0f172a;
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --border-card: #334155;
  --border-strong: #475569;

  --box-repeat-bg: rgba(245, 158, 11, 0.15);
  --box-good-bg: rgba(14, 165, 233, 0.15);
  --box-mastered-bg: rgba(16, 185, 129, 0.15);
}
```

---

## 3. Componentes de Actualización In-App y PWA Multi-Plataforma

### 3.1 Botón de Versión Interactivo (`#btn-check-update`)
- Ubicado en la cabecera junto a la marca: badge redondeado interactivo (`v2.1.0`).
- Al hacer clic, lanza un Toast no invasivo: `🔍 Buscando actualizaciones...` y comprueba el Service Worker en caliente.
- Si no hay cambios: `✅ Tienes la versión más reciente (v2.1.0)`.
- Si hay un nuevo Service Worker esperando: despliega el `#pwa-update-banner`.

### 3.2 Banner de Actualización In-App (`#pwa-update-banner`)
- Ubicación: Barra flotante fija en la parte inferior de la ventana (`z-index: 9999`).
- Contenido:
  - Texto: `⚡ Nueva versión disponible de Flashcards AI`.
  - Botón de Acción: `🔄 Actualizar ahora`.
- Comportamiento: Al pulsar `🔄 Actualizar ahora`, envía `{ action: 'skipWaiting' }` al Service Worker y, ante el evento `controllerchange`, recarga automáticamente la página de forma limpia.

### 3.3 Botón de Instalación PWA Multi-Plataforma (`#btn-install-pwa`)
- Ubicado en la cabecera: botón con acento destacado `📲 Instalar`.
- Estado `standalone`: Se oculta automáticamente si la aplicación ya está instalada o ejecutándose en modo ventana completa.
- Android y Chromium (Edge, Chrome): Captura el evento `beforeinstallprompt` y abre el diálogo nativo del sistema operativo.
- iOS / iPadOS Safari: Detecta el navegador móvil de Apple y muestra un Toast explicativo guiado con el icono oficial de compartir:
  > *«📲 En iPhone / iPad: pulsa el botón Compartir (cuadrado con flecha ↑) y luego "Añadir a pantalla de inicio".»*

### 3.4 Sistema de Toasts Lúdicos (`#toast-container`)
- Contenedor flotante superior centrado para alertas discretas y no bloqueantes.
- Utilizado para:
  - Notificaciones de instalación PWA.
  - Comprobación de actualizaciones.
  - Desbloqueo de medallas.
  - Copiado de enlaces o plantillas CSV.

---

## 4. Checklist del Gate de Revisión UX/UI (Pre-QA)

- [x] **Adaptabilidad Multidispositivo:** Probado en pantallas móviles (390px), tablets (768px) y desktop (1440px).
- [x] **Relieve Táctil Ergonómico:** Botones de acción con área de impacto $\ge 48\times48\text{ px}$.
- [x] **Accesibilidad WCAG 2.2 AA:** Contraste $\ge 4.5:1$ en textos, soporte de navegación completa por teclado (`Espacio`, `Enter`, `1`, `2`, `3`, `V`, `T`, `M`).
- [x] **Cero CDNs Externos:** Todo el CSS, SVGs y fuentes cargan de forma instantánea localmente sin bloqueos de red ni rastreo externo de terceros.
- [x] **Iconos Maskable:** Iconos PNG generados con margen seguro de 10% para corte circular o cuadrado en launchers Android.
