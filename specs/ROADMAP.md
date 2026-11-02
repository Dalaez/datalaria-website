# Hoja de Ruta Maestra y Control de Estado SDD (`ROADMAP.md`)

> **PROPÓSITO CRÍTICO:** Este archivo es la **Memoria de Estado Persistente** del proyecto Datalaria.  
> Todo agente (Antigravity Gemini 4 Argon / Claude) DEBE leer este archivo al inicio de cada sesión para saber exactamente qué se ha completado, qué tarea toca ejecutar ahora y cómo revertir en caso de fallo.

---

## 📍 ESTADO ACTUAL DEL PROYECTO (PUNTERO DE SESIÓN)

- **Fase Activa:** `FASE 5 EN CURSO 🚀` — **Datalaria Pulse (Content Ops as Code)** *(Fases 0, 1, 2 y 3 completadas al 100% ✅)*
- **Último Checkpoint Verificado:** Hito 5.8 — Lanzamiento Editorial Datalaria Pulse completado (5 artículos bilingües ES/EN, ficha /apps/pulse/ en draft por embargo comercial hasta 18 nov, 142 activos, 18/18 pytest verde, Hugo 2.279+ páginas código 0) (Completado el 2026-11-02 ✅).
- **Próximo Hito:** Hito 6.0 — Pre-lanzamiento editorial de Datalaria Helix, integración *in-place* de la tarjeta pack-sdd en /recursos/ y lista de espera Brevo (ADR-017).
- **Ventana agendada (2026-11-04):** Hito 6.0 — Pre-lanzamiento editorial de Datalaria Helix, integración *in-place* de la tarjeta `pack-sdd` en `/recursos/` y lista de espera Brevo (ADR-017). El Hito 6.1 arranca tras cerrar el 5.8.

---

## 📋 PREMISA EDITORIAL VERIFICADA: LAS 7 APPS ACTIVAS EN PRODUCCIÓN

Tras auditar todos los artículos de `/content/es/posts/` y `/content/en/posts/` frente a la página `/apps/` actual, este es el mapa oficial de estado:

| # | App en `/apps/` | Ruta Web | Post(s) Publicados (`draft: false`) | Categoría SDD |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **LifeOps** | `/apps/lifeops/` | `app-lifeops_part1` a `part5` (5 posts) | **🟢 Lista para documentar** (Empezamos por aquí) |
| **2** | **Agentic Radar** | `/apps/obs-management/` | `obs_parte1_intro` a `obs_parte7_dashboard` (7 posts) | **🟡 Requiere aislamiento previo** (Sacar `.py` de `static/` + reparar modo Sandbox para evitar error `OFFLINE`) |
| **3** | **Weather** | `/apps/weather/` | `app-openweather_part1` a `part4` (4 posts) | **🟡 Requiere aislamiento previo** (Limpiar 3 clones y `.git` corrupto) |
| **4** | **Neon Snake** | `/games/snake/` | `game_snake` (1 post — ya tiene botón *"Read Post"*) | **🔴 No migrable (Frozen Legacy)** (Solo verificar RLS en Supabase) |
| **5** | **Flashcards** | `/apps/flashcards/` | `app_flashcards` (1 post) | **🔴 No migrable (Frozen Legacy)** (Solo verificar endpoint Gemini BYOK) |
| **6** | **Unit Converter** | `/apps/conversor/` | `app_conversor_unidades` (1 post) | **🔴 No migrable (Frozen Legacy)** (Mantener congelada) |
| **7** | **Maths** | `/apps/maths/` | `founderz-programando-chatGPT` (1 post) | **🔴 No migrable (Frozen Legacy)** (Mantener congelada) |

> **📦 Proyectos en Incubación (Posponer hasta Fase 4):**
> - **`project-ops` (Agentic PMO Sandbox):** Sus posts `proj_ops_parte1_intro` y `proj_ops_parte2_agentic_pmo` están en **`draft: true`** y la app aún no ha sido publicada.
> - **`sop-pipeline` (S&OP Autonomous Pipeline):** Sus posts enlazan a un Google Colab externo; no existe aún como Web App publicada en `/apps/`.
> - *Regla:* Ambos salen de las Fases 1-3 de migración funcional (solo se sacarán sus archivos `.py`/`.env` de `static/` por seguridad) y se abordarán en la **Fase 4** cuando vayamos a revisarlos, validarlos y publicarlos por primera vez bajo SDD.

---

## 🛡️ PROTOCOLO DE PROGRESO SEGURO Y MARCHA ATRÁS (ROLLBACK)

1. **Granularidad Atómica (1 Hito = 1 Turno):** Nunca mezclamos dos aplicaciones distintas en el mismo paso.
2. **Punto de Restauración Pre-Cambio (Git Checkpoint):** Antes de cualquier hito que mueva archivos o toque código (a partir de Fase 2):
   ```powershell
   git status --short
   git tag -f sdd-checkpoint-pre-<hito-id>
   ```
3. **Marcha Atrás Inmediata (Emergency Rollback):** Si falla cualquier verificación:
   ```powershell
   git reset --hard sdd-checkpoint-pre-<hito-id>
   git clean -fd
   ```

---

## 🗺️ PLAN MAESTRO POR FASES (CHECKLIST DE EJECUCIÓN)

### FASE 0: Cimientos, Gobernanza y Constitución SDD (Completada ✅)
- [x] **Hito 0.1:** Auditoría estática del ecosistema y cruce con posts publicados ([`00-ecosystem-audit.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/audit/00-ecosystem-audit.md)).
- [x] **Hito 0.2:** Constitución Arquitectónica y ADRs actualizados con la regla `App Activa ⇔ Post Publicado` ([`_constitution.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/_constitution.md), [`DECISIONS.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/DECISIONS.md)).
- [x] **Hito 0.3:** Protocolo de arranque multi-modelo y plantilla maestra ([`AGENTS.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/AGENTS.md), [`CLAUDE.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/CLAUDE.md), [`app-spec.template.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/_templates/app-spec.template.md)).

---

### FASE 1: Extracción SDD de LifeOps (#1) & Sistema de Fichas de Apps
*Objetivo: Migrar y aislar con rigor la primera aplicación activa (`LifeOps`), resolver sus riesgos técnicos/seguridad, y desplegar la nueva infraestructura de fichas dedicadas con historial evolutivo (`apps-showcase`) antes de abordar la Fase 2.*

- [x] **Hito 1.1: Especificación Formal de `lifeops` y de `apps-showcase`**
  - *Acción:* 
    1. Generar [`/specs/apps/lifeops/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/lifeops/spec.md) documentando la arquitectura actual (`lifeops-app` + `lifeops-api`), esquema `lifeops`, endpoints REST, modo `mock=true`, invariantes y changelog SemVer v0.1.0 -> v1.0.0.
    2. Generar [`/specs/portal/apps-showcase/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/portal/apps-showcase/spec.md) con el diseño del nuevo sistema de fichas, metadatos en `data/apps/<slug>.yaml`, tarjetas visuales con captura, historial de versiones y shortcode `app-ref`.
  - *Gate de Verificación:* Documentos validados; cero cambios en código de producción. (Completado el 2026-10-24 ✅).

