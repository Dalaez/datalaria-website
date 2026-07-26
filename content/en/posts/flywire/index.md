---
title: "Flywire: How a Spaniard Built the Brain of International Payments from Boston"
date: 2026-07-25
draft: false
categories: ["case-studies"]
tags: ["flywire", "fintech", "international payments", "nasdaq", "spanish startup", "machine learning", "cross-border", "iker marcaide"]
description: "The story of Flywire (FLYW), the Spanish unicorn listed on the Nasdaq that processes billions in international payments for education, healthcare, and travel. How Iker Marcaide turned a student's pain point at MIT into a global platform using ML to optimize every transaction."
summary: "When a Korean student tries to pay tuition at a university in Madrid, they face a maze of opaque banking fees, unfavorable exchange rates, and transfers that take 5 days. A Spanish engineer at MIT decided that was unacceptable. Today, his company Flywire trades on the Nasdaq, generates over $600 million in revenue, and processes payments in 140+ currencies using machine learning to optimize every transaction."
social_text: "A Spanish student at MIT gets fed up with international tuition payments. Founds peerTransfer in 2009. Today it's called Flywire, trades on the Nasdaq ($FLYW), generates $600M+ revenue and processes payments in 140 currencies with ML 🇪🇸💸🌍 #Flywire #Fintech #SpanishStartup"
image: cover.png
weight: 10
authorAvatar: datalaria-logo.png
---

When a Korean student tries to pay tuition at a university in Madrid, they face a Kafkaesque maze: opaque banking fees that devour 3% to 5% of the transaction, unfavorable exchange rates unilaterally imposed by the intermediary bank, SWIFT transfers that take 3 to 5 business days to settle, and a payment reference system where a single wrong digit means the university cannot reconcile the deposit with the student's enrollment. The result: the student overpays, the university receives less, and both waste time in emails and phone calls trying to square the accounts.

**Iker Marcaide**, a Spanish engineer pursuing his MBA at **MIT Sloan School of Management** in Boston, experienced this pain firsthand. But unlike the 99% of people who complain about the international banking system and move on, Marcaide did what founders do: **he asked why it had to be this way and built the alternative**.

In 2009, he founded **peerTransfer** — a platform that allowed international students to pay tuition in their local currency, with transparent exchange rates, minimal fees, and guaranteed settlement in the university's account. In 2016, the company rebranded as **Flywire** to reflect its expansion beyond education. In May 2021, it went public on the **Nasdaq** under the ticker **$FLYW**. In fiscal year 2025, it generated over **$603 million in revenue**, with 27% year-over-year growth. In Q1 2026, revenue reached **$188 million**, a 41% increase over the same quarter the prior year.

Alongside [Carto](/en/posts/carto/), [Devo](/en/posts/devo/), [Clarity AI](/en/posts/clarity_ai/), [Nextail](/en/posts/nextail/), and [Freepik](/en/posts/freepik/), it is one of the Spanish startups that have achieved global scale. But Flywire has a distinguishing trait: **it trades on an American stock exchange**. Not on a private round, not on a European secondary market — on the Nasdaq, alongside Apple, Google, and Tesla.

{{< youtube 0eGSRmq1dPc >}}


### The Technology: The Intelligent Brain of Payments

Flywire is not a conventional payment processor like Stripe or PayPal. The fundamental difference is that Flywire has built a platform designed specifically for **complex, high-value, cross-border payments**, where friction isn't at the user's final click (Stripe already solved that) but in the entire chain behind it: routing between banks, currency conversion, reconciliation with the receiver's system, and regulatory compliance across multiple jurisdictions.

The platform operates across three technological layers that reinforce each other:

**1. Proprietary Global Payment Network**: Flywire has built a network of direct banking connections across more than **240 countries and territories**, supporting payments in over **140 currencies**. This proprietary network allows them to select the optimal route for each transaction — not the default SWIFT route, which may pass through 3-4 intermediary banks, each charging its fee, but the most direct, fastest, and most cost-effective route for that specific currency corridor.

**2. Machine Learning for Transaction Optimization**: This is where data engineering creates the competitive moat. Flywire uses ML algorithms for three critical functions:

