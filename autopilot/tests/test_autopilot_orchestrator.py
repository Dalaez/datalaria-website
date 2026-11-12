"""Tests unitarios end-to-end offline de orchestrator.py, embargo e higiene SDD."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from autopilot.src import brain
from autopilot.src.orchestrator import (
    REPO_ROOT,
    resolve_hero_image_url,
    resolve_secondary_cta,
    run_orchestration,
)
from autopilot.src.quality_validator import audit_social_bundle


def test_social_pack_yaml_priority_over_overrides_and_brain(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    post_dir = tmp_path / "content" / "es" / "posts" / "demo-pack"
    post_dir.mkdir(parents=True)
    post_file = post_dir / "index.md"
    post_file.write_text(
        "---\ntitle: Demo Prioridad Social Pack\ndate: 2026-10-01\nsocial_text: Frontmatter ignorable\n---\n\n## Bloque 1\nTexto de ejemplo para prueba unitaria.\n",
        encoding="utf-8",
    )
    pack_file = post_dir / "social_pack.yaml"
    pack_data = {
        "es": {
            "x": {
                "hook": "Gancho oficial desde social_pack.yaml diseñado por E06.",
                "thread": [
                    "1/4 Primer tweet curado en design-time por E06.",
                    "2/4 Segundo tweet con métrica real y contexto claro.",
                    "3/4 Tercer tweet detallando arquitectura reproducible.",
                    "4/4 Cuarto tweet de cierre hacia Datalaria.",
                ],
                "hashtags": ["Datalaria", "SDD"],
            },
            "linkedin": {
                "text": "Gancho desde social_pack.yaml.\n\nPivote concreto de arquitectura.\n\n¿Qué opinión te merece este enfoque?",
            },
            "newsletter": {
                "archetype": "real_case_number",
                "subject": "3 decisiones reales detrás de nuestro social_pack.yaml",
                "preheader": "Preheader curado por E05 para validar prioridad #1 frente a overrides.",
                "hook_paragraphs": [
                    "Párrafo curado manualmente en design-time para demostrar que social_pack.yaml manda.",
                    "Añadimos un segundo párrafo con profundidad técnica para garantizar legibilidad en Brevo.",
                ],
                "insights_60s": [
                    "Design-time desacoplado de la ejecución automática de CI.",
                    "Validación previa con Pydantic v2 antes de llegar a producción.",
                    "Coste cero garantizado en X mediante Web Intent y threads.",
                ],
            },
        }
    }
    pack_file.write_text(yaml.safe_dump(pack_data, allow_unicode=True), encoding="utf-8")

    monkeypatch.setenv("ENABLE_TWITTER", "true")
    monkeypatch.setenv("ENABLE_LINKEDIN", "true")
    monkeypatch.setenv("ENABLE_NEWSLETTER", "true")
    monkeypatch.setenv("TWITTER_OVERRIDE", "Override que debe quedar por debajo")
    monkeypatch.setenv("LINKEDIN_OVERRIDE", "Override LinkedIn ignorado")

    cache_path = tmp_path / "generated_content.json"
    result = run_orchestration(str(post_file), dry_run=True, cache_file=str(cache_path))

    assert result["x"]["hook"] == "Gancho oficial desde social_pack.yaml diseñado por E06."
    assert result["x"]["web_intent_url"].startswith("https://x.com/intent/tweet?")
    assert "social_pack.yaml" in result["linkedin"]
    assert result["newsletter"]["subject"] == "3 decisiones reales detrás de nuestro social_pack.yaml"
    assert result["audit_report"]["overall_status"] == "PASS"


def test_brain_offline_deterministic_fallback_passes_qa(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    sample_md = (
        "## Diagnóstico inicial\n"
        "La separación entre cálculo determinista y síntesis con IA evita errores costosos.\n\n"
        "## Arquitectura escalable\n"
        "Usar contratos tipados garantiza estabilidad continua en cada despliegue.\n\n"
        "## Checklist final\n"
        "Valida siempre cada cambio con tests automáticos antes de publicar.\n"
    )
    post_url = "https://datalaria.com/es/posts/offline-demo/"
    x_pack = brain.generate_x_thread_pack(
        "Arquitectura SDD Offline", sample_md, lang="es", post_url=post_url
    )
    li_text = brain.generate_linkedin_copy("Arquitectura SDD Offline", sample_md, lang="es")
    nl_payload = brain.generate_newsletter_payload(
        "Arquitectura SDD Offline", sample_md, slug="offline-demo", lang="es"
    )

    audit = audit_social_bundle(
        x_pack=x_pack,
        linkedin_text=li_text,
        newsletter_payload=nl_payload,
        post_url=post_url,
    )
    assert audit.overall_status == "PASS"


def test_resolve_hero_image_url_variants(tmp_path: Path) -> None:
    # 1. Ruta absoluta bajo /images/...
    url_abs = resolve_hero_image_url(
        "autopilot/content/sample_post.md",
        {"image": "/images/posts/ai-bpmn-sop-process.jpg"},
        lang="es",
        slug="sample_post",
    )
    assert url_abs == "https://datalaria.com/images/posts/ai-bpmn-sop-process.jpg"

    # 2. Portada cover.png real dentro de content/es/posts/...
    real_post = REPO_ROOT / "content" / "es" / "posts" / "matriz-dar-cuantitativa" / "index.md"
    if real_post.is_file():
        url_bundle = resolve_hero_image_url(str(real_post), {}, lang="es", slug="matriz-dar-cuantitativa")
        assert url_bundle.startswith(
            "https://raw.githubusercontent.com/Dalaez/datalaria-website/main/content/es/posts/matriz-dar-cuantitativa/cover."
        )

    # 3. Fallback limpio cuando no existe cover ni image
    empty_post = tmp_path / "index.md"
    empty_post.write_text("---\ntitle: Vacío\n---\nTexto", encoding="utf-8")
    assert (
        resolve_hero_image_url(str(empty_post), {}, lang="es", slug="vacio")
        == "https://datalaria.com/images/Datalaria_blog.png"
    )


def test_secondary_cta_blocks_incubating_apps_and_allows_live_apps() -> None:
    # helix.yaml y pulse.yaml están en status: incubating -> deben ser bloqueados por INV-AUTO-6
    label_helix, url_helix = resolve_secondary_cta('Texto con {{< app-ref slug="helix" >}}', lang="es")
    assert url_helix == "https://datalaria.com/es/recursos/"
    assert "recursos" in label_helix.lower()

    label_pulse, url_pulse = resolve_secondary_cta('Text with {{< app-ref slug="pulse" >}}', lang="en")
    assert url_pulse == "https://datalaria.com/en/resources/"

    # lifeops.yaml tiene status: live y demo_url con HashRouter
    label_live, url_live = resolve_secondary_cta('Prueba {{< app-ref slug="lifeops" >}}', lang="es")
    assert url_live == "https://datalaria.com/apps/lifeops/#/?mock=true"
    assert "LifeOps" in label_live


def test_dry_run_end_to_end_on_sample_post(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("BREVO_API_KEY", raising=False)
    monkeypatch.setenv("ENABLE_TWITTER", "true")
    monkeypatch.setenv("ENABLE_LINKEDIN", "true")
    monkeypatch.setenv("ENABLE_NEWSLETTER", "true")

    cache_file = tmp_path / "generated_content.json"
    sample_post = REPO_ROOT / "autopilot" / "content" / "sample_post.md"
    result = run_orchestration(str(sample_post), dry_run=True, cache_file=str(cache_file))

    assert cache_file.is_file()
    saved = json.loads(cache_file.read_text(encoding="utf-8"))
    assert saved["x"]["mode"] == "zero_cost_intent"
    assert saved["x"]["web_intent_url"].startswith("https://x.com/intent/tweet?")
    assert 4 <= len(saved["x"]["thread"]) <= 6
    assert saved["newsletter"]["list_id"] == 3
    assert len(saved["newsletter"]["insights_60s"]) == 3
    assert result["audit_report"]["overall_status"] == "PASS"


def test_deprecated_files_and_heavy_deps_removed() -> None:
    assert not (REPO_ROOT / "autopilot" / "ctrl").exists()
    assert not (REPO_ROOT / "autopilot" / "main_OLD_DEPRECATED.py").exists()
    assert not (REPO_ROOT / "autopilot" / "src" / "agents_OLD_DEPRECATED.py").exists()
    assert not (REPO_ROOT / "autopilot" / "src" / "tasks_OLD_DEPRECATED.py").exists()

    reqs = (REPO_ROOT / "autopilot" / "requirements.txt").read_text(encoding="utf-8").lower()
    assert "crewai" not in reqs
    assert "langchain-google-genai" not in reqs
    assert "pydantic" in reqs
    assert "pytest" in reqs


def test_hugo_firewall_blocks_social_pack_and_static_clean() -> None:
    config_text = (REPO_ROOT / "config.yaml").read_text(encoding="utf-8")
    config_data = yaml.safe_load(config_text)
    ignore_files = config_data.get("ignoreFiles", [])
    assert any("social_pack" in str(item) for item in ignore_files)

    static_dir = REPO_ROOT / "static"
    assert not any(
        "autopilot" in p.as_posix().lower() or "social_pack" in p.name.lower()
        for p in static_dir.rglob("*")
    )