- [x] **Hito 1.2: Aislamiento Limpio, Fix de Seguridad y Verificación de `lifeops`**
  - *Acción:*
    1. Crear checkpoint Git `sdd-checkpoint-pre-1.2`.
    2. Mover `lifeops-app/` a `apps/lifeops/web/` y `lifeops-api/` a `apps/lifeops/api/` con `git mv`.
    3. Resolver **SEC-1** en `apps/lifeops/api/middleware/auth.py` (verificación estricta de firma JWT, eliminando `verify_signature: False`) y **SEC-2** (migrar a `PyJWT`).
    4. Crear suite básica `pytest` en `apps/lifeops/api/tests/` (verificando `/health`, invariantes y token forjado -> 401).
    5. Crear script de build unificado `build:portal` en `apps/lifeops/web/` para compilar y sincronizar con `static/apps/lifeops/`.
    6. Actualizar `rootDir` en `render.yaml`.
  - *Gate de Verificación:* `npm run lint` pasa con 0 errores; `npm run build:portal` compila en 54s a `static/apps/lifeops/`; `pytest` pasa 6/6 tests (100%); `hugo --renderToMemory` compila 2077 páginas con código 0. (Completado el 2026-10-24 ✅).

- [x] **Hito 1.3: Infraestructura del Portal para Fichas de Apps (`apps-showcase`)**
  - *Acción:*
    1. Implementar `layouts/apps/list.html` con soporte de tarjetas visuales (`partials/app-card.html`) agrupadas por tier (`flagship`, `b2b`, `lab`).
    2. Implementar `layouts/apps/single.html` con las 8 secciones de detalle (Hero, Objetivos, Features, Diseño, Tecnologías, Posts relacionados, Changelog evolutivo, CTA).
    3. Implementar shortcode `layouts/shortcodes/app-ref.html`.
    4. Estilos en `assets/css/extended/apps-showcase.css` basados en tokens de PaperMod.
    5. Validaciones automáticas en tiempo de build (`errorf` ante campos requeridos o posts inexistentes).
  - *Gate de Verificación:* `hugo --renderToMemory` compila las 2077 páginas con código 0 en 29.9s; el listado `/es/apps/` y `/en/apps/` compila limpiamente agrupando las 7 apps en sus respectivos tiers. (Completado el 2026-10-24 ✅).

- [x] **Hito 1.4: Despliegue de Ficha de LifeOps y Actualización de Posts**
  - *Acción:*
    1. Crear `data/apps/lifeops.yaml` con todos los metadatos, objetivos, diseño, stack y releases (v0.1.0 -> v1.0.1).
    2. Crear páginas de contenido `content/es/apps/lifeops/index.md` y `content/en/apps/lifeops/index.md` con captura `cover.png` localizada.
    3. Insertar shortcode `{{</* app-ref slug="lifeops" */>}}` y enlaces a la ficha técnica en los 5 artículos de la serie LifeOps en ES y EN (10 archivos en total).
  - *Gate de Verificación:* Las fichas `/es/apps/lifeops/` y `/en/apps/lifeops/` compilan limpiamente mostrando todos sus datos, timeline SemVer, enlaces directos a la App y al modo demo; los 10 posts renderizan la tarjeta del shortcode `app-ref`; `hugo --renderToMemory` compila 2079 páginas con código 0 en 23.3s. (Completado el 2026-10-24 ✅).

- [x] **Hito 1.5: Evolución Analítica del Dashboard 360° de LifeOps (`v1.1.0` — ADR-013)**
  - *Acción:*
    1. Actualizar `/specs/apps/lifeops/spec.md` a `v1.1.0` y registrar `ADR-013` en `/specs/DECISIONS.md`.
    2. Ampliar `GET /api/v1/activities/details` en `apps/lifeops/api/routers/activities.py` con soporte de rango de fechas (`date_from`, `date_to`) y `limit=2000` (def. `500`), más test de contrato `INV-9` en `pytest`.
    3. Enriquecer el dataset sintético (`?mock=true`) en `apps/lifeops/web/src/lib/api.js` con actividades distribuidas en distintas semanas y meses para comparativas inter-periodo realistas.
    4. Implementar el motor determinista `apps/lifeops/web/src/lib/analyticsEngine.js` y el nuevo Dashboard 360° interactivo en `DashboardPage.jsx` + `DashboardPage.css` con los 4 bloques: (1) Filtros por Año/Mes/Semana + Categoría + Subcategoría (ej. Running/Ciclismo/Gym) + Métrica (Sesiones, Km, Calorías, Horas, Páginas), (2) 4 KPIs dinámicos con $\Delta\%$ vs periodo anterior, (3) Gráfico de evolución temporal multimétrica con comparativa, (4) Donut de subcategorías y Mapa de Calor de consistencia diaria (estilo Strava/GitHub).
    5. Actualizar diccionarios `es.js` / `en.js` y publicar release `v1.1.0` en `data/apps/lifeops.yaml`.
  - *Gate de Verificación:* `npm run lint` (`oxlint`: 0 errores), `npm run build:portal` (compilado en 11.7s a `static/apps/lifeops/`), `pytest -v` (7/7 tests en verde) y `hugo --renderToMemory` (2145 páginas ES/EN con código de salida 0). (Completado el 2026-10-27 ✅).

- [x] **Hito 1.6: Mitigación de Latencia Cold-Start, Caché SWR y Corrección de Carga Analítica (`v1.1.1`)**
  - *Acción:*
    1. Corregir parámetro `limit=200` en `DashboardPage.jsx` para cumplir con la restricción `le=200` del endpoint `/api/v1/activities/details` desplegado en Render (que devolvía HTTP 422 con `limit=1000`).
    2. Añadir detección inteligente de ventana temporal inicial (`applyAutoPeriodIfNeeded`): si los últimos 30 días no tienen registros pero existen actividades en los últimos 90 días o en el año en curso, selecciona automáticamente `90 Días` o `Por Año`.
    3. Implementar caché *Stale-While-Revalidate* aislada por `user.id` en `api.js` (`INV-10`), pre-warming temprano (`wakeUpServer`) en `AuthContext.jsx` y banner de sincronización en primer plano (`cloud-sync-banner`) en `DashboardPage.jsx`.
  - *Gate de Verificación:* `npm run lint` (`oxlint`: 0 errores), `npm run build:portal` y `hugo --renderToMemory` con código de salida 0. (Completado el 2026-10-27 ✅).

