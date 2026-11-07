---
title: "Deterministic XS–XL Triage and Multi-Tool Adapters: How to Cut Token Spend by 87% in Antigravity, Claude Code, Cursor, and Codex"
date: 2027-01-26
draft: false
cover:
  image: "cover.png"
  alt: "Datalaria Helix: Deterministic XS-XL Triage and Multi-Tool Adapters"
  caption: "Datalaria Helix (2/5) — Deterministic XS–XL Triage, 87% Context Reduction, and Multi-Tool Compiler"
  relative: true
image: "cover.png"
category: "AI, Engineering & Projects"
categories: ["Software Engineering", "Spec-Driven Development", "AI Agents", "AI, Engineering & Projects"]
tags: ["Datalaria Helix", "Spec-Driven Development", "SDD", "Agentic Triage", "Token Optimization", "Google Antigravity", "Claude Code", "Cursor Rules", "DevOps"]
description: "Why loading dozens of agentic instructions degrades LLM context windows, and how Helix's mathematical triage algorithm and deterministic compiler slash token consumption by 87% with zero friction across Antigravity, Claude, and Cursor."
summary: "The costliest mistake in AI-assisted development is dumping hundreds of instructions into the initial system prompt expecting the model to remember them all. In this second installment of Datalaria Helix, we reveal our deterministic triage engine (sizes XS to XL), non-negotiable mandatory triggers (TRG-SEC, TRG-UX, TRG-I18N), anti-bloat hygiene invariants, and the compiler synchronizing 26 cross-platform adapters from a single canonical spec."
translationKey: "helix-part2"
---

One of the most widespread and costly mistakes made by engineering teams attempting to professionalize artificial intelligence workflows is treating the language model's context window as an infinite storage container.

The initial impulse is understandable: you assemble a directory containing fifteen style guides, microservice architectural standards, TypeScript type-checking rules, corporate security policies, and detailed agent role descriptions. Next, you dump all of those documents into the editor's global instruction file (such as a massive `.cursorrules`, a 2,000-line `CLAUDE.md`, or a bloated system prompt).

The practical outcome is disastrous:
- The model consumes between 80,000 and 140,000 input tokens on every single conversational turn simply reading its own instructions.
- The transformer's mathematical attention fragments across hundreds of secondary guidelines, causing it to disregard foundational security rules and commit elementary errors on trivial tasks (*Prompt Bloat*).
- API bills explode exponentially without yielding a single percentage point of improvement in code quality.

In **Datalaria Helix**, we resolve this challenge through two formal engineering pillars: the **On-Demand Loading Invariant (`INV-HELIX-2`)** governed by a **Deterministic Sizing Matrix (`XS` to `XL`)**, and an **Automated Multi-Tool Adapter Compiler (`ops/helix/build_adapters.py`)** that deterministically synchronizes 26 native artifacts for Google Antigravity, Claude Code, Cursor IDE, and OpenAI Codex from a single canonical specification.

The empirical result is a **~87% reduction in token consumption** (slashing token spend from ~140,000 tokens in unconstrained sessions down to ~18,500 tokens per bounded task), eliminating cognitive distraction and maximizing model precision.

---

### 🗺️ Datalaria Helix Editorial Series Roadmap

1. ⚪ **Part 1:** [The Specification is Your App's DNA: Why Vibe Coding Collapses in 48 Hours and How Helix's 12-Agent Squad Governs AI Development](/en/posts/helix-part1-spec-dna-12-agent-engineering-squad/).
2. 🟢 **Part 2 (This article):** *Deterministic XS–XL Triage and Multi-Tool Adapters: How to Cut Token Spend by 87% in Antigravity, Claude Code, Cursor, and Codex.*
3. ⚪ **Part 3:** [The Deterministic Muscle: Zero-Dependency Python CLI helix.py, Formal SpecQualityScore (0..100), and 2-Failure Automatic Rollback](/en/posts/helix-part3-zero-dependency-python-cli-spec-score-rollback/).
4. ⚪ **Part 4:** [Helix Spec Builder in React 19 + TypeScript: Mode A Client-Side PKZIP Bundling and Mode B Mega-Prompt Exporter](/en/posts/helix-part4-react-sandbox-spec-builder-client-side-zip/).
5. ⚪ **Part 5:** [Empirical Evidence of Veto in Action: The Datalaria Pulse Audit ("Operation Crisol"), MarginGuard B2B, and Commercial Kits](/en/posts/helix-part5-real-case-studies-pulse-crisol-marginguard-kits/).

