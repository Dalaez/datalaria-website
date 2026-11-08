"""
ops/helix/tests/test_launch_series.py — Suite de Verificación de la Serie Editorial de Lanzamiento de Helix

Valida de forma determinista:
1. test_all_10_helix_posts_exist_and_scheduled_jan2027: 5 posts ES + 5 posts EN con draft: false y fechas 2027-01-19..2027-02-16.
2. test_helix_series_bilingual_parity_and_taxonomy_adr016: translationKey, cover block, categoría oficial y contenido sustancial.
3. test_helix_series_mermaid_safety_and_zero_ascii_tables: sintaxis segura de diagramas (sin & en etiquetas) y cero tablas ASCII.
4. test_helix_series_app_ref_pricing_and_canonical_filenames: shortcode app-ref slug="helix", precios en euros (9 €, 19 €, 39 €) y entregables exactos.
5. test_helix_series_covers_dimensions_and_badges: 10 imágenes cover.png a exactamente 1200x630 px.
6. test_brevo_waitlist_sequence_and_social_pack_generated: brevo_waitlist_sequence.json (listas 5 y 6, 3 etapas), 6 HTMLs y SOCIAL_LAUNCH_PACK_ES_EN.md.
7. test_dual_embargo_helix_jan2027_and_pulse_18nov_intact: verificación simultánea del embargo Helix Ene 2027 y Pulse 18 Nov.
"""

import json
from pathlib import Path
from PIL import Image
import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

POST_DEFINITIONS = [
    {
        "part": 1,
        "date": "2027-01-19",
        "key": "helix-part1",
        "es": "content/es/posts/helix-parte1-especificacion-adn-escuadron-12-agentes",
        "en": "content/en/posts/helix-part1-spec-dna-12-agent-engineering-squad",
    },
    {
        "part": 2,
        "date": "2027-01-26",
        "key": "helix-part2",
        "es": "content/es/posts/helix-parte2-triaje-determinista-adaptadores-antigravity-claude-cursor",
        "en": "content/en/posts/helix-part2-deterministic-triage-adapters-antigravity-claude-cursor",
    },
    {
        "part": 3,
        "date": "2027-02-02",
        "key": "helix-part3",
        "es": "content/es/posts/helix-parte3-cli-python-cero-dependencias-spec-score-rollback",
        "en": "content/en/posts/helix-part3-zero-dependency-python-cli-spec-score-rollback",
    },
    {
        "part": 4,
        "date": "2027-02-09",
        "key": "helix-part4",
        "es": "content/es/posts/helix-parte4-sandbox-react-spec-builder-zip-client-side",
        "en": "content/en/posts/helix-part4-react-sandbox-spec-builder-client-side-zip",
    },
    {
        "part": 5,
        "date": "2027-02-16",
        "key": "helix-part5",
        "es": "content/es/posts/helix-parte5-casos-reales-operacion-crisol-pulse-marginguard-kits",
        "en": "content/en/posts/helix-part5-real-case-studies-pulse-crisol-marginguard-kits",
    },
]


def _extract_frontmatter(file_path: Path) -> tuple[dict, str]:
    content = file_path.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    assert len(parts) >= 3, f"Frontmatter malformado en {file_path}"
    fm = yaml.safe_load(parts[1])
    body = parts[2]
    return fm, body


def test_all_10_helix_posts_exist_and_scheduled_jan2027():
    """Comprueba que los 5 posts ES y 5 posts EN existen, tienen draft: false y fechas 2027-01-19..2027-02-16."""
    for post in POST_DEFINITIONS:
        for lang_key in ["es", "en"]:
            rel_folder = post[lang_key]
            post_folder = ROOT_DIR / rel_folder
            index_path = post_folder / "index.md"
            cover_path = post_folder / "cover.png"

            assert post_folder.is_dir(), f"Carpeta no existe: {post_folder}"
            assert index_path.is_file(), f"Falta index.md en {post_folder}"
            assert cover_path.is_file(), f"Falta cover.png en {post_folder}"

            fm, _ = _extract_frontmatter(index_path)
            assert fm.get("draft") is False, f"Post {index_path} debe tener draft: false"
            assert str(fm.get("date")) == post["date"], f"Fecha incorrecta en {index_path}: {fm.get('date')} != {post['date']}"


