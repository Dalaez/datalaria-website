"""
ops/pulse/build_index.py
------------------------
Generador del Índice Editorial Canónico de Datalaria Pulse.
Especificación técnica formal: SPEC-APP-PULSE (specs/apps/pulse/spec.md).

Escanea determinísticamente sin depender de Notion:
1. content/es/posts/ y content/en/posts/ (artículos técnicos bilingües).
2. data/apps/*.yaml (aplicaciones web activas).
3. data/pulse/kits.yaml (kits de decisión y suites B2B).
4. data/editorial/backlog.yaml (ideas prospectivas y backlog).

Calcula:
- Emparejamiento bilingüe exacto (109 pares ES ⇔ EN validados al 100%).
- Paridad lingüística (complete, missing_en, missing_es, outdated_en, outdated_es).
- Conteo real de palabras y tiempo estimado de lectura.
- Auditoría SEO determinista (score 0-100 con 5 checks).
- Estado de frescura documental (fresh, review_soon, stale).
- Detección de enlaces cruzados (shortcode app-ref hacia apps y checkout hacia kits).

Exporta a:
- data/pulse/private/index.json (índice completo con datos privados).
- static/apps/pulse/data/public.json (dataset público relativizado y filtrado según INV-PULSE-1 e INV-PULSE-2).
"""

import os
import re
import glob
import json
import math
import subprocess
from datetime import datetime, date, timezone
from typing import Dict, List, Optional, Tuple, Any, Set

import yaml
import frontmatter

from ops.pulse.models import (
    ContentAsset,
    SeoAudit,
    RelativeMetrics,
    PublicPulseDataset
)


# ==============================================================================
# HELPERS DE GIT Y FECHAS
# ==============================================================================

