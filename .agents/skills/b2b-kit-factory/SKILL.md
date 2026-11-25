---
name: b2b-kit-factory
description: Deterministic factory blueprint for Datalaria B2B downloadable Kits (Excel .xlsx with openpyxl, 4-to-5-page A4 vector PDF guides with PyMuPDF, 1600x980 composite previews, 1200x750 covers, numbered ZIP packaging, SHA-256 manifests, and Lemon Squeezy embargo scripts). Trigger for 06-backend-data, 08-media-i18n, 09-monetization, and 12-release-devops.
---

# Datalaria B2B Kit Factory Skill (Excel + PDF + Visuals + ZIP + Embargo)

Use this progressive skill whenever creating, updating, or verifying a commercial B2B Kit (`packages/<slug>/`, `packages/00_DISTRIBUCION_LEMONSQUEEZY/`, `ops/<slug>/build_kit.py`, or `ops/<slug>/release_*.py`).

## 1. Automated Excel Workbooks (`openpyxl` — `06-backend-data`)
- **Universal Compatibility (`INV-PULSE-5`):**
  - Zero VBA macros (`.xlsx` only, never `.xlsm`). Use standard English openpyxl formula names (`COUNTA`, `COUNTIF`, `IF`, `INDEX`, `MATCH`, `SUMPRODUCT`, `RANK`, `AVERAGEIF`) so Excel auto-translates them to the user's locale on open.
- **Executive Visual Hierarchy & Protection:**
  - Dark Navy headers (`#0F172A`) with crisp white bold text, Zebra data rows, `freeze_panes`, native Excel Tables / AutoFilter on data tabs, and `DataValidation` dropdown lists bound to a canonical `Taxonomía` / `Taxonomy` sheet.
  - Lock formula cells (`Protection(locked=True)`) while unlocking user input cells (`Protection(locked=False)`), and configure A4 Landscape print setup (`fitToWidth=1`, `fitToHeight=0`).
- **Dual Edition (`ES/` & `EN/`) & Strict Data Isolation:**
  - Build both Spanish and English workbooks when targeting international B2B buyers.
  - **Never** package private Datalaria trackers (`data/pulse/private/*`) inside commercial `.zip` archives; generate clean synthetic 10-row sample datasets.

## 2. Executive A4 PDF Guides (`PyMuPDF / fitz` — `06-backend-data`, `08-media-i18n`)
- **Vector Typography & Zero Tofu (`□`) Invariant:**
  - Standard PDF Base-14 fonts (`helv`, `hebo`, `cour`) only support WinAnsi/Latin-1 and render emojis or extended Unicode symbols as empty boxes (`□`).
  - Always sanitize text or draw custom vector badges/icons via `page.new_shape()` (`draw_rect`, `draw_circle`, `draw_line`) and verify via `pymupdf` text extraction in `pytest` that `len(doc) == expected_pages` and `0` replacement characters appear.

## 3. Marketing Previews & App Covers (`Pillow` — `08-media-i18n`)
- **Catalog Modal Previews (`1600×980` px):**
  - Save under `static/images/recursos/<slug>-preview-{es,en}.png`. Render real composite product screenshots (App UI + PDF/Excel + Architecture badge), never generic placeholder wireframes.
- **App Card Covers (`1200×750` px, `16:10`):**
  - Save under `content/{es,en}/apps/<slug>/cover.png`. Keep all titles, badges, and KPIs strictly inside the horizontal **Safe Zone `x ∈ [145, 1055]`** and `y ∈ [55, 695]` so Hugo's `.Fill "720x620 Center"` thumbnail crop never clips text.

## 4. Numbered ZIP Packaging & Embargo Governance (`09-monetization`, `12-release-devops`)
- **Numbered Folder Topology & Dual Sync:**
  - Structure every `.zip` into numbered top-level folders (`01_...`, `02_...`, `03_...`) plus root `README.md` and `LICENSE.txt`.
  - Synchronize identical byte-for-byte copies to both `packages/<slug>/` and `packages/00_DISTRIBUCION_LEMONSQUEEZY/` and verify `zf.testzip() is None`.
- **Staged Embargo Lifecycle (`release_<date>.py`):**
  - Provide `--verify-embargo` (asserts `status: incubating` in `data/apps/<slug>.yaml`, `draft: true` in `content/{es,en}/apps/<slug>/index.md`, `status: coming` in catalog, and `100%` artifact presence with SHA-256 hashes) and `--activate` (atomic unfreeze to `live`/`active` + Lemon Squeezy checkout URL injection).