* **Intelligent routing**: For each transaction, the system evaluates multiple banking routes and selects the optimal combination of exchange rate, settlement speed, and total cost. It's not a static routing table; it's a model that continuously learns from historical transactions to optimize each currency corridor.
* **Automatic reconciliation with deep learning**: The nightmare for university and hospital treasury offices is reconciling received payments with outstanding invoices. When a student pays from South Korea, the payer's name may appear transliterated three different ways, the payment reference may be truncated, and the received amount differs from the invoiced amount due to intermediary fees. Flywire uses **deep neural networks and reinforcement learning** to automatically match payments to invoices, even when data doesn't match exactly.
* **Fraud detection**: ML models that analyze transaction patterns to identify anomalies and prevent fraud before the transaction completes.

**3. Vertical-Specific Software**: For each industry, Flywire doesn't just process payments but integrates directly into the client's core systems — **Student Information Systems (SIS)** in education, **Electronic Health Records (EHR)** in healthcare, **ERPs** in B2B. This deep integration turns Flywire into infrastructure, not an interchangeable vendor.

### Vertical Expansion: The "Land and Expand" Pattern

Flywire's growth story follows a pattern we've seen repeat in every Spanish unicorn analyzed on this blog: **find a specific pain in one vertical, solve it with obsessive engineering, and expand horizontally**.

![Flywire's vertical expansion: from education to healthcare and travel](vertical_expansion.png)

**Education (2009-2016)**: The starting point. peerTransfer solved the international tuition payment pain, beginning with universities in the United States and expanding to Europe, Australia, and Asia. The value proposition was clear: the student pays in their local currency with full transparency, the university receives exactly the invoiced amount with no hidden fees, and reconciliation is automatic. Today, Flywire processes payments for more than **3,800 educational institutions** worldwide.

**Healthcare (2016-2019)**: The leap to healthcare was natural. American hospitals face the same complex payment problem: international patients, fragmented insurance, installment plans, and administrative reconciliation that consumes enormous resources. Flywire adapted its platform to integrate with hospital management systems and offer flexible payment options (financing plans, partial payments) that improve the hospital's collection rate and the patient experience.

**Travel (2019-present)**: The third vertical. Tour operators, travel agencies, and luxury hotels handle high-value bookings from international clients who want to pay in their local currency. Margins are tight, and losing 3-5% in exchange rate fees can destroy a booking's profitability. Flywire offers the same transparency and intelligent routing, adapted to the travel industry's specific workflow.

**B2B (2021-present)**: The fourth frontier. International business-to-business payments — invoices, supplier settlements, royalty payments. The pattern repeats: regulatory complexity, multiple currencies, inefficient manual reconciliation. Flywire automates the complete *invoice-to-cash* flow.

### The Numbers: A Spanish Unicorn on the Nasdaq

| Metric | Data |
| :--- | :--- |
| **Founded** | 2009 (as peerTransfer) |
| **Rebranded to Flywire** | 2016 |
| **Nasdaq IPO** | May 2021 (ticker: $FLYW) |
| **FY2025 Revenue** | ~$603 million (+27% YoY) |
| **Q1 2026 Revenue** | $188 million (+41% YoY) |
| **Currencies supported** | 140+ |
| **Countries** | 240+ |
| **Education clients** | 3,800+ institutions |
| **Headquarters** | Boston, MA (USA) |
| **Founder** | Iker Marcaide (Spain) |

To put these numbers in context within the Spanish unicorn ecosystem: Flywire generates more revenue than [Devo](/en/posts/devo/) (acquired by LogRhythm in 2023 after reaching unicorn valuation) and more than [Nextail](/en/posts/nextail/) (which operates in a narrower retail niche). The most direct comparison is with [Clarity AI](/en/posts/clarity_ai/) — both are fintech, both operate from the European regulatory ecosystem but with a global market, and both face the requirements of the [EU AI Act](/en/posts/eu_ai_act/) for operating in sensitive categories (essential financial services, Annex III of the regulation).

### Lessons for Engineers

Flywire's story distills three lessons applicable to any engineer building technology products:

**Lesson 1: The "Platform Effect" — Start with a pain, expand through infrastructure**

Flywire didn't start by saying "let's build a global payments platform." It started by saying "let's solve international tuition payments for American universities." A specific pain, a specific customer, a specific market. Once the platform was built and proven in education, the expansion to healthcare and travel was a natural extension of the same technological engine applied to a different workflow.

It's the same pattern we saw in [Carto](/en/posts/carto/) (started as a geospatial visualization tool, expanded to enterprise Location Intelligence), in [Devo](/en/posts/devo/) (started as a next-gen SIEM, expanded to full observability for defense and cybersecurity), and in [Nextail](/en/posts/nextail/) (started optimizing store inventory, expanded to prescriptive AI for the entire retail supply chain).

**Lesson 2: Build vs. Buy — Why Flywire built its own payments engine**

The obvious question is: why not use Stripe? Stripe is extraordinary for standard online payments (e-commerce, SaaS). But high-value cross-border payments have three requirements that Stripe didn't solve in 2009 (and still doesn't fully solve for this niche): intelligent routing by currency corridor, automatic reconciliation with vertical systems (SIS, EHR), and multi-jurisdiction regulatory compliance for payments crossing borders. Flywire needed to control the entire chain to optimize every link. The build vs. buy decision boils down to one question: is payment **the** product, or is it an auxiliary feature of your product? If payment is the product (as with Flywire), you build. If it's auxiliary (as with an e-commerce shop), you buy.

