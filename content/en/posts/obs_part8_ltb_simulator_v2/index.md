---
title: "IEC 62402 Radar (Part 8): BOM Graph & Last Time Buy vs Redesign Model"
date: 2026-12-09
draft: false
translationKey: "obs-part8-ltb-simulator-v2"
category: "Strategy & Operations"
categories: ["Operational Control", "Supply Chain", "AI, Engineering & Projects", "Strategy & Operations"]
tags: ["IEC 62402", "Obsolescence Management", "Last Time Buy", "LTB", "FFF Redesign", "BOM", "PCN", "PDN", "EOL", "Agentic Radar", "PostgreSQL RLS", "FastAPI"]
description: "How to operationalize IEC 62402 with Agentic Radar v2.0: cycle-free multilevel BOM traversal, deterministic Last Time Buy (LTB) vs. FFF redesign finance, and Safety Stock synergy."
summary: "Agentic Radar v2.0.0 major release (Zero-CDN Executive Risk Cockpit): cycle-safe BOM DAG engine, deterministic CAPEX Last Time Buy vs. Form-Fit-Function redesign modeling, browser-local CSV privacy, PostgreSQL obs_radar RLS isolation, and lifecycle handoff with recurring Safety Stock ROP."
cover:
  image: "cover.png"
  alt: "Agentic Radar v2.0: IEC 62402 Executive Risk Cockpit, BOM Graph Simulator & LTB vs. Redesign Calculator"
  caption: "Agentic Radar v2.0.0 — Zero-CDN Executive Risk Cockpit (< 34 KB gzip), Live PDN/BOM SVG Simulator & IEC 62402 B2B Kit."
  relative: true
images:
  - "cover.png"
  - "preview-pack.png"
  - "obs_lifecycle_relay.png"
---

Across advanced manufacturing, industrial electronics, medical devices, and aerospace boardrooms, there is one asymmetric financial risk capable of wiping out an entire fiscal year's EBITDA in weeks: **a discontinued EUR 2.15 multilayer ceramic capacitor or legacy microcontroller can halt shipments representing hundreds of thousands of euros in annual P&L gross margin**.

The moment a semiconductor vendor issues a formal **PDN** (*Product Discontinuance Notice*) or **EOL** (*End of Life*) alert, the executive committee immediately splits into two opposing camps:

1. **The Chief Operating Officer (COO) and Component Engineering Lead**, recognizing that zero qualified alternates exist on the Approved Manufacturer List (**AML**), push to approve an emergency 24- to 36-month bridge buy ahead of the factory cutoff date (*LTB Cutoff*) so assembly lines never stop.
2. **The Chief Financial Officer (CFO)** pushes back against an unbudgeted CAPEX outlay that locks vast cash reserves inside stagnant warehouses, drags down Weighted Average Cost of Capital (**WACC**), and carries scrap risk if end-product demand softens.

What turns this dilemma into boardroom paralysis is that most organizations attempt to evaluate End-of-Life notices using **flat spreadsheets and recurring inventory formulas**—a structural mistake that assumes a supplier will keep accepting quarterly purchase orders forever.

Across the first seven chapters of this engineering series ([Part 1: The Obsolescence Chessboard](/en/posts/obs_part1_intro/) through [Part 7: The Tactical Executive Dashboard](/en/posts/obs_part7_executive_dashboard/)), we engineered the core pillars of **Agentic Radar (`obs-management`)**: event-driven FastAPI ingestion, CrewAI semantic MPN extraction, and relational Bill of Materials (**BOM**) modeling in PostgreSQL.

Today we introduce **Agentic Radar `v2.0.0` (Zero-CDN Executive Risk Cockpit)** alongside our dedicated **`pack-obs` (*IEC 62402 Obsolescence, BOM Risk & LTB Decision Kit*)**. In this eighth installment, we examine our cycle-safe BOM DAG engine, the exact financial frontier separating **Last Time Buy (LTB)** from **Form-Fit-Function (FFF) Redesign**, multi-tenant **Row-Level Security (`obs_radar`)**, and—crucially—the exact operational handoff with recurring maturity inventory control (**Safety Stock & Reorder Point `pack-stock`**).

