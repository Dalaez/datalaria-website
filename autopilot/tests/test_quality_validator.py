"""Tests deterministas para models.py, quality_validator.py y política X coste 0 EUR."""

from __future__ import annotations

import pytest

from autopilot.src.models import (
    NewsletterContent,
    SocialPlatformX,
    build_x_web_intent_url,
    count_twitter_weighted_length,
)
from autopilot.src.quality_validator import (
    audit_linkedin_post,
    audit_newsletter_payload,
    audit_social_bundle,
    audit_x_pack,
)
from autopilot.src.social_manager import SocialMediaManager


def test_twitter_weighted_length_urls_and_emojis() -> None:
    text = "Nuevo análisis 🚀 https://datalaria.com/es/posts/demo-larga-con-slug-extenso/"
    # "Nuevo análisis " (15) + "🚀" (2) + " " (1) + URL (23) = 41
    assert count_twitter_weighted_length(text) == 41


def test_build_x_web_intent_url_format() -> None:
    url = build_x_web_intent_url(
        text="El 80% de los proyectos falla antes de programar.",
        url="https://datalaria.com/es/posts/demo/",
        hashtags=["#SDD", "IA"],
    )
    assert url.startswith("https://x.com/intent/tweet?")
    assert "hashtags=SDD%2CIA" in url
    assert "url=https%3A%2F%2Fdatalaria.com%2Fes%2Fposts%2Fdemo%2F" in url


def test_audit_x_pack_pass_and_reject_violations() -> None:
    post_url = "https://datalaria.com/es/posts/test/"
    valid_pack = SocialPlatformX(
        hook="La mayoría de equipos confunde velocidad con rigor arquitectónico.",
        thread=[
            "1/4 Primer tweet técnico con contexto medible y concreto.",
            "2/4 Segundo tweet explicando el cuello de botella real en producción.",
            "3/4 Tercer tweet detallando cómo mitigarlo con contratos deterministas.",
            f"4/4 Guía completa paso a paso aquí: {post_url}",
        ],
        hashtags=["SDD", "DataEngineering"],
        web_intent_url=build_x_web_intent_url(
            "La mayoría de equipos confunde velocidad con rigor arquitectónico.",
            post_url,
            ["SDD"],
        ),
    )
    ok_res = audit_x_pack(valid_pack, post_url=post_url)
    assert ok_res.status == "PASS"

    bad_hook_pack = SocialPlatformX(
        hook=f"Mira esto {post_url}",
        thread=valid_pack.thread,
        web_intent_url=valid_pack.web_intent_url,
    )
    bad_res = audit_x_pack(bad_hook_pack, post_url=post_url)
    assert bad_res.status == "FAIL"
    assert any(issue.code == "X_URL_IN_HOOK" for issue in bad_res.issues)

    over_280_pack = SocialPlatformX(
        hook="Gancho válido de prueba para validar longitud.",
        thread=[
            "1/4 " + ("a" * 281),
            "2/4 Tweet normal de cierre.",
            "3/4 Tweet normal adicional.",
            "4/4 Tweet final.",
        ],
        web_intent_url=valid_pack.web_intent_url,
    )
    over_res = audit_x_pack(over_280_pack, post_url=post_url)
    assert over_res.status == "FAIL"
    assert any(issue.code == "X_TWEET_OVER_280" for issue in over_res.issues)


def test_audit_linkedin_broetry_rules() -> None:
    valid_post = (
        "¿Por qué fallan tantos proyectos de datos en el primer trimestre?\n\n"
        "Casi todo el mundo empieza eligiendo herramientas antes de definir invariantes.\n\n"
        "📊 Cuando separas cálculo determinista y síntesis LLM, los costes caen.\n\n"
        "¿Cuál ha sido tu mayor cuello de botella este año?"
    )
    assert audit_linkedin_post(valid_post).status == "PASS"

    no_question = valid_post.replace("?", ".")
    assert audit_linkedin_post(no_question).status == "FAIL"

    mid_emoji = (
        "Gancho corto de ejemplo.\n\n"
        "Muchos equipos 🚀 pierden foco en producción.\n\n"
        "¿Cómo lo resuelves tú?"
    )
    mid_res = audit_linkedin_post(mid_emoji)
    assert mid_res.status == "FAIL"
    assert any(i.code == "LINKEDIN_MID_SENTENCE_EMOJI" for i in mid_res.issues)


def test_audit_newsletter_payload_greeting_rejection() -> None:
    payload = NewsletterContent(
        archetype="real_case_number",
        subject="3 errores invisibles al automatizar tus pipelines",
        preheader="Cómo evitar fallos silenciosos con contratos deterministas en producción.",
        hook_paragraphs=[
            "Hola equipo, hoy te cuento algo curioso sobre automatización.",
            "Este segundo párrafo explica el contexto técnico sin ruido comercial.",
        ],
        insights_60s=[
            "Separar contratos Pydantic del bloque de generación LLM.",
            "Validar longitud ponderada antes de disparar webhooks externos.",
            "Aplicar fallback offline determinista para CI sin coste.",
        ],
    )
    res = audit_newsletter_payload(payload)
    assert res.status == "FAIL"
    assert any(i.code == "NEWSLETTER_REDUNDANT_GREETING" for i in res.issues)


def test_social_manager_zero_cost_x_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ENABLE_TWITTER_API", raising=False)
    monkeypatch.setenv("TWITTER_API_KEY", "dummy-key")
    manager = SocialMediaManager()
    assert manager.twitter_api_enabled is False
    assert manager.client_v2 is None

    result = manager.post_to_twitter(
        text="Gancho sin llamadas de pago.",
        url="https://datalaria.com/es/posts/test/",
    )
    assert result["mode"] == "zero_cost_intent"
    assert result["web_intent_url"].startswith("https://x.com/intent/tweet?")


def test_audit_social_bundle_aggregates_statuses() -> None:
    post_url = "https://datalaria.com/es/posts/demo/"
    x_pack = SocialPlatformX(
        hook="¿Cuánto cuesta mantener un pipeline sin especificaciones claras?",
        thread=[
            "1/4 Primer paso del hilo con contexto directo.",
            "2/4 Segundo paso con contraste cuantitativo real.",
            "3/4 Tercer paso sobre contratos deterministas.",
            "4/4 Lectura completa disponible en Datalaria.",
        ],
        hashtags=["SDD"],
        web_intent_url=build_x_web_intent_url("Gancho", post_url, ["SDD"]),
    )
    report = audit_social_bundle(
        x_pack=x_pack,
        linkedin_text="Hook directo.\n\nContexto claro.\n\n¿Qué opinas?",
        post_url=post_url,
    )
    assert report.overall_status == "PASS"
    assert set(report.results.keys()) == {"x", "linkedin"}
