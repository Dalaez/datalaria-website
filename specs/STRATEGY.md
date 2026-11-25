# STRATEGY.md — Estrategia Maestra y North Star de Datalaria (`Datalaria OS`)

> **Versión:** 1.0.0 · **Custodio:** [`00-chief-orchestrator`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-os/00-chief-orchestrator.md) · **Decisión:** `ADR-034`  
> **Higiene Anti-Bloat:** Máximo `80` líneas. Solo se carga en decisiones estratégicas, lanzamientos multi-escuadrón o revisiones mensuales (`INV-OS-1`).

---

## 1. Misión y North Star Metric
Convertir **Datalaria** en un proyecto digital autónomo capaz de generar ingresos pasivos crecientes que financien su evolución y la incorporación modular de nuevas capacidades agénticas, preservando **coste fijo de infraestructura `0 €/mes`** hasta consolidar flujo de caja positivo.

- **North Star Primaria:** **Ingresos Netos Mensuales en `€`** (Lemon Squeezy) + **Suscriptores Cualificados Activos** (Brevo ES/EN).
- **Métricas Tractoras Secundarias:** Clics orgánicos GSC (elevar CTR desde `0.58%` hacia `>= 2.0%`), Eventos Clave GA4/30d, Pull-Through Rate (`PTR >= 2%`) en comunidades y Seguidores reales en LinkedIn Página de Empresa.

---

## 2. Escalera de Monetización Híbrida (`EN-First`)
El `72.3%` de la visibilidad orgánica en Search Console procede de consultas en **inglés (EN)**. Toda iniciativa comercial prioriza posicionamiento, distribución y checkout **EN-First** manteniendo paridad bilingüe `ES ⇔ EN`:

| Peldaño | Oferta | Precio Objetivo | Rol Estratégico |
| :--- | :--- | :---: | :--- |
| **0. Captación** | Artículos técnicos + Sandboxes Dual-Mode gratis + Lead Magnets | `0 €` | Demostrar rigor cuantitativo en `< 3 s` y captar leads Brevo. |
| **1. Volumen** | Kits individuales (`pack-dafo..stock`) y Kits Software (`pack-pulse`, `pack-obs`, `pack-sdd`) | `5 € – 19 €` | Primera compra sin fricción (Early-Bird `19 €`, PVP `39 €`). |
| **2. Ticket Medio** | Suites Ejecutivas (`suite-01..03`) y `mega-bundle` | `15 € – 39 €` | Elevar AOV mediante ahorro visible y cross-sell post-compra. |
| **3. Margen B2B** | Licencias Equipo / Corporativas multi-asiento (5–20 usuarios) | `99 € – 249 €` | Multiplicar ingreso neto sin soporte 1-a-1. |
| **4. Escala** | Tier SaaS/Pro recurrente (Supabase) o Implementación B2B a medida | MRR / Proyecto | Activar solo tras validar tracción en Peldaños 1–3. |

---

## 3. Estadios de Madurez y Compuertas de Escalado de Equipos
Se prohíbe añadir nuevos agentes o costes fijos antes de cruzar la compuerta de ingresos correspondiente:

| Estadio | Horizonte | Meta Ingresos | Dotación Agéntica Autorizada |
| :--- | :---: | :---: | :--- |
| **Estadio 1 (Actual)** | Q4 2026 – Q2 2027 | `0 → 500 €/mes` | **Capa 0** (`00`) + **Helix** (12) + **Scriba** (8) + **Mercator Core** (`M01`–`M04`). |
| **Estadio 2 (Escala)** | Q2 2027 – 2028 | `500 → 2.500 €/mes` | Desbloquea `M05-brand-positioning` y `M06-customer-success`, afiliados y primer tier Pro/MRR. |
| **Estadio 3 (Autonomía)** | 2028+ | `> 2.500 €/mes` | Desbloquea Escuadrón **Aegis** (FinOps, Legal/Compliance, SLAs) y célula B2B Enterprise. |

---

## 4. Reglas de Asignación de Foco y Guilds Transversales
1. **Balance Demanda vs. Oferta:** Mientras los ingresos sean `< 500 €/mes`, al menos el **50 % de los hitos** priorizan captación, CRO, distribución externa y retención (`Scriba` + `Mercator`) frente a nuevas apps desde cero.
2. **Cero Releases Silenciosas (`INV-OS-3`):** Toda versión `MAJOR`/`MINOR` de Helix genera obligatoriamente acción en `E01` y `M01`.
3. **4 Guilds de Fuente Única:**
   - **Revenue & Pricing:** `M02` dicta oferta/pricing → `09-monetization` (Helix) y `E05-content-monetizer` (Scriba) ejecutan localmente.
   - **SEO & Inteligencia:** `E02` + `ops/pulse/` (`executive_state.json`) alimentan a `02`, `08`, `E04` y `M02`.
   - **Marca & Voz:** [`specs/_brand.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/_brand.md) gobierna todas las superficies públicas.
   - **Garantía & Privacidad:** `10-security-privacy`, `11-qa-verifier` y `E07-editorial-qa` retienen el veto exclusivo (`INV-HELIX-1`).