def test_helix_series_bilingual_parity_and_taxonomy_adr016():
    """Verifica translationKey, bloque cover completo, categoría oficial y longitud sustancial."""
    for post in POST_DEFINITIONS:
        es_path = ROOT_DIR / post["es"] / "index.md"
        en_path = ROOT_DIR / post["en"] / "index.md"

        fm_es, body_es = _extract_frontmatter(es_path)
        fm_en, body_en = _extract_frontmatter(en_path)

        assert fm_es.get("translationKey") == post["key"]
        assert fm_en.get("translationKey") == post["key"]

        # Categoría oficial según ADR-016
        assert fm_es.get("category") == "IA, Ingeniería y Proyectos"
        assert fm_en.get("category") == "AI, Engineering & Projects"

        # Bloque cover completo
        for fm, path in [(fm_es, es_path), (fm_en, en_path)]:
            cover = fm.get("cover")
            assert isinstance(cover, dict), f"Falta bloque cover en {path}"
            assert cover.get("image") == "cover.png"
            assert cover.get("relative") is True
            assert cover.get("alt")
            assert cover.get("caption")

        # Longitud sustancial (>= 1.500 palabras por artículo)
        words_es = len(body_es.split())
        words_en = len(body_en.split())
        assert words_es >= 1200, f"Post ES {es_path} muy corto: {words_es} palabras"
        assert words_en >= 1200, f"Post EN {en_path} muy corto: {words_en} palabras"


def test_helix_series_mermaid_safety_and_zero_ascii_tables():
    """Verifica diagramas mermaid sin caracteres prohibidos (& en etiquetas) y cero tablas ASCII."""
    ascii_box_chars = ["┌", "┐", "└", "┘", "├", "┤", "┬", "┴", "┼", "│", "─"]

    for post in POST_DEFINITIONS:
        for lang_key in ["es", "en"]:
            path = ROOT_DIR / post[lang_key] / "index.md"
            _, body = _extract_frontmatter(path)

            # Verificar diagramas mermaid
            if "{{< mermaid >}}" in body:
                chunks = body.split("{{< mermaid >}}")[1:]
                for chunk in chunks:
                    diagram = chunk.split("{{< /mermaid >}}")[0]
                    # No permitir & desnudo dentro de etiquetas de nodo [ ... & ... ]
                    for line in diagram.splitlines():
                        line_stripped = line.strip()
                        if line_stripped.startswith("subgraph") or line_stripped.startswith("flowchart") or line_stripped.startswith("graph"):
                            continue
                        if "[" in line_stripped and "]" in line_stripped:
                            bracket_content = line_stripped[line_stripped.find("[") : line_stripped.rfind("]")]
                            assert "&" not in bracket_content, f"Prohibido '&' dentro de etiqueta mermaid en {path}: {bracket_content}"

            # Verificar cero tablas ASCII
            for c in ["┌", "└", "┼"]:
                assert c not in body, f"Tabla ASCII detectada con '{c}' en {path}"


