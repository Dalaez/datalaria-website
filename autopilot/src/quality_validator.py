"""Validador determinista de calidad social y Brevo 2.0 (sustituye a gh copilot / ctrl)."""

from __future__ import annotations

import html
import re
from typing import Dict, List, Optional

from autopilot.src.models import (
    ROBOTIC_SUBJECT_PREFIXES,
    SUBJECT_ARCHETYPES,
    X_WEB_INTENT_BASE,
    NewsletterContent,
    PlatformAuditResult,
    QualityAuditReport,
    QualityIssue,
    SocialPlatformX,
    SyndicationArtifact,
    count_twitter_weighted_length,
)

_URL_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)
_FENCED_CODE_BLOCK_RE = re.compile(
    r"(^```[^\n]*\n.*?^```|^~~~[^\n]*\n.*?^~~~)",
    re.MULTILINE | re.DOTALL,
)
_SYNDICATION_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
_SYNDICATION_LINK_RE = re.compile(r"(?<!\!)\[(?:[^\[\]]|\[[^\[\]]*\])*\]\(([^)]+)\)")
_DEVTO_TAG_RE = re.compile(r"^[a-z0-9]{1,30}$")
_GREETING_SIGNOFF_PATTERN = re.compile(
    r"^(hola|hi|hello|hey|un abrazo|saludos|best regards|kind regards|regards)\b",
    re.IGNORECASE,
)
_MID_SENTENCE_EMOJI_PATTERN = re.compile(
    r"[A-Za-zÀ-ÿ0-9]\s*[\U00010000-\U0010FFFF]\s*[A-Za-zÀ-ÿ0-9]"
)
_IMG_TAG_PATTERN = re.compile(r"<img\b([^>]*)>", re.IGNORECASE)


def _compute_status(issues: List[QualityIssue]) -> str:
    if any(issue.severity == "error" for issue in issues):
        return "FAIL"
    if any(issue.severity == "warning" for issue in issues):
        return "WARN"
    return "PASS"


def audit_x_pack(x_pack: SocialPlatformX, post_url: str = "") -> PlatformAuditResult:
    """Audita el paquete X/Twitter de coste 0 EUR bajo las reglas de E06 y E07."""
    issues: List[QualityIssue] = []
    hook = (x_pack.hook or "").strip()
    hook_len = count_twitter_weighted_length(hook)

    if not hook:
        issues.append(
            QualityIssue(
                code="X_HOOK_EMPTY",
                severity="error",
                message="El gancho de X no puede estar vacío.",
                field="hook",
            )
        )
    if _URL_PATTERN.search(hook):
        issues.append(
            QualityIssue(
                code="X_URL_IN_HOOK",
                severity="error",
                message="El gancho de X no debe incluir URLs dentro del cuerpo (INV E06/E07).",
                field="hook",
            )
        )
    if hook.endswith("...") or hook.endswith("…"):
        issues.append(
            QualityIssue(
                code="X_HOOK_TRUNCATED",
                severity="error",
                message="El gancho de X parece truncado abruptamente con puntos suspensivos.",
                field="hook",
            )
        )
    if hook_len >= 200:
        issues.append(
            QualityIssue(
                code="X_HOOK_OVER_200",
                severity="error",
                message=f"Gancho X excede 200 caracteres ponderados ({hook_len}).",
                field="hook",
            )
        )

    thread = x_pack.thread or []
    if not (4 <= len(thread) <= 6):
        issues.append(
            QualityIssue(
                code="X_THREAD_SIZE_INVALID",
                severity="error",
                message=f"El hilo de X debe tener entre 4 y 6 tweets (recibidos: {len(thread)}).",
                field="thread",
            )
        )

    tweet_lengths: List[int] = []
    for idx, tweet in enumerate(thread, start=1):
        wlen = count_twitter_weighted_length(tweet)
        tweet_lengths.append(wlen)
        if wlen == 0 or wlen > 280:
            issues.append(
                QualityIssue(
                    code="X_TWEET_OVER_280",
                    severity="error",
                    message=f"Tweet {idx} del hilo incumple (0 < len <= 280): {wlen} chars ponderados.",
                    field=f"thread[{idx - 1}]",
                )
            )

    intent_url = (x_pack.web_intent_url or "").strip()
    if not intent_url.startswith(f"{X_WEB_INTENT_BASE}?"):
        issues.append(
            QualityIssue(
                code="X_WEB_INTENT_MISSING",
                severity="error",
                message="Falta web_intent_url oficial de X (https://x.com/intent/tweet?...).",
                field="web_intent_url",
            )
        )
    elif post_url and "url=" not in intent_url:
        issues.append(
            QualityIssue(
                code="X_WEB_INTENT_NO_POST_URL",
                severity="warning",
                message="La URL X Web Intent no incluye parámetro url= explícito.",
                field="web_intent_url",
            )
        )

    return PlatformAuditResult(
        platform="x",
        status=_compute_status(issues),  # type: ignore[arg-type]
        issues=issues,
        metrics={
            "hook_weighted_length": hook_len,
            "thread_count": len(thread),
            "tweet_weighted_lengths": tweet_lengths,
            "has_web_intent": intent_url.startswith(f"{X_WEB_INTENT_BASE}?"),
        },
    )


