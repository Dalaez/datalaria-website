"""Tests unitarios deterministas y offline para markdown_syndicator y CoderLegion (Hito 7.4)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import MagicMock

import pytest
import yaml

from autopilot.src.markdown_syndicator import (
    REPO_ROOT,
    build_syndication_artifact,
    transform_markdown_for_syndication,
)
from autopilot.src.models import SyndicationArtifact, normalize_syndication_tags
from autopilot.src.orchestrator import load_post_content, run_orchestration
from autopilot.src.quality_validator import audit_markdown_syndication
from autopilot.src.social_manager import SocialMediaManager


def test_transform_all_hugo_shortcodes() -> None:
    raw = """
Intro text with {{< ref "posts/guia-anterior" >}} link.

{{< mermaid >}}
flowchart LR
    A[Start] --> B[End]
{{< /mermaid >}}

{{< helix-waitlist >}}

{{< product-card
    title="Suite 01 Estrategia"
    price="19 €"
    original_price="29 €"
    subtitle="DAFO + CAME en Excel"
    checkout_url="https://datalaria.lemonsqueezy.com/checkout/buy/demo"
    guide_url="/es/posts/dafo-cuantitativo-matriz-came/"
    button_text="Descargar Kit"
    items="Plantilla Excel;Manual PDF" >}}
Incluye casos reales listos para comité.
{{< /product-card >}}

{{< product-card title="Mini Kit" price="9 €" guide_url="/es/recursos/" >}}

{{< bundle-card title="Pack Completo" price="39 €" checkout_url="https://datalaria.lemonsqueezy.com/checkout/buy/bundle" >}}

{{< youtube dQw4w9WgXcQ >}}
{{< youtube id="abc123XYZ" >}}
{{< buymeacoffee username="datalaria" >}}
"""
    rendered = transform_markdown_for_syndication(
        raw,
        "content/es/posts/demo-shortcodes/index.md",
        platform="devto",
        lang="es",
        slug="demo-shortcodes",
        canonical_url="https://datalaria.com/es/posts/demo-shortcodes/",
    )

    assert "```mermaid" in rendered
    assert "A[Start] --> B[End]" in rendered
    assert "{{" not in rendered
    assert "utm_content=helix_waitlist#software" in rendered
    assert "https://datalaria.com/es/recursos/" in rendered
    assert "Suite 01 Estrategia" in rendered
    assert "**19 €** ~~29 €~~" in rendered
    assert "https://datalaria.lemonsqueezy.com/checkout/buy/demo" in rendered
    assert "utm_source=devto" in rendered
    assert "https://datalaria.com/es/posts/dafo-cuantitativo-matriz-came/" in rendered
    assert "Mini Kit" in rendered
    assert "Pack Completo" in rendered
    assert "https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg" in rendered
    assert "https://www.youtube.com/watch?v=abc123XYZ" in rendered
    assert "https://www.buymeacoffee.com/datalaria" in rendered
    assert "*Publicado originalmente en [Datalaria](" in rendered


def test_images_with_titles_root_paths_and_code_fence_protection() -> None:
    raw = """
![Diagrama local](preview-pack.png "Arquitectura Dual")
![Logo global](/images/Datalaria_blog.png "Brand")

```python
# Snippet literal que NO debe mutarse:
sample = "{{< helix-waitlist >}}"
img = "![Raw](local.png)"
link = "[Relative](other-post)"
```
"""
    rendered = transform_markdown_for_syndication(
        raw,
        "content/en/posts/fence-test/index.md",
        platform="coderlegion",
        lang="en",
        slug="fence-test",
        canonical_url="https://datalaria.com/en/posts/fence-test/",
    )

    assert (
        '![Diagrama local](https://raw.githubusercontent.com/Dalaez/datalaria-website/main/content/en/posts/fence-test/preview-pack.png "Arquitectura Dual")'
        in rendered
    )
    assert '![Logo global](https://datalaria.com/images/Datalaria_blog.png "Brand")' in rendered
    assert 'sample = "{{< helix-waitlist >}}"' in rendered
    assert 'img = "![Raw](local.png)"' in rendered
    assert 'link = "[Relative](other-post)"' in rendered


def test_utm_injection_preserves_hashrouter_anchors_and_external_urls() -> None:
    raw = """