---

## 1. The Pathology of Prompt Bloat: Why More Rules Produce Worse Code

In modern generative language models, the cognitive penalty of processing irrelevant instructions during an active task is not linear: it is hyperbolic.

If an engineer needs to fix a minor typo on a UI button or tweak a card's padding token, injecting Supabase SQL migration guidelines, Lemon Squeezy webhook protocols, and PyMuPDF vector drawing manuals provides zero value. Quite the contrary: it introduces distractor vectors where the model attempts to "demonstrate holistic knowledge" by refactoring adjacent modules that nobody requested to touch.

```
TOKEN CONSUMPTION COMPARISON PER SESSION:
Vibe Coding / Mega-Prompts: [========== 140,000 tokens ==========] (Cognitive noise)
Datalaria Helix SDD:       [== 18,500 ==] (-87% Direct savings & laser focus)
```

For this reason, the Datalaria Helix Constitution establishes an explicit, inviolable rule:

> **Invariant INV-HELIX-2 (On-Demand Role Loading):** Loading all 12 agent specifications simultaneously into a session's context window for `XS`, `S`, or `M` tasks is strictly prohibited. Every agent must execute deterministic triage and load exclusively the files corresponding to explicitly activated roles.

---

## 2. The Mathematical Triage Algorithm: Sizing Tasks from XS to XL

How does the operating system decide which agents to activate without relying on subjective human intuition? Via a deterministic algorithm parameterized across three objective variables:

1. The estimated count of modified files ($F \in \mathbb{N}$).
2. The set of technical surfaces touched ($S \subseteq \{\text{docs}, \text{ui}, \text{frontend}, \text{backend}, \text{data\_sql}, \text{apis}, \text{media\_i18n}, \text{monetization}, \text{auth\_security}\}$).
3. Boolean flags indicating specification contract modifications ($\Delta_{\text{spec}} \in \{0, 1\}$) or new application creation ($\Delta_{\text{app}} \in \{0, 1\}$).

```
Base Sizing Allocation Logic:
- If Delta_app = 1                   ==> Size XL (Must decompose into N milestones <= L)
- If Delta_spec = 1 or |S| >= 3      ==> Size L  (Expanded squad activation)
- If |S| = 2 or F > 3                ==> Size M  (Architecture + Builders + Release)
- If 1 < F <= 3 and |S| = 1          ==> Size S  (Direct Builder + QA)
- If F = 1 and |S| = 1 and Delta_spec = 0 ==> Size XS (Targeted Builder + QA)
```

### Canonical Task Sizing Matrix:

| Size | Deterministic Objective Criteria | Squad Activation | Loaded Specs | Real-World Example in Datalaria |
| :-: | :--- | :--- | :-: | :--- |
| **`XS`** | $F = 1$ file · $1$ non-sensitive surface · $\Delta_{\text{spec}} = 0$ | `01` + $1$ Builder + `11-qa` | **2–3** | Fixing a typo or tweaking a CSS design token variable. |
| **`S`** | $1 \le F \le 3$ files · $1$ technical surface · Zero architectural changes | `01` + $1\text{–}2$ Builders + `11-qa` | **3–4** | Adding a date filter to a React table or writing a new `pytest` unit test. |
| **`M`** | $F > 3$ files **or** $2$ surfaces combined **or** minor contract adjustment | `01` + `03-architect` + $2\text{–}3$ Builders + `11-qa` + `12-release` | **4–6** | Integrating the Brevo waitlist modal across blog posts and catalog (Milestone 6.0). |
| **`L`** | Full feature creating/modifying a `spec.md` or business model logic | `01` + `02` + `03` + `04` + Builders + `10` + `11-qa` + `12-release` | **6–9** | Comprehensive audit and hardening of Datalaria Pulse and its ZIP kit (Milestone 6.3). |
| **`XL`** | Brand-new application or multi-module epic | **Execution in a single turn is prohibited.** Bounded into $N$ milestones $\le \mathbf{L}$. | Sequential | Full commercial release lifecycle of Datalaria Helix (Milestones 6.0 to 6.9). |

