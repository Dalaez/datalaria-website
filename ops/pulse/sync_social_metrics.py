"""
ops/pulse/sync_social_metrics.py
--------------------------------
Módulo de Ingesta Nativa Gratuita de Comunidades Tech (Dev.to + CoderLegion) y Gestión del Distribution Ledger.
Especificación técnica formal: SPEC-APP-PULSE v1.5.0 (specs/apps/pulse/spec.md) - Hito 7.12 / ADR-024 / ADR-033.

Responsabilidades:
1. Consultar gratuitamente los artículos publicados en Dev.to (`GET /api/articles/me/published?per_page=1000`
   con header `api-key: DEVTO_API_KEY`) extrayendo vistas, reacciones, comentarios, tiempo de lectura y `canonical_url`.
2. Consultar gratuitamente los artículos publicados en CoderLegion (`GET /api/v1/posts/{id}` con header
   obligatorio `X-API-Key: CODERLEGION_API_KEY`, nunca `Bearer` — ADR-024) a partir de `distribution_ledger.json`,
   con soporte opcional `--backfill-coderlegion` acotado por página.
3. Cruzar cada artículo externo con su `ContentAsset` canónico de Datalaria (`index.json`) por `canonical_url` / `source_url`
   y enriquecer de forma idempotente `data/pulse/private/distribution_ledger.json`.
4. Persistir exclusivamente en `data/pulse/private/social_metrics.json` con degradación elegante independiente por plataforma
   (`INV-PULSE-11`, `INV-PULSE-12`) y mantener X/Twitter nativo en `standby_zero_cost` (`0 €`).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

import requests

from autopilot.src.orchestrator import record_distribution_ledger_entry
from ops.pulse.sync_metrics import detect_url_lang, normalize_url_path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
INDEX_PATH = ROOT_DIR / "data" / "pulse" / "private" / "index.json"
LEDGER_PATH = ROOT_DIR / "data" / "pulse" / "private" / "distribution_ledger.json"
SOCIAL_METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "social_metrics.json"
IMPORTS_LINKEDIN_DIR = ROOT_DIR / "data" / "pulse" / "private" / "imports" / "linkedin"

DEVTO_PUBLISHED_URL = "https://dev.to/api/articles/me/published"
DEFAULT_CODERLEGION_URL = "https://coderlegion.com/api/v1/posts"
LINKEDIN_SHARE_STATS_URL = "https://api.linkedin.com/v2/organizationalEntityShareStatistics"
LINKEDIN_FOLLOWER_STATS_URL = "https://api.linkedin.com/v2/followerStatistics"
LINKEDIN_NETWORK_SIZES_URL = "https://api.linkedin.com/v2/networkSizes"
LINKEDIN_OAUTH_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"



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
    """Carga variables desde .env o autopilot/.env solo fuera de ejecuciones de pytest."""
    if "PYTEST_CURRENT_TEST" in os.environ:
        return
    try:
        from dotenv import load_dotenv

        for candidate in (ROOT_DIR / ".env", ROOT_DIR / "autopilot" / ".env"):
            if candidate.is_file():
                load_dotenv(candidate, override=False)
    except Exception:
        pass


def _coerce_count(val: Any) -> int:
    """Convierte un contador de API (int, str numérico o lista de objetos) a entero >= 0."""
    if val is None:
        return 0
    if isinstance(val, list):
        return len(val)
    if isinstance(val, (int, float)):
        return max(0, int(val))
    try:
        return max(0, int(str(val).strip()))
    except Exception:
        return 0


def build_asset_url_lookup(assets: List[Dict[str, Any]]) -> Dict[str, Tuple[str, str, Literal["es", "en"]]]:
    """
    Construye un mapa `{ path_normalizado: (asset_id, slug, lang) }` y `{ slug: (asset_id, slug) }`
    para cruzar `canonical_url` / `source_url` con los activos de Datalaria Pulse.
    """
    by_path: Dict[str, Tuple[str, str, Literal["es", "en"]]] = {}
    for asset in assets:
        if not isinstance(asset, dict):
            continue
        aid = str(asset.get("id") or "").strip()
        slug = str(asset.get("slug") or aid).strip()
        if not aid:
            continue
        norm_es = normalize_url_path(asset.get("url_es"))
        norm_en = normalize_url_path(asset.get("url_en"))
        if norm_es:
            by_path[norm_es] = (aid, slug, "es")
        if norm_en:
            by_path[norm_en] = (aid, slug, "en")
    return by_path


def match_canonical_to_asset(
    canonical_url: Optional[str],
    assets: List[Dict[str, Any]],
    lookup: Optional[Dict[str, Tuple[str, str, Literal["es", "en"]]]] = None,
) -> Tuple[Optional[str], str, Literal["es", "en", "other"]]:
    """
    Cruza una `canonical_url` con el catálogo de `index.json`.
    Devuelve `(asset_id | None, slug, lang)`.
    """
    raw = str(canonical_url or "").strip()
    norm_path = normalize_url_path(raw)
    if not norm_path:
        return None, "", "other"

    path_map = lookup if lookup is not None else build_asset_url_lookup(assets)
    if norm_path in path_map:
        aid, slug, lang = path_map[norm_path]
        return aid, slug, lang

    lang_detected = detect_url_lang(norm_path)
    parts = [p for p in norm_path.strip("/").split("/") if p]
    extracted_slug = parts[-1] if parts else ""

    for asset in assets:
        if not isinstance(asset, dict):
            continue
        aid = str(asset.get("id") or "").strip()
        aslug = str(asset.get("slug") or "").strip()
        if extracted_slug and (extracted_slug == aid or extracted_slug == aslug):
            eff_lang: Literal["es", "en", "other"] = lang_detected if lang_detected in ("es", "en") else "en"
            return aid, aslug or aid, eff_lang

    return None, extracted_slug, lang_detected


def load_distribution_ledger(ledger_path: Path = LEDGER_PATH) -> Dict[str, Any]:
    """Lee `distribution_ledger.json` o devuelve una estructura vacía válida."""
    if ledger_path.is_file():
        try:
            with open(ledger_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict) and isinstance(data.get("entries"), list):
                return data
        except Exception:
            pass
    return {
        "version": "1.0.0",
        "visibility": "private",
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "entries": [],
    }


def fetch_devto_published_articles(
    api_key: Optional[str] = None,
    per_page: int = 1000,
    timeout: int = 15,
) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Consulta `GET https://dev.to/api/articles/me/published?per_page=1000` (Forem API gratuita).
    Devuelve `(devto_ok, normalized_articles)`.
    """
    token = (api_key if api_key is not None else os.environ.get("DEVTO_API_KEY", "")).strip()
    if not token:
        print("[WARN] DEVTO_API_KEY no configurada. Saltando sincronización activa de Dev.to.")
        return False, []

    headers = {
        "api-key": token,
        "accept": "application/vnd.forem.api-v1+json",
        "User-Agent": "DatalariaPulse/1.5",
    }
    try:
        response = requests.get(
            DEVTO_PUBLISHED_URL,
            headers=headers,
            params={"page": 1, "per_page": min(max(1, per_page), 1000)},
            timeout=timeout,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list):
            print("[WARN] Respuesta inesperada de Dev.to API (no es una lista JSON).")
            return False, []

        articles: List[Dict[str, Any]] = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            ext_id = str(item.get("id") or "").strip()
            if not ext_id:
                continue
            pos_react = _coerce_count(item.get("positive_reactions_count"))
            pub_react = _coerce_count(item.get("public_reactions_count"))
            articles.append({
                "external_id": ext_id,
                "title": str(item.get("title") or "").strip(),
                "slug": str(item.get("slug") or "").strip(),
                "url": str(item.get("url") or "").strip(),
                "canonical_url": str(item.get("canonical_url") or "").strip(),
                "views": _coerce_count(item.get("page_views_count")),
                "reactions": max(pos_react, pub_react),
                "positive_reactions": pos_react,
                "public_reactions": pub_react,
                "comments": _coerce_count(item.get("comments_count")),
                "reading_time_min": _coerce_count(item.get("reading_time_minutes")),
                "published_at": str(item.get("published_at") or item.get("published_timestamp") or "").strip() or None,
            })

        print(f"[DEVTO] Extraídos {len(articles)} artículos publicados desde Dev.to API.")
        return True, articles

    except requests.exceptions.HTTPError as exc:
        code = exc.response.status_code if exc.response is not None else "?"
        print(f"[WARN] Error HTTP en Dev.to API ({code}): {exc}")
        return False, []
    except Exception as exc:
        print(f"[WARN] Error consultando Dev.to API: {exc}")
        return False, []


