"""Transformador universal de Markdown para sindicación omnicanal (SPEC-OPS-AUTOPILOT v2.1.0)."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple
from urllib.parse import urlsplit

import yaml

from autopilot.src.models import (
    SyndicationArtifact,
    SyndicationConfig,
    SyndicationPlatform,
    append_utm_params,
    normalize_syndication_tags,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SITE_BASE_URL = "https://datalaria.com"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/Dalaez/datalaria-website/main"
EMBARGOED_APP_STATUSES = frozenset({"incubating", "draft", "deprecated", "archived"})

_CODE_FENCE_RE = re.compile(r"(^```[^\n]*\n.*?^```|^~~~[^\n]*\n.*?^~~~)", re.MULTILINE | re.DOTALL)
_MERMAID_SHORTCODE_RE = re.compile(
    r"\{\{[<%]\s*mermaid\b([^>%]*)[>%]\}\}(.*?)\{\{[<%]\s*/mermaid\s*[>%]\}\}",
    re.DOTALL | re.IGNORECASE,
)
_APP_REF_RE = re.compile(
    r'\{\{[<%]\s*app-ref\s+(?:slug=)?["\']?([a-zA-Z0-9_-]+)["\']?\s*[>%]\}\}',
    re.IGNORECASE,
)
_HELIX_WAITLIST_RE = re.compile(
    r"\{\{[<%]\s*helix-waitlist\b[^>%]*[>%]\}\}(?:\s*\{\{[<%]\s*/helix-waitlist\s*[>%]\}\})?",
    re.DOTALL | re.IGNORECASE,
)
_PRODUCT_CARD_PAIRED_RE = re.compile(
    r"\{\{[<%]\s*product-card\b(.*?)[>%]\}\}(.*?)\{\{[<%]\s*/product-card\s*[>%]\}\}",
    re.DOTALL | re.IGNORECASE,
)
_PRODUCT_CARD_SINGLE_RE = re.compile(
    r"\{\{[<%]\s*product-card\b(.*?)[>%]\}\}",
    re.DOTALL | re.IGNORECASE,
)
_BUNDLE_CARD_PAIRED_RE = re.compile(
    r"\{\{[<%]\s*bundle-card\b(.*?)[>%]\}\}(.*?)\{\{[<%]\s*/bundle-card\s*[>%]\}\}",
    re.DOTALL | re.IGNORECASE,
)
_BUNDLE_CARD_SINGLE_RE = re.compile(
    r"\{\{[<%]\s*bundle-card\b(.*?)[>%]\}\}",
    re.DOTALL | re.IGNORECASE,
)
_YOUTUBE_RE = re.compile(
    r"\{\{[<%]\s*youtube\b(.*?)[>%]\}\}",
    re.DOTALL | re.IGNORECASE,
)
_BUYMEACOFFEE_RE = re.compile(
    r"\{\{[<%]\s*buymeacoffee\b(.*?)[>%]\}\}",
    re.DOTALL | re.IGNORECASE,
)
_FIGURE_RE = re.compile(
    r"\{\{[<%]\s*figure\b(.*?)[>%]\}\}",
    re.DOTALL | re.IGNORECASE,
)
_STANDALONE_REF_RE = re.compile(
    r'\{\{[<%]\s*(?:ref|relref)\s+["\']([^"\']+)["\']\s*[>%]\}\}',
    re.IGNORECASE,
)
_ATTR_KV_RE = re.compile(r'([a-zA-Z0-9_-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', re.DOTALL)
_MARKDOWN_IMAGE_RE = re.compile(r"!\[(.*?)\]\((.*?)\)")
_MARKDOWN_LINK_RE = re.compile(r"(?<!\!)\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(([^)]+)\)")


def get_app_catalog_entry(
    app_slug: str,
    apps_dir: Optional[Path] = None,
) -> Optional[Dict[str, Any]]:
    """Carga el YAML público de una app desde data/apps/<slug>.yaml."""
    search_dir = apps_dir or (REPO_ROOT / "data" / "apps")
    yaml_path = search_dir / f"{app_slug}.yaml"
    if not yaml_path.is_file():
        return None
    try:
        with open(yaml_path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        return data if isinstance(data, dict) else {}
    except Exception:
        return None


def is_app_status_embargoed(app_data: Optional[Dict[str, Any]]) -> bool:
    """Devuelve True si la app tiene estado embargado (status: incubating/draft/deprecated/archived)."""
    if not app_data:
        return False
    status = str(app_data.get("status", "")).strip().lower()
    return status in EMBARGOED_APP_STATUSES


def _split_target_and_title(raw_target: str) -> Tuple[str, str]:
    """Separa URL/ruta de un título Markdown opcional entre comillas."""
    stripped = raw_target.strip()
    title_match = re.match(r'^(\S+?)\s+(["\'].*["\'])$', stripped)
    if title_match:
        return title_match.group(1), f" {title_match.group(2)}"
    return stripped, ""


def resolve_single_image_ref(
    image_ref: str,
    file_path: str,
    lang: str = "es",
    slug: str = "",
    base_url: str = SITE_BASE_URL,
) -> str:
    """Normaliza una referencia de imagen individual a URL absoluta pública o GitHub Raw."""
    ref = str(image_ref or "").strip()
    if not ref:
        return ""
    if ref.startswith(("http://", "https://")):
        return ref
    if ref.startswith("/"):
        return f"{base_url}{ref}"

    clean_ref = ref.lstrip("./")
    normalized_path = file_path.replace("\\", "/")
    dir_path = os.path.dirname(normalized_path)
    if dir_path:
        return f"{GITHUB_RAW_BASE}/{dir_path}/{clean_ref}"
    if slug and lang in ("es", "en"):
        return f"{GITHUB_RAW_BASE}/content/{lang}/posts/{slug}/{clean_ref}"
    return f"{GITHUB_RAW_BASE}/{clean_ref}"


def resolve_image_urls(
    content: str,
    file_path: str,
    base_url: str = SITE_BASE_URL,
) -> str:
    """Reemplaza imágenes Markdown relativas por URLs absolutas preservando títulos y /images/."""
    normalized_path = file_path.replace("\\", "/")
    dir_path = os.path.dirname(normalized_path)

    def replacer(match: re.Match[str]) -> str:
        alt_text = match.group(1)
        img_path, title_part = _split_target_and_title(match.group(2))
        if img_path.startswith(("http://", "https://")):
            return match.group(0)
        if img_path.startswith("/"):
            return f"![{alt_text}]({base_url}{img_path}{title_part})"
        clean_img_path = img_path.lstrip("./")
        abs_url = (
            f"{GITHUB_RAW_BASE}/{dir_path}/{clean_img_path}"
            if dir_path
            else f"{GITHUB_RAW_BASE}/{clean_img_path}"
        )
        return f"![{alt_text}]({abs_url}{title_part})"

    return _MARKDOWN_IMAGE_RE.sub(replacer, content)


def _resolve_ref_slug(raw_slug: str, lang: str, base_url: str) -> str:
    ref_slug = raw_slug.strip().lstrip("./").lstrip("/")
    if ref_slug.startswith("posts/"):
        ref_slug = ref_slug[len("posts/") :]
    return f"{base_url}/{lang}/posts/{ref_slug.strip('/')}/"


def resolve_markdown_links(
    content: str,
    file_path: str,
    lang: str = "es",
    base_url: str = SITE_BASE_URL,
) -> str:
    """Convierte rutas relativas Markdown [Texto](url) y shortcodes {{< app-ref >}} a URLs absolutas."""
    normalized_path = file_path.replace("\\", "/")
    dir_path = os.path.dirname(normalized_path)
    file_extensions = (".docx", ".pptx", ".pdf", ".xlsx", ".zip", ".csv")

    def resolve_target(target: str) -> str:
        target = target.strip()
        if not target or target.startswith(("#", "mailto:", "tel:", "javascript:")):
            return target
        if target.startswith(("http://", "https://", "//")):
            return target
        if target.startswith("https:www.datalaria.com"):
            return target.replace("https:www.datalaria.com", "https://www.datalaria.com")

        ref_match = _STANDALONE_REF_RE.search(target)
        if ref_match:
            return _resolve_ref_slug(ref_match.group(1), lang=lang, base_url=base_url)

        if any(target.lower().endswith(ext) for ext in file_extensions) and not target.startswith("/"):
            clean_file = target.lstrip("./")
            return f"{GITHUB_RAW_BASE}/{dir_path}/{clean_file}"

        if target.startswith("/"):
            return f"{base_url}{target}"
        if target.startswith(("es/", "en/")):
            return f"{base_url}/{target}"
        if target.startswith("posts/"):
            return f"{base_url}/{lang}/{target}"
        if target.startswith(("apps/", "recursos/", "blog/")):
            return f"{base_url}/{target}"

        clean_target = target.lstrip("./").strip("/")
        return f"{base_url}/{lang}/posts/{clean_target}/"

    def replacer(match: re.Match[str]) -> str:
        label = match.group(1)
        url_part, title_part = _split_target_and_title(match.group(2))
        new_url = resolve_target(url_part)
        return f"[{label}]({new_url}{title_part})"

    content = _MARKDOWN_LINK_RE.sub(replacer, content)

    def app_ref_replacer(match: re.Match[str]) -> str:
        app_slug = match.group(1)
        app_name = app_slug.replace("-", " ").title()
        if lang == "es":
            return (
                f"> 🚀 **App Oficial en Datalaria**: [{app_name}]({base_url}/es/apps/{app_slug}/) "
                f"— [Probar Demo en Vivo]({base_url}/apps/{app_slug}/?mock=true)"
            )
        return (
            f"> 🚀 **Official Datalaria App**: [{app_name}]({base_url}/en/apps/{app_slug}/) "
            f"— [Try Live Demo]({base_url}/apps/{app_slug}/?mock=true)"
        )

    return _APP_REF_RE.sub(app_ref_replacer, content)


def _split_fenced_code_blocks(text: str) -> Tuple[str, List[str]]:
    """Sustituye bloques cercados ```...``` y ~~~...~~~ por tokens temporales para protegerlos."""
    blocks: List[str] = []

    def replacer(match: re.Match[str]) -> str:
        token = f"@@DATALARIA_CODE_BLOCK_{len(blocks)}@@"
        blocks.append(match.group(0))
        return token

    return _CODE_FENCE_RE.sub(replacer, text), blocks


def _restore_fenced_code_blocks(text: str, blocks: List[str]) -> str:
    """Restaura bloques cercados protegidos tras las transformaciones Markdown."""
    restored = text
    for idx, block in enumerate(blocks):
        restored = restored.replace(f"@@DATALARIA_CODE_BLOCK_{idx}@@", block)
    return restored


def _parse_shortcode_attrs(attr_str: str) -> Dict[str, str]:
    """Extrae pares key=value de shortcodes Hugo simples o multilínea."""
    attrs: Dict[str, str] = {}
    for match in _ATTR_KV_RE.finditer(attr_str or ""):
        key = match.group(1).strip().lower()
        val = match.group(2) if match.group(2) is not None else (match.group(3) or "")
        attrs[key] = val.strip()
    return attrs


def _first_positional_arg(attr_str: str) -> str:
    """Obtiene el primer argumento posicional si un shortcode no usa key=value."""
    cleaned = _ATTR_KV_RE.sub("", attr_str or "").strip()
    if not cleaned:
        return ""
    first = cleaned.split()[0].strip("\"'")
    return first


def _render_commercial_card(
    attrs: Dict[str, str],
    inner_body: str,
    lang: Literal["es", "en"],
    kind: Literal["product", "bundle"],
) -> str:
    """Convierte product-card / bundle-card en una tarjeta Markdown universal y limpia."""
    icon = attrs.get("icon", "📦" if kind == "bundle" else "🧰")
    title = attrs.get("title") or (
        "Kit Profesional Datalaria" if lang == "es" else "Datalaria Professional Kit"
    )
    subtitle = attrs.get("subtitle", "")
    price = attrs.get("price", "")
    original_price = attrs.get("original_price", "")
    checkout_url = attrs.get("checkout_url", "")
    guide_url = attrs.get("guide_url", "")
    button_text = attrs.get("button_text") or (
        "Ver Kit Completo" if lang == "es" else "Get the Full Kit"
    )
    items_raw = attrs.get("items", "")

    lines: List[str] = [f"> {icon} **{title}**"]
    if subtitle:
        lines.append(f"> _{subtitle}_")

    if price:
        price_str = f"**{price}**"
        if original_price:
            price_str += f" ~~{original_price}~~"
        price_label = "Precio" if lang == "es" else "Price"
        lines.append(f"> {price_label}: {price_str}")

    if items_raw:
        sep = "|" if "|" in items_raw else (";" if ";" in items_raw else "\n")
        for item in [part.strip(" -\t") for part in items_raw.split(sep)]:
            if item:
                lines.append(f"> - {item}")

    inner_clean = "\n".join(line.strip() for line in inner_body.strip().splitlines() if line.strip())
    if inner_clean:
        lines.append(f"> {inner_clean}")

    ctas: List[str] = []
    if checkout_url:
        ctas.append(f"[{button_text}]({checkout_url})")
    if guide_url:
        guide_label = "Ver guía técnica" if lang == "es" else "Read technical guide"
        ctas.append(f"[{guide_label}]({guide_url})")
    if ctas:
        lines.append("> " + " · ".join(ctas))

    return "\n".join(lines)


def _transform_shortcodes(
    content: str,
    *,
    platform: SyndicationPlatform,
    lang: Literal["es", "en"],
    slug: str,
    apps_dir: Optional[Path] = None,
    base_url: str = SITE_BASE_URL,
) -> str:
    """Transforma los shortcodes Hugo del blog fuera de bloques cercados."""

    def replace_app_ref(match: re.Match[str]) -> str:
        app_slug = match.group(1).strip()
        app_data = get_app_catalog_entry(app_slug, apps_dir=apps_dir)
        resources_path = "es/recursos/" if lang == "es" else "en/resources/"

        if is_app_status_embargoed(app_data):
            resources_url = append_utm_params(
                f"{base_url}/{resources_path}",
                source=platform,
                medium="syndication",
                campaign=slug,
                content=f"embargo_{app_slug}",
            )
            if lang == "es":
                return (
                    f"> 🔒 **Software en acceso anticipado**: Explora herramientas y kits "
                    f"ya disponibles en [Recursos de Datalaria]({resources_url})."
                )
            return (
                f"> 🔒 **Software in early access**: Explore live tools and kits "
                f"available now at [Datalaria Resources]({resources_url})."
            )

        title_map = (app_data or {}).get("title") if isinstance(app_data, dict) else {}
        app_title = (
            (title_map.get(lang) or title_map.get("es") or title_map.get("en"))
            if isinstance(title_map, dict)
            else None
        ) or app_slug.replace("-", " ").title()

        demo_raw = ""
        if isinstance(app_data, dict):
            demo_raw = str(app_data.get("demo_url") or app_data.get("app_url") or "").strip()
        demo_url = (
            demo_raw
            if demo_raw.startswith("http")
            else (f"{base_url}{demo_raw}" if demo_raw else f"{base_url}/apps/{app_slug}/?mock=true")
        )
        info_url = f"{base_url}/{lang}/apps/{app_slug}/"
        if lang == "es":
            return (
                f"> 🚀 **App Oficial en Datalaria**: [{app_title}]({info_url}) "
                f"— [Probar Demo en Vivo]({demo_url})"
            )
        return (
            f"> 🚀 **Official Datalaria App**: [{app_title}]({info_url}) "
            f"— [Try Live Demo]({demo_url})"
        )

    def replace_helix_waitlist(_: re.Match[str]) -> str:
        resources_path = "es/recursos/" if lang == "es" else "en/resources/"
        waitlist_url = append_utm_params(
            f"{base_url}/{resources_path}#software",
            source=platform,
            medium="syndication",
            campaign=slug,
            content="helix_waitlist",
        )
        if lang == "es":
            return (
                "> 🛠️ **Datalaria Helix · Acceso Prioritario**: Próximamente disponible. "
                f"[Únete a la lista prioritaria en Recursos]({waitlist_url})."
            )
        return (
            "> 🛠️ **Datalaria Helix · Priority Access**: Launching soon. "
            f"[Join the priority waitlist on Resources]({waitlist_url})."
        )

    def replace_youtube(match: re.Match[str]) -> str:
        attrs = _parse_shortcode_attrs(match.group(1))
        video_id = attrs.get("id") or _first_positional_arg(match.group(1))
        if not video_id:
            return ""
        alt_text = "Ver vídeo en YouTube" if lang == "es" else "Watch video on YouTube"
        return (
            f"[![{alt_text}](https://img.youtube.com/vi/{video_id}/hqdefault.jpg)]"
            f"(https://www.youtube.com/watch?v={video_id})"
        )

    def replace_buymeacoffee(match: re.Match[str]) -> str:
        attrs = _parse_shortcode_attrs(match.group(1))
        username = attrs.get("username") or attrs.get("user") or _first_positional_arg(match.group(1))
        target_url = attrs.get("url") or (
            f"https://www.buymeacoffee.com/{username}"
            if username
            else f"{base_url}/{lang}/"
        )
        if lang == "es":
            return f"> ☕ ¿Te resultó útil esta arquitectura? [Apoya el proyecto aquí]({target_url})."
        return f"> ☕ Found this architecture useful? [Support the project here]({target_url})."

    def replace_figure(match: re.Match[str]) -> str:
        attrs = _parse_shortcode_attrs(match.group(1))
        src = attrs.get("src", "")
        if not src:
            return ""
        alt = attrs.get("alt") or attrs.get("caption") or attrs.get("title") or "Image"
        return f"![{alt}]({src})"

    transformed = _APP_REF_RE.sub(replace_app_ref, content)
    transformed = _HELIX_WAITLIST_RE.sub(replace_helix_waitlist, transformed)
    transformed = _PRODUCT_CARD_PAIRED_RE.sub(
        lambda m: _render_commercial_card(_parse_shortcode_attrs(m.group(1)), m.group(2), lang, "product"),
        transformed,
    )
    transformed = _PRODUCT_CARD_SINGLE_RE.sub(
        lambda m: _render_commercial_card(_parse_shortcode_attrs(m.group(1)), "", lang, "product"),
        transformed,
    )
    transformed = _BUNDLE_CARD_PAIRED_RE.sub(
        lambda m: _render_commercial_card(_parse_shortcode_attrs(m.group(1)), m.group(2), lang, "bundle"),
        transformed,
    )
    transformed = _BUNDLE_CARD_SINGLE_RE.sub(
        lambda m: _render_commercial_card(_parse_shortcode_attrs(m.group(1)), "", lang, "bundle"),
        transformed,
    )
    transformed = _YOUTUBE_RE.sub(replace_youtube, transformed)
    transformed = _BUYMEACOFFEE_RE.sub(replace_buymeacoffee, transformed)
    transformed = _FIGURE_RE.sub(replace_figure, transformed)
    return transformed


def _inject_syndication_utms(
    content: str,
    *,
    platform: SyndicationPlatform,
    slug: str,
) -> str:
    """Inyecta utm_source/utm_medium/utm_campaign solo en enlaces hacia datalaria.com."""

    def replacer(match: re.Match[str]) -> str:
        label = match.group(1)
        url_part, title_part = _split_target_and_title(match.group(2))
        parsed = urlsplit(url_part)
        netloc = parsed.netloc.lower()
        if parsed.scheme in ("http", "https") and (
            netloc == "datalaria.com" or netloc.endswith(".datalaria.com")
        ):
            tagged_url = append_utm_params(
                url_part,
                source=platform,
                medium="syndication",
                campaign=slug,
            )
            return f"[{label}]({tagged_url}{title_part})"
        return match.group(0)

    return _MARKDOWN_LINK_RE.sub(replacer, content)


def transform_markdown_for_syndication(
    post_content: str,
    file_path: str,
    *,
    platform: SyndicationPlatform,
    lang: Literal["es", "en"],
    slug: str,
    canonical_url: str,
    apps_dir: Optional[Path] = None,
    discussion_question: Optional[str] = None,
    base_url: str = SITE_BASE_URL,
) -> str:
    """Ejecuta el pipeline completo de transformación Hugo -> Markdown estándar con atribución y UTMs."""
    def replace_mermaid(match: re.Match[str]) -> str:
        attrs = _parse_shortcode_attrs(match.group(1))
        diagram_body = match.group(2).strip()
        image_ref = attrs.get("image") or attrs.get("img") or attrs.get("src") or ""
        if image_ref:
            alt_text = (
                attrs.get("alt")
                or attrs.get("title")
                or attrs.get("caption")
                or "Architecture Diagram"
            )
            return f"\n![{alt_text}]({image_ref})\n"
        return f"\n```mermaid\n{diagram_body}\n```\n"

    body = _MERMAID_SHORTCODE_RE.sub(replace_mermaid, post_content or "")
    masked_body, code_blocks = _split_fenced_code_blocks(body)

    masked_body = _transform_shortcodes(
        masked_body,
        platform=platform,
        lang=lang,
        slug=slug,
        apps_dir=apps_dir,
        base_url=base_url,
    )
    masked_body = resolve_image_urls(masked_body, file_path, base_url=base_url)
    masked_body = resolve_markdown_links(masked_body, file_path, lang=lang, base_url=base_url)
    masked_body = _STANDALONE_REF_RE.sub(
        lambda m: _resolve_ref_slug(m.group(1), lang=lang, base_url=base_url),
        masked_body,
    )
    masked_body = _inject_syndication_utms(masked_body, platform=platform, slug=slug)

    final_body = _restore_fenced_code_blocks(masked_body, code_blocks).strip()

    canonical_with_utm = append_utm_params(
        canonical_url,
        source=platform,
        medium="syndication",
        campaign=slug,
        content="canonical_attribution",
    )
    if lang == "en":
        attribution = f"> *Originally published at [Datalaria]({canonical_with_utm}).*\n\n"
    else:
        attribution = f"> *Publicado originalmente en [Datalaria]({canonical_with_utm}).*\n\n"

    if discussion_question and discussion_question.strip():
        heading = "### 💬 Tu turno" if lang == "es" else "### 💬 Over to you"
        footer = f"\n\n---\n\n{heading}\n\n{discussion_question.strip()}\n"
    elif lang == "es":
        footer = (
            f"\n\n---\n\n*¿Preguntas o comentarios sobre esta implementación? "
            f"Únete al debate en el [artículo original en Datalaria]({canonical_with_utm}).*\n"
        )
    else:
        footer = (
            f"\n\n---\n\n*Questions or feedback on this implementation? "
            f"Join the discussion in the [original article on Datalaria]({canonical_with_utm}).*\n"
        )

    return attribution + final_body + footer


def render_dist_markdown(
    artifact: SyndicationArtifact,
    published: bool = True,
) -> str:
    """Serializa el artefacto dist_*.md con frontmatter YAML compatible con Dev.to/CoderLegion."""
    frontmatter_data: Dict[str, Any] = {
        "title": artifact.title,
        "published": published,
        "description": artifact.description,
        "tags": artifact.tags,
        "canonical_url": artifact.canonical_url,
    }
    if artifact.platform == "coderlegion":
        frontmatter_data["source_url"] = artifact.canonical_url
        if artifact.cover_image_url:
            frontmatter_data["cover_image_url"] = artifact.cover_image_url
    else:
        if artifact.cover_image_url:
            frontmatter_data["cover_image"] = artifact.cover_image_url

    yaml_header = yaml.safe_dump(
        frontmatter_data,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    ).strip()
    return f"---\n{yaml_header}\n---\n\n{artifact.markdown.strip()}\n"


def build_syndication_artifact(
    post_content: str,
    file_path: str,
    *,
    platform: SyndicationPlatform,
    lang: Literal["es", "en"],
    slug: str,
    post_title: str,
    canonical_url: str,
    post_meta: Optional[Dict[str, Any]] = None,
    config: Optional[SyndicationConfig] = None,
    cover_image_url: Optional[str] = None,
    apps_dir: Optional[Path] = None,
    output_dir: Optional[Path] = None,
) -> SyndicationArtifact:
    """Construye el SyndicationArtifact y opcionalmente escribe dist_<platform>_<lang>.md."""
    meta = post_meta or {}
    title = config.title.strip() if (config and config.title) else post_title
    description = (
        config.description.strip()
        if (config and config.description)
        else str(meta.get("description") or "").strip()
    )
    effective_canonical = (
        config.canonical_url.strip()
        if (config and config.canonical_url)
        else canonical_url
    )

    resolved_cover = cover_image_url
    if config and config.main_image:
        resolved_cover = resolve_single_image_ref(
            config.main_image,
            file_path,
            lang=lang,
            slug=slug,
        )

    raw_tags: List[str]
    if config and config.tags:
        raw_tags = list(config.tags)
    else:
        meta_tags = meta.get("tags") or meta.get("categories") or []
        raw_tags = list(meta_tags) if isinstance(meta_tags, (list, tuple)) else [str(meta_tags)]

    max_tags = 4 if platform == "devto" else 6
    normalized_tags = normalize_syndication_tags(raw_tags, platform=platform, max_tags=max_tags)

    markdown_body = transform_markdown_for_syndication(
        post_content,
        file_path,
        platform=platform,
        lang=lang,
        slug=slug,
        canonical_url=effective_canonical,
        apps_dir=apps_dir,
        discussion_question=config.discussion_question if config else None,
    )

    artifact = SyndicationArtifact(
        platform=platform,
        lang=lang,
        slug=slug,
        title=title,
        description=description,
        canonical_url=effective_canonical,
        cover_image_url=resolved_cover,
        tags=normalized_tags,
        markdown=markdown_body,
    )

    if output_dir is not None:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        dist_file = out_path / f"dist_{platform}_{lang}.md"
        published_flag = config.published if config else True
        dist_file.write_text(
            render_dist_markdown(artifact, published=published_flag),
            encoding="utf-8",
        )
        artifact.output_path = str(dist_file)

    return artifact
