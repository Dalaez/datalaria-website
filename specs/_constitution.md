# Constitución Arquitectónica SDD de Datalaria (`_constitution.md`)

> **Versión:** 1.0.0  
> **Estado:** ACTIVA Y VINCULANTE  
> **Propósito:** Definir las reglas innegociables de ingeniería, seguridad, datos y negocio que gobiernan todas las aplicaciones y componentes de la plataforma **Datalaria**. Ninguna especificación particular (`spec.md`) ni implementación puede contradecir esta Constitución.

---

## Artículo 1: Primacía de la Especificación (Spec-First Invariant)
1. **Ningún código sin Spec:** Ninguna aplicación nueva o refactorización estructural puede escribirse sin que exista previamente su archivo `/specs/apps/<app-slug>/spec.md` validado.
2. **Agnosticismo del Modelo:** Las especificaciones se redactan en Markdown estándar enriquecido con diagramas Mermaid, esquemas SQL declarativos y contratos JSON Schema / OpenAPI / Pydantic. No deben depender de plugins propietarios de un único proveedor de IA.
3. **Separación de "El Cerebro" y "El Músculo":**
   - **El Músculo (Determinista):** Todo cálculo matemático, financiero o estadístico (EVM, PERT, Monte Carlo, Forecasting Prophet, Optimización Lineal PuLP, recorrido de árboles BOM) DEBE ejecutarse en código determinista (Python/NumPy/Pandas o motor JS tipado) cubierto por tests unitarios.
   - **El Cerebro (Agéntico/LLM):** Los agentes de IA (Gemini / CrewAI) se utilizan para extracción semántica, interpretación ejecutiva de resultados ya calculados y orquestación de herramientas, **nunca para inventar o aproximar aritmética financiera**.

---

## Artículo 2: Higiene Estricta entre Código Fuente y Assets Estáticos (`static/` Firewall)
1. **Prohibición de Código Backend en `static/`:** El directorio `/static/` de Hugo se publica íntegramente en Internet. Está **estrictamente prohibido** almacenar dentro de `/static/` archivos `.py`, `.sql`, `.env`, `.ipynb`, `requirements.txt`, configuraciones de servidores o metadatos `.git`.
2. **Ubicación del Código Fuente:**
   - Todo código fuente de aplicaciones vive en `/apps/<app-slug>/`.
   - Toda herramienta interna de automatización o generación de paquetes vive en `/ops/` (o `/scripts/` y `/autopilot/` durante la transición).
   - `/static/apps/<app-slug>/` solo puede contener artefactos frontend compilados (`index.html`, bundles `.js`/`.css` minificados y datasets públicos de demostración).

---

## Artículo 3: Arquitectura de Producto y Monetización "Dual-Mode" (Sandbox + Pro)
Toda aplicación B2B o ejecutiva publicada en el catálogo de Datalaria debe cumplir el **Patrón Dual-Mode**:

1. **Prohibición de Pantallas "OFFLINE" en Producción:** Ninguna aplicación servida en `datalaria.com/apps/*` puede depender exclusivamente de `http://localhost` ni mostrar errores de conexión cuando el backend cloud esté en reposo o el usuario no esté autenticado.
2. **Modo 1 — Executive Sandbox (Gratis / Instantáneo / 24x7):**
   - Funciona de inmediato al abrir la URL sin requerir registro.
   - Carga un escenario ejecutivo realista pre-computado o ejecuta una simulación determinista en el navegador (`mock=true` / dataset sintético).
   - Incluye el **Componente de Upsell Contextual**: un enlace directo y trazado con GA4 hacia el *Executive Decision Pack* o *Suite* correspondiente en **Lemon Squeezy**.
3. **Modo 2 — Live Engine / Pro (Autenticado o Con Licencia):**
   - Se activa cuando el usuario inicia sesión con Supabase Auth o introduce una licencia válida.
   - Conecta con el backend FastAPI para procesar archivos propios del usuario (`.xlsx`, `.csv`), persistir datos en Supabase y disparar agentes de IA o generación de informes (`.docx`, `.xlsx`).

---

## Artículo 4: Unificación de Datos Multi-Esquema (`datalaria-core`)
1. **Un Único Proyecto Supabase:** Se prohíbe crear nuevos proyectos de Supabase aislados por aplicación. Toda la plataforma converge hacia el cluster principal **`datalaria-core`**.
2. **Aislamiento por Esquemas PostgreSQL (`schemas`):**
   - Cada aplicación opera exclusivamente dentro de su propio esquema dedicado:
     - `lifeops` → App LifeOps.
     - `pmo_analytics` → App Agentic PMO Sandbox (`project-ops`).
     - `sop_engine` → App S&OP Autonomous Pipeline (`sop-pipeline`).
     - `obs_radar` → App Radar de Obsolescencia (`obs-management`).
     - `arcade` → Tablas públicas acotadas de gamificación (ej. `snake_scores`).
