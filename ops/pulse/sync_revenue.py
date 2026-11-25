"""
ops/pulse/sync_revenue.py
-------------------------
Extractor privado de Telemetría Financiera y Audiencia a Coste 0 € (Hito 9.2 / ADR-034 / INV-PULSE-13).
Especificación técnica formal: SPEC-APP-PULSE v1.6.0 (specs/apps/pulse/spec.md).

Responsabilidades:
1. Consultar gratuitamente Lemon Squeezy API v1 (`GET /v1/orders`, `/v1/products`, `/v1/checkouts`)
   mediante `LEMON_SQUEEZY_API_KEY` y `LEMON_SQUEEZY_STORE_ID`.
2. Consultar gratuitamente Brevo API v3 (`GET /v3/contacts/lists`, `/v3/emailCampaigns`)
   mediante `BREVO_API_KEY`.
3. Descartar el 100 % de PII en memoria antes de construir modelos Pydantic (`INV-PULSE-13`):
   prohibido persistir emails, nombres, IPs o direcciones de compradores.
4. Persistir únicamente en ficheros gitignored (`data/pulse/private/revenue_metrics.json`,
   `data/pulse/private/executive_state.json`, `data/pulse/private/REVENUE_REPORT.md`)
   con degradación elegante independiente por fuente (`INV-PULSE-11`).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

import requests

from ops.pulse.models import (
    BrevoAudienceSummary,
    BrevoCampaignSummary,
    BrevoListSummary,
    ExecutiveStateSnapshot,
    LemonSqueezySummary,
    RevenueCountryBreakdown,
    RevenueLanguageSlice,
    RevenueMetricsReport,
    RevenueMonthlyPoint,
    RevenueProductBreakdown,
)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PRIVATE_DIR = ROOT_DIR / "data" / "pulse" / "private"
REVENUE_METRICS_PATH = PRIVATE_DIR / "revenue_metrics.json"
EXECUTIVE_STATE_PATH = PRIVATE_DIR / "executive_state.json"
REVENUE_REPORT_PATH = PRIVATE_DIR / "REVENUE_REPORT.md"

INDEX_PATH = PRIVATE_DIR / "index.json"
IMPACT_REPORT_PATH = PRIVATE_DIR / "impact_report.json"
CHANNEL_METRICS_PATH = PRIVATE_DIR / "channel_metrics.json"
SOCIAL_METRICS_PATH = PRIVATE_DIR / "social_metrics.json"

LEMON_SQUEEZY_API_BASE = "https://api.lemonsqueezy.com/v1"
BREVO_API_BASE = "https://api.brevo.com/v3"

ES_COUNTRY_CODES = frozenset({
    "ES", "MX", "AR", "CO", "CL", "PE", "EC", "UY", "PY", "BO",
    "VE", "CR", "PA", "GT", "HN", "SV", "NI", "DO", "CU", "PR",
})
EN_COUNTRY_CODES = frozenset({"US", "GB", "CA", "AU", "NZ", "IE", "SG", "IN", "ZA"})

# Claves PII que nunca pueden filtrarse al resultado serializado (INV-PULSE-13)
FORBIDDEN_PII_KEYS = frozenset({
    "user_email",
    "user_name",
    "customer_email",
    "customer_name",
    "email",
    "first_name",
    "last_name",
    "billing_address",
    "ip_address",
    "receipt_url",
})


def _configure_utf8_stdio() -> None:
    """Evita errores cp1252/charmap en consola Windows al imprimir emojis o caracteres UTF-8."""
    for stream in (sys.stdout, sys.stderr):
        reconf = getattr(stream, "reconfigure", None)
        if callable(reconf):
            try:
                reconf(encoding="utf-8", errors="replace")
            except Exception:
                pass


def _load_local_env_if_needed() -> None:
    """Carga variables desde .env solo fuera de ejecuciones de pytest."""
    if "PYTEST_CURRENT_TEST" in os.environ:
        return
    try:
        from dotenv import load_dotenv

        for candidate in (ROOT_DIR / ".env", ROOT_DIR / "autopilot" / ".env"):
            if candidate.is_file():
                load_dotenv(candidate, override=False)
    except Exception:
        pass


def _safe_read_json(path: Path) -> Any:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _parse_iso_dt(raw: Optional[str]) -> Optional[datetime]:
    if not raw:
        return None
    try:
        cleaned = str(raw).strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def _extract_net_eur(attrs: Dict[str, Any]) -> float:
    """Convierte importes de pedido Lemon Squeezy (céntimos) a EUR netos de forma determinista."""
    currency = str(attrs.get("currency") or "EUR").strip().upper()
    subtotal = attrs.get("subtotal")
    total = attrs.get("total")
    tax = attrs.get("tax") or 0

    raw_cents = subtotal if subtotal is not None else max(0, int(total or 0) - int(tax or 0))
    try:
        cents = max(0.0, float(raw_cents))
    except Exception:
        cents = 0.0

    if currency == "EUR":
        return round(cents / 100.0, 2)

    # Si está en otra divisa, usar subtotal_usd / total_usd con tipo de cambio aproximado determinista
    # o currency_rate si Lemon Squeezy lo proporciona.
    usd_cents = attrs.get("subtotal_usd")
    if usd_cents is None:
        usd_cents = max(0.0, float(attrs.get("total_usd") or 0) - float(attrs.get("tax_usd") or 0))
    try:
        usd_val = max(0.0, float(usd_cents)) / 100.0
    except Exception:
        usd_val = cents / 100.0

    if usd_val > 0 and currency != "EUR":
        return round(usd_val * 0.92, 2)
    return round(cents / 100.0, 2)


def _extract_country_iso(attrs: Dict[str, Any]) -> str:
    """Extrae únicamente el código ISO-2 de país (nunca calle, ciudad ni código postal)."""
    billing = attrs.get("billing_address")
    country = ""
    if isinstance(billing, dict):
        country = str(billing.get("country") or "").strip().upper()
    if not country:
        country = str(attrs.get("country") or attrs.get("tax_country") or "").strip().upper()
    if len(country) == 2 and country.isalpha():
        return country
    return "UNK"


def _infer_order_lang(country: str, product_name: str) -> Literal["es", "en", "other"]:
    """Clasifica el pedido por idioma inferido sin acceder a ningún dato personal."""
    pname = product_name.lower()
    if "español" in pname or "(es)" in pname or "estrategia" in pname:
        return "es"
    if "(en)" in pname or "english" in pname:
        return "en"
    if country in ES_COUNTRY_CODES:
        return "es"
    if country in EN_COUNTRY_CODES:
        return "en"
    return "other"


def _fetch_ls_paginated(
    endpoint: str,
    headers: Dict[str, str],
    store_id: str,
    timeout: int = 12,
    max_pages: int = 20,
) -> List[Dict[str, Any]]:
    """Consulta paginada segura sobre Lemon Squeezy JSON:API v1."""
    items: List[Dict[str, Any]] = []
    next_url: Optional[str] = f"{LEMON_SQUEEZY_API_BASE}/{endpoint}?filter[store_id]={store_id}&page[size]=100"
    page_count = 0

    while next_url and page_count < max_pages:
        resp = requests.get(next_url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        payload = resp.json()
        batch = payload.get("data") or []
        if isinstance(batch, list):
            items.extend(batch)
        links = payload.get("links") or {}
        next_url = links.get("next") if isinstance(links, dict) else None
        page_count += 1
    return items


def fetch_lemon_squeezy_summary(
    api_key: Optional[str] = None,
    store_id: Optional[str] = None,
    now_utc: Optional[datetime] = None,
    timeout: int = 12,
) -> Tuple[bool, LemonSqueezySummary]:
    """
    Extrae estadísticas agregadas anónimas desde Lemon Squeezy API v1 (INV-PULSE-13).
    Descarta cualquier PII en memoria antes de construir LemonSqueezySummary.
    """
    now = now_utc or datetime.now(timezone.utc)
    cutoff_30d = now - timedelta(days=30)

    token = (api_key if api_key is not None else os.environ.get("LEMON_SQUEEZY_API_KEY", "")).strip()
    store = (store_id if store_id is not None else os.environ.get("LEMON_SQUEEZY_STORE_ID", "")).strip()

    if not token or not store:
        print("[INFO] LEMON_SQUEEZY_API_KEY o LEMON_SQUEEZY_STORE_ID no configuradas; fuente marcada como unavailable.")
        return False, LemonSqueezySummary(
            status="unavailable",
            note="Faltan credenciales LEMON_SQUEEZY_API_KEY / LEMON_SQUEEZY_STORE_ID (degradación elegante coste 0 €).",
        )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.api+json",
    }

    try:
        orders_raw = _fetch_ls_paginated("orders", headers, store, timeout=timeout)
        products_raw = _fetch_ls_paginated("products", headers, store, timeout=timeout)
        checkouts_raw: List[Dict[str, Any]] = []
        try:
            checkouts_raw = _fetch_ls_paginated("checkouts", headers, store, timeout=timeout)
        except requests.HTTPError as exc:
            # Algunos planes/tokens pueden restringir /checkouts; degradar sin perder /orders
            print(f"[INFO] Lemon Squeezy /checkouts no accesible ({exc}); se omite tasa de abandono API.")

        active_products_count = sum(
            1
            for p in products_raw
            if isinstance(p, dict)
            and str((p.get("attributes") or {}).get("status") or "").lower() in {"published", "active"}
        )

        net_30d = 0.0
        net_total = 0.0
        orders_30d = 0
        orders_total = 0
        refunded_30d = 0

        prod_acc: Dict[str, Dict[str, Any]] = {}
        country_acc: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"orders_30d": 0, "net_revenue_eur_30d": 0.0})
        monthly_acc: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"orders": 0, "net_revenue_eur": 0.0})
        lang_acc: Dict[str, Dict[str, Any]] = {
            "es": {"orders_30d": 0, "net_revenue_eur_30d": 0.0},
            "en": {"orders_30d": 0, "net_revenue_eur_30d": 0.0},
            "other": {"orders_30d": 0, "net_revenue_eur_30d": 0.0},
        }

        for order in orders_raw:
            if not isinstance(order, dict):
                continue
            attrs = order.get("attributes") or {}
            if bool(attrs.get("test_mode")):
                continue

            status = str(attrs.get("status") or "").lower()
            is_refunded = bool(attrs.get("refunded")) or status == "refunded"
            created_dt = _parse_iso_dt(attrs.get("created_at"))
            in_30d = bool(created_dt and created_dt >= cutoff_30d)

            if is_refunded:
                if in_30d:
                    refunded_30d += 1
                continue

            if status not in {"paid", "completed", ""}:
                continue

            net_eur = _extract_net_eur(attrs)
            first_item = attrs.get("first_order_item") or {}
            product_id = str(first_item.get("product_id") or "unknown")
            product_name = str(first_item.get("product_name") or "Datalaria Product").strip()
            country = _extract_country_iso(attrs)
            lang_key = _infer_order_lang(country, product_name)

            orders_total += 1
            net_total = round(net_total + net_eur, 2)

            p_entry = prod_acc.setdefault(
                product_id,
                {
                    "product_id": product_id,
                    "product_name": product_name,
                    "orders_30d": 0,
                    "orders_total": 0,
                    "net_revenue_eur_30d": 0.0,
                    "net_revenue_eur_total": 0.0,
                },
            )
            p_entry["orders_total"] += 1
            p_entry["net_revenue_eur_total"] = round(p_entry["net_revenue_eur_total"] + net_eur, 2)

            if created_dt:
                ym = created_dt.strftime("%Y-%m")
                monthly_acc[ym]["orders"] += 1
                monthly_acc[ym]["net_revenue_eur"] = round(monthly_acc[ym]["net_revenue_eur"] + net_eur, 2)

            if in_30d:
                orders_30d += 1
                net_30d = round(net_30d + net_eur, 2)
                p_entry["orders_30d"] += 1
                p_entry["net_revenue_eur_30d"] = round(p_entry["net_revenue_eur_30d"] + net_eur, 2)
                country_acc[country]["orders_30d"] += 1
                country_acc[country]["net_revenue_eur_30d"] = round(
                    country_acc[country]["net_revenue_eur_30d"] + net_eur, 2
                )
                lang_acc[lang_key]["orders_30d"] += 1
                lang_acc[lang_key]["net_revenue_eur_30d"] = round(
                    lang_acc[lang_key]["net_revenue_eur_30d"] + net_eur, 2
                )

        checkouts_created_30d = 0
        checkouts_completed_30d = 0
        for chk in checkouts_raw:
            if not isinstance(chk, dict):
                continue
            c_attrs = chk.get("attributes") or {}
            if bool(c_attrs.get("test_mode")):
                continue
            c_dt = _parse_iso_dt(c_attrs.get("created_at"))
            if c_dt and c_dt >= cutoff_30d:
                checkouts_created_30d += 1
                if c_attrs.get("completed") or c_attrs.get("order_id"):
                    checkouts_completed_30d += 1

        # Si /checkouts no refleja checkouts hospedados estándar, estimar solo si created > 0
        if checkouts_created_30d > 0:
            completed_effective = max(checkouts_completed_30d, min(orders_30d, checkouts_created_30d))
            abandonment_pct = round(
                max(0.0, min(100.0, ((checkouts_created_30d - completed_effective) / checkouts_created_30d) * 100.0)),
                1,
            )
            checkouts_completed_30d = completed_effective
        else:
            abandonment_pct = 0.0

        aov = round(net_30d / orders_30d, 2) if orders_30d > 0 else (round(net_total / orders_total, 2) if orders_total > 0 else 0.0)

        by_product = [
            RevenueProductBreakdown(
                **row,
                avg_order_value_eur=round(row["net_revenue_eur_total"] / row["orders_total"], 2)
                if row["orders_total"] > 0
                else 0.0,
            )
            for row in sorted(
                prod_acc.values(),
                key=lambda x: (x["net_revenue_eur_30d"], x["net_revenue_eur_total"]),
                reverse=True,
            )
        ]

        by_country = [
            RevenueCountryBreakdown(country=c, **vals)
            for c, vals in sorted(
                country_acc.items(),
                key=lambda item: item[1]["net_revenue_eur_30d"],
                reverse=True,
            )[:15]
        ]

        monthly_trend = [
            RevenueMonthlyPoint(month=m, **vals)
            for m, vals in sorted(monthly_acc.items())[-12:]
        ]

        summary = LemonSqueezySummary(
            status="ok",
            last_synced_at=now.isoformat(),
            currency="EUR",
            net_revenue_eur_30d=net_30d,
            net_revenue_eur_total=net_total,
            orders_30d=orders_30d,
            orders_total=orders_total,
            refunded_orders_30d=refunded_30d,
            avg_order_value_eur=aov,
            active_products_count=active_products_count,
            checkouts_created_30d=checkouts_created_30d,
            checkouts_completed_30d=checkouts_completed_30d,
            checkout_abandonment_pct=abandonment_pct,
            language_breakdown={k: RevenueLanguageSlice(**v) for k, v in lang_acc.items()},
            by_product=by_product,
            by_country=by_country,
            monthly_trend=monthly_trend,
            note="Agregados Lemon Squeezy API v1 sin PII (INV-PULSE-13).",
        )
        return True, summary
    except Exception as exc:
        print(f"[WARN] Error consultando Lemon Squeezy API: {exc}")
        return False, LemonSqueezySummary(
            status="error",
            last_synced_at=now.isoformat(),
            note=f"Error de conexión/API Lemon Squeezy: {exc}",
        )


def _classify_brevo_list_lang(list_id: int, name: str) -> Literal["es", "en", "all"]:
    low = name.lower()
    if list_id in {3, 5} or " es" in low or "(es)" in low or "español" in low or low.endswith("_es"):
        return "es"
    if list_id in {4, 6} or " en" in low or "(en)" in low or "english" in low or low.endswith("_en"):
        return "en"
    return "all"


def fetch_brevo_audience_summary(
    api_key: Optional[str] = None,
    now_utc: Optional[datetime] = None,
    timeout: int = 12,
) -> Tuple[bool, BrevoAudienceSummary]:
    """
    Extrae conteos agregados de listas y campañas desde Brevo API v3 (cero PII).
    """
    now = now_utc or datetime.now(timezone.utc)
    token = (api_key if api_key is not None else os.environ.get("BREVO_API_KEY", "")).strip()

    if not token:
        print("[INFO] BREVO_API_KEY no configurada; fuente marcada como unavailable.")
        return False, BrevoAudienceSummary(
            status="unavailable",
            note="Falta credencial BREVO_API_KEY (degradación elegante coste 0 €).",
        )

    headers = {
        "api-key": token,
        "Accept": "application/json",
    }

    try:
        lists_resp = requests.get(
            f"{BREVO_API_BASE}/contacts/lists?limit=50&offset=0",
            headers=headers,
            timeout=timeout,
        )
        lists_resp.raise_for_status()
        lists_payload = lists_resp.json()
        raw_lists = lists_payload.get("lists") or []

        parsed_lists: List[BrevoListSummary] = []
        total_subs = 0
        es_subs = 0
        en_subs = 0
        helix_subs = 0

        for item in raw_lists:
            if not isinstance(item, dict):
                continue
            lid = int(item.get("id") or 0)
            name = str(item.get("name") or f"List {lid}").strip()
            tot = max(0, int(item.get("totalSubscribers") or 0))
            uniq = max(0, int(item.get("uniqueSubscribers") or tot))
            lang_hint = _classify_brevo_list_lang(lid, name)

            parsed_lists.append(
                BrevoListSummary(
                    list_id=lid,
                    name=name,
                    lang_hint=lang_hint,
                    total_subscribers=tot,
                    unique_subscribers=uniq,
                )
            )
            total_subs += uniq
            if lang_hint == "es":
                es_subs += uniq
            elif lang_hint == "en":
                en_subs += uniq
            if lid in {5, 6} or "helix" in name.lower() or "waitlist" in name.lower():
                helix_subs += uniq

        campaigns_resp = requests.get(
            f"{BREVO_API_BASE}/emailCampaigns?status=sent&limit=20&offset=0",
            headers=headers,
            timeout=timeout,
        )
        campaigns_resp.raise_for_status()
        campaigns_payload = campaigns_resp.json()
        raw_campaigns = campaigns_payload.get("campaigns") or []

        parsed_campaigns: List[BrevoCampaignSummary] = []
        sum_delivered = 0
        sum_opens = 0
        sum_clicks = 0
        sum_unsubs = 0

        for camp in raw_campaigns:
            if not isinstance(camp, dict):
                continue
            cid = int(camp.get("id") or 0)
            cname = str(camp.get("name") or f"Campaign {cid}").strip()
            sent_date = camp.get("sentDate")
            gstats = ((camp.get("statistics") or {}).get("globalStats") or {})
            delivered = max(0, int(gstats.get("delivered") or gstats.get("sent") or 0))
            u_opens = max(0, int(gstats.get("uniqueViews") or gstats.get("viewed") or 0))
            u_clicks = max(0, int(gstats.get("uniqueClicks") or gstats.get("clickers") or 0))
            unsubs = max(0, int(gstats.get("unsubscriptions") or 0))

            open_pct = round((u_opens / delivered) * 100.0, 2) if delivered > 0 else 0.0
            ctr_pct = round((u_clicks / delivered) * 100.0, 2) if delivered > 0 else 0.0
            open_pct = min(100.0, open_pct)
            ctr_pct = min(100.0, ctr_pct)

            sum_delivered += delivered
            sum_opens += u_opens
            sum_clicks += u_clicks
            sum_unsubs += unsubs

            parsed_campaigns.append(
                BrevoCampaignSummary(
                    campaign_id=cid,
                    name=cname,
                    sent_date=str(sent_date) if sent_date else None,
                    delivered=delivered,
                    unique_opens=u_opens,
                    open_rate_pct=open_pct,
                    unique_clicks=u_clicks,
                    ctr_pct=ctr_pct,
                    unsubscribes=unsubs,
                )
            )

        avg_open = round(min(100.0, (sum_opens / sum_delivered) * 100.0), 2) if sum_delivered > 0 else 0.0
        avg_ctr = round(min(100.0, (sum_clicks / sum_delivered) * 100.0), 2) if sum_delivered > 0 else 0.0

        summary = BrevoAudienceSummary(
            status="ok",
            last_synced_at=now.isoformat(),
            total_lists=len(parsed_lists),
            total_subscribers=total_subs,
            es_subscribers=es_subs,
            en_subscribers=en_subs,
            waitlist_helix_subscribers=helix_subs,
            campaigns_analyzed=len(parsed_campaigns),
            avg_open_rate_pct=avg_open,
            avg_ctr_pct=avg_ctr,
            total_unsubscribes=sum_unsubs,
            lists=parsed_lists,
            recent_campaigns=parsed_campaigns[:10],
            note="Agregados Brevo API v3 sin PII (INV-PULSE-13).",
        )
        return True, summary
    except Exception as exc:
        print(f"[WARN] Error consultando Brevo API: {exc}")
        return False, BrevoAudienceSummary(
            status="error",
            last_synced_at=now.isoformat(),
            note=f"Error de conexión/API Brevo: {exc}",
        )


def consolidate_revenue_report(
    *,
    ls_ok: bool,
    ls_summary: LemonSqueezySummary,
    brevo_ok: bool,
    brevo_summary: BrevoAudienceSummary,
    existing_report: Optional[Dict[str, Any]] = None,
    now_utc: Optional[datetime] = None,
) -> RevenueMetricsReport:
    """
    Combina fuentes financieras y de audiencia aplicando degradación independiente (INV-PULSE-11).
    Si una fuente falla y existe snapshot previo válido, preserva el snapshot previo con nota.
    """
    now = now_utc or datetime.now(timezone.utc)
    prev = existing_report if isinstance(existing_report, dict) else {}

    final_ls = ls_summary
    if not ls_ok and isinstance(prev.get("lemon_squeezy"), dict) and prev["lemon_squeezy"].get("status") == "ok":
        preserved = dict(prev["lemon_squeezy"])
        preserved["status"] = ls_summary.status
        preserved["note"] = f"{ls_summary.note} (Preservando último snapshot válido)."
        final_ls = LemonSqueezySummary(**preserved)

    final_brevo = brevo_summary
    if not brevo_ok and isinstance(prev.get("brevo"), dict) and prev["brevo"].get("status") == "ok":
        preserved = dict(prev["brevo"])
        preserved["status"] = brevo_summary.status
        preserved["note"] = f"{brevo_summary.note} (Preservando último snapshot válido)."
        final_brevo = BrevoAudienceSummary(**preserved)

    return RevenueMetricsReport(
        version="1.0.0",
        visibility="private",
        pii_stripped=True,
        generated_at=now,
        lemon_squeezy=final_ls,
        brevo=final_brevo,
    )


def build_executive_state(
    revenue_report: RevenueMetricsReport,
    *,
    index_path: Path = INDEX_PATH,
    impact_report_path: Path = IMPACT_REPORT_PATH,
    channel_metrics_path: Path = CHANNEL_METRICS_PATH,
    social_metrics_path: Path = SOCIAL_METRICS_PATH,
    now_utc: Optional[datetime] = None,
) -> ExecutiveStateSnapshot:
    """
    Genera el bus ejecutivo unificado `executive_state.json` cruzando
    GA4/GSC + Social + Brevo + Lemon Squeezy + alertas de releases silenciosas.
    """
    now = now_utc or datetime.now(timezone.utc)
    impact = _safe_read_json(impact_report_path) or {}
    index_assets = _safe_read_json(index_path) or []
    channel_data = _safe_read_json(channel_metrics_path) or {}
    social_data = _safe_read_json(social_metrics_path) or {}

    ls = revenue_report.lemon_squeezy
    brevo = revenue_report.brevo

    target_eur = 500.0
    progress_pct = round(min(100.0, (ls.net_revenue_eur_30d / target_eur) * 100.0), 1)
    if ls.net_revenue_eur_30d >= 2500.0:
        stage_label = "Estadio 3 (> 2.500 €/mes)"
    elif ls.net_revenue_eur_30d >= 500.0:
        stage_label = "Estadio 2 (500 -> 2.500 €/mes)"
    else:
        stage_label = "Estadio 1 (0 -> 500 €/mes)"

    total_assets = len(index_assets) if isinstance(index_assets, list) else 0
    silent_releases = int(impact.get("silent_releases_count", 0) or 0)
    quick_wins = len(impact.get("quick_wins_ctr") or [])
    orphans = len(impact.get("monetization_orphans") or [])

    channel_rows = channel_data.get("channel_summary") if isinstance(channel_data, dict) else []
    total_key_events = 0
    if isinstance(channel_rows, list):
        total_key_events = sum(int(r.get("key_events_30d", 0) or 0) for r in channel_rows if isinstance(r, dict))

    platforms = social_data.get("platforms") if isinstance(social_data, dict) else {}
    li_followers = int(((platforms or {}).get("linkedin_company") or {}).get("followers_count", 0) or 0)

    priorities: List[str] = []
    if ls.status != "ok":
        priorities.append("Configurar LEMON_SQUEEZY_API_KEY y LEMON_SQUEEZY_STORE_ID en GitHub Secrets para medir ventas reales en €.")
    if brevo.status != "ok":
        priorities.append("Configurar BREVO_API_KEY en GitHub Secrets para sincronizar suscriptores y open rate.")
    if silent_releases > 0:
        priorities.append(f"Activar relevo Scriba/Mercator sobre {silent_releases} alertas de releases silenciosas (INV-OS-3).")
    if quick_wins > 0:
        priorities.append(f"Capturar CTR orgánico en {quick_wins} Quick Wins GSC (CTR actual {impact.get('avg_gsc_ctr_pct', 0)}% -> meta >= 2.0%).")
    if li_followers == 0:
        priorities.append("Ejecutar plan de activación LinkedIn Página de Empresa (M04) partiendo de 0 seguidores reportados.")
    if not priorities:
        priorities.append("Escalar lanzamientos EN-first (72.3% demanda GSC) y optimizar AOV hacia Suites/Mega Bundle.")

    return ExecutiveStateSnapshot(
        version="1.0.0",
        visibility="private",
        pii_stripped=True,
        generated_at=now,
        north_star_target_eur_month=target_eur,
        stage_label=stage_label,
        stage_progress_pct=progress_pct,
        revenue={
            "lemon_squeezy_status": ls.status,
            "net_revenue_eur_30d": ls.net_revenue_eur_30d,
            "net_revenue_eur_total": ls.net_revenue_eur_total,
            "orders_30d": ls.orders_30d,
            "orders_total": ls.orders_total,
            "avg_order_value_eur": ls.avg_order_value_eur,
            "checkout_abandonment_pct": ls.checkout_abandonment_pct,
        },
        audience={
            "brevo_status": brevo.status,
            "total_subscribers": brevo.total_subscribers,
            "es_subscribers": brevo.es_subscribers,
            "en_subscribers": brevo.en_subscribers,
            "waitlist_helix_subscribers": brevo.waitlist_helix_subscribers,
            "avg_open_rate_pct": brevo.avg_open_rate_pct,
            "avg_ctr_pct": brevo.avg_ctr_pct,
        },
        traffic_seo={
            "post_views_30d": int(impact.get("total_30d_post_views", 0) or 0),
            "gsc_impressions_30d": int(impact.get("total_30d_gsc_impressions", 0) or 0),
            "gsc_clicks_30d": int(impact.get("total_30d_gsc_clicks", 0) or 0),
            "avg_gsc_ctr_pct": float(impact.get("avg_gsc_ctr_pct", 0.0) or 0.0),
            "en_gsc_impressions_share_pct": float(impact.get("en_gsc_impressions_share_pct", 0.0) or 0.0),
            "ga4_key_events_30d": total_key_events,
        },
        social={
            "linkedin_company_followers": li_followers,
            "devto_status": ((platforms or {}).get("devto") or {}).get("status", "unavailable"),
            "coderlegion_status": ((platforms or {}).get("coderlegion") or {}).get("status", "unavailable"),
            "x_status": "standby_zero_cost",
        },
        catalog_health={
            "total_assets": total_assets,
            "published_posts": int(impact.get("total_published_posts", 0) or 0),
            "quick_wins_ctr": quick_wins,
            "monetization_orphans": orphans,
            "silent_releases_count": silent_releases,
        },
        top_priorities=priorities[:5],
    )


def render_revenue_report_markdown(
    report: RevenueMetricsReport,
    exec_state: ExecutiveStateSnapshot,
) -> str:
    """Genera el reporte ejecutivo local en Markdown (gitignored bajo INV-PULSE-13)."""
    ls = report.lemon_squeezy
    br = report.brevo
    lines = [
        "# 💰 REVENUE_REPORT — Telemetría Privada Datalaria (`INV-PULSE-13`)",
        "",
        f"> **Generado:** {report.generated_at.isoformat()} · **Estadio:** `{exec_state.stage_label}` ({exec_state.stage_progress_pct:.1f}% de {exec_state.north_star_target_eur_month:.0f} €/mes) · **PII Stripped:** `{report.pii_stripped}`",
        "",
        "## 1. Lemon Squeezy (Ingresos Netos Agregados)",
        f"- **Estado Conector:** `{ls.status}` ({ls.note})",
        f"- **Ingresos Netos 30d:** `{ls.net_revenue_eur_30d:.2f} €` · **Histórico:** `{ls.net_revenue_eur_total:.2f} €`",
        f"- **Pedidos 30d / Total:** `{ls.orders_30d}` / `{ls.orders_total}` · **AOV:** `{ls.avg_order_value_eur:.2f} €` · **Abandono Checkout:** `{ls.checkout_abandonment_pct:.1f}%`",
        "",
        "## 2. Brevo (Audiencia & Retención)",
        f"- **Estado Conector:** `{br.status}` ({br.note})",
        f"- **Suscriptores Totales:** `{br.total_subscribers}` (`ES`: {br.es_subscribers} · `EN`: {br.en_subscribers} · `Waitlist Helix`: {br.waitlist_helix_subscribers})",
        f"- **Open Rate Medio:** `{br.avg_open_rate_pct:.2f}%` · **CTR Medio:** `{br.avg_ctr_pct:.2f}%` · **Bajas:** `{br.total_unsubscribes}`",
        "",
        "## 3. Prioridades Ejecutivas (`00-chief-orchestrator` / `M01`)",
    ]
    for idx, prio in enumerate(exec_state.top_priorities, start=1):
        lines.append(f"{idx}. {prio}")
    lines.append("")
    return "\n".join(lines)


def assert_no_pii_in_payload(obj: Any, path_prefix: str = "") -> None:
    """Guardia determinista anti-PII antes de persistir o subir a Supabase."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            kl = str(k).lower()
            if kl in FORBIDDEN_PII_KEYS:
                raise ValueError(f"Violación INV-PULSE-13: clave PII prohibida '{path_prefix}{k}' detectada.")
            assert_no_pii_in_payload(v, f"{path_prefix}{k}.")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            assert_no_pii_in_payload(item, f"{path_prefix}[{i}].")


