"""Contratos Pydantic v2 y músculo determinista de Autopilot 2.0 (SPEC-OPS-AUTOPILOT)."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator

SubjectArchetype = Literal[
    "counterintuitive_question",
    "real_case_number",
    "invisible_error",
    "architecture_inside",
    "direct_framework",
]

SUBJECT_ARCHETYPES: Tuple[SubjectArchetype, ...] = (
    "counterintuitive_question",
    "real_case_number",
    "invisible_error",
    "architecture_inside",
    "direct_framework",
)

ROBOTIC_SUBJECT_PREFIXES: Tuple[str, ...] = (
    "🚀 nuevo en datalaria:",
    "nuevo en datalaria:",
    "🚀 new on datalaria:",
    "new on datalaria:",
)

X_WEB_INTENT_BASE = "https://x.com/intent/tweet"
_URL_REGEX = re.compile(r"https?://\S+")


def count_twitter_weighted_length(text: str) -> int:
    """Calcula la longitud ponderada oficial de X/Twitter.

    - Cualquier URL (http/https) cuenta como 23 caracteres (t.co).
    - Caracteres fuera del plano BMP (ord > 0xFFFF, ej. emojis) cuentan como 2.
    - El resto de caracteres cuentan como 1.
    """
    if not text:
        return 0
    normalized = _URL_REGEX.sub("x" * 23, text)
    return sum(2 if ord(ch) > 0xFFFF else 1 for ch in normalized)


def build_x_web_intent_url(
    text: str,
    url: str,
    hashtags: Optional[List[str]] = None,
) -> str:
    """Construye una URL oficial 1-clic de X Web Intent sin llamadas a API de pago."""
    params: Dict[str, str] = {"text": (text or "").strip()}
    if url:
        params["url"] = url.strip()
    if hashtags:
        cleaned = [tag.lstrip("#").strip() for tag in hashtags if tag and tag.lstrip("#").strip()]
        if cleaned:
            params["hashtags"] = ",".join(cleaned)
    return f"{X_WEB_INTENT_BASE}?{urlencode(params)}"


def select_subject_archetype(
    slug: str,
    explicit_archetype: Optional[str] = None,
) -> SubjectArchetype:
    """Selecciona de forma 100 % determinista uno de los 5 arquetipos de asunto de E05."""
    if explicit_archetype and explicit_archetype in SUBJECT_ARCHETYPES:
        return explicit_archetype  # type: ignore[return-value]
    seed = (slug or "datalaria").strip().encode("utf-8")
    digest = int(hashlib.sha256(seed).hexdigest(), 16)
    return SUBJECT_ARCHETYPES[digest % len(SUBJECT_ARCHETYPES)]


def append_utm_params(
    url: str,
    source: str = "newsletter",
    medium: str = "email",
    campaign: Optional[str] = None,
    content: Optional[str] = None,
) -> str:
    """Inyecta parámetros UTM respetando query params previos y fragmentos HashRouter (#/...)."""
    if not url:
        return url
    parts = urlsplit(url.strip())
    query_pairs = dict(parse_qsl(parts.query, keep_blank_values=True))
    query_pairs["utm_source"] = source
    query_pairs["utm_medium"] = medium
    if campaign:
        query_pairs["utm_campaign"] = campaign
    if content:
        query_pairs["utm_content"] = content
    encoded_query = urlencode(list(query_pairs.items()))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, encoded_query, parts.fragment))


class NewsletterContent(BaseModel):
    """Contrato estructurado para Brevo Newsletter 2.0 Anti-Churn (E05 + INV-AUTO-2)."""

    model_config = ConfigDict(extra="ignore")

    archetype: SubjectArchetype
    subject: str = Field(min_length=25, max_length=110)
    preheader: str = Field(min_length=35, max_length=160)
    hook_paragraphs: List[str] = Field(min_length=1, max_length=4)
    insights_60s: List[str] = Field(min_length=3, max_length=3)
    secondary_cta_label: Optional[str] = None
    secondary_cta_url: Optional[str] = None
    ps_referral_text: Optional[str] = None

    @field_validator("subject")
    @classmethod
    def _reject_robotic_subject_prefix(cls, value: str) -> str:
        cleaned = value.strip()
        lowered = cleaned.lower()
        for prefix in ROBOTIC_SUBJECT_PREFIXES:
            if lowered.startswith(prefix):
                raise ValueError(
                    f"Asunto rechazado por INV-AUTO-2 (prefijo robótico '{prefix}'): {cleaned}"
                )
        return cleaned

    @field_validator("preheader")
    @classmethod
    def _strip_preheader(cls, value: str) -> str:
        return value.strip()

    @field_validator("hook_paragraphs")
    @classmethod
    def _validate_hooks(cls, paragraphs: List[str]) -> List[str]:
        cleaned = [p.strip() for p in paragraphs if p and p.strip()]
        if not cleaned:
            raise ValueError("hook_paragraphs debe contener al menos 1 párrafo no vacío.")
        return cleaned

    @field_validator("insights_60s")
    @classmethod
    def _validate_insights(cls, items: List[str]) -> List[str]:
        cleaned = [item.strip() for item in items if item and item.strip()]
        if len(cleaned) != 3:
            raise ValueError("insights_60s debe contener exactamente 3 insights no vacíos.")
        return cleaned


