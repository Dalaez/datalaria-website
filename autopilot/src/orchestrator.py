"""Orquestador principal de Autopilot 2.0 y Sindicación Universal (SPEC-OPS-AUTOPILOT v2.1.0)."""

from __future__ import annotations

import os
import re
import sys
import json
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

import frontmatter
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from autopilot.src import brain
from autopilot.src.markdown_syndicator import (
    GITHUB_RAW_BASE,
    SITE_BASE_URL,
    _APP_REF_RE,
    build_syndication_artifact,
    get_app_catalog_entry,
    is_app_status_embargoed,
    resolve_image_urls,
    resolve_markdown_links,
)
from autopilot.src.models import (
    NewsletterContent,
    SocialPack,
    SocialPackLanguageSection,
    SocialPlatformLinkedIn,
    SocialPlatformX,
    SyndicationArtifact,
    build_x_web_intent_url,
)
from autopilot.src.newsletter_manager import NewsletterManager
from autopilot.src.quality_validator import audit_social_bundle
from autopilot.src.social_manager import SocialMediaManager

CACHE_FILE = "generated_content.json"
DEFAULT_HERO_FALLBACK_URL = f"{SITE_BASE_URL}/images/Datalaria_blog.png"


def _configure_utf8_console() -> None:
    """Evita UnicodeEncodeError en consolas Windows cp1252 al imprimir emojis o acentos."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def save_generated_content(
    twitter_text: str,
    linkedin_text: str,
    newsletter_text: Any = None,
    extra_payload: Optional[Dict[str, Any]] = None,
    cache_file: str = CACHE_FILE,
) -> bool:
    """Guarda el contenido generado por Autopilot en JSON para persistir entre jobs de CI."""
    cache_data: Dict[str, Any] = {
        "twitter": twitter_text,
        "linkedin": linkedin_text,
        "newsletter": newsletter_text,
    }
    if extra_payload:
        cache_data.update(extra_payload)
    try:
        with open(cache_file, "w", encoding="utf-8") as fh:
            json.dump(cache_data, fh, ensure_ascii=False, indent=2)
        print(f"💾 Contenido guardado en {cache_file}")
        return True
    except Exception as exc:
        print(f"⚠️ Error guardando cache: {exc}")
        return False


def load_generated_content(cache_file: str = CACHE_FILE) -> Optional[Dict[str, Any]]:
    """Carga el contenido generado previamente desde generated_content.json."""
    if not os.path.exists(cache_file):
        return None
    try:
        with open(cache_file, "r", encoding="utf-8") as fh:
            cache_data = json.load(fh)
        print(f"📦 Contenido cargado desde cache ({cache_file})")
        return cache_data
    except Exception as exc:
        print(f"⚠️ Error leyendo cache: {exc}")
        return None


def str_to_bool(value: Any) -> bool:
    """Convierte strings de entorno ('true', 'false', '1', '0') a booleano."""
    return str(value).lower() in ("yes", "true", "t", "1")


def _summarize_syndication_artifact(
    artifact: Optional[SyndicationArtifact],
) -> Optional[Dict[str, Any]]:
    """Convierte un SyndicationArtifact en resumen serializable para caché y retorno."""
    if artifact is None:
        return None
    return {
        "platform": artifact.platform,
        "lang": artifact.lang,
        "slug": artifact.slug,
        "title": artifact.title,
        "description": artifact.description,
        "canonical_url": artifact.canonical_url,
        "cover_image_url": artifact.cover_image_url,
        "tags": list(artifact.tags),
        "output_path": artifact.output_path,
        "char_count": len(artifact.markdown),
    }


def load_social_pack(
    file_path: str,
    slug: str,
    lang: Literal["es", "en"] = "es",
) -> Optional[SocialPackLanguageSection]:
    """Busca y valida social_pack.yaml junto al post o en data/editorial/social_packs/."""
    post_dir = Path(file_path).resolve().parent
    candidates = [
        post_dir / "social_pack.yaml",
        post_dir / "social_pack.yml",
        REPO_ROOT / "data" / "editorial" / "social_packs" / f"{slug}.yaml",
        REPO_ROOT / "data" / "editorial" / "social_packs" / f"{slug}.yml",
    ]
    for candidate in candidates:
        if candidate.is_file():
            try:
                with open(candidate, "r", encoding="utf-8") as fh:
                    raw = yaml.safe_load(fh) or {}
                if not isinstance(raw, dict):
                    print(f"⚠️ {candidate} no contiene un mapeo YAML válido.")
                    continue
                pack = SocialPack(**raw)
                return pack.resolve_language(lang)
            except Exception as exc:
                print(f"⚠️ Error validando social_pack en {candidate}: {exc}")
    return None


def _relative_repo_posix(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def resolve_hero_image_url(
    file_path: str,
    post_meta: Dict[str, Any],
    lang: str = "es",
    slug: str = "",
) -> str:
    """Resuelve la imagen Hero clicable (GitHub Raw en bundles o URL pública Datalaria)."""
    cover_meta = post_meta.get("cover")
    image_ref: Optional[str] = None
    if isinstance(cover_meta, dict):
        image_ref = cover_meta.get("image")
    elif isinstance(cover_meta, str):
        image_ref = cover_meta

    if not image_ref:
        image_ref = post_meta.get("image")

    post_dir = Path(file_path).resolve().parent
    if not image_ref:
        for default_name in ("cover.png", "cover.jpg", "cover.jpeg", "cover.webp"):
            if (post_dir / default_name).is_file():
                image_ref = default_name
                break

    if not image_ref:
        return DEFAULT_HERO_FALLBACK_URL

    ref = str(image_ref).strip()
    if ref.startswith(("http://", "https://")):
        return ref
    if ref.startswith("/"):
        return f"{SITE_BASE_URL}{ref}"

    clean_ref = ref.lstrip("./")
    rel_dir = _relative_repo_posix(post_dir)
    if rel_dir.startswith("content/"):
        return f"{GITHUB_RAW_BASE}/{rel_dir}/{clean_ref}"

    if slug and lang in ("es", "en"):
        return f"{GITHUB_RAW_BASE}/content/{lang}/posts/{slug}/{clean_ref}"
    return DEFAULT_HERO_FALLBACK_URL


def resolve_secondary_cta(
    post_content: str,
    lang: str = "es",
    apps_dir: Optional[Path] = None,
) -> Tuple[str, str]:
    """Determina el CTA secundario seguro respetando embargos status: incubating (INV-AUTO-6)."""
    for match in _APP_REF_RE.finditer(post_content or ""):
        app_slug = match.group(1)
        app_data = get_app_catalog_entry(app_slug, apps_dir=apps_dir)
        if not app_data or is_app_status_embargoed(app_data):
            continue

        target_path = str(app_data.get("demo_url") or app_data.get("app_url") or "").strip()
        if not target_path:
            continue
        full_url = target_path if target_path.startswith("http") else f"{SITE_BASE_URL}{target_path}"
        title_map = app_data.get("title") or {}
        app_title = (
            title_map.get(lang)
            or title_map.get("es")
            or app_slug.replace("-", " ").title()
        )
        label = (
            f"Probar Demo Sandbox de {app_title}"
            if lang == "es"
            else f"Try {app_title} Live Sandbox"
        )
        return label, full_url

    if lang == "es":
        return "Explorar Kits y Apps en /recursos/", f"{SITE_BASE_URL}/es/recursos/"
    return "Explore Kits & Apps at /resources/", f"{SITE_BASE_URL}/en/resources/"


def load_post_content(file_path: str) -> Dict[str, Any]:
    """Lee el archivo Markdown y extrae metadatos normalizados calculando idioma, slug y URL."""
    if not os.path.exists(file_path):
        print(f"❌ El archivo no existe: {file_path}")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            post = frontmatter.load(fh)

        norm_path = file_path.replace("\\", "/")
        lang: Literal["es", "en"] = "en" if "/en/" in norm_path else "es"

        filename = os.path.basename(file_path)
        if filename.lower() == "index.md":
            slug = os.path.basename(os.path.dirname(os.path.abspath(file_path)))
        else:
            slug = os.path.splitext(filename)[0]

        url = f"{SITE_BASE_URL}/{lang}/posts/{slug}/"
        return {
            "title": str(post.metadata.get("title", "Sin título")),
            "slug": slug,
            "url": url,
            "content": post.content or "",
            "social_text": post.metadata.get("social_text"),
            "lang": lang,
            "image": post.metadata.get("image"),
            "cover": post.metadata.get("cover"),
            "metadata": dict(post.metadata),
        }
    except Exception as exc:
        print(f"❌ Error leyendo el archivo {file_path}: {exc}")
        sys.exit(1)


def _wrap_x_override(
    raw_override: str,
    title: str,
    content: str,
    lang: str,
    post_url: str,
) -> SocialPlatformX:
    fallback_pack = brain.build_deterministic_fallback_x(
        title=title, content=content, lang=lang, post_url=post_url
    )
    cleaned_hook = re.sub(r"https?://\S+", "", raw_override or "").strip()
    if len(cleaned_hook) < 10:
        return fallback_pack
    return SocialPlatformX(
        hook=cleaned_hook[:195],
        thread=fallback_pack.thread,
        hashtags=fallback_pack.hashtags,
        web_intent_url=build_x_web_intent_url(cleaned_hook[:195], post_url, fallback_pack.hashtags),
    )


def _resolve_local_image_for_legacy(file_path: str, post_meta: Dict[str, Any]) -> Optional[str]:
    cover_meta = post_meta.get("cover", {})
    image_filename: Optional[str] = None
    if isinstance(cover_meta, dict):
        image_filename = cover_meta.get("image")
    elif isinstance(cover_meta, str):
        image_filename = cover_meta
    if not image_filename:
        image_filename = post_meta.get("image")
    if not image_filename:
        return None
    if str(image_filename).startswith("/"):
        candidate = REPO_ROOT / "static" / str(image_filename).lstrip("/")
    else:
        candidate = Path(file_path).resolve().parent / str(image_filename)
    return str(candidate) if candidate.is_file() else None


def run_orchestration(
    file_path: str,
    dry_run: Optional[bool] = None,
    cache_file: str = CACHE_FILE,
    apps_dir: Optional[Path] = None,
    dist_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """Ejecuta el pipeline completo de Autopilot 2.0 y sindicación universal sobre un artículo."""
    print(f"🔍 Analizando archivo: {file_path}")
    post_data = load_post_content(file_path)
    lang: Literal["es", "en"] = post_data["lang"]
    slug: str = post_data["slug"]
    post_url: str = post_data["url"]
    post_title: str = post_data["title"]
    post_content: str = post_data["content"]
    post_meta: Dict[str, Any] = post_data["metadata"]

    print(f"📄 Post cargado: '{post_title}' ({lang})")
    print(f"🔗 URL Calculada: {post_url}")

    is_dry_run = str_to_bool(os.getenv("DRY_RUN", "false")) if dry_run is None else dry_run
    strict_qa = str_to_bool(os.getenv("STRICT_QA", "true"))

    enable_twitter = str_to_bool(os.getenv("ENABLE_TWITTER", "true"))
    enable_linkedin = str_to_bool(os.getenv("ENABLE_LINKEDIN", "true"))
    enable_devto = str_to_bool(os.getenv("ENABLE_DEVTO", "false"))
    enable_coderlegion = str_to_bool(os.getenv("ENABLE_CODERLEGION", "false"))
    coderlegion_langs = [
        item.strip().lower()
        for item in os.getenv("CODERLEGION_LANGS", "en").split(",")
        if item.strip()
    ]
    enable_newsletter = str_to_bool(os.getenv("ENABLE_NEWSLETTER", "false"))
    target_dist_dir = dist_dir if dist_dir is not None else (REPO_ROOT / "autopilot" / "dist" / slug)

    hero_image_url = resolve_hero_image_url(file_path, post_meta, lang=lang, slug=slug)
    sec_label, sec_url = resolve_secondary_cta(post_content, lang=lang, apps_dir=apps_dir)

    # Prioridad 1: social_pack.yaml generado en design-time
    design_pack = load_social_pack(file_path, slug=slug, lang=lang)
    if design_pack is not None:
        print("📦 social_pack.yaml detectado (Prioridad #1 Design-Time).")

    # Prioridad 2: overrides manuales (workflow_dispatch)
    env_twitter = os.getenv("TWITTER_OVERRIDE", "").strip()
    env_linkedin = os.getenv("LINKEDIN_OVERRIDE", "").strip()
    env_newsletter = os.getenv("NEWSLETTER_OVERRIDE", "").strip()

    # Prioridad 3: caché previa en live / frontmatter social_text
    cached = load_generated_content(cache_file=cache_file) if not is_dry_run else None
    frontmatter_social = post_data.get("social_text")

    # --- RESOLVER CANAL X (Coste 0 EUR) ---
    x_pack: Optional[SocialPlatformX] = None
    if enable_twitter:
        if design_pack and design_pack.x is not None:
            x_pack = design_pack.x
            if not x_pack.web_intent_url:
                x_pack.web_intent_url = build_x_web_intent_url(
                    x_pack.hook, post_url, x_pack.hashtags
                )
        elif env_twitter:
            x_pack = _wrap_x_override(env_twitter, post_title, post_content, lang, post_url)
        elif frontmatter_social:
            x_pack = _wrap_x_override(
                str(frontmatter_social), post_title, post_content, lang, post_url
            )
        elif cached and isinstance(cached.get("x"), dict):
            try:
                x_pack = SocialPlatformX(**cached["x"])
            except Exception:
                x_pack = None
        if x_pack is None:
            x_pack = brain.generate_x_thread_pack(
                post_title, post_content, lang=lang, post_url=post_url
            )

    # --- RESOLVER CANAL LINKEDIN ---
    linkedin_text: Optional[str] = None
    if enable_linkedin:
        if design_pack and design_pack.linkedin is not None:
            linkedin_text = design_pack.linkedin.text
        elif env_linkedin:
            linkedin_text = env_linkedin
        elif frontmatter_social:
            linkedin_text = str(frontmatter_social)
        elif cached and cached.get("linkedin"):
            linkedin_text = str(cached["linkedin"])
        else:
            linkedin_text = brain.generate_linkedin_copy(post_title, post_content, lang=lang)

    # --- RESOLVER CANAL NEWSLETTER BREVO 2.0 ---
    newsletter_manager = NewsletterManager()
    newsletter_payload: Optional[NewsletterContent] = None
    newsletter_html: Optional[str] = None

    if enable_newsletter:
        if design_pack and design_pack.newsletter is not None:
            newsletter_payload = design_pack.newsletter
        elif env_newsletter:
            newsletter_payload = newsletter_manager._coerce_newsletter_payload(
                env_newsletter,
                subject=post_title,
                post_title=post_title,
                lang=lang,
                slug=slug,
            )
        elif cached and isinstance(cached.get("newsletter"), dict):
            try:
                newsletter_payload = NewsletterContent(**cached["newsletter"])
            except Exception:
                newsletter_payload = None

        if newsletter_payload is None:
            newsletter_payload = brain.generate_newsletter_payload(
                title=post_title,
                content=post_content,
                slug=slug,
                lang=lang,
                secondary_cta_label=sec_label,
                secondary_cta_url=sec_url,
            )

        if not newsletter_payload.secondary_cta_url:
            newsletter_payload.secondary_cta_url = sec_url
        if not newsletter_payload.secondary_cta_label:
            newsletter_payload.secondary_cta_label = sec_label

        newsletter_html = newsletter_manager._build_html_template(
            newsletter_payload,
            post_title=post_title,
            post_url=post_url,
            lang=lang,
            hero_image_url=hero_image_url,
            slug=slug,
        )

    # --- RESOLVER SINDICACIÓN MARKDOWN (Dev.to + CoderLegion) ---
    devto_cfg = design_pack.devto if design_pack else None
    coderlegion_cfg = design_pack.coderlegion if design_pack else None
    devto_artifact: Optional[SyndicationArtifact] = None
    coderlegion_artifact: Optional[SyndicationArtifact] = None

    if enable_devto and not (devto_cfg and devto_cfg.enabled is False):
        devto_artifact = build_syndication_artifact(
            post_content,
            file_path,
            platform="devto",
            lang=lang,
            slug=slug,
            post_title=post_title,
            canonical_url=post_url,
            post_meta=post_meta,
            config=devto_cfg,
            cover_image_url=hero_image_url,
            apps_dir=apps_dir,
            output_dir=target_dist_dir,
        )

    if enable_coderlegion and not (coderlegion_cfg and coderlegion_cfg.enabled is False):
        if lang in coderlegion_langs:
            coderlegion_artifact = build_syndication_artifact(
                post_content,
                file_path,
                platform="coderlegion",
                lang=lang,
                slug=slug,
                post_title=post_title,
                canonical_url=post_url,
                post_meta=post_meta,
                config=coderlegion_cfg,
                cover_image_url=hero_image_url,
                apps_dir=apps_dir,
                output_dir=target_dist_dir,
            )
        else:
            print(
                f"🔕 CoderLegion omitido para idioma '{lang}' (CODERLEGION_LANGS={coderlegion_langs})"
            )

    # --- ASSURANCE QA GATE INTEGRADO ---
    audit_report = audit_social_bundle(
        x_pack=x_pack,
        linkedin_text=linkedin_text,
        newsletter_payload=newsletter_payload,
        newsletter_html=newsletter_html,
        post_url=post_url,
        devto_artifact=devto_artifact,
        coderlegion_artifact=coderlegion_artifact,
    )
    print(f"🛡️ Quality Gate Autopilot 2.0: {audit_report.overall_status}")
    for channel_name, res in audit_report.results.items():
        if res.issues:
            summary_msgs = "; ".join(f"{i.code}: {i.message}" for i in res.issues)
            print(f"   ⚠️ [{channel_name}] {res.status} -> {summary_msgs}")

    x_summary: Optional[Dict[str, Any]] = None
    if x_pack is not None:
        x_summary = {
            "mode": "zero_cost_intent",
            "hook": x_pack.hook,
            "hashtags": x_pack.hashtags,
            "web_intent_url": x_pack.web_intent_url
            or build_x_web_intent_url(x_pack.hook, post_url, x_pack.hashtags),
            "thread": x_pack.thread,
        }

    nl_summary: Optional[Dict[str, Any]] = None
    if newsletter_payload is not None:
        nl_summary = {
            "archetype": newsletter_payload.archetype,
            "subject": newsletter_payload.subject,
            "preheader": newsletter_payload.preheader,
            "hook_paragraphs": newsletter_payload.hook_paragraphs,
            "insights_60s": newsletter_payload.insights_60s,
            "hero_image_url": hero_image_url,
            "secondary_cta_label": newsletter_payload.secondary_cta_label,
            "secondary_cta_url": newsletter_payload.secondary_cta_url,
            "ps_referral_text": newsletter_payload.ps_referral_text,
            "list_id": newsletter_manager._get_list_id(lang),
        }

    devto_summary = _summarize_syndication_artifact(devto_artifact)
    coderlegion_summary = _summarize_syndication_artifact(coderlegion_artifact)
    dist_files = [
        item["output_path"]
        for item in (devto_summary, coderlegion_summary)
        if item and item.get("output_path")
    ]
    audit_dict = audit_report.model_dump()

    if is_dry_run:
        save_generated_content(
            twitter_text=x_pack.hook if x_pack else "",
            linkedin_text=linkedin_text or "",
            newsletter_text=nl_summary,
            extra_payload={
                "post_url": post_url,
                "lang": lang,
                "slug": slug,
                "x": x_summary,
                "devto": devto_summary,
                "coderlegion": coderlegion_summary,
                "dist_files": dist_files,
                "audit_report": audit_dict,
            },
            cache_file=cache_file,
        )

        print("\n🚧 --- DRY RUN MODE (Autopilot 2.0 Preview) --- 🚧")
        if enable_twitter and x_pack is not None:
            SocialMediaManager().prepare_x_zero_cost(x_pack, post_url=post_url)
        if enable_linkedin and linkedin_text:
            print(f"\n💼 [LINKEDIN]:\n{linkedin_text}")
        if devto_artifact is not None:
            print(
                f"\n🦄 [DEV.TO Preview] tags={devto_artifact.tags} -> {devto_artifact.output_path}\n"
                f"{devto_artifact.markdown[:500]}...\n"
            )
        if coderlegion_artifact is not None:
            print(
                f"\n🛡️ [CODERLEGION Preview] source_url={coderlegion_artifact.canonical_url} "
                f"tags={coderlegion_artifact.tags} -> {coderlegion_artifact.output_path}\n"
                f"{coderlegion_artifact.markdown[:500]}...\n"
            )
        if enable_newsletter and newsletter_payload is not None:
            newsletter_manager.preview_campaign(
                subject=newsletter_payload.subject,
                intro_text=newsletter_payload,
                post_title=post_title,
                post_url=post_url,
                lang=lang,
                hero_image_url=hero_image_url,
                slug=slug,
            )

        return {
            "dry_run": True,
            "post_url": post_url,
            "slug": slug,
            "lang": lang,
            "hero_image_url": hero_image_url,
            "secondary_cta": {"label": sec_label, "url": sec_url},
            "x": x_summary,
            "linkedin": linkedin_text,
            "newsletter": nl_summary,
            "newsletter_html": newsletter_html,
            "devto": devto_summary,
            "coderlegion": coderlegion_summary,
            "dist_files": dist_files,
            "audit_report": audit_dict,
        }

    # --- LIVE MODE ---
    print("\n🚀 --- LIVE MODE (Autopilot 2.0 Dispatch) --- 🚀")
    manager = SocialMediaManager()
    local_img = _resolve_local_image_for_legacy(file_path, post_meta)

    if enable_twitter and x_pack is not None:
        x_audit = audit_report.results.get("x")
        if strict_qa and x_audit and x_audit.status == "FAIL":
            print(f"⛔ Envío X bloqueado por Quality Gate: {[i.code for i in x_audit.issues]}")
        else:
            manager.post_to_twitter(
                text=x_pack.hook, url=post_url, image_path=local_img, x_pack=x_pack
            )
    else:
        print("🔕 Twitter omitido (ENABLE_TWITTER=false)")

    if enable_linkedin and linkedin_text:
        li_audit = audit_report.results.get("linkedin")
        if strict_qa and li_audit and li_audit.status == "FAIL":
            print(
                f"⛔ Envío LinkedIn bloqueado por Quality Gate: {[i.code for i in li_audit.issues]}"
            )
        else:
            manager.post_to_linkedin(text=linkedin_text, url=post_url)
    else:
        print("🔕 LinkedIn omitido (ENABLE_LINKEDIN=false)")

    if devto_artifact is not None:
        devto_audit = audit_report.results.get("devto")
        if strict_qa and devto_audit and devto_audit.status == "FAIL":
            print(
                f"⛔ Envío Dev.to bloqueado por Quality Gate: {[i.code for i in devto_audit.issues]}"
            )
        else:
            manager.post_to_devto(
                title=devto_artifact.title,
                content_markdown=devto_artifact.markdown,
                canonical_url=devto_artifact.canonical_url,
                main_image=devto_artifact.cover_image_url,
                tags=devto_artifact.tags,
                description=devto_artifact.description or None,
                published=devto_cfg.published if devto_cfg else True,
            )
    else:
        print("🔕 Dev.to omitido (ENABLE_DEVTO=false o deshabilitado en social_pack)")

    if coderlegion_artifact is not None:
        cl_audit = audit_report.results.get("coderlegion")
        if strict_qa and cl_audit and cl_audit.status == "FAIL":
            print(
                f"⛔ Envío CoderLegion bloqueado por Quality Gate: {[i.code for i in cl_audit.issues]}"
            )
        else:
            manager.post_to_coderlegion(
                title=coderlegion_artifact.title,
                content_markdown=coderlegion_artifact.markdown,
                canonical_url=coderlegion_artifact.canonical_url,
                cover_image_url=coderlegion_artifact.cover_image_url,
                tags=coderlegion_artifact.tags,
                description=coderlegion_artifact.description or None,
                category_id=coderlegion_cfg.category if coderlegion_cfg else None,
            )
    else:
        print("🔕 CoderLegion omitido (ENABLE_CODERLEGION=false, idioma excluido o deshabilitado)")

    if enable_newsletter and newsletter_payload is not None:
        nl_audit = audit_report.results.get("newsletter")
        if strict_qa and nl_audit and nl_audit.status == "FAIL":
            print(
                f"⛔ Envío Brevo bloqueado por Quality Gate: {[i.code for i in nl_audit.issues]}"
            )
        else:
            newsletter_manager.send_campaign(
                subject=newsletter_payload.subject,
                intro_text=newsletter_payload,
                post_title=post_title,
                post_url=post_url,
                lang=lang,
                hero_image_url=hero_image_url,
                slug=slug,
            )
    else:
        print("🔕 Newsletter omitida (ENABLE_NEWSLETTER=false)")

    print("\n✅ Orquestación finalizada.")
    return {
        "dry_run": False,
        "post_url": post_url,
        "slug": slug,
        "lang": lang,
        "hero_image_url": hero_image_url,
        "secondary_cta": {"label": sec_label, "url": sec_url},
        "x": x_summary,
        "linkedin": linkedin_text,
        "newsletter": nl_summary,
        "newsletter_html": newsletter_html,
        "devto": devto_summary,
        "coderlegion": coderlegion_summary,
        "dist_files": dist_files,
        "audit_report": audit_dict,
    }


def main() -> None:
    _configure_utf8_console()
    if len(sys.argv) < 2:
        print("❌ Uso: python orchestrator.py <ruta_al_post.md>")
        sys.exit(1)
    run_orchestration(sys.argv[1])


if __name__ == "__main__":
    main()