- [x] **Hito 1.7: Publicación Editorial de LifeOps v1.1.1 (Parte 6 de la Serie + Ficha Técnica y Capturas Pobladas)**
  - *Acción:*
    1. Actualizar `data/apps/lifeops.yaml` incorporando la feature del Dashboard 360° Analytics, las releases `v1.1.0` y `v1.1.1`, y el enlace bidireccional al nuevo post Parte 6 en la lista de artículos.
    2. Actualizar `/specs/apps/lifeops/spec.md` (§1.3 con la Parte 6 y §9 con el historial evolutivo).
    3. Redactar y publicar el artículo técnico en español e inglés: `content/es/posts/app-lifeops_part6_analytics_dashboard_360/` y `content/en/posts/app-lifeops_part6_analytics_dashboard_360/` con capturas de pantalla, diagrama Mermaid, shortcode `app-ref` e ilustraciones del banner de sincronización Supabase/Render y mapa de calor.
    4. *Población y Capturas Reales:* Inserción en Supabase PostgreSQL de dataset sintético en inglés exclusivamente para `datalaria@gmail.com` (16 actividades de octubre de 2026 con running, ciclismo, gym, libros técnicos y cine + tareas Kanban en 2 proyectos) y extracción automatizada con Microsoft Edge headless de capturas reales pobladas para sobreescribir las imágenes de los posts ES y EN (`cover.png`, `lifeops_dashboard_360_analytics`, `lifeops_analytics_filters_drilldown`, `lifeops_consistency_heatmap_streaks`, `lifeops_cloud_sync_banner_coldstart`). Purga de registros sintéticos duplicados que se habían insertado por error en `dalaez1@gmail.com` y rotación de prefijo de caché SWR (`lifeops_swr_v2:`) en [`api.js`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/apps/lifeops/web/src/lib/api.js).
    5. *Auditoría de Enlaces e Imágenes:* Corrección de enlaces internos con prefijo de idioma (`/es/posts/...` y `/en/posts/...`), sanitización de enlace en `AuthContext.jsx` y reinicio del servidor Hugo para montar en memoria los assets binarios recién agregados. Verificación HTTP 200 de todas las imágenes y enlaces internos.
    6. *Guardia de Seguridad Anti-Contaminación de Datos y Tests INV-11 (ADR-014):* Creación del servicio `services/seeder_guard.py` con listas blancas de seeding y nueva suite `tests/test_data_isolation.py` que bloquea y verifica el aislamiento estricto de cuentas de producción frente a inserciones sintéticas.
  - *Gate de Verificación:* `hugo --renderToMemory` compila limpiamente 2167 páginas con código de salida 0 y paridad total ES/EN; suite HTTP `verify_hugo_links.py` confirma código 200 en todas las imágenes y enlaces de la Parte 6; `pytest` 13/13 tests en verde (100%); `oxlint` 0 errores. (Completado el 2026-10-28 ✅).

---

### FASE 2: Aislamiento y Saneamiento de las Apps Activas con Deuda (`obs-management` y `weather`)
*Objetivo: Arreglar y formalizar bajo SDD las otras dos aplicaciones principales que hoy están publicadas en `/apps/`.*