def audit_linkedin_post(text: str) -> PlatformAuditResult:
    """Audita el formato Broetry y reglas editoriales de E06/E07 para LinkedIn."""
    issues: List[QualityIssue] = []
    cleaned = (text or "").strip()

    if not cleaned:
        issues.append(
            QualityIssue(
                code="LINKEDIN_EMPTY",
                severity="error",
                message="El texto de LinkedIn no puede estar vacío.",
                field="text",
            )
        )
        return PlatformAuditResult(
            platform="linkedin",
            status="FAIL",
            issues=issues,
            metrics={"char_count": 0, "paragraph_count": 0},
        )

    if len(cleaned) > 3000:
        issues.append(
            QualityIssue(
                code="LINKEDIN_OVER_3000",
                severity="error",
                message=f"El post de LinkedIn supera el límite de 3000 caracteres ({len(cleaned)}).",
                field="text",
            )
        )

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", cleaned) if p.strip()]
    if len(paragraphs) < 3:
        issues.append(
            QualityIssue(
                code="LINKEDIN_BROETRY_PARAGRAPHS",
                severity="error",
                message=f"LinkedIn requiere al menos 3 párrafos separados por doble salto (detectados: {len(paragraphs)}).",
                field="text",
            )
        )

    max_lines_per_paragraph = 0
    for idx, paragraph in enumerate(paragraphs, start=1):
        lines = [ln for ln in paragraph.splitlines() if ln.strip()]
        max_lines_per_paragraph = max(max_lines_per_paragraph, len(lines))
        if len(paragraph) > 450:
            issues.append(
                QualityIssue(
                    code="LINKEDIN_WALL_OF_TEXT",
                    severity="error",
                    message=f"Párrafo {idx} forma un muro de texto (>450 caracteres sin doble salto).",
                    field="text",
                )
            )
        elif len(lines) > 3:
            issues.append(
                QualityIssue(
                    code="LINKEDIN_PARAGRAPH_OVER_3_LINES",
                    severity="warning",
                    message=f"Párrafo {idx} supera las 3 líneas recomendadas por Broetry ({len(lines)}).",
                    field="text",
                )
            )

    if "?" not in paragraphs[-1]:
        issues.append(
            QualityIssue(
                code="LINKEDIN_MISSING_QUESTION",
                severity="error",
                message="El último párrafo de LinkedIn debe cerrar con una pregunta de debate (?).",
                field="text",
            )
        )

    for line_no, line in enumerate(cleaned.splitlines(), start=1):
        if _MID_SENTENCE_EMOJI_PATTERN.search(line):
            issues.append(
                QualityIssue(
                    code="LINKEDIN_MID_SENTENCE_EMOJI",
                    severity="error",
                    message=f"Emoji incrustado en mitad de frase en línea {line_no}; usar solo como viñeta o cierre.",
                    field="text",
                )
            )

    return PlatformAuditResult(
        platform="linkedin",
        status=_compute_status(issues),  # type: ignore[arg-type]
        issues=issues,
        metrics={
            "char_count": len(cleaned),
            "paragraph_count": len(paragraphs),
            "max_lines_per_paragraph": max_lines_per_paragraph,
        },
    )