def sync_all_revenue(
    *,
    dry_run: bool = False,
    strict: bool = False,
    output_path: Path = REVENUE_METRICS_PATH,
    executive_state_path: Path = EXECUTIVE_STATE_PATH,
    report_path: Path = REVENUE_REPORT_PATH,
    index_path: Path = INDEX_PATH,
    impact_report_path: Path = IMPACT_REPORT_PATH,
    channel_metrics_path: Path = CHANNEL_METRICS_PATH,
    social_metrics_path: Path = SOCIAL_METRICS_PATH,
) -> Tuple[RevenueMetricsReport, ExecutiveStateSnapshot]:
    """Orquesta la ingesta privada de ingresos (Lemon Squeezy + Brevo) y el estado ejecutivo."""
    _load_local_env_if_needed()

    existing = _safe_read_json(output_path)
    ls_ok, ls_summary = fetch_lemon_squeezy_summary()
    brevo_ok, brevo_summary = fetch_brevo_audience_summary()

    if strict and (not ls_ok or not brevo_ok):
        raise RuntimeError(
            f"Modo --strict activo y alguna fuente falló o está unavailable: "
            f"lemon_squeezy={ls_summary.status}, brevo={brevo_summary.status}"
        )

    report = consolidate_revenue_report(
        ls_ok=ls_ok,
        ls_summary=ls_summary,
        brevo_ok=brevo_ok,
        brevo_summary=brevo_summary,
        existing_report=existing,
    )
    exec_state = build_executive_state(
        report,
        index_path=index_path,
        impact_report_path=impact_report_path,
        channel_metrics_path=channel_metrics_path,
        social_metrics_path=social_metrics_path,
    )

    report_dict = report.model_dump(mode="json")
    exec_dict = exec_state.model_dump(mode="json")
    assert_no_pii_in_payload(report_dict)
    assert_no_pii_in_payload(exec_dict)

    if dry_run:
        print(
            f"[DRY-RUN] sync_revenue completado sin escribir en disco · "
            f"Lemon Squeezy: status={report.lemon_squeezy.status} ({report.lemon_squeezy.net_revenue_eur_30d:.2f} €/30d, {report.lemon_squeezy.orders_30d} pedidos) · "
            f"Brevo: status={report.brevo.status} ({report.brevo.total_subscribers} subs, Open {report.brevo.avg_open_rate_pct:.1f}%) · "
            f"Estadio: {exec_state.stage_label} ({exec_state.stage_progress_pct:.1f}%)."
        )
        return report, exec_state

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report_dict, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    executive_state_path.write_text(json.dumps(exec_dict, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(render_revenue_report_markdown(report, exec_state), encoding="utf-8")
    print(f"[SYNC-REVENUE] Agregados sin PII guardados localmente (gitignored): {output_path.name}, {executive_state_path.name}, {report_path.name}.")
    return report, exec_state


def main(argv: Optional[List[str]] = None) -> int:
    _configure_utf8_stdio()
    parser = argparse.ArgumentParser(
        description="Extractor privado de ingresos Lemon Squeezy + Brevo sin PII (Hito 9.2 / INV-PULSE-13)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Ejecuta la consulta y consolidación sin escribir ficheros locales en disco.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Falla con código de salida != 0 si Lemon Squeezy o Brevo no están disponibles.",
    )
    args = parser.parse_args(argv)

    try:
        sync_all_revenue(dry_run=args.dry_run, strict=args.strict)
        return 0
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
