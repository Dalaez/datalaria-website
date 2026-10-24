# 00 — Auditoría de Ecosistema y Plan de Modernización SDD (Datalaria)

> **Fecha de Auditoría:** 2026-10-20  
> **Rol:** Principal Software Architect (Spec-Driven Development & Modular Modernization)  
> **Estado del Código de Producción:** INTACTO (Auditoría 100% Estática / Modo Lectura)  
> **Objetivo:** Transformar el repositorio híbrido de Datalaria en una arquitectura modular gobernada por especificaciones formales (`spec.md`), agnóstica del modelo (Google Antigravity / Gemini 4 Argon y agentes Claude) y orientada a la monetización B2B/SaaS.

---

## 1. INVENTARIO Y MAPA DEL ECOSISTEMA

El repositorio actual (`datalaria`) ha evolucionado orgánicamente desde un generador de sitios estáticos en **Hugo** hasta convertirse en un "monorepo accidental" que mezcla contenido editorial, productos digitales B2B (Executive Decision Packs), aplicaciones web interactivas, sandboxes de ingeniería de operaciones y automatizaciones agénticas.

### 1.1 Mapa Visual de la Topología Actual

```mermaid
flowchart TB
    subgraph Portal["Portal Base (Hugo + PaperMod + Netlify)"]
        Hugo["Hugo SSG\n(config.yaml, layouts/, content/)"]
        Edge["Netlify Functions\n(subscribe.js, agent-chat.js)"]
        Catalog["Catálogo B2B / LemonSqueezy\n(recursos_catalog.html)"]
        Redirects["Enrutador Estático\n(static/_redirects, netlify.toml)"]
    end

    subgraph Tier1["Tier 1: Flagship SaaS (Full-Stack Desacoplado)"]
        LifeOpsFE["LifeOps Frontend\n(lifeops-app/ -> copy to static/apps/lifeops/)"]
        LifeOpsBE["LifeOps API\n(lifeops-api/ FastAPI @ Render)"]
    end

    subgraph Tier2["Tier 2: Motores Cuantitativos & Agénticos B2B (Python)"]
        PMO["Agentic PMO Sandbox\n(static/apps/project-ops/)"]
        SOP["S&OP Autonomous Pipeline\n(static/apps/sop-pipeline/)"]
        OBS["Agentic Obsolescence Radar\n(static/apps/obs-management/)"]
    end

    subgraph Tier3["Tier 3: Apps Interactivas & Lead Magnets (HTML/JS)"]
        Weather["Dashboard Climático IA\n(static/apps/weather/ + 2 clones)"]
        Flashcards["Flashcards IA\n(static/apps/flashcards/)"]
        Snake["Neon Snake Cyberpunk\n(static/games/snake/)"]
    end

    subgraph Tier4["Tier 4: Micro-Utilidades Estáticas"]
        Conversor["Conversor Universal Pro\n(static/apps/conversor/)"]
        Maths["Juego de Matemáticas\n(static/apps/maths/)"]
    end

    subgraph Internal["Herramientas Internas & Automatización"]
        Autopilot["Datalaria Autopilot & Ctrl\n(autopilot/, .github/workflows/)"]
        PackBuilders["Generadores Executive Packs\n(scripts/, packages/)"]
    end

    subgraph Cloud["Infraestructura Externa & Datos"]
        Supa1[("Supabase: wkbmxekmofrjtcsyytrv\n(schema: lifeops)")]
        Supa2[("Supabase: wxwnbzmbzztegcdzrxbg\n(public.snake_scores)")]
        Supa3[("Supabase: Env Vars (.env)\n(pmo_analytics, supply_plans, bom_lines)")]
        ExtNet["Netlify Externo\n(datalaria-app-weather.netlify.app)"]
    end

    Hugo --> Redirects
    LifeOpsFE -.->|"Build manual copiado a"| Hugo
    LifeOpsFE -->|"JWT + REST"| LifeOpsBE
    LifeOpsBE --> Supa1
    Snake -->|"Anon Key Hardcodeada"| Supa2
    PMO --> Supa3
    SOP --> Supa3
    OBS --> Supa3
    Redirects -->|"Proxy 200!"| ExtNet
```

---

### 1.2 Inventario Completo de Componentes y Aplicaciones (Cruce con Posts Publicados)

> **Premisa de Publicación Verificada:** Cada aplicación activa en el escaparate de Datalaria (`/es/apps/` y `/en/apps/`) está respaldada por un artículo o serie de artículos con `draft: false`. Las aplicaciones cuyos artículos siguen en borrador (`draft: true`) o que solo servían como código de apoyo (Google Colab) pertenecen al **Backlog de Incubación (No Publicadas)** y no deben migrarse ni exponerse en el catálogo hasta completar las 7 apps activas.

#### A. Las 7 Aplicaciones Activas en Producción (Escaparate `/apps/` + Post Publicado)

