---
title: "An Engineer's Productivity Stack in 2026: The Tools I Use Every Day"
date: 2026-08-01
draft: false
categories: ["Engineering"]
tags: ["productivity", "tools", "stack", "engineer", "workflow", "python", "supabase", "github actions", "crewai", "hugo"]
description: "The real tool stack of a data engineer in 2026: from Gemini Deep Research to GitHub Actions, through Python, Supabase, CrewAI, and Hugo. No sponsorships, no affiliates, no filters. Every tool explained with the post where I use it."
summary: "After 60+ articles, 9 technical series, and 4 production applications, this is the real stack I use every day. No sponsorships, no affiliates, no filters. 10 tools organized by workflow phase, what I tried and discarded, and the total cost: less than €5 per month."
social_text: "After 60+ articles, 9 technical series and 4 production apps, this is my REAL productivity stack as an engineer in 2026. No sponsorships, no filters. Total cost: <€5/month ⚡🛠️🧠 #Productivity #Engineering #Stack #Tools"
image: cover.jpg
weight: 10
authorAvatar: datalaria-logo.png
---

After more than 60 articles, 9 technical series, 4 production applications, and a bilingual blog that generates weekly content, I get asked the same question over and over: **"What tools do you use?"** Not what tools I recommend, not what tools are trending, but which ones I actually use, every single day, to build what you see on Datalaria.

This article is the answer. No sponsorships, no affiliate links, no filters. Every tool listed here has been tested in production, paid for (or not) with my own money, and documented in at least one post on this blog. If I haven't used it in a real project, it's not on this list.

### The Workflow: 10 Phases, 10 Tools

The key to my productivity isn't in individual tools but in how they fit together. Each workflow phase feeds the next, and the output of one tool is the input of another. No silos; it's a pipeline.

![The complete workflow: from idea to deployment](workflow.jpg)

| Phase | Tool | Why this one |
| :--- | :--- | :--- |
| 🧠 **Think** | Gemini Deep Research | Exhaustive research in minutes |
| ✍️ **Write** | Hugo + VS Code + Markdown | Full control, Git-native, speed |
| 💻 **Code** | Python + Pandas + FastAPI | The data engineering trident |
| 🗄️ **Store** | Supabase (PostgreSQL) | Free BaaS, RLS, automatic REST APIs |
| 🤖 **Orchestrate AI** | CrewAI + Gemini 2.5 | Autonomous agents with Tool Calling |
| ⚙️ **Automate** | GitHub Actions | Free CI/CD, event-driven |
| 🚀 **Deploy** | Netlify | Deploy from Git in seconds |
| 📧 **Communicate** | Brevo (Newsletter) | Free email marketing, API, segmentation |
| 📊 **Visualize** | Chart.js + Vanilla JS | Lightweight, no heavy frameworks, interactive |
| 📚 **Learn** | NotebookLM | Transforms any source into study resources |

### 🧠 Think: Gemini Deep Research

Before writing a single line, I research. And this is where generative AI has radically changed my workflow. **Gemini Deep Research** (within Gemini Advanced) is the tool I use for exhaustive research before every article and every technical project.

When I was preparing the article on [Thomas Bayes](/en/posts/thomas_bayes/), I needed to verify dates, publications, historical context of the Royal Society, and the precise mathematical connection between Bayes' theorem and Facebook Prophet. What previously would have required hours of browsing through Wikipedia, Stanford Encyclopedia of Philosophy, and academic papers, Gemini Deep Research compiled into a structured report in **under 10 minutes**, with verifiable citations and sources.

The key: **I don't use it to write; I use it to research**. The final text is always mine. Gemini gives me the raw material; I build the narrative. I documented this approach in detail in [AI in Education with Deep Research](/en/posts/ai-education-deep_research/).

### ✍️ Write: Hugo + VS Code + Markdown

Everything you see on Datalaria is written in **pure Markdown**, edited in **VS Code**, compiled with **Hugo**, and versioned in **Git**. Zero WordPress, zero visual CMS, zero drag-and-drop.

Why this seemingly masochistic decision? Because a Hugo blog is **code**. I can run `git diff` to see what I changed in an article. I can run `git blame` to know when I changed it. I can fork, create a branch, experiment with a new structure, and merge only if it works. And I can automate deployment with a `git push`. I documented all these architectural decisions in [Building Datalaria](/en/posts/datalaria-blog/).

Hugo compiles the 700+ pages of this blog (Spanish + English) in **under 4 minutes**. A traditional CMS would take several seconds just to render a single page. When you iterate fast, compilation speed isn't a luxury; it's a necessity.

