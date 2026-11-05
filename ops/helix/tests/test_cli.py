"""Suite de pruebas deterministas para el CLI helix cero-dependencias (INV-HELIX-5 / Hito 6.5)."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import pytest

from ops.helix.cli import (
    main,
    score_spec_markdown,
    std_calculate_triage,
)
from ops.helix.models import calculate_triage


def test_inv_helix_5_zero_external_dependencies_ast() -> None:
    """INV-HELIX-5: ops/helix/cli.py utiliza EXCLUSIVAMENTE la librería estándar de Python."""
    cli_path = Path("ops/helix/cli.py")
    assert cli_path.exists()

    tree = ast.parse(cli_path.read_text(encoding="utf-8"))
    imported_modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:
                imported_modules.add(node.module.split(".")[0])

    stdlib = set(sys.stdlib_module_names)
    stdlib.add("__future__")

    # Módulos del propio repo permitidos bajo fallback
    internal_repo_modules = {"ops"}

    for mod in imported_modules:
        assert mod in stdlib or mod in internal_repo_modules, (
            f"Violación INV-HELIX-5: '{mod}' no pertenece a la librería estándar de Python."
        )


def test_cli_triage_matches_pydantic_models_parity() -> None:
    """Verifica que std_calculate_triage en cli.py replica 100% el comportamiento de calculate_triage."""
    test_cases = [
        {"milestone_id": "6.5-doc", "estimated_files": 1, "surfaces": ["docs"], "spec_contract_change": False, "is_new_app": False},
        {"milestone_id": "6.5-fix", "estimated_files": 2, "surfaces": ["backend"], "spec_contract_change": False, "is_new_app": False},
        {"milestone_id": "6.5-ui", "estimated_files": 2, "surfaces": ["frontend"], "spec_contract_change": False, "is_new_app": False},
        {"milestone_id": "6.5-mid", "estimated_files": 4, "surfaces": ["backend", "docs"], "spec_contract_change": False, "is_new_app": False},
        {"milestone_id": "6.5-big", "estimated_files": 8, "surfaces": ["backend", "ui", "monetization"], "spec_contract_change": True, "is_new_app": False},
        {"milestone_id": "6.5-app", "estimated_files": 15, "surfaces": ["backend", "frontend"], "spec_contract_change": False, "is_new_app": True},
    ]

    for tc in test_cases:
        pydantic_res = calculate_triage(
            milestone_id=tc["milestone_id"],
            estimated_files=tc["estimated_files"],
            surfaces=tc["surfaces"],  # type: ignore[arg-type]
            spec_contract_change=tc["spec_contract_change"],
            is_new_app=tc["is_new_app"],
        )
        std_res = std_calculate_triage(
            milestone_id=tc["milestone_id"],
            estimated_files=tc["estimated_files"],
            surfaces=tc["surfaces"],
            spec_contract_change=tc["spec_contract_change"],
            is_new_app=tc["is_new_app"],
        )

        assert std_res["size"] == pydantic_res.size
        assert std_res["active_agents"] == pydantic_res.active_agents
        assert std_res["benched_agents"] == pydantic_res.benched_agents
        assert std_res["checkpoint_tag"] == pydantic_res.checkpoint_tag
        assert std_res["requires_human_approval"] == pydantic_res.requires_human_approval


def test_spec_quality_score_on_real_specs() -> None:
    """Verifica que score_spec_markdown evalúa correctamente specs completas vs incompletas."""
    helix_spec = Path("specs/apps/helix/spec.md").read_text(encoding="utf-8")
    score_helix = score_spec_markdown(helix_spec)
    assert score_helix["total_score"] >= 80
    assert score_helix["passed"] is True
    assert len(score_helix["invariants_found"]) >= 3

    pulse_spec = Path("specs/apps/pulse/spec.md").read_text(encoding="utf-8")
    score_pulse = score_spec_markdown(pulse_spec)
    assert score_pulse["total_score"] >= 80
    assert score_pulse["passed"] is True

    # Spec incompleta / vacía
    score_empty = score_spec_markdown("# Spec Incompleta\nTexto sin secciones.")
    assert score_empty["total_score"] < 50
    assert score_empty["passed"] is False


def test_cli_status_on_datalaria_repo() -> None:
    """Verifica la ejecución de helix status --json sobre el repositorio."""
    ret = main(["status", "--json"])
    assert ret == 0


def test_cli_new_spec_and_verify_in_tmp_repo(tmp_path: Path) -> None:
    """Verifica la creación y verificación de una nueva spec con helix new-spec y helix verify."""
    # 1. new-spec
    ret_new = main([
        "new-spec",
        "billing-engine",
        "--title", "Motor de Facturación",
        "--tier", "flagship",
        "--with-design",
        "--root", str(tmp_path),
    ])
    assert ret_new == 0

    spec_file = tmp_path / "specs" / "apps" / "billing-engine" / "spec.md"
    design_file = tmp_path / "specs" / "apps" / "billing-engine" / "design.md"
    assert spec_file.exists()
    assert design_file.exists()

    # 2. verify
    ret_ver = main([
        "verify",
        "--spec", str(spec_file),
        "--min-score", "80",
        "--root", str(tmp_path),
    ])
    assert ret_ver == 0


def test_cli_checkpoint_and_rollback_git_lifecycle(tmp_path: Path) -> None:
    """Verifica el ciclo de vida de checkpoint y rollback seguro en un repositorio Git efímero."""
    # Inicializar git repo en tmp_path
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@datalaria.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Helix Test Runner"], cwd=tmp_path, check=True)

    # Crear estructura base y commit inicial
    specs_dir = tmp_path / "specs"
    specs_dir.mkdir(parents=True)
    roadmap = specs_dir / "ROADMAP.md"
    roadmap.write_text("# ROADMAP\n## REGISTRO DE BLOQUEOS Y ROLLBACKS (AUDIT LOG)\n", encoding="utf-8")
    tracked_file = tmp_path / "file.txt"
    tracked_file.write_text("version 1.0\n", encoding="utf-8")

    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=tmp_path, check=True)

    # 1. Checkpoint
    ret_chk = main(["checkpoint", "1.0", "--root", str(tmp_path)])
    assert ret_chk == 0

    # 2. Modificar archivo
    tracked_file.write_text("version 2.0 (broken)\n", encoding="utf-8")
    assert tracked_file.read_text(encoding="utf-8") == "version 2.0 (broken)\n"

    # 3. Rollback Dry-Run (no debe modificar)
    ret_dry = main(["rollback", "1.0", "--root", str(tmp_path)])
    assert ret_dry == 0
    assert tracked_file.read_text(encoding="utf-8") == "version 2.0 (broken)\n"

    # 4. Rollback con --confirm y --log-reason
    ret_rb = main([
        "rollback", "1.0",
        "--confirm",
        "--log-reason", "Fallo en prueba de integración",
        "--root", str(tmp_path),
    ])
    assert ret_rb == 0
    assert tracked_file.read_text(encoding="utf-8") == "version 1.0\n"

    roadmap_text = roadmap.read_text(encoding="utf-8")
    assert "Fallo en prueba de integración" in roadmap_text


def test_cli_init_standalone_from_core_kit(tmp_path: Path) -> None:
    """Verifica que helix init inicializa un proyecto con cimientos SDD y helix.py."""
    target_repo = tmp_path / "new_project"
    ret = main(["init", "--target", str(target_repo), "--blueprint", "blueprint-01-static-calculator"])
    assert ret == 0

    assert (target_repo / "AGENTS.md").exists()
    assert (target_repo / "CLAUDE.md").exists()
    assert (target_repo / "specs" / "_constitution.md").exists()
    assert (target_repo / "specs" / "ROADMAP.md").exists()
    assert (target_repo / "specs" / "spec.md").exists()
    assert (target_repo / "helix.py").exists()


def test_no_cli_parity_guide_and_helix_py_in_core_kit() -> None:
    """Verifica la presencia de NO_CLI_PARITY_GUIDE.md y helix.py en el kit y en el paquete ZIP."""
    core_kit_dir = Path("packages/helix/core_kit")
    guide_path = core_kit_dir / "05_Case_Studies_and_Docs" / "NO_CLI_PARITY_GUIDE.md"
    assert guide_path.exists()
    guide_content = guide_path.read_text(encoding="utf-8")
    assert "INV-HELIX-5" in guide_content
    assert "helix status" in guide_content
    assert "helix rollback" in guide_content

    helix_py = core_kit_dir / "helix.py"
    assert helix_py.exists()

    zip_path = Path("packages/helix/kit-datalaria-helix-core-v1.0.0.zip")
    assert zip_path.exists()
    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        assert "helix.py" in namelist
        assert any("NO_CLI_PARITY_GUIDE.md" in n for n in namelist)
