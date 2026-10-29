# Registro de Decisiones de Arquitectura (ADR Log — Datalaria SDD)

> **Propósito:** Mantener la memoria histórica de **por qué** se tomaron las decisiones clave de arquitectura en Datalaria. Esto evita que en futuras sesiones un humano o un agente de IA proponga revertir patrones ya evaluados y descartados.

---

## ADR-001: Adopción de Spec-Driven Development (SDD) Agnóstico del Modelo
- **Fecha:** 2026-10-24
- **Estado:** Aceptado
- **Contexto:** La plataforma Datalaria se desarrolla utilizando múltiples asistentes agénticos de vanguardia (principalmente Google Antigravity con Gemini 4 Argon y agentes basados en Claude). El crecimiento orgánico previo generó código heterogéneo sin una fuente única de verdad.
- **Decisión:** Adoptar una arquitectura estricta **Spec-First** centralizada en `/specs/`, con [`AGENTS.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/AGENTS.md) como punto de entrada universal y [`CLAUDE.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/CLAUDE.md) como puntero ligero. Ningún código de producción se modifica sin actualizar antes su `spec.md`.
- **Consecuencias:** Coherencia total entre sesiones y entre distintos modelos de IA; reducción drástica de regresiones y alucinaciones arquitectónicas.

---

