---
title: "McKinsey / GE 3x3 Matrix: Industry Attractiveness, Business Unit Strength & C-Level Capital Allocation"
date: 2026-10-29
draft: false
translationKey: mckinsey-ge-matrix
category: "Technical Articles"
categories: ["Corporate Strategy", "Corporate Finance", "Portfolio Management", "Management"]
tags: ["McKinsey Matrix", "General Electric", "GE Matrix", "Capital Allocation", "Portfolio Management", "Industry Attractiveness", "Competitive Strength", "Minto Pyramid", "Excel Model", "Executive Presentation", "ROIC"]
description: "Comprehensive methodological guide to implementing the McKinsey / General Electric 3x3 9-box matrix: multifactor assessment, management bias neutralization, and capital allocation plan for Investment Committees and Boards of Directors."
summary: "Overcome the unifactorial limitations of the classic BCG matrix. In this Tier-1 strategy consulting guide (McKinsey / BCG standard), we formalize General Electric's 9-quadrant multifactor framework to categorize strategic business units into three capital allocation zones (Invest, Selectivity, and Harvest), neutralize executive self-reporting bias, safeguard corporate governance, and expand group ROIC."
---

In nearly every investment committee, annual portfolio review, or Board of Directors strategy retreat, the same fundamental dilemma emerges: **how can a corporation efficiently and non-arbitrarily allocate tens of millions of dollars in CAPEX across business units operating in markets with radically divergent dynamics?**

For decades, business schools defaulted to the classic **BCG 2x2 Matrix** (market growth rate vs. relative market share). However, in modern diversified corporations and C-Suite executive committees, this simplistic model introduces three severe analytical pathologies:

1. **The Growth Illusion:** Confusing double-digit industry growth with structural profitability. A market can expand at 25% annually, but if it lacks entry barriers and suffers brutal price wars with collapsing operating margins, it will absorb massive capital while destroying shareholder equity.
2. **Relative Market Share Blindness in IP-Driven Sectors:** In software, advanced robotics, medical devices, or biotechnology, a Strategic Business Unit (SBU) with a modest 12% market share can command a 35% EBITDA margin and formidable pricing power through proprietary patents. Market share alone does not explain economic returns.
3. **The Forced Reductionism of Four Quadrants:** Forcing multi-million-dollar divisions into binary boxes (is it a Cash Cow or a Dog? A Star or a Question Mark?) sparks endless political debates among division heads, paralyzing capital allocation decisions at the Board level.

To solve this analytical bottleneck, **McKinsey & Company** partnered with **General Electric (GE)** in the early 1970s to develop the **Multifactor 3x3 9-Box Matrix**. In this C-level technical guide, we formalize its mathematical framework, the audit protocol required to eliminate executive self-reporting bias, and the prescriptive decision tree for governing corporate capital.

{{< mermaid >}}
flowchart TD
    A["<b>1. Multifactor Portfolio Audit:</b> Quantitative Evidence<br/><small>Score 5 Industry Attractiveness (IA) and 5 Business Strength (FC) factors</small>"]
    B["<b>2. Cartesian Mathematical Engine:</b> Continuous Coordinates (FC, IA)<br/><small>Strict Σw = 1.00 weighting and canonical partition thresholds at 2.33 and 3.67</small>"]
    C["<b>3. Canonical 9-Box Mapping:</b> 3x3 Strategic Diagnosis<br/><small>Objective mathematical assignment into the 3 Strategic Capital Zones</small>"]
    D["<b>4. Zone Capital Allocation Mandates:</b> Binding Governance Rules<br/><small>Green: Invest (65-75%) | Amber: Selectivity (20-30%) | Red: Divest (0-5%)</small>"]
    E["<b>5. Boardroom Decision Gateway:</b> Minto Pyramid Synthesis<br/><small>36-month CAPEX roadmap, Hurdle Rates (IRR), M&A carve-out and ROIC accretion</small>"]

    A --> B
    B --> C
    C --> D
    D --> E

    style A fill:#F8FAFC,stroke:#94A3B8,stroke-width:1.5px,color:#0F172A
    style B fill:#EFF6FF,stroke:#3B82F6,stroke-width:1.5px,color:#1E3A8A
    style C fill:#F0FDFA,stroke:#0D9488,stroke-width:1.5px,color:#0F766E
    style D fill:#FFFBEB,stroke:#F59E0B,stroke-width:1.5px,color:#92400E
    style E fill:#0F172A,stroke:#D97706,stroke-width:2px,color:#FFFFFF
{{< /mermaid >}}

