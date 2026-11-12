"""Tests unitarios para Brevo Newsletter 2.0 Anti-Churn y NewsletterManager."""

from __future__ import annotations

import re
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from autopilot.src.models import (
    SUBJECT_ARCHETYPES,
    NewsletterContent,
    append_utm_params,
    select_subject_archetype,
)
from autopilot.src.newsletter_manager import NewsletterManager
from autopilot.src.quality_validator import audit_newsletter_payload


def test_subject_archetypes_deterministic_coverage() -> None:
    slugs = [f"articulo-prueba-{idx}" for idx in range(25)]
    observed = {select_subject_archetype(slug) for slug in slugs}
    assert observed == set(SUBJECT_ARCHETYPES)
    assert select_subject_archetype("mi-slug") == select_subject_archetype("mi-slug")
    assert select_subject_archetype("mi-slug", "direct_framework") == "direct_framework"


@pytest.mark.parametrize(
    "bad_subject",
    [
        "🚀 Nuevo en Datalaria: Guía completa de BPMN e IA",
        "Nuevo en Datalaria: Guía completa de BPMN e IA",
        "🚀 New on Datalaria: Complete BPMN & AI Guide",
        "New on Datalaria: Complete BPMN & AI Guide",
    ],
)
def test_rejects_robotic_subject_prefixes(bad_subject: str) -> None:
    with pytest.raises(ValidationError):
        NewsletterContent(
            archetype="direct_framework",
            subject=bad_subject,
            preheader="Un preheader válido con longitud suficiente para pasar validación.",
            hook_paragraphs=["Párrafo personal de prueba con contexto técnico real."],
            insights_60s=[
                "Primer insight accionable sobre arquitectura.",
                "Segundo insight medible sobre costes y latencia.",
                "Tercer insight aplicable en producción hoy mismo.",
            ],
        )


