---
name: pwa-offline-arcade-builder
description: Architecture and verification blueprint for Datalaria Zero-CDN Monolithic Offline PWAs, EdTech apps, and Arcade simulators (conversor, maths, flashcards, snake, reading, weather). Trigger for 04-ux-ui, 05-frontend, 08-media-i18n, and 11-qa-verifier when building or auditing static offline PWAs in /apps/<slug>/ and /static/apps/<slug>/.
---

# Datalaria Zero-CDN Monolithic Offline PWA & Arcade Builder Skill

Use this progressive skill whenever designing, building, or verifying a **100% Client-Side, Offline-First, Zero-CDN PWA** in the Datalaria ecosystem (`conversor`, `maths`, `flashcards`, `snake`, `reading`, `weather`, or new static micro-apps).

## 1. Zero-CDN & Single-File / Static Bundle Invariants (`INV-STATIC-1`)
- **Zero External CDNs in Production (`static/apps/<slug>/`):**
  - Never load Tailwind, React, Babel, Lucide, Google Fonts, or audio assets from external CDNs (`unpkg`, `jsdelivr`, `cdnjs`, `fonts.googleapis.com`) in the production bundle under `static/apps/<slug>/`.
  - If `/apps/<slug>/build.py` compiles a modular source tree (`apps/<slug>/*.js`, `*.css`) into a monolithic `static/apps/<slug>/index.html`, it must inline CSS (`<style>`) and JS (`<script>`) deterministically and copy offline assets (`manifest.json`, `sw.js`, `icons/icon-*.png`).
- **Anti-FOUC Theme Hydration:**
  - Inject a synchronous inline `<script>` inside `<head>` before first paint to read `localStorage` (`theme: 'dark' | 'light'`) and apply `data-theme` on `document.documentElement` with `0 ms` flash.

## 2. Offline PWA & Service Worker Lifecycle (`05-frontend`, `11-qa-verifier`)
- **Manifest & 6 Standard Icons (`build_icons.py`):**
  - Every PWA in `static/apps/<slug>/` must ship a valid `manifest.json` (`display: "standalone"`, `start_url: "/apps/<slug>/"`, `scope: "/apps/<slug>/"`) and 6 deterministic PNG icons generated via Pillow (`icon-192.png`, `icon-512.png` with `"purpose": "any"`, `icon-maskable-192.png`, `icon-maskable-512.png` with `"purpose": "maskable"`, `apple-touch-icon.png` `180×180`, and `favicon-32.png` `32×32`).
- **Service Worker (`sw.js`) Update & Anti-Loop Rules:**
  - Use **Network-First** for HTML navigation (`request.mode === 'navigate'`) so new deployments appear immediately when online, falling back to cache when offline.
  - Use **Stale-While-Revalidate** for static same-origin assets (`icons/`, JSON datasets).
  - **First-Install Guard (`hadController`):** In the `controllerchange` listener, record `const hadController = Boolean(navigator.serviceWorker.controller);` before registration and only reload (`window.location.reload()`) when `hadController === true`, preventing infinite reload loops on first visit.

## 3. EdTech, Gamification & Procedural Audio/SVG (`04-ux-ui`, `08-media-i18n`)
- **Procedural Web Audio & Offline Web Speech TTS:**
  - Synthesize arcade sound effects (`success`, `error`, `levelUp`, `click`, `fanfare`) via the native `AudioContext` API (`OscillatorNode` + `GainNode`) with zero external `.mp3`/`.wav` requests and a persistent Mute toggle.
  - For language/reading apps (`flashcards`, `reading`), wrap `window.speechSynthesis` with explicit language selection (`es-ES`, `en-US`), normal (`1.0x`) and slow/syllable (`0.5x`) playback rates, and graceful fallback when voices are unavailable.
- **Deterministic Daily Challenge (`Mulberry32` PRNG):**
  - Seed daily challenges from the UTC date integer (`YYYYMMDD`) using a pure 32-bit `mulberry32(seed)` PRNG so every user gets the exact same daily seed offline without a backend coordinator.
- **100% Self-Contained Vector Illustrations (`INV-READ-13`):**
  - For educational cards where emojis are ambiguous, use inline semantic `<svg viewBox="0 0 120 120">` maps indexed by item ID (`1:1` coverage, `0` external image requests).