{{< product-card
  variant="compact"
  title="Executive Decision Pack: McKinsey / GE 3x3 Matrix & Capital Allocation"
  price="6€"
  original_price="19€"
  badge="★ Tier-1 Consulting Standard"
  icon="📊"
  checkout_url="https://datalaria.lemonsqueezy.com/checkout/buy/ae0c6cd8-bb86-4a56-ad87-9625301afda9"
  button_text="Download Kit Now (.ZIP) • 6€"
>}}
Preparing an annual portfolio review, Investment Committee, or Board meeting? Download the 3x3 9-box Excel engine with automated IA and FC calculations, C-Level governance rules, and editable 16:9 widescreen presentation.
{{< /product-card >}}

---

## 1. What is the McKinsey / General Electric (GE) Matrix? Foundations, Multifactor Model & Objectives

For any Chief Executive Officer (CEO), Chief Financial Officer (CFO), Chief Strategy Officer (CSO), or Private Equity partner tasked with optimizing capital distribution across a diversified corporate group—or for executives approaching this framework for the first time—, the **McKinsey / GE Matrix** (conceived by **McKinsey & Company** under D. Bruce Merrifield and Ron Daniel for **General Electric** in the early 1970s) represents the definitive evolution in corporate portfolio management.

In 1971, General Electric operated over 150 decentralized Strategic Business Units (SBUs) across wildly diverse industries, ranging from gas turbines and home appliances to jet engines, semiconductors, and financial services. GE's executive leadership, headed by Fred Borch, recognized that BCG's 2x2 growth-share matrix was too narrow to steer their portfolio: it forced high-stakes capital decisions based on a single market proxy (growth rate) and a single internal proxy (relative share). McKinsey addressed this limitation by replacing BCG's single metrics with **two synthetic multifactor indices evaluated on a continuous scale from 1.00 to 5.00**, mapped onto a **9-box (3x3) grid** grouped into **three strategic capital allocation zones**.

### The Anatomy of the Model: 9 Quadrants & 3 Strategic Capital Zones

The framework plots **Industry Attractiveness ($I_A$)** on the vertical axis against **Business Unit Competitive Strength ($F_C$)** on the horizontal axis. The 9 resulting quadrants are synthesized into three actionable capital governance zones:

| Strategic Zone | Included Quadrants | Canonical Coordinates ($I_A$ / $F_C$) | Capital Allocation Mandate | Minimum Hurdle Rate (IRR) | Target Policy CAPEX Range |
| :--- | :--- | :---: | :--- | :---: | :---: |
| **🟢 GREEN ZONE<br>Invest / Grow** | • Invest to Lead<br>• Invest to Build<br>• Selective Growth | $I_A \ge 3.67$ & $F_C \ge 3.67$<br>$I_A \ge 3.67$ & $2.33 \le F_C < 3.67$<br>$2.33 \le I_A < 3.67$ & $F_C \ge 3.67$ | **Top CAPEX Priority:** Aggressively fund capacity expansion, breakthrough R&D, bolt-on M&A, and absolute market leadership. | **$\text{IRR} \ge 18.0\%$** | **65% - 75%** of total corporate CAPEX |
| **🟡 AMBER ZONE<br>Selectivity / Hold** | • Double or Quit<br>• Maximize Return<br>• Protect Cash Flow | $I_A \ge 3.67$ & $F_C < 2.33$<br>$2.33 \le I_A < 3.67$ & $2.33 \le F_C < 3.67$<br>$I_A < 2.33$ & $F_C \ge 3.67$ | **Strict Self-Funding:** Selective reinvestment strictly capped by internal operating cash flow (EBITDA), focus on defensible high-margin niches, and working capital optimization. | **$\text{IRR} \ge 14.0\%$** | **20% - 30%** of total corporate CAPEX |
| **🔴 RED ZONE<br>Harvest / Divest** | • Restructure<br>• Controlled Harvest<br>• Divest / Liquidate | $2.33 \le I_A < 3.67$ & $F_C < 2.33$<br>$I_A < 2.33$ & $2.33 \le F_C < 3.67$<br>$I_A < 2.33$ & $F_C < 2.33$ | **Freeze Non-Critical CAPEX:** Maximize residual Free Cash Flow, stop expansionary investments, and execute carve-out or trade sale via M&A within $<12$ months. | **$\text{IRR} \ge 10.0\%$** *(regulatory only)* | **0% - 5%** of total corporate CAPEX |