def test_preview_campaign_fixes_list_id_bug_es_and_en(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BREVO_API_KEY", raising=False)
    manager = NewsletterManager()

    res_es = manager.preview_campaign(
        subject="3 claves de ingeniería para procesos S&OP",
        intro_text="Texto de prueba para verificar que preview_campaign funciona en español.",
        post_title="Procesos S&OP con IA",
        post_url="https://datalaria.com/es/posts/sop-ia/",
        lang="es",
        hero_image_url="https://datalaria.com/images/Datalaria_blog.png",
    )
    res_en = manager.preview_campaign(
        subject="3 engineering keys for S&OP workflows",
        intro_text="Sample body text verifying preview_campaign runs cleanly in English.",
        post_title="S&OP Workflows with AI",
        post_url="https://datalaria.com/en/posts/sop-ai/",
        lang="en",
        hero_image_url="https://datalaria.com/images/Datalaria_blog.png",
    )

    assert res_es["list_id"] == 3
    assert res_en["list_id"] == 4
    assert "En 60 segundos: Los 3 Insights Clave" in res_es["html"]
    assert "In 60 seconds: 3 Key Insights" in res_en["html"]


def test_brevo_v2_html_single_hero_image_anti_spam_and_audit() -> None:
    manager = NewsletterManager()
    payload = NewsletterContent(
        archetype="architecture_inside",
        subject="Por dentro: arquitectura SDD sin costes fijos de LLM",
        preheader="Descubre cómo diseñamos validación determinista con cero llamadas de pago.",
        hook_paragraphs=[
            "Esta semana revisamos un cuello de botella clásico al automatizar envíos de newsletter y redes sociales desde repositorios estáticos.",
            "Separando el cerebro creativo del músculo determinista logramos pruebas 100% reproducibles sin comprometer ni la estética ni la entrega en bandeja de entrada.",
        ],
        insights_60s=[
            "Mantener una única imagen Hero clicable protege la entregabilidad frente a filtros anti-spam.",
            "Rotar 5 arquetipos de asunto evita la fatiga por encabezados repetitivos.",
            "Inyectar UTMs antes del fragmento hash mantiene intacto el enrutado en SPAs React.",
        ],
        secondary_cta_label="Probar Demo Sandbox de LifeOps",
        secondary_cta_url="https://datalaria.com/apps/lifeops/#/?mock=true",
        ps_referral_text="P.D. Reenvía esta edición a quien lidere automatización en tu equipo.",
    )
    html_doc = manager._build_html_template(
        payload,
        post_title="Arquitectura Autopilot 2.0",
        post_url="https://datalaria.com/es/posts/autopilot-v2/",
        lang="es",
        hero_image_url="https://raw.githubusercontent.com/Dalaez/datalaria-website/main/content/es/posts/autopilot-v2/cover.png",
        slug="autopilot-v2",
    )

    img_tags = re.findall(r"<img\b[^>]*>", html_doc, flags=re.IGNORECASE)
    assert len(img_tags) == 1
    assert "max-width: 560px" in img_tags[0]
    assert "border-radius: 12px" in img_tags[0]
    assert "En 60 segundos: Los 3 Insights Clave" in html_doc
    assert "{{ unsubscribe }}" in html_doc

    audit = audit_newsletter_payload(payload, html_content=html_doc)
    assert audit.status == "PASS"
    assert audit.metrics["text_to_img_ok"] is True


def test_append_utm_params_preserves_hashrouter_fragment() -> None:
    raw = "https://datalaria.com/apps/lifeops/#/?mock=true"
    enriched = append_utm_params(
        raw,
        source="newsletter",
        medium="email",
        campaign="post-demo",
        content="cta_secondary",
    )
    assert enriched.startswith(
        "https://datalaria.com/apps/lifeops/?utm_source=newsletter&utm_medium=email"
    )
    assert enriched.endswith("#/?mock=true")


def test_html_escaping_protects_against_script_injection() -> None:
    manager = NewsletterManager()
    payload = NewsletterContent(
        archetype="invisible_error",
        subject="El fallo invisible en <script>alert(1)</script> y plantillas",
        preheader="Un preheader limpio para comprobar el escape HTML de campos dinámicos.",
        hook_paragraphs=[
            'Párrafo con payload <script>alert("xss")</script> que debe quedar neutralizado.',
        ],
        insights_60s=[
            "Primer punto <b>seguro</b> sin inyección ejecutada en correo.",
            "Segundo punto comprobando el escape en la caja de 60 segundos.",
            "Tercer punto validando la estructura tabular ligera de Brevo.",
        ],
        ps_referral_text='P.D. Prueba <img src=x onerror=alert(1)> controlada.',
    )
    html_doc = manager._build_html_template(
        payload,
        post_title='Título <script>bad()</script>',
        post_url="https://datalaria.com/es/posts/xss-test/",
        lang="es",
        hero_image_url="https://datalaria.com/images/Datalaria_blog.png",
    )
    assert "<script>" not in html_doc
    assert "&lt;script&gt;" in html_doc
    # Única etiqueta <img> es la portada Hero oficial
    assert len(re.findall(r"<img\b[^>]*>", html_doc, flags=re.IGNORECASE)) == 1


def test_send_campaign_mock_posts_brevo_v3_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BREVO_API_KEY", "test-secret-key")
    calls = []

    def fake_post(url: str, headers=None, json=None, timeout=None):
        calls.append({"url": url, "headers": headers, "json": json})
        resp = MagicMock()
        resp.status_code = 201 if url.endswith("/emailCampaigns") else 204
        resp.json.return_value = {"id": 90210}
        return resp

    monkeypatch.setattr("autopilot.src.newsletter_manager.requests.post", fake_post)
    manager = NewsletterManager()
    payload = NewsletterContent(
        archetype="direct_framework",
        subject="Framework práctico de gobernanza editorial con Pulse",
        preheader="Cómo evitar enlaces rotos y desincronización ES/EN con Pydantic v2.",
        hook_paragraphs=[
            "Hoy compartimos la nueva arquitectura automatizada de envío editorial sin ruido.",
        ],
        insights_60s=[
            "Paridad estricta ES/EN antes de compilar Hugo en producción.",
            "Zero-Click Value directo en los primeros 60 segundos de lectura.",
            "Segmentación automática por lista de idioma en Brevo API v3.",
        ],
    )

    ok = manager.send_campaign(
        subject=payload.subject,
        intro_text=payload,
        post_title="Gobernanza Pulse",
        post_url="https://datalaria.com/en/posts/pulse-governance/",
        lang="en",
        hero_image_url="https://datalaria.com/images/Datalaria_blog.png",
    )
    assert ok is True
    assert len(calls) == 2
    assert calls[0]["json"]["previewText"] == payload.preheader
    assert calls[0]["json"]["recipients"] == {"listIds": [4]}
    assert calls[1]["url"].endswith("/emailCampaigns/90210/sendNow")