## ADR-002: Expulsión del Código Fuente Backend fuera de `/static/`
- **Fecha:** 2026-10-24
- **Estado:** En ejecución (Completado para LifeOps e Hito 2.1 Obs-Management; pendiente cuarentena Fase 3)
- **Contexto:** Durante la auditoría inicial ([`00-ecosystem-audit.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/audit/00-ecosystem-audit.md)) se detectó que proyectos backend en Python (`project-ops`, `sop-pipeline`, `obs-management`), junto con esquemas `.sql` y archivos `.env`, residían dentro de `static/apps/`. Hugo copia todo el contenido de `static/` al directorio público `public/`.
- **Decisión:** Mover todo código fuente de aplicaciones a un directorio raíz `/apps/<app-slug>/`. El directorio `/static/apps/` queda restringido exclusivamente a artefactos frontend compilados (`dist/`) y activos estáticos puros.
- **Consecuencias:** Eliminación del riesgo de filtración de código propietario y credenciales en despliegues de Netlify; separación limpia entre código fuente y artefactos de distribución.

---

## ADR-003: Patrón de Monetización y Ejecución "Dual-Mode" (Executive Sandbox + Live Engine)
- **Fecha:** 2026-10-24
- **Estado:** Aceptado
- **Contexto:** Algunas aplicaciones B2B (como `obs-management`) apuntaban a `http://localhost:8001` en su HTML estático, mostrando un error `OFFLINE` a los visitantes reales de `datalaria.com`. Además, mantener múltiples servidores backend encendidos 24/7 para tráfico exploratorio es costoso, pero las apps necesitan demostrar valor inmediato para vender los *Executive Decision Packs* de Lemon Squeezy.
- **Decisión:** Todas las aplicaciones B2B implementarán dos modos:
  1. **Modo Sandbox (Por defecto en web pública):** Funciona 100% en el navegador sin requerir backend activo ni login, utilizando datos ejecutivos pre-calculados o motores deterministas ligeros en cliente, e integrando un banner contextual de compra del *Executive Pack* en Lemon Squeezy.
  2. **Modo Live Engine / Pro:** Conecta con el backend FastAPI + Supabase + IA Agéntica cuando el usuario se autentica o conecta su entorno.
- **Consecuencias:** Cero pantallas rotas en producción, latencia cero para visitantes del blog, coste de infraestructura controlado y embudo de conversión directo hacia Lemon Squeezy.

---

## ADR-004: Consolidación de Persistencia en un Único Proyecto Supabase Multi-Esquema
- **Fecha:** 2026-10-24
- **Estado:** Aceptado
- **Contexto:** Existían referencias a múltiples proyectos de Supabase distintos (`wkbmxekmofrjtcsyytrv` en LifeOps, `wxwnbzmbzztegcdzrxbg` en Neon Snake, e instancias por `.env` en las demás apps).
- **Decisión:** Consolidar todas las aplicaciones en un único cluster Supabase (`datalaria-core`), aislando los dominios mediante esquemas de PostgreSQL (`lifeops`, `pmo_analytics`, `sop_engine`, `obs_radar`, `arcade`) con políticas RLS estrictas.
- **Consecuencias:** SSO unificado para el usuario en todas las apps de Datalaria, administración centralizada de backups/secretos y prevención de pausas por inactividad en planes gratuitos dispersos.

---

## ADR-005: Congelación ("Feature Freeze") de Micro-Apps Legacy
- **Fecha:** 2026-10-24
- **Estado:** Aceptado
- **Contexto:** Las utilidades iniciales (`conversor`, `maths`, `flashcards`, `snake`) están construidas con HTML duplicado por idioma (`/es/`, `/en/`) y Tailwind por CDN. Su valor de negocio B2B es nulo o marginal frente al esfuerzo de migrarlas a SDD.
- **Decisión:** Clasificarlas como **No Migrables (Frozen Legacy)**. Se mantienen sus rutas estáticas para no romper enlaces entrantes ni SEO histórico, pero se reubican visualmente en una sección secundaria (*"Open Lab & Arcade"*) dentro de `/apps/`, reservando la cabecera del catálogo para las Suites Ejecutivas y Operativas.
- **Consecuencias:** Foco del 100% de la capacidad de ingeniería en activos monetizables B2B y mejora sustancial de la percepción de marca C-Level.

---

## ADR-006: Sincronización Estricta entre Publicación Editorial y Catálogo de Apps (`Post ⇔ App`)
- **Fecha:** 2026-10-24
- **Estado:** Aceptado
- **Contexto:** Al cruzar las carpetas de `/static/apps/` con los artículos de `/content/*/posts/`, se comprobó que existen exactamente **7 aplicaciones publicadas en la web** (`lifeops`, `obs-management`, `snake`, `weather`, `flashcards`, `conversor`, `maths`), todas respaldadas por artículos con `draft: false`. En cambio, `project-ops` tiene sus artículos en borrador (`draft: true`) y `sop-pipeline` solo enlazaba a un Google Colab externo, pero sus archivos `.py` y `.env` estaban alojados dentro de `static/apps/`.
- **Decisión:**
  1. **Prioridad Exclusiva en las 7 Apps Activas:** Ejecutar todo el ciclo de consolidación SDD primero sobre las 7 aplicaciones que hoy están publicitadas en la web (empezando por `lifeops`, `obs-management` y `weather`, y congelando `snake`, `flashcards`, `conversor` y `maths`).
  2. **Cuarentena de Incubación para Apps Inéditas:** `project-ops` y `sop-pipeline` no se migran ni se publican ahora; únicamente se retiran sus archivos Python/SQL/env de `static/apps/` por higiene de seguridad y pasan a la **Fase 4 (Incubadora de Nuevos Lanzamientos)** para ser revisadas, validadas y estrenadas bajo SDD cuando se publiquen sus posts.
- **Consecuencias:** Cero trabajo prematuro sobre apps aún no validadas funcionalmente por el autor, eliminación inmediata de código inédito expuesto en `/static/` y alineación total entre el blog editorial y el catálogo de aplicaciones.

---

## ADR-007: Fichas de App Data-Driven con Historial Evolutivo (`apps-showcase`)
- **Fecha:** 2026-10-24
- **Estado:** Implementado (Completado en Hitos 1.3, 1.4, 2.1 y 2.2)
- **Contexto:** El listado `/apps/` actual es HTML embebido en `content/*/apps/_index.md` con tarjetas de solo icono y texto, duplicado por idioma. No existe un lugar donde el usuario vea objetivos, diseño, tecnologías ni la evolución de cada App, y los posts enlazan directamente a la App sin contexto.
- **Decisión:**
  1. Una **ficha por App** en `/{lang}/apps/<slug>/` (page bundle Hugo) con layout común `layouts/apps/single.html`.
  2. **Metadatos en `data/apps/<slug>.yaml`** (bilingüe en un único fichero) como fuente única para ficha, tarjeta y shortcode de posts.
  3. **Tarjetas visuales con captura** en el listado, agrupadas por `tier` (flagship / b2b / lab).
  4. **Shortcode `app-ref`** en los posts de referencia para enlazar a la ficha.
  5. **Validación en build** (campos obligatorios, posts existentes, versión coherente).
- **Alternativas descartadas:**
  - *Front matter por idioma en cada `index.md`:* duplicaría el changelog y las tecnologías en ES y EN → desincronización garantizada.
  - *Generar las fichas desde `spec.md`:* acopla documentación de ingeniería (con deuda y riesgos internos) a contenido público.
  - *Página única con todas las Apps en acordeón:* peor SEO y sin URL compartible por App.
- **Consecuencias:** Añadir una App nueva = 1 YAML + 2 `index.md` + 1 captura. El changelog público se mantiene en paralelo a la spec (regla de Constitución Art. 8.3).

---

## ADR-008: Despliegue Híbrido Serverless con Proxy Netlify para Apps de ETL Continuo (`weather`)
- **Fecha:** 2026-10-24
- **Estado:** Aceptado
- **Contexto:** El Dashboard Climático (`weather`) ingesta telemetría 3 veces al día de más de 160 ciudades y reentrena modelos de Machine Learning. Alojar el dataset vivo dentro del repositorio de Datalaria saturaría Git con decenas de miles de commits automáticos de actualización de CSVs.
- **Decisión:**
  1. Mantener la ejecución continua desatendida en el repositorio upstream `https://github.com/Dalaez/app_weather.git` mediante GitHub Actions y despliegue a Netlify (`datalaria-app-weather.netlify.app`).
  2. Servir la aplicación a los usuarios finales transparentemente bajo el dominio de Datalaria mediante la regla de proxy forzado `200!` en `static/_redirects` (`/apps/weather/* https://datalaria-app-weather.netlify.app/:splat 200!`).
  3. Consolidar el código fuente canónico, scripts de recolección y especificación SDD en [`apps/weather/`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/apps/weather) y [`specs/apps/weather/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/weather/spec.md).
- **Consecuencias:** Cero ruido de commits en el blog principal, 100% serverless con coste $0/mes y preservación transparente de la URL pública canónica `https://datalaria.com/apps/weather/`.

---

## ADR-009: Cuarentena de Código Inédito en `apps/_incubadora/` y Congelación de Apps Legacy (#4 a #7)
- **Fecha:** 2026-10-24
- **Estado:** Aceptado e Implementado
- **Contexto:**
  1. Durante la auditoría del árbol de archivos, se identificó que `project-ops` y `sop-pipeline` contenían código backend Python, migraciones SQL, muestras de datos y archivos de variables de entorno `.env` alojados indebidamente en `static/apps/`. Al estar sus artículos de blog en borrador (`draft: true`) o referenciados a notebooks externos, exponerlos en `static/` violaba el Artículo 2 de la Constitución de Ingeniería (Firewall de Directorios).
  2. Las 4 aplicaciones legacy secundarias (`snake` en `/games/snake/`, `flashcards` en `/apps/flashcards/`, `conversor` en `/apps/conversor/`, `maths` en `/apps/maths/`) se encuentran 100% publicadas y referenciadas en artículos activos (`draft: false`), pero son aplicaciones puramente frontend sin dependencias backend. Además, `snake` contenía un subdirectorio `.git` huérfano.
- **Decisión:**
  1. **Cuarentena No Destructiva:** Mover íntegramente `static/apps/project-ops/` y `static/apps/sop-pipeline/` hacia [`apps/_incubadora/`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/apps/_incubadora/) preservando toda su lógica original, dotándolas de `.gitignore` independientes para blindar sus `.env` y muestras de datos, a la espera de la Fase 4.
  2. **Purga de Metadatos y Firewall Estricto:** Eliminar el subdirectorio `.git` de `static/games/snake/` y purgar todos los restos de `__pycache__` en `static/`.
  3. **Congelación de Apps Legacy:** Mantener las 4 apps estáticas en sus rutas canónicas intactas en `static/` (`/games/snake/`, `/apps/flashcards/`, `/apps/conversor/`, `/apps/maths/`).
- **Consecuencias:**
  - Cumplimiento absoluto del Firewall de Directorios: cero archivos `.py`, `.sql`, `.env`, `.pyc` ni `.git` en todo el árbol de `static/` ni en `public/`.
  - Preparación limpia de la base para el Hito 3.2 (Reorganización Visual del Escaparate de Apps).

---

## ADR-010: Fichas Data-Driven, Portadas 16:10 y Estandarización de las 4 Apps Legacy (#4 a #7)
- **Fecha:** 2026-10-25
- **Estado:** Aceptado e Implementado
- **Contexto:** Las 4 aplicaciones secundarias de laboratorio (`snake`, `flashcards`, `conversor`, `maths`) carecían de páginas de ficha técnica dedicadas (`/{lang}/apps/<slug>/`), apoyándose únicamente en un fallback en `layouts/apps/list.html` sin soporte para portadas visuales, objetivos, diagramas de arquitectura ni historial de versiones SemVer. Además, sus artículos en el blog no contaban con el shortcode interactivo `app-ref`.
- **Decisión:**
  1. **Estandarización Data-Driven Completa:** Crear `data/apps/<slug>.yaml`, `specs/apps/<slug>/spec.md` y bundles `content/{es,en}/apps/<slug>/index.md` para las 4 apps legacy, documentando objetivos, diagramas Mermaid, stack técnico y changelogs SemVer que explican su estado final congelado.
  2. **Portadas Nativas 16:10 (1280x800):** Generar portadas optimizadas en relación 16:10 para cada app (`cover.png`) que se adaptan a las tarjetas del catálogo (`.Fill "800x500"`) y a los encabezados Hero (`.Resize "1200x"`) sin recortes accidentales ni barras negras.
  3. **Bidireccionalidad Blog ⇔ App (Constitución Art. 7):** Insertar el shortcode `{{< app-ref slug="..." >}}` y enlaces a la ficha técnica en los 8 artículos de referencia (ES y EN).
- **Consecuencias:**
  - Catálogo 100% data-driven: las 7 aplicaciones activas cuentan con el mismo estándar de calidad documental y visual.
  - Cero discrepancias o campos vacíos en compilación; 2.091 páginas generadas con código 0.

---

## ADR-011: Reorganización Visual del Escaparate de Apps, Botones Multi-Acción y Conexión B2B
- **Fecha:** 2026-10-25
- **Estado:** Aceptado e Implementado (Cierre de la Fase 3)
- **Contexto:**
  1. Con las 7 aplicaciones formalizadas bajo fichas data-driven, el listado `/apps/` requería una jerarquización visual clara y componentes interactivos completos.
  2. Anteriormente, las tarjetas solo ofrecían el enlace a la Ficha o a la App en vivo, pero los usuarios no contaban con un botón directo para acceder al artículo técnico publicado (como hacía originalmente `Neon Snake`).
  3. La aplicación B2B (`obs-management`) no destacaba visualmente su vinculación comercial con los recursos ejecutivos de Lemon Squeezy en el catálogo.
- **Decisión:**
  1. **Especificación Canónica del Portal:** Consolidar [`specs/portal/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/portal/spec.md) gobernando los tiers (`flagship`, `b2b`, `lab`), el contrato de datos y las reglas de diseño.
  2. **Botón Universal "Leer Post / Read Post":** Modificar `layouts/partials/app-card.html` para resolver automáticamente el artículo publicado principal de cada app en el idioma activo (ES/EN) y renderizar un botón secundario estilizado.
  3. **Conexión Directa con Suites B2B:** Integrar en las tarjetas de tier `b2b` el botón `"Suite B2B ⚡"` enlazando a `/es/recursos/` o `/en/resources/`, junto con un badge y nota ejecutiva.
  4. **Píldoras de Navegación por Tiers:** Incorporar en la cabecera de `content/{es,en}/apps/_index.md` anclas directas (`#tier-flagship`, `#tier-b2b`, `#tier-lab`) para una exploración instantánea.
- **Consecuencias:**
  - Experiencia de usuario premium: navegación fluida en 1 clic entre Ficha técnica, App en vivo, Tutorial del blog y Suite B2B.
  - 100% verificado determinísticamente mediante tests automatizados sobre el HTML compilado en ES y EN.
  - Fase 3 cerrada formalmente con cero deuda técnica.

---

## ADR-012: Nueva App de nicho "Datalaria Pulse" (Content Ops as Code) para sustituir la gestión editorial en Notion
- **Fecha:** 2026-10-25 (Consolidado el 2026-10-28)
- **Estado:** Aceptado — Especificación aprobada en [`specs/apps/pulse/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/pulse/spec.md) (Hito 5.0 cerrado)
- **Contexto:**
  1. La gestión editorial (posts, apps, kits) se hace a mano en Notion: 95 filas con ES/EN mezclados frente a 108 posts por idioma en el repo, sin vínculo ES⇔EN y con 6 columnas siempre vacías.
  2. Casi todos esos datos ya existen en el front matter de Hugo, en `git log` y en `data/analytics.json` (GA4).
  3. Se evaluaron tres opciones: (1) sección pública del blog, (2) funcionalidad dentro de LifeOps y (3) una App nueva con Supabase.
- **Decisión:**
  1. **Opción 3, con enfoque de nicho "Content Ops as Code"**: el repo es la fuente de verdad y un generador automático (`ops/content_index/`) produce el índice editorial en cada push y con un cron diario.
  2. **La Opción 1 se absorbe como Sandbox (Art. 3):** muestra lo publicado, lo programado y las ideas marcadas como `visibility: public`.
  3. **Las ideas prospectivas** viven en `data/editorial/backlog.yaml` con `visibility: private`: no se publican ni se cargan en Supabase.
  4. **La Opción 2 se descarta:** se reutilizan patrones de código de LifeOps sin modificar LifeOps, para no diluir su producto.
  5. **Ronda 2 (2026-10-25):** nombre **Datalaria Pulse** (slug `pulse`) · público B2B prioritario (equipos de documentación, SEO y marketing de empresas, y medios digitales) con dos formas de importar contenido (repo Git + `sitemap.xml`) · primer producto de pago: **Kit de pago único**; Pro/Team alojado más adelante con Lemon Squeezy Subscriptions · métricas iniciales: **GA4 + Search Console**; las ventas de Lemon Squeezy quedan fuera hasta que existan y nunca serán visibles en el Sandbox público.
  6. **Ronda 3 (2026-10-25):** el Sandbox público muestra métricas reales **relativas** (percentil, tendencia, índice base 100; nunca valores absolutos). **La suscripción Pro/Team y el modo Supabase quedan aparcados** hasta medir la respuesta de la serie, la App y el Kit (Hito 5.8). La v1 no tiene backend: monetización solo con el Kit (plantilla Excel rellenable o importando el export de Notion).
  7. **Orden:** spec y ADR → revisión de columnas → generador → automatización → app web → Pro con Supabase → lanzamiento editorial.
- **Consecuencias:**
  - Se elimina la doble entrada de datos; la paridad ES/EN y las métricas GA4 pasan a ser automáticas.
  - Hará falta enmendar el Art. 4 de la Constitución para añadir el esquema `content_ops` (Hito 5.5).
  - La App solo se listará en `/apps/` cuando tenga su serie de posts publicada (Art. 7).

---

## ADR-013: Motor Analítico 360° Nativo en React + Recharts con Agregación en Memoria vs. Herramienta BI Externa (Grafana / Metabase)
- **Fecha:** 2026-10-27
- **Estado:** Aceptado (Implementado en Hito 1.5 — LifeOps `v1.1.0`)
- **Contexto:**
  1. El Dashboard 360° de LifeOps (`v1.0.1`) solo mostraba conteos globales de la tabla padre `activities` y un gráfico estático de los últimos 30 días, sin permitir filtrar por semana/mes/año, comparar contra el periodo anterior ($\Delta\%$), ni profundizar por subcategorías (ej. `running` dentro de `sport`) o métricas cuantitativas (`distance_km`, `calories`, `duration_seconds`, `pages_read`).
  2. Se evaluaron dos caminos tecnológicos: (A) construir el motor analítico de forma nativa en React 19 + Recharts (ya instalado en `package.json`) filtrando en memoria sobre el dataset con detalles (`GET /api/v1/activities/details`), o (B) embeber un panel externo tipo Grafana Cloud / Metabase / Apache Superset.
- **Decisión:**
  1. **Adoptar la Opción A (Panel Analítico Nativo en React 19 + Recharts `v3.10.1` + Motor Determinista en Cliente `analyticsEngine.js`).**
  2. **Descartar Grafana / Metabase embebido** porque:
     - Rompe el aislamiento multi-usuario RLS basado en el JWT de sesión de Supabase Auth salvo licencias Enterprise o proxies de tokens.
     - Rompe el invariante de coste 0 €/mes y el modo Sandbox (`?mock=true`, Constitución Art. 3), ya que un iframe externo no puede leer el estado simulado del navegador.
     - Penaliza la experiencia móvil táctil y la estética uniforme *Dark Glassmorphism*.
  3. **Integración directa en la vista principal del Dashboard 360°** con 4 bloques visuales: (1) Tarjetas KPI dinámicas con variación $\Delta\%$, (2) Gráfico de evolución temporal multimétrica (Barras + Línea/Área comparativa), (3) Gráfico Donut de distribución por subcategorías y (4) Mapa de calor de consistencia diaria estilo GitHub/Strava.
- **Consecuencias:**
  - Cero coste adicional de infraestructura y 0 KB de nuevas librerías de terceros en el bundle.
  - Filtrado instantáneo (0 ms de latencia entre clics de filtro) tanto en modo autenticado como en modo Demo (`?mock=true`).

---

## ADR-014: Guardia de Seguridad para Carga de Datos Sintéticos y Aislamiento Estricto de Cuentas de Producción (INV-11)
- **Fecha:** 2026-10-28
- **Estado:** Aceptado (Implementado en Hito 1.7 — LifeOps `v1.1.2`)
- **Contexto:**
  1. Durante la generación de capturas pobladas para la Parte 6 de la serie LifeOps, un script de seeding insertó actividades y tareas sintéticas tanto en la cuenta de prueba (`datalaria@gmail.com`) como inadvertidamente en la cuenta real de producción (`dalaez1@gmail.com`).
  2. Aunque el backend utiliza PostgreSQL con RLS y el schema `lifeops` separa los datos por `user_id`, los scripts de seeding y benchmarking que operan con `service_role` pueden saltarse RLS si no cuentan con una barrera de seguridad a nivel de aplicación que impida escribir en cuentas de usuario reales.
- **Decisión:**
  1. **Instituir la Invariante INV-11 (Seeder Guard & Anti-Contaminación de Datos):**
     - Crear el servicio [`seeder_guard.py`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/apps/lifeops/api/services/seeder_guard.py) con listas blancas explícitas de cuentas demo autorizadas (`ALLOWED_DEMO_EMAILS`, `ALLOWED_DEMO_UIDS`) y lista de protección para cuentas reales (`PROTECTED_REAL_EMAILS`).
     - Función `validate_synthetic_seed_target(user_id, email)` que arroja de inmediato `SeederProtectionError` ante cualquier intento de cargar datos en cuentas de producción o no autorizadas.
     - Función `detect_synthetic_leakage` para escanear registros contra firmas sintéticas conocidas.
  2. **Integrar verificación automática en la suite de pruebas (`pytest`):**
     - Implementar [`test_data_isolation.py`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/apps/lifeops/api/tests/test_data_isolation.py) con tests deterministas para:
       - Bloqueo inmediato de seeding ante cuentas reales (`dalaez1@gmail.com`).
       - Bloqueo de usuarios no registrados en la lista blanca.
       - Aprobación exclusiva de cuentas demo autorizadas (`datalaria@gmail.com`).
       - Detección precisa de firmas sintéticas sin falsos positivos en datos de usuarios reales.
       - Verificación de aislamiento estricto por `user_id` en las consultas de los routers de la API.
       - Auditoría de la base de datos para certificar cero presencia de datos sintéticos en cuentas de producción.
- **Consecuencias:**
  - Imposibilidad de que futuros scripts de prueba, benchmarking o captura de marketing contaminen cuentas de usuarios reales.
  - La suite de CI/CD `pytest` falla de forma automática si un script o test intenta mutar cuentas no autorizadas o si se detecta fuga de datos sintéticos.
