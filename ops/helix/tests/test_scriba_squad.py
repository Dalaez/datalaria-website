"""Suite de pruebas deterministas para el Escuadrón Editorial Datalaria Scriba (Hito 7.1 / ADR-020)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from ops.helix.build_adapters import build_editorial_adapters
from ops.helix.models import (
    EXPECTED_EDITORIAL_AGENT_IDS,
    MAX_AGENT_SPEC_LINES,
    MAX_FRICTION_RULES,
    AgentSpecDocument,
    AgentSpecFrontmatter,
    calculate_editorial_triage,
    load_editorial_squad_specs,
)


def test_all_8_scriba_specs_valid_pydantic() -> None:
    """Verifica que las 8 fichas en specs/squad-editorial/ existen y cumplen el contrato Pydantic v2."""
    docs = load_editorial_squad_specs(Path("specs/squad-editorial"))
    assert len(docs) == 8
    assert tuple(d.frontmatter.id for d in docs) == EXPECTED_EDITORIAL_AGENT_IDS

    for d in docs:
        fp = Path(d.source_path)
        lines = fp.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= MAX_AGENT_SPEC_LINES, (
            f"Ficha editorial {d.frontmatter.id} excede {MAX_AGENT_SPEC_LINES} líneas ({len(lines)} líneas)."
        )
        assert d.total_lines <= MAX_AGENT_SPEC_LINES
        assert "## 6. Reglas de Fricción Real y Correcciones" in d.body_markdown


def test_scriba_veto_separation() -> None:
    """INV-HELIX-1 aplicado a Scriba: Solo E07-editorial-qa tiene veto y cell assurance; constructores sin veto."""
    docs = load_editorial_squad_specs(Path("specs/squad-editorial"))
    veto_ids = {d.frontmatter.id for d in docs if d.frontmatter.has_veto_power}
    assert veto_ids == {"E07-editorial-qa"}

    for d in docs:
        if d.frontmatter.cell == "construction":
            assert d.frontmatter.has_veto_power is False
            assert d.frontmatter.can_write_production_code is True
        if d.frontmatter.has_veto_power:
            assert d.frontmatter.can_write_production_code is False
            assert d.frontmatter.cell == "assurance"

    # Verificar que el validador Pydantic rechaza un constructor editorial con veto
    with pytest.raises(ValidationError):
        AgentSpecFrontmatter(
            id="E03-technical-writer",
            name_es="Redactor Técnico",
            name_en="Technical Writer",
            cell="construction",
            icon="✍️",
            activates_on_sizes=["S"],
            mandatory_triggers=["content_es"],
            can_write_production_code=True,
            has_veto_power=True,
            inputs=["topic"],
            outputs=["index.md"],
        )


def test_build_editorial_adapters_generates_18_artifacts() -> None:
    """build_editorial_adapters genera los 18 artefactos (.agents, .claude, .cursor y manifest.json de Scriba)."""
    generated = build_editorial_adapters(Path("."), check_only=False)
    assert len(generated) == 18  # 8 .agents + 8 .claude + 1 manifest.json + 1 .cursor/rules/scriba-squad.mdc

    manifest_path = Path(".agents/squad-editorial/manifest.json")
    assert manifest_path.exists()
    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest_data["total_agents"] == 8
    assert "Scriba" in manifest_data["squad"]

    claude_qa = Path(".claude/agents/E07-editorial-qa.md").read_text(encoding="utf-8")
    assert "DO NOT EDIT MANUALLY (INV-HELIX-4)" in claude_qa
    assert "Edit, Write" not in claude_qa  # QA Verifier editorial no tiene permiso de escritura directa

    cursor_rule = Path(".cursor/rules/scriba-squad.mdc").read_text(encoding="utf-8")
    assert "globs:" in cursor_rule
    assert "E01-editorial-orchestrator" in cursor_rule


def test_build_editorial_adapters_idempotency_and_check_mode() -> None:
    """El modo --check pasa sin errores cuando los adaptadores editoriales están sincronizados."""
    checked = build_editorial_adapters(Path("."), check_only=True)
    assert len(checked) == 18


def test_editorial_triage_rubric_and_card() -> None:
    """Verifica que el triaje editorial y la tarjeta TRIAGE SCRIBA cumplen el contrato de 6 líneas."""
    xs = calculate_editorial_triage(
        task_id="7.2-fix",
        estimated_posts=1,
        surfaces=["content_es"],
    )
    assert xs.size == "XS"
    assert "E01-editorial-orchestrator" in xs.active_agents
    assert "E07-editorial-qa" in xs.active_agents
    assert xs.requires_human_approval is False

    brevo_task = calculate_editorial_triage(
        task_id="7.4-nl",
        estimated_posts=2,
        surfaces=["newsletter_brevo"],
    )
    assert "E05-content-monetizer" in brevo_task.active_agents
    assert "E07-editorial-qa" in brevo_task.active_agents

    social_task = calculate_editorial_triage(
        task_id="7.5-social",
        estimated_posts=2,
        surfaces=["social_syndication"],
    )
    assert "E06-social-syndicator" in social_task.active_agents

    card = brevo_task.format_triage_card()
    lines = card.splitlines()
    assert len(lines) == 6
    assert lines[0].startswith("TRIAGE SCRIBA · Tarea 7.4-nl · Talla:")
    assert "Roles activados" in lines[2]
    assert "Verification Gate:" in lines[4]


def test_agents_md_section_6_and_decisions_adr_020() -> None:
    """Verifica que AGENTS.md §6, CLAUDE.md y specs/DECISIONS.md contienen la especificación de Scriba."""
    agents_md = Path("AGENTS.md").read_text(encoding="utf-8")
    assert "## 6. ESCUADRÓN EDITORIAL DATALARIA SCRIBA Y PROTOCOLO DEL SUPEREQUIPO" in agents_md
    assert "/specs/squad-editorial/" in agents_md

    claude_md = Path("CLAUDE.md").read_text(encoding="utf-8")
    assert "specs/squad-editorial/" in claude_md

    decisions_md = Path("specs/DECISIONS.md").read_text(encoding="utf-8")
    assert "## ADR-020:" in decisions_md


def test_no_editorial_adapters_leaked_into_static() -> None:
    """Invariante de seguridad: Ningún adaptador editorial o script debe filtrarse a static/."""
    static_dir = Path("static")
    forbidden_suffixes = {".py", ".sql", ".env", ".pyc", ".mdc"}
    leaked = [
        p.as_posix()
        for p in static_dir.rglob("*")
        if p.is_file() and (p.suffix.lower() in forbidden_suffixes or "scriba" in p.name.lower())
    ]
    assert not leaked, f"Archivos prohibidos detectados en static/: {leaked}"
