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


---

## ADR-015: Evolución de Datalaria Pulse a Arquitectura Dual-Mode con Supabase (`pulse` schema) para Sincronización Web ↔ Localhost y Acceso Multi-Usuario Demo
- **Fecha:** 2026-10-29
- **Estado:** Aceptado (Planificado para Hito 5.8)
- **Contexto:**
  1. En los Hitos 5.5 y 5.6 se consolidó Datalaria Pulse como una SPA estática impulsada por Git y `public.json`, complementada con captura de ideas locales en `localStorage`.
  2. Aunque este modelo cumple con excelencia la premisa de no depender de Notion y permitir auditar el repositorio localmente, introduce una barrera operativa: las modificaciones de ideas o reprogramaciones de fechas realizadas en la web en producción (móvil, tablet, portátil) no se sincronizan en tiempo real con el entorno de desarrollo local (localhost) sin pasar por exportaciones manuales YAML y commits de Git.
  3. Asimismo, los visitantes de la web que desean probar la herramienta de forma continuada requieren persistencia multi-dispositivo sin alterar el repositorio maestro.
- **Decisión:**
  1. **Evolucionar Datalaria Pulse al Patrón Dual-Mode con Supabase en la Fase Pro (Hito 5.8):**
     - Crear el esquema PostgreSQL dedicado `pulse` dentro del cluster principal `datalaria-core` (Constitución Art. 4).
     - Desplegar las tablas `pulse.ideas` y `pulse.content_schedule` con Row-Level Security (`auth.uid() = user_id`) y soporte de Supabase Auth (reutilizando la infraestructura ya existente en LifeOps).
     - **Modo 1 (Sandbox Público Inmediato):** Opera por defecto sin login leyendo `public.json` y persistiendo ideas temporales en `localStorage` (Constitución Art. 3).
     - **Modo 2 (Pro Cloud Autenticado):** Conexión en tiempo real con Supabase. Cualquier idea, nota o reprogramación guardada en la web se sincroniza al instante con localhost al pulsar "Refrescar Datos", y viceversa.
  2. **Estrategia Editorial de Lanzamiento (Hito 5.7):**
     - Los 5 artículos técnicos se centran en la metodología base, el Kit descargable y las herramientas sin código (Power Query M, Python puro), garantizando una adopción accesible y masiva.
     - Cada uno de los 5 artículos concluye con un **apartado final de cierre** destacando las capacidades de la versión Pro, la demo interactiva en la web y los servicios de consultoría técnica corporativa a medida de Datalaria.
- **Consecuencias:**
  - Plena paridad arquitectónica entre LifeOps y Pulse.
  - Sincronización instantánea Web ↔ Localhost en cuanto se active la sesión.
  - Embudo de monetización escalonado: Kit Básico ($39-$49) ➔ Demo Interactiva Web ➔ Contratos de Consultoría y Despliegue Pro.


---

## ADR-016: Reestructuración de la Taxonomía Editorial en 5 Pilares con Blindaje SEO
- **Fecha:** 2026-10-31
- **Estado:** Aceptado
- **Contexto:**
  1. La home de Datalaria agrupaba los artículos en 4 categorías: `Artículos Técnicos` (52), `Proyectos Tech` (37), `Startups` (13) y `Biografías` (12).
  2. Esta estructura presentaba dos fricciones: diluía los artículos culturales (cine, series, libros como *Her* o *Halt and Catch Fire*) dentro de artículos técnicos, y fragmentaba las series de desarrollo de software (*Pulse* en técnicos vs. *LifeOps* en proyectos). Además, los 20 artículos cuantitativos clave para la venta de *Executive Decision Packs* carecían de visibilidad agrupada.
  3. Cualquier cambio en taxonomías de Hugo conlleva el riesgo de romper páginas `/categories/` o `/tags/` previamente indexadas por motores de búsqueda si se eliminan destructivamente.
- **Decisión:**
  1. Evolucionar la categorización a **5 Pilares Editoriales**:
     - `IA, Ingeniería y Proyectos` (`AI, Engineering & Projects`): Fusión de proyectos y artículos de desarrollo/IA.
     - `Estrategia y Operaciones` (`Strategy & Operations`): Modelos cuantitativos, PMO, finanzas y embudo B2B.
     - `Startups` (`Startups`): Casos de éxito y escalado empresarial.
     - `Pioneros y Referentes` (`Pioneers & Icons`): Evolución de «Biografías» hacia pensamiento epistemológico y científico.
     - `Cultura Tech y Media` (`Tech Culture & Media`): Cine, series, literatura técnica y contenidos digitales.
  2. **Blindaje Estricto de SEO (Invariante INV-TAX-1):** Se prohíbe eliminar tags (`tags: [...]`) o categorías secundarias existentes en los archivos markdown. Se actualiza únicamente el discriminador primario `category:` y se preserva intacta la totalidad de taxonomías preexistentes.