---

## 1. The Two-Stage Component Lifecycle Relay: `pack-stock` (Maturity ROP) vs. `pack-obs` (IEC 62402 / LTB Crisis)

One of the highest-cost errors we uncover during industrial supply chain audits is confusing **continuous stochastic inventory management during maturity** with **lifecycle obsolescence engineering during vendor discontinuation**. While both disciplines protect manufacturing continuity, they rely on mutually exclusive mathematical assumptions.

While a component remains **`Active`** (the vendor manufactures normally and accepts recurring monthly purchase orders), your core challenge is absorbing joint volatility in customer demand ($\sigma_d$) and supplier lead times ($\sigma_L$) through **Safety Stock ($SS_3$)**, **Reorder Point ($ROP$)**, and **Wilson Economic Order Quantity ($EOQ$)**—the exact scope automated by our [Safety Stock & Reorder Point Calculator (`pack-stock`)](/en/posts/safety-stock-reorder-point-calculator/), Pillar 5 of [Suite 03: Operational Control](/en/posts/operational-control-pmbok-quantitative-framework/).

However, the instant a **PCN** (*Product Change Notification*), **PDN**, or **EOL** lands in procurement, **the recurring Reorder Point ($ROP$) model ceases to apply**. The silicon line is shutting down permanently. Leaving automated ERP reorder triggers active produces rejected purchase orders, erratic MRP signals, or stranded sub-assemblies piling up as Dead Stock. Operational governance mandates an immediate switch: **freeze the recurring $ROP$ parameter for that part number** and hand execution over to the **IEC 62402** protocol.

{{< mermaid image="obs_lifecycle_relay.png" alt="Component Lifecycle Relay Diagram: Phase 1 Maturity (pack-stock APICS SS3/ROP/EOQ) vs. Phase 2 End-of-Life BOM Crisis (Agentic Radar v2.0 & pack-obs IEC 62402 LTB)" >}}
flowchart LR
    subgraph F1["PHASE 1 · MATURITY & CONTINUOUS FLOW (Active Vendor)"]
        A["pack-stock (EUR 7) / Suite 03 (EUR 22)<br/>APICS / ASCM & MIT CTL Standard<br/>Demand & Lead-Time Convolution (SS3)<br/>Dynamic Reorder Point (ROP)<br/>Wilson Economic Order Quantity (EOQ)"]
    end

    subgraph EV["LIFECYCLE DISRUPTION EVENT"]
        X["Vendor PCN / PDN / EOL Notice<br/>RULE: Freeze Automated ROP Immediately"]
    end

    subgraph F2["PHASE 2 · END-OF-LIFE & BOM CRISIS (Line Shuts Down)"]
        B["Agentic Radar v2.0 + pack-obs (EUR 19)<br/>International IEC 62402 Standard<br/>Multilevel BOM DAG (MPN to End SKU)<br/>One-Shot Bridge Buffer SS_LTB<br/>CAPEX Verdict: LTB (WACC) vs. FFF (NRE)"]
    end

    A -->|"Continuous MPN lifecycle watch"| X
    X -->|"Alert CRITICAL LTB REQUIRED"| B
    B -->|"Component redesigned (FFF)"| A

    style F1 fill:#0b1720,stroke:#10b981,stroke-width:2px,color:#f8fafc
    style EV fill:#261c0f,stroke:#f59e0b,stroke-width:2px,color:#f8fafc
    style F2 fill:#0b1324,stroke:#0ea5e9,stroke-width:2px,color:#f8fafc
{{< /mermaid >}}

To ensure Procurement, Component Engineering, and Finance know precisely which workbook to open in any boardroom review with zero overlap, this side-by-side matrix separates both kits cleanly:

