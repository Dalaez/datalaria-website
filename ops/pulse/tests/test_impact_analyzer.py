"""
Suite de pruebas deterministas para el Motor de Impacto SEO/GA4 (Hitos 7.2 y 7.2b / ADR-020).
Incluye garantías de no fuga a static (INV-PULSE-6) e integridad cronológica (INV-SCRIBA-CHRONO).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

import frontmatter
import pytest

from ops.pulse.impact_analyzer import (
    calculate_editorial_roi_score,
    detect_monetization_orphans,
    run_impact_analysis,
)
from ops.pulse.models import PulseImpactReport


def test_impact_analyzer_execution_and_pydantic_contract() -> None:
    """Verifica que run_impact_analysis ejecuta limpiamente y genera impact_report.json válido."""
    report = run_impact_analysis()
    assert isinstance(report, PulseImpactReport)
    assert report.total_published_posts >= 98
    assert report.total_scheduled_posts >= 20
    assert report.total_30d_post_views > 1000
    assert report.median_post_views >= 5.0
    assert report.p75_post_views >= 15.0

    report_path = Path("data/pulse/private/impact_report.json")
    assert report_path.exists()

    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    validated = PulseImpactReport(**data)
    assert validated.visibility == "private"
    assert validated.total_published_posts >= 98


def test_quick_wins_ctr_titles_and_descriptions_within_optimal_bounds() -> None:
    """Verifica que los Quick Wins cumplen los rangos de caracteres óptimos (35-95 en título, 75-245 en descripción)."""
    report = run_impact_analysis()
    assert len(report.quick_wins_ctr) >= 10

    for qw in report.quick_wins_ctr:
        assert 35 <= len(qw.recommended_title_es) <= 95, (
            f"Título ES de {qw.id} ({len(qw.recommended_title_es)} chars) fuera de rango [35, 95]: '{qw.recommended_title_es}'"
        )
        assert 35 <= len(qw.recommended_title_en) <= 95, (
            f"Título EN de {qw.id} ({len(qw.recommended_title_en)} chars) fuera de rango [35, 95]: '{qw.recommended_title_en}'"
        )
        assert 75 <= len(qw.recommended_desc_es) <= 245, (
            f"Descripción ES de {qw.id} ({len(qw.recommended_desc_es)} chars) fuera de rango [75, 245]: '{qw.recommended_desc_es}'"
        )


def test_monetization_orphans_post_remediation_and_fixture_mapping() -> None:
    """
    Verifica que tras el Hito 7.2b el cuartil superior real tiene 0 huérfanos de monetización,
    y comprueba con un fixture sintético que detect_monetization_orphans asigna puentes válidos.
    """
    # 1. Catálogo real remediado en Hito 7.2b: 0 huérfanos en cuartil superior
    report = run_impact_analysis()
    assert len(report.monetization_orphans) == 0

    # 2. Fixture sintético: simular posts sin app ni kit para verificar la asignación determinista de puentes
    synthetic_posts = [
        {"id": "sdd_vs_vibe_coding", "slug": "sdd_vs_vibe_coding", "related_app": None, "related_kit": None},
        {"id": "john_von_neumann", "slug": "john_von_neumann", "related_app": None, "related_kit": None},
        {"id": "kantorovich", "slug": "kantorovich", "related_app": None, "related_kit": None},
        {"id": "kurt_godel", "slug": "kurt_godel", "related_app": None, "related_kit": None},
    ]
    synthetic_metrics = {
        "sdd_vs_vibe_coding": {"ga4_views_30d": 100, "ga4_users_30d": 50, "ga4_engagement_sec": 4000.0},
        "john_von_neumann": {"ga4_views_30d": 80, "ga4_users_30d": 60, "ga4_engagement_sec": 2000.0},
        "kantorovich": {"ga4_views_30d": 38, "ga4_users_30d": 30, "ga4_engagement_sec": 1200.0},
        "kurt_godel": {"ga4_views_30d": 30, "ga4_users_30d": 20, "ga4_engagement_sec": 2400.0},
    }
    synth_orphans = detect_monetization_orphans(synthetic_posts, synthetic_metrics, p75_views=20.0)
    assert len(synth_orphans) == 4
    orphan_ids = [o.id for o in synth_orphans]
    assert "sdd_vs_vibe_coding" in orphan_ids
    assert "john_von_neumann" in orphan_ids
    assert "kantorovich" in orphan_ids
    assert "kurt_godel" in orphan_ids

    for o in synth_orphans:
        assert o.ga4_views_30d >= 20.0
        assert o.recommended_bridge_type in {"kit_b2b", "app_sandbox", "helix_waitlist"}
        assert len(o.recommended_shortcode_or_url) > 0
        assert len(o.rationale_es) > 0


def test_category_performance_and_roi_ranking() -> None:
    """Verifica el cálculo por categorías, liderazgo de Estrategia y ascenso de Pioneros a 50% de monetización."""
    report = run_impact_analysis()
    categories = {c.category: c for c in report.category_performance}
    assert len(categories) == 5

    # Estrategia y Operaciones lidera en cobertura de monetización
    strat = categories["Estrategia y Operaciones"]
    assert strat.monetization_coverage_pct > 80.0
    assert strat.avg_views_per_post >= 25.0

    # Pioneros y Referentes alcanza 50.0% tras la intervención de Hito 7.2b
    pioneers = categories["Pioneros y Referentes"]
    assert pioneers.monetization_coverage_pct >= 45.0
    assert pioneers.avg_views_per_post >= 20.0
    assert pioneers.avg_engagement_sec >= 25.0

    # Orden descendente por editorial_roi_score
    scores = [c.editorial_roi_score for c in report.category_performance]
    assert scores == sorted(scores, reverse=True)


def test_remediated_23_posts_achieve_perfect_seo_score() -> None:
    """Verifica que los 23 posts estratégicos alcanzan seo_audit.score_0_100 == 100 sin incidencias."""
    index_path = Path("data/pulse/private/index.json")
    assert index_path.exists()
    with open(index_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assets_list = data if isinstance(data, list) else data.get("assets", [])
    assets = {a["id"]: a for a in assets_list if a.get("asset_type") == "post"}

    target_ids = [
        "abraham_wald", "alan_turing", "app-lifeops_part6_analytics_dashboard_360",
        "business-case-financiero-van-tir", "evaluacion_agentes_ia", "ex_machina",
        "graphrag", "her", "john_von_neumann", "kantorovich", "kurt_godel",
        "matriz-dar-cuantitativa", "matriz-rice-ice-priorizacion", "multiverse_computing",
        "nextail", "oppenheimer", "quantitative-porter-5-forces", "quantitative-swot-tows-matrix",
        "ravenpack", "sdd_vs_vibe_coding", "silicon_valley", "submer", "the_thinking_game"
    ]
    for pid in target_ids:
        assert pid in assets, f"Activo {pid} no encontrado en index.json"
        audit = assets[pid].get("seo_audit", {})
        score = audit.get("score_0_100", 0)
        issues = audit.get("issues", [])
        assert score == 100, f"Post {pid} tiene score={score} (issues={issues})"
        assert len(issues) == 0, f"Post {pid} tiene issues={issues}"


def test_no_published_post_links_to_scheduled_or_draft_post() -> None:
    """INV-SCRIBA-CHRONO: Ningún artículo publicado en producción contiene hipervínculos hacia posts futuros o drafts."""
    index_path = Path("data/pulse/private/index.json")
    with open(index_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assets_list = data if isinstance(data, list) else data.get("assets", [])
    posts = [a for a in assets_list if a.get("asset_type") == "post"]

    scheduled_slugs = set()
    for p in posts:
        if p.get("status") != "published":
            if p.get("url_es"):
                scheduled_slugs.add(p["url_es"].strip("/").split("/")[-1])
            if p.get("url_en"):
                scheduled_slugs.add(p["url_en"].strip("/").split("/")[-1])

    leaks: List[str] = []
    for p in posts:
        if p.get("status") == "published":
            for lang_key, base_dir in [("url_es", "content/es/posts"), ("url_en", "content/en/posts")]:
                u = p.get(lang_key)
                if not u:
                    continue
                slug = u.strip("/").split("/")[-1]
                md_path = Path(base_dir) / slug / "index.md"
                if not md_path.exists():
                    continue
                fm = frontmatter.load(md_path)
                links = re.findall(r"/(?:es|en)/posts/([^/\"\'\s)#]+)", fm.content)
                for lnk in links:
                    if lnk in scheduled_slugs:
                        leaks.append(f"{md_path.as_posix()} -> {lnk}")

    assert not leaks, f"Violación INV-SCRIBA-CHRONO: enlaces a posts futuros/drafts detectados:\n" + "\n".join(leaks)


def test_backlog_prioritization_formula_determinism() -> None:
    """Verifica el determinismo de la fórmula Editorial ROI Score y el orden del backlog."""
    # 0.40 * 80 + 0.35 * 90 + 0.25 * 70 = 32.0 + 31.5 + 17.5 = 81.0
    assert calculate_editorial_roi_score(80.0, 90.0, 70.0) == 81.0
    assert calculate_editorial_roi_score(92.0, 96.0, 98.0) == 94.9

    report = run_impact_analysis()
    assert len(report.prioritized_backlog) == 6

    # Verificar orden descendente
    scores = [b.editorial_roi_score for b in report.prioritized_backlog]
    assert scores == sorted(scores, reverse=True)

    # La idea de subagentes y contratos SDD lidera
    assert report.prioritized_backlog[0].id == "idea-claude-subagents-sdd-contracts"


def test_executive_markdown_report_generated_and_complete() -> None:
    """Verifica que specs/audit/IMPACT_REPORT.md existe y contiene las secciones requeridas."""
    report_md_path = Path("specs/audit/IMPACT_REPORT.md")
    assert report_md_path.exists()
    content = report_md_path.read_text(encoding="utf-8")

    assert "# 📈 Primera Auditoría Estratégica de Impacto SEO" in content
    assert "E02-seo-impact-strategist" in content
    assert "Quick Wins de CTR" in content
    assert "Huérfanos de Monetización" in content
    assert "Editorial ROI Score" in content
    assert "flowchart TD" in content


def test_inv_pulse_6_impact_report_never_leaked_to_static() -> None:
    """INV-PULSE-6: impact_report.json es de visibilidad privada y nunca se filtra a static/."""
    report = run_impact_analysis()
    assert report.visibility == "private"

    static_dir = Path("static")
    leaked = [
        p.as_posix()
        for p in static_dir.rglob("*")
        if p.is_file() and ("impact_report" in p.name.lower() or p.suffix.lower() == ".py")
    ]
    assert not leaked, f"Archivos privados detectados en static/: {leaked}"