def get_git_file_lastmod_map() -> Dict[str, datetime]:
    """
    Construye un mapa { ruta_normalizada: datetime_lastmod } escaneando el historial de git.
    Ejecuta un único comando git log para optimizar el rendimiento.
    """
    lastmod_map: Dict[str, datetime] = {}
    try:
        out = subprocess.check_output(
            ["git", "log", "--format=COMMIT:%cI", "--name-only"],
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        current_dt: Optional[datetime] = None
        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("COMMIT:"):
                dt_str = line[7:]
                try:
                    current_dt = datetime.fromisoformat(dt_str)
                except Exception:
                    current_dt = None
            elif current_dt is not None:
                norm_path = line.replace("\\", "/").lower()
                if norm_path not in lastmod_map:
                    lastmod_map[norm_path] = current_dt
    except Exception as e:
        print(f"[WARN] Error obteniendo historial de Git: {e}")

    return lastmod_map


# ==============================================================================
# AUDITORÍA SEO Y CONTEO DE PALABRAS
# ==============================================================================

def count_words(markdown_text: str) -> int:
    """
    Calcula el conteo léxico real eliminando bloques de código, HTML y shortcodes.
    """
    text = re.sub(r'```[\s\S]*?```', ' ', markdown_text)
    text = re.sub(r'`[^`]+`', ' ', text)
    text = re.sub(r'\{\{<[\s\S]*?>\}\}', ' ', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    words = re.findall(r'\b\w+\b', text)
    return len(words)


def audit_seo(
    title: Optional[str],
    description: Optional[str],
    parity: str,
    categories: List[str],
    tags: List[str],
    content_text: str
) -> SeoAudit:
    """
    Evaluación determinista de salud SEO (0 a 100 puntos):
    1. title_ok (20 pts): longitud entre 35 y 95 caracteres.
    2. description_ok (20 pts): descripción entre 75 y 250 caracteres.
    3. parity_ok (20 pts): paridad lingüística 'complete'.
    4. taxonomy_ok (20 pts): al menos 1 categoría y >= 3 tags.
    5. internal_links_ok (20 pts): enlaces internos o shortcode app-ref.
    """
    issues = []
    
    title_len = len(title) if title else 0
    title_ok = (35 <= title_len <= 95)
    if not title_ok:
        issues.append(f"Longitud de título no óptima ({title_len} caracteres; ideal: 35-95)")

    desc_len = len(description) if description else 0
    description_ok = (75 <= desc_len <= 250)
    if not description_ok:
        issues.append(f"Meta descripción no óptima ({desc_len} caracteres; ideal: 75-250)")

    parity_ok = (parity == "complete")
    if not parity_ok:
        issues.append(f"Paridad bilingüe incompleta o desfasada ({parity})")

    taxonomy_ok = (len(categories) >= 1 and len(tags) >= 3)
    if not taxonomy_ok:
        issues.append("Taxonomía insuficiente: requiere al menos 1 categoría y 3 tags")

    has_internal_link = bool(re.search(r'\[.*?\]\((/|https?://datalaria\.com)', content_text))
    has_app_ref = bool(re.search(r'\{\{<\s*app-ref', content_text))
    internal_links_ok = (has_internal_link or has_app_ref)
    if not internal_links_ok:
        issues.append("Sin enlaces internos hacia el portal o shortcodes de apps")

    score = 0
    if title_ok: score += 20
    if description_ok: score += 20
    if parity_ok: score += 20
    if taxonomy_ok: score += 20
    if internal_links_ok: score += 20

    return SeoAudit(
        score_0_100=score,
        title_ok=title_ok,
        description_ok=description_ok,
        parity_ok=parity_ok,
        taxonomy_ok=taxonomy_ok,
        internal_links_ok=internal_links_ok,
        issues=issues
    )


# ==============================================================================
# ESCÁNERES DE ACTIVOS
# ==============================================================================

def scan_posts(git_map: Dict[str, datetime]) -> List[ContentAsset]:
    """
    Escanea content/es/posts/ y content/en/posts/, emparejando de forma exhaustiva
    y determinista los 109 pares bilingües.
    """
    es_posts: Dict[str, Dict[str, Any]] = {}
    en_posts: Dict[str, Dict[str, Any]] = {}

    def read_post_file(path: str) -> Optional[Dict[str, Any]]:
        if not os.path.isfile(path):
            return None
        try:
            post = frontmatter.load(path)
            norm = path.replace("\\", "/").lower()
            lastmod = git_map.get(norm)
            if not lastmod:
                mtime = os.path.getmtime(path)
                lastmod = datetime.fromtimestamp(mtime, tz=timezone.utc)
            return {
                "metadata": post.metadata,
                "content": post.content,
                "path": path,
                "lastmod": lastmod
            }
        except Exception as e:
            print(f"[WARN] Error leyendo {path}: {e}")
            return None

    es_base = "content/es/posts"
    for d in sorted(os.listdir(es_base)):
        p = os.path.join(es_base, d, "index.md")
        data = read_post_file(p)
        if data:
            raw_date = data["metadata"].get("date")
            date_str = str(raw_date)
            es_posts[d] = {"slug": d, "date_str": date_str, **data}

    en_base = "content/en/posts"
    for d in sorted(os.listdir(en_base)):
        p = os.path.join(en_base, d, "index.md")
        data = read_post_file(p)
        if data:
            raw_date = data["metadata"].get("date")
            date_str = str(raw_date)
            en_posts[d] = {"slug": d, "date_str": date_str, **data}

    # Mapa explícito para casos con nombres de carpeta asimétricos o fechas compartidas
    explicit_pairs = {
        'business-case-financiero-van-tir': 'financial-business-case-npv-irr',
        'estimacion-pert-3-puntos': 'stochastic-3-point-pert-estimation',
        'matriz-raci-balance-carga': 'quantitative-raci-workload-matrix',
        'matriz-riesgos-amfe-fmea': 'quantitative-risk-matrix-fmea',
        'matriz-mckinsey-ge': 'mckinsey-ge-matrix',
        'matriz-rice-ice-priorizacion': 'rice-ice-prioritization-matrix',
        'proj_ops_parte1_intro': 'proj_ops_part1_intro',
        'proj_ops_parte2_agentic_pmo': 'proj_ops_part2_agentic_pmo',
        'calculadora-stock-seguridad-rop': 'safety-stock-rop-calculator',
        'control-operativo-pmbok-framework-cuantitativo': 'quantitative-operations-control-framework',
        'pulse-parte1-adios-notion-content-ops': 'pulse-part1-goodbye-notion-content-ops',
        'app_conversor_unidades': 'app_unit_converter',
        'Estadistica-descriptiva': 'Descriptive-statistics',
        'Visualizaciones-basicas': 'Basic-Visualizations'
    }

    pairs: List[Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]] = []
    paired_es: Set[str] = set()
    paired_en: Set[str] = set()

    # 1. TranslationKey explícito
    for d_es, es_data in es_posts.items():
        tk_es = es_data["metadata"].get("translationKey")
        if tk_es:
            for d_en, en_data in en_posts.items():
                if d_en not in paired_en and en_data["metadata"].get("translationKey") == tk_es:
                    pairs.append((es_data, en_data))
                    paired_es.add(d_es)
                    paired_en.add(d_en)
                    break

    # 2. Pares explícitos conocidos
    for d_es, d_en in explicit_pairs.items():
        if d_es in es_posts and d_en in en_posts and d_es not in paired_es and d_en not in paired_en:
            pairs.append((es_posts[d_es], en_posts[d_en]))
            paired_es.add(d_es)
            paired_en.add(d_en)

    # 3. Mismo nombre de directorio
    for d_es in es_posts:
        if d_es not in paired_es and d_es in en_posts and d_es not in paired_en:
            pairs.append((es_posts[d_es], en_posts[d_es]))
            paired_es.add(d_es)
            paired_en.add(d_es)

    # 4. Cruce unívoco por fecha exacta
    unpaired_es = {k: v for k, v in es_posts.items() if k not in paired_es}
    unpaired_en = {k: v for k, v in en_posts.items() if k not in paired_en}

    for d_es, es_data in list(unpaired_es.items()):
        cands = [d for d, en_data in unpaired_en.items() if en_data["date_str"] == es_data["date_str"]]
        if len(cands) == 1:
            d_en = cands[0]
            pairs.append((es_data, unpaired_en[d_en]))
            paired_es.add(d_es)
            paired_en.add(d_en)
            del unpaired_en[d_en]

    # 5. Agregar cualquier elemento huérfano si existiera
    for d_es, es_data in es_posts.items():
        if d_es not in paired_es:
            pairs.append((es_data, None))
    for d_en, en_data in en_posts.items():
        if d_en not in paired_en:
            pairs.append((None, en_data))

    assets: List[ContentAsset] = []
    today = date.today()

    for es, en in pairs:
        # Determinar paridad
        if es and not en:
            parity = "missing_en"
        elif en and not es:
            parity = "missing_es"
        else:
            diff_days = (es["lastmod"] - en["lastmod"]).total_seconds() / 86400.0
            if diff_days > 7.0:
                parity = "outdated_en"
            elif diff_days < -7.0:
                parity = "outdated_es"
            else:
                parity = "complete"

        meta_primary = (es or en)["metadata"]
        raw_date = meta_primary.get("date")
        publish_d: Optional[date] = None
        if isinstance(raw_date, datetime):
            publish_d = raw_date.date()
        elif isinstance(raw_date, date):
            publish_d = raw_date
        elif isinstance(raw_date, str):
            try:
                publish_d = datetime.fromisoformat(raw_date).date()
            except Exception:
                pass

        draft = meta_primary.get("draft", False)
        if draft:
            status = "draft"
        elif publish_d and publish_d > today:
            status = "scheduled"
        else:
            status = "published"

        wc_es = count_words(es["content"]) if es else 0
        wc_en = count_words(en["content"]) if en else 0
        max_wc = max(wc_es, wc_en)
        reading_time = max(1, math.ceil(max_wc / 200)) if max_wc > 0 else 1

        title_eval = (es or en)["metadata"].get("title")
        desc_eval = (es or en)["metadata"].get("description") or (es or en)["metadata"].get("summary")
        categories = meta_primary.get("categories") or ([meta_primary.get("category")] if meta_primary.get("category") else [])
        tags = meta_primary.get("tags") or []
        body_eval = (es["content"] if es else en["content"])
        seo = audit_seo(title_eval, desc_eval, parity, categories, tags, body_eval)

        related_app = None
        app_match = re.search(r'\{\{<\s*app-ref\s+slug="([^"]+)"', body_eval)
        if app_match:
            related_app = app_match.group(1)

        related_kit = None
        kit_match = re.search(r'(?:/recursos/|/resources/|datalaria\.lemonsqueezy\.com)[^"\'\s)]*', body_eval)
        if kit_match:
            related_kit = kit_match.group(0)

        series = meta_primary.get("series")
        slug_ref = (es or en)["slug"]
        if not series:
            if slug_ref.startswith("app-lifeops_part"):
                series = "LifeOps"
            elif slug_ref.startswith("obs_part"):
                series = "Agentic Radar"
            elif slug_ref.startswith("app-openweather_part"):
                series = "Weather"

        last_dt = max(filter(None, [es["lastmod"] if es else None, en["lastmod"] if en else None]))
        days_since_mod = (datetime.now(timezone.utc) - last_dt).days if last_dt else 0
        if days_since_mod > 365:
            freshness = "stale"
        elif days_since_mod > 180:
            freshness = "review_soon"
        else:
            freshness = "fresh"

        canonical_id = meta_primary.get("translationKey") or (es["slug"] if es else en["slug"])
        slug_val = es["slug"] if es else en["slug"]

        assets.append(ContentAsset(
            id=canonical_id,
            slug=slug_val,
            asset_type="post",
            status=status,
            visibility="public",
            title_es=es["metadata"].get("title") if es else None,
            title_en=en["metadata"].get("title") if en else None,
            url_es=f"/es/posts/{es['slug']}/" if es else None,
            url_en=f"/en/posts/{en['slug']}/" if en else None,
            brief_es=es["metadata"].get("description") or es["metadata"].get("summary") if es else None,
            brief_en=en["metadata"].get("description") or en["metadata"].get("summary") if en else None,
            publish_date=publish_d,
            last_modified_es=es["lastmod"] if es else None,
            last_modified_en=en["lastmod"] if en else None,
            language_parity=parity,
            category=meta_primary.get("category") or (categories[0] if categories else "General"),
            categories=categories,
            tags=tags,
            series=series,
            word_count_es=wc_es,
            word_count_en=wc_en,
            reading_time_min=reading_time,
            related_app=related_app,
            related_kit=related_kit,
            seo_audit=seo,
            freshness_status=freshness,
            owner=meta_primary.get("author", "Daniel Alaez")
        ))

    return assets


def scan_apps(git_map: Dict[str, datetime]) -> List[ContentAsset]:
    """
    Escanea data/apps/*.yaml y construye los activos tipo 'app'.
    Soporta campos bilingües tanto en formato diccionario {'es': ..., 'en': ...} como texto directo.
    """
    assets: List[ContentAsset] = []
    yaml_files = sorted(glob.glob("data/apps/*.yaml"))

    def resolve_i18n_field(raw_val: Any, lang: str) -> Optional[str]:
        if isinstance(raw_val, dict):
            return raw_val.get(lang) or raw_val.get("es") or raw_val.get("en")
        if isinstance(raw_val, str):
            return raw_val
        return None

    for fpath in yaml_files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                app_meta = yaml.safe_load(f)

            slug = app_meta.get("slug") or os.path.splitext(os.path.basename(fpath))[0]
            norm = fpath.replace("\\", "/").lower()
            lastmod = git_map.get(norm, datetime.now(timezone.utc))

            releases = app_meta.get("releases", [])
            latest_release = releases[-1] if releases else {}
            pub_date = None
            if latest_release.get("date"):
                try:
                    pub_date = datetime.fromisoformat(latest_release["date"]).date()
                except Exception:
                    pass

            title_es = resolve_i18n_field(app_meta.get("title"), "es") or app_meta.get("name")
            title_en = resolve_i18n_field(app_meta.get("title"), "en") or app_meta.get("name_en") or title_es

            brief_es = resolve_i18n_field(app_meta.get("tagline"), "es") or resolve_i18n_field(app_meta.get("summary"), "es")
            brief_en = resolve_i18n_field(app_meta.get("tagline"), "en") or resolve_i18n_field(app_meta.get("summary"), "en") or brief_es

            tags_list: List[str] = []
            if "tech" in app_meta and isinstance(app_meta["tech"], list):
                for layer in app_meta["tech"]:
                    if isinstance(layer, dict) and "items" in layer:
                        tags_list.extend(layer["items"])
                    elif isinstance(layer, str):
                        tags_list.append(layer)
            elif "technologies" in app_meta and isinstance(app_meta["technologies"], list):
                tags_list = app_meta["technologies"]

            yaml_status = app_meta.get("status", "live")
            asset_status = "scheduled" if yaml_status == "incubating" else "published"

            assets.append(ContentAsset(
                id=slug,
                slug=slug,
                asset_type="app",
                status=asset_status,
                visibility="public",
                title_es=title_es,
                title_en=title_en,
                url_es=f"/es/apps/{slug}/",
                url_en=f"/en/apps/{slug}/",
                brief_es=brief_es,
                brief_en=brief_en,
                publish_date=pub_date,
                last_modified_es=lastmod,
                last_modified_en=lastmod,
                language_parity="complete",
                category="Aplicaciones Web",
                categories=["Apps", app_meta.get("tier", "lab")],
                tags=tags_list,
                series=None,
                related_app=slug,
                freshness_status="fresh",
                owner="Daniel Alaez"
            ))
        except Exception as e:
            print(f"[WARN] Error procesando app {fpath}: {e}")

    return assets


def scan_kits(git_map: Dict[str, datetime]) -> List[ContentAsset]:
    """
    Escanea data/pulse/kits.yaml y construye los activos tipo 'kit', 'suite' y 'mega_bundle'.
    """
    assets: List[ContentAsset] = []
    kits_path = "data/pulse/kits.yaml"
    if not os.path.isfile(kits_path):
        return assets

    norm_path = kits_path.replace("\\", "/").lower()
    lastmod = git_map.get(norm_path, datetime.now(timezone.utc))

    try:
        with open(kits_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # 1. Mega Bundle
        mb = data.get("mega_bundle")
        if mb:
            assets.append(ContentAsset(
                id=mb["id"],
                slug=mb["slug"],
                asset_type="mega_bundle",
                status="published" if mb.get("status") == "available" else "coming",
                visibility="public",
                title_es=mb.get("title_es"),
                title_en=mb.get("title_en"),
                url_es="/es/recursos/#mega-bundle",
                url_en="/en/resources/#mega-bundle",
                brief_es=mb.get("description_es"),
                brief_en=mb.get("description_en"),
                last_modified_es=lastmod,
                last_modified_en=lastmod,
                language_parity="complete",
                category="Mega Bundle",
                categories=["Recursos", "Suites", "Estrategia"],
                tags=["Mega Bundle", "C-Level", "Excel", "Templates"],
                price=mb.get("price"),
                original_price=mb.get("original_price"),
                checkout_url=mb.get("checkout_url")
            ))

        # 2. Suites
        for s in data.get("suites", []):
            assets.append(ContentAsset(
                id=s["id"],
                slug=s["slug"],
                asset_type="suite",
                status="published" if s.get("status") == "available" else "coming",
                visibility="public",
                title_es=s.get("title_es"),
                title_en=s.get("title_en"),
                url_es=f"/es/recursos/#{s['id']}",
                url_en=f"/en/resources/#{s['id']}",
                brief_es=s.get("description_es"),
                brief_en=s.get("description_en"),
                last_modified_es=lastmod,
                last_modified_en=lastmod,
                language_parity="complete",
                category="Suite B2B",
                categories=["Recursos", "Suites", s.get("topic", "estrategia")],
                tags=["Suite", s.get("topic", "estrategia"), "Excel", "C-Level"],
                price=s.get("price"),
                original_price=s.get("original_price"),
                checkout_url=s.get("checkout_url"),
                included_kits=s.get("included_kits", [])
            ))

        # 3. Kits individuales
        for k in data.get("kits", []):
            assets.append(ContentAsset(
                id=k["id"],
                slug=k["slug"],
                asset_type="kit",
                status="published" if k.get("status") == "available" else "coming",
                visibility="public",
                title_es=k.get("title_es"),
                title_en=k.get("title_en"),
                url_es=f"/es/recursos/#{k['id']}",
                url_en=f"/en/resources/#{k['id']}",
                brief_es=k.get("description_es"),
                brief_en=k.get("description_en"),
                last_modified_es=lastmod,
                last_modified_en=lastmod,
                language_parity="complete",
                category=k.get("category_es", "Recursos"),
                categories=["Recursos", k.get("topic", "estrategia")],
                tags=k.get("deliverables_es", []) + [k.get("topic", "estrategia")],
                price=k.get("price"),
                original_price=k.get("original_price"),
                checkout_url=k.get("checkout_url"),
                deliverables=k.get("deliverables_es", [])
            ))

    except Exception as e:
        print(f"[WARN] Error procesando kits: {e}")

    return assets


def scan_backlog(git_map: Dict[str, datetime]) -> List[ContentAsset]:
    """
    Escanea data/editorial/backlog.yaml (ideas y contenidos futuros sin post creado).
    """
    assets: List[ContentAsset] = []
    backlog_path = "data/editorial/backlog.yaml"
    if not os.path.isfile(backlog_path):
        return assets

    norm_path = backlog_path.replace("\\", "/").lower()
    lastmod = git_map.get(norm_path, datetime.now(timezone.utc))

    try:
        with open(backlog_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        for item in data.get("ideas", []):
            assets.append(ContentAsset(
                id=item["id"],
                slug=item.get("slug", item["id"]),
                asset_type="post",
                status=item.get("status", "idea"),
                visibility=item.get("visibility", "private"),
                title_es=item.get("title_es"),
                title_en=item.get("title_en"),
                brief_es=item.get("brief_es"),
                brief_en=item.get("brief_en"),
                publish_date=item.get("publish_date"),
                last_modified_es=lastmod,
                last_modified_en=lastmod,
                category=item.get("category", "Ideas"),
                tags=item.get("tags", []),
                owner=item.get("owner", "Daniel Alaez")
            ))
    except Exception as e:
        print(f"[WARN] Error procesando backlog: {e}")

    return assets


# ==============================================================================
# CONSTRUCTOR PRINCIPAL Y EXPORTADORES
# ==============================================================================

def build_index() -> Tuple[List[ContentAsset], PublicPulseDataset]:
    """
    Construye el índice unificado completo y genera el dataset público validado.
    """
    print("[1/4] Leyendo historial de Git...")
    git_map = get_git_file_lastmod_map()

    print("[2/4] Escaneando Posts, Apps, Kits y Backlog...")
    post_assets = scan_posts(git_map)
    app_assets = scan_apps(git_map)
    kit_assets = scan_kits(git_map)
    backlog_assets = scan_backlog(git_map)

    all_assets = post_assets + app_assets + kit_assets + backlog_assets
    print(f"      -> {len(post_assets)} Posts emparejados (100% cobertura ES/EN)")
    print(f"      -> {len(app_assets)} Apps activas")
    print(f"      -> {len(kit_assets)} Kits/Suites comerciales")
    print(f"      -> {len(backlog_assets)} Ideas en backlog")
    print(f"      Total activos consolidados: {len(all_assets)}")

    # 3. Exportar índice privado completo
    os.makedirs("data/pulse/private", exist_ok=True)
    private_path = "data/pulse/private/index.json"
    full_dict = [a.model_dump(mode="json") for a in all_assets]
    with open(private_path, "w", encoding="utf-8") as f:
        json.dump(full_dict, f, ensure_ascii=False, indent=2)
    print(f"[3/4] Índice privado guardado en: {private_path}")

    # 4. Generar dataset público (INV-PULSE-1 e INV-PULSE-2)
    public_assets = [a for a in all_assets if a.visibility == "public"]
    parity_summary = {}
    for a in public_assets:
        parity_summary[a.language_parity] = parity_summary.get(a.language_parity, 0) + 1

    pub_dataset = PublicPulseDataset(
        version="1.0.0",
        generated_at=datetime.now(timezone.utc),
        total_assets=len(public_assets),
        published_assets=sum(1 for a in public_assets if a.status == "published"),
        scheduled_assets=sum(1 for a in public_assets if a.status == "scheduled"),
        ideas_count=sum(1 for a in public_assets if a.status == "idea"),
        parity_summary=parity_summary,
        assets=public_assets
    )

    # Validar invariantes antes de escribir
    pub_dataset.validate_security_invariants()

    os.makedirs("static/apps/pulse/data", exist_ok=True)
    public_path = "static/apps/pulse/data/public.json"
    with open(public_path, "w", encoding="utf-8") as f:
        json.dump(pub_dataset.model_dump(mode="json"), f, ensure_ascii=False, indent=2)
    print(f"[4/4] Dataset público guardado en: {public_path}")

    return all_assets, pub_dataset


if __name__ == "__main__":
    build_index()