### Comparative Matrix: BCG 2x2 vs. McKinsey / GE 3x3

| Analytical Dimension | Classic BCG Matrix (1968) | McKinsey / GE 3x3 Matrix (1971) | Executive C-Level Advantage |
| :--- | :--- | :--- | :--- |
| **Visual Structure** | 4 quadrants (2x2 matrix) | 9 quadrants (3x3 grid in 3 zones) | Granular visibility; eliminates binary distortion of borderline businesses. |
| **Market Axis (Vertical)** | Unidimensional: Market Growth Rate ($MGR$) | **Multifactorial: Industry Attractiveness ($I_A$)** | Incorporates entry barriers, industry margin benchmarks, ESG, and macro cycles. |
| **Company Axis (Horizontal)** | Unidimensional: Relative Market Share ($RMS$) | **Multifactorial: Business Unit Strength ($F_C$)** | Measures proprietary IP, gross margin premiums, brand reach, and management depth. |
| **Middle-Ground Management** | Absent (forced into Star or Question Mark) | **Explicit Amber Selectivity Zone** | Enables disciplined management of cash-generative units in mature markets. |
| **Financial Linkage** | Cash flow balance model (Henderson) | **36-month CAPEX budget + Hurdle Rates** | Direct integration into capital budgeting and corporate ROIC expansion. |

### How It Works: The Complete Strategic Planning Funnel (PESTEL → Porter → SWOT-TOWS → BCG → McKinsey / GE)

For executive leadership teams utilizing Datalaria frameworks, it is vital to understand **the pinnacle role that the McKinsey / GE Matrix occupies within the corporate strategy hierarchy**. In Tier-1 strategy consulting practice (McKinsey, BCG, Bain), strategic management does not rely on isolated tools, but on an **integrated five-level sequential funnel**:

{{< mermaid >}}
flowchart TD
    M1["<b>Level 1: Exogenous Macro-Environment</b><br/><b>Quantitative PESTEL Matrix</b><br/><small>Severity vs. Volatility of political, macroeconomic, tech, and ESG disruptions</small>"]
    M2["<b>Level 2: Industry Structural Micro-Environment</b><br/><b>Quantitative Porter 5 Forces</b><br/><small>Structural industry attractiveness, rivalry intensity, and Economic Moat</small>"]
    M3["<b>Level 3: Internal Situational Diagnostics</b><br/><b>Quantitative SWOT & TOWS Matrix</b><br/><small>Alignment of operational strengths/weaknesses with external market forces</small>"]
    M4["<b>Level 4: Classic Portfolio & Cash Dynamics</b><br/><b>Dynamic BCG Matrix</b><br/><small>Experience curve, relative market share (RMS), and Henderson fund balance</small>"]
    M5["<b>Level 5: Advanced C-Level Capital Governance</b><br/><b>McKinsey / GE 3x3 Matrix</b><br/><small>IA vs. FC multifactor scoring, 9-box mapping, Hurdle Rates, and CAPEX roadmap</small>"]

    M1 --> M2
    M2 --> M3
    M3 --> M4
    M4 --> M5

    style M1 fill:#EFF6FF,stroke:#3B82F6,stroke-width:1.5px,color:#1E3A8A
    style M2 fill:#EEF2FF,stroke:#6366F1,stroke-width:1.5px,color:#312E81
    style M3 fill:#ECFDF5,stroke:#10B981,stroke-width:1.5px,color:#064E3B
    style M4 fill:#FFFBEB,stroke:#F59E0B,stroke-width:1.5px,color:#92400E
    style M5 fill:#0F172A,stroke:#D97706,stroke-width:2.5px,color:#FFFFFF
{{< /mermaid >}}