- **Consecuencias:**
  - Cero roturas de URLs ni pérdida de posicionamiento orgánico en Google.
  - Mayor conversión hacia productos de Lemon Squeezy gracias a la pestaña dedicada `Estrategia & Operaciones`.
  - Presentación equilibrada y profesional en el portal sin saturación de artículos.


## ADR-017: Nuevo Producto "Datalaria Helix" (Kit SDD con Escuadrón de 12 Agentes) para Profesionales No Desarrolladores
- **Fecha:** 2026-11-01
- **Estado:** Aceptado (Estrategia y Plan) — la especificación técnica se formalizará en el Hito 6.1 (`specs/apps/helix/spec.md`).
- **Contexto:**
  1. El catálogo `data/pulse/kits.yaml` y `/recursos/` (`recursos_catalog.html`) contenían una tarjeta `pack-sdd` / `suite-sdd` en estado `coming` (8 € / 29 €) basada únicamente en plantillas Markdown y con un botón `Avisarme` implementado como enlace `mailto:contacto@datalaria.com` sin telemetría GA4 ni formulario web (lo que provocaba abandono casi total en usuarios de correo en navegador y cero registros recibidos). Además, en noviembre de 2026 existen alternativas gratuitas (GitHub spec-kit, BMAD Method, IDEs spec-driven), por lo que las plantillas aisladas a 8 € carecen de valor comercial diferencial.
  2. Datalaria dispone de un sistema SDD probado en producción (`AGENTS.md`, Constitución, ROADMAP, ADRs, specs, gates y rollback) que gobierna el portal y sus apps, y del patrón Dual-Mode validado en Datalaria Pulse (Sandbox → Kit ZIP → Pro Supabase).
  3. El boom de las aplicaciones personales construidas con agentes de IA por profesionales sin formación técnica genera *Vibe Debt*, un dolor no atendido en español.
- **Decisión:**
  1. **Producto:** "Datalaria Helix" (*la spec es el ADN de tu app*), dirigido prioritariamente a **profesionales no desarrolladores**, agnóstico de la herramienta (Antigravity, Claude Code, Cursor, Codex) mediante núcleo Markdown + `AGENTS.md` y adaptadores generados.
  2. **Escuadrón de 12 roles en 4 células:** Dirección (Orquestador/Delivery Lead, Product Analyst, Arquitecto), Diseño y Construcción (UX/UI, Frontend, Backend y Datos, APIs e Integraciones, Media/Contenido/i18n, Monetización y Analítica), Garantía (Seguridad y Privacidad, QA Verifier con veto) y Entrega (Release y DevOps).
     - El **Orquestador** realiza un triaje determinista (tallas XS–XL + disparadores automáticos de Seguridad, UX/UI, Media y QA) para activar solo los roles necesarios (media objetivo 2–4 por tarea) y es el único interlocutor del usuario. Se descarta el nombre "Scrum Master" porque en Scrum ese rol facilita y no asigna trabajo.
     - El **Diseñador UX/UI** es dueño de `design.md` (dirección de diseño por preset, design tokens, flujos, estados, WCAG 2.2 AA) y de la revisión visual previa al gate de QA.
     - Principio rector: **nadie verifica su propio trabajo**.
  3. **Sandbox gratuito A+B:** Spec Builder determinista en navegador + exportador de prompt (sin API key, coste cero). BYOK Gemini (opción C) aplazado a v1.1.
  4. **Oferta de partida y homologación de precio de lanzamiento (19 €):** Starter (~9 €) y Kit Core homologado a **19 € como precio oficial de lanzamiento** (antes 39 €) en tarjetas y catálogo de Lemon Squeezy (en paridad con el precio de lanzamiento de 19 € acordado para el *Datalaria Pulse Kit* y las Suites Ejecutivas). **El modelo Pro (suscripción / lifetime) queda pendiente** hasta medir tracción (Hito 6.10: ≥300 emails, ≥50 ventas Core, ≥30 % de demanda de actualizaciones/dashboard).
  5. **Integración de la tarjeta previa en `/recursos/` y Waitlist Brevo:** Se transforma *in-place* la ficha `pack-sdd` / `suite-sdd` en **Datalaria Helix** (19 € lanzamiento / 39 €, eliminando el ancla de 8 €, activando el enlace al artículo técnico desde el 4 de noviembre y reemplazando los 3 enlaces `mailto:` por un formulario/modal web conectado a 2 nuevas listas de Brevo ES/EN vía `/.netlify/functions/subscribe` + evento GA4 `join_waitlist_helix`).
  6. **Calendario Acelerado y "Operación Crisol" sobre Datalaria Pulse:**
     - **4 y 11 nov (Hito 6.0):** Publicación de `sdd_vs_vibe_coding` (4 nov) y `agentes_ia_operativa_sdd` (11 nov en exclusiva, abriendo la Waitlist), incluyendo mención *teaser* a **Datalaria Pulse** como primer producto real auditado con Datalaria Helix.
     - **5–11 nov (Hitos 6.1 y 6.2):** Especificación formal de las 12 fichas `AGENT_SPEC` y despliegue interno del escuadrón en el repositorio de Datalaria (`ADR-018`).
     - **12–16 nov (Hito 6.3 — Operación Crisol):** Auditoría formal y robustecimiento de **Datalaria Pulse** (App, Kit ZIP, UX/UI, seguridad RLS y empaquetado comercial a **19 €**) ejecutada por los 12 agentes de Helix ya operativos, **respetando embargo estricto hasta el 2026-11-18** (ni la ficha pública en `/apps/` ni `#pack-pulse` en `/recursos/` se habilitan antes de la salida del Post 1 de Pulse el día 18). Pulse Pro se posiciona en el Post 5 exclusivamente como implementación B2B a medida / CMS autónomo y agéntico.
     - **Dic 2026 → ~19 Ene 2027 (Hitos 6.4–6.9):** Extracción del Kit genérico, CLI `helix`, Sandbox Web, micro-app demo externa y lanzamiento comercial de Datalaria Helix.
