import json
import os
from ops.pulse.sync_metrics import sync_all_metrics
from ops.pulse.publish_public import publish_public_dataset
from ops.pulse.models import PublicPulseDataset


def test_sync_metrics_graceful_execution():
    """Verifica que sync_all_metrics genera data/pulse/private/metrics.json."""
    metrics = sync_all_metrics()
    assert len(metrics) >= 135
    assert os.path.isfile("data/pulse/private/metrics.json")
    
    # Verificar estructura de métricas absolutas
    sample_key = next(iter(metrics.keys()))
    m = metrics[sample_key]
    assert "ga4_views_30d" in m
    assert "ga4_users_30d" in m
    assert "ga4_engagement_sec" in m
    assert "gsc_clicks_30d" in m
    assert "gsc_impressions_30d" in m


def test_publish_public_relativization_and_security():
    """Verifica que publish_public_dataset relativiza métricas y cumple INV-PULSE-1 e INV-PULSE-2."""
    pub_dataset = publish_public_dataset()
    assert pub_dataset.total_assets >= 135
    
    # Validar invariantes del modelo
    pub_dataset.validate_security_invariants()
    
    # Comprobar sobre el archivo generado en disco
    with open("static/apps/pulse/data/public.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for asset in data["assets"]:
        # 1. Cero privados (INV-PULSE-1)
        assert asset["visibility"] == "public"
        # 2. Cero absolutos (INV-PULSE-2)
        assert asset.get("metrics_absolute") is None
        # 3. Métricas relativas presentes y acotadas
        m_rel = asset.get("metrics_relative")
        assert m_rel is not None
        assert 0 <= m_rel["rank_pct"] <= 100
        assert m_rel["index_100"] >= 0
        assert isinstance(m_rel["gsc_opportunity"], bool)