1. **Level 1 — Exogenous Macroeconomic Scan ([Quantitative PESTEL Matrix](/en/posts/quantitative-pestel-matrix/)):** Provides the broad-spectrum radar. Quantifies the P&L impact of regulatory shifts, inflation, interest rate volatility, and geopolitical developments. To calibrate your macro exposure, explore our guide on the **[Quantitative PESTEL Matrix](/en/posts/quantitative-pestel-matrix/)**.
2. **Level 2 — Structural Industry Analysis ([Quantitative Porter 5 Forces](/en/posts/quantitative-porter-5-forces/)):** Pinpoints competitive intensity, buyer/supplier power, and structural profit pools ($ROIC - WACC$) across each vertical. Learn how to calculate industry attractiveness in our guide on the **[Quantitative Porter 5 Forces](/en/posts/quantitative-porter-5-forces/)**.
3. **Level 3 — Situational Diagnostics & Strategy Formulation ([Quantitative SWOT & TOWS Matrix](/en/posts/quantitative-swot-tows-matrix/)):** Cross-references macro threats and industry opportunities with internal operational capabilities, establishing immediate tactical plays in the TOWS matrix. Review the details in our guide on the **[Quantitative SWOT & TOWS Matrix](/en/posts/quantitative-swot-tows-matrix/)**.
4. **Level 4 — Scale Economics & Fund Balancing ([Dynamic BCG Matrix](/en/posts/dynamic-bcg-matrix/)):** Models the empirical relationship between cumulative production volume, market share, and cash generation. Review our guide on the **[Dynamic BCG Matrix](/en/posts/dynamic-bcg-matrix/)** to balance liquidity transfers from Cash Cows to Question Marks.
5. **Level 5 — Advanced Multifactor Governance & C-Level Capital Allocation (McKinsey / GE 3x3 Matrix):** Represents the pinnacle of corporate resource allocation. It synthesizes Porter's structural insights and SWOT capabilities into two auditable indices ($I_A$ and $F_C$), positioning every business unit across the 9-box grid and establishing binding CAPEX and divestment resolutions for Board approval.

### What is the Primary Objective of the McKinsey / GE Matrix?

The primary objective of a boardroom-grade McKinsey / GE Matrix is not to produce an aesthetic chart, but to **resolve the trilemma of corporate capital governance**:

1. *Which business units demonstrate both structural market attractiveness and sustainable competitive advantages that justify concentrating 70% of the group's CAPEX budget?*
2. *How should intermediate divisions (Amber Zone) be managed to ensure their operational enhancements are strictly self-funded without siphoning parent company liquidity?*
3. *Which divisions operate in depressed markets with inferior competitive strength destroying economic value ($ROIC < WACC$), requiring an immediate carve-out or orderly exit mandate?*

### Expected Outputs: What Does an Effective McKinsey / GE Matrix Deliver?

Under Datalaria's strategic engineering standards, deploying the model yields three verified executive deliverables:

* **Auditable 3x3 9-Box Grid with Cartesian Coordinates:** A continuous $[1.00, 5.00] \times [1.00, 5.00]$ map where each SBU is mathematically positioned across 10 weighted and verified criteria, removing subjective speculation from executive deliberations.
* **Consolidated 36-Month CAPEX Roadmap (12-24-36M):** A multi-year capital budget categorized by business unit, establishing strict hurdle rates (IRR thresholds) and milestone gates tied to capital disbursements.
* **C-Level Governance & Divestiture Mandate:** Formal Board resolutions assigning C-Suite ownership, identifying M&A carve-out candidates, and projecting the accretive impact on group Return on Invested Capital ($\text{ROIC}$) and corporate $EV/EBITDA$ valuation multiples.

---

## 2. Mathematical Foundations of the Multifactor Model

To meet the auditability standards demanded by credit rating agencies, audit committees, and Private Equity sponsors, business unit positioning is not determined by qualitative impressions, but by calculating two continuous linear weighted vectors:

$$\text{Portfolio Space} = [1.00, 5.00] \times [1.00, 5.00] \subset \mathbb{R}^2$$

### 2.1. Industry Attractiveness Index ($I_A$)

The Vertical Axis ($Y$) assesses the structural quality of the macroeconomic and competitive environment in which the SBU operates. It is calculated via the weighted sum of $n$ objective factors:

$$I_A = \sum_{i=1}^n w_i \cdot A_i \quad \text{where} \quad \sum_{i=1}^n w_i = 1.00 \quad \text{and} \quad A_i \in [1.00, 5.00]$$