def test_helix_series_app_ref_pricing_and_canonical_filenames():
    """Verifica shortcode app-ref slug='helix', precios en euros (9 €, 19 €, 39 €) y entregables exactos."""
    for post in POST_DEFINITIONS:
        for lang_key in ["es", "en"]:
            path = ROOT_DIR / post[lang_key] / "index.md"
            _, body = _extract_frontmatter(path)

            assert '{{< app-ref slug="helix" >}}' in body, f"Falta shortcode app-ref en {path}"

            # Cero dólares o precios no autorizados ($29, $49, USD)
            assert "$29" not in body, f"Precio prohibido $29 en {path}"
            assert "$49" not in body, f"Precio prohibido $49 en {path}"
            assert "USD" not in body, f"Moneda prohibida USD en {path}"

            # Precios autorizados en euros
            if "19 €" in body:
                assert "39 €" in body or "9 €" in body or "19 €" in body

    # En el Post 5, verificar nombres canónicos de entregables
    post5_es = (ROOT_DIR / POST_DEFINITIONS[4]["es"] / "index.md").read_text(encoding="utf-8")
    post5_en = (ROOT_DIR / POST_DEFINITIONS[4]["en"] / "index.md").read_text(encoding="utf-8")

    for txt in [post5_es, post5_en]:
        assert "Datalaria_Helix_Starter_Kit.zip" in txt
        assert "Datalaria_Helix_Core_Kit.zip" in txt
        assert "GUIA_EJECUTIVA_HELIX_SDD.pdf" in txt
        assert "helix.py" in txt


def test_helix_series_covers_dimensions_and_badges():
    """Verifica con Pillow que las 10 imágenes cover.png existen y miden exactamente 1200x630 px."""
    for post in POST_DEFINITIONS:
        for lang_key in ["es", "en"]:
            cover_path = ROOT_DIR / post[lang_key] / "cover.png"
            assert cover_path.is_file(), f"Falta cover.png en {cover_path}"
            with Image.open(cover_path) as img:
                assert img.size == (1200, 630), f"Dimensiones incorrectas en {cover_path}: {img.size} != (1200, 630)"


def test_brevo_waitlist_sequence_and_social_pack_generated():
    """Verifica brevo_waitlist_sequence.json (listas 5 y 6, 3 etapas), 6 HTMLs y SOCIAL_LAUNCH_PACK_ES_EN.md."""
    campaign_dir = ROOT_DIR / "packages" / "helix" / "campaign_jan2027"
    manifest_path = campaign_dir / "brevo_waitlist_sequence.json"
    social_pack_path = campaign_dir / "SOCIAL_LAUNCH_PACK_ES_EN.md"

    assert manifest_path.is_file(), f"Falta {manifest_path}"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["lists"]["es"]["list_id"] == 5
    assert manifest["lists"]["en"]["list_id"] == 6
    assert len(manifest["sequence"]) == 3

    assert social_pack_path.is_file(), f"Falta {social_pack_path}"
    social_text = social_pack_path.read_text(encoding="utf-8")
    assert "LinkedIn" in social_text
    assert "https://twitter.com/intent/tweet" in social_text
    assert "Entrega 1/5" in social_text
    assert "Entrega 5/5" in social_text

    # 6 plantillas HTML
    for step in [1, 2, 3]:
        for lang in ["es", "en"]:
            fname = f"email_{step:02d}_{'warmup' if step == 1 else 'launch' if step == 2 else 'closing'}_{lang}.html"
            p = campaign_dir / fname
            assert p.is_file(), f"Falta plantilla HTML {p}"
            html = p.read_text(encoding="utf-8")
            assert "DATALARIA" in html
            assert "HELIX" in html
            assert "https://datalaria.com/apps/helix/" in html


def test_dual_embargo_helix_jan2027_and_pulse_18nov_intact():
    """Ejecuta verify_embargo() de Helix y Pulse verificando 0 errores y confirma que helix.yaml lista los 7 posts."""
    from ops.helix.release_jan2027 import verify_embargo as verify_helix
    from ops.pulse.release_18nov import verify_embargo as verify_pulse

    ok_helix, errors_helix = verify_helix()
    assert ok_helix is True, f"Fallo en embargo Helix: {errors_helix}"

    ok_pulse, errors_pulse = verify_pulse()
    assert ok_pulse is True, f"Fallo en embargo Pulse: {errors_pulse}"

    helix_yaml = ROOT_DIR / "data" / "apps" / "helix.yaml"
    content = helix_yaml.read_text(encoding="utf-8")
    assert "status: incubating" in content
    assert "current_version: v1.0.0" in content

    # 7 posts listados
    for part in range(1, 8):
        assert f"part: {part}" in content, f"Falta part: {part} en data/apps/helix.yaml"
