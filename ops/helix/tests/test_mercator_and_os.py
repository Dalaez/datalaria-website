"""Suite de pruebas deterministas para Datalaria OS (Capa 0) y Escuadrón Datalaria Mercator (Hito 9.1 / ADR-034)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from ops.helix.build_adapters import (
    build_adapters,
    build_editorial_adapters,
    build_mercator_adapters,
    build_os_adapters,
)
from ops.helix.models import (
    EXPECTED_MERCATOR_AGENT_IDS,
    EXPECTED_OS_AGENT_IDS,
    MAX_AGENT_SPEC_LINES,
    AgentSpecFrontmatter,
    calculate_mercator_triage,
    load_mercator_squad_specs,
    load_os_specs,
)

VALID_BRAND_VERTICALS = {"executive_b2b", "ai_systems", "open_lab"}


def test_strategy_and_brand_docs_anti_bloat_limit() -> None:
    """Verifica que specs/STRATEGY.md y specs/_brand.md existen y cumplen el límite <= 80 líneas."""
    for rel_path, expected_token in (
        ("specs/STRATEGY.md", "500 €/mes"),
        ("specs/_brand.md", "executive_b2b"),
    ):
        fp = Path(rel_path)
        assert fp.exists(), f"Falta documento estratégico obligatorio: {rel_path}"
        content = fp.read_text(encoding="utf-8")
        lines = content.splitlines()
        assert len(lines) <= 80, f"{rel_path} excede 80 líneas ({len(lines)} líneas)."
        assert expected_token in content


def test_os_and_mercator_specs_valid_pydantic_and_anti_bloat() -> None:
    """Valida Capa 0 (00-chief-orchestrator) y Mercator (M01..M04) contra Pydantic v2 e INV-HELIX-8."""
    os_docs = load_os_specs(Path("specs/squad-os"))
    assert len(os_docs) == 1
    assert tuple(d.frontmatter.id for d in os_docs) == EXPECTED_OS_AGENT_IDS
    assert os_docs[0].frontmatter.can_write_production_code is False
    assert os_docs[0].frontmatter.has_veto_power is False
    assert os_docs[0].total_lines <= MAX_AGENT_SPEC_LINES

    merc_docs = load_mercator_squad_specs(Path("specs/squad-mercator"))
    assert len(merc_docs) == 4
    assert tuple(d.frontmatter.id for d in merc_docs) == EXPECTED_MERCATOR_AGENT_IDS
    for d in merc_docs:
        lines = Path(d.source_path).read_text(encoding="utf-8").splitlines()
        assert len(lines) <= MAX_AGENT_SPEC_LINES, (
            f"Ficha Mercator {d.frontmatter.id} excede {MAX_AGENT_SPEC_LINES} líneas ({len(lines)})."
        )
        assert d.frontmatter.has_veto_power is False, (
            f"Violación INV-OS-2: {d.frontmatter.id} no puede tener veto propio; reutiliza 10/11/E07."
        )
        if d.frontmatter.cell == "construction":
            assert d.frontmatter.can_write_production_code is True
        else:
            assert d.frontmatter.can_write_production_code is False


def test_inv_os_2_rejects_mercator_or_os_veto_duplication() -> None:
    """INV-OS-2 / INV-HELIX-1: Pydantic rechaza otorgar has_veto_power=True a agentes de OS o Mercator."""
    for bad_id in ("00-chief-orchestrator", "M01-revenue-orchestrator", "M02-cro-pricing-revops"):
        with pytest.raises(ValidationError):
            AgentSpecFrontmatter(
                id=bad_id,
                name_es="Agente de prueba",
                name_en="Test Agent",
                cell="direction",
                icon="💰",
                activates_on_sizes=["L"],
                mandatory_triggers=["TRG-CRO"],
                can_write_production_code=False,
                has_veto_power=True,
                inputs=["specs/STRATEGY.md"],
                outputs=["report"],
            )


def test_build_os_and_mercator_adapters_preserves_helix_and_scriba() -> None:
    """Compila adaptadores de OS (4) y Mercator (10) preservando intactos Helix (26) y Scriba (18)."""
    helix_gen = build_adapters(Path("."), check_only=True)
    assert len(helix_gen) == 26

    scriba_gen = build_editorial_adapters(Path("."), check_only=True)
    assert len(scriba_gen) == 18

    os_gen = build_os_adapters(Path("."), check_only=False)
    assert len(os_gen) == 4
    assert len(build_os_adapters(Path("."), check_only=True)) == 4

    merc_gen = build_mercator_adapters(Path("."), check_only=False)
    assert len(merc_gen) == 10
    assert len(build_mercator_adapters(Path("."), check_only=True)) == 10

    os_rule = Path(".cursor/rules/datalaria-os.mdc").read_text(encoding="utf-8")
    assert "alwaysApply: false" in os_rule
    assert "00-chief-orchestrator" in os_rule

    merc_manifest = json.loads(Path(".agents/squad-mercator/manifest.json").read_text(encoding="utf-8"))
    assert merc_manifest["total_agents"] == 4
    assert merc_manifest["reused_veto_agents"] == ["10-security-privacy", "11-qa-verifier", "E07-editorial-qa"]

    claude_m01 = Path(".claude/agents/M01-revenue-orchestrator.md").read_text(encoding="utf-8")
    assert "DO NOT EDIT MANUALLY (INV-HELIX-4)" in claude_m01
    assert "Edit, Write" not in claude_m01


def test_mercator_triage_algorithm_and_6_line_card() -> None:
    """Verifica el triaje comercial determinista, triggers y tarjeta TRIAGE MERCATOR de 6 líneas."""
    xs = calculate_mercator_triage(
        campaign_id="9.3-cta",
        estimated_files=1,
        surfaces=["lifecycle_brevo"],
    )
    assert xs.size == "XS"
    assert xs.active_agents == ["M01-revenue-orchestrator", "M03-lifecycle-retention"]
    assert xs.reused_veto_agents == ["E07-editorial-qa"]
    assert xs.requires_human_approval is False

    sprint = calculate_mercator_triage(
        campaign_id="9.3-pack-obs",
        estimated_files=6,
        surfaces=["cro_pricing", "lifecycle_brevo", "external_dist"],
        is_commercial_sprint=True,
    )
    assert sprint.size == "L"
    assert len(sprint.active_agents) == 4
    assert sprint.reused_veto_agents == ["10-security-privacy", "11-qa-verifier", "E07-editorial-qa"]
    assert sprint.requires_human_approval is True

    card = sprint.format_triage_card()
    lines = card.splitlines()
    assert len(lines) == 6
    assert lines[0] == "TRIAGE MERCATOR · Campaña 9.3-pack-obs · Talla: L"
    assert "+ Veto:" in lines[2]
    assert "Verification Gate:" in lines[4]


def test_governance_docs_harmonization_and_brand_vertical_in_app_yamls() -> None:
    """Verifica Constitución v1.2.0 Art. 10, ADR-034, AGENTS.md §7, CLAUDE.md, E04 SEO y 10 data/apps/*.yaml."""
    constitution = Path("specs/_constitution.md").read_text(encoding="utf-8")
    assert "Versión:** 1.2.0" in constitution
    assert "## Artículo 10: Federación `Datalaria OS`" in constitution

    decisions = Path("specs/DECISIONS.md").read_text(encoding="utf-8")
    assert "## ADR-034:" in decisions

    agents_md = Path("AGENTS.md").read_text(encoding="utf-8")
    assert "## 7. DATALARIA OS (CAPA 0) Y ESCUADRÓN DATALARIA MERCATOR" in agents_md
    assert "/specs/squad-mercator/" in agents_md

    claude_md = Path("CLAUDE.md").read_text(encoding="utf-8")
    assert "specs/squad-os/" in claude_md
    assert "specs/squad-mercator/" in claude_md

    e04 = Path("specs/squad-editorial/E04-bilingual-seo-editor.md").read_text(encoding="utf-8")
    assert "35–95" in e04
    assert "140–160" in e04

    app_yamls = sorted(Path("data/apps").glob("*.yaml"))
    assert len(app_yamls) == 10
    for fp in app_yamls:
        data = yaml.safe_load(fp.read_text(encoding="utf-8"))
        assert "brand_vertical" in data, f"Falta brand_vertical en {fp.as_posix()}"
        assert data["brand_vertical"] in VALID_BRAND_VERTICALS, (
            f"brand_vertical inválido '{data['brand_vertical']}' en {fp.as_posix()}"
        )


def test_no_mercator_or_os_artifacts_leaked_into_static() -> None:
    """Firewall Art. 2: Ningún archivo de Datalaria OS o Mercator debe aparecer dentro de static/."""
    static_dir = Path("static")
    leaked = [
        p.as_posix()
        for p in static_dir.rglob("*")
        if p.is_file() and ("mercator" in p.name.lower() or "squad-os" in p.as_posix().lower())
    ]
    assert not leaked, f"Artefactos prohibidos en static/: {leaked}"