**Lesson 3: Regulation as competitive advantage, not as a brake**

Flywire operates in one of the most regulated sectors on the planet: cross-border financial payments. It complies with anti-money laundering (AML) regulations, know-your-customer (KYC) requirements, PCI DSS for card data security, and the financial regulations of every country where it operates. As we discussed in the [EU AI Act article](/en/posts/eu_ai_act/), AI systems that determine access to essential financial services fall under the European regulation's "high-risk" category.

But Flywire has turned this regulatory complexity into a **barrier to entry for competitors**. Any startup wanting to compete with Flywire in cross-border university payments needs not only to build a comparable technology platform but also to obtain regulatory licenses in dozens of jurisdictions — a process that can take years and cost millions. The regulation that suffocates potential competitors protects well-positioned incumbents.

### The Spanish Pattern: Local Pain, Global Scale

If you look at the complete series of Spanish startups analyzed on this blog, the pattern repeats with almost algorithmic consistency:

| Startup | Initial pain | Expansion | Outcome |
| :--- | :--- | :--- | :--- |
| **Flywire** | International tuition payments | Education → Healthcare → Travel → B2B | Nasdaq ($FLYW), $603M revenue |
| [**Devo**](/en/posts/devo/) | Security logging | SIEM → Observability → Defense | Unicorn, LogRhythm acquisition |
| [**Carto**](/en/posts/carto/) | Web maps | Visualization → Location Intelligence | Enterprise cloud platform |
| [**Nextail**](/en/posts/nextail/) | Store inventory | Retail → Prescriptive AI → Supply chain | ESPR 2026, global expansion |
| [**Clarity AI**](/en/posts/clarity_ai/) | ESG scoring | Sustainability → Fintech → Regulation | Impact platform, BlackRock |
| [**Freepik**](/en/posts/freepik/) | Stock images | Stock → Generative AI → Design | Profitable from day 1 |

The common denominator is always the same: a Spanish founder with international training, a concrete and verifiable pain, a technically obsessive solution, and horizontal expansion once the base platform demonstrates traction. Neither the lack of VC ecosystem in Spain, nor the distance to Silicon Valley, nor the language barrier has prevented these companies from reaching global scale. What propelled them is exactly what [Deming](/en/posts/deming/) preached decades ago: **obsessive quality in execution and continuous improvement based on evidence**.

Iker Marcaide didn't invent international payments. But he did what great engineers do: he looked at a broken process, understood every link in the chain, and built a solution that was 10 times better than the *status quo*. Today, that solution processes billions of dollars and trades on the Nasdaq. And it started with a Spanish student at MIT who refused to pay abusive fees on his tuition.

---

#### Sources of Interest:
* [**Flywire**: Official Site — Global Payments Platform](https://www.flywire.com/)
* [**Nasdaq**: Flywire Corporation ($FLYW) — Listing Profile](https://www.nasdaq.com/market-activity/stocks/flyw)
* [**Flywire Investor Relations**: Q1 2026 Financial Results](https://ir.flywire.com/)
* [**Xataka**: Iker Marcaide and the Flywire Story](https://www.xataka.com/)
* [**YouTube**: Flywire — Simplifying Complex Payments](https://www.youtube.com/watch?v=0eGSRmq1dPc)
* [**Datalaria**: Devo — The Spanish SIEM That Scaled to the Pentagon](/en/posts/devo/)
* [**Datalaria**: Clarity AI — The Fintech That Scores the Planet](/en/posts/clarity_ai/)
* [**Datalaria**: Carto — From Web Maps to Enterprise Location Intelligence](/en/posts/carto/)
* [**Datalaria**: EU AI Act — Regulation and Fintech as a High-Risk Category](/en/posts/eu_ai_act/)
