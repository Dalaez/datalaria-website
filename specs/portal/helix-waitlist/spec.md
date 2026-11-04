# Especificación Técnica SDD: Pre-Lanzamiento Editorial Datalaria Helix, Transformación de `pack-sdd` y Lista de Espera Brevo (`SPEC-PORTAL-HELIX-WL`)

> **ID de Especificación:** `SPEC-PORTAL-HELIX-WL`  
> **Versión:** `1.0.0`  
> **Estado:** `APPROVED`  
> **Propietario de Dominio:** Datalaria (Operations Engineering & Applied AI)  
> **Hito Asociado:** `FASE 6 — Hito 6.0`  
> **Referencia ADR:** [`ADR-017`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/DECISIONS.md#adr-017-datalaria-helix--arquitectura-del-kit-sdd-escuadrón-de-12-agentes-con-orquestador-y-uxui-embudo-sandbox-ab-dogfooding-y-auditoría-crisol-de-datalaria-pulse-2026-11-01--actualizado-2026-11-02)

---

## 1. Propósito Ejecutivo y Contexto de Negocio

Activar el embudo de captación temprana (*Waitlist*) y el puente editorial de **Datalaria Helix** (el Kit de Spec-Driven Development con escuadrón de 12 agentes especializados, lanzamiento oficial en **Enero 2027** a precio Early-Bird de **19 €** / PVP **39 €**) coincidiendo con los dos artículos fundacionales de SDD:
1. **`2026-11-04`:** [`content/{es,en}/posts/sdd_vs_vibe_coding/index.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/content/es/posts/sdd_vs_vibe_coding/index.md)
2. **`2026-11-11`:** [`content/{es,en}/posts/agentes_ia_operativa_sdd/index.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/content/es/posts/agentes_ia_operativa_sdd/index.md) (adelantado en exclusiva desde el `2026-11-17`).

Simultáneamente, evolucionar *in-place* la tarjeta preexistente **`#pack-sdd`** y la suite **`#suite-sdd`** en el catálogo de Recursos (`/es/recursos/` y `/en/resources/`), reemplazando los enlaces pasivos `mailto:contacto@datalaria.com` (0 conversiones registradas) por un flujo transaccional de 1 clic conectado a **Brevo** (`/.netlify/functions/subscribe`) con telemetría GA4 (`join_waitlist_helix`).

---

## 2. Invariantes de Dominio y Seguridad (`INV-HELIX-WL-*`)

### `INV-HELIX-WL-1`: Cero Enlaces 404 bajo `buildFuture: false` y Cero Enlaces a Borradores (`draft: true`)
Con `buildFuture: false` en `config.yaml`, Hugo no genera páginas con `date` futura ni `draft: true`. Por tanto:
- En `sdd_vs_vibe_coding` (`2026-11-04`), la referencia a `agentes_ia_operativa_sdd` (`2026-11-11`) **NO debe incluir hipervínculo `<a href>`** mientras no haya llegado el 11 de noviembre; debe citarse como entrega programada para el **11 de noviembre** y enlazar a `/es/recursos/#software` (`/en/resources/#software`).
- Se eliminan los enlaces a artículos en `draft: true` (`proj_ops_parte1_intro`, `proj_ops_parte2_agentic_pmo`) sustituyéndolos por la serie publicada de Observabilidad Agéntica (`/es/posts/obs_parte1_intro/`, `/en/posts/obs_part1_intro/`).
- Se elimina el hipervínculo prematuro a `inference_time_scaling` (`2026-11-29`) en `agentes_ia_operativa_sdd`, citándolo como próxima entrega sin enlace muerto.
- Se corrige en `sdd_vs_vibe_coding` (EN) los slugs rotos `/en/posts/evaluacion_agentes_ia/` → `/en/posts/evaluating_ai_agents/` y `/en/posts/stack_productividad_2026/` → `/en/posts/productivity_stack_2026/`, así como `/es/resources/` → `/es/recursos/#software` en `agentes_ia_operativa_sdd` (ES).

### `INV-HELIX-WL-2`: Embargo Comercial Estricto de Datalaria Pulse hasta el `2026-11-18`
- Antes del **18 de noviembre de 2026**, ni el Kit comercial de Datalaria Pulse ni su ficha `/apps/pulse/` (`status: incubating`) pueden estar habilitados públicamente.
- En los artículos SDD del **4 y 11 de noviembre**, **Datalaria Pulse** se menciona exclusivamente en formato *teaser* sin hipervínculo como el **Caso Cero (*Operación Crisol*)**: el primer sistema en producción auditado de extremo a extremo por el escuadrón de 12 agentes de Datalaria Helix antes de su estreno del 18 de noviembre.

### `INV-HELIX-WL-3`: Lista Blanca Cerrada en `netlify/functions/subscribe.js` y Seguridad de Atributos Brevo
- La función serverless [`netlify/functions/subscribe.js`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/netlify/functions/subscribe.js) debe validar el parámetro opcional `list` contra una lista blanca cerrada (`['newsletter', 'helix']`). Cualquier otro valor hace *fallback* seguro a `'newsletter'`.
- Cuando `list === 'helix'`, los contactos se enrutan a `Number(process.env.BREVO_HELIX_LIST_ES || 5)` (para `language === 'es'`) y `Number(process.env.BREVO_HELIX_LIST_EN || 6)` (para `language === 'en'`).
- **Seguridad de Esquema Brevo:** Solo se envían los atributos estándar preexistentes `{ FIRSTNAME, LASTNAME, LANGUAGE }` en el payload `attributes` hacia `https://api.brevo.com/v3/contacts` para evitar errores `400 Bad Request` por atributos no declarados en Brevo.

### `INV-HELIX-WL-4`: Erradicación de `mailto:` en Waitlist y Paridad Bilingüe ES/EN
- Ningún botón `Avisarme` / `Notify Me` / `Waitlist` en [`layouts/partials/recursos_catalog.html`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/layouts/partials/recursos_catalog.html), [`scripts/generate_recursos_pages.py`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/scripts/generate_recursos_pages.py), [`content/es/recursos/_index.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/content/es/recursos/_index.md) o [`content/en/resources/_index.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/content/en/resources/_index.md) puede utilizar `mailto:contacto@datalaria.com`.
- Todos los puntos de entrada de lista de espera en `/recursos/` y `/resources/` (tarjeta Grid, fila Tabla, banner de Suite Software y botón primario del Modal Detalles) deben invocar `openWaitlistModal('pack-sdd')`, abriendo un modal interactivo conectado a `/.netlify/functions/subscribe` (`list: 'helix'`) y disparando el evento GA4 `join_waitlist_helix`.

---

### `INV-HELIX-WL-5`: Resiliencia en Entornos Locales (`localhost`) y Compatibilidad CORS/OPTIONS
- En servidores de desarrollo puramente estáticos (`hugo server` en `localhost:1313`), las solicitudes a `/.netlify/functions/subscribe` devuelven HTTP 404 por ausencia del runtime Node.js serverless de Netlify.
- Todos los componentes cliente ([`layouts/shortcodes/helix-waitlist.html`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/layouts/shortcodes/helix-waitlist.html), [`layouts/partials/recursos_catalog.html`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/layouts/partials/recursos_catalog.html) y [`layouts/partials/extend_footer.html`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/layouts/partials/extend_footer.html)) detectan `localhost` / `127.0.0.1` y ejecutan una simulación exitosa limpia: imprimen logs detallados en `console.info`, disparan el evento de telemetría GA4, muestran la confirmación en verde indicando el modo localhost y resetean el formulario sin fallar.
- En [`netlify/functions/subscribe.js`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/netlify/functions/subscribe.js) se garantizan cabeceras CORS en todas las respuestas, preflight `OPTIONS` `200 OK`, esquema de respuesta `{ success: true, message: ..., list: ... }` y manejo idempotente de duplicados de Brevo (`duplicate_parameter`).

---

## 3. Manifiesto de Archivos Afectados

| Archivo | Acción Requerida |
| :--- | :--- |
| [`specs/portal/helix-waitlist/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/portal/helix-waitlist/spec.md) | Especificación técnica SDD del Hito 6.0 (este documento). |
| [`content/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/index.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/content/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/index.md) | Desplazar `date: 2026-11-11` → `date: 2026-11-14` para liberar en exclusiva el 11 de noviembre. |
| [`content/en/posts/decision-making-prioritization-quantitative-framework/index.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/content/en/posts/decision-making-prioritization-quantitative-framework/index.md) | Alinear `date: 2026-11-12` → `date: 2026-11-14` en paridad estricta con ES. |
| [`netlify/functions/subscribe.js`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/netlify/functions/subscribe.js) | Soportar parámetro `list` (`'newsletter'` \| `'helix'`) con variables `BREVO_HELIX_LIST_ES` (default `5`) y `BREVO_HELIX_LIST_EN` (default `6`). |
| [`layouts/shortcodes/helix-waitlist.html`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/layouts/shortcodes/helix-waitlist.html) | Nuevo shortcode bilingüe ES/EN para insertar la caja de prelanzamiento de **Datalaria Helix (19 € Early-Bird)** y alta directa en Brevo dentro de los artículos SDD. |
| [`content/es/posts/sdd_vs_vibe_coding/index.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/content/es/posts/sdd_vs_vibe_coding/index.md) | Eliminar enlace futuro a `agentes_ia_operativa_sdd` (`INV-HELIX-WL-1`), sustituir enlace draft `proj_ops_parte1_intro` por `obs_parte1_intro`, añadir mención *teaser* a Datalaria Pulse + Datalaria Helix e incrustar `{{< helix-waitlist >}}`. |
| [`content/en/posts/sdd_vs_vibe_coding/index.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/content/en/posts/sdd_vs_vibe_coding/index.md) | Paridad con ES + corrección de slugs `/en/posts/evaluating_ai_agents/` y `/en/posts/productivity_stack_2026/` + `{{< helix-waitlist >}}`. |
| [`content/es/posts/agentes_ia_operativa_sdd/index.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/content/es/posts/agentes_ia_operativa_sdd/index.md) | Mover `date` a `2026-11-11`, corregir orden temporal en §6 hacia `sdd_vs_vibe_coding`, corregir enlaces draft/futuros y `/es/resources/` → `/es/recursos/#software`, presentar **Datalaria Helix** (12 agentes, 19 €, mención *teaser* a Pulse) e incrustar `{{< helix-waitlist >}}`. |
| [`content/en/posts/agentes_ia_operativa_sdd/index.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/content/en/posts/agentes_ia_operativa_sdd/index.md) | Paridad exacta con ES (`date: 2026-11-11`, corrección de enlaces y cierre con **Datalaria Helix** + `{{< helix-waitlist >}}`). |
| [`data/pulse/kits.yaml`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/data/pulse/kits.yaml) | Evolucionar `suite-sdd` y `pack-sdd` hacia **Datalaria Helix — Kit SDD & Escuadrón de 12 Agentes IA** (`price: 19€`, `original_price: 39€`, `icon: 🧬`, `guide_url_es: /es/posts/sdd_vs_vibe_coding/`, `guide_url_en: /en/posts/sdd_vs_vibe_coding/`). |
| [`layouts/partials/recursos_catalog.html`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/layouts/partials/recursos_catalog.html) | Actualizar `pack-sdd` y `suite-sdd` (ES y EN), habilitar preview visual específico de Helix en `renderModalPreview`/`getModalMockSvg`, activar botón `Artículo técnico 📖` y sustituir `mailto:` por `openWaitlistModal('pack-sdd')` conectado a Brevo. |
| [`scripts/generate_recursos_pages.py`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/scripts/generate_recursos_pages.py) | Sincronizar con `recursos_catalog.html` y regenerar `content/es/recursos/_index.md` y `content/en/resources/_index.md`. |

---

## 4. Contratos de Interfaz y Telemetría

### 4.1 Contrato HTTP `POST /.netlify/functions/subscribe`
- **Request JSON:**
  ```json
  {
    "name": "Nombre Apellido",
    "email": "usuario@dominio.com",
    "language": "es",
    "list": "helix"
  }
  ```
- **Response JSON (`200 OK`):**
  ```json
  {
    "message": "Suscripción exitosa",
    "list": "helix"
  }
  ```

### 4.2 Evento GA4
Al completarse el alta en el shortcode `helix-waitlist` o en el modal de Waitlist de `/recursos/`:
- **Event Name:** `join_waitlist_helix`
- **Event Params:** `{ item_id: 'pack-sdd', item_name: 'Datalaria Helix', language: 'es' | 'en', source: 'post_shortcode' | 'catalog_modal' }`

---

## 5. Criterios de Aceptación y Comandos de Verificación (Verification Gates)

Para marcar el **Hito 6.0** como `[x]` en [`specs/ROADMAP.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/ROADMAP.md), deben ejecutarse y superar con código `0`:

1. **Regeneración de Páginas de Recursos y Verificación de Cero `mailto:`:**
   ```powershell
   python scripts/generate_recursos_pages.py
   python -c "import pathlib; [assert 'mailto:contacto@datalaria.com' not in pathlib.Path(p).read_text(encoding='utf-8') for p in ['layouts/partials/recursos_catalog.html','content/es/recursos/_index.md','content/en/resources/_index.md']]; print('OK: Zero mailto links')"
   ```
2. **Gobernanza Editorial Automatizada (Datalaria Pulse) y Suite Pytest:**
   ```powershell
   python -m ops.pulse.build_index
   python -m ops.pulse.publish_public
   pytest ops/pulse/tests -v
   ```
3. **Verificación de Embargo de Datalaria Pulse (`INV-HELIX-WL-2`) e Integridad de Enlaces (`INV-HELIX-WL-1`):**
   ```powershell
   hugo --gc --minify
   ```
   - Código de salida `0`.
   - `public/es/apps/pulse/index.html` **NO** debe existir (embargo activo hasta el 18 nov).
   - `public/es/posts/sdd_vs_vibe_coding/index.html` y `public/en/posts/sdd_vs_vibe_coding/index.html` **SÍ** deben existir y contener el formulario `helix-waitlist`.