### 💻 Code: Python + Pandas + FastAPI

The trident I use for absolutely everything involving data:

* **Python** as the base language. No debate. The library ecosystem for data engineering, ML, and automation has no rival.
* **Pandas** for data manipulation, cleaning, and transformation. Every pipeline in the [S&OP series](/en/posts/sop-engineering-part2-forecasting/) — from sales data ingestion to forecast generation with Prophet — goes through Pandas.
* **FastAPI** when I need to expose a service as a REST API. We used it in [Part 6 of the Observability series](/en/posts/obs_part6_fastapi/) to build the obsolescence radar backend, and in the [OpenWeather app](/en/posts/app-openweather_part1_backend/) as a weather prediction backend.

### 🗄️ Store: Supabase (PostgreSQL)

**Supabase** is managed PostgreSQL with superpowers: authentication, Row Level Security (RLS), automatic REST APIs generated from the database schema, and a free tier that covers 95% of my development and prototyping needs.

I use it as the data backend in the [Observability series](/en/posts/obs_part4_ingestion/) (storing the component catalog, obsolescence alerts, and BOM graphs), in the [S&OP pipelines](/en/posts/sop-engineering-part3-optimization/) (demand data, forecasts, production plans), and in the [Snake game with a global leaderboard](/en/posts/game_snake/).

Why Supabase over Firebase? Because Supabase is **real PostgreSQL**. I can write native SQL, create materialized views, use complex JOINs, and migrate to any other managed PostgreSQL (RDS, Cloud SQL) without changing a single line of code. Firebase traps you in its proprietary ecosystem; Supabase includes the exit door.

### 🤖 Orchestrate AI: CrewAI + Gemini 2.5

When I need AI to not just answer questions but **execute complex multi-step tasks**, I use **CrewAI** as the agent orchestration framework. Each agent has a role, an objective, specific Python tools (decorated with `@tool`), and the ability to coordinate with other agents.

Gemini 2.5 Pro/Flash is the LLM powering the agents. The CrewAI + Gemini + Tool Calling combination is the architecture documented across the entire [9-part Autopilot series](/en/posts/ai_agents_part1/), from the automatic content generator to the Ops Copilot.

As we analyzed in the [RAG vs. Tool Calling article](/en/posts/rag_antipatterns/), the key is separating the "semantic brain" (the LLM understands context) from the "deterministic muscle" (Python tools execute precision operations). The LLM thinks; the tools do.

### ⚙️ Automate: GitHub Actions

Every CI/CD pipeline at Datalaria runs on **GitHub Actions**. It's free for public repositories, event-driven (triggers on push, cron, webhook), and flexible enough to orchestrate everything from Hugo compilation to CrewAI pipeline execution.

In [Autopilot Part 5](/en/posts/ai_agents_part5/), we documented how to configure a GitHub Actions workflow that runs the complete agentic pipeline every week: generates content with CrewAI, creates Markdown files, commits, pushes, and automatically deploys to Netlify. All without human intervention.

### 🚀 Deploy: Netlify

**Netlify** deploys Datalaria directly from the GitHub repository. Every `git push` to the `main` branch triggers a Hugo build and publishes the site in seconds. Features like Netlify Functions (serverless), redirects, and custom headers cover everything I need without managing servers.

We documented it in [OpenWeather app Part 2](/en/posts/app_openweather_part2_frontend/) as the deployment platform for frontend applications with serverless backends.

### 📧 Communicate: Brevo (Newsletter)

Datalaria's newsletter uses **Brevo** (formerly Sendinblue). Generous free tier (300 emails/day), REST API for automation, audience segmentation, and a template editor.

In [Autopilot Part 6](/en/posts/ai_agents_part6/), we documented how the CrewAI pipeline generates email content, builds the HTML, and sends it automatically via Brevo's API — closing the complete generation → publication → distribution cycle without manual intervention.

### 📊 Visualize: Chart.js + Vanilla JS

When I need interactive charts in web apps, I use **Chart.js** with **vanilla JavaScript**. No React, no Vue, no heavy frameworks. The philosophy is intentional: every library you add is a dependency to maintain, an attack surface to protect, and a bundle to inflate.

[OpenWeather app Part 4](/en/posts/app_openweather_part4_extras_ux/) and [Basic Visualizations](/en/posts/basic-visualizations/) demonstrate that Chart.js + pure CSS produces professional-quality interactive dashboards without needing a 200KB framework.

### 📚 Learn: NotebookLM

