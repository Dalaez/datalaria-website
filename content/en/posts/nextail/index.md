---
title: "Nextail: How a Spanish Startup's Prescriptive AI Is Defeating Excel in Fashion Retail"
date: 2026-03-31
draft: false
categories: ["case-studies", "AI"]
tags: ["nextail", "ai", "retail", "supply chain", "S&OP", "machine learning", "optimization", "fashion", "startup"]
description: "The story of Nextail, the Madrid-based startup founded by a former Zara logistics director that is replacing fashion retail spreadsheets with a mathematical brain capable of making billions of inventory decisions per season."
summary: "The future of retail doesn't fit in Excel. A former Zara executive founded Nextail to prove it, building a prescriptive AI engine that processes billions of inventory combinations and frees up to 75% of merchandising teams' time. This is the story of how mathematical optimization is conquering fast fashion."
social_text: "The future of retail doesn't fit in Excel. A former Zara exec founded Nextail to prove it with prescriptive AI processing billions of inventory decisions. The story of how math is conquering fast fashion 🧠👗📊 #RetailTech #AI #SupplyChain"
image: cover.png
weight: 10
authorAvatar: datalaria-logo.png
---

In the cutthroat world of fast fashion, where trends are born and die in weeks and the wrong size in the wrong store can mean the difference between selling at full price or slashing margins in clearance sales, there's an uncomfortable truth the industry has taken decades to accept: **the most critical business decisions—what to ship, where, and when—are still being made with spreadsheets, gut feeling, and mental maps**.