| ID | Nombre en Web | Ubicación en Repositorio | Ruta Pública | Post(s) de Respaldo (`draft: false`) | Stack Tecnológico |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **APP-01** | **LifeOps** | [lifeops-app/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/lifeops-app), [lifeops-api/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/lifeops-api), [static/apps/lifeops/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/static/apps/lifeops) | `/apps/lifeops/` | Serie de 5 posts: `app-lifeops_part1` a `part5` (Sept 2026) | **FE:** React 19.2, Vite 8.2, React Router 7, Recharts, Oxlint.<br>**BE:** FastAPI 0.115, Pydantic v2, SlowAPI, DOCX/XLSX, Supabase (`lifeops`). |
| **APP-02** | **Agentic Radar / Radar de Obsolescencia** | [static/apps/obs-management/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/static/apps/obs-management) | `/apps/obs-management/` | Serie de 7 posts: `obs_parte1_intro` a `obs_parte7_dashboard` (Abr-May 2026) | **FE:** HTML5 + Tailwind CDN.<br>**BE:** FastAPI (`main.py`, `dashboard_api.py`), CrewAI, Gemini 2.5 Flash, Supabase. |
| **APP-03** | **Neon Snake** | [static/games/snake/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/static/games/snake) | `/games/snake/` (`es` y `en`) | `game_snake` (Feb 2026) | HTML5 Canvas, Web Audio API (sintetizador retro), Tailwind CDN, Supabase Realtime (`snake_scores`). |
| **APP-04** | **Weather / El Tiempo** | [static/apps/weather/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/static/apps/weather), [temp_app_weather/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/temp_app_weather), [github.io/app-openweather/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/github.io/app-openweather) | `/apps/weather/` (Proxy `200!` a Netlify externo) | Serie de 4 posts: `app-openweather_part1` a `part4` (Oct-Dic 2025) | **FE:** HTML5 monolítico (1.864 líneas), Chart.js, Leaflet, PapaParse.<br>**BE/Batch:** Python (`read_weather.py`), Scikit-Learn, GitHub Actions cron. |
| **APP-05** | **Flashcards** | [static/apps/flashcards/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/static/apps/flashcards) | `/apps/flashcards/` (`es` y `en`) | `app_flashcards` (Oct 2025) | HTML5, Vanilla JS, Tailwind CDN, Google Gemini REST API directa (BYOK). |
| **APP-06** | **Unit Converter / Conversor de Unidades** | [static/apps/conversor/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/static/apps/conversor) | `/apps/conversor/` (`es` y `en`) | `app_conversor_unidades` / `app_unit_converter` (Oct 2025) | HTML5 multipágina (14 archivos `.html`), Vanilla JS, Tailwind CDN. |
| **APP-07** | **Maths / Matemáticas** | [static/apps/maths/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/static/apps/maths) | `/apps/maths/` (`es` y `en`) | `founderz-programando-chatGPT` (Ago 2025) | HTML5, Vanilla JS, Tailwind CDN. |

#### B. Motores en Incubación / No Publicados como Web App (Posponer hasta Fase 4)

| ID | Nombre / Componente | Ubicación Actual | Estado Editorial | Diagnóstico y Acción |
| :--- | :--- | :--- | :--- | :--- |
| **INC-01** | **Agentic PMO Sandbox (`project-ops`)** | [static/apps/project-ops/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/static/apps/project-ops) | **NO PUBLICADO.** Sus artículos `proj_ops_parte1_intro` y `proj_ops_parte2_agentic_pmo` tienen **`draft: true`** y la Parte 3 aún no existe. | **Posponer migración funcional.** Solo debemos sacar sus archivos `.py`/`.env` de `static/` por seguridad, y dejar su validación, revisión y primer lanzamiento oficial para cuando terminemos con las 7 apps activas. |
| **INC-02** | **S&OP Autonomous Pipeline (`sop-pipeline`)** | [static/apps/sop-pipeline/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/static/apps/sop-pipeline) | Serie `sop-ingenieria` publicada (`draft: false`), pero su Parte 5 enlaza a un **Google Colab externo**, no a una Web App en `/apps/`. | **Posponer migración a Web App.** Sacar los scripts `.py`/`.env` de `static/` por higiene y dejar la creación de su Web App SDD para la fase de nuevas publicaciones. |

#### C. Infraestructura del Portal y Automatización Interna

| ID | Nombre / Componente | Ubicación en Repositorio | Ruta Pública (URL) | Stack Tecnológico |
| :--- | :--- | :--- | :--- | :--- |
| **CORE** | **Portal Editorial & Catálogo B2B** | [config.yaml](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/config.yaml), [layouts/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/layouts), [content/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/content) | `/es/`, `/en/`, `/es/recursos/`, `/es/apps/` | Hugo SSG, Go Templates, PaperMod, Lemon Squeezy Checkout Overlay + GA4 Telemetry. |
| **EDGE** | **Portal Serverless Functions** | [netlify/functions/agent-chat.js](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/netlify/functions/agent-chat.js), [subscribe.js](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/netlify/functions/subscribe.js) | `/.netlify/functions/*` | Node.js (Proxy Algolia Agent Studio + Suscripción Brevo). |
| **OPS** | **Autopilot & Suite Pack Builders** | [autopilot/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/autopilot), [scripts/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/scripts), [packages/](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/packages) | *Interno (CI/CD & Build)* | Python, CrewAI, OpenPyXL, ReportLab, Python-PPTX, Algolia Sync. |

---

## 2. AUDITORÍA DE DEUDA TÉCNICA, SEGURIDAD Y ACOPLAMIENTO

### 2.1 Hallazgos Críticos de Seguridad e Higiene de Repositorio (Blocker Risk)