Google's **NotebookLM** is my accelerated learning tool. I upload technical documentation, academic papers, or conference transcripts, and NotebookLM generates summaries, study questions, and — most transformatively — **audio podcasts** where two hosts discuss the material as if it were a natural conversation.

I documented it in depth in [NotebookLM + SQL](/en/posts/notebooklm-sql/), showing how to transform PostgreSQL documentation into interactive study resources.

### What I Tried and Discarded

Not everything you try survives contact with production. These are the tools I evaluated and discarded, with reasons:

* **WordPress**: Used it for years. Abandoned it for the slowness, the plugins, the constant security updates, and the impossibility of versioning content with Git. Hugo is 100x faster and everything is code.
* **LangChain**: LLM orchestration framework I tried before CrewAI. Too much abstraction, deep inheritance chains that were hard to debug, and an API that changed with every minor version. CrewAI is simpler, more explicit, and more stable.
* **Streamlit**: Excellent for rapid data dashboard prototypes. But when you need control over the frontend (CSS, animations, UX), Streamlit becomes a straitjacket. For production, I prefer FastAPI + HTML/CSS/JS, where I have full control.
* **MongoDB**: Tried it as a PostgreSQL alternative for semi-structured data. But the lack of JOINs and the impossibility of complex relational queries quickly ruled it out for my industrial use cases (BOM graphs, demand table cross-referencing).

### Total Stack Cost: The Real Economics

This is where the [Hidden Economics of AI](/en/posts/hidden_economics_ai/) becomes directly relevant. How much does operating this entire stack cost?

| Tool | Monthly cost | Notes |
| :--- | :--- | :--- |
| Gemini Advanced | ~€22/month | Includes Deep Research, 2.5 Pro, etc. |
| Hugo | €0 | Open source |
| VS Code | €0 | Open source |
| Python + libraries | €0 | Open source |
| Supabase | €0 | Free tier |
| CrewAI | €0 | Open source |
| GitHub Actions | €0 | Free for public repos |
| Netlify | €0 | Free tier |
| Brevo | €0 | Free tier (300 emails/day) |
| Chart.js | €0 | Open source |
| NotebookLM | €0 | Included in Gemini Advanced |
| **TOTAL** | **~€22/month** | |

Virtually the entire stack is free or open source. The only recurring cost is the Gemini Advanced subscription, which covers both Deep Research and the models powering CrewAI agents. Even if we count Gemini API costs for Autopilot pipeline executions, the total rarely exceeds **€5 extra per month**.

Compare this with the cost of an "enterprise" stack: a licensed CMS (€50-500/month), a premium email marketing tool (€30-200/month), a managed hosting service (€20-100/month), and a BI platform (€50-300/month). The open source stack isn't just cheaper; it's **more powerful**, because every tool is a box you can open, inspect, modify, and learn from.

### The Philosophy: Learning > Comfort

If there's a common thread across every decision in this stack, it's this: **I prioritize learning over comfort**. Hugo is harder than WordPress, but I learned static site generation, Go templates, and CI/CD. FastAPI is more work than Streamlit, but I learned REST API design, async/await, and OpenAPI. Supabase with native SQL is more verbose than Firebase, but I learned real PostgreSQL, RLS, and migrations.

Every tool in the stack isn't just a tool; it's a **course**. And the 60+ articles on this blog are the notes from those courses, shared openly so anyone can walk the same path.

As [Deming](/en/posts/deming/) would say: *"Learning is not compulsory. Neither is survival."* In a world where AI redefines the rules of the game every quarter, the stack you use matters less than **your ability to learn the next stack**. And that ability is built by choosing tools that force you to understand what's under the hood.

---

#### Sources of Interest:
* [**Hugo**: Static Site Generator — Official Documentation](https://gohugo.io/)
* [**Supabase**: Open Source Backend as a Service](https://supabase.com/)
* [**CrewAI**: AI Agent Framework](https://www.crewai.com/)
* [**FastAPI**: Modern Web Framework for Python](https://fastapi.tiangolo.com/)
* [**Chart.js**: Open Source JavaScript Visualizations](https://www.chartjs.org/)
* [**Brevo**: Email Marketing Platform](https://www.brevo.com/)
* [**Datalaria**: Building the Blog — Architecture Decisions](/en/posts/datalaria-blog/)
* [**Datalaria**: The Hidden Economics of AI — The Real Stack Cost](/en/posts/hidden_economics_ai/)
* [**Datalaria**: Autopilot Series — 9 Parts of Agentic Engineering](/en/posts/ai_agents_part1/)
