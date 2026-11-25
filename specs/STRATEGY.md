# STRATEGY.md — Estrategia Maestra y North Star de Datalaria (`Datalaria OS`)

> **Versión:** 1.1.0 · **Custodio:** [`00-chief-orchestrator`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-os/00-chief-orchestrator.md) + Red-Team [`00B-board-advisor`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-os/00B-board-advisor.md) · **Decisiones:** `ADR-034`, `ADR-035`  
> **Higiene Anti-Bloat:** Máximo `80` líneas. Solo se carga en decisiones estratégicas, lanzamientos o auditorías (`INV-OS-1`).

---

## 1. Misión, 3 Horizontes Coexistentes y Telemetría Dual
Convertir **Datalaria** en un ecosistema digital autofinanciado que genere ingresos pasivos crecientes preservando **coste fijo `0 €/mes`** y operando simultáneamente 3 horizontes deliberados sin inversión externa:
1. **Hobby Premium / Career Equity:** Laboratorio personal/familiar y portfolio de ingeniería IA de élite (no prioritario, nunca a `0`).
2. **Estudio Bootstrapped (`Mercator Real`):** Motor actual hacia primeros ingresos reales en `€` con márgenes `> 90 %`.
3. **Spin-off SaaS B2B / Multi-Marca:** Evolución hacia software/agentes B2B y *Datalaria Media* financiada **100 % con ingresos propios**.

- **North Star:** **Ingresos Netos Mensuales (`€`, Lemon Squeezy)** + **Suscriptores Activos (Brevo ES/EN)**.
- **Telemetría en Doble Capa (`ADR-035`):** GA4 producción permanece intacto hasta la **1.ª venta** (curva motivacional); todas las decisiones de negocio leen en paralelo el **Tráfico Externo Neto** (sin `localhost`, spam ni `site:`), tráfico AI/GEO y `sync_revenue.py`.

---

## 2. Escalera de Monetización Híbrida (`EN-First`)
El `72.2%` de impresiones GSC son en inglés (**EN**). Prioridad **EN-First** con paridad `ES ⇔ EN`:

| Peldaño | Oferta | Precio Objetivo | Rol Estratégico |
| :--- | :--- | :---: | :--- |
| **0. Captación** | Artículos + Sandboxes Dual-Mode + *Helix Starter* (GitHub MIT) | `0 €` | Demostrar rigor en `< 3 s`, captar leads Brevo y backlinks GEO/SEO. |
| **1. Volumen** | Kits (`pack-dafo..stock`) y Kits Software (`pack-pulse`, `pack-obs`, `pack-sdd`) | `5 € – 19 €` | Primera compra sin fricción (Early-Bird `19 €`, PVP `39 €`) y testimonios. |
| **2. Ticket Medio** | Suites (`suite-01..03`), `mega-bundle` (`39 €`) y **Datalaria Apex (Q1 2027)** | `15 € – 79 €` | **Apex:** Consejo Directivo Agéntico C-Level sobre Suites 1–3 + `pack-obs` (`49 €` / Bundle `79 €`). |
| **3. Margen B2B** | Licencias Equipo / Corporativas (`5–20` usuarios: Kits, Helix y Apex) | `99 € – 299 €` | Multiplicar ingreso neto B2B sin soporte 1-a-1. |
| **4. Escala** | Tier SaaS/Pro recurrente (Supabase) o Implementación B2B a medida | MRR / Proyecto | Activar solo tras validar tracción en Peldaños 1–3. |

---

## 3. Estadios de Madurez, Reinversión Cash-Positive y Compuertas
- **Regla de Reinversión Cash-Positive (`ADR-035`):** Desde el `1.er €` neto, se autoriza reinvertir hasta `<= 50 %` del beneficio acumulado en capacidades agénticas (*Gemini Plus*, APIs, hardware) manteniendo siempre caja positiva y `0` deuda.
- **Compuerta Publicitaria y Multi-Marca:** Publicidad display/patrocinios y desdoblamiento hacia **Datalaria Media** (libros, podcasts, webs separadas) permanecen en *stand-by* hasta cruzar **Estadio 2 (`> 500 €/mes` sostenidos o `> 10.000` sesiones orgánicas netas/mes)**.

| Estadio | Horizonte | Meta Ingresos | Dotación y Desbloqueos Autorizados |
| :--- | :---: | :---: | :--- |
| **Estadio 1 (Actual)** | Q4 2026 – Q2 2027 | `0 → 500 €/mes` | **Capa 0** (`00` + `00B`) + **Helix** (12) + **Scriba** (8) + **Mercator** (`M01`–`M04`) · Dominio único `datalaria.com`. |
| **Estadio 2 (Escala)** | Q2 2027 – 2028 | `500 → 2.500 €/mes` | Desbloquea `M05`/`M06`, **Datalaria Media** / multi-marca, publicidad selectiva (`> 10k` netas) y primer tier SaaS/MRR. |
| **Estadio 3 (Autonomía)** | 2028+ | `> 2.500 €/mes` | Desbloquea Escuadrón **Aegis** (FinOps, Legal/Compliance, SLAs) y spin-off B2B Enterprise. |

---

## 4. Reglas de Foco (`70 / 20 / 10`) y Guilds Transversales
1. **Portfolio Balance `70 / 20 / 10` (`< 500 €/mes`):** **`70 %`** Armas B2B, Mercator y lanzamientos (`pack-obs`, `Helix`, `Apex`) · **`20 %`** Blog semanal amplio (`1` post/sem con bloque mid-article *«De la teoría a tu empresa»* → Kit/App + bloque GEO) · **`10 %`** *Open Lab* (máx. `1` hito ligero/mes).
2. **Validación Previa de Apex y Cero Releases Silenciosas (`INV-OS-3`):** Arrancar **Datalaria Apex** tras el `19 Ene` con `>= 3` señales reales de demanda; toda release `MAJOR`/`MINOR` dispara relevo a `E01` y `M01`.
3. **4 Guilds de Fuente Única:** **Revenue & Pricing** (`M02` → `09`/`E05`) · **SEO & Inteligencia** (`E02` + `ops/pulse/` Doble Capa → `00B`/`02`/`08`/`E04`/`M02`) · **Marca & Voz** (`specs/_brand.md`) · **Garantía & Privacidad** (`10`/`11`/`E07`, veto exclusivo `INV-HELIX-1`).