- **Alternativas descartadas:** vender solo plantillas (commodity); escuadrón de 10 roles sin Orquestador (sobrecarga en tareas pequeñas); BYOK obligatorio desde el día 1 (fricción para no devs); habilitar la ficha o el Kit de Datalaria Pulse antes del 18 de noviembre (violaría la invariante constitucional Art. 7.1 `App Activa ⇔ Post Publicado`).
- **Consecuencias:**
  - FASE 6 estructurada en Hitos 6.0–6.10 en `ROADMAP.md`, convirtiendo a Datalaria Pulse en el *Case Study #1* auditado por el escuadrón de 12 agentes antes de su salida el 18 de noviembre.
  - La adopción interna del escuadrón (Constitución v1.1.0, Art. 9) será aditiva, con carga de roles bajo demanda y sin cambios retroactivos en specs existentes; se registrará en ADR-018 al ejecutar el Hito 6.2.


---

## ADR-018: Despliegue Interno (Dogfooding) del Escuadrón de 12 Agentes Datalaria Helix, Constitución v1.1.0 (Art. 9) y Compilador Multi-Herramienta (`ops/helix/build_adapters.py`)
- **Fecha:** 2026-11-03
- **Estado:** Aceptado (Implementado en Hito 6.2)
- **Contexto:**
  1. Con la especificación maestra `SPEC-APP-HELIX` y las 12 fichas canónicas `AGENT_SPEC` aprobadas en `specs/squad/` (Hito 6.1), Datalaria debe convertirse en el **Caso Cero (*Dogfooding*)** de su propio producto antes de auditar Datalaria Pulse en el Hito 6.3 (*Operación Crisol*).
  2. Existen dos riesgos técnicos documentados en la literatura de sistemas multi-agente para codificación: (a) la **saturación de ventana de contexto** si se cargan las 12 fichas simultáneamente en cada sesión, y (b) la **deriva de configuración (*Adapter Drift*)** entre distintas herramientas de IA (Google Antigravity, Claude Code, Cursor, Codex).
