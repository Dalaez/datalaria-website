---
title: "EU AI Act: What Every Engineer Needs to Know (No Lawyers Required)"
date: 2026-07-05
draft: false
categories: ["Artificial Intelligence", "Engineering", "Regulation"]
tags: ["eu ai act", "ai regulation", "compliance", "high risk", "startups", "engineering", "europe"]
description: "A technical guide to the European AI Regulation (EU AI Act) written by and for engineers. Risk classification, technical obligations, fines, compliance checklist and connection with Spanish AI Law and AESIA."
summary: "On August 2, 2026, most obligations of the EU AI Act come into force. Maximum fine: 35 million euros or 7% of your global turnover. And most articles explaining this regulation are written by lawyers, for lawyers. Not this one. This one is written by an engineer who already operates AI agents in production, translating every article of the regulation into the language we actually understand: architectures, pipelines, and code."
social_text: "On August 2, 2026, the EU AI Act comes into force. Maximum fine: €35M. Most guides are written by lawyers. Not this one. Written by an engineer who runs AI agents in production 🇪🇺🤖⚖️ #EUAIAct #AI #Regulation #Engineering"
image: cover.png
weight: 10
authorAvatar: datalaria-logo.png
---

Picture this scenario: your European startup launches an AI tool that scans résumés to filter candidates in hiring processes. The product works, clients are happy, revenue is growing. Three months later, you receive a formal notification from the national AI supervisory authority. Your system has been classified as **"high-risk"** under Regulation (EU) 2024/1689, better known as the **EU AI Act**. You have no mandatory technical documentation, you haven't implemented human oversight, and your training data doesn't meet the governance requirements. Potential fine: up to **35 million euros** or **7% of your worldwide annual turnover**.

Impossible? Not at all. This is exactly what European regulation has stipulated since February 2025 for prohibited practices, and what from **August 2, 2026** extends to the majority of obligations for high-risk systems ([Art. 113, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)).

If you already operate AI agents in production — as we've done on this blog with the [Autopilot Project](/en/posts/ai_agents_part1/) or the [agentic obsolescence radar](/en/posts/obs_part5_radar_agent/) — you need to know exactly where the line is. And most guides on the EU AI Act are written by lawyers, for lawyers. Not this one. This one is written by an engineer who translates every article of the regulation into the language we actually understand: architectures, pipelines, and code.

### The Risk Pyramid: Classify Your AI in 60 Seconds

The EU AI Act doesn't ban artificial intelligence. What it does is classify every AI system into **four risk levels** and assign proportional obligations to each level. It's a pragmatic approach inspired by existing regulatory frameworks like REACH for the chemical industry or the Machinery Directive for manufacturing: the higher the potential risk, the stricter the control requirements.

![EU AI Act risk classification pyramid](risk_pyramid.png)

#### 🔴 Unacceptable Risk — PROHIBITED (Article 5)

