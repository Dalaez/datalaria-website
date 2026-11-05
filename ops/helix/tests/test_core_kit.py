"""Suite de pruebas deterministas para el Kit Helix Core y Blueprints de Proyecto (Hito 6.4)."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from ops.helix.build_core_kit import (
    AVAILABLE_BLUEPRINTS,
    build_core_kit,
    init_project_from_core_kit,
)


def test_build_core_kit_structure(tmp_path: Path) -> None:
    """Verifica que build_core_kit genera los 5 subdirectorios numerados y los archivos raíz."""
    out_dir = tmp_path / "core_kit"
    dist_dir = tmp_path / "dist"

    result_path = build_core_kit(
        source_root=Path("."),
        output_dir=out_dir,
        distribution_dir=dist_dir,
    )
    assert result_path.exists()

    expected_folders = [
        "01_Constitution_and_Memory",
        "02_Templates",
        "03_Squad_12_Agents_and_Adapters",
        "04_Project_Blueprints",
        "05_Case_Studies_and_Docs",
    ]
    for folder in expected_folders:
        assert (out_dir / folder).is_dir(), f"Falta el directorio {folder}"

    assert (out_dir / "README.md").exists()
    assert (out_dir / "LICENSE.txt").exists()

    # Comprobar 01_Constitution_and_Memory
    assert (out_dir / "01_Constitution_and_Memory" / "AGENTS.md").exists()
    assert (out_dir / "01_Constitution_and_Memory" / "CLAUDE.md").exists()
    assert (out_dir / "01_Constitution_and_Memory" / "specs" / "_constitution.md").exists()
    assert (out_dir / "01_Constitution_and_Memory" / "specs" / "ROADMAP.md").exists()
    assert (out_dir / "01_Constitution_and_Memory" / "specs" / "DECISIONS.md").exists()

    # Comprobar 03_Squad_12_Agents_and_Adapters
    assert (out_dir / "03_Squad_12_Agents_and_Adapters" / ".agents" / "squad" / "manifest.json").exists()
    assert (out_dir / "03_Squad_12_Agents_and_Adapters" / ".claude" / "agents" / "01-orchestrator.md").exists()
    assert (out_dir / "03_Squad_12_Agents_and_Adapters" / ".cursor" / "rules" / "helix-squad.mdc").exists()
    assert (out_dir / "03_Squad_12_Agents_and_Adapters" / "specs" / "squad" / "01-orchestrator.md").exists()

    # Comprobar ZIPs
    zip_helix = tmp_path / "kit-datalaria-helix-core-v1.0.0.zip"
    zip_dist = dist_dir / "kit-datalaria-helix-core-v1.0.0.zip"
    assert zip_helix.exists()
    assert zip_dist.exists()

    with zipfile.ZipFile(zip_helix, "r") as zf:
        namelist = zf.namelist()
        assert "README.md" in namelist
        assert "LICENSE.txt" in namelist
        assert any("01_Constitution_and_Memory" in n for n in namelist)
        assert any("04_Project_Blueprints" in n for n in namelist)


def test_init_project_from_core_kit_empty_dir(tmp_path: Path) -> None:
    """Verifica que init_project_from_core_kit inicializa un repositorio vacío con la base SDD."""
    target_repo = tmp_path / "new_repo"
    init_project_from_core_kit(target_dir=target_repo)

    assert (target_repo / "AGENTS.md").exists()
    assert (target_repo / "CLAUDE.md").exists()
    assert (target_repo / "specs" / "_constitution.md").exists()
    assert (target_repo / "specs" / "ROADMAP.md").exists()
    assert (target_repo / "specs" / "DECISIONS.md").exists()
    assert (target_repo / "specs" / "_templates" / "app-spec.template.md").exists()
    assert (target_repo / ".agents" / "squad" / "manifest.json").exists()
    assert (target_repo / ".claude" / "agents" / "11-qa-verifier.md").exists()
    assert (target_repo / ".cursor" / "rules" / "helix-squad.mdc").exists()


@pytest.mark.parametrize("blueprint_id", AVAILABLE_BLUEPRINTS)
def test_init_project_with_all_blueprints(tmp_path: Path, blueprint_id: str) -> None:
    """Verifica la inicialización de proyectos con cada uno de los 3 blueprints."""
    target_repo = tmp_path / f"repo_{blueprint_id}"
    init_project_from_core_kit(target_dir=target_repo, blueprint_id=blueprint_id)

    assert (target_repo / "AGENTS.md").exists()
    assert (target_repo / "specs" / "spec.md").exists()
    assert (target_repo / "specs" / "ROADMAP.md").exists()

    if blueprint_id == "blueprint-01-static-calculator":
        assert (target_repo / "index.html").exists()
        assert (target_repo / "app.js").exists()
        assert (target_repo / "styles.css").exists()
    elif blueprint_id == "blueprint-02-react-supabase-rls":
        assert (target_repo / "package.json").exists()
        assert (target_repo / "supabase" / "schema.sql").exists()
    elif blueprint_id == "blueprint-03-python-quant-engine":
        assert (target_repo / "pyproject.toml").exists()
        assert (target_repo / "src" / "engine.py").exists()
        assert (target_repo / "tests" / "test_engine.py").exists()


def test_blueprint_03_python_quant_engine_logic(tmp_path: Path) -> None:
    """Ejecuta directamente la lógica del motor cuantitativo incluido en el Blueprint 03."""
    target_repo = tmp_path / "quant_repo"
    init_project_from_core_kit(target_dir=target_repo, blueprint_id="blueprint-03-python-quant-engine")

    # Importar dinámicamente engine.py del blueprint
    import importlib.util

    engine_path = target_repo / "src" / "engine.py"
    spec = importlib.util.spec_from_file_location("blueprint_engine", engine_path)
    assert spec is not None and spec.loader is not None
    engine_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine_mod)

    Portfolio = engine_mod.Portfolio
    AssetAllocation = engine_mod.AssetAllocation

    p = Portfolio(
        assets=[
            AssetAllocation(symbol="SP500", weight=0.7, expected_return=0.10),
            AssetAllocation(symbol="BONDS", weight=0.3, expected_return=0.04),
        ]
    )
    assert pytest.approx(p.weighted_return(), 0.001) == 0.082

    # Probar que rechaza pesos que no suman 1.0
    with pytest.raises(ValueError, match="Los pesos deben sumar 1.0"):
        bad_p = Portfolio(
            assets=[
                AssetAllocation(symbol="SP500", weight=0.5, expected_return=0.10),
            ]
        )
        bad_p.weighted_return()