| Operational Dimension | 📦 `pack-stock` (*Safety Stock & ROP Engine · €7*) | 📡 `pack-obs` (*IEC 62402 Obsolescence, BOM & LTB Kit · €19*) |
| :--- | :--- | :--- |
| **Lifecycle Stage** | **Maturity (`Active`):** Active supplier accepting recurring orders. | **Decline / Crisis (`NRND / PDN / EOL / Obsolete`):** Factory shutting down. |
| **Catalog Placement** | Pillar 5 of **Suite 03: Operations Control** (€22). | **Specialized Vertical Toolkit** paired with **Agentic Radar v2.0**. |
| **Global Standard** | **APICS / ASCM & MIT CTL** (Continuous review $(s, Q)$). | **IEC 62402 & JEDEC J-STD-048** (Obsolescence & PDN management). |
| **Structural Scope** | Individual warehouse SKU / replenishment policy. | **Multilevel BOM Graph** (`MPN → Internal PN → AML → Sub-Assembly → SKU`). |
| **Core Math Engine** | Stochastic $SS_3$ convolution, $ROP$ trigger, Wilson $EOQ$. | Cycle-safe BOM DAG traversal, IEC Criticality (0–100), $SS_{\text{LTB}}$ & LTB vs. FFF. |
| **Executive Question** | *What monthly buffer delivers a 98% fill rate without trapping cash?* | *Which end SKUs halt, and should we buy a 3-year LTB or fund NRE redesign?* |
| **`.ZIP` Deliverables** | 35-SKU Excel + Sawtooth Chart + 16:9 PPTX + 5-page PDF Guide. | 5-Sheet Dual Excel (ES/EN) + 5-page PDF Playbook + SQL RLS/Python/CSV Blueprint. |

---

## 2. Deterministic "Muscle": BOM DAG Traversal, IEC 62402 Criticality & LTB vs. FFF Math

In **Agentic Radar v2.0**, we enforce one strict quantitative governance law: **LLM agents (CrewAI) parse unstructured supplier emails, yet they never compute financial margins or traverse cost trees**. All critical math lives inside deterministic functions verified for exact numerical parity (`< €0.01` delta) across twin engines: `apps/obs-management/web/engine.js` (instant client-side execution) and `apps/obs-management/api/bom_engine.py` (server-side FastAPI verification).

### 2.1 Upward Multilevel BOM Traversal with Cycle Guard

In real ERP exports, one vendor `MPN` maps to an internal part number (`Internal Part`), which feeds multiple shared sub-assemblies across several commercial end products (`End SKU`). Even worse, legacy ERP extracts often harbor circular assembly references.

To eliminate infinite recursion and double-counted revenue exposure, our engine runs an **upward Depth-First Search (DFS)** maintaining a per-branch `visited` set and **strict `sku`-level deduplication** in the final P&L rollup:

1. **AML Resolution (*Approved Manufacturer List*):** Starting from an impacted MPN, the engine counts how many qualified alternate MPNs remain in `Active` status under the same `internal_part_id`. Active alternates immediately lower criticality.
2. **Cycle-Safe Recursive Propagation:** Walking upward through `bom_lines` toward parent assemblies, every hop executes `if next_part in visited: flag cycle_detected = True; continue`.
3. **Deduplicated P&L Exposure:** When a single end product (`DRONE-X1`, annual gross margin €12,500) consumes two different EOL capacitors on separate PCBs, the table exposes both engineering bottlenecks for remediation while counting €12,500 **exactly once** toward total P&L Margin at Risk.

### 2.2 Quantitative IEC 62402 Criticality Index (0–100)

Every impacted path receives an auditable 0–100 score visible in both the Cockpit's `IEC Formula` popover and tab `02_IEC62402_CRITICALITY` of the companion Excel workbook:

$$
C_{\text{IEC}} = \min\left(100,\; \text{AML}_{40} + \text{EOL}_{35} + \text{LT}_{15} + \text{PnL}_{10}\right)
$$

Where:
- **Single-Source AML Risk ($\text{AML}_{40}$):** `40` pts when zero active alternates exist (`alt_sources = 0`), `20` pts for 1 alternate, and `5` pts for $\ge 2$ qualified alternates.
- **Lifecycle Urgency ($\text{EOL}_{35}$):** `35` pts for `Obsolete`, `30` pts for `EOL`, `22` pts for `PDN`, `12` pts for `NRND`, and `0` pts for `Active`.
- **Lead-Time Exposure ($\text{LT}_{15}$):** `15` pts when `lead_time >= 24 weeks`, `10` pts for `12–23 weeks`, and `4` pts under `12 weeks`.
- **Financial P&L Impact ($\text{PnL}_{10}$):** `10` pts for high annual exposure (`>= €150,000/yr` or flagship threshold), `6` pts mid-tier, and `2` pts low exposure.