- [Sandbox LifeOps](/apps/lifeops/#/?mock=true)
- [Ir a sección](#arquitectura)
- [Checkout](https://datalaria.lemonsqueezy.com/checkout/buy/abc)
- [Repo](https://github.com/Dalaez/datalaria-website)
"""
    rendered = transform_markdown_for_syndication(
        raw,
        "content/en/posts/utm-test/index.md",
        platform="coderlegion",
        lang="en",
        slug="utm-test",
        canonical_url="https://datalaria.com/en/posts/utm-test/",
    )

    assert (
        "https://datalaria.com/apps/lifeops/?utm_source=coderlegion&utm_medium=syndication&utm_campaign=utm-test#/?mock=true"
        in rendered
    )
    assert "[Ir a sección](#arquitectura)" in rendered
    assert "https://datalaria.lemonsqueezy.com/checkout/buy/abc)" in rendered
    assert "utm_source=" not in rendered.split("lemonsqueezy.com")[1].splitlines()[0]
    assert "[Repo](https://github.com/Dalaez/datalaria-website)" in rendered


def test_app_ref_embargo_inv_auto_6(tmp_path: Path) -> None:
    apps_dir = tmp_path / "apps"
    apps_dir.mkdir(parents=True)
    (apps_dir / "helix.yaml").write_text(
        yaml.safe_dump({"status": "incubating", "title": {"es": "Helix", "en": "Helix"}}),
        encoding="utf-8",
    )
    (apps_dir / "lifeops.yaml").write_text(
        yaml.safe_dump(
            {
                "status": "active",
                "title": {"es": "LifeOps", "en": "LifeOps"},
                "demo_url": "/apps/lifeops/#/?mock=true",
            }
        ),
        encoding="utf-8",
    )

    raw = '{{< app-ref slug="helix" >}}\n\n{{< app-ref slug="lifeops" >}}'
    rendered = transform_markdown_for_syndication(
        raw,
        "content/es/posts/embargo-test/index.md",
        platform="devto",
        lang="es",
        slug="embargo-test",
        canonical_url="https://datalaria.com/es/posts/embargo-test/",
        apps_dir=apps_dir,
    )

    assert "/apps/helix" not in rendered
    assert "https://datalaria.com/es/recursos/?utm_source=devto" in rendered
    assert "https://datalaria.com/es/apps/lifeops/?utm_source=devto" in rendered
    assert (
        "https://datalaria.com/apps/lifeops/?utm_source=devto&utm_medium=syndication&utm_campaign=embargo-test#/?mock=true"
        in rendered
    )


def test_normalize_tags_and_social_pack_syndication_overrides(tmp_path: Path) -> None:
    assert normalize_syndication_tags(
        ["IA Generativa", "SDD & Testing!", "python-3.12", "extra", "fifth"],
        platform="devto",
        max_tags=4,
    ) == ["iagenerativa", "sddtesting", "python312", "extra"]

    assert normalize_syndication_tags(
        ["Spec Driven", "AI Agents", "Spec Driven"],
        platform="coderlegion",
        max_tags=4,
    ) == ["spec-driven", "ai-agents"]

    post_dir = tmp_path / "content" / "en" / "posts" / "override-post"
    post_dir.mkdir(parents=True)
    post_file = post_dir / "index.md"
    post_file.write_text(
        "---\ntitle: Original Title\ndate: 2026-10-01\ntags: [Generic]\n---\n\nBody text enough characters "
        + ("alpha " * 30),
        encoding="utf-8",
    )
    pack_data = {
        "en": {
            "devto": {
                "title": "Dev.to Custom Title",
                "description": "Custom Dev.to description",
                "tags": ["Python", "AI Agents", "SDD", "Clean Code", "Ignored"],
                "main_image": "hero-devto.png",
                "discussion_question": "How do you enforce specs in your repo?",
            }
        }
    }
    (post_dir / "social_pack.yaml").write_text(
        yaml.safe_dump(pack_data, allow_unicode=True),
        encoding="utf-8",
    )

    from autopilot.src.orchestrator import load_social_pack

    section = load_social_pack(str(post_file), slug="override-post", lang="en")
    assert section is not None and section.devto is not None

    artifact = build_syndication_artifact(
        "Long enough body content " + ("detail " * 25),
        str(post_file),
        platform="devto",
        lang="en",
        slug="override-post",
        post_title="Original Title",
        canonical_url="https://datalaria.com/en/posts/override-post/",
        config=section.devto,
        output_dir=tmp_path / "dist",
    )

    assert artifact.title == "Dev.to Custom Title"
    assert artifact.description == "Custom Dev.to description"
    assert artifact.tags == ["python", "aiagents", "sdd", "cleancode"]
    assert artifact.cover_image_url is not None
    assert artifact.cover_image_url.endswith("override-post/hero-devto.png")
    assert "How do you enforce specs in your repo?" in artifact.markdown
    assert artifact.output_path is not None and Path(artifact.output_path).is_file()


def test_audit_markdown_syndication_pass_and_fail_cases() -> None:
    clean_artifact = SyndicationArtifact(
        platform="devto",
        lang="en",
        slug="clean-demo",
        title="Clean Title",
        canonical_url="https://datalaria.com/en/posts/clean-demo/",
        tags=["python", "sdd"],
        markdown=(
            "> *Originally published at [Datalaria](https://datalaria.com/en/posts/clean-demo/?utm_source=devto&utm_medium=syndication&utm_campaign=clean-demo).*\n\n"
            "Detailed article content explaining deterministic architectures and verification pipelines in production systems.\n\n"
            "![Banner](https://raw.githubusercontent.com/Dalaez/datalaria-website/main/content/en/posts/clean-demo/banner.png)\n"
        ),
    )
    pass_result = audit_markdown_syndication(clean_artifact)
    assert pass_result.status == "PASS"

    broken_artifact = SyndicationArtifact(
        platform="devto",
        lang="en",
        slug="broken",
        title="Broken",
        canonical_url="http://localhost:1313/post/",
        tags=["bad-tag!", "two", "three", "four", "five"],
        markdown="{{< youtube xyz >}} ![Local](img.png) [Rel](other-post)",
    )
    fail_result = audit_markdown_syndication(broken_artifact)
    assert fail_result.status == "FAIL"
    codes = {issue.code for issue in fail_result.issues}
    assert {
        "SYNDICATION_CANONICAL_MISSING",
        "SYNDICATION_EMPTY_CONTENT",
        "SYNDICATION_RESIDUAL_SHORTCODE",
        "SYNDICATION_RELATIVE_IMAGE",
        "SYNDICATION_RELATIVE_LINK",
        "SYNDICATION_MISSING_UTM",
        "SYNDICATION_DEVTO_TAGS_INVALID",
    }.issubset(codes)


def test_social_manager_coderlegion_and_devto_http_contract(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    captured_calls: List[Dict[str, Any]] = []

    def fake_post(url: str, headers: Dict[str, str], json: Dict[str, Any], timeout: int) -> MagicMock:
        captured_calls.append({"url": url, "headers": headers, "json": json, "timeout": timeout})
        resp = MagicMock()
        resp.status_code = 201
        resp.raise_for_status.return_value = None
        resp.json.return_value = {"id": 999, "url": "https://dev.to/demo/999"}
        return resp

    monkeypatch.setattr("autopilot.src.social_manager.requests.post", fake_post)
    monkeypatch.setenv("CODERLEGION_API_KEY", "secret-cl-token-xyz")
    monkeypatch.setenv("CODERLEGION_CATEGORY_ID", "2")
    monkeypatch.setenv("DEVTO_API_KEY", "secret-devto-token-xyz")

    manager = SocialMediaManager()

    # Missing/non-HTTPS source_url must be blocked by INV-AUTO-8 before calling network
    assert manager.post_to_coderlegion("Title", "Content", "http://datalaria.com/bad") is None
    assert len(captured_calls) == 0

    cl_resp = manager.post_to_coderlegion(
        title="SDD Architecture",
        content_markdown="Published body",
        canonical_url="https://datalaria.com/en/posts/sdd/",
        cover_image_url="https://datalaria.com/images/hero.png",
        tags=["sdd", "ai"],
        description="Summary",
    )
    assert cl_resp == {"id": 999, "url": "https://dev.to/demo/999"}
    cl_call = captured_calls[0]
    assert cl_call["url"] == "https://coderlegion.com/api/v1/posts"
    assert cl_call["headers"]["X-API-Key"] == "secret-cl-token-xyz"
    assert "Authorization" not in cl_call["headers"]
    assert cl_call["json"]["source_url"] == "https://datalaria.com/en/posts/sdd/"
    assert cl_call["json"]["category_id"] == 2
    assert cl_call["json"]["cover_image_url"] == "https://datalaria.com/images/hero.png"

    devto_resp = manager.post_to_devto(
        title="Dev.to Title",
        content_markdown="Body",
        canonical_url="https://datalaria.com/en/posts/sdd/",
        tags=["python", "ai"],
        description="Short desc",
        published=False,
    )
    assert devto_resp is not None
    devto_call = captured_calls[1]
    assert devto_call["headers"]["api-key"] == "secret-devto-token-xyz"
    assert devto_call["json"]["article"]["tags"] == ["python", "ai"]
    assert devto_call["json"]["article"]["description"] == "Short desc"
    assert devto_call["json"]["article"]["published"] is False

    stdout = capsys.readouterr().out
    assert "secret-cl-token-xyz" not in stdout
    assert "secret-devto-token-xyz" not in stdout


def test_run_orchestration_dry_run_syndication_and_lang_filter(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    en_dir = tmp_path / "content" / "en" / "posts" / "demo-sync"
    en_dir.mkdir(parents=True)
    en_post = en_dir / "index.md"
    en_post.write_text(
        "---\ntitle: Demo Syndication Flow\ndate: 2026-11-12\ntags: [Architecture, AI, SDD]\n"
        "description: Complete syndication check.\n---\n\n"
        "## Core Concept\nExploring deterministic engineering pipelines.\n\n"
        "{{< mermaid >}}\ngraph LR\n  A-->B\n{{< /mermaid >}}\n\n"
        "See [Resources](/en/resources/) and ![Img](diagram.png \"Flow\").\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("ENABLE_TWITTER", "true")
    monkeypatch.setenv("ENABLE_LINKEDIN", "true")
    monkeypatch.setenv("ENABLE_NEWSLETTER", "true")
    monkeypatch.setenv("ENABLE_DEVTO", "true")
    monkeypatch.setenv("ENABLE_CODERLEGION", "true")
    monkeypatch.setenv("CODERLEGION_LANGS", "en")

    dist_out = tmp_path / "dist"
    res_en = run_orchestration(
        str(en_post),
        dry_run=True,
        cache_file=str(tmp_path / "cache_en.json"),
        dist_dir=dist_out,
    )

    assert res_en["audit_report"]["overall_status"] == "PASS"
    assert res_en["devto"] is not None
    assert res_en["coderlegion"] is not None
    devto_dist = dist_out / "dist_devto_en.md"
    cl_dist = dist_out / "dist_coderlegion_en.md"
    assert devto_dist.is_file()
    assert cl_dist.is_file()
    assert "canonical_url: https://datalaria.com/en/posts/demo-sync/" in devto_dist.read_text(encoding="utf-8")
    assert "source_url: https://datalaria.com/en/posts/demo-sync/" in cl_dist.read_text(encoding="utf-8")

    # Spanish post should skip CoderLegion when CODERLEGION_LANGS=en without failing
    es_dir = tmp_path / "content" / "es" / "posts" / "demo-sync-es"
    es_dir.mkdir(parents=True)
    es_post = es_dir / "index.md"
    es_post.write_text(
        "---\ntitle: Demo Español\ndate: 2026-11-12\ntags: [Ingenieria]\n---\n\n"
        "## Arquitectura\nContenido suficiente para validar Dev.to en español con enlaces [Recursos](/es/recursos/).\n",
        encoding="utf-8",
    )
    res_es = run_orchestration(
        str(es_post),
        dry_run=True,
        cache_file=str(tmp_path / "cache_es.json"),
        dist_dir=tmp_path / "dist_es",
    )
    assert res_es["devto"] is not None
    assert res_es["coderlegion"] is None
    assert res_es["audit_report"]["overall_status"] == "PASS"


@pytest.mark.parametrize(
    ("rel_post", "lang", "platform"),
    [
        ("content/en/posts/sdd_vs_vibe_coding/index.md", "en", "devto"),
        ("content/en/posts/sdd_vs_vibe_coding/index.md", "en", "coderlegion"),
        ("content/en/posts/corporate-strategy-mba-quantitative-framework/index.md", "en", "devto"),
        ("content/es/posts/agentes_ia_operativa_sdd/index.md", "es", "devto"),
    ],
)
def test_real_repo_posts_smoke_clean_syndication(
    rel_post: str,
    lang: str,
    platform: str,
) -> None:
    post_path = REPO_ROOT / rel_post
    if not post_path.is_file():
        pytest.skip(f"Real post not found: {post_path}")

    loaded = load_post_content(str(post_path))
    artifact = build_syndication_artifact(
        loaded["content"],
        rel_post,
        platform=platform,  # type: ignore[arg-type]
        lang=lang,  # type: ignore[arg-type]
        slug=loaded["slug"],
        post_title=loaded["title"],
        canonical_url=loaded["url"],
        post_meta=loaded["metadata"],
    )
    audit = audit_markdown_syndication(artifact)
    assert audit.status == "PASS", f"Issues on {rel_post}: {audit.issues}"
