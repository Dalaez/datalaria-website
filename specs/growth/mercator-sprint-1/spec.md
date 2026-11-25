# Especificación SDD: Primer Sprint Comercial Datalaria Mercator (Hito 9.3)

> **Versión:** 1.0.0 · **Fecha:** 2026-11-24 · **Estado:** ACTIVA  
> **Orquestación:** `00-chief-orchestrator` ⇔ `M01-revenue-orchestrator` (`M02`, `M03`, `M04`) + `01-orchestrator` (`04`, `09`, `10`, `11`) + `E01-editorial-orchestrator` (`E07`)  
> **Decisión Marco:** `ADR-034`, `specs/STRATEGY.md`, `specs/_brand.md`, `specs/audit/IMPACT_REPORT.md`

---

## 1. Objetivo y Alcance
Maximizar la conversión pasiva y la captación **EN-First** (con paridad 100 % `ES ⇔ EN`) antes de los lanzamientos de **`pack-obs`** (`2026-12-09`) y **`Datalaria Helix`** (`2027-01-19`), operando a **coste fijo `0 €/mes`** y respetando el 100 % de los embargos vigentes (`INV-AUTO-6`).

---

## 2. Arquitectura de Oferta, Licencias B2B y Cupón Progresivo (`M02` + `09`)

### 2.1 Escalera de Valor en `/es/recursos/` y `/en/resources/`
1. **Kit Individual (`5 € – 9 €`):** Entrada sin fricción para un problema puntual (Excel `.xlsx` sin VBA + PPTX 16:9 + Guía PDF).
2. **Suite Temática (`15 € – 22 €`):** Ahorro real del `25% – 35%` agrupando 3–5 modelos de una misma disciplina (`suite-01` `19 €` vs `28 €`, `suite-02` `15 €` vs `20 €`, `suite-03` `22 €` vs `34 €`).
3. **Mega Bundle Total (`39 €`):** Colección de los 13 kits estratégicos y operativos (`> 52%` ahorro frente a `82 €` individual; subida programada a `59 €`).
4. **Kits de Software & IA (`19 €` Early-Bird / `39 €` PVP):** `pack-pulse` (disponible), `pack-obs` (embargo `2026-12-09`), `pack-sdd` / `suite-sdd` (embargo `2027-01-19`).

### 2.2 Tier Licencia Equipo / Corporativa B2B (`99 € – 149 €`)
Para multiplicar margen neto sin soporte 1-a-1 (Peldaño 3 de `specs/STRATEGY.md`):
- **Licencia Equipo (hasta 5 usuarios) — `99 €` (pago único):** Uso interno compartido en equipo/departamento sobre Mega Bundle o Kit de Software (`pack-pulse`, `pack-obs`, `pack-sdd`), factura B2B con IVA/VIES y 12 meses de actualizaciones.
- **Licencia Corporativa / PMO (hasta 20 usuarios) — `149 €` (pago único):** Despliegue corporativo interno para PMO, consultoras o dirección de operaciones, documentación de compra/PO, factura VIES y 12 meses de actualizaciones.
- **Flujo de Solicitud y Checkout (Cero `mailto:`):** Enlace directo trazado con GA4 `beacon` hacia `/es/contact/?topic=b2b-license` y `/en/contact/?topic=b2b-license` (Netlify Forms con preselección automática del asunto) listo para cablear variantes de Lemon Squeezy cuando se publiquen en tienda.

### 2.3 Especificación Operativa del Cupón de Cross-Sell Progresivo (`OPP-MON-01`)
- **Plataforma:** Lemon Squeezy Discounts (capa gratuita).
- **Código:** `DATALARIA-UPGRADE20` (`20%` de descuento).
- **Ámbito:** Aplicable a `suite-01`, `suite-02`, `suite-03` y `mega-bundle` (`39 €` → `31,20 €`). Excluye productos embargados (`status: coming`).
- **Entrega Automática:** Email #3 (`D+14`) del Flujo Post-Compra en Brevo (`data/growth/lifecycle_flows.yaml`).
- **Reglas de Control:** Máximo 1 uso por email comprador, validez 14 días desde recepción, telemetría agregada sin PII en `ops/pulse/sync_revenue.py` (`INV-PULSE-13`).

---

## 3. Componentes UI, Accesibilidad y Telemetría (`04` + `M02`)
- **Bloque Comparativo de Ahorro Real (`#pricing-comparison`):** Tabla/tarjetas responsivas en `layouts/partials/recursos_catalog.html` (compilada a `content/es/recursos/_index.md` y `content/en/resources/_index.md`).
- **Banner Licencia Equipo/Corporativa B2B (`#b2b-team-license`):** Integrado en `/recursos/` y enlazado desde las fichas de aplicaciones (`layouts/apps/single.html`, `pulse`, `obs-management`) erradicando cualquier enlace `mailto:`.
- **FAQ Compacta en `<details>` Nativo (`#catalog-faq`):** Basada en `modern-web-guidance` (`accordion`), no exclusiva, sin etiquetas `<h*>` dentro de `<summary>`, con animación progresiva `::details-content` y respeto a `prefers-reduced-motion`.
- **Telemetría GA4 No Bloqueante:** Todos los eventos (`begin_checkout_kit`, `b2b_license_inquiry`, `faq_expand`, `join_waitlist_helix`) envían `transport_type: 'beacon'` para cero impacto en INP.

---

## 4. Activos Declarativos de Crecimiento (`M03` y `M04`)
- [`data/growth/lifecycle_flows.yaml`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/data/growth/lifecycle_flows.yaml): 3 flujos Brevo Evergreen (`welcome_segmented`, `helix_waitlist_nurture`, `post_purchase_lemonsqueezy`) 100 % bilingües ES/EN, ratio texto/imagen `> 80%`, HTML tabular limpio y cero `mailto:`.
- [`data/growth/launch_pack_obs_helix.yaml`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/data/growth/launch_pack_obs_helix.yaml): Playbooks EN-first para Product Hunt, Show HN, Reddit nicho (`r/supplychain`, `r/projectmanagement`, `r/ClaudeAI`, `r/Excel`), directorios IA/Awesome Lists y Plan de 4 semanas para LinkedIn Página de Empresa (`ADR-033` UTMs).

---

## 5. Invariantes y Criterios de Verificación
- **INV-AUTO-6 (Embargos):** `pack-obs` (`2026-12-09`), `reading` (`2026-12-16`) y `pack-sdd`/`suite-sdd`/`helix` (`2027-01-19`) permanecen estrictamente embargados sin `checkout_url` activa.
- **INV-HELIX-WL-4 (Cero `mailto:`):** Cero enlaces `mailto:` en `/recursos/`, `/resources/`, `layouts/apps/single.html` y `data/growth/*.yaml`.
- **Verification Gate:** `build_index` + `publish_public`, `pytest ops/helix/tests ops/pulse/tests autopilot/tests -v`, `hugo --renderToMemory`, `modern-web-guidance legacy-scan`, verificación headless Edge `1440×900` / `390×844` ES/EN y dictámenes `SECURITY_PASS`, `EDITORIAL_QA_PASS` y `QA_PASS`.