Any line scoring $C_{\text{IEC}} \ge 70$ triggers **`CRITICAL LTB REQUIRED`** and flags procurement to freeze recurring ERP $ROP$ replenishment immediately.

### 2.3 Financial Derivation: Last Time Buy (LTB) vs. Form-Fit-Function (FFF) Redesign

Once recurring $ROP$ is frozen, the CFO must evaluate the total economic cost of purchasing the remaining commercial product horizon ($H_{\text{months}}$) in one upfront transaction against funding engineering Non-Recurring Engineering ($NRE$) and regulatory recertification:

1. **One-Shot Bridge Buffer ($SS_{\text{LTB}}$) and Total Purchase Volume ($Q_{\text{LTB}}$):**
   Because no follow-on factory orders will be possible, cumulative demand uncertainty scales with the square root of the full remaining horizon ($H_{\text{months}}$):

$$
SS_{\text{LTB}} = \left\lceil Z \cdot \sigma_m \cdot \sqrt{H_{\text{months}}} \right\rceil \quad \Longrightarrow \quad Q_{\text{LTB}} = \left\lceil H_{\text{months}} \cdot D_m + SS_{\text{LTB}} \right\rceil
$$

2. **Total Financial Cost of Last Time Buy ($C_{\text{LTB}}$):**
   Captures immediate invoice cash-out ($Q_{\text{LTB}} \cdot P_{\text{LTB}}$) plus true working capital opportunity cost (**WACC**) and annual holding, insurance, and scrap decay ($h$) applied to average inventory held across the horizon ($H_{\text{months}} / 24$ years):

$$
C_{\text{LTB}} = \left(Q_{\text{LTB}} \cdot P_{\text{LTB}}\right) \cdot \left[ 1 + \left(\text{WACC} + h\right) \cdot \frac{H_{\text{months}}}{24} \right]
$$

3. **Total FFF Redesign Cost ($C_{\text{FFF}}$) and Break-Even Horizon ($T^*$):**
   Aggregates fixed engineering $\text{NRE}$, compliance recertification, and schedule stoppage exposure during engineering transition:

$$
C_{\text{FFF}} = \text{NRE} + \text{Recertification} + \text{Stoppage\_Risk} \quad \Longrightarrow \quad T^* = \frac{\text{NRE} + \text{Recertification}}{D_m \cdot P_{\text{LTB}} \cdot \left(1 + 0.5 \cdot (\text{WACC} + h)\right)}
$$

Applying a $\pm 8\%$ indifference tolerance band, the engine issues an unambiguous directive:
- If $C_{\text{LTB}} \le 0.92 \cdot C_{\text{FFF}}$: **`EXECUTE LTB`** (ideal for medical or aerospace assemblies carrying steep recertification fees).
- If $C_{\text{FFF}} \le 0.92 \cdot C_{\text{LTB}}$: **`REDESIGN FFF`** (high-volume flagship SKUs with $> 36$ months of remaining market life).
- Inside the $\pm 8\%$ indifference corridor: **`HYBRID BRIDGE`** (execute a 12-month tactical LTB while hardware engineering qualifies a pin-compatible alternate).

#### Audited Executive Case Study: `TI-CAP-10U-50` Discontinuation on `DRONE-X1-PRO`

Consider a live EOL alert hitting the critical single-source capacitor `TI-CAP-10U-50` ($D_m = 400\text{ units/mo}$, $\sigma_m = 65$, quoted Last Time Buy unit price $P_{\text{LTB}} = €1.85$, remaining product lifecycle horizon $H = 24\text{ months}$, target bridge service factor $Z = 1.96$ for $97.5\%$, annual $\text{WACC} + h = 18\%$, hardware engineering $\text{NRE} = €28,000$, and regulatory recertification $= €9,500$):