- [x] **Hito 2.1: Especificación, Aislamiento y Reparación Dual-Mode de `obs-management` (App #2 — Agentic Radar)**
  - *Acción:*
    1. Crear `/specs/apps/obs-management/spec.md` alineado con los 7 artículos publicados (`obs_parte1` a `obs_parte7`).
    2. Sacar los archivos `.py`, `.sql` y `.env` de `static/apps/obs-management/` hacia `apps/obs-management/api/` (eliminando la exposición de código backend en la web y limpiando `.pyc` / `.gitignore`).
    3. Actualizar `static/apps/obs-management/index.html` con el **Modo Sandbox Determinista** (eliminando el error `> OFFLINE`; mostrando `15.450,00 EUR` en riesgo, 2 alertas críticas, tablas de SKUs `DRONE-X1` / `SERVER-RACK-9`, terminal animada CrewAI con replay, upsell a B2B packs y navegación hacia `/es/apps/`).
    4. Crear metadatos en `data/apps/obs-management.yaml`, fichas dedicadas en `content/{es,en}/apps/obs-management/` y actualizar las 14 entradas de blog (`obs_parte1`..`obs_parte7` y `obs_part1`..`obs_part7`) con `{{</* app-ref slug="obs-management" */>}}` y enlaces a la ficha técnica.
  - *Gate de Verificación:* `hugo --renderToMemory` compila las 2081 páginas con código 0 en 20.7s; `static/apps/obs-management/` contiene únicamente `index.html` (cero `.py`/`.sql`/`.env`/`.pyc`); dashboard 100% interactivo en navegador sin backend local. (Completado el 2026-10-24 ✅).
- [x] **Hito 2.2: Especificación y Limpieza de Clones de `weather` (App #3 — Dashboard Climático)**
  - *Acción:*
    1. Crear `/specs/apps/weather/spec.md` alineado con los 4 artículos publicados (`app-openweather_part1` a `part4`).
    2. Consolidar el código fuente canónico en `apps/weather/` (`index.html`, `read_weather.py`, `requirements.txt`, `ciudades.txt`, workflow GitHub Actions `.github/workflows/actualizar-clima.yml` y datos muestra) con su `README.md`.
    3. Purgar metadatos `.git` huérfanos y código Python/backend de `static/apps/weather/`; eliminar la carpeta duplicada `temp_app_weather/` (liberando ~144 MB).
    4. Crear metadatos en `data/apps/weather.yaml`, páginas dedicadas en `content/{es,en}/apps/weather/` con `cover.png` y actualizar los 8 artículos de la serie con `{{</* app-ref slug="weather" */>}}` y enlaces a la ficha técnica.
  - *Gate de Verificación:* `git status` limpio; proxy `200!` hacia `datalaria-app-weather.netlify.app` verificado en `static/_redirects`; `hugo --renderToMemory` compila 2083 páginas con código 0 en 50.6s. (Completado el 2026-10-24 ✅).

---

### FASE 3: Congelación de las 4 Apps Legacy, Higiene de `/static/` y Mejora del Escaparate `/apps/`
*Objetivo: Cerrar el ciclo de las 7 aplicaciones publicadas, retirar de `/static/` los borradores no publicados y dejar el catálogo `/apps/` impecable.*

- [x] **Hito 3.1: Revisión Ligera, Congelación Legacy (Apps #4 a #7) y Cuarentena de No Publicadas**
  - *Acción:*
    1. Verificar estado operativo de las 4 apps legacy congeladas: `snake` (#4), `flashcards` (#5), `conversor` (#6) y `maths` (#7). Purgado subdirectorio `.git` huérfano en `static/games/snake/`.
    2. **Higiene de Seguridad:** Mover las carpetas inéditas `static/apps/project-ops/` y `static/apps/sop-pipeline/` fuera de `static/` hacia `apps/_incubadora/` con sus `.gitignore` dedicados y `README.md`.
    3. **Estandarización de Fichas Legacy:** Crear fichas dedicadas en `content/{es,en}/apps/`, metadatos en `data/apps/`, especificaciones en `specs/apps/`, portadas 16:10 (`cover.png`) e inserción del shortcode `app-ref` y enlaces a ficha en los 8 posts asociados para las 4 apps legacy (`snake`, `flashcards`, `conversor`, `maths`).
  - *Gate de Verificación:* `hugo --renderToMemory` compila las 2.091 páginas con código 0 en 75.0s; cero archivos `.py`, `.sql`, `.env`, `.pyc` ni `.git` en todo el árbol `static/`. (Completado el 2026-10-25 ✅).
- [x] **Hito 3.2: Especificación del Portal y Reorganización Visual de `/es/apps/` y `/en/apps/`**
  - *Acción:*
    1. Crear `/specs/portal/spec.md`.
    2. Actualizar `/content/es/apps/_index.md` y `/content/en/apps/_index.md` con las **7 aplicaciones activas**, jerarquizando arriba las aplicaciones principales (`LifeOps`, `Agentic Radar`, `Weather`) y debajo la sección de laboratorio/arcade (`Neon Snake`, `Flashcards`, `Unit Converter`, `Maths`), añadiendo en **todas** el botón secundario **"Leer Post / Read Post"** hacia su artículo publicado y conectando las B2B con las Suites de Lemon Squeezy (`/recursos/`).
  - *Gate de Verificación:* Paridad exacta ES/EN; 7 botones "Leer Post" y 1 botón "Suite B2B" validados determinísticamente en el HTML generado de `/es/apps/` y `/en/apps/`; compilación de 2.091 páginas con código 0. (Completado el 2026-10-25 ✅).

---

- [x] **Hito 3.3: Reestructuración de la Taxonomía Editorial en 5 Pilares con Blindaje SEO (`ADR-016` / `SPEC-PORTAL-TAXONOMY`)**
  - *Acción:*
    1. Crear [`specs/portal/blog-taxonomy/spec.md`](specs/portal/blog-taxonomy/spec.md) y registrar `ADR-016` en [`specs/DECISIONS.md`](specs/DECISIONS.md).
    2. Migración atómica de los 114 pares de artículos ES/EN (228 archivos markdown) estableciendo los 5 pilares canónicos bilingües (`tech`, `strategy`, `startups`, `pioneers`, `culture`) y preservando el 100% de `tags: [...]` y `categories: [...]` preexistentes para blindar el SEO contra cualquier rotura de URLs.
    3. Actualizar [`layouts/partials/index_profile.html`](layouts/partials/index_profile.html) con soporte dinámico para las 5 pestañas y títulos actualizados (*"El blog en 5 temáticas"* / *"The blog in 5 topics"*).
    4. Adaptar [`assets/css/extended/home-portal.css`](assets/css/extended/home-portal.css) con layout grid de 5 columnas en escritorio y media queries fluidas.
    5. Actualizar la aplicación Datalaria Pulse (`apps/pulse/web/`) integrando los 5 pilares en sus gráficos analíticos, métricas, modales e i18n (`view_mode_themes`), y compilar el bundle a `static/apps/pulse/`.
    6. Reconstrucción determinista del índice de Datalaria Pulse (`build_index.py`, `publish_public.py`) sincronizando los 141 activos.
    7. Actualizar la sección general de Blog ([`layouts/posts/section.html`](layouts/posts/section.html) y [`assets/css/extended/blog-filter.css`](assets/css/extended/blog-filter.css)) con fila de botones de filtrado (estilo homologado con `/recursos/`) para las 5 temáticas más píldora "Todos", buscador reactivo en tiempo real con contador en vivo y renderizado 100% HTML estático para garantizar indexabilidad total por crawlers y Googlebot.
  - *Gate de Verificación:* Invariante INV-TAX-1 verificada (0 tags perdidos); suite `pytest ops/pulse/tests/` 18/18 tests pasando (100%); `oxlint` 0 advertencias; compilación de Hugo con código de salida 0; paridad bilingüe exacta ES/EN verificada en los 92 artículos publicados en vivo (48 tech, 8 strategy, 13 startups, 12 pioneers, 11 culture). Auditoría de DOM en `/posts/` confirma 92 tarjetas con enlaces canónicos `<a class="entry-link">` directamente en el código fuente HTML sin muros de paginación. (Completado el 2026-10-31 ✅).

### FASE 4: Incubadora de Nuevos Lanzamientos SDD (Apps No Publicadas y Futuras)
*Objetivo: Una vez consolidado el ecosistema de las 7 apps actuales, revisar, validar contigo y publicar por primera vez las nuevas aplicaciones B2B bajo arquitectura SDD.*

- [ ] **Hito 4.1:** Revisión, validación, creación de UI Sandbox, publicación de los posts (`draft: true` ➔ `draft: false`) y lanzamiento en `/apps/` de **`project-ops` (Agentic PMO Sandbox)**.
- [ ] **Hito 4.2:** Revisión, consolidación de motor `v2`, diseño de UI Sandbox y lanzamiento en `/apps/` de **`sop-pipeline` (S&OP Autonomous Copilot)**.

---

### FASE 5: Nueva App de nicho "Datalaria Pulse" (Content Ops as Code) (sustituye la gestión editorial en Notion) — ver ADR-012
*Objetivo: generar automáticamente desde el repo el registro editorial de posts, apps y kits (vistas tabla, kanban y calendario), dejar Notion y convertirlo en producto monetizable (Sandbox → Kit → Pro).*

- [x] **Hito 5.0: Spec [`specs/apps/pulse/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/pulse/spec.md)** — ADR-012 y especificación formal completados (2026-10-28 ✅). Definidos: arquitectura sin backend cloud v1, modelo de datos unificado (`post`/`app`/`kit`), invariantes `INV-PULSE-1..5` (cero fuga de ideas privadas ni métricas absolutas en `public.json`), compatibilidad Excel 2016+/365 y serie de 5 artículos ES/EN.
- [x] **Hito 5.1: Modelo de datos y Catálogo de Kits** (Completado el 2026-10-28 ✅). Creados contratos tipados Pydantic v2 en ops/pulse/models.py, suite pytest verde (4/4 tests) validando INV-PULSE-1 e INV-PULSE-2, catálogo data/pulse/kits.yaml con 14 Kits, 4 Suites y Mega Bundle, e inicializado data/editorial/backlog.yaml sin depender de Notion.
- [x] **Hito 5.2: Generador de Índice (`ops/pulse/build_index.py`)** (Completado el 2026-10-28 ✅). Emparejamiento bilingüe determinista 100% de los 109 posts ES y 109 posts EN, 7 apps y 19 kits/suites (135 activos consolidados). Tests `pytest` 7/7 pasando.
- [x] **Hito 5.3: Métricas GA4 + Search Console y Relativización** (Completado el 2026-10-28 ✅). Extracción resiliente en `sync_metrics.py` y relativización a base 100 y percentiles en `publish_public.py` (`INV-PULSE-1` e `INV-PULSE-2` verificados). Tests `pytest` 9/9 pasando.
- [x] **Hito 5.4: Automatización CI/CD y Tracker Excel Privado** (Completado el 2026-10-28 ✅). Workflow `.github/workflows/pulse.yml`, regla obligatoria en `AGENTS.md` y generador de Excel comercial y privado (`Pulse_Private_Tracker.xlsx`). Tests `pytest` 11/11 pasando.
- [x] **Hito 5.5: App Web Sandbox React 19 + TypeScript** (Completado el 2026-10-28 ✅). Vistas Tabla, Kanban, Calendario y Salud Editorial, selector bilingüe ES/EN, importador client-side de Notion. Compilada en `static/apps/pulse/`. `oxlint` 0 errores, Hugo código 0.
- [x] **Hito 5.6: Kit descargable** (Completado el 2026-10-28 ✅). Plantilla Excel con taxonomía y desplegables (Pulse_Content_Ops_Template.xlsx), migrador Notion (migrate_notion.py), conector Power Query M (notion_power_query.m), escáner universal en Python puro (pulse_repo_scanner.py), manual maestro (GUIA_PULSE_KIT.md) y paquete comercial ZIP (Datalaria_Pulse_Kit.zip). 15/15 tests pytest en verde.
- [x] **Hito 5.7: Datalaria Pulse Pro (Supabase Cloud + Auth + Sincronización Web ↔ Localhost)** (Completado el 2026-10-29 ✅). Despliegue del esquema pulse en datalaria-core (migración SQL con RLS y PostgREST reload), integración de Supabase Auth en apps/pulse/web/, sincronización bidireccional en tiempo real Web ↔ Localhost, cuenta demo demo@datalaria.com confirmada en Auth con seeder sintético ops/pulse/seed_demo.py y suite pytest 18/18 verde — ADR-015).
- [x] **Hito 5.8: Lanzamiento editorial** (Completado el 2026-11-02 ✅ — 5 posts ES/EN centrados en el Kit básico con capítulo especial en Post 5 sobre el modo Pro y bloque de cierre con demo interactiva en todos los posts, ficha /apps/pulse/, producto en Lemon Squeezy y /recursos/). *Nota Helix:* el Post 5 cerrará con un puente hacia Datalaria Helix (lanzamiento en enero de 2027).

---

### FASE 6: Datalaria Helix — Kit SDD con Escuadrón de 12 Agentes (ver ADR-017)
*Objetivo: convertir el sistema SDD de Datalaria en un producto para profesionales no desarrolladores (Sandbox gratis A+B → Starter → Kit Core; Pro pendiente de validación), desplegando primero el escuadrón de 12 roles internamente en noviembre para auditar y robustecer Datalaria Pulse antes de su salida comercial el 2026-11-18. Plan actualizado el 2026-11-02.*

- [ ] **Hito 6.0: Pre-lanzamiento editorial, mención *teaser* de Pulse, transformación de `pack-sdd` en `/recursos/` y lista de espera Brevo** *(agendado para el 2026-11-04; editorial y portal, sin tocar `/apps/`)*
  - *Acción:* (1) mini-spec `specs/portal/helix-waitlist/spec.md`; (2) mover `agentes_ia_operativa_sdd` ES/EN en exclusiva al `2026-11-11` (desplazando `toma-decisiones-priorizacion-framework-cuantitativo` de esa fecha), alinear referencias cruzadas con `sdd_vs_vibe_coding` (`buildFuture: false` → evitar enlace 404 del 4 al 11 nov) e **incluir mención *teaser* (sin enlace antes del 18 nov) a Datalaria Pulse como primer producto sometido al escuadrón de Datalaria Helix**; (3) corregir `/es/resources/` → `/es/recursos/`; (4) shortcode `helix-waitlist` + parámetro `list: "helix"` en lista blanca en `netlify/functions/subscribe.js` apuntando a las 2 nuevas listas de Brevo (`BREVO_HELIX_LIST_ES` / `BREVO_HELIX_LIST_EN`); (5) **integrar y evolucionar *in-place* la tarjeta existente `pack-sdd` / `suite-sdd`** en `layouts/partials/recursos_catalog.html`, `scripts/generate_recursos_pages.py` y `data/pulse/kits.yaml` hacia **Datalaria Helix** (19€ lanzamiento Early-Bird / 39€, enlace activo a `sdd_vs_vibe_coding`, vista previa en modal, sustitución de los 3 enlaces `mailto:` sin conversión por modal/formulario Brevo de 1 clic y telemetría GA4 `join_waitlist_helix`).
  - *Gate:* `python -m ops.pulse.build_index` + `python -m ops.pulse.publish_public`; `hugo --gc --minify` código 0; alta de prueba verificada en las listas Brevo Helix ES y EN.
- [ ] **Hito 6.1: Spec de Helix y del escuadrón de 12 Agentes** *(ventana: 5–7 nov 2026)* — `specs/apps/helix/spec.md` (invariantes `INV-HELIX-*`), `specs/squad/` (12 fichas `AGENT_SPEC`, `triage-rubric.md`, plantilla `design.md`). *Gate:* solo documentación, aprobación del propietario.
- [ ] **Hito 6.2: Despliegue interno (*Dogfooding*) del escuadrón en Datalaria** *(ventana: 8–11 nov 2026)* — `AGENTS.md` §5 (triaje y carga de roles bajo demanda), Constitución v1.1.0 Art. 9 (separación construcción/verificación, veto QA, disparadores Seguridad/UX), plantilla de spec con "Triaje y asignación", `CLAUDE.md`, ADR-018, `ops/helix/build_adapters.py` (`.agents/`, `.claude/agents/`). *Gate:* `pytest ops/helix/tests`, `pytest ops/pulse/tests` en verde, `hugo --gc --minify` código 0.
- [ ] **Hito 6.3: "Operación Crisol" — Auditoría formal y robustecimiento de Datalaria Pulse por los 12 Agentes de Helix + Preparación del lanzamiento del 18 nov** *(ventana: 12–16 nov 2026; embargo público estricto hasta el 2026-11-18)*
  - *Acción:* Ejecutar el escuadrón completo de 12 agentes sobre Datalaria Pulse (App + Kit ZIP + Lemon Squeezy): (1) **Product Analyst + Monetización:** re-empaquetar `Datalaria_Pulse_Kit.zip` en 3 carpetas numeradas con ambos conectores Power Query (`.csv` Notion + `public.json` Git), `sample_notion_export.csv`, soporte `--format xlsx` en `migrate_notion.py` y Guía Ejecutiva PDF; preparar producto Lemon Squeezy y tarjeta `#pack-pulse` a **19 €** (antes 39 €) **en estado staged/embargado hasta el 2026-11-18** (sin activar `pack-pulse` ni pasar `pulse.yaml` a `live` antes del día 18); (2) **UX/UI + Frontend:** `design.md` de Pulse, navegación `← Datalaria`, detección `?lang=es|en` y `?demo=true`, URLs dinámicas ES/EN, botón `⚡ Probar con CSV de ejemplo (1 clic)` + diagnóstico de conversión, avance rápido de estado en Kanban, limpieza *above-the-fold*, eventos GA4 y capturas reales `pulse-preview-{es,en}.png`; (3) **Seguridad + QA + Release:** auditoría `INV-PULSE-1..5`/RLS, checklist atómico de activación para el **2026-11-18** y registro del **Case Study #1 de Datalaria Helix**.
  - *Gate:* `pytest ops/pulse/tests`, `oxlint` + `npm run build:portal`, `hugo --gc --minify` código 0 (verificando que antes del 18 nov ni `/apps/` ni `/recursos/` exponen Pulse como publicado).
- [ ] **Hito 6.4: Kit Core genérico** *(dic, sem. 1)* — plantillas, 12 agentes en formato agnóstico + adaptadores (Antigravity, Claude Code, Cursor, Codex), 3 blueprints (estático, React + Supabase, Python + FastAPI). *Gate:* `pytest` de estructura y prueba de init en directorio vacío.
- [ ] **Hito 6.5: CLI `helix`** *(dic, sem. 2; Python sin dependencias)*: `init`, `triage`, `new-spec`, `checkpoint`, `verify`, `rollback`, `status`. *Gate:* `pytest` + CI Windows/macOS/Linux.
- [ ] **Hito 6.6: Sandbox Helix Spec Builder (`/apps/helix/`)** *(dic, sem. 3–4)* — React 19 + TS, entrevista ramificada, ZIP en cliente, puntuación de calidad de spec, exportador de prompt, i18n, CTA lista de espera/compra, GA4. *Gate:* `npm run lint`, `npm run build:portal`, `hugo --gc --minify`, firewall `static/`.
- [ ] **Hito 6.7: Caso demo externo de principio a fin** *(ene, sem. 1)* — micro-app real para profesional no dev construida con Helix, con timeline de triajes y gates. *Gate:* gates de la app demo en verde.
- [ ] **Hito 6.8: Empaquetado comercial** *(ene, sem. 2)* — `ops/helix/build_kit.py` (ZIP Starter + Core), productos Lemon Squeezy, `data/apps/helix.yaml`, ficha `/apps/helix/`, `/recursos/`. *Gate:* `pytest`, `build_index`/`publish_public`, `hugo --gc --minify`, checkout de prueba.
- [ ] **Hito 6.9: Lanzamiento Oficial (~2027-01-19)** — serie de 5 posts ES/EN, secuencia Brevo para la lista de espera, LinkedIn. *Gate:* paridad ES/EN, Hugo código 0, enlaces 200.
- [ ] **Hito 6.10: Decisión Pro (condicional, ~marzo 2027)** — medición a +60 días (≥300 emails, ≥50 ventas Core, ≥30 % de demanda) y ADR del modelo Pro.
---

## 📓 REGISTRO DE BLOQUEOS Y ROLLBACKS (AUDIT LOG)

| Fecha | Hito | Incidencia / Motivo | Acción de Rollback / Resolución | Estado |
| :--- | :--- | :--- | :--- | :--- |
| 2026-10-24 | `0.1 - 0.3` | Inicio del sistema SDD | Sin incidencias. Creados archivos base en modo no destructivo. | ✅ Cerrado |
| 2026-10-24 | `Ajuste Plan` | Alineación con las 7 Apps publicadas en `/apps/` y cruce con posts (`draft: false`). | Pospuestos `project-ops` (posts en `draft: true`) y `sop-pipeline` (sin web app) a la Fase 4 (Incubadora). Priorizadas las 7 apps activas empezando por `lifeops`. | ✅ Cerrado |
| 2026-10-24 | `3.1` | Purgado de código inédito y `.git` huérfano en `static/` | Mover `project-ops` y `sop-pipeline` a `apps/_incubadora/`; purgar `.git` en `snake`; 0 violaciones en `static/`. | ✅ Cerrado |
| 2026-10-25 | `3.1-Ext` | Fichas dedicadas, portadas 16:10 y shortcodes `app-ref` para las 4 Apps Legacy | Creados 4 specs, 4 YAMLs, 8 fichas markdown, 8 portadas 16:10 y actualizados 8 posts en ES/EN. 2.091 páginas compilan limpiamente. | ✅ Cerrado |
| 2026-10-25 | `3.2` | Especificación del portal, píldoras por tiers, botones "Leer Post" y Suites B2B | Creado `specs/portal/spec.md`, modificado `app-card.html` y CSS. Verificados 7 enlaces de post y 1 B2B suite en ES/EN con script determinista. Cierre de Fase 3. | ✅ Cerrado |
| 2026-10-28 | `5.0` | Cierre del Plan y Especificación SDD de Datalaria Pulse (`specs/apps/pulse/spec.md`) | Consolidado ADR-012 y creada `spec.md` con modelo de columnas, invariantes `INV-PULSE-1..5` y diseño del Kit Excel + Notion importer. | ✅ Cerrado |
| 2026-10-28 | `5.1` | Modelo de datos Pydantic v2 y Catálogo de Kits (`data/pulse/kits.yaml`) | Creados contratos en `ops/pulse/models.py`, `pytest` 4/4 verde (INV-PULSE-1 e INV-PULSE-2), 14 Kits + 4 Suites catalogados, y desacople total de Notion. | ✅ Cerrado |
| 2026-10-28 | 5.2 | Generador de Índice Editorial uild_index.py sin dependencia de Notion | Indexados 135 activos (109 posts bilingües emparejados, 7 apps, 19 kits/suites). Tests pytest 7/7 pasando. | ✅ Cerrado |
| 2026-10-28 | 5.3 | Sincronización GA4/GSC y compilación de dataset público | Extraídas métricas reales a metrics.json y relativizadas en public.json (base 100, percentiles). pytest 9/9 verde. | ✅ Cerrado |
| 2026-10-28 | 5.4 | Automatización CI/CD y generación de Tracker Excel privado | Pipeline pulse.yml, regla obligatoria en AGENTS.md y generado packages/pulse/Pulse_Private_Tracker.xlsx. pytest 11/11 verde. | ✅ Cerrado |
| 2026-10-28 | `5.5` | App Web Sandbox React 19 + TS con Importador Notion | Vistas Tabla, Kanban, Calendario y Salud Editorial compiladas en static/apps/pulse/. oxlint 0 errores, Hugo código 0. | ✅ Cerrado |
| 2026-10-28 | `5.5-Ext` | Evolución UI/UX, Analytics, Paginación y Calendario Notion | Tipografía Outfit+Inter (LifeOps), filtros pills, ordenación interactiva, paginación (10/25/50), Dashboard Analytics, Kanban 5 columnas y Calendario mensual Notion. oxlint 0 errores, pytest 11/11, Hugo código 0. | ✅ Cerrado |
| 2026-10-28 | `5.5-Ext2` | Dashboard Analytics Ampliado (100% width), 3 Vistas de Taxonomía, Profundidad Léxica y Modales de Apertura Web | Gráficos apilados al 100% (GA4 base 100 y Cadencia histórica), selector de 3 modos (Ecosistema, 4 Temáticas oficiales y Categorías), nuevo gráfico de Profundidad Editorial & Tiempo de Lectura (~18.4h de lectura técnica), chips y tarjetas clicables con modal de detalle y apertura web directa. oxlint 0 errores, pytest 11/11, Hugo código 0. | ✅ Cerrado |
| 2026-10-28 | `5.5-Ext3` | Captura y Edición de Ideas (localStorage), Exportación YAML y Botón de Refresco HTTP | Botón "Refrescar Datos" con bypass de caché HTTP; modal "+ Nueva Idea" y edición completa de campos al pulsar sobre ideas locales; visualización de briefing/notas; persistencia en localStorage y fusión en tiempo real con public.json; exportador a `backlog_ideas.yaml`. oxlint 0 errores, pytest 11/11, Hugo código 0. | ✅ Cerrado |
| 2026-10-28 | `5.6` | Kit Comercial Descargable Datalaria Pulse (Excel + Notion + Escáner + ZIP) | Plantilla Excel con validaciones desplegables y taxonomía, migrador de Notion, Power Query M, escáner universal sin dependencias (pulse_repo_scanner.py), manual GUIA_PULSE_KIT.md y paquete ZIP final. 15/15 tests pytest verde. | ✅ Cerrado |
| 2026-10-29 | `5.7` | Datalaria Pulse Pro (Supabase Cloud + Auth + Modo Demo + Rediseño Visual) | Aislamiento multi-tenant (RLS con demo@datalaria.com sintético y Master Admins enlazados al repo), modal de Auth Supabase, cabecera alineada a 1 fila (ES/EN) y rediseño de jerarquía visual (Macro KPIs con neon borders vs Specific KPIs con icon badges, y View Navigation Deck segmentado flotante). 18/18 tests pytest verde, oxlint 0 errores. | ✅ Cerrado |
| 2026-11-02 | 5.8 | Lanzamiento Editorial Datalaria Pulse (Serie 5 Artículos Bilingües + Ficha App) | Redactados, homologados y verificados los 5 artículos bilingües (10 posts ES/EN) con bloque cover estructurado, taxonomía unificada (ADR-016), precio oficial de lanzamiento de 19 € (antes 39 €), shortcode app-ref en posts 1 a 5, diagramas nativos Mermaid, posicionamiento B2B de Pulse Pro y puente oficial hacia Datalaria Helix. Mantenido el embargo comercial estricto de Pulse hasta el 18 de noviembre (status: incubating, draft: true, sin pack comercial activo). 142 activos consolidados, 115 posts emparejados, 18/18 tests pytest verde y compilación Hugo código 0 (2.279+ páginas). | ✅ Cerrado |
| 2026-10-31 | `Suite 01 Pillar` | Post Pilar Maestro Suite 01 (ES/EN) + Product Cards + Botones Catálogo Recursos + Home Index Card + Cover Safe Zone | **COMPLETADO (100% Verificado ✅):**<br>1. ✅ **Imágenes Compuestas `preview-pack.png` (1600×980 px):** Capturas reales de los 5 packs en `content/{es,en}/posts/.../preview-pack.png` y `static/images/recursos/suite-01-preview-{es,en}.png`.<br>2. ✅ **Portadas `cover.png` con Safe Zone [145px, 1055px]:** Regeneradas con `generate_cover.py` enmarcando perfectamente título, viñetas, badges y pentagrama geométrico, eliminando recortes visuales.<br>3. ✅ **Alineación de Títulos de Herramientas:** Reemplazados los bloques de código delimitados (`===`) por encabezados Markdown `###` con iconos (`🌐 Herramienta 1`, `🛡️ Herramienta 2`, `🎯 Herramienta 3`, `⭐ Herramienta 4`, `🧭 Herramienta 5`), normalizando la jerarquía visual y la TOC editorial.<br>4. ✅ **Diagramas Mermaid & Cero Bloques ASCII:** Sustituido el diagrama ASCII de flujo intermatricial de la sección 4 por un diagrama nativo vectorial `{{< mermaid >}} flowchart TD {{< /mermaid >}}` (sin desbordamiento ni barras de scroll) y convertida la caja ASCII de la sección 5 en un encabezado H3 ejecutivo (`### 🚀 Recorrido Secuencial...`). Cero bloques de código monospaciados accidentales.<br>5. ✅ **Resolución de Shortcodes & SVGs:** Subsanado el dimensionamiento de los SVG en `bundle-card.html` (`width="16" height="16"` y CSS específico) y eliminada la duplicación redundante de tarjetas en Sección 6, cerrando de forma limpia con la `product-card` visual completa.<br>6. ✅ **UI Catálogo Recursos (`recursos_catalog.html` & `recursos.css`):** Mini tarjetas de suite y banner contextual (`setTopic`) con layout responsivo, comprobación de estado corregida (`suite.status === 'available'`) y botonera activa `[Detalles ℹ️]` (`openModal('suite-01')`), `[Artículo técnico 📖]` y `[Descargar →]`, eliminando el falso estado 'Próximamente'.<br>7. ✅ **Sección Recursos del Home (`index_profile.html` & `home-portal.css`):** Reemplazada la tarjeta de DAFO por la tarjeta de la **Suite 1: Estrategia MBA (19€)** con triple enlace: botón principal de `Descarga` a Lemon Squeezy (`dlh-btn-pack-dl`), y subfila dual con `[Detalles ℹ️]` (enlace ancla a `/recursos/#suite-01`) y `[Artículo técnico 📖]` (al post pilar maestro).<br>8. ✅ **Gobernanza Pulse & Build Hugo:** Catálogo `data/pulse/kits.yaml` sincronizado. Verificados `build_index` y `publish_public` (141 activos, 114 posts bilingües, 117 publicados), `verify_all.py` OK y `hugo --renderToMemory` (2.221 páginas, código 0). | ✅ Cerrado |
| 2026-10-31 | `Semana 29: Her` | Publicación de artículos bilingües sobre 'Her' (Spike Jonze) y Agentes IA con SDD | **COMPLETADO (100% Verificado ✅):**<br>1. ✅ **Posts Bilingües 'Her' (Semana 29 - 2026-12-27):** `content/es/posts/her/` y `content/en/posts/her/` creados (>3.000 palabras c/u), portada oficial `cover.jpg`, fotograma cinemático `theodore_skyline.jpg` e infografía conceptual `cognitive_divergence_her.jpg`. Tráilers oficiales de YouTube incrustados (`6k3iXk5wKkg` en ES / `ne6p6MfLBxc` en EN).<br>2. ✅ **Posts Previos SDD Agentes (2026-11-17):** `content/es/posts/agentes_ia_operativa_sdd/` y versión EN creados con portada e infografía de arquitectura agéntica.<br>3. ✅ **Gobernanza Editorial Datalaria Pulse:** Ejecutados `build_index` y `publish_public` emparejando 114 posts con 100% paridad ES/EN (141 activos consolidados). Invariantes `INV-PULSE-1` e `INV-PULSE-2` verificadas. | ✅ Cerrado |
| 2026-10-31 | `Suite 01 Individual Tools Assets` | Alineación de Modales "Detalles" y Portadas `cover:` en los 5 Packs de la Suite 01 (ES/EN) | **COMPLETADO (100% Verificado ✅):**<br>1. ✅ **Modales "Detalles" (`layouts/partials/recursos_catalog.html`):** Actualizados `previewImg` en `KITS_DATA` para las 5 herramientas individuales (`pack-dafo`, `pack-porter`, `pack-pestel`, `pack-bcg`, `pack-mckinsey`) en español e inglés, enlazando directamente a las capturas de alta definición de los entregables reales (`/images/recursos/*-preview-es.png` y `*-preview-en.png`), análogo al Mega Bundle.<br>2. ✅ **Portadas de Artículos (`cover:` Frontmatter):** Añadido el bloque `cover: { image: "cover.png", alt: "...", caption: "...", relative: true }` en el frontmatter YAML de los 10 artículos (5 en español y 5 en inglés), activando la renderización de la cabecera hero ejecutiva en PaperMod y las miniaturas en las tarjetas del blog.<br>3. ✅ **Gobernanza & Compilación:** Ejecutados `build_index` y `publish_public` (141 activos, 114 posts bilingües, 117 publicados). Verificación completa de enlaces y compilación con `hugo --renderToMemory` (2.221 páginas, 0 errores, código de salida 0). | ✅ Cerrado |
| 2026-11-01 | `6.x Plan` | Planificación estratégica de Datalaria Helix (Kit SDD, escuadrón de 12 roles con Orquestador y UX/UI, Sandbox A+B, calendario 4/11 nov y lanzamiento enero 2027) | Registrado ADR-017 y añadida FASE 6 (Hitos 6.0–6.9) al ROADMAP. Solo documentación en `/specs/`; cero cambios en código. | ✅ Cerrado |
| 2026-11-01 | `Suite 02 Pack DAR Articles & Catalog` | Publicación de artículos técnicos bilingües de la Matriz DAR, activación de botones en el catálogo, capturas REALES de los entregables (Excel, PPTX y PDF) y resolución de diagrama Mermaid | **COMPLETADO (100% Verificado ✅):**<br>1. ✅ **Capítulo 1 Bilingüe:** Incorporado el nuevo capítulo introductorio sobre qué es la Matriz DAR (CMMI DAR & Kepner-Tregoe), sus componentes (*Must-Haves* vs. *Wants*), erradicación del sesgo cognitivo/HiPPO y entregables esperados.<br>2. ✅ **Interconexión con Suite 01 Estrategia:** Añadido diagrama de embudo intermatricial (Nivel 1 a 5) y enlaces directos a DAFO, PESTEL, Porter, BCG, McKinsey y al Kit de Estrategia Corporativa MBA.<br>3. ✅ **Corrección Diagrama Mermaid:** Reparado el error de sintaxis en Mermaid 10.9.8 (eliminación de operadores `&` en etiquetas, llaves conflictivas con paréntesis y simplificación de aristas) en ES y EN.<br>4. ✅ **Capturas Reales de Alta Definición (1600x980 px):** Sustituidos los mockups simulados por capturas 100% auténticas de los entregables del pack en `static/images/recursos/dar-preview-{es,en}.png` y `content/{es,en}/posts/.../preview-pack.png`:<br>   - *Excel .xlsx:* Captura real del Dashboard Ejecutivo horizontal A4 con tabla de 5 alternativas, 3 tarjetas KPI (Vendor Beta 88.5, Gap +9.0 pts, 4/5 Aptas) y desglose de 4 pilares.<br>   - *PDF .pdf:* Capturas PyMuPDF en 200 DPI de las Páginas 1 y 2 (Encuadre directivo y formulación matemática formal CMMI DAR con $V_k$, $S_k$ e invarianza).<br>   - *PowerPoint .pptx:* Captura nativa 1920x1080 de la Diapositiva 3 (Roadmap Q1-Q4, Board Decision Gateway y 4 bloques de firmas digitales CEO, CFO, CIO, CPO).<br>   - *Cero Glifos Rotos (□):* Iconografía vectorial pura (sparkles ejecutivos y flechas de descarga) eliminando cualquier tofu tipográfico.<br>5. ✅ **Product Cards Integradas:** Añadida la tarjeta superior compacta y configurada la imagen `preview-pack.png` con pie descriptivo en la tarjeta inferior en ambos idiomas.<br>6. ✅ **Habilitación "Artículo técnico" en Catálogo:** Sustituido el botón deshabilitado por el enlace activo en `recursos_catalog.html`, `content/es/recursos/_index.md`, `content/en/resources/_index.md` y `scripts/generate_recursos_pages.py`.<br>7. ✅ **Configuración Modal "Detalles":** Asignadas las imágenes `dar-preview-{es,en}.png` al modal y preservado `DAR.png` como icono cuadrado.<br>8. ✅ **Empaquetado & Gobernanza Pulse & Build Hugo:** Regenerados los libros Excel horizontales y el paquete maestro `Executive_Decision_Pack_DAR_Dual.zip` (275 KB) en `packages/Suite_02_Toma_Decisiones/01_Matriz_DAR_Cuantitativa/` y sincronizado en `packages/00_DISTRIBUCION_LEMONSQUEEZY/`. Ejecutados `python -m ops.pulse.build_index` y `publish_public` (141 activos, 114 posts bilingües). Hugo `--renderToMemory` verificado (2.241 páginas, código de salida 0). | ✅ Cerrado |