> [!CAUTION]
> **Riesgo de Exposición de Código Backend y Secretos en `/static/`:**
> En Hugo, **todo archivo ubicado dentro del directorio `static/` se copia literalmente a la raíz de `public/` durante el build** (`hugo`) y se despliega en el CDN de Netlify, a menos que esté explícitamente excluido en `.gitignore` y no exista en el árbol de Git del servidor de build.
> Actualmente residen en `static/apps/` tres proyectos backend en Python completos:
> - `static/apps/obs-management/.env`, `main.py`, `supabase_schema.sql`, `supabase_tools.py`
> - `static/apps/project-ops/.env`, `main.py`, `db_tools.py`, `evm_engine.py`
> - `static/apps/sop-pipeline/.env`, `agent_brain.py`, `db_tools.py`, `optimization_engine_v2.py`
>
> Aunque `.gitignore` ignora `.env` en la raíz, si Netlify o un despliegue manual empaqueta `static/`, el código fuente de tus motores cuantitativos y esquemas SQL queda expuesto públicamente bajo `https://datalaria.com/apps/project-ops/main.py` o `https://datalaria.com/apps/obs-management/supabase_schema.sql`.

1. **Fragmentación de Instancias de Supabase y Claves Hardcodeadas:**
   - [lifeops-app/src/lib/supabase.js](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/lifeops-app/src/lib/supabase.js#L3) apunta como fallback a `https://wkbmxekmofrjtcsyytrv.supabase.co`.
   - [static/games/snake/es/index.html](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/static/games/snake/es/index.html#L199-L200) apunta a una instancia distinta (`https://wxwnbzmbzztegcdzrxbg.supabase.co`) con una clave pública hardcodeada en el HTML (`sb_publishable_hAEvRnntjRnk11ps4n1yVw__PwZYoSy`).
   - [netlify/functions/agent-chat.js](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/netlify/functions/agent-chat.js#L8-L10) tiene hardcodeados como fallback el `ALGOLIA_APP_ID`, `ALGOLIA_SEARCH_KEY` y `ALGOLIA_AGENT_ID`.
2. **Triplicación y Corrupción Git en `weather`:**
   - La app del clima existe simultáneamente en tres rutas del workspace: `static/apps/weather/`, `temp_app_weather/` y `github.io/app-openweather/app_weather/`.
   - Además, `static/apps/weather/` contiene los archivos internos de un repositorio Git bare/desempaquetado (`HEAD`, `config`, `objects/pack/*`, `refs/`, `logs/`) mezclados con los archivos de la aplicación.
3. **Doble Build Manual en `lifeops-app`:**
   - El código fuente vive en `lifeops-app/`, se compila en `lifeops-app/dist/` y luego se copia manualmente a `static/apps/lifeops/` (ambos directorios contienen exactamente los mismos hashes de bundle JS/CSS como `index-BZYsjzT8.js`).
4. **Proliferación de Versiones Muertas (`_v2`, `_OLD_DEPRECATED`, `scratch/`):**
   - En `static/apps/sop-pipeline/` coexisten todos los módulos por duplicado (`data_hygiene.py` y `data_hygiene_v2.py`, `forecast_manager.py` y `forecast_manager_v2.py`, `optimization_engine.py` y `optimization_engine_v2.py`).
   - En `autopilot/` existen `main_OLD_DEPRECATED.py`, `agents_OLD_DEPRECATED.py`, `tasks_OLD_DEPRECATED.py`.
   - En la raíz del proyecto hay 6 archivos `mockup_*.html`, 3 archivos `extracted*.txt` de ~140KB y scripts sueltos (`copy_images.py`, `extract.py`, `test_chars.pdf`).

---

### 2.2 Evaluación Detallada por Aplicación

#### 1. **LifeOps (`lifeops-app` + `lifeops-api`)**
- **Acoplamiento con el Portal:** **Bajo/Medio.** No comparte estado ni estilos con Hugo (usa su propio sistema de tokens CSS Glassmorphism y autenticación propia con Supabase Auth + JWT). Su único acoplamiento es el artefacto compilado depositado en `static/apps/lifeops/` y su enlace en el catálogo. Dispone de un "Modo Demo/Mock" (`?mock=true`) excelente para visitantes del blog sin cuenta.
- **Cobertura de Tests y Verificación Automatizada:** **Baja (0% tests unitarios/E2E), Media en Linting/Tipado.** `lifeops-app` cuenta con `oxlint` configurado ([.oxlintrc.json](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/lifeops-app/.oxlintrc.json)), pero está escrito en `.jsx`/`.js` sin TypeScript (`tsconfig.json` ausente). `lifeops-api` usa validación estricta con Pydantic v2, pero carece de suite `pytest`.
- **Dependencias:** Modernas en general (`react@^19.2.8`, `vite@^8.2.0`, `fastapi==0.115.12`), pero `lifeops-api` utiliza `python-jose[cryptography]==3.4.0` (librería sin mantenimiento activo y con vulnerabilidades conocidas frente a `PyJWT`). Además, `main.py` incluye un monkey-patch global de `socket.getaddrinfo` para forzar IPv4 en Windows.
- **Valor de Negocio (Datalaria):** **Alto (B2C Prosumer / Portfolio Flagship).** Demuestra capacidad de ingeniería Full-Stack real en producción (series de 5 posts técnicos), aunque su temática es más "Productividad Personal/Profesional" que el core C-Level industrial de Datalaria. Potencial como SaaS freemium o plantilla integrable.

#### 2. **Agentic PMO Sandbox (`project-ops`)**
- **Acoplamiento con el Portal:** **Nulo en runtime, Crítico en ubicación física.** Vive erróneamente dentro de `static/apps/project-ops/`, pero es un backend puro en FastAPI (`port 8001`). No tiene interfaz web conectada en el portal (la Fase 4a con Streamlit está declarada en `requirements.txt` pero aún no implementada).
- **Cobertura de Tests y Verificación Automatizada:** **Media.** Es la única app que ya posee una especificación técnica formal ejemplar ([TECH_SPEC.md](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/static/apps/project-ops/TECH_SPEC.md)) y contratos estrictos en Pydantic v2 ([models.py](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/static/apps/project-ops/models.py)). Le falta suite `pytest` automatizada que verifique las invariantes matemáticas de `evm_engine.py`.
- **Dependencias:** Limpias (`fastapi`, `pandas`, `numpy`, `openpyxl`, `pydantic>=2.0.0`, `supabase>=2.0.0`), pero con rangos abiertos (`>=`) en lugar de versiones fijadas con lockfile.
- **Valor de Negocio (Datalaria):** **Muy Alto (Core B2B / Upsell Directo).** Conecta directamente con la **Suite 03: Control Operativo (PERT y Cuadro EVM)** que vendes en Lemon Squeezy. Es el puente perfecto entre tus plantillas Excel de pago y un SaaS B2B o servicio de consultoría ejecutiva.

#### 3. **S&OP Autonomous Pipeline (`sop-pipeline`)**
- **Acoplamiento con el Portal:** **Nulo en runtime, Crítico en ubicación física.** Alojado en `static/apps/sop-pipeline/`. Ni siquiera aparece listado en `/es/apps/_index.md`, sino que sirve como código de respaldo de la serie de posts sobre S&OP e IA Agéntica.
- **Cobertura de Tests y Verificación Automatizada:** **Muy Baja.** Contiene 3 scripts sueltos (`test_gemini.py`, `test_genai.py`, `test_models.py`) que son pruebas de humo manuales contra la API de Gemini, no tests unitarios de los motores matemáticos (`forecasting_engine_v2.py` y `optimization_engine_v2.py`).
- **Dependencias:** Pesadas (`prophet`, `pulp`, `scipy`, `plotly`, `crewai` sin declarar en `requirements.txt` aunque se usa en `agent_brain.py`). Gran deuda interna por duplicidad de archivos `v1` y `v2`.
- **Valor de Negocio (Datalaria):** **Muy Alto (Core B2B / Consultoría C-Level).** Representa exactamente la propuesta de valor diferencial de Datalaria ("Ingeniería de Operaciones, Modelos Cuantitativos e IA Aplicada"). Convertirlo en una app interactiva (Sandbox S&OP donde el usuario sube su CSV o juega con restricciones de capacidad) dispararía la conversión de leads ejecutivos.

#### 4. **Radar de Obsolescencia (`obs-management`)**
- **Acoplamiento con el Portal:** **Alto riesgo de experiencia rota en producción.** Está enlazado en `/es/apps/` hacia `/apps/obs-management/`, lo que sirve `static/apps/obs-management/index.html`. Sin embargo, ese HTML hace un `fetch("http://localhost:8001/api/v1/dashboard/risk-metrics")` en la línea 112. Cuando un visitante entra desde `datalaria.com`, la llamada a `localhost:8001` falla siempre y el dashboard muestra permanentemente: `> OFFLINE. Cannot connect to Analytics API on port 8001.`
- **Cobertura de Tests y Verificación Automatizada:** **Nula (0%).** Sin tests ni linters. Además, tiene dos entrypoints FastAPI separados (`main.py` en puerto 8000 para webhooks y `dashboard_api.py` en puerto 8001 con datos mockeados).
- **Dependencias:** Usa `tailwindcss` vía CDN en el navegador, y en Python mezcla `langchain>=0.1.0`, `langchain-google-genai>=0.0.9` y `crewai>=0.11.0` (versiones antiguas).
- **Valor de Negocio (Datalaria):** **Muy Alto (Core B2B / Supply Chain Risk).** Es un caso de uso ejecutivo brillante (calcular el impacto en P&L de un componente EOL recorriendo el árbol BOM). Arreglar su modo demo/interactivo en web es prioritario para la imagen de marca.

#### 5. **Dashboard Climático (`weather`)**
- **Acoplamiento con el Portal:** **Bajo (Desacoplado por Proxy).** Aunque hay copias locales en `static/apps/weather/` y `temp_app_weather/`, en producción `static/_redirects` redirige `/apps/weather/*` mediante un proxy `200!` hacia `https://datalaria-app-weather.netlify.app/`.
- **Cobertura de Tests y Verificación Automatizada:** **Nula.** Es un único archivo `index.html` de 1.864 líneas que mezcla estilos CSS, marcado HTML, traducciones ES/EN y lógica de Chart.js/Leaflet, acompañado de un script monolítico `read_weather.py` (19 KB).
- **Dependencias:** Múltiples librerías cargadas por CDN (`PapaParse`, `Chart.js`, `date-fns`, `Choices.js`, `Leaflet`, `Feather Icons`).
- **Valor de Negocio (Datalaria):** **Medio (Portfolio / Tráfico SEO).** Es un buen escaparate de visualización de datos y ML ligero respaldado por una serie de 4 posts, pero no monetiza directamente en el segmento C-Level.

#### 6. **Flashcards IA (`flashcards`), Neon Snake (`snake`), Conversor (`conversor`) y Matemáticas (`maths`)**
- **Acoplamiento con el Portal:** **Bajo en código, Alto en duplicación por idioma.** En lugar de usar internacionalización (i18n) basada en diccionarios JSON, estas 4 aplicaciones duplican sus archivos HTML enteros en subcarpetas `/es/` y `/en/` (en el caso de `conversor`, son 7 archivos HTML en `/es/` y 7 archivos HTML idénticos traducidos en `/en/`). Cualquier cambio funcional obliga a editar el código por duplicado.
- **Seguridad y Dependencias:**
  - Todas usan `<script src="https://cdn.tailwindcss.com"></script>` en producción (desaconsejado por rendimiento y estabilidad visual).
  - `flashcards` pide al usuario su `GEMINI_API_KEY` en el cliente (patrón BYOK válido para demos gratuitas, pero llama a modelos/endpoints que pueden quedar deprecados si están hardcodeados en los archivos HTML).
  - `snake` expone la URL y Anon Key de un proyecto Supabase secundario directamente en el HTML.
- **Valor de Negocio (Datalaria):** **Bajo (Experimentos de etapas iniciales del blog).** Cumplen una función simpática de entretenimiento o curiosidad ("Lead Magnets blandos"), pero diluyen el posicionamiento ejecutivo C-Level de Datalaria si ocupan el mismo nivel jerárquico que `Agentic Radar` o `LifeOps`.

---

### 2.3 Matriz Resumen de Auditoría (Estado Actual)

| Aplicación | Acoplamiento Portal | Deuda / Riesgo Técnico | Tests / Verificación | Alineación B2B / Monetización |
| :--- | :---: | :--- | :---: | :---: |
| **1. LifeOps (`lifeops`)** | Bajo (Build copiado a `static/`) | Media (JS sin TS, copia manual de `dist/`, `python-jose`) | Oxlint + Pydantic (0% Tests) | ⭐⭐⭐⭐ (Potencial SaaS Prosumer / Flagship) |
| **2. Agentic PMO (`project-ops`)** | Crítico (Código Python en `static/`) | Baja en código, Alta por falta de UI y ubicación | `TECH_SPEC.md` + Pydantic (0% Tests) | ⭐⭐⭐⭐⭐ (Upsell directo de Suite 03 PMBOK) |
| **3. S&OP Pipeline (`sop-pipeline`)** | Crítico (Código Python en `static/`) | Alta (Archivos `v1`/`v2` duplicados, sin API/UI web) | Humo manual (0% Tests) | ⭐⭐⭐⭐⭐ (Core Operations Engineering B2B) |
| **4. Obsolescence Radar (`obs-management`)** | Crítico (UI en `static/` apunta a `localhost:8001` roto) | Alta (UI rota en prod, código Python en `static/`) | 0% Tests / Sin Linter | ⭐⭐⭐⭐⭐ (Caso ejecutivo estrella para CFO/COO) |
| **5. Weather (`weather`)** | Bajo (Proxy Netlify externo) | Alta (3 copias en repo, `.git` corrupto, HTML 1.8k LOC) | 0% Tests / Sin Linter | ⭐⭐⭐ (Demostrador técnico Data/ML) |
| **6. Neon Snake (`snake`)** | Bajo (Estático en `static/games/`) | Media (HTML duplicado ES/EN, Supabase hardcodeado) | 0% Tests | ⭐⭐ (Engagement / Gamificación) |
| **7. Flashcards (`flashcards`)** | Bajo (Estático en `static/apps/`) | Media (HTML duplicado ES/EN, Tailwind CDN) | 0% Tests | ⭐⭐ (experimento IA BYOK) |
| **8. Conversor (`conversor`)** | Bajo (Estático en `static/apps/`) | Alta (14 HTMLs duplicados ES/EN, Tailwind CDN) | 0% Tests | ⭐ (Commodity sin retorno B2B) |
| **9. Matemáticas (`maths`)** | Bajo (Estático en `static/apps/`) | Media (HTML duplicado ES/EN, fuera de nicho) | 0% Tests | ⭐ (Fuera del target ejecutivo de Datalaria) |

---

## 3. PROPUESTA DE ARQUITECTURA DEL PORTAL (VISIÓN A FUTURO SDD)

Para que Datalaria escale con nuevas aplicaciones rentables, mantenibles a largo plazo y **100% gobernables mediante Spec-Driven Development (SDD)** tanto por **Google Antigravity (Gemini 4 Argon)** como por **agentes basados en Claude**, debemos erradicar el patrón de "meter scripts y HTMLs sueltos dentro de `static/`" y adoptar una arquitectura de **Monorepo Políglota Orientado a Especificaciones (Spec-First Modular Monorepo)**.

### 3.1 Estructura de Directorios Objetivo

```text
datalaria/
├── AGENTS.md                        # Punto de entrada universal agnóstico del modelo (Antigravity + Claude)
├── CLAUDE.md                        # Puntero ligero a AGENTS.md para compatibilidad nativa con Claude Code
├── package.json                     # Workspace JS/TS raíz (pnpm/npm workspaces: apps/* y shared/*)
├── pyproject.toml                   # Workspace Python raíz (uv / ruff / pytest unificados)
│
├── specs/                           # 🏛️ EL CORAZÓN SDD (Fuente Única de Verdad)
│   ├── _constitution.md             # Principios innegociables de arquitectura, seguridad, UI y testing
│   ├── _templates/                  # Plantillas formales para nuevas apps (spec.md, plan.md, tasks.md)
│   ├── audit/
│   │   └── 00-ecosystem-audit.md    # Este informe
│   ├── portal/                      # Especificaciones del portal Hugo, Catálogo LemonSqueezy y Edge Functions
│   └── apps/                        # 1 carpeta por App con su contrato formal antes de tocar código
│       ├── lifeops/                 # spec.md, api-contract.openapi.yaml, data-model.sql
│       ├── project-ops/             # Evolución de su actual TECH_SPEC.md
│       ├── sop-pipeline/            # spec.md
│       ├── obs-management/          # spec.md
│       └── weather/                 # spec.md
│
├── portal/ (o raíz limpia para Hugo)# El generador estático Hugo (content/, layouts/, themes/, config.yaml)
│   └── static/                      # EXCLUSIVAMENTE assets estáticos reales y builds compilados por CI/CD
│
├── apps/                            # 🚀 CÓDIGO FUENTE DE LAS APLICACIONES (Fuera de static/)
│   ├── lifeops-web/                 # React + Vite + TypeScript (migrar progresivamente a TS)
│   ├── lifeops-api/                 # FastAPI + Pydantic v2 + Pytest
│   ├── project-ops/                 # FastAPI + Motor EVM/MonteCarlo + UI Sandbox Interactiva
│   ├── sop-pipeline/                # Motor S&OP v2 limpio + API/Sandbox interactivo
│   ├── obs-management/              # Radar de Obsolescencia (FastAPI + UI con Fallback Mock en prod)
│   ├── weather/                     # Instancia única limpia del Dashboard Climático
│   └── legacy-static/               # Contenedor congelado para flashcards, snake, conversor, maths
│
├── shared/                          # 🧩 PAQUETES COMPARTIDOS DEL ECOSISTEMA
│   ├── ui-kit/                      # Tokens CSS corporativos Datalaria, cabecera "Volver al Portal", CTA Upsell
│   ├── auth-sdk/                    # Cliente unificado de Supabase Auth + Gatekeeper de Licencias LemonSqueezy
│   └── py-core/                     # Utilidades compartidas Python (cliente Supabase, logging, LLM wrappers)
│
└── ops/                             # 🤖 AUTOMATIZACIÓN INTERNA (Fuera del runtime de usuario)
    ├── autopilot/                   # Orquestador de RRSS y Autopilot-Ctrl
    └── pack-builders/               # Scripts generadores de los Executive Decision Packs (Excel/PPTX/PDF)
```

---

### 3.2 Cómo Compartirán UI, Autenticación, Datos y Monetización

```mermaid
flowchart LR
    subgraph SpecLayer["1. Capa SDD (/specs/)"]
        Spec["spec.md\n(Contratos, Modelo, Invariantes)"]
    end

    subgraph SharedLayer["2. Capa Compartida (/shared/)"]
        UI["@datalaria/ui-kit\n(Design Tokens, Shell Header, Upsell Banner)"]
        Auth["@datalaria/auth-sdk\n(Supabase SSO + LemonSqueezy License Check)"]
    end

    subgraph AppLayer["3. Islas de Aplicación (/apps/*)"]
        Sandbox["Modo Sandbox (Gratis / In-Browser o Mock)\nCaptura el Lead Ejecutivo"]
        ProMode["Modo Pro / Cloud (Autenticado)\nPersistencia + IA Agéntica + Exportación DOCX/XLSX"]
    end

    subgraph DataLayer["4. Capa de Datos Unificada (Supabase Core)"]
        PG[("Proyecto Único Supabase\n(datalaria-core)\nAislamiento por PostgreSQL Schemas:\n- schema: lifeops\n- schema: pmo_analytics\n- schema: sop_engine\n- schema: obs_radar\n- schema: public (leaderboards/auth)")]
    end

    Spec ==>|"Gobierna a Agentes\n(Gemini 4 / Claude)"| AppLayer
    UI --> AppLayer
    Auth --> AppLayer
    Sandbox -->|"CTA: Desbloquear Pack o Pro"| ProMode
    ProMode --> Auth
    ProMode --> PG
```

1. **Integración de UI y Experiencia de Marca (`@datalaria/ui-kit`):**
   - **Problema actual:** Cada app tiene un diseño inconexo (LifeOps es dark emerald glassmorphism, Obsolescence Radar es azul táctico, Flashcards es blanco celeste, Conversor es gris oscuro, el Portal es PaperMod). Además, varias apps carecen de barra de navegación de retorno al portal o de enlaces a los Executive Packs relacionados.
   - **Solución:** Definir un archivo ligero de Design Tokens CSS (`datalaria-tokens.css`) y un Web Component o Partial compartido (`<datalaria-app-shell>`) que inyecte automáticamente en todas las apps:
     1. Cabecera compacta con logo de Datalaria, selector de idioma (`ES`/`EN`) y botón de retorno al portal.
     2. **Banner Contextual de Monetización (Upsell):** Si el usuario está en el sandbox de `project-ops`, el shell muestra un CTA directo al *Executive Pack de EVM / PERT* o a la *Suite 03 en Lemon Squeezy*.
2. **Unificación de Datos en un Único Proyecto Supabase Multi-Esquema:**
   - **Problema actual:** Tienes múltiples proyectos de Supabase dispersos (`wkbmxekmofrjtcsyytrv`, `wxwnbzmbzztegcdzrxbg`, etc.) que en el plan gratuito de Supabase se pausan por inactividad o agotan el límite de proyectos activos.
   - **Solución:** Consolidar toda la persistencia en **un único cluster de Supabase (`datalaria-core`)** separado estrictamente por **Esquemas PostgreSQL (`schemas`)** con Row-Level Security (RLS) activado, exactamente como ya empezaste a hacer en `lifeops` (`schema: lifeops`) y `project-ops` (`schema: pmo_analytics`).
     - `schema: auth` (Gestionado por Supabase para SSO único en todas las apps de Datalaria).
     - `schema: lifeops` (Tablas de LifeOps).
     - `schema: pmo_analytics` (Tablas de Project-Ops).
     - `schema: sop_engine` (Tablas de S&OP Pipeline).
     - `schema: obs_radar` (Tablas BOM/AML de Obsolescence Management).
     - `schema: arcade` (Tabla `snake_scores` con políticas RLS de solo inserción acotada).
3. **Autenticación y Monetización "Dual-Mode" (Sandbox Gratis + Pro/Pack):**
   - **Regla de Oro para Datalaria:** Ninguna aplicación publicada en `/apps/` puede fallar con un error de conexión a `localhost` (como ocurre hoy en `obs-management`) ni exigir login obligatorio antes de mostrar valor.
   - **Patrón "Offline-First / Mock-First Sandbox":** Siguiendo el excelente patrón que implementaste en [lifeops-app/src/lib/api.js](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/lifeops-app/src/lib/api.js#L10-L15) (`mock=true`), **todas las apps B2B tendrán un modo interactivo determinista en el navegador** (usando datasets precargados o cálculo en cliente/Edge) para que cualquier ejecutivo pueda probar el dashboard al instante.
   - **Desbloqueo de Valor (Monetización):** Cuando el usuario quiera (a) subir su propio Excel/CSV corporativo, (b) ejecutar el agente de IA sobre sus datos o (c) descargar el modelo financiero desbloqueado, la app verifica su sesión de Supabase Auth o valida una **Clave de Licencia de Lemon Squeezy** para habilitar el backend FastAPI.
4. **Compatibilidad 100% Agnóstica del Modelo (Antigravity Gemini 4 Argon + Agentes Claude):**
   - El estándar común será un archivo raíz **`AGENTS.md`** (leído nativamente por agentes modernos y referenciado desde `CLAUDE.md`) junto con el árbol **`/specs/`**.
   - Ningún agente tendrá permitido escribir código en `/apps/` sin antes leer y actualizar el archivo `/specs/apps/<app-name>/spec.md`, donde estarán definidos en Markdown puro y Mermaid: (1) Contexto de negocio y vínculo con Lemon Squeezy, (2) Contratos de entrada/salida (Pydantic / JSON Schema), (3) Esquema de base de datos, (4) Invariantes matemáticas y (5) Comandos exactos de verificación automatizada (`pytest`, `oxlint`, `tsc`).

---

## 4. PLAN DE EXTRACCIÓN SDD (MATRIZ DE MIGRACIÓN REAJUSTADA A LAS 7 APPS ACTIVAS)

Aplicando la regla de negocio verificada (**solo se auditan/migran primero las 7 aplicaciones publicadas en `/apps/` que cuentan con artículo publicado `draft: false`**), la matriz de migración queda estructurada en 4 grupos claros:

### Categoría A: "Listas para documentar" (Activas y Maduras — Prioridad 1)
*Aplicaciones publicadas y respaldadas por posts activos cuya arquitectura permite extraer su especificación SDD (`spec.md`) de inmediato.*

| Aplicación | Respaldo Editorial (`draft: false`) | Acción de Extracción SDD | Valor de Negocio |
| :--- | :--- | :--- | :--- |
| **1. `lifeops` (`lifeops-app` + `lifeops-api`)** | 5 posts publicados (`app-lifeops_part1` a `part5`). | **Primera App a documentar (Hito 1.1).** Extraer `/specs/apps/lifeops/spec.md` documentando sus 5 dominios (Activities, Projects/Kanban, Stats, Alerts, DOCX/XLSX Reports), contrato OpenAPI, esquema `lifeops` y modo `mock=true`. | **Alto (Flagship SaaS).** Es la aplicación Full-Stack más completa publicada hoy en la web. |

---

### Categoría B: "Requieren aislamiento previo" (Activas con Deuda de Contorno — Prioridad 2)
*Aplicaciones publicadas en `/apps/` y con serie de artículos activos, pero que requieren desacoplar código backend de `static/` o limpiar duplicados antes de cerrar su migración SDD.*

| Aplicación | Respaldo Editorial (`draft: false`) | Problema de Contorno / Deuda | Refactorización SDD Requerida |
| :--- | :--- | :--- | :--- |
| **2. `obs-management` (Agentic Radar / Radar de Obsolescencia)** | 7 posts publicados (`obs_parte1_intro` a `obs_parte7_dashboard`). | 1. El frontend en `/apps/obs-management/` falla en producción (`OFFLINE`) porque hace `fetch` duro a `http://localhost:8001`.<br>2. Expone `.py`, `.sql` y `.env` dentro de `static/apps/obs-management/`. | 1. Crear `/specs/apps/obs-management/spec.md`.<br>2. Sacar los scripts Python/SQL a `apps/obs-management/`.<br>3. Dotar a `index.html` de **Modo Sandbox / Fallback Determinista** para que el visitante vea siempre la telemetría CrewAI y los 15.450 € de margen en riesgo funcionando en vivo, más el enlace al post y suites. |
| **3. `weather` (Weather / El Tiempo)** | 4 posts publicados (`app-openweather_part1` a `part4`). | 1. Triplicado en el repositorio (`static/apps/weather/`, `temp_app_weather/`, `github.io/app-openweather/`).<br>2. Contiene objetos `.git` corruptos dentro de `static/apps/weather/`. | 1. Crear `/specs/apps/weather/spec.md`.<br>2. Eliminar los clones redundantes y limpiar los metadatos `.git` huérfanos.<br>3. Mantener intacto el proxy `200!` hacia `datalaria-app-weather.netlify.app`. |

---

### Categoría C: "No migrables / Congelar en Legacy" (Activas de Baja Complejidad — Prioridad 3)
*Las 4 aplicaciones restantes de las 7 publicadas en `/apps/`. Cuentan con post publicado y funcionan como experimentos o juegos, pero por su simpleza estática no compensa reescribirlas ni migrarlas a SDD completo.*

| Aplicación | Respaldo Editorial (`draft: false`) | Acción en el Plan (Revisión Ligera y Congelación) |
| :--- | :--- | :--- |
| **4. `snake` (Neon Snake)** | `game_snake` (única tarjeta en `/apps/` que hoy tiene botón *"Leer Post"*). | Mantener congelada en `static/games/snake/`. Solo verificar RLS en la tabla `snake_scores` de Supabase y agrupar en la sección de experimentos/arcade. |
| **5. `flashcards` (Flashcards)** | `app_flashcards` | Mantener congelada en `static/apps/flashcards/`. Verificar únicamente que el endpoint/modelo de Gemini invocado por el cliente BYOK siga activo. |
| **6. `conversor` (Unit Converter)** | `app_conversor_unidades` / `app_unit_converter` | Mantener congelada tal cual en `static/apps/conversor/` para preservar los enlaces del artículo. |
| **7. `maths` (Maths)** | `founderz-programando-chatGPT` | Mantener congelada tal cual en `static/apps/maths/` para preservar el enlace del artículo. |

---

### Categoría D: "En Incubación / No Publicadas" (Posponer hasta cerrar las 7 activas — Prioridad 4)
*Proyectos cuyo código existe en `static/apps/` pero que **NO están publicados en `/apps/`** (o cuyos artículos siguen en `draft: true`). Se revisarán, validarán y publicarán por primera vez directamente bajo la nueva arquitectura SDD una vez terminemos con las 7 apps activas.*

| Proyecto en Incubación | Estado de Publicación Actual | Acción Inmediata (Solo Higiene) vs. Acción Futura (Fase 4) |
| :--- | :--- | :--- |
| **8. `project-ops` (Agentic PMO Sandbox)** | **Inédito.** Sus posts `proj_ops_parte1_intro` y `proj_ops_parte2_agentic_pmo` están en **`draft: true`** y falta el post del Sandbox. No aparece en `/apps/`. | **Ahora:** No migrar ni publicar. Únicamente retirar su carpeta de `static/apps/` hacia `apps/project-ops/` (en cuarentena de incubación) para que Hugo no publique sus `.py`/`.env` por accidente.<br>**Después (Fase 4):** Revisar contigo su `TECH_SPEC.md`, validar el motor, crear su UI Sandbox y publicarlo por primera vez junto con sus artículos. |
| **9. `sop-pipeline` (S&OP Autonomous Pipeline)** | **Sin Web App publicada.** Los 5 posts de S&OP están publicados pero enlazan a un Google Colab externo, no a `/apps/sop-pipeline/`. No aparece en `/apps/`. | **Ahora:** No migrar a Web App todavía. Únicamente retirar sus scripts `.py`/`.env` de `static/apps/` hacia `apps/sop-pipeline/` por seguridad.<br>**Después (Fase 4):** Revisar, limpiar `v1`/`v2`, especificar bajo SDD y lanzar como nueva App B2B si así lo decides. |

---

## 5. HOJA DE RUTA DE EJECUCIÓN REAJUSTADA

1. **Fase 0 — Gobernanza y Constitución SDD (Completada ✅):**
   - `AGENTS.md`, `CLAUDE.md`, `specs/_constitution.md`, `specs/DECISIONS.md` y `specs/ROADMAP.md` actualizados con la regla de correspondencia `App Activa <-> Post Publicado`.
2. **Fase 1 — Extracción SDD de la App Activa Lista (`lifeops`) y del Portal:**
   - **Hito 1.1:** Generar `/specs/apps/lifeops/spec.md` (nuestra primera App activa de las 7).
   - **Hito 1.2:** Generar `/specs/portal/spec.md` (incluyendo el catálogo de las 7 apps y la regla de que toda tarjeta en `/apps/` tenga su botón *"Leer Post / Read Post"*, como ya tiene `Neon Snake`).
3. **Fase 2 — Aislamiento y Saneamiento de las Apps Activas con Deuda (`obs-management` y `weather`) + Cuarentena de No Publicadas:**
   - **Hito 2.1:** Especificar, aislar Python y reparar el modo Sandbox de **`obs-management` (Agentic Radar)** para que funcione 24/7 en producción sin dar error `OFFLINE`.
   - **Hito 2.2:** Especificar y limpiar los 3 clones y el `.git` corrupto de **`weather`**.
   - **Hito 2.3:** Checklist de verificación de las 4 apps legacy activas (`snake`, `flashcards`, `conversor`, `maths`) y movimiento preventivo a cuarentena fuera de `static/` de los códigos inéditos (`project-ops` y `sop-pipeline`).
4. **Fase 3 — Reorganización Visual de `/apps/` (Las 7 Apps Activas):**
   - Estructurar `/es/apps/` y `/en/apps/` destacando las Apps principales con enlaces directos a sus series de artículos publicados y a las Suites de Lemon Squeezy.
5. **Fase 4 — Incubadora de Nuevos Lanzamientos SDD (`project-ops` y futuras Apps):**
   - Revisar, validar y publicar por primera vez `project-ops` (y el nuevo frontend de `sop-pipeline`) siguiendo de principio a fin la nueva arquitectura SDD cuando quitemos el `draft: true` de sus artículos.