1. **One-Shot Bridge Buffer After Freezing ROP:** $SS_{\text{LTB}} = \lceil 1.96 \cdot 65 \cdot \sqrt{24} \rceil = 624\text{ units}$, setting the total bridge purchase order to $Q_{\text{LTB}} = 24 \cdot 400 + 624 = 10,224\text{ units}$.
2. **CAPEX Outlay & Total LTB Economic Cost:** Immediate invoice cash-out equals $€18,914.40$ plus $€3,404.59$ in working-capital WACC and warehouse decay across the two-year consumption window, yielding $C_{\text{LTB}} = €22,318.99$.
3. **FFF Redesign Comparison:** Against $€37,500$ in upfront engineering NRE and recertification alone—before accounting for transition stoppage exposure—the break-even horizon exceeds **46 months**. The engine delivers an unambiguous boardroom verdict: **`EXECUTE LTB`, delivering over `€15,180` in verified net economic savings** while keeping assembly lines uninterrupted and allowing procurement to freeze automated recurring $ROP$ replenishment cleanly without accumulating orphaned sub-assemblies or suffering unbudgeted factory downtime across the remainder of the product lifecycle.

---

## 3. Executive Risk Cockpit `v2.0.0`: Zero-CDN Architecture (< 34 KB gzip) & Browser-Local CSV Privacy

While `v1.0` relied on runtime `cdn.tailwindcss.com` scripts and a single static English view, **Agentic Radar `v2.0.0`** was rebuilt from the ground up following Google/MDN **Modern Web Guidance** and our *Executive Data-Dense* visual contract:

- **Zero External CDNs & Ultra-Light Shell (`33.03 KB` gzipped):** Every byte of `index.html`, `styles.css`, `i18n.js`, `engine.js`, `app.js`, `manifest.json`, and `sw.js` compiles cleanly from `apps/obs-management/web/` into `static/apps/obs-management/`. Zero third-party CDNs, crisp `tabular-nums` alignment, Dark/Light `<meta name="color-scheme">` synchronization, and strict WCAG 2.2 AA compliance (`<= 60 px` single-row header).
- **Installable 100% Offline PWA:** Includes vector `SVG` plus `any`/`maskable` PNG icons (80% safe zone) and a **Network-First** Service Worker keeping the Sandbox operable on factory floors with zero connectivity.
- **100% Native ES/EN Bilingualism (`?lang=es|en`):** Dynamically switches KPIs, currency formatting (`€33,850.00` vs. `33.850,00 €`), SVG BOM labels, financial verdicts, catalog links, and client-side Canvas-rendered **PNG `1200×630`** executive summary cards.
- **100% Browser-Local BOM CSV Importer (`<dialog>`):** Manufacturing Bills of Materials are fiercely guarded trade secrets. Our RFC-4180 parser runs **strictly in local browser RAM**, transmitting zero bytes to any backend server, and provides both template download and a **`Try sample industrial BOM (1 click)`** button.

---

## 4. Multi-Tenant Security & Backend Hardening: `obs_radar` PostgreSQL Schema with Real RLS

For engineering teams connecting the Cockpit to live corporate databases and automated distributor webhooks, the backend under `apps/obs-management/api/` was unified and hardened:

```sql
CREATE SCHEMA IF NOT EXISTS obs_radar;

-- Strict tenant isolation across all 6 relational BOM/EOL tables
ALTER TABLE obs_radar.products ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.internal_parts ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.bom_lines ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.aml ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.manufacturer_parts ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.eol_alerts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation_products" ON obs_radar.products
  FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
```

Additionally, our unified FastAPI backend (`main.py` + Pydantic v2 `models.py`) enforces four production guards:
1. **HMAC-SHA256 / Bearer Verification (`HTTP 401`):** Rejects unauthenticated inbound webhook payloads immediately.
2. **Anti-Prompt-Injection Boundaries in `obsolescence_agent.py`:** Unstructured supplier emails are encapsulated inside strict delimiter tags and validated via Pydantic schemas before touching SQL queries.
3. **Strict `ALLOWED_ORIGINS` CORS & `seeder_guard.py`:** Prevents test data generators from writing into production accounts.
4. **Automated Python–JS Math Parity Tests:** `pytest` asserts identical financial outputs (`< €0.01`) between `bom_engine.py` and `engine.js` across preset scenarios and circular BOM edge cases.