- **Decisión:**
  1. **Elevar la Constitución SDD a la versión `1.1.0` incorporando el Artículo 9 (`Gobernanza del Escuadrón de 12 Agentes Datalaria Helix`):**
     - Instituye con rango constitucional las invariantes `INV-HELIX-1` (separación estricta Construcción vs. Verificación y derecho a veto exclusivo de `10-security-privacy` y `11-qa-verifier`), `INV-HELIX-2` (triaje determinista `XS–XL` y carga de fichas bajo demanda), `INV-HELIX-3` (disparadores automáticos innegociables `TRG-SEC`, `TRG-UX`, `TRG-I18N`, `TRG-MON`, `TRG-QA`) e `INV-HELIX-4` (fuente única en `specs/squad/`).
  2. **Ampliación Aditiva de `AGENTS.md` (§5), `CLAUDE.md` y `_templates/app-spec.template.md`:**
     - Se mantiene intacta la secuencia de arranque rápida en 3 pasos y se añade en `AGENTS.md` §5 la emisión obligatoria de la **Tarjeta de Triaje de 6 líneas** y la lectura selectiva de fichas.
     - No se modifican retroactivamente las especificaciones de aplicaciones ya cerradas; la nueva sección §2.2 de la plantilla se aplica a nuevas apps o al auditar módulos activos (empezando por Datalaria Pulse en el Hito 6.3).
  3. **Construcción del Motor de Validación y Compilador Multi-Herramienta (`ops/helix/`):**
     - `ops/helix/models.py`: Contratos Pydantic v2 (`AgentSpecFrontmatter`, `TriageDecision`) y motor determinista `calculate_triage()` que implementa el algoritmo matemático de `SPEC-APP-HELIX` §4.1.
     - `ops/helix/build_adapters.py`: Compilador determinista e idempotente (con soporte `--check` para CI/CD) que transforma `specs/squad/*.md` en adaptadores nativos para **Antigravity** (`.agents/squad/`), **Claude Code** (`.claude/agents/`) y **Cursor** (`.cursor/rules/helix-squad.mdc`), insertando cabeceras `DO NOT EDIT MANUALLY`.
- **Alternativas descartadas:**
  - *Incrustar el texto de los 12 agentes dentro de `AGENTS.md`:* Descartado por multiplicar por 8 el consumo de tokens de entrada en cada turno y degradar la atención del modelo en tareas pequeñas (`XS`/`S`).
  - *Mantener archivos separados a mano en `.claude/agents/` y `specs/squad/`:* Descartado por garantizar desincronización a corto plazo.
- **Consecuencias:**
  - El repositorio de Datalaria opera desde hoy bajo el escuadrón de 12 agentes con verificación automatizada en `ops/helix/tests/` (`10/10 tests pytest`), dejando todo listo para ejecutar la **Operación Crisol sobre Datalaria Pulse (Hito 6.3)**.


---

## ADR-019: Evolución Continua del Escuadrón Helix bajo Presupuesto Estricto de Contexto (INV-HELIX-8), Registro de Fricción Real ([USER-FIX]/[ENV-FIX]) y Debriefing Ejecutivo
- **Fecha:** 2026-11-04
- **Estado:** Aceptado (Implementado en Hito 6.4)
- **Contexto:**
  1. Datalaria Helix se concibe como el equipo de trabajo de ingeniería y negocio de Datalaria a largo plazo. Con cada hito completado surgen aprendizajes técnicos (ej. particularidades de Windows PowerShell frente a npm, comportamiento de React Compiler frente a `useEffect`, fórmulas Mermaid en Hugo) y oportunidades de negocio/monetización.
  2. Existe un grave riesgo de **saturación y pérdida de foco (*Context Bloat*)** si las fichas de los agentes crecen indefinidamente con teoría general o conocimientos redundantes que el modelo LLM ya posee de fábrica.
  3. El usuario requiere que el escuadrón aprenda principalmente de **los ajustes solicitados en nuevos prompts y los errores empíricos de ejecución**, y que el Coordinador cierre cada trabajo con un informe ejecutivo proporcional de participación, riesgos y propuestas de alto ROI sin sobrecargar el contexto rutinario.