This is the story of **[Nextail](https://nextail.co/)**, a Madrid-based startup founded in 2014 by a team that knew that reality from the inside and decided to destroy it with mathematics. It is a case study of how prescriptive analytics and stochastic optimization are replacing Excel in an industry worth billions.

![Nextail image](nextail.png)

### The Origin: When Zara Wasn't Enough

Nextail's genesis is directly linked to the epicenter of global fast fashion. **Joaquín Villalba**, an industrial engineer from the Universitat Politècnica de València with an MBA from INSEAD, served as European Logistics Director at **Zara-Inditex**, where he oversaw operations for over a thousand stores with annual sales exceeding $10 billion. From that privileged vantage point, [Villalba analyzed the foundations of Amancio Ortega's empire](https://medium.com/authority-magazine/the-future-of-retail-over-the-next-five-years-with-joaquin-villalba-ceo-of-nextail-713703af4310) and reached a conclusion that would define his career: Zara's logistics model was revolutionary in its structure, but daily decisions about what to send to each store still depended on human intuition.

Customers left frustrated without finding their size. The cause wasn't a lack of global stock, but a distribution model too static to react to micro-local demand fluctuations. Villalba saw an immense opportunity to take retail agility to the next level by injecting data science and operations research directly into the core of merchandising.

To bring this vision to life, he partnered with **Carlos Miragall**, a corporate finance expert with experience scaling startups from scratch to over 150 employees and raising more than $60 million in funding, and **Javier Lafuente García** as CTO. [Together they founded Nextail](https://nextail.co/company) with a clear mission: **democratize the operational excellence of fast fashion through mathematical precision**.

### The Problem: The Combinatorial Explosion That Breaks Excel

To understand why Nextail exists, you need to grasp a mathematical phenomenon that merchandising teams endure daily: the **combinatorial explosion**. A fashion retailer doesn't make aggregated decisions. It crosses thousands of products (SKUs), multiplied by several sizes, distributed across hundreds of stores, requiring updates several times a week. The result: **millions of decision points every day**.

Spreadsheets collapse. Literally. [As Mark Scouller notes](https://nextail.co/resource/implementing-ai-driven-merchandising-tech-mark-scoullers-experience), a merchandising veteran at firms like Next, New Look, and Mountain Warehouse, teams deal with files that freeze beyond half a million rows, held together by thousands of interdependent macros that break with any change.

But the technical collapse is just the surface. The business consequences are devastating:

* **Forced Store Clustering**: Unable to calculate demand per individual store, teams [group locations into broad categories](https://nextail.co/resource/assortment-planning-evolution-fashion-retail-spreadsheets-ai) and apply uniform distributions. The result: overstock in some stores and stockouts in others within the same cluster.

* **"Mental Map" Dependency**: Decisions end up relying on the buyer's subjective intuition, an approach blind to week-over-week trend shifts.

* **The Abandoned "Middle Class"**: Teams spend all their time replenishing sold-out best-sellers or liquidating worst-sellers, completely neglecting mid-sellers and mid-tier stores. As Scouller puts it: these ignored products are the ones that **"silently drain profit margins."**

* **Destructive Markdowns**: Procedural slowness forces massive end-of-season clearance campaigns to liquidate accumulated inventory.

> **"The future of retail doesn't fit in Excel"** — Mark Scouller

### The Solution: A Mathematical Brain That Thinks in Probabilities

Nextail's architecture attacks the problem across three perfectly orchestrated layers within the S&OP (Sales and Operations Planning) process:

#### 1. "AI-Ready" Data (Data Ingestion & Optimization)

The foundational premise is data purity. Retailer datasets come from a myriad of disconnected systems (ERPs, WMS, POS). [The platform consolidates and cleanses all this information](https://help.nextail.co/en) daily, correcting phenomena like "phantom stock" (where the system reports inventory for garments that have been stolen or misplaced), imputing null values, and generating a **single source of truth** that eliminates friction between departments.

#### 2. Hyper-Local Probabilistic Forecasting

Unlike traditional forecasting that produces a single prediction number, [Nextail's algorithms build a complete probability distribution](https://nextail.co/solution/analytics) for each combination of SKU, store, and day. They don't just anticipate expected volume; they quantify uncertainty. That forecast is then calibrated against real constraints: backroom capacity, packing logistics, size distribution by ZIP code demographics, and minimum display requirements.

#### 3. Prescriptive Optimization (The MILP Engine)

This is where the real innovation lives. Once the probabilistic model dictates *how much* demand will occur, *where*, and *when*, the system must prescribe the exact optimal operational action. To do this, it deploys **Mixed-Integer Linear Programming (MILP)** algorithms combined with stochastic optimization.

Conceptually, the engine solves an objective function that maximizes the probability of full-price sell-through for each SKU at each store, weighted by gross margin, minus the logistics costs of each transfer. All subject to hard constraints: inventory conservation, available physical space, brand aesthetic standards, and size curve coherence.

The system evaluates billions of permutations and decides: is it more profitable to hold stock at the distribution center to protect e-commerce, or rush it to a store showing high imminent probability of a stockout?

{{< youtube xD5D943-888 >}}


The output isn't a static report, but an **actionable execution directive** delivered to ERP and WMS systems within minutes. This automation frees [up to 75% of merchandising teams' time](https://nextail.co/company/customer-impact) to refocus on strategic decisions.

### Beyond Allocation: Intelligent Rebalancing

One of Nextail's most disruptive features is **[inventory rebalancing between stores](https://nextail.co/resource/5-benefits-ai-driven-inventory-rebalancing)** (Store Transfers). As products approach end-of-life, demand fragments: some stores have excess sizes nobody wants, while others need exactly those sizes.

Traditionally, that leftover stock went straight to markdowns. Nextail does the opposite: the optimizer scans store pairs, calculates whether the increase in full-price sale probability justifies the logistics cost of the transfer, and actively regroups broken size curves into active demand centers. This way, **markdowns stop being an endemic evil** and become a tool of absolute last resort.

### The Impact: ROI in 30 Days

Prescriptive analytics wouldn't matter without results. Nextail's numbers speak for themselves:

| Metric | Impact |
| :--- | :--- |
| **Inventory coverage** | Reduction of up to **30%** |
| **Stockouts** | Decrease of up to **60%** |
| **Direct sales** | Increase of **5-10%** |
| **Merchandiser time freed** | Up to **75%** |
| **Demonstrable ROI** | Within the first **30 days** |

International brands such as **Pepe Jeans**, **River Island**, **Guess**, **[Scotta](https://retailtechinnovationhub.com/home/2025/7/10/scotta-taps-nextail-ai-powered-technology-to-support-retailers-growth-across-stores-and-online)**, **Bimani**, **Silbon**, and **Sports Emotion** have integrated the platform to overcome the bottlenecks of their omnichannel scaling. The Pepe Jeans case is particularly illustrative: a brand with lead times of up to six months that shifted from static forecasts to dynamic optimization capable of adapting to consumer behavior in weeks.

### Financial Trajectory and Leadership Transition

The corporate timeline reveals a growth pattern backed by the European venture capital elite:

| Round | Date | Amount (USD) | Lead Investor(s) |
| :--- | :--- | :--- | :--- |
| **Seed** | 2016 | [$1.6M](https://www.nautacapital.com/news-insights/nextail-raises-1-6m-investment-led-by-nauta-capital) | Nauta Capital |
| **Series A** | Jun 2018 | [$10M](https://www.eu-startups.com/2018/06/madrid-based-nextail-raises-10-million-bring-artificial-intelligence-into-retailers-inventory-planning/) | Nauta Capital |
| **2024 Investment** | Nov 2024 | [Multi-million](https://retailtechinnovationhub.com/home/2024/11/7/ai-powered-retail-technology-firm-nextail-announces-new-ceo-and-multi-million-euro-investment-from-current-investors) | Existing investors |

After a decade leading the product vision and positioning the platform to automate over **one billion inventory decisions per season** across a park of **20,000 stores**, [Joaquín Villalba orchestrated an executive succession in 2024](https://retailtimes.co.uk/nextail-marks-a-decade-of-retail-transformation-with-new-ceo/). He adopted the role of Corporate Ambassador—in line with his recognition as a **World Economic Forum Tech Pioneer**—and handed the CEO position to **Carlos Miragall**, co-founder and former CFO, to captain the company into the era of LLMs and agentic systems.

Institutional recognition has been emphatic: **[Best Fashion Retail Merchandising Platform 2025](https://nextail.co/press-release/best-fashion-retail-merchandising-platform-2025)** (EU Business News), **triple victory at the Just Style Excellence Awards 2025**, and repeated recognition as a **[Representative Vendor by Gartner](https://nextail.co/press-release/retail-forecasting-allocation-replenishment-gartner-representative-vendor)** in their retail optimization market guides.

### The Sociological Mountain: The Biggest Obstacle Isn't Technology

Despite technical superiority, the biggest hurdle to adoption isn't computational—**it's human**. [As Mark Lewis warns](https://nextail.co/resource/dispellling-ai-magic-fashion-retail-mark-lewis), a retail technology strategist: *"The biggest barrier to AI success in fashion is purely and exclusively a matter of collective mindset."*

There's a dangerous fallacy that perceives AI as incomprehensible "dark magic." This generates unrealistic expectations in boardrooms or visceral rejection from merchandising professionals who fear the "black box" verdict. Retailers invest millions in platforms that end up underutilized because they haven't restructured their teams or invested in training.

The key, according to Scouller, is understanding that AI *"isn't dark magic, but crushing logic: massive processing of clean data and the iterative application of mathematics at an inhuman scale and speed."* And the corporate tipping point arrives at a very specific moment: **when the pain of inefficiency exceeds the inertia of operational comfort**.

### The Future: Generative AI, Autonomous Agents, and the ESPR Regulatory Shield

Nextail's roadmap converges on three forces that will define retail in 2026:

**1. Conversational Interface with RAG**: Generative AI won't replace the MILP optimization engines (LLMs fail at massive numerical computation at efficient cost). Its role will be to act as a **cognitive orchestration layer**: a commercial director will be able to interact with the mathematical brain in natural language, requesting profitability analyses for a specific rebalancing and authorizing automatic executions.

**2. Multi-Agent AI Systems**: [Gartner projects that by end of 2026](https://www.deloitte.com/us/en/services/consulting/blogs/business-operations-room/llm-for-supply-chain-optimization.html), more than 40% of enterprise applications will incorporate AI agents. In the S&OP context, a "swarm" of agents will autonomously monitor volatile variables—weather, supply chain disruptions, trending virality on social media—and recalibrate the optimizer without human intervention.

**3. The ESPR Shield**: The [European ESPR 2026 regulatory framework](https://nextail.co/resource/q2-2025-nextail-ai-fashion-retail-growth) will penalize (and even ban) the destruction of unsold textile inventory. Surpluses will no longer be "sunk costs" but **auditable environmental liabilities**. In this context, Nextail's ability to reduce overproduction and minimize leftovers transforms from a financial advantage into a legal survival requirement.

### Conclusion: Mathematics Wins the Game

Nextail's story is the chronicle of an industry that has crossed a point of no return. The complexity of modern omnichannel retail has definitively exceeded human capacity for manual management. Spreadsheets are not a minor inconvenience; they are a **systemic risk** that silently drains profit margins.

Nextail has proven that the answer lies in the fusion of probabilistic forecasting, stochastic optimization, and a clean data culture. Its journey demonstrates that sometimes, revolution doesn't arrive with an entirely new idea, but with the rigorous application of mathematics to a problem everyone had given up on.

As Villalba discovered in the corridors of Zara: the agility of the future isn't built on intuition—it's built on equations.

---

#### Sources of Interest:
* [**Nextail**: The Merchandise Execution Platform for Fashion](https://nextail.co/)
* [**Silicon Republic**: Nextail is bringing science to retail decision-making](https://www.siliconrepublic.com/start-ups/nextail-retail-ai-analytics-platform-spain)
* [**Authority Magazine (Medium)**: The Future of Retail, with Joaquín Villalba, CEO of Nextail](https://medium.com/authority-magazine/the-future-of-retail-over-the-next-five-years-with-joaquin-villalba-ceo-of-nextail-713703af4310)
* [**Nextail**: Implementing AI-Driven Merchandising - Mark Scouller's Experience](https://nextail.co/resource/implementing-ai-driven-merchandising-tech-mark-scoullers-experience)
* [**Nextail**: From Spreadsheets to AI in Assortment Planning](https://nextail.co/resource/assortment-planning-evolution-fashion-retail-spreadsheets-ai)
* [**EU-Startups**: Nextail raises $10M to bring AI into retailers' inventory planning](https://www.eu-startups.com/2018/06/madrid-based-nextail-raises-10-million-bring-artificial-intelligence-into-retailers-inventory-planning/)
* [**Retail Tech Innovation Hub**: Nextail announces new CEO and multi-million euro investment](https://retailtechinnovationhub.com/home/2024/11/7/ai-powered-retail-technology-firm-nextail-announces-new-ceo-and-multi-million-euro-investment-from-current-investors)
* [**Retail Times**: Nextail marks a decade of retail transformation with new CEO](https://retailtimes.co.uk/nextail-marks-a-decade-of-retail-transformation-with-new-ceo/)
* [**McKinsey**: Autonomous supply chain planning for consumer goods companies](https://www.mckinsey.com/capabilities/operations/our-insights/autonomous-supply-chain-planning-for-consumer-goods-companies)
* [**Nextail**: Recognized as Representative Vendor by Gartner](https://nextail.co/press-release/retail-forecasting-allocation-replenishment-gartner-representative-vendor)
* [**Nextail**: AI Drives Fashion Retail Growth – Q2 2025](https://nextail.co/resource/q2-2025-nextail-ai-fashion-retail-growth)
* [**Deloitte**: AI - The Helping Hand in Sales and Operations Planning](https://www.deloitte.com/us/en/services/consulting/blogs/business-operations-room/llm-for-supply-chain-optimization.html)
* [**Mark Lewis on Nextail**: Dispelling the magic - 5 retail realities about AI in fashion](https://nextail.co/resource/dispellling-ai-magic-fashion-retail-mark-lewis)
* [**Retail Tech Innovation Hub**: Scotta taps Nextail AI technology](https://retailtechinnovationhub.com/home/2025/7/10/scotta-taps-nextail-ai-powered-technology-to-support-retailers-growth-across-stores-and-online)
