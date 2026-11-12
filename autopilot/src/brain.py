"""El Cerebro de Autopilot 2.0: síntesis JSON vía Gemini + fallback determinista offline."""

from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional

from google import genai
from google.genai import types

from autopilot.src.models import (
    ROBOTIC_SUBJECT_PREFIXES,
    NewsletterContent,
    SocialPlatformX,
    SubjectArchetype,
    build_x_web_intent_url,
    count_twitter_weighted_length,
    select_subject_archetype,
)

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"

_SHORTCODE_RE = re.compile(r"\{\{<.*?>\}\}|\{\{%.*?%\}\}", re.DOTALL)
_MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
_CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)


def _strip_markdown(text: str) -> str:
    """Limpia sintaxis Markdown y shortcodes Hugo dejando prosa legible."""
    cleaned = _CODE_BLOCK_RE.sub(" ", text or "")
    cleaned = _SHORTCODE_RE.sub(" ", cleaned)
    cleaned = _MD_IMAGE_RE.sub(" ", cleaned)
    cleaned = _MD_LINK_RE.sub(r"\1", cleaned)
    cleaned = _URL_RE.sub("", cleaned)
    cleaned = re.sub(r"[*_`>#|]+", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def _extract_headings_and_sentences(content: str) -> tuple[List[str], List[str]]:
    """Extrae encabezados H2/H3 y oraciones informativas del cuerpo Markdown."""
    headings: List[str] = []
    sentences: List[str] = []

    raw_without_code = _CODE_BLOCK_RE.sub("\n", content or "")
    for line in raw_without_code.splitlines():
        stripped = line.strip()
        if stripped.startswith(("## ", "### ")):
            heading = _strip_markdown(stripped.lstrip("# "))
            if len(heading) >= 10:
                headings.append(heading)

    plain = _strip_markdown(raw_without_code)
    for part in re.split(r"(?<=[.!?])\s+", plain):
        candidate = part.strip()
        if len(candidate) >= 35 and candidate not in sentences:
            sentences.append(candidate)

    return headings, sentences


_TRAILING_CONNECTORS = {
    "y", "e", "o", "u", "de", "del", "la", "las", "el", "los", "en", "con",
    "para", "por", "a", "un", "una", "and", "or", "of", "the", "in", "for",
    "to", "with", "on", "an",
}


def _trim_weighted_text(text: str, max_weighted: int) -> str:
    """Recorta texto por palabras asegurando límite ponderado sin conectores colgados."""
    cleaned = re.sub(r"\s+", " ", (text or "").strip())
    if count_twitter_weighted_length(cleaned) <= max_weighted:
        return cleaned
    words = cleaned.split()
    acc: List[str] = []
    for word in words:
        trial = " ".join([*acc, word])
        if count_twitter_weighted_length(trial) > max_weighted:
            break
        acc.append(word)
    while len(acc) > 2 and acc[-1].rstrip(".,;:-").lower() in _TRAILING_CONNECTORS:
        acc.pop()
    result = " ".join(acc).rstrip(".,;:- ")
    return result or cleaned[: max(10, max_weighted // 2)]


def _sanitize_subject(subject: str, title: str, archetype: SubjectArchetype, lang: str) -> str:
    """Elimina prefijos robóticos y ajusta el asunto dentro de [25, 110] caracteres."""
    cleaned = re.sub(r"\s+", " ", (subject or "").strip())
    lowered = cleaned.lower()
    for prefix in ROBOTIC_SUBJECT_PREFIXES:
        if lowered.startswith(prefix):
            cleaned = cleaned[len(prefix) :].strip()
            lowered = cleaned.lower()

    if len(cleaned) < 25:
        short_title = _trim_weighted_text(title, 65)
        if lang == "es":
            fallback_map: Dict[SubjectArchetype, str] = {
                "counterintuitive_question": f"¿Por qué falla el enfoque clásico en {short_title}?",
                "real_case_number": f"3 claves reales detrás de {short_title}",
                "invisible_error": f"El error invisible al aplicar {short_title}",
                "architecture_inside": f"Por dentro: la arquitectura de {short_title}",
                "direct_framework": f"Framework práctico sobre {short_title}",
            }
        else:
            fallback_map = {
                "counterintuitive_question": f"Why standard approaches fail in {short_title}?",
                "real_case_number": f"3 practical lessons behind {short_title}",
                "invisible_error": f"The hidden mistake when applying {short_title}",
                "architecture_inside": f"Inside the architecture of {short_title}",
                "direct_framework": f"A practical framework for {short_title}",
            }
        cleaned = fallback_map[archetype]

    if len(cleaned) > 110:
        words = cleaned.split()
        acc: List[str] = []
        for word in words:
            trial = " ".join([*acc, word])
            if len(trial) > 108:
                break
            acc.append(word)
        cleaned = " ".join(acc).rstrip(".,;:- ")

    if len(cleaned) < 25:
        cleaned = f"{cleaned} — Datalaria Engineering"
    return cleaned[:110]


def _extract_json_object(raw_text: str) -> Optional[Dict[str, Any]]:
    """Extrae objeto JSON limpio desde la respuesta del LLM."""
    text = (raw_text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.DOTALL).strip()
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            return None
        try:
            parsed = json.loads(match.group(0))
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            return None


def _call_gemini_json(system_instruction: str, user_prompt: str) -> Optional[Dict[str, Any]]:
    """Invoca Gemini solicitando JSON estructurado; devuelve None sin fallar si no hay clave."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=DEFAULT_GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                max_output_tokens=2000,
                temperature=0.6,
            ),
        )
        return _extract_json_object(response.text or "")
    except Exception as exc:
        print(f"⚠️ Fallback offline activado en brain.py ({exc})")
        return None


def build_deterministic_fallback_x(
    title: str,
    content: str,
    lang: str = "es",
    post_url: str = "",
    hashtags: Optional[List[str]] = None,
) -> SocialPlatformX:
    """Construye determinísticamente un hilo X de 4 tweets + Web Intent URL sin red."""
    headings, sentences = _extract_headings_and_sentences(content)
    clean_title = _strip_markdown(title) or "Datalaria Engineering"
    default_tags = hashtags or (
        ["DataEngineering", "AI", "Datalaria"] if lang == "en" else ["IngenieriaDeDatos", "IA", "Datalaria"]
    )

    if lang == "es":
        hook = _trim_weighted_text(
            f"La brecha entre teoría y ejecución en {clean_title} suele romper proyectos antes de empezar.",
            185,
        )
        point_2 = headings[0] if headings else (sentences[0] if sentences else clean_title)
        point_3 = (
            headings[1]
            if len(headings) > 1
            else (sentences[1] if len(sentences) > 1 else "Estructura determinista y trazabilidad medible.")
        )
        tweet_1 = _trim_weighted_text(f"1/4 {hook}", 270)
        tweet_2 = _trim_weighted_text(f"2/4 Qué cambia en la práctica: {point_2}", 270)
        tweet_3 = _trim_weighted_text(f"3/4 Punto crítico de arquitectura: {point_3}", 270)
        closing = f"4/4 Guía completa paso a paso en Datalaria: {post_url}".strip() if post_url else "4/4 Análisis completo con ejemplo paso a paso en Datalaria."
        tweet_4 = _trim_weighted_text(closing, 275) if count_twitter_weighted_length(closing) > 280 else closing
    else:
        hook = _trim_weighted_text(
            f"Most teams miss the structural detail behind {clean_title} before shipping to production.",
            185,
        )
        point_2 = headings[0] if headings else (sentences[0] if sentences else clean_title)
        point_3 = (
            headings[1]
            if len(headings) > 1
            else (sentences[1] if len(sentences) > 1 else "Deterministic pipelines and measurable execution.")
        )
        tweet_1 = _trim_weighted_text(f"1/4 {hook}", 270)
        tweet_2 = _trim_weighted_text(f"2/4 Core operational shift: {point_2}", 270)
        tweet_3 = _trim_weighted_text(f"3/4 Architecture takeaway: {point_3}", 270)
        closing = f"4/4 Full breakdown and architecture notes on Datalaria: {post_url}".strip() if post_url else "4/4 Full breakdown and implementation guide on Datalaria."
        tweet_4 = _trim_weighted_text(closing, 275) if count_twitter_weighted_length(closing) > 280 else closing

    intent_url = build_x_web_intent_url(hook, post_url, default_tags)
    return SocialPlatformX(
        hook=hook,
        thread=[tweet_1, tweet_2, tweet_3, tweet_4],
        hashtags=[t.lstrip("#") for t in default_tags],
        web_intent_url=intent_url,
    )


def build_deterministic_fallback_linkedin(
    title: str,
    content: str,
    lang: str = "es",
) -> str:
    """Construye determinísticamente un post estilo Broetry limpio para LinkedIn."""
    headings, sentences = _extract_headings_and_sentences(content)
    clean_title = _strip_markdown(title) or "Datalaria"

    detail_1 = headings[0] if headings else (sentences[0][:180] if sentences else clean_title)
    detail_2 = (
        headings[1]
        if len(headings) > 1
        else (sentences[1][:180] if len(sentences) > 1 else clean_title)
    )

    if lang == "es":
        paragraphs = [
            f"¿Por qué seguimos improvisando procesos críticos en torno a {clean_title}?",
            "La mayoría de los equipos intenta acelerar con herramientas aisladas.\nEl cuello de botella real aparece cuando falta rigor estructurado.",
            f"📊 Primer pilar clave: {detail_1}.\n\n🎯 Segundo punto decisivo: {detail_2}.",
            "¿Qué parte de este enfoque te genera más fricción en tus proyectos actuales?",
        ]
    else:
        paragraphs = [
            f"Why do engineering teams still improvise critical workflows around {clean_title}?",
            "Most teams reach for isolated tools first.\nThe real bottleneck appears when structured rigor is missing.",
            f"📊 Key pillar one: {detail_1}.\n\n🎯 Key pillar two: {detail_2}.",
            "Which part of this workflow creates the biggest friction in your team today?",
        ]
    return "\n\n".join(paragraphs)


def build_deterministic_fallback_newsletter(
    title: str,
    content: str,
    slug: str,
    lang: str = "es",
    archetype: Optional[SubjectArchetype] = None,
    secondary_cta_label: Optional[str] = None,
    secondary_cta_url: Optional[str] = None,
) -> NewsletterContent:
    """Genera payload Brevo 2.0 Anti-Churn 100 % determinista desde el Markdown real."""
    chosen_archetype = select_subject_archetype(slug, archetype)
    clean_title = _strip_markdown(title) or slug
    headings, sentences = _extract_headings_and_sentences(content)

    subject = _sanitize_subject("", clean_title, chosen_archetype, lang)

    if sentences:
        preheader_raw = sentences[0]
    else:
        preheader_raw = (
            f"3 aprendizajes accionables sobre {clean_title} aplicables hoy."
            if lang == "es"
            else f"3 actionable takeaways on {clean_title} ready to apply today."
        )
    preheader = _trim_weighted_text(preheader_raw, 145)
    if len(preheader) < 35:
        preheader = (
            f"{preheader} Descubre las claves prácticas en Datalaria."
            if lang == "es"
            else f"{preheader} Explore the practical takeaways at Datalaria."
        )[:155]

    if lang == "es":
        hook_1 = (
            sentences[0][:220]
            if sentences
            else f"Esta semana analicé a fondo un reto habitual en torno a {clean_title} que suele frenar a los equipos técnicos."
        )
        hook_2 = (
            f"En el nuevo artículo desgloso cómo pasar de la teoría a una ejecución repetible sobre {clean_title}, "
            "evitando los errores silenciosos más costosos."
        )
        insights = [
            f"Foco estratégico: {headings[0]}" if len(headings) > 0 else f"Marco claro de decisión aplicado a {clean_title}.",
            f"Arquitectura ejecutable: {headings[1]}" if len(headings) > 1 else "Separación limpia entre diseño determinista y automatización.",
            f"Siguiente paso práctico: {headings[2]}" if len(headings) > 2 else "Checklist medible para validar impacto antes de escalar.",
        ]
        ps_text = "P.D. Si conoces a un compañero de datos, producto u operaciones al que le ayude esta guía, reenvíale este correo."
    else:
        hook_1 = (
            sentences[0][:220]
            if sentences
            else f"This week I took a close look at a recurring bottleneck around {clean_title} that slows down technical teams."
        )
        hook_2 = (
            f"In this new deep dive I break down how to move from scattered ideas to repeatable execution on {clean_title}, "
            "without falling into the silent traps."
        )
        insights = [
            f"Strategic focus: {headings[0]}" if len(headings) > 0 else f"Clear decision framework applied to {clean_title}.",
            f"Actionable architecture: {headings[1]}" if len(headings) > 1 else "Clean separation between deterministic logic and automation.",
            f"Practical next step: {headings[2]}" if len(headings) > 2 else "Measurable validation checklist before scaling.",
        ]
        ps_text = "P.S. Know a colleague in data, product, or operations who would find this useful? Forward this email their way."

    normalized_insights = [
        item if len(item.strip()) >= 12 else f"{item.strip()} — Datalaria"
        for item in insights[:3]
    ]

    return NewsletterContent(
        archetype=chosen_archetype,
        subject=subject,
        preheader=preheader,
        hook_paragraphs=[hook_1, hook_2],
        insights_60s=normalized_insights,
        secondary_cta_label=secondary_cta_label,
        secondary_cta_url=secondary_cta_url,
        ps_referral_text=ps_text,
    )


def generate_x_thread_pack(
    title: str,
    content: str,
    lang: str = "es",
    post_url: str = "",
    hashtags: Optional[List[str]] = None,
) -> SocialPlatformX:
    """Genera paquete estructurado X (hook < 200 chars sin URL + hilo 4-6 tweets + Web Intent)."""
    snippet = (content or "")[:6000]
    default_tags = hashtags or (
        ["DataEngineering", "AI", "Datalaria"] if lang == "en" else ["IngenieriaDeDatos", "IA", "Datalaria"]
    )
    sys_instruction = (
        "Return strict JSON with keys: 'hook' (string < 185 chars, NO URLs, complete sentence), "
        "'thread' (array of 4 to 5 tweets numbered 1/N..N/N, each <= 265 chars, NO abrupt ellipsis), "
        "'hashtags' (array of 2-3 tags without '#'). "
        f"Language: {'English' if lang == 'en' else 'Spanish'}."
    )
    data = _call_gemini_json(sys_instruction, f"Title: {title}\nURL: {post_url}\nContent:\n{snippet}")
    if data:
        try:
            hook = _URL_RE.sub("", str(data.get("hook", ""))).strip()
            hook = _trim_weighted_text(hook, 190)
            raw_thread = [str(t).strip() for t in data.get("thread", []) if str(t).strip()]
            raw_tags = [str(t).lstrip("#").strip() for t in data.get("hashtags", default_tags) if str(t).strip()]
            intent_url = build_x_web_intent_url(hook, post_url, raw_tags or default_tags)
            candidate = SocialPlatformX(
                hook=hook,
                thread=raw_thread[:6],
                hashtags=raw_tags or default_tags,
                web_intent_url=intent_url,
            )
            if all(count_twitter_weighted_length(t) <= 280 for t in candidate.thread):
                return candidate
        except Exception as exc:
            print(f"⚠️ Validación X LLM falló, usando fallback determinista: {exc}")

    return build_deterministic_fallback_x(title, content, lang=lang, post_url=post_url, hashtags=default_tags)


def generate_linkedin_copy(title: str, content: str, lang: str = "es") -> str:
    """Genera copy estilo Broetry para LinkedIn con fallback determinista offline."""
    snippet = (content or "")[:6000]
    sys_instruction = (
        "Return strict JSON with key 'text' for a LinkedIn thought-leadership post in Broetry format: "
        "1) Hook (max 2 lines), 2) Pivot, 3) Specific Insight, 4) Concrete Detail, 5) Closing Debate Question ending with '?'. "
        "CRITICAL: Separate every paragraph with '\\n\\n'. No paragraph over 3 lines. Never embed emojis inside the middle of sentences. "
        f"Never include URLs. Language: {'English' if lang == 'en' else 'Spanish'}."
    )
    data = _call_gemini_json(sys_instruction, f"Title: {title}\nContent:\n{snippet}")
    if data and isinstance(data.get("text"), str):
        candidate = data["text"].strip()
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", candidate) if p.strip()]
        if len(paragraphs) >= 3 and "?" in paragraphs[-1] and len(candidate) <= 3000:
            return candidate
    return build_deterministic_fallback_linkedin(title, content, lang=lang)


def generate_newsletter_payload(
    title: str,
    content: str,
    slug: str,
    lang: str = "es",
    archetype: Optional[SubjectArchetype] = None,
    secondary_cta_label: Optional[str] = None,
    secondary_cta_url: Optional[str] = None,
) -> NewsletterContent:
    """Genera contrato Brevo 2.0 Anti-Churn con rotación de 5 arquetipos y fallback offline."""
    chosen_archetype = select_subject_archetype(slug, archetype)
    snippet = (content or "")[:6000]
    sys_instruction = (
        "Return strict JSON with keys: 'subject' (30-95 chars, NEVER start with 'Nuevo en Datalaria' or 'New on Datalaria', "
        f"follow archetype '{chosen_archetype}'), 'preheader' (45-145 chars), "
        "'hook_paragraphs' (array of 2-3 short personal paragraphs, NO 'Hola'/'Hi' greeting and NO signature), "
        "'insights_60s' (array of EXACTLY 3 concrete actionable takeaways >= 15 chars each), "
        "'ps_referral_text' (short P.D./P.S. inviting readers to forward the email). "
        f"Language: {'English' if lang == 'en' else 'Spanish'}."
    )
    data = _call_gemini_json(sys_instruction, f"Title: {title}\nSlug: {slug}\nContent:\n{snippet}")
    if data:
        try:
            subject = _sanitize_subject(str(data.get("subject", "")), title, chosen_archetype, lang)
            preheader = str(data.get("preheader", "")).strip()
            hooks = [str(p).strip() for p in data.get("hook_paragraphs", []) if str(p).strip()]
            insights = [str(i).strip() for i in data.get("insights_60s", []) if str(i).strip()]
            ps_text = str(data.get("ps_referral_text", "")).strip() or None
            return NewsletterContent(
                archetype=chosen_archetype,
                subject=subject,
                preheader=preheader,
                hook_paragraphs=hooks[:4],
                insights_60s=insights[:3],
                secondary_cta_label=secondary_cta_label,
                secondary_cta_url=secondary_cta_url,
                ps_referral_text=ps_text,
            )
        except Exception as exc:
            print(f"⚠️ Validación Brevo 2.0 LLM falló, usando fallback determinista: {exc}")

    return build_deterministic_fallback_newsletter(
        title=title,
        content=content,
        slug=slug,
        lang=lang,
        archetype=chosen_archetype,
        secondary_cta_label=secondary_cta_label,
        secondary_cta_url=secondary_cta_url,
    )


def generate_social_copy(
    title: str,
    content: str,
    platform: str = "twitter",
    lang: str = "es",
) -> Optional[str]:
    """Interfaz retrocompatible que delega en los generadores estructurados de Autopilot 2.0."""
    if platform == "twitter":
        return generate_x_thread_pack(title=title, content=content, lang=lang).hook
    if platform == "linkedin":
        return generate_linkedin_copy(title=title, content=content, lang=lang)
    if platform == "newsletter":
        slug_hint = re.sub(r"[^a-z0-9-]+", "-", title.lower()).strip("-") or "datalaria-post"
        payload = generate_newsletter_payload(title=title, content=content, slug=slug_hint, lang=lang)
        return "\n\n".join(payload.hook_paragraphs)
    return None