def _extract_visible_text(html_content: str) -> str:
    without_blocks = re.sub(
        r"<(style|script|head)\b[^>]*>.*?</\1>",
        " ",
        html_content,
        flags=re.IGNORECASE | re.DOTALL,
    )
    without_comments = re.sub(r"<!--.*?-->", " ", without_blocks, flags=re.DOTALL)
    without_tags = re.sub(r"<[^>]+>", " ", without_comments)
    unescaped = html.unescape(without_tags)
    return re.sub(r"\s+", " ", unescaped).strip()


def audit_newsletter_payload(
    payload: NewsletterContent,
    html_content: Optional[str] = None,
) -> PlatformAuditResult:
    """Audita contrato Brevo 2.0 Anti-Churn (asunto, 60s insights y HTML anti-spam)."""
    issues: List[QualityIssue] = []

    subject = (payload.subject or "").strip()
    lowered_subject = subject.lower()
    if any(lowered_subject.startswith(prefix) for prefix in ROBOTIC_SUBJECT_PREFIXES):
        issues.append(
            QualityIssue(
                code="NEWSLETTER_ROBOTIC_SUBJECT",
                severity="error",
                message="Asunto rechazado por INV-AUTO-2: contiene prefijo robótico prohibido.",
                field="subject",
            )
        )
    if not (25 <= len(subject) <= 110):
        issues.append(
            QualityIssue(
                code="NEWSLETTER_SUBJECT_BOUNDS",
                severity="error",
                message=f"Longitud de asunto fuera de [25, 110] caracteres ({len(subject)}).",
                field="subject",
            )
        )
    if payload.archetype not in SUBJECT_ARCHETYPES:
        issues.append(
            QualityIssue(
                code="NEWSLETTER_INVALID_ARCHETYPE",
                severity="error",
                message=f"Arquetipo de asunto desconocido: {payload.archetype}",
                field="archetype",
            )
        )

    if len(payload.insights_60s) != 3 or any(len(i.strip()) < 10 for i in payload.insights_60s):
        issues.append(
            QualityIssue(
                code="NEWSLETTER_INSIGHTS_INVALID",
                severity="error",
                message="insights_60s debe contener exactamente 3 aprendizajes concretos (>=10 chars c/u).",
                field="insights_60s",
            )
        )

    for idx, paragraph in enumerate(payload.hook_paragraphs, start=1):
        if _GREETING_SIGNOFF_PATTERN.search(paragraph.strip()):
            issues.append(
                QualityIssue(
                    code="NEWSLETTER_REDUNDANT_GREETING",
                    severity="error",
                    message=f"hook_paragraphs[{idx - 1}] contiene saludo o despedida redundante; la plantilla lo añade automáticamente.",
                    field="hook_paragraphs",
                )
            )

    metrics: Dict[str, object] = {
        "subject_length": len(subject),
        "archetype": payload.archetype,
        "insights_count": len(payload.insights_60s),
    }

    if html_content is not None:
        img_matches = _IMG_TAG_PATTERN.findall(html_content)
        img_count = len(img_matches)
        metrics["img_count"] = img_count
        if img_count != 1:
            issues.append(
                QualityIssue(
                    code="NEWSLETTER_HTML_IMG_COUNT",
                    severity="error",
                    message=f"Brevo 2.0 exige exactamente 1 imagen Hero clicable en el HTML (encontradas: {img_count}).",
                    field="html_content",
                )
            )
        else:
            img_attrs = img_matches[0].lower()
            if "max-width: 560px" not in img_attrs or "border-radius: 12px" not in img_attrs:
                issues.append(
                    QualityIssue(
                        code="NEWSLETTER_HERO_STYLE_INVALID",
                        severity="error",
                        message="La imagen Hero debe declarar 'max-width: 560px' y 'border-radius: 12px'.",
                        field="html_content",
                    )
                )

        if (
            "En 60 segundos: Los 3 Insights Clave" not in html_content
            and "In 60 seconds: 3 Key Insights" not in html_content
        ):
            issues.append(
                QualityIssue(
                    code="NEWSLETTER_MISSING_60S_BOX",
                    severity="error",
                    message="Falta el bloque visual Zero-Click 'En 60 segundos: Los 3 Insights Clave' / 'In 60 seconds: 3 Key Insights'.",
                    field="html_content",
                )
            )

        if "utm_source=newsletter" not in html_content or "utm_medium=email" not in html_content:
            issues.append(
                QualityIssue(
                    code="NEWSLETTER_MISSING_UTMS",
                    severity="error",
                    message="Los enlaces CTA deben incluir utm_source=newsletter y utm_medium=email.",
                    field="html_content",
                )
            )

        if "{{ unsubscribe }}" not in html_content:
            issues.append(
                QualityIssue(
                    code="NEWSLETTER_MISSING_UNSUBSCRIBE",
                    severity="error",
                    message="Falta el enlace obligatorio {{ unsubscribe }} de Brevo.",
                    field="html_content",
                )
            )

        visible_text = _extract_visible_text(html_content)
        visible_words = len(visible_text.split())
        visible_chars = len(visible_text)
        text_to_img_ok = img_count == 1 and visible_chars >= 400 and visible_words >= 75
        metrics["visible_words"] = visible_words
        metrics["visible_chars"] = visible_chars
        metrics["text_to_img_ok"] = text_to_img_ok

        if not text_to_img_ok:
            issues.append(
                QualityIssue(
                    code="NEWSLETTER_TEXT_IMAGE_RATIO_LOW",
                    severity="error",
                    message=f"Ratio textual anti-spam insuficiente ({visible_words} palabras, {visible_chars} chars, {img_count} img).",
                    field="html_content",
                )
            )

    return PlatformAuditResult(
        platform="newsletter",
        status=_compute_status(issues),  # type: ignore[arg-type]
        issues=issues,
        metrics=metrics,
    )


