"""
ops/growth/build_activation_kit.py
----------------------------------
Factoría determinista del Hito 9.5 (Datalaria Mercator · INV-HELIX-WL-4 / INV-MERCATOR-UTM-1 / INV-AUTO-6).

Compila desde:
  - data/growth/lifecycle_flows.yaml
  - data/growth/launch_pack_obs_helix.yaml

Hacia packages/growth/hito_9_5/ (gitignored, fuera de static/ y fuera de data/):
  1. brevo_html/<flow>_step<n>_<lang>.html (20 plantillas HTML 600px listas para Brevo Automations)
  2. brevo_html/BREVO_SETUP_GUIDE.md
  3. LINKEDIN_SEMANAS_1_2_READY.md
  4. DIRECTORIOS_4_SUBMISSIONS_READY.md
  5. CREDENCIALES_Y_CUPON_RUNBOOK.md
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlsplit

import yaml

ROOT_DIR = Path(__file__).resolve().parents[2]
LIFECYCLE_PATH = ROOT_DIR / "data" / "growth" / "lifecycle_flows.yaml"
LAUNCH_PACK_PATH = ROOT_DIR / "data" / "growth" / "launch_pack_obs_helix.yaml"
DEFAULT_OUT_DIR = ROOT_DIR / "packages" / "growth" / "hito_9_5"

MALFORMED_FRAGMENT_UTM_RE = re.compile(r"#[^\s\"']*?\?[^\s\"']*utm_")


def _configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconf = getattr(stream, "reconfigure", None)
        if callable(reconf):
            try:
                reconf(encoding="utf-8", errors="replace")
            except Exception:
                pass


def validate_utm_url(url: str, context: str) -> None:
    """Garantiza INV-MERCATOR-UTM-1 e INV-HELIX-WL-4: HTTPS válido, cero mailto: y query antes de #fragment."""
    low = url.lower()
    if "mailto:" in low:
        raise ValueError(f"Violación INV-HELIX-WL-4 (mailto prohibido) en {context}: {url}")
    if MALFORMED_FRAGMENT_UTM_RE.search(url):
        raise ValueError(
            f"Violación INV-MERCATOR-UTM-1 (?utm_ detrás de #fragment) en {context}: {url}"
        )
    parts = urlsplit(url)
    if parts.scheme != "https" or not parts.netloc:
        raise ValueError(f"URL no HTTPS válida en {context}: {url}")
    if "datalaria.com" in parts.netloc.lower():
        if "utm_source=" not in parts.query or "utm_medium=" not in parts.query:
            raise ValueError(f"Faltan UTMs en query string real (antes de #) en {context}: {url}")


def render_brevo_email_html(
    *,
    skeleton: str,
    subject: str,
    preheader: str,
    value_bullets: List[str],
    cta_label: str,
    cta_url: str,
    secondary_cta_label: str | None = None,
    secondary_cta_url: str | None = None,
) -> str:
    """Renderiza un HTML tabular 600px compatible Outlook/Gmail (>80% texto, 0 imágenes pesadas)."""
    bullets_html = "".join(
        f'<p style="margin:0 0 8px;">• {html.escape(str(item))}</p>'
        for item in value_bullets
    )
    if secondary_cta_label and secondary_cta_url:
        bullets_html += (
            f'<p style="margin:10px 0 0;font-size:13px;">'
            f'<a href="{html.escape(secondary_cta_url, quote=True)}" style="color:#38bdf8;text-decoration:underline;">'
            f"{html.escape(secondary_cta_label)}</a></p>"
        )

    preheader_div = (
        f'<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">'
        f"{html.escape(preheader)}</div>\n"
    )
    rendered = (
        skeleton.replace("{{ params.SUBJECT }}", html.escape(subject))
        .replace("{{ params.VALUE_60S_HTML }}", bullets_html)
        .replace("{{ params.CTA_URL }}", html.escape(cta_url, quote=True))
        .replace("{{ params.CTA_LABEL }}", html.escape(cta_label))
    )
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        '<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">'
        f"<title>{html.escape(subject)}</title></head>\n"
        '<body style="margin:0;padding:0;background:#0b0f17;">\n'
        f"{preheader_div}{rendered}\n"
        "</body>\n</html>\n"
    )