class SocialPlatformX(BaseModel):
    """Paquete de publicación X/Twitter a coste 0 EUR (Web Intent + hilo de 4-6 tweets)."""

    model_config = ConfigDict(extra="ignore")

    hook: str = Field(min_length=10)
    thread: List[str] = Field(min_length=4, max_length=6)
    hashtags: List[str] = Field(default_factory=list)
    web_intent_url: Optional[str] = None

    @field_validator("hook")
    @classmethod
    def _clean_hook(cls, value: str) -> str:
        return value.strip()

    @field_validator("thread")
    @classmethod
    def _clean_thread(cls, tweets: List[str]) -> List[str]:
        cleaned = [t.strip() for t in tweets if t and t.strip()]
        if not (4 <= len(cleaned) <= 6):
            raise ValueError("El hilo de X debe tener entre 4 y 6 tweets.")
        return cleaned


class SocialPlatformLinkedIn(BaseModel):
    """Paquete estructurado para LinkedIn estilo Broetry (E06)."""

    model_config = ConfigDict(extra="ignore")

    text: str = Field(min_length=30, max_length=3000)
    hashtags: List[str] = Field(default_factory=list)

    @field_validator("text")
    @classmethod
    def _clean_text(cls, value: str) -> str:
        return value.strip()


class SyndicationConfig(BaseModel):
    """Configuración opcional por canal de sindicación dentro de social_pack.yaml."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    enabled: Optional[bool] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    canonical_url: Optional[str] = None
    main_image: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("main_image", "cover_image_url"),
    )
    discussion_question: Optional[str] = None
    published: bool = True
    category: Optional[Union[str, int]] = None


SyndicationPlatform = Literal["devto", "coderlegion"]


def normalize_syndication_tags(
    tags: Optional[List[str]],
    platform: SyndicationPlatform = "devto",
    max_tags: int = 4,
) -> List[str]:
    """Normaliza etiquetas según restricciones estrictas de Dev.to y CoderLegion."""
    if not tags or max_tags <= 0:
        return []

    normalized: List[str] = []
    seen = set()
    for raw in tags:
        text = unicodedata.normalize("NFKD", str(raw or "")).encode("ascii", "ignore").decode("ascii").lower().strip()
        if not text:
            continue
        if platform == "devto":
            token = re.sub(r"[^a-z0-9]", "", text)[:30]
        else:
            token = re.sub(r"[\s_]+", "-", text)
            token = re.sub(r"[^a-z0-9-]", "", token)
            token = re.sub(r"-{2,}", "-", token).strip("-")[:30]
        if not token or token in seen:
            continue
        seen.add(token)
        normalized.append(token)
        if len(normalized) >= max_tags:
            break
    return normalized


class SyndicationArtifact(BaseModel):
    """Artefacto Markdown listo para publicar y guardar en autopilot/dist/."""

    model_config = ConfigDict(extra="ignore")

    platform: SyndicationPlatform
    lang: Literal["es", "en"]
    slug: str
    title: str
    description: str = ""
    canonical_url: str
    cover_image_url: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    markdown: str
    output_path: Optional[str] = None


class SocialPackLanguageSection(BaseModel):
    """Sección de un idioma dentro de social_pack.yaml (Autopilot 2.0 + Hito 7.4)."""

    model_config = ConfigDict(extra="ignore")

    x: Optional[SocialPlatformX] = None
    linkedin: Optional[SocialPlatformLinkedIn] = None
    newsletter: Optional[NewsletterContent] = None
    devto: Optional[SyndicationConfig] = None
    coderlegion: Optional[SyndicationConfig] = None


class SocialPack(BaseModel):
    """Contrato raíz para social_pack.yaml generado en design-time por E06/E05."""

    model_config = ConfigDict(extra="ignore")

    es: Optional[SocialPackLanguageSection] = None
    en: Optional[SocialPackLanguageSection] = None
    x: Optional[SocialPlatformX] = None
    linkedin: Optional[SocialPlatformLinkedIn] = None
    newsletter: Optional[NewsletterContent] = None
    devto: Optional[SyndicationConfig] = None
    coderlegion: Optional[SyndicationConfig] = None

    def resolve_language(self, lang: Literal["es", "en"]) -> SocialPackLanguageSection:
        """Devuelve la sección del idioma solicitado o hace fallback a campos raíz monolingües."""
        section = self.es if lang == "es" else self.en
        if section is not None:
            return section
        return SocialPackLanguageSection(
            x=self.x,
            linkedin=self.linkedin,
            newsletter=self.newsletter,
            devto=self.devto,
            coderlegion=self.coderlegion,
        )


class QualityIssue(BaseModel):
    """Incidencia individual detectada por quality_validator."""

    code: str
    severity: Literal["error", "warning"]
    message: str
    field: Optional[str] = None


class PlatformAuditResult(BaseModel):
    """Resultado de auditoría determinista para una plataforma."""

    platform: Literal["x", "linkedin", "newsletter", "devto", "coderlegion"]
    status: Literal["PASS", "WARN", "FAIL"]
    issues: List[QualityIssue] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)


class QualityAuditReport(BaseModel):
    """Dictamen agregado del Verification Gate editorial/social de Autopilot 2.0."""

    overall_status: Literal["PASS", "WARN", "FAIL"]
    results: Dict[str, PlatformAuditResult] = Field(default_factory=dict)