def _extract_markdown_url_target(raw_target: str) -> str:
    """Extrae la parte URL de un target Markdown descartando títulos opcionales."""
    stripped = raw_target.strip()
    title_match = re.match(r'^(\S+?)\s+(["\'].*["\'])$', stripped)
    return title_match.group(1) if title_match else stripped


def audit_markdown_syndication(artifact: SyndicationArtifact) -> PlatformAuditResult:
    """Audita artefactos Markdown sindicados hacia Dev.to y CoderLegion (INV-AUTO-7/8)."""
    issues: List[QualityIssue] = []
    canonical = (artifact.canonical_url or "").strip()
    body = artifact.markdown or ""
    body_without_code = _FENCED_CODE_BLOCK_RE.sub("", body)

    if not canonical.startswith("https://datalaria.com/"):
        issues.append(
            QualityIssue(
                code="SYNDICATION_CANONICAL_MISSING",
                severity="error",
                message="La URL canónica debe comenzar por 'https://datalaria.com/'.",
                field="canonical_url",
            )
        )

    if len(body.strip()) < 120:
        issues.append(
            QualityIssue(
                code="SYNDICATION_EMPTY_CONTENT",
                severity="error",
                message=f"El cuerpo sindicado ({len(body.strip())} chars) es demasiado corto (< 120).",
                field="markdown",
            )
        )

    if "{{" in body_without_code and ("{{<" in body_without_code or "{{%" in body_without_code):
        issues.append(
            QualityIssue(
                code="SYNDICATION_RESIDUAL_SHORTCODE",
                severity="error",
                message="Se detectaron shortcodes Hugo residuales fuera de bloques de código.",
                field="markdown",
            )
        )

    relative_images: List[str] = []
    for match in _SYNDICATION_IMAGE_RE.finditer(body_without_code):
        img_target = _extract_markdown_url_target(match.group(1))
        if not img_target.startswith(("http://", "https://")):
            relative_images.append(img_target)
    if relative_images:
        issues.append(
            QualityIssue(
                code="SYNDICATION_RELATIVE_IMAGE",
                severity="error",
                message=f"Imágenes relativas sin resolver: {', '.join(relative_images[:3])}.",
                field="markdown",
            )
        )

    relative_links: List[str] = []
    datalaria_links: List[str] = []
    for match in _SYNDICATION_LINK_RE.finditer(body_without_code):
        link_target = _extract_markdown_url_target(match.group(1))
        if not link_target.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            relative_links.append(link_target)
        elif "datalaria.com" in link_target.lower():
            datalaria_links.append(link_target)

    if relative_links:
        issues.append(
            QualityIssue(
                code="SYNDICATION_RELATIVE_LINK",
                severity="error",
                message=f"Enlaces relativos sin resolver: {', '.join(relative_links[:3])}.",
                field="markdown",
            )
        )

    normalized_canonical = canonical.rstrip("/")
    if normalized_canonical and normalized_canonical not in body_without_code:
        issues.append(
            QualityIssue(
                code="SYNDICATION_ATTRIBUTION_MISSING",
                severity="error",
                message="Falta el enlace de atribución canónica hacia la URL original en Datalaria.",
                field="markdown",
            )
        )

    expected_utm = f"utm_source={artifact.platform}"
    if not any(expected_utm in link for link in datalaria_links):
        issues.append(
            QualityIssue(
                code="SYNDICATION_MISSING_UTM",
                severity="error",
                message=f"Falta parámetro de trazabilidad '{expected_utm}' en enlaces hacia datalaria.com.",
                field="markdown",
            )
        )

    if artifact.platform == "devto":
        invalid_tags = [tag for tag in artifact.tags if not _DEVTO_TAG_RE.match(tag)]
        if len(artifact.tags) > 4 or invalid_tags:
            issues.append(
                QualityIssue(
                    code="SYNDICATION_DEVTO_TAGS_INVALID",
                    severity="error",
                    message=(
                        f"Tags inválidos para Dev.to (máx. 4, ^[a-z0-9]{{1,30}}$): {artifact.tags}."
                    ),
                    field="tags",
                )
            )

    metrics = {
        "char_count": len(body.strip()),
        "relative_images": len(relative_images),
        "relative_links": len(relative_links),
        "datalaria_links": len(datalaria_links),
        "tags_count": len(artifact.tags),
    }

    return PlatformAuditResult(
        platform=artifact.platform,
        status=_compute_status(issues),  # type: ignore[arg-type]
        issues=issues,
        metrics=metrics,
    )


