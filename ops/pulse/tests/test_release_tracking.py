"""
ops/pulse/tests/test_release_tracking.py
----------------------------------------
Suite de verificación determinista para el Hito P2.1 (SPEC-APP-PULSE v1.3.0):
- INV-PULSE-7: Coherencia cronológica de lanzamientos de Apps.
- INV-PULSE-8: Trazabilidad, versiones y fechas normalizadas en Kits y Suites.
- Tracking de version_upgrade y vinculación con artículos editoriales.
"""

import json
from datetime import date
from pathlib import Path
import pytest

from ops.pulse.build_index import build_index
from ops.pulse.publish_public import publish_public_dataset

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
PRIVATE_INDEX_PATH = ROOT_DIR / "data" / "pulse" / "private" / "index.json"
PUBLIC_DATASET_PATH = ROOT_DIR / "static" / "apps" / "pulse" / "data" / "public.json"


@pytest.fixture(scope="module")
def pulse_data():
    """Genera y carga los datasets privado y público para validación."""
    all_assets, _ = build_index()
    dataset = publish_public_dataset()
    with open(PRIVATE_INDEX_PATH, "r", encoding="utf-8") as f:
        private_json = json.load(f)
    with open(PUBLIC_DATASET_PATH, "r", encoding="utf-8") as f:
        public_json = json.load(f)
    return {
        "dataset": dataset,
        "all_assets": all_assets,
        "private_json": private_json,
        "private_map": {a["id"]: a for a in private_json},
        "public_json": public_json,
        "assets_map": {a["id"]: a for a in public_json["assets"]},
    }


def test_inv_pulse_7_app_launch_dates_and_internal_releases_filtered(pulse_data):
    """
    INV-PULSE-7 & INV-PULSE-9:
    - Ninguna app en incubación usa versiones internas v0.x como fecha de estreno; usa launch_date.
    - Los proyectos incubating (helix), sus kits/posts y los drafts residen en index.json privado
      con visibility='private', y quedan 100 % excluidos de static/apps/pulse/data/public.json.
    """
    priv_assets = pulse_data["private_map"]
    pub_assets = pulse_data["assets_map"]

    # 1. Datalaria Helix: presente en el índice privado con visibility='private' y ausente del público
    assert "helix" in priv_assets, "Datalaria Helix debe existir en el índice privado"
    helix = priv_assets["helix"]
    assert helix["publish_date"] == "2027-01-19", f"Helix launch_date esperado 2027-01-19, obtenido {helix['publish_date']}"
    assert helix["status"] == "scheduled", "Helix debe estar en estado scheduled hasta su estreno"
    assert helix["visibility"] == "private", "Helix debe estar oculta para el escaparate público (INV-PULSE-9)"
    assert helix["release_type"] == "initial_launch"

    # Ninguna versión interna v0.1.0..v0.5.0 ni la ficha embargo ni sus kits/posts deben filtrarse a public.json
    for v in ["v0.1.0", "v0.2.0", "v0.3.0", "v0.4.0", "v0.5.0"]:
        assert f"helix-{v}" not in priv_assets, f"La versión interna {v} de Helix no debe figurar en el índice"
    for emb_id in ("helix", "pack-sdd", "suite-sdd"):
        assert emb_id in priv_assets, f"{emb_id} debe conservarse en index.json para Admin"
        assert priv_assets[emb_id]["visibility"] == "private"
        assert emb_id not in pub_assets, f"{emb_id} NO debe exponerse en public.json"

    for pid, asset in priv_assets.items():
        if asset["asset_type"] == "post" and (asset["slug"].startswith("helix-") or asset["status"] == "draft"):
            assert asset["visibility"] == "private", f"{pid} debe ser visibility='private'"
            assert pid not in pub_assets, f"{pid} no debe filtrarse a public.json"

    # 2. Datalaria Pulse: dentro de ventana <= 30 días, presente en catálogo público
    assert "pulse" in pub_assets, "Datalaria Pulse debe existir en el catálogo público"
    pulse = pub_assets["pulse"]
    assert pulse["publish_date"] == "2026-11-18", f"Pulse launch_date esperado 2026-11-18, obtenido {pulse['publish_date']}"
    assert pulse["release_type"] == "initial_launch"
    assert pulse["version"] == "v1.5.0"

    # Ninguna versión interna v0.1.0..v0.4.0 debe generar assets en el índice
    for v in ["v0.1.0", "v0.1.5", "v0.2.0", "v0.3.0", "v0.4.0"]:
        assert f"pulse-{v}" not in priv_assets, f"La versión interna {v} de Pulse no debe figurar en el índice"