---

## 5. Launch the Live Simulator & Equip Your Executive Committee

Test an industrial obsolescence crisis or analyze your own `.csv` Bill of Materials privately right now in **Agentic Radar `v2.0.0`**:

{{< app-ref slug="obs-management" >}}

### The Complete Operations & Component Engineering Kit (`pack-obs`)

To deploy this methodology inside VBA-free corporate Excel workbooks, present boardroom CAPEX cases with an IEC 62402 normative Playbook, and integrate the PostgreSQL RLS Starter Blueprint (`obs_radar` SQL + `bom_engine.py` + compatible CSV), Early-Bird access opens on **Wednesday, December 9**:

{{< product-card
  title="IEC 62402 Obsolescence, BOM Risk & LTB Decision Kit"
  category="Supply Risk & IEC 62402"
  price="19€"
  original_price="39€"
  badge="📡 Launching Dec 9 • Pairs with pack-stock"
  icon="📡"
  status="coming"
  preview_image="preview-pack.png"
  preview_caption="Kit v2.0 Preview: Executive Risk Cockpit + 5-Page Vector PDF Playbook + 5-Sheet VBA-Free Dual Excel"
  deliverables="5-Sheet Dual Excel (0 VBA)|5-Page A4 PDF Playbook|SQL RLS + Python Starter Blueprint"
  features="Zero-VBA Dual ES/EN Excel workbook with 5 audited tabs (BOM/AML Explorer, IEC 62402 Criticality Matrix, LTB vs. FFF Redesign Simulator with SS_LTB bridge buffer after freezing ROP, CAPEX Mitigation Roadmap & C-Level Dashboard)|5-Page A4 Vector Executive PDF Playbook (ES & EN) featuring our pack-stock vs. pack-obs decision matrix|Complete Technical Starter Blueprint: PostgreSQL obs_radar schema with RLS on 6 tables, cycle-safe pure bom_engine.py, Pydantic v2 contracts & compatible CSV template for Agentic Radar v2.0"
  guide_url="/en/apps/obs-management/"
  guide_text="Launch Interactive Web App v2.0"
>}}
B2B toolkit engineered specifically for **discontinuation crises (PCN/PDN/EOL)** once recurring Reorder Points are frozen. Includes a built-in early-access modal inside the live Web App (`🚀 IEC 62402 Kit & B2B Pro Mode`).
{{< /product-card >}}

### Managing Recurring Inventory & Operations Control Too?

Combine lifecycle obsolescence defense with continuous operational control across all stages:

* **📦 For Continuous Flow During Maturity:** Size stochastic APICS safety buffers ($SS_3$), Reorder Points ($ROP$), and Wilson EOQ batches using our [Safety Stock & Reorder Point Calculator (`pack-stock` · €7)](/en/posts/safety-stock-reorder-point-calculator/) or download directly via [Lemon Squeezy Secure Checkout (€7)](https://datalaria.lemonsqueezy.com/checkout/buy/513e5cad-9f9f-4b53-a435-b511a846d79e?embed=1).
* **🛡️ For Single-Source Supplier Failure Protection:** Rank Severity × Occurrence × Detection (RPN) using the [Quantitative Risk Matrix & FMEA Pack (`pack-amfe` · €7)](https://datalaria.lemonsqueezy.com/checkout/buy/6eea6aa0-fe9f-440b-8bb9-6f29b303e57a?embed=1).
* **🏛️ For Full 5-Pillar Operations Control (5 Kits, 35% Savings):** Unlock RACI, FMEA, 3-Point PERT, EVM S-Curve, and Safety Stock/ROP inside [Suite 03: Operations Control (€22)](https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a?embed=1), detailed in the [5-Pillar Quantitative Operational Control Framework](/en/posts/operational-control-pmbok-quantitative-framework/).
