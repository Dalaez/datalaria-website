import json
import os
from ops.pulse.build_index import build_index
from ops.pulse.models import PublicPulseDataset


def test_build_index_execution():
    """Verifica que build_index genera correctamente los archivos y activos."""
    all_assets, pub_dataset = build_index()
    
    # 1. Totalidad de activos: 109 posts + 7 apps + 19 kits/suites = 135
    assert len(all_assets) >= 135
    assert pub_dataset.total_assets >= 135
    
    # 2. Archivos en disco
    assert os.path.isfile("data/pulse/private/index.json")
    assert os.path.isfile("static/apps/pulse/data/public.json")
    
    # 3. Validación de contratos
    pub_dataset.validate_security_invariants()


def test_public_json_security_invariants():
    """Valida determinísticamente INV-PULSE-1 e INV-PULSE-2 sobre el JSON compilado."""
    with open("static/apps/pulse/data/public.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    dataset = PublicPulseDataset(**data)
    dataset.validate_security_invariants()
    
    for asset in dataset.assets:
        # INV-PULSE-1: Cero fuga de privados
        assert asset.visibility == "public"
        # INV-PULSE-2: Cero métricas absolutas
        assert asset.metrics_absolute is None


def test_post_bilingual_pairing_parity():
    """Verifica que los 109 posts están emparejados con paridad 'complete'."""
    with open("data/pulse/private/index.json", "r", encoding="utf-8") as f:
        assets = json.load(f)
        
    posts = [a for a in assets if a["asset_type"] == "post"]
    assert len(posts) == 109
    
    for p in posts:
        assert p["title_es"] is not None
        assert p["title_en"] is not None
        assert p["url_es"] is not None
        assert p["url_en"] is not None
        assert p["language_parity"] == "complete"
        assert p["word_count_es"] > 0
        assert p["word_count_en"] > 0
        assert p["reading_time_min"] >= 1
