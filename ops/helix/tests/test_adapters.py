"""Suite de pruebas deterministas para el Escuadrón Datalaria Helix y Compilador de Adaptadores (Hito 6.2)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from ops.helix.build_adapters import build_adapters
from ops.helix.models import (
    EXPECTED_AGENT_IDS,
    AgentSpecFrontmatter,
    calculate_triage,
    load_squad_specs,
)


def test_all_12_squad_specs_valid_pydantic() -> None:
    """Verifica que las 12 fichas en specs/squad/ existen y cumplen el contrato Pydantic v2."""
    docs = load_squad_specs(Path("specs/squad"))
    assert len(docs) == 12
    assert tuple(d.frontmatter.id for d in docs) == EXPECTED_AGENT_IDS


def test_inv_helix_1_separation_construction_and_veto() -> None:
    """INV-HELIX-1: Ningún constructor tiene veto y solo Seguridad (10) y QA (11) tienen veto."""
    docs = load_squad_specs(Path("specs/squad"))
    veto_ids = {d.frontmatter.id for d in docs if d.frontmatter.has_veto_power}
    assert veto_ids == {"10-security-privacy", "11-qa-verifier"}

    for d in docs:
        if d.frontmatter.cell == "construction":
            assert d.frontmatter.has_veto_power is False
        if d.frontmatter.has_veto_power:
            assert d.frontmatter.can_write_production_code is False

    # Verificar que el validador Pydantic rechaza un constructor con veto
    with pytest.raises(ValidationError):
        AgentSpecFrontmatter(
            id="05-frontend",
            name_es="Frontend",
            name_en="Frontend",
            cell="construction",
            icon="⚡",
            activates_on_sizes=["S"],
            mandatory_triggers=["ui"],
            can_write_production_code=True,
            has_veto_power=True,
            inputs=["spec.md"],
            outputs=["app.tsx"],
        )


def test_inv_helix_2_lazy_loading_triage_xs_and_s() -> None:
    """INV-HELIX-2: Las tareas XS y S activan solo 2-4 agentes y dejan el resto en el banquillo."""
    xs = calculate_triage(
        milestone_id="6.2-typo",
        estimated_files=1,
        surfaces=["docs"],
    )
    assert xs.size == "XS"
    assert len(xs.active_agents) == 3  # 01-orchestrator, 08-media-i18n, 11-qa-verifier
    assert len(xs.benched_agents) == 9
    assert xs.requires_human_approval is False

    s_task = calculate_triage(
        milestone_id="6.2-filter",
        estimated_files=2,
        surfaces=["backend"],
    )
    assert s_task.size == "S"
    assert len(s_task.active_agents) <= 4
    assert "02-product-analyst" not in s_task.active_agents
    assert "03-architect" not in s_task.active_agents


def test_inv_helix_3_mandatory_security_trigger_on_xs() -> None:
    """INV-HELIX-3: Aunque sea 1 archivo (XS), tocar auth_security o data_sql fuerza 10-security-privacy."""
    sec_xs = calculate_triage(
        milestone_id="6.2-sec-fix",
        estimated_files=1,
        surfaces=["auth_security"],
    )
    assert sec_xs.size == "XS"
    assert "10-security-privacy" in sec_xs.active_agents
    assert "11-qa-verifier" in sec_xs.active_agents


def test_inv_helix_3_mandatory_ux_i18n_monetization_triggers() -> None:
    """INV-HELIX-3: Tocar frontend activa 04-ux-ui; tocar monetization activa 09 y 10."""
    fe_task = calculate_triage(
        milestone_id="6.2-ui",
        estimated_files=2,
        surfaces=["frontend"],
    )
    assert "04-ux-ui" in fe_task.active_agents
    assert "05-frontend" in fe_task.active_agents

    mon_task = calculate_triage(
        milestone_id="6.2-price",
        estimated_files=2,
        surfaces=["monetization"],
    )
    assert "09-monetization" in mon_task.active_agents
    assert "10-security-privacy" in mon_task.active_agents


def test_triage_card_6_lines_contract() -> None:
    """El contrato de la Tarjeta de Triaje debe tener exactamente 6 líneas y cabecera TRIAGE HELIX."""
    decision = calculate_triage(
        milestone_id="6.2",
        estimated_files=5,
        surfaces=["docs", "backend"],
    )
    card = decision.format_triage_card()
    lines = card.splitlines()
    assert len(lines) == 6
    assert lines[0].startswith("TRIAGE HELIX · Hito 6.2 · Talla: M")
    assert "Roles activados" in lines[2]
    assert "Verification Gate:" in lines[4]


def test_build_adapters_generates_all_targets() -> None:
    """INV-HELIX-4: build_adapters genera los 26 artefactos (.agents, .claude, .cursor y manifest.json)."""
    generated = build_adapters(Path("."), check_only=False)
    assert len(generated) == 26  # 12 .agents + 12 .claude + 1 manifest.json + 1 .cursor/rules/helix-squad.mdc

    manifest_path = Path(".agents/squad/manifest.json")
    assert manifest_path.exists()
    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest_data["total_agents"] == 12

    claude_qa = Path(".claude/agents/11-qa-verifier.md").read_text(encoding="utf-8")
    assert "DO NOT EDIT MANUALLY (INV-HELIX-4)" in claude_qa
    assert "Edit, Write" not in claude_qa  # QA Verifier no tiene permiso de escritura de código prod

    cursor_rule = Path(".cursor/rules/helix-squad.mdc").read_text(encoding="utf-8")
    assert "alwaysApply: true" in cursor_rule
    assert "01-orchestrator" in cursor_rule


def test_build_adapters_idempotency_and_check_mode() -> None:
    """El modo --check pasa sin errores cuando los adaptadores están sincronizados."""
    checked = build_adapters(Path("."), check_only=True)
    assert len(checked) == 26


def test_constitution_v1_1_0_article_9_and_agents_md_section_5() -> None:
    """Verifica la adopción interna en _constitution.md (v1.1.0 Art. 9), AGENTS.md (§5) y ADR-018."""
    constitution = Path("specs/_constitution.md").read_text(encoding="utf-8")
    assert "Versión:** 1.1.0" in constitution
    assert "## Artículo 9: Gobernanza del Escuadrón de 12 Agentes Datalaria Helix" in constitution

    agents_md = Path("AGENTS.md").read_text(encoding="utf-8")
    assert "## 5. ESCUADRÓN DATALARIA HELIX Y TRIAJE BAJO DEMANDA" in agents_md

    decisions_md = Path("specs/DECISIONS.md").read_text(encoding="utf-8")
    assert "## ADR-018:" in decisions_md


def test_no_python_or_adapters_leaked_into_static() -> None:
    """Constitución Art. 2 & INV-HELIX-6: Cero archivos .py, .sql, .env o .mdc dentro de static/."""
    static_dir = Path("static")
    forbidden_suffixes = {".py", ".sql", ".env", ".pyc", ".mdc"}
    leaked = [
        p.as_posix()
        for p in static_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in forbidden_suffixes
    ]
    assert not leaked, f"Archivos prohibidos detectados en static/: {leaked}"