def _normalize_coderlegion_post_object(raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Normaliza un objeto de post devuelto por CoderLegion API v1."""
    obj = raw.get("data") if isinstance(raw.get("data"), dict) else raw
    if not isinstance(obj, dict):
        return None
    ext_id = str(obj.get("id") or obj.get("post_id") or "").strip()
    if not ext_id:
        return None

    views = _coerce_count(
        obj.get("views")
        if obj.get("views") is not None
        else (obj.get("view_count") if obj.get("view_count") is not None else obj.get("page_views_count"))
    )
    reactions = _coerce_count(
        obj.get("reactions_count")
        if obj.get("reactions_count") is not None
        else (
            obj.get("likes_count")
            if obj.get("likes_count") is not None
            else (
                obj.get("reactions")
                if obj.get("reactions") is not None
                else (obj.get("likes") if obj.get("likes") is not None else obj.get("positive_reactions_count"))
            )
        )
    )
    comments = _coerce_count(
        obj.get("comments_count")
        if obj.get("comments_count") is not None
        else (obj.get("comment_count") if obj.get("comment_count") is not None else obj.get("comments"))
    )
    canonical = str(
        obj.get("source_url")
        or obj.get("canonical_url")
        or obj.get("original_url")
        or ""
    ).strip()
    url = str(obj.get("url") or obj.get("permalink") or f"https://coderlegion.com/posts/{ext_id}").strip()
    pub_at = str(obj.get("published_at") or obj.get("created_at") or obj.get("created") or "").strip() or None

    return {
        "external_id": ext_id,
        "title": str(obj.get("title") or "").strip(),
        "slug": str(obj.get("slug") or "").strip(),
        "url": url,
        "canonical_url": canonical,
        "views": views,
        "reactions": reactions,
        "comments": comments,
        "reading_time_min": _coerce_count(obj.get("reading_time_minutes") or obj.get("reading_time")),
        "published_at": pub_at,
    }


def fetch_coderlegion_posts(
    api_key: Optional[str] = None,
    ledger_entries: Optional[List[Dict[str, Any]]] = None,
    api_base_url: Optional[str] = None,
    backfill_pages: int = 0,
    timeout: int = 15,
) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Consulta gratuitamente CoderLegion API v1 usando header obligatorio `X-API-Key` (`ADR-024`).
    1) Opcionalmente explora `backfill_pages` páginas de `GET /api/v1/posts?page=N` buscando `source_url` de Datalaria.
    2) Consulta `GET /api/v1/posts/{id}` para cada `external_id` de CoderLegion registrado en `distribution_ledger.json`.
    Devuelve `(coderlegion_ok, normalized_posts)`.
    """
    token = (api_key if api_key is not None else os.environ.get("CODERLEGION_API_KEY", "")).strip()
    if not token:
        print("[WARN] CODERLEGION_API_KEY no configurada. Saltando sincronización activa de CoderLegion.")
        return False, []

    base_url = (
        api_base_url
        or os.environ.get("CODERLEGION_API_URL", DEFAULT_CODERLEGION_URL)
    ).rstrip("/")
    headers = {
        "X-API-Key": token,
        "Accept": "application/json",
        "User-Agent": "DatalariaPulse/1.5",
    }

    cl_ledger = [
        e
        for e in (ledger_entries or [])
        if isinstance(e, dict)
        and e.get("channel") == "coderlegion"
        and str(e.get("external_id") or "").strip()
    ]

    discovered_by_id: Dict[str, Dict[str, Any]] = {}
    any_http_success = False
    had_http_error = False

    # 1. Backfill opcional acotado por página
    if backfill_pages > 0:
        for page_no in range(1, backfill_pages + 1):
            try:
                resp = requests.get(
                    base_url,
                    headers=headers,
                    params={"page": page_no},
                    timeout=timeout,
                )
                resp.raise_for_status()
                any_http_success = True
                payload = resp.json()
                raw_list: List[Any] = []
                if isinstance(payload, list):
                    raw_list = payload
                elif isinstance(payload, dict):
                    for key in ("data", "posts", "items", "results"):
                        if isinstance(payload.get(key), list):
                            raw_list = payload[key]
                            break
                if not raw_list:
                    break
                for raw_item in raw_list:
                    if not isinstance(raw_item, dict):
                        continue
                    norm = _normalize_coderlegion_post_object(raw_item)
                    if not norm:
                        continue
                    if "datalaria.com" in (norm.get("canonical_url") or "").lower():
                        discovered_by_id[norm["external_id"]] = norm
            except Exception as exc:
                had_http_error = True
                print(f"[WARN] Error en backfill CoderLegion (página {page_no}): {exc}")
                break

    # 2. Consulta individual por ID del Distribution Ledger (`GET /api/v1/posts/{id}`)
    for entry in cl_ledger:
        ext_id = str(entry["external_id"]).strip()
        if not ext_id:
            continue
        try:
            resp = requests.get(
                f"{base_url}/{ext_id}",
                headers=headers,
                timeout=timeout,
            )
            resp.raise_for_status()
            any_http_success = True
            payload = resp.json()
            if isinstance(payload, dict):
                norm = _normalize_coderlegion_post_object(payload)
                if norm:
                    if not norm.get("canonical_url") and entry.get("canonical_url"):
                        norm["canonical_url"] = str(entry["canonical_url"]).strip()
                    discovered_by_id[ext_id] = norm
        except Exception as exc:
            had_http_error = True
            print(f"[WARN] Error consultando CoderLegion post ID {ext_id}: {exc}")

    # Si no había entradas en el ledger ni backfill solicitado, pero la clave está presente y sin errores:
    if not cl_ledger and backfill_pages <= 0:
        print("[CODERLEGION] Ledger sin IDs de CoderLegion aún (0 peticiones enviadas).")
        return True, []

    if not any_http_success and had_http_error:
        return False, []

    posts = list(discovered_by_id.values())
    print(f"[CODERLEGION] Extraídos {len(posts)} posts desde CoderLegion API v1.")
    return True, posts


def _refresh_linkedin_token(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    refresh_token: Optional[str] = None,
) -> Optional[str]:
    """Renueva el token de acceso OAuth de LinkedIn usando refresh_token."""
    cid = (client_id if client_id is not None else os.environ.get("LINKEDIN_CLIENT_ID", "")).strip()
    csecret = (client_secret if client_secret is not None else os.environ.get("LINKEDIN_CLIENT_SECRET", "")).strip()
    rtoken = (refresh_token if refresh_token is not None else os.environ.get("LINKEDIN_REFRESH_TOKEN", "")).strip()
    if not (cid and csecret and rtoken):
        return None

    try:
        resp = requests.post(
            LINKEDIN_OAUTH_TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": rtoken,
                "client_id": cid,
                "client_secret": csecret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        new_token = data.get("access_token")
        new_refresh = data.get("refresh_token")
        if not new_token:
            return None

        # Guardar en .linkedin_new_tokens.json para CI / persistencia segura
        token_data: Dict[str, str] = {"access_token": str(new_token)}
        if new_refresh:
            token_data["refresh_token"] = str(new_refresh)
        tokens_file = ROOT_DIR / ".linkedin_new_tokens.json"
        try:
            with open(tokens_file, "w", encoding="utf-8") as fh:
                json.dump(token_data, fh)
        except Exception:
            pass

        return str(new_token)
    except Exception as exc:
        print(f"[WARN] Error al renovar token de LinkedIn: {exc}")
        return None


def fetch_linkedin_company_api_metrics(
    company_id: Optional[str] = None,
    access_token: Optional[str] = None,
    refresh_token: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    ledger_entries: Optional[List[Dict[str, Any]]] = None,
    timeout: int = 15,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Carril A — API Oficial Gratuita (Community Management API):
    Lee estadísticas agregadas y por publicación para la Página de Empresa (`urn:li:organization:{company_id}`).
    PROHIBIDO monitorizar perfiles personales y PROHIBIDO scraping/cookies li_at (Veto 10-security-privacy / INV-PULSE-12).
    Si devuelve HTTP 403 o 401 irresoluble (producto en revisión), degrada elegantemente con [INFO] limpio.
    """
    raw_comp = (company_id if company_id is not None else os.environ.get("LINKEDIN_COMPANY_ID", "")).strip()
    clean_comp = raw_comp.replace("urn:li:organization:", "").strip()
    if not clean_comp:
        print("[INFO] LINKEDIN_COMPANY_ID no configurada. Saltando Carril A (API LinkedIn).")
        return False, {}

    current_token = (access_token if access_token is not None else os.environ.get("LINKEDIN_ACCESS_TOKEN", "")).strip()
    if not current_token:
        print("[INFO] LINKEDIN_ACCESS_TOKEN no configurada. Saltando Carril A (API LinkedIn).")
        return False, {}

    org_urn = f"urn:li:organization:{clean_comp}"

    def _headers(tok: str) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {tok}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Accept": "application/json",
            "User-Agent": "DatalariaPulse/1.5",
        }

    # Intentar petición con auto-refresh en 401 (máx 2 intentos)
    resp_stats = None
    for attempt in range(2):
        try:
            resp_stats = requests.get(
                LINKEDIN_SHARE_STATS_URL,
                headers=_headers(current_token),
                params={"q": "organizationalEntity", "organizationalEntity": org_urn},
                timeout=timeout,
            )
            if resp_stats.status_code == 401 and attempt == 0:
                print("[INFO] LinkedIn Access Token expirado (HTTP 401). Intentando renovación...")
                refreshed = _refresh_linkedin_token(client_id, client_secret, refresh_token)
                if refreshed:
                    current_token = refreshed
                    continue
            break
        except Exception as exc:
            print(f"[WARN] Fallo de conexión consultando LinkedIn API: {exc}")
            return False, {}

    if resp_stats is None:
        return False, {}

    if resp_stats.status_code in (401, 403):
        print(
            f"[INFO] LinkedIn Community Management API devolvió HTTP {resp_stats.status_code} "
            f"(producto en revisión o permisos insuficientes). Conmutando a Carril B (.xlsx) o snapshot previo."
        )
        return False, {}

    if resp_stats.status_code != 200:
        print(f"[WARN] LinkedIn API devolvió HTTP {resp_stats.status_code}: {resp_stats.text[:200]}")
        return False, {}

    payload_stats = resp_stats.json()
    elements = payload_stats.get("elements", []) if isinstance(payload_stats, dict) else []

    total_impr = 0
    total_clicks = 0
    total_react = 0
    total_comm = 0
    total_shares = 0
    posts_by_urn: Dict[str, Dict[str, Any]] = {}

    for el in elements:
        if not isinstance(el, dict):
            continue
        st = el.get("totalShareStatistics") or {}
        impr = _coerce_count(st.get("impressionCount") or st.get("uniqueImpressionsCount"))
        clk = _coerce_count(st.get("clickCount"))
        rea = _coerce_count(st.get("likeCount"))
        com = _coerce_count(st.get("commentCount"))
        sh = _coerce_count(st.get("shareCount"))
        total_impr += impr
        total_clicks += clk
        total_react += rea
        total_comm += com
        total_shares += sh

        share_urn = str(el.get("share") or el.get("ugcPost") or "").strip()
        if share_urn:
            posts_by_urn[share_urn] = {
                "external_id": share_urn,
                "urn": share_urn,
                "url": f"https://www.linkedin.com/feed/update/{share_urn}/" if share_urn.startswith("urn:li:") else "",
                "impressions": impr,
                "clicks": clk,
                "reactions": rea,
                "comments": com,
                "shares": sh,
                "engagement_rate": float(st.get("engagement") or 0.0),
            }

    # Consulta específica por URN en distribution_ledger.json (shares / ugcPosts)
    li_ledger_entries = [
        e
        for e in (ledger_entries or [])
        if isinstance(e, dict)
        and e.get("channel") == "linkedin"
        and str(e.get("external_id") or "").startswith("urn:li:")
    ]
    for ent in li_ledger_entries:
        urn = str(ent["external_id"]).strip()
        if not urn or urn in posts_by_urn:
            continue
        urn_param_key = "ugcPosts[0]" if "ugcPost" in urn else "shares[0]"
        try:
            resp_urn = requests.get(
                LINKEDIN_SHARE_STATS_URL,
                headers=_headers(current_token),
                params={
                    "q": "organizationalEntity",
                    "organizationalEntity": org_urn,
                    urn_param_key: urn,
                },
                timeout=timeout,
            )
            if resp_urn.status_code != 200:
                continue
            urn_els = (resp_urn.json() or {}).get("elements", [])
            for uel in urn_els:
                if not isinstance(uel, dict):
                    continue
                ust = uel.get("totalShareStatistics") or {}
                posts_by_urn[urn] = {
                    "external_id": urn,
                    "urn": urn,
                    "url": str(ent.get("external_url") or f"https://www.linkedin.com/feed/update/{urn}/"),
                    "canonical_url": str(ent.get("canonical_url") or ""),
                    "impressions": _coerce_count(ust.get("impressionCount") or ust.get("uniqueImpressionsCount")),
                    "clicks": _coerce_count(ust.get("clickCount")),
                    "reactions": _coerce_count(ust.get("likeCount")),
                    "comments": _coerce_count(ust.get("commentCount")),
                    "shares": _coerce_count(ust.get("shareCount")),
                    "engagement_rate": float(ust.get("engagement") or 0.0),
                }
        except Exception:
            continue

    post_metrics_list = list(posts_by_urn.values())
    if total_impr == 0 and post_metrics_list:
        total_impr = sum(p["impressions"] for p in post_metrics_list)
        total_clicks = sum(p["clicks"] for p in post_metrics_list)
        total_react = sum(p["reactions"] for p in post_metrics_list)
        total_comm = sum(p["comments"] for p in post_metrics_list)
        total_shares = sum(p["shares"] for p in post_metrics_list)

    # Consulta de seguidores (Followers)
    followers_count = 0
    try:
        resp_foll = requests.get(
            LINKEDIN_FOLLOWER_STATS_URL,
            headers=_headers(current_token),
            params={"q": "organizationalEntity", "organizationalEntity": org_urn},
            timeout=timeout,
        )
        if resp_foll.status_code == 200:
            foll_data = resp_foll.json()
            foll_elements = foll_data.get("elements", []) if isinstance(foll_data, dict) else []
            for fel in foll_elements:
                if isinstance(fel, dict):
                    org_f = _coerce_count(fel.get("organicFollowerCount"))
                    paid_f = _coerce_count(fel.get("paidFollowerCount"))
                    tot_f = _coerce_count(fel.get("totalFollowerCount"))
                    followers_count = max(followers_count, tot_f, org_f + paid_f)
    except Exception:
        pass

    if followers_count == 0:
        try:
            resp_ns = requests.get(
                f"{LINKEDIN_NETWORK_SIZES_URL}/{org_urn}",
                headers=_headers(current_token),
                params={"edgeType": "CompanyFollowedByMember"},
                timeout=timeout,
            )
            if resp_ns.status_code == 200:
                ns_data = resp_ns.json()
                followers_count = _coerce_count(ns_data.get("firstDegreeSize"))
        except Exception:
            pass

    ctr_pct = round((total_clicks / max(total_impr, 1)) * 100.0, 2) if total_impr > 0 else 0.0

    print(
        f"[LINKEDIN-API] Éxito Página de Empresa ({clean_comp}): "
        f"{total_impr} impresiones, {total_clicks} clics, {followers_count} seguidores."
    )

    return True, {
        "status": "api_ok",
        "source": "api",
        "scope": "company_page_only",
        "company_id": clean_comp,
        "total_impressions": total_impr,
        "total_clicks": total_clicks,
        "native_ctr_pct": ctr_pct,
        "total_reactions": total_react,
        "total_comments": total_comm,
        "total_shares": total_shares,
        "followers_count": followers_count,
        "posts": post_metrics_list,
    }


def parse_linkedin_company_xlsx(
    folder_path: Path = IMPORTS_LINKEDIN_DIR,
    file_path: Optional[Path] = None,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Carril B — Parser Determinista .xlsx Oficial (openpyxl):
    Lee exportaciones oficiales de LinkedIn Company Page Analytics (.xlsx) depositadas en
    data/pulse/private/imports/linkedin/*.xlsx (o archivo específico).
    Tolerante a encabezados ES/EN ('All posts'/'Todas las publicaciones', 'Metrics'/'Métricas', 'Followers'/'Seguidores').
    Devuelve (True, parsed_data) o (False, {}).
    """
    try:
        import openpyxl
    except ImportError:
        print("[WARN] openpyxl no está instalado. No se pueden procesar archivos .xlsx de LinkedIn.")
        return False, {}

    target_files: List[Path] = []
    if file_path is not None:
        p = Path(file_path)
        if p.is_file() and p.suffix.lower() == ".xlsx":
            target_files = [p]
    elif folder_path.is_dir():
        for item in folder_path.glob("*.xlsx"):
            if not item.name.startswith("~$"):
                target_files.append(item)

    if not target_files:
        return False, {}

    target_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    newest_file = target_files[0]

    posts_list: List[Dict[str, Any]] = []
    total_impr = 0
    total_clicks = 0
    total_react = 0
    total_comm = 0
    total_shares = 0
    followers_count = 0

    try:
        wb = openpyxl.load_workbook(newest_file, data_only=True)
    except Exception as exc:
        print(f"[WARN] Error abriendo {newest_file.name} con openpyxl: {exc}")
        return False, {}

    sheet_names = wb.sheetnames
    posts_sheet = None
    metrics_sheet = None
    followers_sheet = None

    for name in sheet_names:
        lower_name = name.lower().strip()
        if any(kw in lower_name for kw in ("post", "publicacion", "publicación", "update", "contenido", "content")):
            posts_sheet = wb[name]
        elif any(kw in lower_name for kw in ("metric", "métrica", "metrica", "summary", "resumen", "overview")):
            metrics_sheet = wb[name]
        elif any(kw in lower_name for kw in ("follower", "seguidor")):
            followers_sheet = wb[name]

    if posts_sheet is None:
        posts_sheet = wb.active

    def _clean_header(h: Any) -> str:
        s = str(h or "").lower().strip()
        for char in "()[]{}.,-_:;/\\":
            s = s.replace(char, " ")
        return " ".join(s.split())

    if posts_sheet is not None:
        rows = list(posts_sheet.iter_rows(values_only=True))
        header_idx = -1
        col_map: Dict[str, int] = {}

        for idx, row in enumerate(rows[:10]):
            cleaned_row = [_clean_header(c) for c in row if c is not None]
            joined = " ".join(cleaned_row)
            if any(kw in joined for kw in ("title", "título", "titulo", "post", "publicacion", "update", "impression", "impresion", "clicks", "clics")):
                header_idx = idx
                for col_i, cell in enumerate(row):
                    if cell is None:
                        continue
                    ch = _clean_header(cell)
                    if any(w in ch for w in ("title", "título", "titulo", "texto", "text", "update title", "post title")):
                        col_map.setdefault("title", col_i)
                    elif any(w in ch for w in ("link", "enlace", "url", "permalink", "post link", "update link")):
                        col_map.setdefault("url", col_i)
                    elif any(w in ch for w in ("urn", "id", "update urn", "post urn")):
                        col_map.setdefault("urn", col_i)
                    elif any(w in ch for w in ("date", "fecha", "created", "publicado")):
                        col_map.setdefault("date", col_i)
                    elif any(w in ch for w in ("impression", "impresion", "impresión", "views", "vistas", "visualizaciones")):
                        col_map.setdefault("impressions", col_i)
                    elif any(w in ch for w in ("click", "clic")):
                        col_map.setdefault("clicks", col_i)
                    elif any(w in ch for w in ("reaction", "reaccion", "reacción", "like", "me gusta")):
                        col_map.setdefault("reactions", col_i)
                    elif any(w in ch for w in ("comment", "comentario")):
                        col_map.setdefault("comments", col_i)
                    elif any(w in ch for w in ("repost", "share", "compartido", "veces compartido")):
                        col_map.setdefault("shares", col_i)
                    elif any(w in ch for w in ("engagement rate", "tasa de interaccion", "tasa de interacción", "interaccion", "interacción")):
                        col_map.setdefault("engagement_rate", col_i)
                break

        if header_idx >= 0 and ("impressions" in col_map or "clicks" in col_map or "title" in col_map):
            for row in rows[header_idx + 1:]:
                if not row or all(v is None for v in row):
                    continue
                title_val = str(row[col_map["title"]] or "").strip() if "title" in col_map and col_map["title"] < len(row) else ""
                url_val = str(row[col_map["url"]] or "").strip() if "url" in col_map and col_map["url"] < len(row) else ""
                urn_val = str(row[col_map["urn"]] or "").strip() if "urn" in col_map and col_map["urn"] < len(row) else ""
                date_val = str(row[col_map["date"]] or "").strip() if "date" in col_map and col_map["date"] < len(row) else ""

                if any(w in title_val.lower() for w in ("total", "promedio", "average")):
                    continue

                impr = _coerce_count(row[col_map["impressions"]]) if "impressions" in col_map and col_map["impressions"] < len(row) else 0
                clk = _coerce_count(row[col_map["clicks"]]) if "clicks" in col_map and col_map["clicks"] < len(row) else 0
                rea = _coerce_count(row[col_map["reactions"]]) if "reactions" in col_map and col_map["reactions"] < len(row) else 0
                com = _coerce_count(row[col_map["comments"]]) if "comments" in col_map and col_map["comments"] < len(row) else 0
                sh = _coerce_count(row[col_map["shares"]]) if "shares" in col_map and col_map["shares"] < len(row) else 0
                eng = 0.0
                if "engagement_rate" in col_map and col_map["engagement_rate"] < len(row):
                    try:
                        eng_raw = row[col_map["engagement_rate"]]
                        eng = float(eng_raw) if eng_raw is not None else 0.0
                    except Exception:
                        eng = 0.0

                if not urn_val and url_val:
                    if "update/" in url_val:
                        parts = url_val.split("update/")[-1].strip("/").split("/")
                        if parts:
                            urn_val = parts[0]

                if impr > 0 or clk > 0 or rea > 0 or com > 0 or title_val:
                    total_impr += impr
                    total_clicks += clk
                    total_react += rea
                    total_comm += com
                    total_shares += sh

                    posts_list.append({
                        "title": title_val,
                        "url": url_val,
                        "urn": urn_val or f"xlsx_row_{len(posts_list) + 1}",
                        "external_id": urn_val or f"xlsx_row_{len(posts_list) + 1}",
                        "date": date_val or None,
                        "impressions": impr,
                        "clicks": clk,
                        "reactions": rea,
                        "comments": com,
                        "shares": sh,
                        "engagement_rate": eng,
                    })

    if followers_sheet is not None:
        f_rows = list(followers_sheet.iter_rows(values_only=True))
        for r in reversed(f_rows):
            if not r:
                continue
            for val in r:
                if isinstance(val, (int, float)) and val > followers_count:
                    if 1 <= int(val) <= 10_000_000:
                        followers_count = int(val)
            if followers_count > 0:
                break

    if followers_count == 0 and metrics_sheet is not None:
        m_rows = list(metrics_sheet.iter_rows(values_only=True))
        for r in m_rows:
            if not r:
                continue
            r_str = " ".join([str(c or "").lower() for c in r])
            if any(w in r_str for w in ("follower", "seguidor")):
                for cell in r:
                    c_num = _coerce_count(cell)
                    if c_num > followers_count:
                        followers_count = c_num

    ctr_pct = round((total_clicks / max(total_impr, 1)) * 100.0, 2) if total_impr > 0 else 0.0

    print(
        f"[LINKEDIN-XLSX] Parseado {newest_file.name}: "
        f"{len(posts_list)} publicaciones, {total_impr} impresiones, {total_clicks} clics, {followers_count} seguidores."
    )

    return True, {
        "status": "xlsx_import_ok",
        "source": "xlsx",
        "scope": "company_page_only",
        "file_name": newest_file.name,
        "total_impressions": total_impr,
        "total_clicks": total_clicks,
        "native_ctr_pct": ctr_pct,
        "total_reactions": total_react,
        "total_comments": total_comm,
        "total_shares": total_shares,
        "followers_count": followers_count,
        "posts": posts_list,
    }



def consolidate_social_metrics(
    assets: List[Dict[str, Any]],
    devto_articles: List[Dict[str, Any]],
    devto_ok: bool,
    coderlegion_posts: List[Dict[str, Any]],
    coderlegion_ok: bool,
    linkedin_company_data: Optional[Dict[str, Any]] = None,
    linkedin_company_ok: bool = False,
    existing_social_metrics: Optional[Dict[str, Any]] = None,
    ledger_path: Optional[Path] = LEDGER_PATH,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Consolida las métricas nativas de Dev.to, CoderLegion y LinkedIn Página de Empresa (Modo Dual: API + XLSX)
    por plataforma y por activo (`ContentAsset`).
    Garantiza degradación elegante independiente por fuente (`INV-PULSE-11/12`) y actualiza el ledger.
    """
    existing = existing_social_metrics or {}
    prev_platforms = existing.get("platforms") if isinstance(existing.get("platforms"), dict) else {}
    prev_by_asset = existing.get("by_asset") if isinstance(existing.get("by_asset"), dict) else {}

    now_iso = datetime.now(timezone.utc).isoformat()
    lookup = build_asset_url_lookup(assets)

    platforms_out: Dict[str, Dict[str, Any]] = {}
    by_asset_out: Dict[str, Dict[str, Any]] = defaultdict(dict)

    # Copiar primero el estado previo de todos los activos para preservar plataformas que no se refresquen hoy
    for aid, ch_map in prev_by_asset.items():
        if isinstance(ch_map, dict):
            by_asset_out[aid] = {k: dict(v) for k, v in ch_map.items() if isinstance(v, dict)}

    # --- 1. Bloque DEV.TO (aislado) ---
    if devto_ok:
        # Limpiar entradas previas de devto en by_asset_out antes de reconstruir con datos frescos
        for aid in list(by_asset_out.keys()):
            by_asset_out[aid].pop("devto", None)

        devto_by_asset: Dict[str, Dict[str, Any]] = {}
        matched_articles: List[Dict[str, Any]] = []

        for art in devto_articles:
            canonical = str(art.get("canonical_url") or "").strip()
            aid, slug, lang = match_canonical_to_asset(canonical, assets, lookup=lookup)
            eff_lang: Literal["es", "en"] = "es" if lang == "es" else "en"
            record = {
                **art,
                "platform": "devto",
                "asset_id": aid,
                "matched_slug": slug or art.get("slug", ""),
                "lang": lang,
            }
            matched_articles.append(record)

            if aid:
                bucket = devto_by_asset.setdefault(
                    aid,
                    {
                        "views": 0,
                        "views_es": 0,
                        "views_en": 0,
                        "reactions": 0,
                        "comments": 0,
                        "articles_count": 0,
                        "external_ids": [],
                        "urls": [],
                    },
                )
                v = int(art.get("views", 0) or 0)
                r = int(art.get("reactions", 0) or 0)
                c = int(art.get("comments", 0) or 0)
                bucket["views"] += v
                if lang == "es":
                    bucket["views_es"] += v
                else:
                    bucket["views_en"] += v
                bucket["reactions"] += r
                bucket["comments"] += c
                bucket["articles_count"] += 1
                if art.get("external_id") and art["external_id"] not in bucket["external_ids"]:
                    bucket["external_ids"].append(art["external_id"])
                if art.get("url") and art["url"] not in bucket["urls"]:
                    bucket["urls"].append(art["url"])

                if not dry_run and ledger_path is not None and canonical:
                    record_distribution_ledger_entry(
                        asset_id=aid,
                        slug=slug or aid,
                        lang=eff_lang,
                        channel="devto",
                        external_id=str(art["external_id"]),
                        external_url=art.get("url"),
                        canonical_url=canonical,
                        published_at_utc=art.get("published_at"),
                        ledger_path=ledger_path,
                    )

        for aid, b in devto_by_asset.items():
            by_asset_out[aid]["devto"] = b

        platforms_out["devto"] = {
            "status": "ok",
            "last_synced_at": now_iso,
            "articles_count": len(matched_articles),
            "matched_assets_count": len(devto_by_asset),
            "total_views": sum(int(a.get("views", 0) or 0) for a in matched_articles),
            "total_reactions": sum(int(a.get("reactions", 0) or 0) for a in matched_articles),
            "total_comments": sum(int(a.get("comments", 0) or 0) for a in matched_articles),
            "articles": matched_articles,
        }
    else:
        platforms_out["devto"] = dict(
            prev_platforms.get(
                "devto",
                {
                    "status": "unavailable",
                    "last_synced_at": None,
                    "articles_count": 0,
                    "matched_assets_count": 0,
                    "total_views": 0,
                    "total_reactions": 0,
                    "total_comments": 0,
                    "articles": [],
                },
            )
        )

    # --- 2. Bloque CODERLEGION (aislado) ---
    if coderlegion_ok:
        for aid in list(by_asset_out.keys()):
            by_asset_out[aid].pop("coderlegion", None)

        cl_by_asset: Dict[str, Dict[str, Any]] = {}
        matched_cl: List[Dict[str, Any]] = []

        for post in coderlegion_posts:
            canonical = str(post.get("canonical_url") or "").strip()
            aid, slug, lang = match_canonical_to_asset(canonical, assets, lookup=lookup)
            eff_lang = "es" if lang == "es" else "en"
            record = {
                **post,
                "platform": "coderlegion",
                "asset_id": aid,
                "matched_slug": slug or post.get("slug", ""),
                "lang": eff_lang if aid else lang,
            }
            matched_cl.append(record)

            if aid:
                bucket = cl_by_asset.setdefault(
                    aid,
                    {
                        "views": 0,
                        "views_es": 0,
                        "views_en": 0,
                        "reactions": 0,
                        "comments": 0,
                        "articles_count": 0,
                        "external_ids": [],
                        "urls": [],
                    },
                )
                v = int(post.get("views", 0) or 0)
                r = int(post.get("reactions", 0) or 0)
                c = int(post.get("comments", 0) or 0)
                bucket["views"] += v
                if eff_lang == "es":
                    bucket["views_es"] += v
                else:
                    bucket["views_en"] += v
                bucket["reactions"] += r
                bucket["comments"] += c
                bucket["articles_count"] += 1
                if post.get("external_id") and post["external_id"] not in bucket["external_ids"]:
                    bucket["external_ids"].append(post["external_id"])
                if post.get("url") and post["url"] not in bucket["urls"]:
                    bucket["urls"].append(post["url"])

                if not dry_run and ledger_path is not None and canonical:
                    record_distribution_ledger_entry(
                        asset_id=aid,
                        slug=slug or aid,
                        lang=eff_lang,
                        channel="coderlegion",
                        external_id=str(post["external_id"]),
                        external_url=post.get("url"),
                        canonical_url=canonical,
                        published_at_utc=post.get("published_at"),
                        ledger_path=ledger_path,
                    )

        for aid, b in cl_by_asset.items():
            by_asset_out[aid]["coderlegion"] = b

        platforms_out["coderlegion"] = {
            "status": "ok",
            "last_synced_at": now_iso,
            "articles_count": len(matched_cl),
            "matched_assets_count": len(cl_by_asset),
            "total_views": sum(int(p.get("views", 0) or 0) for p in matched_cl),
            "total_reactions": sum(int(p.get("reactions", 0) or 0) for p in matched_cl),
            "total_comments": sum(int(p.get("comments", 0) or 0) for p in matched_cl),
            "articles": matched_cl,
        }
    else:
        platforms_out["coderlegion"] = dict(
            prev_platforms.get(
                "coderlegion",
                {
                    "status": "unavailable",
                    "last_synced_at": None,
                    "articles_count": 0,
                    "matched_assets_count": 0,
                    "total_views": 0,
                    "total_reactions": 0,
                    "total_comments": 0,
                    "articles": [],
                },
            )
        )

    # --- 3. Bloque LINKEDIN EMPRESA (Carril Dual: API + XLSX — Hito 7.13 / ADR-033) ---
    if linkedin_company_ok and isinstance(linkedin_company_data, dict) and linkedin_company_data:
        for aid in list(by_asset_out.keys()):
            by_asset_out[aid].pop("linkedin_company", None)

        li_by_asset: Dict[str, Dict[str, Any]] = {}
        matched_posts: List[Dict[str, Any]] = []
        raw_posts = linkedin_company_data.get("posts", []) or []

        ledger_li_by_id: Dict[str, Dict[str, Any]] = {}
        if ledger_path is not None and ledger_path.is_file():
            try:
                with open(ledger_path, "r", encoding="utf-8") as fh:
                    cur_led = json.load(fh)
                for ent in (cur_led.get("entries", []) or []):
                    if isinstance(ent, dict) and ent.get("channel") == "linkedin":
                        ext_id_k = str(ent.get("external_id") or "").strip()
                        if ext_id_k:
                            ledger_li_by_id[ext_id_k] = ent
            except Exception:
                pass

        for p in raw_posts:
            if not isinstance(p, dict):
                continue
            urn = str(p.get("urn") or p.get("external_id") or "").strip()
            url_str = str(p.get("url") or "").strip()
            canonical = str(p.get("canonical_url") or "").strip()

            aid: Optional[str] = None
            slug: str = ""
            lang: Literal["es", "en", "other"] = "other"

            if urn and urn in ledger_li_by_id:
                lent = ledger_li_by_id[urn]
                aid = str(lent.get("asset_id") or "")
                slug = str(lent.get("slug") or aid)
                lang = lent.get("lang") or "es"
                if not canonical:
                    canonical = str(lent.get("canonical_url") or "")
            elif url_str:
                aid, slug, lang = match_canonical_to_asset(url_str, assets, lookup=lookup)
            elif p.get("title"):
                t_lower = str(p.get("title", "")).lower()
                for asset in assets:
                    aslug = str(asset.get("slug") or "").lower()
                    if aslug and aslug in t_lower:
                        aid = str(asset.get("id"))
                        slug = str(asset.get("slug") or aid)
                        lang = "es" if "/es/" in str(asset.get("url_es", "")) else "en"
                        break

            eff_lang: Literal["es", "en"] = "es" if lang == "es" else "en"
            impr = _coerce_count(p.get("impressions"))
            clk = _coerce_count(p.get("clicks"))
            rea = _coerce_count(p.get("reactions"))
            com = _coerce_count(p.get("comments"))
            sh = _coerce_count(p.get("shares"))

            rec = {
                **p,
                "platform": "linkedin_company",
                "asset_id": aid,
                "matched_slug": slug or urn,
                "lang": eff_lang if aid else lang,
            }
            matched_posts.append(rec)

            if aid:
                b = li_by_asset.setdefault(
                    aid,
                    {
                        "impressions": 0,
                        "views": 0,
                        "clicks": 0,
                        "reactions": 0,
                        "comments": 0,
                        "shares": 0,
                        "posts_count": 0,
                        "external_ids": [],
                        "urls": [],
                    },
                )
                b["impressions"] += impr
                b["views"] += impr
                b["clicks"] += clk
                b["reactions"] += rea
                b["comments"] += com
                b["shares"] += sh
                b["posts_count"] += 1
                if urn and urn not in b["external_ids"]:
                    b["external_ids"].append(urn)
                if url_str and url_str not in b["urls"]:
                    b["urls"].append(url_str)

                if not dry_run and ledger_path is not None and canonical:
                    record_distribution_ledger_entry(
                        asset_id=aid,
                        slug=slug or aid,
                        lang=eff_lang,
                        channel="linkedin",
                        external_id=urn or f"li_{aid}_{eff_lang}",
                        external_url=url_str or f"https://www.linkedin.com/feed/update/{urn}/",
                        canonical_url=canonical,
                        published_at_utc=p.get("date") or p.get("published_at"),
                        ledger_path=ledger_path,
                    )

        for aid, b in li_by_asset.items():
            by_asset_out[aid]["linkedin_company"] = b

        tot_impr = int(linkedin_company_data.get("total_impressions", 0) or 0)
        tot_clicks = int(linkedin_company_data.get("total_clicks", 0) or 0)
        tot_react = int(linkedin_company_data.get("total_reactions", 0) or 0)
        tot_comm = int(linkedin_company_data.get("total_comments", 0) or 0)
        tot_shares = int(linkedin_company_data.get("total_shares", 0) or 0)
        foll_cnt = int(linkedin_company_data.get("followers_count", 0) or 0)
        native_ctr = round((tot_clicks / max(tot_impr, 1)) * 100.0, 2) if tot_impr > 0 else 0.0

        platforms_out["linkedin_company"] = {
            "status": str(linkedin_company_data.get("status") or "api_ok"),
            "source": str(linkedin_company_data.get("source") or "api"),
            "scope": "company_page_only",
            "company_id": str(linkedin_company_data.get("company_id") or os.environ.get("LINKEDIN_COMPANY_ID", "")),
            "last_synced_at": now_iso,
            "posts_count": len(matched_posts),
            "matched_assets_count": len(li_by_asset),
            "total_impressions": tot_impr,
            "total_clicks": tot_clicks,
            "native_ctr_pct": native_ctr,
            "total_reactions": tot_react,
            "total_comments": tot_comm,
            "total_shares": tot_shares,
            "followers_count": foll_cnt,
            "posts": matched_posts,
        }
    else:
        prev_li = dict(
            prev_platforms.get(
                "linkedin_company",
                {
                    "status": "unavailable",
                    "source": "none",
                    "scope": "company_page_only",
                    "last_synced_at": None,
                    "total_impressions": 0,
                    "total_clicks": 0,
                    "native_ctr_pct": 0.0,
                    "total_reactions": 0,
                    "total_comments": 0,
                    "total_shares": 0,
                    "followers_count": 0,
                    "posts_count": 0,
                    "matched_assets_count": 0,
                    "posts": [],
                },
            )
        )
        if prev_li.get("status") == "pending_hito_7_13":
            prev_li["status"] = "unavailable"
        if "source" not in prev_li:
            prev_li["source"] = "none"
        platforms_out["linkedin_company"] = prev_li

    # --- 4. Bloque X / TWITTER (Stand-by Coste 0 € — ADR-033 / INV-PULSE-12) ---
    platforms_out["x"] = {
        "status": "standby_zero_cost",
        "last_synced_at": None,
        "note": "Medición activa vía GA4 + UTMs (Hito 7.11); API nativa X en stand-by por política coste 0 EUR.",
    }

    clean_by_asset = {aid: chs for aid, chs in sorted(by_asset_out.items()) if chs}

    return {
        "version": "1.0.0",
        "visibility": "private",
        "generated_at": now_iso,
        "platforms": platforms_out,
        "by_asset": clean_by_asset,
    }


def sync_all_social_metrics(
    *,
    dry_run: bool = False,
    backfill_coderlegion_pages: int = 0,
    skip_linkedin_api: bool = False,
    import_linkedin_xlsx_path: Optional[Path] = None,
    index_path: Path = INDEX_PATH,
    ledger_path: Path = LEDGER_PATH,
    output_path: Path = SOCIAL_METRICS_PATH,
    imports_linkedin_dir: Path = IMPORTS_LINKEDIN_DIR,
) -> Dict[str, Any]:
    """Ejecuta el pipeline completo de sincronización social gratuita (Dev.to + CoderLegion + LinkedIn Modo Dual)."""
    _load_local_env_if_needed()

    assets: List[Dict[str, Any]] = []
    if index_path.is_file():
        try:
            with open(index_path, "r", encoding="utf-8") as fh:
                assets = json.load(fh)
        except Exception as exc:
            print(f"[WARN] No se pudo leer {index_path}: {exc}")

    existing_social: Dict[str, Any] = {}
    if output_path.is_file():
        try:
            with open(output_path, "r", encoding="utf-8") as fh:
                existing_social = json.load(fh)
        except Exception:
            existing_social = {}

    ledger = load_distribution_ledger(ledger_path)
    ledger_entries = ledger.get("entries", []) if isinstance(ledger, dict) else []

    devto_ok, devto_articles = fetch_devto_published_articles()
    cl_ok, cl_posts = fetch_coderlegion_posts(
        ledger_entries=ledger_entries,
        backfill_pages=backfill_coderlegion_pages,
    )

    # Carril Dual LinkedIn Página de Empresa (API > XLSX > snapshot previo)
    li_ok = False
    li_data: Dict[str, Any] = {}
    if not skip_linkedin_api:
        li_ok, li_data = fetch_linkedin_company_api_metrics(ledger_entries=ledger_entries)

    if not li_ok:
        xlsx_ok, xlsx_data = parse_linkedin_company_xlsx(
            folder_path=imports_linkedin_dir,
            file_path=import_linkedin_xlsx_path,
        )
        if xlsx_ok:
            li_ok = True
            li_data = xlsx_data

    consolidated = consolidate_social_metrics(
        assets=assets,
        devto_articles=devto_articles,
        devto_ok=devto_ok,
        coderlegion_posts=cl_posts,
        coderlegion_ok=cl_ok,
        linkedin_company_data=li_data,
        linkedin_company_ok=li_ok,
        existing_social_metrics=existing_social,
        ledger_path=ledger_path,
        dry_run=dry_run,
    )

    if dry_run:
        dt_meta = consolidated["platforms"]["devto"]
        cl_meta = consolidated["platforms"]["coderlegion"]
        li_meta = consolidated["platforms"]["linkedin_company"]
        print(
            f"[DRY-RUN] sync_social_metrics completado sin escribir en disco · "
            f"Dev.to: status={dt_meta.get('status')} ({dt_meta.get('articles_count', 0)} arts, {dt_meta.get('total_views', 0)} vistas) · "
            f"CoderLegion: status={cl_meta.get('status')} ({cl_meta.get('articles_count', 0)} posts, {cl_meta.get('total_views', 0)} vistas) · "
            f"LinkedIn: status={li_meta.get('status')} source={li_meta.get('source')} ({li_meta.get('total_impressions', 0)} imp, {li_meta.get('total_clicks', 0)} clics, {li_meta.get('followers_count', 0)} seguidores) · "
            f"X: {consolidated['platforms']['x']['status']}."
        )
        return consolidated

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(consolidated, fh, ensure_ascii=False, indent=2)
    print(f"[SYNC-SOCIAL] Métricas sociales guardadas en {output_path}.")
    return consolidated


def main(argv: Optional[List[str]] = None) -> int:
    _configure_utf8_stdio()
    parser = argparse.ArgumentParser(
        description="Sincronizador gratuito de métricas nativas Dev.to, CoderLegion y LinkedIn Empresa Modo Dual (Hito 7.13)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Ejecuta la consulta y consolidación sin modificar social_metrics.json ni distribution_ledger.json.",
    )
    parser.add_argument(
        "--backfill-coderlegion",
        type=int,
        default=0,
        metavar="PAGES",
        help="Número acotado de páginas de GET /api/v1/posts a explorar para descubrir posts con source_url de Datalaria.",
    )
    parser.add_argument(
        "--skip-linkedin-api",
        action="store_true",
        help="Omite la llamada a LinkedIn Community Management API (fuerza Carril B .xlsx o snapshot previo).",
    )
    parser.add_argument(
        "--import-linkedin-xlsx",
        type=str,
        default=None,
        metavar="FILE_PATH",
        help="Ruta específica a un archivo .xlsx exportado desde LinkedIn Analytics para importar inmediatamente.",
    )
    args = parser.parse_args(argv)

    try:
        import_path = Path(args.import_linkedin_xlsx) if args.import_linkedin_xlsx else None
        sync_all_social_metrics(
            dry_run=args.dry_run,
            backfill_coderlegion_pages=max(0, min(args.backfill_coderlegion, 10)),
            skip_linkedin_api=args.skip_linkedin_api,
            import_linkedin_xlsx_path=import_path,
        )
        return 0
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