def audit_social_bundle(
    x_pack: Optional[SocialPlatformX] = None,
    linkedin_text: Optional[str] = None,
    newsletter_payload: Optional[NewsletterContent] = None,
    newsletter_html: Optional[str] = None,
    post_url: str = "",
    devto_artifact: Optional[SyndicationArtifact] = None,
    coderlegion_artifact: Optional[SyndicationArtifact] = None,
) -> QualityAuditReport:
    """Agrega auditorías individuales de X, LinkedIn, Brevo 2.0 y sindicación Markdown."""
    results: Dict[str, PlatformAuditResult] = {}

    if x_pack is not None:
        results["x"] = audit_x_pack(x_pack, post_url=post_url)
    if linkedin_text is not None:
        results["linkedin"] = audit_linkedin_post(linkedin_text)
    if newsletter_payload is not None:
        results["newsletter"] = audit_newsletter_payload(newsletter_payload, html_content=newsletter_html)
    if devto_artifact is not None:
        results["devto"] = audit_markdown_syndication(devto_artifact)
    if coderlegion_artifact is not None:
        results["coderlegion"] = audit_markdown_syndication(coderlegion_artifact)

    statuses = [res.status for res in results.values()]
    if "FAIL" in statuses:
        overall = "FAIL"
    elif "WARN" in statuses:
        overall = "WARN"
    else:
        overall = "PASS"

    return QualityAuditReport(overall_status=overall, results=results)  # type: ignore[arg-type]