- **Decisión:**
  1. **Arquitectura de Memoria en 3 Capas + Invariante Anti-Bloat (`INV-HELIX-8`):**
     - **Capa Caliente (`specs/squad/*.md`):** Tope duro innegociable de $\le 85$ líneas por ficha de agente y máximo 6 ítems en su Sección `## 6. Reglas de Fricción Real y Correcciones`. Si entra una regla nueva al límite, se aplica poda FIFO o síntesis.
     - **Capa Templada (`TECH_RADAR.yaml` y `OPPORTUNITY_BACKLOG.md`):** Radar tecnológico oficial (anillos `ADOPT`, `TRIAL`, `ASSESS`, `HOLD`) y registro priorizado RICE de mejoras técnicas, UX y monetización. **Queda prohibido cargarlos en tareas rutinarias `XS`, `S`, `M` o `L`**; solo se leen bajo demanda o en planificación `XL` por el Coordinador.
     - **Capa Fría (`DECISIONS.md`, `specs/audit/case-study-*.md`):** Historial permanente de decisiones y casos de estudio.
  2. **Criterio Estricto de Registro (`User-Correction & Friction First`):**
     - En la Sección `## 6` de cada agente se registran **únicamente** reglas precedidas por:
       - `[USER-FIX]`: Correcciones explícitas indicadas por el usuario en nuevos prompts tras una ejecución.
       - `[ENV-FIX]`: Soluciones a fallos reales de ejecución o particularidades de herramientas/entorno.
       - `[RADAR-SKILL]`: Competencia activa de vigilancia proactiva de mercado/tecnología con filtro ROI.
     - Queda terminantemente prohibido registrar teoría académica o conocimientos genéricos ya adquiridos por el LLM.
  3. **Tarjeta de Cierre `DEBRIEF HELIX`:**
     - En tareas `M`, `L` y `XL`, el Coordinador (`01-orchestrator`) cierra la intervención con un resumen estructurado: (1) participación por rol convocado, (2) conclusiones y aprendizajes destilados, (3) riesgos detectados y mitigación, y (4) propuestas de mejora tecnológica, UX o de monetización filtradas por su impacto y retorno real para Datalaria.
  4. **Ampliación de Habilidades de Negocio sin Aumentar el Número de Agentes (Preservación de los 12 Roles):**
     - Se mantiene la identidad canónica de 12 agentes potenciando las skills de negocio en tres roles existentes:
       - `02-product-analyst`: Estrategia de producto, dolor B2B y radar de mercado.
       - `08-media-i18n`: SEO orgánico (GSC), distribución de contenidos y optimización de CTR.
       - `09-monetization`: Embudos PLG, monetización editorial y conversión en Lemon Squeezy/Brevo.
- **Alternativas descartadas:**
  - *Añadir un 13º o 14º agente de "Growth" o "Marketing":* Descartado por romper la paridad con los artículos ya publicados y la identidad del producto Datalaria Helix (12 agentes).
  - *Permitir que las fichas crezcan sin límite de líneas:* Descartado por garantizar degradación cognitiva del modelo a medio plazo (*Lost in the Middle*).
  - *Cargar el radar tecnológico y backlog de oportunidades en cada turno:* Descartado por consumir miles de tokens innecesarios en tareas de desarrollo acotadas.
- **Consecuencias:**
  - El escuadrón evoluciona de forma medible y acumulativa sin penalizar la ventana de contexto.
  - El Kit Core genérico (`packages/helix/core_kit/`) se entrega a los compradores con esta disciplina de memoria anti-bloat y con los 3 Blueprints de arquitectura listos para producción.


---

## ADR-020: Despliegue del Segundo Escuadrón "Datalaria Scriba" (8 Agentes Editoriales & Growth), Analista SEO/GA4 (`impact_analyzer.py`), Brevo Newsletter 2.0 y Autopilot 2.0
- **Fecha:** 2026-11-07
- **Estado:** Aceptado (Planificado como FASE 7 en `specs/ROADMAP.md`, a ejecutar inmediatamente tras cerrar y congelar los Hitos 6.8 y 6.9 de Datalaria Helix)
- **Contexto:**
  1. El blog técnico bilingüe (`ES ⇔ EN`) es el principal motor de captación de usuarios y autoridad orgánica de Datalaria. Con el escuadrón de ingeniería **Datalaria Helix** (`specs/squad/`) consolidado para construir aplicaciones y Kits B2B, se requiere un equipo homólogo especializado exclusivamente en la cadena de valor editorial: calendario, redacción orientada a conversión pasiva, sindicación omnicanal y análisis cuantitativo post-publicación.
  2. La auditoría de [`autopilot/`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/autopilot/src/orchestrator.py) reveló oportunidades críticas de mejora y alineación con SDD:
     - **Newsletter Brevo (`newsletter_manager.py`):** Todos los correos compartían un asunto fijo (`🚀 Nuevo en Datalaria: ...`), carecían de la imagen de portada del artículo (`cover.png`) y operaban como meros *teasers* sin valor autónomo en bandeja de entrada, provocando fatiga y bajas de suscriptores (*churn*).
     - **Canales Sociales:** X/Twitter eliminó su capa gratuita de publicación por API (`402 Payment Required`), mientras que **CoderLegion** dispone de API activa (`/api/v1/posts` con clave ya configurada en `autopilot/.env` y GitHub Secrets como `CODERLEGION_API_KEY`).
     - **Solapamiento y Deuda:** `autopilot/ctrl/` dependía de llamadas a `gh copilot suggest` por subproceso y mantenía archivos `*_OLD_DEPRECATED.py` fuera del estándar de contratos Pydantic v2.