### The Canonical 6-Line Triage Card:

Before modifying a single file or running a code generation turn, the Orchestrator (`01-orchestrator`) emits a compact, structured triage block into the conversational stream:

```text
TRIAGE HELIX · Hito 6.2 · Talla: M
Superficies afectadas: backend, docs, auth_security
Roles activados (5 de 12): 🎯 01-orchestrator, 🏛️ 03-architect, 🗄️ 06-backend-data, 🛡️ 10-security-privacy, ✅ 11-qa-verifier (VETO)
Roles en banquillo: 02, 04, 05, 07, 08, 09, 12
Verification Gate: pytest ops/helix/tests -v ; python -m ops.helix.build_adapters --check ; hugo --renderToMemory
Presupuesto y Gobernanza: Máx. 2 intentos por gate · Checkpoint sdd-checkpoint-pre-6.2 · Aprobación humana previa: SÍ
```

Any agent not enumerated under **Roles activados** remains benched and **is never loaded into session memory**.

---

## 3. Non-Negotiable Mandatory Triggers (`INV-HELIX-3`)

A fatal flaw in naive triage systems is the temptation to classify as `XS` a task that modifies few lines of code but carries critical security ramifications (such as editing a variable in `.env` or loosening a Supabase Row Level Security policy).

To prevent this hazard, Helix codifies **Invariant INV-HELIX-3**:

> **Invariant INV-HELIX-3 (Non-Negotiable Mandatory Triggers):** No task, regardless of touching a single file or a single line of code, may be executed without summoning the designated specialist if any of the 5 mandatory triggers are detected:

1. **`TRG-SEC` (Security & Privacy):** Touches environment variables, authentication, Supabase RLS, serverless functions, payment gateways, or `/static/` $\implies$ Automatically activates [`10-security-privacy`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/10-security-privacy.md) with binding veto authority.
2. **`TRG-UX` (Design & Visual Experience):** Touches any user-facing interface element (`.tsx`, `.html`, `.css`, modals, color tokens) $\implies$ Automatically activates [`04-ux-ui`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md) to audit against `design.md` and WCAG 2.2 AA.
3. **`TRG-I18N` (Content & Linguistic Parity):** Touches articles in `content/`, metadata in `data/apps/*.yaml`, or `i18n` dictionaries $\implies$ Activates [`08-media-i18n`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/08-media-i18n.md) to enforce strict `ES ⇔ EN` parity and regenerate the Pulse index.
4. **`TRG-MON` (Monetization & Pricing):** Touches prices, Lemon Squeezy URLs, `/recursos/` cards, or analytics tracking $\implies$ Activates [`09-monetization`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/09-monetization.md).
5. **`TRG-QA` (Universal Quality Assurance):** Applies to **100% of all tasks** $\implies$ Activates [`11-qa-verifier`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/11-qa-verifier.md) with independent veto power.

---

## 4. Context Hygiene and Anti-Bloat Governance (`INV-HELIX-8`)

Over time, agentic systems tend to suffer from cumulative bloat: developers continuously add instructions, exceptions, and workarounds until system prompts exceed thousands of lines.

Datalaria Helix prevents this degradation through **Invariant INV-HELIX-8**:

```
ANTI-BLOAT CONTEXT HYGIENE INVARIANTS (INV-HELIX-8):
1. Hard Spec Ceiling:   <= 85 total lines per canonical file in specs/squad/*.md
2. Friction Rule Limit: Maximum 6 rules in Section 6 ([USER-FIX] / [ENV-FIX])
3. Admission Criteria:  Strictly no general theory; only documented empirical friction
4. Warm Memory Isolation: TECH_RADAR.yaml and OPPORTUNITY_BACKLOG.md never load routinely
```

### Strict Admission Criteria: Empirical Friction Lessons Only

In Section `## 6` of each agent specification, **only rules derived from documented real-world friction are permitted**:
- **`[USER-FIX]`:** Explicit corrections issued by the human engineer following a model hallucination or drift in a prior session (e.g., *"prohibit the '&' character within Hugo Mermaid diagram node labels"*).
- **`[ENV-FIX]`:** Platform-specific runtime anomalies (e.g., *"in Windows PowerShell consoles, invoke npm.cmd instead of npm to avoid script execution policy blocks"*).