3. **Seguridad Row-Level Security (RLS) y Secretos:**
   - Toda tabla en esquemas de usuario debe tener **RLS activado** filtrando por `auth.uid() = user_id`.
   - Ninguna credencial (`SUPABASE_KEY`, `GEMINI_API_KEY`, `ALGOLIA_API_KEY`, `BREVO_API_KEY`) puede escribirse como literal en el código fuente; siempre deben inyectarse por variables de entorno (`.env` ignorado por Git) con validación de arranque (fail-fast).

---

## Artículo 5: Coherencia de Marca, Internacionalización (i18n) y Telemetría
1. **Bilingüismo Nativo (ES / EN) sin Duplicar Código:**
   - Se prohíbe el antipatrón legacy de duplicar archivos `.html` enteros en carpetas `/es/` y `/en/` para nuevas aplicaciones o migraciones.
   - Toda app migrada a SDD debe tener **una única base de código** con diccionarios de traducción estructurados (`es.json` / `en.json` o módulo `i18n`) que detecte el idioma por parámetro URL (`?lang=es|en`), `localStorage` o ruta del portal.
2. **Shell Visual Datalaria:** Toda aplicación debe presentar una navegación clara para volver al portal (`datalaria.com`), soporte de modo oscuro ejecutivo y tipografía limpia.
3. **Telemetría de Conversión:** Los eventos clave de interacción con CTAs de productos deben emitir eventos compatibles con el tracker de GA4 y Lemon Squeezy definido en el portal.

---

## Artículo 6: Calidad, Tipado y Verificación Automatizada
Para que un módulo se considere conforme a SDD, debe contar con verificación ejecutable por línea de comandos:
1. **Backends y Motores Python:**
   - Contratos de entrada/salida tipados estrictamente con **Pydantic v2**.
   - Linting y formateo con `ruff` (o equivalente limpio sin errores de sintaxis).
   - Suite de pruebas **`pytest`** que valide las invariantes matemáticas del motor (ej. fórmulas CPI/SPI, restricciones de capacidad, recorrido de grafos) sin requerir llamadas reales de pago a LLMs.
2. **Frontends Modernos (React / Vite):**
   - Linting estático ultrarrápido con **`oxlint`** (`npm run lint`).
   - Compilación de producción limpia con **`vite build`** (`npm run build`) sin errores ni advertencias de enlaces rotos.

---

## Artículo 7: Política de Contención Legacy y Regla de Publicación Editorial
1. **Invariante de Publicación Editorial (`App Activa ⇔ Post Publicado`):**
   - Ninguna aplicación debe figurar públicamente en el catálogo `/es/apps/` o `/en/apps/` si no cuenta con al menos un artículo técnico publicado (`draft: false`) que la respalde y documente su caso de uso.
   - Los motores o aplicaciones cuyos artículos estén en borrador (`draft: true`, como `project-ops`) o que aún no se hayan lanzado como Web App (`sop-pipeline`) permanecen en estado **Incubación Privada** dentro de `/apps/` (nunca expuestos en `/static/apps/`), hasta que sean revisados, validados bajo SDD y publicados junto con sus artículos.
   - Toda tarjeta de aplicación en `/es/apps/` y `/en/apps/` debe incluir, además del botón para abrir la App, el enlace directo a su artículo o serie de artículos de referencia (*"Leer Post" / "Read Post"*).
2. **Contención de Apps Experimentales ("Frozen Legacy"):**
   - Las 4 aplicaciones experimentales activas (`conversor`, `maths`, `flashcards`, `snake`) quedan en estado **Frozen Legacy**:
     - No se invertirá tiempo de ingeniería ni tokens de IA en reescribirlas en frameworks modernos ni en crearles suites de tests complejas.
     - Sus URLs públicas actuales se mantienen 100% operativas para conservar los enlaces de los artículos publicados que las referencian.
     - En el catálogo visual de `/es/apps/` y `/en/apps/`, se agruparán en una sección secundaria claramente diferenciada de las **Suites Ejecutivas B2B**.

---

## Artículo 8: Ficha Pública, Versionado y Trazabilidad de cada App
1. **Ficha obligatoria:** Toda App listada en `/apps/` (activa, legacy o nueva) tiene una ficha pública bilingüe en `/es/apps/<slug>/` y `/en/apps/<slug>/`, renderizada según [`specs/portal/apps-showcase/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/portal/apps-showcase/spec.md).
2. **Fuente única de metadatos:** Los metadatos públicos de una App (objetivos, diseño, tecnologías, posts, versiones) viven exclusivamente en `data/apps/<slug>.yaml`. Está prohibido duplicarlos a mano en HTML o Markdown.
3. **Versionado SemVer y Changelog:** Toda release de una App incrementa su versión (`MAJOR.MINOR.PATCH`) y añade una entrada en `releases` de su `data/apps/<slug>.yaml` **y** en la sección "Historial Evolutivo" de su `spec.md`, en el mismo commit que el cambio de código.
4. **Enlace bidireccional Post ⇔ Ficha:** Los posts de referencia de una App incluyen el shortcode `app-ref` hacia su ficha, y la ficha lista esos posts. El build de Hugo falla si un post referenciado no existe o no está publicado.
