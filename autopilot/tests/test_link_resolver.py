"""
Tests automatizados para la resolución de enlaces Markdown e imágenes en Autopilot (Dev.to).
Verifica que las rutas relativas se transformen determinísticamente a URLs canónicas
de https://datalaria.com y que los assets locales apunten a GitHub Raw.
"""

import pytest
from autopilot.src.orchestrator import resolve_markdown_links, resolve_image_urls


def test_resolve_root_relative_links():
    content = "[Florence Nightingale](/es/posts/florence-nightingale/) y [Claude Shannon](/en/posts/claude_shannon/)"
    result = resolve_markdown_links(content, "content/es/posts/test/index.md", lang="es")
    assert "[Florence Nightingale](https://datalaria.com/es/posts/florence-nightingale/)" in result
    assert "[Claude Shannon](https://datalaria.com/en/posts/claude_shannon/)" in result


def test_resolve_language_relative_links_without_slash():
    content = "[Thomas Bayes](es/posts/thomas_bayes/) y [Abraham Wald](en/posts/abraham_wald/)"
    result = resolve_markdown_links(content, "content/es/posts/test/index.md", lang="es")
    assert "[Thomas Bayes](https://datalaria.com/es/posts/thomas_bayes/)" in result
    assert "[Abraham Wald](https://datalaria.com/en/posts/abraham_wald/)" in result


def test_resolve_apps_and_resources_links():
    content = "[LifeOps](/apps/lifeops/), [Radar](es/apps/obs-management/) y [Recursos](/recursos/)"
    result = resolve_markdown_links(content, "content/es/posts/test/index.md", lang="es")
    assert "[LifeOps](https://datalaria.com/apps/lifeops/)" in result
    assert "[Radar](https://datalaria.com/es/apps/obs-management/)" in result
    assert "[Recursos](https://datalaria.com/recursos/)" in result


def test_resolve_hugo_ref_shortcodes():
    content_es = '[Post 1: La Estrategia]({{< ref "ia_agents_part1" >}}) y [Post 2]({{< ref "posts/ia_agents_part2" >}})'
    result_es = resolve_markdown_links(content_es, "content/es/posts/test/index.md", lang="es")
    assert "[Post 1: La Estrategia](https://datalaria.com/es/posts/ia_agents_part1/)" in result_es
    assert "[Post 2](https://datalaria.com/es/posts/ia_agents_part2/)" in result_es

    content_en = '[Post 1: The Strategy]({{< ref "ai_agents_part1" >}})'
    result_en = resolve_markdown_links(content_en, "content/en/posts/test/index.md", lang="en")
    assert "[Post 1: The Strategy](https://datalaria.com/en/posts/ai_agents_part1/)" in result_en


def test_resolve_downloadable_assets():
    content = "[Descargar PPTX](Nanobanana_ingenieria.pptx) y [Descargar DOCX](report.docx)"
    result = resolve_markdown_links(content, "content/es/posts/mi-post/index.md", lang="es")
    expected_pptx = "https://raw.githubusercontent.com/Dalaez/datalaria-website/main/content/es/posts/mi-post/Nanobanana_ingenieria.pptx"
    expected_docx = "https://raw.githubusercontent.com/Dalaez/datalaria-website/main/content/es/posts/mi-post/report.docx"
    assert f"[Descargar PPTX]({expected_pptx})" in result
    assert f"[Descargar DOCX]({expected_docx})" in result


def test_preserve_external_and_anchor_links():
    content = "[Google](https://google.com), [Email](mailto:hola@datalaria.com), [Ancla](#seccion)"
    result = resolve_markdown_links(content, "content/es/posts/test/index.md", lang="es")
    assert "[Google](https://google.com)" in result
    assert "[Email](mailto:hola@datalaria.com)" in result
    assert "[Ancla](#seccion)" in result


def test_nested_image_within_link_and_standalone_image():
    raw = "[![App Banner](banner.png)](/es/apps/lifeops/)\n![Standalone](diagram.png)"
    # Primero resolver imágenes
    with_images = resolve_image_urls(raw, "content/es/posts/mi-post/index.md")
    # Luego resolver enlaces
    final_result = resolve_markdown_links(with_images, "content/es/posts/mi-post/index.md", lang="es")

    expected_banner = "https://raw.githubusercontent.com/Dalaez/datalaria-website/main/content/es/posts/mi-post/banner.png"
    expected_diagram = "https://raw.githubusercontent.com/Dalaez/datalaria-website/main/content/es/posts/mi-post/diagram.png"
    
    assert f"[![App Banner]({expected_banner})](https://datalaria.com/es/apps/lifeops/)" in final_result
    assert f"![Standalone]({expected_diagram})" in final_result


def test_app_ref_shortcode_conversion():
    content_es = '{{< app-ref slug="lifeops" >}}'
    result_es = resolve_markdown_links(content_es, "content/es/posts/test/index.md", lang="es")
    assert "> 🚀 **App Oficial en Datalaria**: [Lifeops](https://datalaria.com/es/apps/lifeops/)" in result_es
    assert "[Probar Demo en Vivo](https://datalaria.com/apps/lifeops/?mock=true)" in result_es

    content_en = '{{< app-ref slug="pulse" >}}'
    result_en = resolve_markdown_links(content_en, "content/en/posts/test/index.md", lang="en")
    assert "> 🚀 **Official Datalaria App**: [Pulse](https://datalaria.com/en/apps/pulse/)" in result_en
    assert "[Try Live Demo](https://datalaria.com/apps/pulse/?mock=true)" in result_en