- **Decisión:**
  1. **Arquitectura Federada del "Superequipo Datalaria" (Helix + Scriba):**
     - Crear el escuadrón **`Datalaria Scriba`** (comercializable a futuro dentro de la suite como *Datalaria Pulse Scriba*) en `specs/squad-editorial/` con **8 agentes en 4 células** bajo las mismas invariantes de higiene de contexto (`INV-HELIX-2`, `INV-HELIX-8`, fichas $\le 85$ líneas) y separación Creación vs. Verificación con Veto (`E07-editorial-qa`).
     - Coordinación mediante dos directores específicos: `01-orchestrator` (Ingeniería/Producto en Helix) y `E01-editorial-orchestrator` (Calendario/Contenido/Growth en Scriba).
  2. **Analista SEO y Consultor Estratégico (`E02-seo-impact-strategist`) + Músculo Determinista (`ops/pulse/impact_analyzer.py`):**
     - Cumpliendo el Art. 1.3 de la Constitución (*Separación Cerebro vs. Músculo*), se desarrollará `ops/pulse/impact_analyzer.py` para cruzar automáticamente `metrics.json` (GA4 + Search Console) e `index.json` tras cada actualización y generar reportes accionables de *Quick Wins de CTR*, *Huérfanos de Monetización (PLG)*, *Decay Alerts* y *Editorial ROI Score*.
  3. **Brevo Newsletter 2.0 Anti-Churn (`newsletter_manager.py` + `E05-content-monetizer`):**
     - Eliminar el prefijo fijo de asunto e implantar rotación entre 5 arquetipos de alto Open Rate + Preheader dinámico.
     - Incluir **1 única imagen Hero clicable (`cover.png` del post)** manteniendo un ratio Texto/Imagen $>80\%$ para proteger la entregabilidad en la bandeja Principal.
     - Incorporar la caja visual **"⚡ En 60 segundos: Los 3 Insights Clave"** (*Zero-Click Value*) para que el suscriptor reciba valor tangible sin salir del correo, reduciendo las bajas, junto con doble CTA (Artículo + Sandbox/Kit) y bucle de recomendación.
  4. **Autopilot 2.0 con Coste Fijo 0 €/mes e Integración `CoderLegion`:**
     - **LinkedIn, Dev.to, CoderLegion (`/api/v1/posts`) y Brevo:** 100 % automatizados vía API gratuita a partir del paquete `social_pack.yaml` validado por `E07-editorial-qa` y el transformador universal `markdown_syndicator.py`.
     - **X / Twitter:** Política de coste 0 € (`ENABLE_TWITTER_API=false`), generando automáticamente el Tweet gancho + Hilo de 4–5 tweets + enlace `X Web Intent` (`https://x.com/intent/tweet?...`) para publicación manual en 1 clic sin pagar créditos de API.
  5. **Orden de Ejecución Estricto:**
     - Completar y dejar congelados primero los **Hitos 6.8 y 6.9 de Datalaria Helix** (empaquetado comercial y serie de posts programados para enero de 2027), y a continuación ejecutar los **Hitos 7.1 a 7.5 de Datalaria Scriba**.
- **Consecuencias:**
  - Sincronización total entre el blog, los productos de 19 € en Lemon Squeezy, la lista de Brevo y la distribución en 5 canales sin costes fijos de APIs.


---

## ADR-021: Evolución de Weather Service a Observatorio Climático & Laboratorio ML (`v2.0.0`), Estrategia de Almacenamiento en 3 Etapas de Coste 0 € y Ejecución Híbrida Argon/Flash
- **Fecha:** 2026-11-08
- **Estado:** Aceptado (En ejecución en Hitos 2.3 a 2.7)
- **Contexto:**
  1. La aplicación Flagship **Weather Service** (`/apps/weather/`) acumula en producción (`Dalaez/app_weather` → `datalaria-app-weather.netlify.app`) más de **377 días continuos** de telemetría real (**~192.360 registros** en **168 ciudades globales** con 15 variables cada 8 horas), habiendo cruzado por primera vez un ciclo estacional completo (>365 días).
  2. La auditoría del Escuadrón Datalaria Helix detectó 5 oportunidades de alto impacto:
     - **Modelo ML sin memoria ni estacionalidad cíclica:** `read_weather.py` utilizaba `dia_del_anio` ($1 \dots 366$) como variable lineal directa en `LinearRegression` (provocando distorsión en el cambio de año y al modelar una curva anual sinusoidal como una recta) y sobrescribía las predicciones diarias sin medir su acierto real (MAE / $R^2$ / Win-Rate) frente a OpenWeatherMap.
     - **168 ciudades sin agregación global:** El cliente solo cargaba `city_locations.json` (4 campos) y obligaba a buscar ciudades a ciegas, sin rankings de extremos, anomalías térmicas ($\Delta_{30\text{d}}$) ni Índice de Confort Outdoor.
     - **Desconexión UX/UI, i18n y GA4:** Interfaz legacy en modo claro por defecto, pérdida de idioma al cruzar desde `/en/apps/weather/`, `app_url` y `demo_url` idénticos en `data/apps/weather.yaml`, y cero telemetría GA4 ni conversión PLG.
     - **Copias CSV obsoletas en `static/apps/weather/datos/`:** 168 archivos CSV de noviembre de 2025 residían en `static/apps/weather/datos/` sin ser utilizados en producción debido al proxy `200!` de `_redirects`.
  3. El usuario requiere mantener **coste fijo 0,00 €/mes** hasta que el producto monetice por sí mismo, preparando una ruta limpia hacia Supabase u otra plataforma cuando el volumen escale sustancialmente en ~1 año, y optimizar la agilidad y el consumo de tokens combinando **Gemini 4 Argon** (Diseño/Specs) con **Gemini 3.8 Flash** (Ejecución hito a hito).