def _walk_and_validate_urls(obj: Any, prefix: str) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and ("url" in k.lower()) and v.startswith("http"):
                validate_utm_url(v, f"{prefix}.{k}")
            else:
                _walk_and_validate_urls(v, f"{prefix}.{k}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            _walk_and_validate_urls(item, f"{prefix}[{idx}]")


def build_activation_kit(
    *,
    lifecycle_path: Path = LIFECYCLE_PATH,
    launch_pack_path: Path = LAUNCH_PACK_PATH,
    out_dir: Path = DEFAULT_OUT_DIR,
) -> Dict[str, Any]:
    """Valida ambos YAMLs de crecimiento y compila los artefactos accionables del Hito 9.5."""
    lifecycle_raw = lifecycle_path.read_text(encoding="utf-8")
    launch_raw = launch_pack_path.read_text(encoding="utf-8")
    if "mailto:" in lifecycle_raw.lower() or "mailto:" in launch_raw.lower():
        raise ValueError("Violación INV-HELIX-WL-4: detectado 'mailto:' en data/growth/*.yaml.")

    lifecycle = yaml.safe_load(lifecycle_raw)
    launch = yaml.safe_load(launch_raw)
    _walk_and_validate_urls(lifecycle, "lifecycle_flows")
    _walk_and_validate_urls(launch, "launch_pack_obs_helix")

    out_dir.mkdir(parents=True, exist_ok=True)
    brevo_dir = out_dir / "brevo_html"
    brevo_dir.mkdir(parents=True, exist_ok=True)

    skeleton = str(lifecycle["html_template_skeleton"]["table_layout_snippet"])
    coupon = lifecycle["cross_sell_coupon_spec"]
    lists = lifecycle["brevo_constraints"]["lists"]

    # 1. Compilar 20 plantillas HTML de Brevo + guía de configuración
    html_count = 0
    guide_lines = [
        "# 🔁 Brevo Automations — Guía de Activación Evergreen (Hito 9.5)",
        "",
        f"> **Coste mensual:** `0 €` · **Tope free tier:** `{lifecycle['brevo_constraints']['daily_send_cap']} emails/día` · "
        f"**Regla colisión `E05`:** {lifecycle['brevo_constraints']['digest_collision_rule']}",
        f"> **Listas configuradas:** Newsletter ES=`#{lists['newsletter_es']}`, Newsletter EN=`#{lists['newsletter_en']}`, "
        f"Helix Waitlist ES=`#{lists['helix_waitlist_es']}`, Helix Waitlist EN=`#{lists['helix_waitlist_en']}`.",
        "",
    ]

    for flow in lifecycle["flows"]:
        fid = flow["id"]
        embargo = flow.get("embargo_until")
        guide_lines.append(f"## {flow['name_es']} (`{fid}`)")
        guide_lines.append(f"- **Trigger:** `{flow['trigger']}`")
        if embargo:
            guide_lines.append(f"- **Embargo comercial (`INV-AUTO-6`):** `{embargo}` (NO activar links de checkout antes).")
        guide_lines.append("")
        guide_lines.append("| Paso | Delay | Idioma | Asunto | Archivo HTML listo |")
        guide_lines.append("| :-: | :-: | :-: | :--- | :--- |")

        for step_obj in flow["emails"]:
            step_num = step_obj["step"]
            delay_label = (
                f"Fecha fija `{step_obj['scheduled_date']}`"
                if "scheduled_date" in step_obj
                else f"D+{step_obj['delay_days']}"
            )
            for lang in ("es", "en"):
                loc = step_obj[lang]
                fname = f"{fid}_step{step_num}_{lang}.html"
                html_doc = render_brevo_email_html(
                    skeleton=skeleton,
                    subject=loc["subject"],
                    preheader=loc["preheader"],
                    value_bullets=loc["value_60s"],
                    cta_label=loc["cta_label"],
                    cta_url=loc["cta_url"],
                    secondary_cta_label=loc.get("secondary_cta_label"),
                    secondary_cta_url=loc.get("secondary_cta_url"),
                )
                (brevo_dir / fname).write_text(html_doc, encoding="utf-8")
                html_count += 1
                guide_lines.append(
                    f"| {step_num} | {delay_label} | `{lang.upper()}` | {loc['subject']} | `{fname}` |"
                )
        guide_lines.append("")

    (brevo_dir / "BREVO_SETUP_GUIDE.md").write_text("\n".join(guide_lines), encoding="utf-8")

    # 2. Compilar Semanas 1-2 de LinkedIn Empresa (activos LIVE sin embargo)
    li_plan = launch["linkedin_company_4week_plan"]
    li_lines = [
        "# 💼 LinkedIn Página de Empresa — Semanas 1 y 2 Listas para Publicar (Hito 9.5)",
        "",
        f"> **Página de Empresa:** {li_plan['company_page_url']} (`INV-PULSE-12`: 0 perfiles personales, 0 scraping)",
        f"> **Meta 4 semanas:** {li_plan['target_4week_followers']} · **Atribución:** `ADR-033` UTMs verificados",
        "",
    ]
    li_post_count = 0
    for week in li_plan["weeks"]:
        if int(week["week"]) > 2:
            continue
        li_lines.append(f"## Semana {week['week']}: {week['theme']}")
        li_lines.append("")
        for p in week["posts"]:
            li_post_count += 1
            li_lines.append(f"### {p['day']} · Idioma `{p['lang'].upper()}` · Formato: {p['format']}")
            if p.get("recommended_visual"):
                li_lines.append(f"- **Imagen recomendada:** `{p['recommended_visual']}`")
            li_lines.append(f"- **CTA UTM verificada:** `{p['cta_url']}`")
            li_lines.append("")
            li_lines.append("```text")
            li_lines.append(str(p.get("full_post") or p["hook"]).strip())
            li_lines.append("```")
            li_lines.append("")

    (out_dir / "LINKEDIN_SEMANAS_1_2_READY.md").write_text("\n".join(li_lines), encoding="utf-8")

    # 3. Compilar 4 Directorios Gratuitos (respetando embargos INV-AUTO-6)
    dirs = launch["directories_and_marketplaces"]["ai_and_devtools_directories"]
    dir_lines = [
        "# 🌐 Alta en 4 Directorios Gratuitos — Fichas Listas Hito 9.5 (Coste 0 €)",
        "",
        "> **Regla de Embargo (`INV-AUTO-6`):** Todos los envíos inmediatos del Hito 9.5 apuntan exclusivamente a **Sandboxes LIVE** (`obs-management` y `pulse`). **`pack-sdd` / `Helix` queda diferido al `2027-01-19` (`Hito 9.7`).**",
        "",
    ]
    for d in dirs:
        dir_lines.append(f"## {d['name']} ({d['url']})")
        dir_lines.append(f"- **Estado Hito 9.5:** `hito_9_5_ready={d.get('hito_9_5_ready')}` · **Productos LIVE:** `{', '.join(d.get('target_products', []))}`")
        if d.get("deferred_products_embargoed"):
            dir_lines.append(f"- **Diferido por embargo:** `{', '.join(d['deferred_products_embargoed'])}`")
        if d.get("alternative_to"):
            dir_lines.append(f"- **Alternativa a:** `{', '.join(d['alternative_to'])}`")
        dir_lines.append(f"- **Categorías sugeridas:** `{', '.join(d.get('categories', []))}`")
        dir_lines.append(f"- **URL con UTM (`ADR-033`):** `{d.get('tracked_url', '')}`")
        dir_lines.append(f"- **Tagline:** `{d.get('tagline', '')}`")
        dir_lines.append("")
        dir_lines.append("**Descripción lista para copiar:**")
        dir_lines.append("```text")
        dir_lines.append(str(d.get("short_description", "")).strip())
        dir_lines.append("```")
        dir_lines.append("")

    (out_dir / "DIRECTORIOS_4_SUBMISSIONS_READY.md").write_text("\n".join(dir_lines), encoding="utf-8")

    # 4. Runbook de Credenciales + Cupón DATALARIA-UPGRADE20
    runbook = "\n".join(
        [
            "# 🔐 Runbook del Fundador — Credenciales Reales y Cupón `DATALARIA-UPGRADE20` (Hito 9.5)",
            "",
            "## 1. Conectar Lemon Squeezy + Brevo en Local y GitHub Secrets",
            "1. **Lemon Squeezy (`Settings → API`):** Crea una API key de solo lectura y anota tu **Store ID** (número en `Settings → Stores`).",
            "2. **Brevo (`SMTP & API → API Keys`):** Reutiliza tu `BREVO_API_KEY` (ya está activa en GitHub Secrets).",
            "3. **Añadir en `.env` local (en `.gitignore`, nunca commitear):**",
            "   ```dotenv",
            "   LEMON_SQUEEZY_API_KEY=tu_api_key_real",
            "   LEMON_SQUEEZY_STORE_ID=tu_store_id_numerico",
            "   BREVO_API_KEY=tu_brevo_api_key",
            "   SUPABASE_URL=https://wkbmxekmofrjtcsyytrv.supabase.co",
            "   ```",
            "4. **Añadir en GitHub Secrets (para ejecución nocturna en `pulse.yml`):**",
            "   ```powershell",
            "   gh secret set LEMON_SQUEEZY_API_KEY",
            "   gh secret set LEMON_SQUEEZY_STORE_ID",
            "   ```",
            "5. **Verificar en vivo (0 PII, gitignored):**",
            "   ```powershell",
            "   python -m ops.pulse.sync_revenue --strict",
            "   python -m ops.pulse.sync_admin_snapshot",
            "   ```",
            "",
            f"## 2. Cupón Progresivo `{coupon['code']}` en Lemon Squeezy (`OPP-MON-01`)",
            f"- **Nombre interno (factura):** `{coupon.get('name', coupon['code'])}`",
            f"- **Código checkout (alfanumérico sin guiones):** `{coupon['code']}`",
            f"- **Descuento:** `{coupon['discount_value']}%` (`{coupon['discount_type']}`)",
            f"- **Límite:** `{coupon['max_uses_per_buyer']}` uso por email comprador · Validez recomendada `{coupon['validity_days']}` días",
            f"- **Productos elegibles:** `{', '.join(coupon['eligible_products'])}`",
            f"- **Productos EXCLUIDOS (embargo `INV-AUTO-6`):** `{', '.join(coupon['excluded_embargoed_products'])}`",
            "",
            "## 3. Webhook Automático Lemon Squeezy → Brevo (`/.netlify/functions/lemonsqueezy-webhook`)",
            "1. **En Brevo (`Contacts → Lists`):** Crea 2 listas nuevas (`Buyers ES` y `Buyers EN`) y anota sus IDs numéricos.",
            "2. **En Netlify (`Site configuration → Environment variables`):** Añade:",
            "   - `LEMON_SQUEEZY_WEBHOOK_SECRET`: genera una cadena aleatoria segura (ej. 32+ caracteres).",
            "   - `BREVO_BUYERS_LIST_ES`: ID numérico de `Buyers ES`.",
            "   - `BREVO_BUYERS_LIST_EN`: ID numérico de `Buyers EN`.",
            "   *(Verifica que `BREVO_API_KEY` ya existe en Netlify y dispara un deploy para aplicar las variables).* ",
            "3. **En Lemon Squeezy (`Settings → Webhooks → +`):**",
            "   - **Callback URL:** `https://datalaria.com/.netlify/functions/lemonsqueezy-webhook`",
            "   - **Signing secret:** pega exactamente el mismo valor de `LEMON_SQUEEZY_WEBHOOK_SECRET`.",
            "   - **Event:** selecciona `order_created`.",
            "",
        ]
    )
    (out_dir / "CREDENCIALES_Y_CUPON_RUNBOOK.md").write_text(runbook, encoding="utf-8")

    return {
        "out_dir": out_dir.as_posix(),
        "brevo_html_count": html_count,
        "linkedin_week1_2_count": li_post_count,
        "directories_count": len(dirs),
    }


def main(argv: List[str] | None = None) -> int:
    _configure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Compila el kit accionable del Hito 9.5 (Brevo + LinkedIn + Directorios).")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args(argv)
    try:
        summary = build_activation_kit(out_dir=args.out_dir)
        print(
            f"[HITO 9.5 KIT] Compilado en {summary['out_dir']} -> "
            f"{summary['brevo_html_count']} HTMLs Brevo, "
            f"{summary['linkedin_week1_2_count']} posts LinkedIn W1-W2, "
            f"{summary['directories_count']} directorios."
        )
        return 0
    except Exception as exc:
        print(f"[HITO 9.5 KIT ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