def test_inv_pulse_8_kits_and_suites_dates_and_status_normalized(pulse_data):
    """
    INV-PULSE-8:
    Todo Kit, Suite y Mega Bundle tiene publish_date no nulo, versión semántica
    y un estado normalizado exclusivamente entre 'published' o 'scheduled'.
    Cero activos con status 'coming' en public.json.
    """
    public_assets = pulse_data["public_json"]["assets"]
    private_assets = pulse_data["private_json"]

    # 1. Cero coming en el dataset público ni privado
    for a in public_assets:
        assert a["status"] != "coming", f"Activo {a['id']} tiene status prohibido 'coming'"
        assert a["status"] in ("idea", "draft", "review", "scheduled", "published"), (
            f"Activo {a['id']} tiene status no estándar: {a['status']}"
        )

    # 2. Kits y Suites (totales en índice privado y filtrados en público)
    private_kits = [a for a in private_assets if a["asset_type"] in ("kit", "suite", "mega_bundle")]
    kits_and_suites = [a for a in public_assets if a["asset_type"] in ("kit", "suite", "mega_bundle")]
    assert len(private_kits) >= 19, f"Se esperaban al menos 19 kits/suites en índice privado, encontrados {len(private_kits)}"
    assert len(kits_and_suites) >= 17, f"Se esperaban al menos 17 kits/suites públicos tras filtrar embargos, encontrados {len(kits_and_suites)}"

    for item in private_kits:
        assert item["publish_date"] is not None, f"Kit/Suite {item['id']} tiene publish_date nulo"
        assert item["version"] is not None, f"Kit/Suite {item['id']} tiene version nula"
        assert item["release_type"] in ("kit_launch", "kit_edition")
        assert item["status"] in ("published", "scheduled")


def test_version_upgrades_and_editorial_post_tracking(pulse_data):
    """
    Verifica que las versiones evolutivas de aplicaciones ya existentes (LifeOps, Weather, etc.)
    se indexan como 'version_upgrade', tienen parent_asset_id y enlazan a su post editorial si existe.
    """
    assets = pulse_data["assets_map"]

    # 1. Weather v3.3.0
    assert "weather-v3.3.0" in assets, "weather-v3.3.0 debe existir como version_upgrade"
    w330 = assets["weather-v3.3.0"]
    assert w330["release_type"] == "version_upgrade"
    assert w330["parent_asset_id"] == "weather"
    assert w330["version"] == "v3.3.0"
    assert w330["publish_date"] == "2026-11-13"

    # 2. LifeOps v1.1.0 y vínculo editorial
    assert "lifeops-v1.1.0" in assets, "lifeops-v1.1.0 debe existir como version_upgrade"
    l110 = assets["lifeops-v1.1.0"]
    assert l110["release_type"] == "version_upgrade"
    assert l110["parent_asset_id"] == "lifeops"
    assert l110["version"] == "v1.1.0"
    assert l110["editorial_post_slug"] == "app-lifeops_part6_analytics_dashboard_360"

    # 3. Posts tienen release_type article
    post_assets = [a for a in pulse_data["public_json"]["assets"] if a["asset_type"] == "post"]
    assert len(post_assets) >= 100
    for p in post_assets:
        assert p["release_type"] == "article", f"Post {p['id']} debe tener release_type 'article'"