- **Decisión:**
  1. **Estrategia de Persistencia Escalable en 3 Etapas (Coste 0,00 € Garantizado):**
     - **Etapa 1 (Actual — Hitos 2.3 a 2.7, hasta ~550k filas / 3 años):** Mantener Git + Netlify CDN con pre-agregación en `global_summary.json` ($\sim 45\text{ KB}$) generado por `read_weather.py v2.0` para carga instantánea ($< 15\text{ ms}$) y lectura de CSVs bajo demanda. Eliminar los 168 CSVs obsoletos de `static/apps/weather/datos/`.
     - **Etapa 2 (Horizonte +12–18 meses):** Compactación columnar en **Apache Parquet** (reducción de tamaño $10\times$) consultable en cliente con DuckDB-Wasm o desde CDN gratuito, evitando saturar los 500 MB del Free Tier PostgreSQL de `datalaria-core` con series temporales *append-only*.
     - **Etapa 3 (Monetización Pro):** Esquema `weather` en Supabase (`datalaria-core`) reservado exclusivamente a tablas transaccionales ligeras de usuarios registrados (`weather.user_alerts`, `weather.favorite_cities`, `weather.daily_model_scores`, $< 5\text{ MB}$ con RLS).
  2. **Evolución Funcional a `Weather Service v2.0` (`SPEC-APP-WEATHER` v2.0.0 y `DESIGN-APP-WEATHER`):**
     - **Motor ML v2.0:** Transformación armónica de Fourier ($\sin/\cos$ del día del año), retardos a 24h/48h, amplitud térmica diurna, coherencia física $\min \le \text{media} \le \max$, walk-forward backtesting ($\text{MAE}_{30\text{d}}$, $R^2$, importancia de variables) e **Índice de Confort Outdoor (`0..100`)**.
     - **Executive Weather Cockpit en 3 Vistas:** `Observatorio` (Mapa multicapa + Presets en 1 clic + Super-Cards + Matriz estacional), `Laboratorio ML (IA vs OWM)` y `Atlas Global (168 Ciudades)` con exportación CSV/JSON, Deep-Links (`?lang=`, `?preset=`, `?cities=`, `?view=`) y eventos GA4.
  3. **Protocolo de Ejecución Híbrida Argon + Flash:**
     - **Gemini 4 Argon** diseña y cierra los contratos formales (`spec.md`, `design.md`, fórmulas e invariantes) en el Hito 2.3.
     - **Gemini 3.8 Flash** ejecuta secuencialmente los Hitos 2.4 (Backend Python + `pytest`), 2.5 (Frontend Cockpit `index.html`), 2.6 (Fichas ES/EN + `weather.yaml` + sync upstream) y 2.7 (Artículo Parte 5 ES/EN) guiado por los Verification Gates deterministas.
- **Consecuencias:**
  - Máxima velocidad de entrega y ahorro de tokens de modelo pesado sin pérdida de calidad gracias a contratos SDD verificables al 100% por CLI (`pytest` + `hugo`).
  - Protección total de la cuota gratuita de Supabase (`datalaria-core`) mientras `Weather Service` multiplica por 10 el valor percibido de sus +192.000 registros.

---

