---
name: modern-web-guidance
description: >-
  Search and retrieve Google Chrome / Edge / Firefox / MDN Modern Web Guidance (v1.0.1,
  GoogleChrome/modern-web-guidance-src) before designing or implementing HTML, CSS, client-side JS,
  Core Web Vitals (INP/LCP/CLS), accessibility, PWA, client security, or WebMCP features.
  Use FIRST for UI/UX (04-ux-ui), Frontend (05-frontend), Client Security (10-security-privacy),
  WebMCP/Browser AI (07-apis-integrations), and Legacy Audits (11-qa-verifier).
  Do NOT trigger for Python backends, SQL/RLS, Hugo Markdown prose, Git, or CI scripts.
---

# Modern Web Guidance (Helix Workspace Skill)

> **Upstream Source:** `GoogleChrome/modern-web-guidance-src` (`modern-web-guidance@latest` v1.0.1 · Stewarded by Google Chrome, Microsoft Edge, Mozilla Firefox & MDN · 209 guides, 262 web features, 52 deterministic `legacy-scan` rules).  
> **Helix Roles:** `04-ux-ui` · `05-frontend` · `07-apis-integrations` · `10-security-privacy` · `11-qa-verifier`  
> **Governance:** `ADR-031` · `INV-HELIX-2` · `INV-HELIX-8` (Progressive Disclosure — zero bloat on non-web tasks).

## Datalaria Baseline Browser Support Policy

- **Baseline Widely Available:** Adopt directly without fallbacks or third-party polyfills (`<dialog>`, Popover API, Container Queries, `:has()`, `subgrid`, `oklch()`, `light-dark()`, `:user-invalid`, `text-wrap: balance`, `inert`, `content-visibility: auto`).
- **Baseline Newly Available / Limited Availability:** Allow ONLY with progressive enhancement (`@supports` or runtime feature detection) adding `<= 20` lines of custom fallback and **zero external dependencies** (e.g., CSS Anchor Positioning, View Transitions, Scroll-Driven Animations, `interpolate-size`, `scheduler.yield()`, WebMCP).
- **Platform-First Invariant:** Reject heavy npm UI/positioning/modal libraries whenever a native Baseline platform primitive fulfills the UX requirement with better accessibility and INP.

## Primary Workflow (Before Designing or Coding Web UI/Client JS)

### 1. Search Use Cases (2–5 Word Action-Oriented English Query)
Describe the user-visible capability or UI primitive (`<verb> + <UI/platform object>`), omitting framework names (`React`, `Vite`, `Hugo`) and domain nouns. Split multi-feature tasks into separate searches.

```powershell
# Windows PowerShell (always use npx.cmd to avoid .ps1 ExecutionPolicy blocks)
npx.cmd -y modern-web-guidance@latest search "light dismiss dialog"
npx.cmd -y modern-web-guidance@latest search "responsive data table"
npx.cmd -y modern-web-guidance@latest search "break up long tasks"
```

- Judge results by `description`. If a match is found, call `retrieve` directly (do not also call `list`).
- If results are weak/empty, rephrase once with the concrete HTML/CSS/UI noun (`dialog`, `popover`, `anchor`, `table`, `form`, `inp`, `pwa`).
- If offline or sandboxed without outbound network, retry with `npx.cmd --offline modern-web-guidance ...` or rely on local Baseline knowledge and note it clearly.

### 2. Retrieve Full Guide(s)
Pass one or more comma-separated IDs (both the specific use-case ID and applicable discipline guide such as `css-layout`, `accessibility`, `forms`, `color`, `performance`, `security`, `pwa`, `webmcp`):

```powershell
npx.cmd -y modern-web-guidance@latest retrieve "dialog,light-dismiss-a-dialog"
```

If `retrieve` writes output > 9.5 KB to a temporary file path, read that file with `read_file` in full.

### 3. Adapt to Datalaria Stack Without Dropping Modern Features
- **React 19 + TypeScript (`apps/*/web/`):**
  - Call `showModal()` / `moveBefore()` via `ref` on non-VDOM-managed nodes.
  - Generate per-instance IDs and `anchor-name` values with React `useId()`.
  - Keep `:root`, `@starting-style`, and `@keyframes` top-level/unscoped.
  - Cast/spread newly shipped HTML attributes cleanly without dropping native semantics or triggering `oxlint` warnings.
- **Zero-CDN Monolithic Apps (`apps/conversor/`, `apps/maths/`, `apps/reading/`, `apps/weather/`):**
  - Keep 100 % native vanilla HTML/CSS/JS with zero external CDNs; respect `prefers-reduced-motion`, `forced-colors`, and OS `rem` text scaling.
- **PWA & Resilience:**
  - Use `Network-First` for HTML/App Shell + `Stale-While-Revalidate` for compact JSON derived data, `hadController` guard on `controllerchange`, and clean `localhost` unregister (`?pwa_test=1` bypass).

### 4. Verify & Disclose
- Cross-check implementation against the retrieved guide's rules and fallback clauses before handoff to `11-qa-verifier`.
- In `DEBRIEF HELIX` (or design/PR notes), cite applied guide `<id>`s and the concrete legacy pitfall prevented.

## Modernization Workflow (`11-qa-verifier` & Open-Ended Audits ONLY)

Do **not** run `legacy-scan` on narrow feature edits; run it ONLY when performing a broad codebase modernization audit:

```powershell
npx.cmd -y modern-web-guidance@latest legacy-scan apps/<slug> --json
```

1. **Scan:** Runs 52 deterministic AST/DOM/CSS rules across ~20 % of the corpus at zero token cost.
2. **Filter (`keepWhen` / `dropWhen`):** Drop false positives (intentional fallbacks, vendor bundles, cross-file helpers).
3. **Prioritize:** Feed verified modernization opportunities into `specs/squad/OPPORTUNITY_BACKLOG.md` (with RICE score) or execute when explicitly requested by the user.