These practices have been **completely banned in the EU since February 2, 2025** ([Art. 5, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689#d1e2816-1-1)). There are no commercial exceptions or sandboxes that permit them. They are the absolute red lines of the regulation:

* **Subliminal or deceptive manipulation**: AI systems designed to distort a person's behavior using techniques that operate below their threshold of consciousness, causing significant harm.
* **Exploitation of vulnerabilities**: AI that exploits the age, disability, or socioeconomic situation of vulnerable persons to alter their behavior in a harmful way.
* **Social scoring**: Systems used by public authorities to evaluate or classify people based on their social behavior or personal traits, resulting in unjustified detrimental treatment.
* **Predictive policing**: AI that predicts a person's criminal behavior based solely on their profiling or personality traits (with limited exceptions for ongoing investigations).
* **Untargeted facial scraping**: The creation or expansion of facial recognition databases through untargeted collection of facial images from the internet or CCTV footage.
* **Emotion recognition at work and school**: Inferring the emotions of employees in the workplace or students in educational institutions (with very limited medical or safety exceptions).
* **Sensitive biometric categorization**: Systems that infer data such as political or religious beliefs, sexual orientation, or race from biometric data.

If any AI system in your organization touches any of these categories, the correct position is not to "find a legal loophole" but to remove it from the product. The fine for these practices reaches **35 million euros** or **7% of global annual turnover**, whichever is higher ([Art. 99.3, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689#d1e9487-1-1)).

#### 🟠 High Risk — STRICT REGULATION (Articles 6-49 and Annex III)

This is where most enterprise AI systems land, and where the regulation demands the greatest technical effort. A system is classified as "high-risk" if it is a safety component of a product regulated by EU harmonized legislation (medical devices, toys, aviation), or if it operates in any of the sensitive areas defined in **Annex III** of the regulation:

* **Critical infrastructure**: Systems for the management of essential services (transport, water, gas, electricity, telecommunications).
* **Education and training**: AI that determines access to educational institutions or assesses student performance.
* **Employment and HR**: AI tools for recruitment, CV screening, task assignment, or worker management. This is directly relevant to what we analyzed in the [Onboarding with AI article](/en/posts/onboarding/): using IDP and GenAI to automate employee onboarding falls into the high-risk category if the system makes or influences decisions about people.
* **Essential services**: Systems that determine access to credit, essential public services, or life and health insurance. Startups like [Clarity AI](/en/posts/clarity_ai/), which calculates sustainability scores for investment decisions, operate directly in this zone.
* **Law enforcement, justice, and migration**: AI in border control, asylum processing, security risk assessment, or the administration of justice.
* **Biometrics**: Certain remote biometric identification systems.

The fine for non-compliance with high-risk system obligations is up to **15 million euros** or **3% of worldwide annual turnover** ([Art. 99.4, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689#d1e9487-1-1)).

> **Important note**: The legislative proposal known as the *"Digital Omnibus"* (2025) may postpone certain Annex III (high-risk) obligations from August 2026 to **December 2027**. However, the underlying technical requirements remain unchanged — only the enforcement timeline shifts. Don't wait.

#### 🟡 Limited Risk — TRANSPARENCY (Articles 50-52)

Limited-risk systems have a single fundamental obligation: **inform the user that they are interacting with an AI**. This applies to chatbots, content generation systems (deepfakes), and conversational assistants. Our [Ops Engineering Copilot](/en/posts/ai_agents_part8/) (the chatbot based on Algolia Agent Studio and RAG that answers questions about the blog) falls into this category: the user must know they're talking to a machine, not a person.

#### 🟢 Minimal Risk — FREE (no additional obligations)

The majority of commercial AI systems fall here: spam filters, recommendation engines, generative AI for marketing content. The [Autopilot Project](/en/posts/ai_agents_part1/) that automatically generates social media posts has no specific obligations under the EU AI Act beyond general good practices. The same applies to tools like the [unit converter](/en/posts/app_unit_converter/) or the [flashcards app](/en/posts/app_flashcards/).

### The 5 Technical Commandments of High Risk

If your system falls into the 🟠 category, you need to implement five blocks of technical requirements. What's notable is that, if you already follow the engineering practices we've documented on this blog, you're closer to compliance than you think:

**1. Risk Management — Article 9**

The regulation requires establishing, implementing, and maintaining a **risk management system that operates throughout the entire lifecycle of the AI system** ([Art. 9, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689#d1e3383-1-1)). This includes identifying known and foreseeable risks to health, safety, and fundamental rights, estimating those risks, and adopting mitigation measures.

*Translation for engineers*: It's a CI/CD pipeline applied to risk. Document, monitor, iterate. It's not a static document you write once and file away; it's a living process. Exactly the philosophy that [W. Edwards Deming](/en/posts/deming/) systematized with the PDCA cycle (Plan-Do-Check-Act). If you already implement PDCA in your quality processes, the AI Act's risk management will feel familiar.

**2. Data Governance — Article 10**

Training, validation, and testing datasets must meet high-quality criteria: be **representative, relevant, free of errors to the extent possible, and with appropriate governance practices** to prevent bias ([Art. 10, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689#d1e3549-1-1)).

*Translation*: The [data hygiene](/en/posts/sop_engineering-data-hygiene/) we preached in the S&OP series is no longer an optional best practice — **it's the law**. The cleanup pipeline with Z-Score for outlier detection, anomaly flagging (not deletion), and persistence in Supabase with Row Level Security that we built in that series directly fulfills the spirit of this article. What the regulation adds is the requirement that all of this be documented and auditable.

**3. Technical Documentation — Article 11 and Annex IV**

Before marketing or putting a high-risk system into service, you must prepare a **technical file** demonstrating compliance with the regulation ([Art. 11, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689#d1e3667-1-1)). Annex IV details the minimum content: general system description, detailed architecture and components, training data information, performance metrics (accuracy, robustness, cybersecurity), and the development process.

*Translation*: Your README and your Confluence page aren't enough. The regulation requires a living document covering the system architecture (like the Mermaid diagrams we use in the [Obsolescence series](/en/posts/obs_part3_architecture/)), model performance metrics, robustness tests, and cybersecurity measures. Think of it as an Architecture Decision Record on regulatory steroids.

**4. Record-Keeping and Logging — Article 12**

High-risk systems must be designed to **automatically generate logs** during operation, ensuring full traceability of every decision and the ability to reconstruct events if a compliance issue arises ([Art. 12, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689#d1e3702-1-1)).

*Translation*: If you already use Supabase + FastAPI with the architecture from the [agentic radar](/en/posts/obs_part6_fastapi_server/), this should sound familiar. Every ingestion event, every CrewAI agent decision, every LLM response gets logged in the database. What the regulation formalizes is what any competent backend engineer should already be doing: structured logging, not as an afterthought, but as a design requirement from day zero.

**5. Human Oversight — Article 14**

The system must be designed with **"human-in-the-loop"** or **"human-on-the-loop"** mechanisms, ensuring that a qualified human operator can oversee, interpret, and if necessary, override the AI's decisions ([Art. 14, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689#d1e3789-1-1)).

*Translation*: This is the principle we implemented in [Autopilot Part 5](/en/posts/ai_agents_part5/) with **GitHub Environments for manual approval**. The pipeline generates content automatically with AI agents, but no post gets published without explicit human review and approval. It's not a new concept for us; now it has the force of law.

### Spain and the AESIA: The Local Sheriff

The EU AI Act is a **European Regulation** (not a Directive), which means it is directly applicable in Spain without needing national legislative transposition. However, Spain has taken an additional step: in May 2026, the Council of Ministers approved the **Spanish AI Law**, which complements the European regulation and defines the role of the **AESIA (Spanish Agency for AI Supervision)** as the national competent authority.

The AESIA is the entity that will investigate complaints, conduct audits, and, where applicable, impose the AI Act's penalties on Spanish territory. Additionally, Spain has launched **regulatory sandboxes**: controlled environments where startups and companies can test innovative AI systems under AESIA supervision, without sanctioning risk during the trial period.

The Spanish startups we've analyzed on this blog are not strangers to this regulation. [Clarity AI](/en/posts/clarity_ai/) operates in ESG financial scoring, an area that Annex III classifies as high-risk. [Nextail](/en/posts/nextail/) makes inventory decisions with prescriptive AI in the supply chain. [Devo](/en/posts/devo/) protects critical military infrastructure, the most sensitive category in the regulation. All of them will need to demonstrate compliance.

### Compliance-as-Code: The Engineer's Checklist

If there's one thing we've learned building data pipelines on this blog, it's that documentation that isn't automated doesn't get maintained. Here's an actionable checklist, designed so that a technical team can execute it sprint by sprint:

**Phase 1 — Inventory and Classification** *(Sprint 1)*
* Inventory all AI systems in your organization (including ones you don't call "AI" but internally use ML)
* Classify each system in the risk pyramid: Prohibited / High / Limited / Minimal
* For each system classified as High Risk, assign a technical compliance owner

**Phase 2 — Technical Implementation** *(Sprints 2-4)*
* Implement automatic logging of model decisions (Art. 12): timestamps, inputs, outputs, confidence scores
* Create living technical documentation (Art. 11 + Annex IV): architecture, data, metrics, process
* Design human oversight mechanism (Art. 14): manual approval, "kill switch" button, monitoring dashboards
* Audit training datasets (Art. 10): bias, representativeness, traceability, versioning

**Phase 3 — Continuous Management** *(Ongoing)*
* Establish risk management pipeline (Art. 9): periodic review, Concept Drift monitoring, mitigation plan
* For Limited Risk systems: verify the user knows they're interacting with AI
* Configure cost and usage alerts (connect with [The Hidden Economics of AI](/en/posts/hidden_economics_ai/): compliance is an additional hidden cost)
* Register the system in the EU public database (when applicable for high-risk)

### The Regulation Isn't the Enemy; Ignorance Is

There is an understandable temptation to see the EU AI Act as a bureaucratic brake on European innovation. And in part, the criticism has merit: the definition of "high-risk" in Annex III is extremely broad, the documentation burden of Annex IV can be disproportionate for a five-person startup, and the uncertainty around the *Digital Omnibus* generates paralysis in legal teams.

But if you strip away the legal jargon and look at the bare technical requirements, what the regulation actually asks is: **document your system, control your data, log your AI's decisions, manage risks continuously, and keep a human in the control loop**. In other words, exactly what a good engineer should already be doing.

If you've followed the practices we've documented on this blog — [data hygiene with Z-Score](/en/posts/sop_engineering-data-hygiene/), [automatic logging with FastAPI and Supabase](/en/posts/obs_part6_fastapi_server/), [human-in-the-loop with GitHub Environments](/en/posts/ai_agents_part5/), [risk management with Deming's PDCA cycle](/en/posts/deming/) — **you're already 80% of the way to compliance**. The remaining 20% is formalization and documentation.

As Deming said: *"It is not enough to do your best; you must first know what to do."* Now the regulation tells you what to do. How to do it, you already know. Or at least, you have a blog where you can find it.

---

#### Sources of Interest:
* [**Regulation (EU) 2024/1689**: Full text of the EU AI Act on EUR-Lex (EN)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)
* [**European Commission**: Official EU AI Act page](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
* [**EU AI Act Explorer**: Navigable guide through the regulation's articles](https://artificialintelligenceact.eu/)
* [**digital.gob.es**: Information about the AESIA and AI regulation in Spain](https://portal.mineco.gob.es/es-es/digitalizacion/Paginas/ia.aspx)
* [**Datalaria**: The Hidden Economics of AI — Real Production Costs](/en/posts/hidden_economics_ai/)
* [**Datalaria**: W. Edwards Deming — The Father of Total Quality Who Predicted the Future of AI](/en/posts/deming/)
* [**Datalaria**: S&OP Data Hygiene — Why Your Spreadsheet Lies to You](/en/posts/sop_engineering-data-hygiene/)
* [**Datalaria**: Autopilot Part 5 — From Localhost to the Cloud with GitHub Actions and CI/CD](/en/posts/ai_agents_part5/)