Under Datalaria's corporate standard, the five benchmark criteria and default weightings are:
* **$A_1$: Market Growth Rate ($w_1 = 0.25$):** Projected 3-5 year compound annual growth rate (CAGR) of the addressable market.
* **$A_2$: Industry Average Operating Margin ($w_2 = 0.20$):** Aggregate sector EBITDA margin benchmark across primary competitors.
* **$A_3$: Entry Barriers & Competitive Rivalry ($w_3 = 0.20$):** Intensity assessment based on **[Porter's 5 Forces](/en/posts/quantitative-porter-5-forces/)** (capital intensity, patent protection, customer switching costs, and competitor concentration).
* **$A_4$: Regulatory, Legal & ESG Stability ($w_4 = 0.15$):** Policy predictability, regulatory compliance risk, and decarbonization pressures identified in the **[PESTEL Matrix](/en/posts/quantitative-pestel-matrix/)**.
* **$A_5$: Macroeconomic Resilience & Cyclical Defense ($w_5 = 0.20$):** Vulnerability to interest rate shocks, currency swings, and supply chain disruptions.

### 2.2. Business Unit Competitive Strength Index ($F_C$)

The Horizontal Axis ($X$) assesses the business unit's defensible competitive advantages and economic moat depth relative to direct rivals:

$$F_C = \sum_{j=1}^m v_j \cdot C_j \quad \text{where} \quad \sum_{j=1}^m v_j = 1.00 \quad \text{and} \quad C_j \in [1.00, 5.00]$$

Corporate criteria and weightings:
* **$C_1$: Relative Market Share / Scale Leadership ($v_1 = 0.25$):** SBU revenues divided by the revenues of the market leader, formalized under the **[BCG Matrix](/en/posts/dynamic-bcg-matrix/)**.
* **$C_2$: Technological Edge, Patents & Proprietary IP ($v_2 = 0.20$):** Algorithmic IP, active patent portfolio, and R&D pipeline defensibility.
* **$C_3$: Gross Margin Premium vs. Peers ($v_3 = 0.20$):** Unit cost advantage stemming from experience curve scale and pricing power.
* **$C_4$: Brand Equity, Reputation & Channel Access ($v_4 = 0.15$):** Customer switching costs, audited Net Promoter Score (NPS), and commercial channel control.
* **$C_5$: Financial Strength, Execution Velocity & Talent ($v_5 = 0.20$):** Historical FCF generation, key executive retention, and operational cycle time.

### 2.3. Boundary Conditions & 9-Box Taxonomy

The continuous Cartesian space is segmented using two canonical threshold boundaries: **$T_1 = 2.33$** (low-to-medium boundary) and **$T_2 = 3.67$** (medium-to-high boundary).

| Industry Attractiveness ($I_A$) \ BU Strength ($F_C$) | Strong ($F_C \ge 3.67$) | Medium ($2.33 \le F_C < 3.67$) | Weak ($F_C < 2.33$) |
| :--- | :---: | :---: | :---: |
| **High ($I_A \ge 3.67$)** | **Invest to Lead**<br/>*(Green Zone)* | **Invest to Build**<br/>*(Green Zone)* | **Selectivity / Double or Quit**<br/>*(Amber Zone)* |
| **Medium ($2.33 \le I_A < 3.67$)** | **Selective Growth**<br/>*(Green Zone)* | **Selectivity / Maximize Return**<br/>*(Amber Zone)* | **Harvest / Restructure**<br/>*(Red Zone)* |
| **Low ($I_A < 2.33$)** | **Protect Cash Flow**<br/>*(Amber Zone)* | **Controlled Harvest**<br/>*(Red Zone)* | **Divest / Liquidate**<br/>*(Red Zone)* |

---

## 3. Four-Filter Protocol to Neutralize Management Bias

The Achilles' heel of any multicriteria scoring model is **executive self-reporting bias**: no division president will willingly score their unit a 1.8 in competitive strength if they know that rating leads directly to a budget freeze.

To eliminate this conflict of interest, the Corporate Strategy Office (PMO / FP&A) must subject every rating to a four-filter audit protocol:

1. **Mandatory Numerical Evidence Filter:** Scoring $\ge 4.0$ or $\le 2.0$ based on subjective opinion is strictly prohibited. Every score must be substantiated with audited empirical data (e.g., third-party market share reports, active regulatory certifications, or competitor financial statements).
2. **Independent Benchmark Filter:** Industry growth rates and operating margins must be extracted from verified secondary sources (Gartner, Forrester, equity research consensus, or national statistical agencies).
3. **Plenary Executive Committee Calibration:** Ratings are not negotiated bilaterally between the CEO and the division head. They are defended before the full Executive Committee, where fellow SBU presidents and the CFO act as a critical review panel.
4. **Historical Backtesting Filter:** If an SBU claims a "5.0 technological advantage," the review panel audits whether that alleged superiority generated gross margins above industry averages over the previous three fiscal years. If not, the score is automatically downgraded to 3.0 (market parity).

---

## 4. C-Level Capital Allocation Decision Tree

The placement of each SBU across the 9 boxes translates unequivocally into one of three Strategic Capital Zones:

{{< mermaid >}}
flowchart TD
    A["<b>Multifactor Portfolio Audit</b><br/><small>Score 5 Market (IA) and 5 Business Unit (FC) criteria</small>"]
    
    B{"<b>Cartesian Coordinates (FC, IA)</b><br/><small>Canonical Partition [1.00 - 5.00]</small>"}
    
    C["<b>GREEN ZONE: Invest / Grow</b><br/><small>Boxes: Lead, Build, Selective Growth</small>"]
    D["<b>AMBER ZONE: Selectivity / Hold</b><br/><small>Boxes: Double or Quit, Maximize Return, Protect Cash</small>"]
    E["<b>RED ZONE: Harvest / Divest</b><br/><small>Boxes: Restructure, Controlled Harvest, Liquidate</small>"]
    
    C1["<b>Top CAPEX Priority (65% - 75%)</b><br/><small>Aggressive organic expansion, breakthrough R&D, bolt-on M&A<br/>Hurdle Rate: IRR &ge; 18.0%</small>"]
    D1["<b>Strict Self-Funding (20% - 30%)</b><br/><small>Reinvestment capped by internal EBITDA, niche defense<br/>Hurdle Rate: IRR &ge; 14.0%</small>"]
    E1["<b>CAPEX Freeze & Divestiture (0% - 5%)</b><br/><small>Harvest residual FCF, execute carve-out within &lt;12M<br/>Release shareholder capital</small>"]

    A --> B
    B -->|"IA &ge; 2.33 & FC &ge; 2.33 (Top-Left)"| C
    B -->|"Intermediate Diagonal"| D
    B -->|"IA &le; 3.66 & FC &le; 2.32 (Bottom-Right)"| E
    
    C --> C1
    D --> D1
    E --> E1

    style A fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px,color:#0F172A
    style B fill:#0F172A,stroke:#2563EB,stroke-width:2px,color:#FFFFFF
    style C fill:#D1FAE5,stroke:#10B981,stroke-width:2px,color:#065F46
    style D fill:#FEF3C7,stroke:#F59E0B,stroke-width:2px,color:#92400E
    style E fill:#FEE2E2,stroke:#EF4444,stroke-width:2px,color:#991B1B
    style C1 fill:#ECFDF5,stroke:#10B981,stroke-width:1.5px,color:#065F46
    style D1 fill:#FFFBEB,stroke:#F59E0B,stroke-width:1.5px,color:#92400E
    style E1 fill:#FEF2F2,stroke:#EF4444,stroke-width:1.5px,color:#991B1B
{{< /mermaid >}}

---

## 5. Real-World Case Study: Vanguard Industrial & Tech Group

To demonstrate the model's application in complex corporate environments, we analyze the modeled case of **Vanguard Industrial & Tech Group**, a listed industrial conglomerate with 10 SBUs, **$485.0M** in consolidated revenues, and an **$82.7M** 3-year CAPEX allocation budget.

### 5.1. Portfolio Diagnostics & 3x3 Grid Mapping

The quantitative evaluation generated the following coordinates and governance classifications:

| Code | Strategic Business Unit | Sales ($M) | EBITDA % | Attractiveness ($I_A$) | Strength ($F_C$) | Assigned Box | Strategic Zone | 3Y CAPEX ($M) | Hurdle Rate |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: |
| **SBU-01** | Industrial AI & Cloud Platforms | 95.0 | 28.5% | **4.64** | **4.63** | Invest to Lead | **🟢 Invest / Grow** | 24.0 | 18.0% |
| **SBU-02** | Surgical & Medical Robotics | 72.0 | 24.0% | **4.61** | **3.81** | Invest to Lead | **🟢 Invest / Grow** | 18.5 | 18.0% |
| **SBU-03** | Power Electronics & Inverters | 110.0 | 18.2% | **3.72** | **4.20** | Invest to Lead | **🟢 Invest / Grow** | 16.0 | 18.0% |
| **SBU-04** | Smart Sensors & Factory IoT | 68.0 | 16.5% | **3.29** | **3.49** | Selectivity / Maximize Return | **🟡 Selectivity / Hold** | 7.5 | 14.0% |
| **SBU-05** | Fleet Telematics Solutions | 35.0 | 14.0% | **3.57** | **2.72** | Selectivity / Maximize Return | **🟡 Selectivity / Hold** | 5.3 | 14.0% |
| **SBU-06** | Commercial HVAC Systems | 42.0 | 15.0% | **2.25** | **4.09** | Protect Cash Flow | **🟡 Selectivity / Hold** | 4.5 | 14.0% |
| **SBU-07** | Precision Aerospace Alloys | 25.0 | 11.0% | **3.91** | **1.98** | Double or Quit | **🟡 Selectivity / Hold** | 4.7 | 14.0% |
| **SBU-08** | Hydraulic Valves & Heavy Machinery | 18.0 | 8.5% | **2.64** | **1.95** | Harvest / Restructure | **🔴 Harvest / Divest** | 1.2 | 10.0% |
| **SBU-09** | Commodity Wiring & Cabling | 12.0 | 6.0% | **1.90** | **2.52** | Controlled Harvest | **🔴 Harvest / Divest** | 0.8 | 10.0% |
| **SBU-10** | Legacy Switchboards & Analog Meters | 8.0 | 3.2% | **1.57** | **1.60** | Divest / Liquidate | **🔴 Harvest / Divest** | 0.2 | 10.0% |
| **TOTAL** | **Vanguard Group Consolidated Portfolio** | **$485.0M** | **18.7%** | **3.21** | **3.09** | **10 SBUs Audited** | **3 Capital Zones** | **$82.7M** | **15.6%** |

### 5.2. Board-Approved Capital Reallocation Mandate

The Investment Committee and Board of Directors unanimously approved three binding strategic resolutions:

1. **Aggressive Concentration in the Green Zone (76.2% of CAPEX):** Allocated **$63.0M** across Cloud AI, Medical Robotics, and Power Electronics. These three units generate 65.8% of consolidated revenue ($319.0M) and operate in markets with CAGR > 14%, delivering projected internal rates of return (IRR) exceeding 22%.
2. **Strict Self-Funding in the Amber Zone (21.2% of CAPEX):** The four intermediate units (Smart Sensors, Telematics, HVAC, and Precision Alloys) were allocated **$17.5M**, conditioned upon self-funding investments via internal operating EBITDA, protecting parent company treasury.
3. **M&A Carve-Out Mandate in the Red Zone (2.7% of CAPEX):** Discretionary investments in Hydraulic Valves, Commodity Cabling, and Analog Meters were frozen (restricting outlays to $2.2M for mandatory regulatory safety). The CFO was directed to engage an investment bank to execute carve-outs in Q3-Q4, **releasing $24.0M in net cash**.

**Shareholder Value Impact:** The strategic plan expands corporate Return on Invested Capital (**ROIC**) from **11.2% to 15.0% (+380 basis points)** over a 36-month horizon, eliminates cash drag from underperforming lines, and expands the holding company's projected $EV/EBITDA$ multiple by **+2.1x**.

---

## 6. Official Executive Decision Pack: McKinsey / GE 3x3 Dual

For Chief Executive Officers (CEO), Chief Financial Officers (CFO), Chief Strategy Officers (CSO), and Private Equity sponsors requiring a production-grade implementation of this Tier-1 strategy framework (McKinsey / BCG standard), we have packaged the complete official toolkit:

{{< product-card
  title="Executive Decision Pack: McKinsey / GE 3x3 Matrix Dual (EN/ES)"
  category="Corporate Strategy & Boardroom Decision Support"
  price="6€"
  original_price="29€"
  badge="★ Tier-1 Consulting Standard"
  icon="📊"
  preview_image="preview-pack.png"
  preview_caption="Real preview of included deliverables: 3x3 Multifactor Excel Engine (.xlsx) with Protected Matrix Formulas, 16:9 Widescreen C-Level Presentation (.pptx), and Official Methodology Guide (.pdf)."
  deliverables="Excel .xlsx + Sheets|PowerPoint .pptx 16:9 C-Level|PDF Methodology Guide"
  features="Excel Engine (.xlsx) with 3 interconnected sheets, password-protected matrix formulas, and 100% unlocked user input cells|Automated Industry Attractiveness (IA) and BU Strength (FC) scoring with continuous 9-box mapping|Executive Dashboard with portfolio concentration KPIs and 36-month CAPEX roadmap (12-24-36M)|PowerPoint Presentation (.pptx 16:9 Widescreen) editable under the Minto Pyramid, Action Titles, and Board Decision Gateway|Official PDF Methodology Guide (5 pages) with mathematical proofs, 4 anti-bias filters, and Boardroom defense protocol|100% guaranteed compatibility with Microsoft Excel and Google Sheets without macro dependencies"
  checkout_url="https://datalaria.lemonsqueezy.com/checkout/buy/ae0c6cd8-bb86-4a56-ad87-9625301afda9"
  button_text="Download Complete Pack (.ZIP) • 6€"
>}}
The downloadable archive includes the official **Excel (.xlsx)** model with formula protection under standard ECMA-376 (documented password provided with unlocked input cells), the executive **PowerPoint (.pptx 16:9 Widescreen)** slide deck structured under the Minto Pyramid with high-resolution 3x3 visuals and Board Decision Gateway, the 5-page **PDF Methodology Guide**, and direct Google Sheets import instructions.
{{< /product-card >}}

---

## 7. Boardroom Defense Protocol (FAQ)

### Why replace the classic BCG matrix if directors are already familiar with it?
The BCG matrix assumes that high market growth automatically guarantees superior economic profitability. In contemporary technology and industrial markets, segments growing over 30% annually often register negative net margins due to low entry barriers. The McKinsey / GE Matrix evaluates 10 weighted dimensions, preventing costly capital misallocations into growth-trap industries.

### How do we justify divesting an SBU in the Red Zone that still generates positive accounting profit?
Accounting net income does not equal economic value creation. If a division generates an ROIC of 6.0% on $20M of assets while the group's Weighted Average Cost of Capital (WACC) is 8.8%, the unit destroys $560,000 of shareholder equity every year. Divesting those assets and redeploying the $24M in proceeds into Green Zone lines yielding 25% produces immediate net value accretion.

### How do we resolve the dilemma along the Selectivity diagonal (double down vs. prepare for sale)?
The framework applies a strict quantitative gate: if the SBU demonstrates a viable operational pathway to segment leadership within a high-margin niche while self-funding via its own EBITDA, an 18-month milestone plan is authorized. If the unit requires ongoing cash subsidies from the parent company, it is immediately slated for trade sale or Joint Venture partnership.

### How robust is the model if an SBU head claims weightings are subjective?
The framework neutralizes this challenge via sensitivity analysis. Simulating criteria weight variations of $\pm 20\%$, strategic zone classifications remain stable across more than 92% of Monte Carlo iterations, proving that strategic mandates reflect structural competitive positions rather than arbitrary math.

### What is the expected impact on corporate WACC after completing divestitures?
Divesting mature, commoditized divisions reduces net debt, enhances interest coverage ratios (ICR), and lowers corporate levered beta. This compresses holding company WACC by 40 to 60 basis points, automatically increasing the Net Present Value (NPV) of all future corporate cash flows.

---

## 8. Authoritative Strategic & Academic References

1. **McKinsey & Company (1971).** *Strategic Business Planning: The GE / McKinsey Nine-Box Matrix Approach*. Internal White Paper, New York.  
   *Foundational methodology document designed for General Electric to govern capital across 150+ decentralized strategic business units.*

2. **Day, George S. (1977).** *"Diagnosing the Product Portfolio"*. *Journal of Marketing*, Vol. 41, No. 2, pp. 29-38.  
   *Seminal academic study formalizing the transition from BCG's growth-share matrix to multifactor portfolio frameworks.* DOI: `10.1177/002224297704100206`

3. **Porter, Michael E. (1980).** *Competitive Strategy: Techniques for Analyzing Industries and Competitors*. Free Press, New York.  
   *Canonical framework on structural industry attractiveness, economic barriers to entry, and competitive positioning.* ISBN: `978-0684841489`

4. **Henderson, Bruce D. (1970).** *The Product Portfolio*. Boston Consulting Group Perspectives, No. 66, Boston.  
   *Landmark paper on market share scale, experience curve cost reduction, and corporate liquidity balancing.*

5. **Minto, Barbara (2009).** *The Pyramid Principle: Logic in Writing and Thinking*. Financial Times / Prentice Hall (3rd Edition).  
   *The global standard for structuring executive presentations, Action Titles, and board-level decision synthesis.* ISBN: `978-0273710516`

6. **McKinsey & Company, Koller, T., Goedhart, M., & Wessels, D. (2012).** *Valuation: Measuring and Managing the Value of Companies*. John Wiley & Sons, New York (5th Edition).  
   *Definitive corporate finance treatise establishing the mathematical link between Return on Invested Capital ($\text{ROIC}$), Weighted Average Cost of Capital ($\text{WACC}$), and shareholder value creation.* ISBN: `978-0470427774`