When an agent reaches 6 rules and a 7th lesson is learned, the Orchestrator applies **FIFO pruning** (dropping the oldest rule already internalized by the LLM) or performs synthetic rule fusion, permanently keeping the file under 85 lines.

---

## 5. The Multi-Tool Compiler: 1 Canonical Source Compiling 26 Adapters

One of the crowning engineering achievements of Datalaria Helix is its **absolute neutrality regarding AI tooling**. Helix does not lock you into a proprietary IDE or demand a specific vendor subscription: it operates identically across **Google Antigravity**, **Claude Code**, **Cursor IDE**, and **OpenAI Codex / GitHub Copilot**.

How do we achieve this without maintaining 4 drifting copies of each agent? Through our deterministic compiler: **`ops/helix/build_adapters.py`**:

{{< mermaid >}}
flowchart LR
    SRC["12 Canonical Markdown Specs\n(specs/squad/*.md)"] --> COMP["Python Compiler\n(ops/helix/build_adapters.py)"]
    COMP --> AGY[".agents/squad/\n12 Antigravity Adapters\n+ manifest.json"]
    COMP --> CLD[".claude/agents/\n12 Claude Code Subagents\n+ CLAUDE.md"]
    COMP --> CUR[".cursor/rules/\nhelix-squad.mdc\n(Cursor IDE Rule)"]
    COMP --> CDX["AGENTS.md\n(OpenAI Codex / Copilot\nUniversal Entrypoint)"]
{{< /mermaid >}}

### Deterministic & Idempotent CI/CD Execution:

The compiler is integrated directly into the automated verification pipeline:

```bash
# Compile and propagate adapters across all tool directories
python -m ops.helix.build_adapters

# Verify synchronization in CI/CD (exits with code 1 if drift is detected)
python -m ops.helix.build_adapters --check
```

From the 12 master specifications in `specs/squad/`, the compiler automatically generates:
1. **For Google Antigravity:** 12 Markdown files optimized for Gemini models in `.agents/squad/<id>.md` and the structured `.agents/squad/manifest.json`.
2. **For Anthropic Claude Code:** 12 subagents with YAML invocation frontmatter in `.claude/agents/<id>.md`.
3. **For Cursor IDE:** The unified global rule featuring deterministic triage guidelines in `.cursor/rules/helix-squad.mdc`.
4. **For OpenAI Codex / GitHub Copilot:** The governance protocol and 3-step boot sequence in `AGENTS.md`.

Compiled adapters are strictly read-only build artifacts (`INV-HELIX-4`). Editing them manually is strictly prohibited: every improvement is made exclusively in the canonical `specs/squad/` file and propagated in under one second by the compiler.

---

## 6. Adopt Spec-Driven Governance in Your Own Repository

The deterministic triage discipline and adapter compilation architecture governing Datalaria Helix are designed to be deployed into any software repository within minutes.

{{< app-ref slug="helix" >}}

### Start Building with Datalaria Helix Today:

1. **Test the Triage Engine in the Web Sandbox ([/apps/helix/](/apps/helix/)):**  
   Input your project's technical specifications into our interactive configurator. Watch the engine size your task in real time, identify mandatory triggers, and select the exact minimal squad required for your stack.  
   👉 [**Test the Live Triage Engine in the Sandbox →**](/apps/helix/)

2. **Acquire the Core Kit with All Pre-Compiled Adapters:**  
   Visit our resources section to download the **Datalaria Helix Core Kit** at the Early-Bird launch price of **19 €** (regularly **39 €**). It includes the 12 canonical specs, the `build_adapters.py` compiler, all 26 ready-to-copy adapters, the zero-dependency CLI `helix.py`, and 3 production blueprints.  
   🚀 [**Download Datalaria Helix Core Kit in Resources →**](/en/resources/#pack-sdd)

In our upcoming installment (*Part 3/5*), we will explore the **deterministic muscle** of the operating system: the standard library Python CLI `helix.py`, the 5-pillar mathematical **SpecQualityScore (0..100)**, and the **Automatic Rollback Protocol on two consecutive failures**.