## ADR-022: Data Truth Pipeline: Derivados JSON en Upstream, Frontend Remote-First y Persistencia Local Opcional (`v3.0.0`)
- **Fecha:** 2026-11-08
- **Estado:** Aceptado (En ejecución en Hitos W3.1, W3.2 y W3.3)
- **Contexto:**
  1. La auditoría empírica de la interfaz `v2.0` reveló que las gráficas de evolución temporal, amplitud diurna y perfil estacional aparecían incompletas o vacías en entornos locales y de producción porque:
     - Los CSVs locales en `apps/weather/datos/*.csv` estaban congelados en el 30 de noviembre de 2025 (124 registros por estación), mientras que el repositorio upstream en producción (`Dalaez/app_weather`) alojaba más de 1.147 registros por ciudad hasta la fecha actual (>192.000 lecturas en total).
     - La lógica de carga del cliente solo recurría al CDN remoto si el archivo local devolvía HTTP 404, bloqueando el refresco de datos reales.
     - OpenWeatherMap v2.5 devuelve frecuentemente `temp_min == temp_max` en cada lectura puntual tri-diaria, provocando que la amplitud térmica diurna calculada en crudo fuese 0.
     - La columna `ciudad` presenta variaciones nominales respecto al estándar (ej. "Sol" en lugar de "Madrid").
  2. El usuario requiere resolver la veracidad y completitud de datos sin saturar el almacenamiento de su equipo local con descargas masivas de CSVs ni introducir sobrecargas de commits diarios en el monorepo web `datalaria-website`, al tiempo que se habilita uso offline y experiencia PWA instalable de alta usabilidad sin abrumar con controles redundantes.
- **Decisión:**
  1. **Generación de Derivados Compactos en el Upstream (`build_derived.py`):**
     - La automatización de GitHub Actions en `Dalaez/app_weather` (`actualizar-clima.yml`) incorporará un paso diario nocturno (`22:00 UTC`) no bloqueante (`continue-on-error: true`) que pre-calcula y emite:
       - `derived/daily/<slug>.json`: Series agregadas diarias (~15 KB/ciudad vs. 130 KB de CSV crudo), con amplitud calculada como `max - min` de las muestras del día (`n >= 2`).
       - `derived/climatology.json`: Normales mensuales y armónicos de Fourier de 168 estaciones.
       - `derived/index.json`: Índice rápido de estaciones y recuentos de registros.
       - `derived/forecast_log/AAAA-MM.csv`: Auditoría idempotente de acierto IA vs. OWM.
  2. **Arquitectura Frontend "Remote-First":**
     - El cliente web (`apps/weather/index.html`) prioriza la lectura directa de los derivados JSON servidos por el CDN de Netlify (`REMOTE_BASE`), utilizando la copia local solo como fallback de contingencia.
     - Se ancla la ventana temporal al último registro real (`last_date`) y se despliega un badge de frescura contextual (`INV-WEATHER-7`).
  3. **Almacenamiento Local Opcional y Acotado (`sync_upstream.py --pull`):**
     - La máquina local no requiere descargar los 168 CSVs completos. El CLI `--pull` descarga exclusivamente los metadatos y resúmenes compactos (≤ 2 MB en total).
  4. **Divulgación Progresiva y Puerta de Suficiencia (`INV-WEATHER-8`):**
     - Se reemplaza la sobrecarga de controles por una Tarjeta Respuesta ejecutiva por ciudad, agrupando gráficas bajo demanda en acordeones `<details>` que solo se renderizan si superan el umbral mínimo de datos históricos.
  5. **PWA Offline Determinista (`INV-WEATHER-10`):**
     - Service Worker (`sw.js`) con estrategia `stale-while-revalidate` para derivados JSON y prohibición estricta de cachear CSVs planos.
- **Alternativas Descartadas:**
  - *Alternativa A: Parsear los 168 CSVs crudos en el navegador con PapaParse.* Descartada porque saturaría el ancho de banda del cliente (>25 MB de descarga total) y degradaría severamente la CPU móvil.
  - *Alternativa B: Generar derivados durante el build estático de Netlify.* Descartada porque Netlify aloja un deploy estático sin runtime persistente de Python programado cada 8 horas.
  - *Alternativa C: Commits y pushes diarios de datos meteorológicos dentro de `datalaria-website`.* Descartada taxativamente para preservar la limpieza del monorepo principal y evitar inundar el historial Git local con telemetría no editable.
- **Consecuencias:**
  - Cero riesgo de pérdida de datos históricos y preservación absoluta del SEO existente.
  - Carga inmediata (<100 ms) de visualizaciones ricas y fiables en cualquier dispositivo sin consumir almacenamiento en la máquina local del desarrollador.
  - Base de datos relacional implícita lista para una migración limpia hacia Supabase en la Etapa 3.
