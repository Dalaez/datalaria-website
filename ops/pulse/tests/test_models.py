import pytest
from datetime import date, datetime
from ops.pulse.models import (
    ContentAsset,
    SeoAudit,
    RelativeMetrics,
    AbsoluteMetrics,
    PublicPulseDataset
)


def test_content_asset_creation():
    asset = ContentAsset(
        id="dafo-cuantitativo-matriz-came",
        slug="dafo-cuantitativo-matriz-came",
        asset_type="post",
        status="published",
        visibility="public",
        title_es="DAFO Cuantitativo & Matriz CAME",
        title_en="Quantitative SWOT & TOWS Matrix",
        url_es="/es/posts/dafo-cuantitativo-matriz-came/",
        url_en="/en/posts/dafo-cuantitativo-matriz-came/",
        publish_date=date(2025, 9, 20),
        word_count_es=1450,
        word_count_en=1380,
        reading_time_min=7,
        language_parity="complete"
    )
    assert asset.id == "dafo-cuantitativo-matriz-came"
    assert asset.language_parity == "complete"
    assert asset.reading_time_min == 7


def test_inv_pulse_1_private_asset_rejection():
    """INV-PULSE-1: Cero fuga de activos privados a formato público."""
    private_asset = ContentAsset(
        id="idea-secreta",
        slug="idea-secreta",
        asset_type="post",
        status="idea",
        visibility="private",
        title_es="Idea Confidencial"
    )
    with pytest.raises(ValueError, match="Violación de INV-PULSE-1"):
        private_asset.to_public_dict()


def test_inv_pulse_2_absolute_metrics_stripped():
    """INV-PULSE-2: Cero fuga de métricas cuantitativas absolutas en export público."""
    asset = ContentAsset(
        id="post-test",
        slug="post-test",
        asset_type="post",
        status="published",
        visibility="public",
        title_es="Post Test",
        metrics_absolute=AbsoluteMetrics(
            ga4_views_30d=5420,
            ga4_users_30d=1200,
            gsc_clicks_30d=350,
            gsc_impressions_30d=14500
        ),
        metrics_relative=RelativeMetrics(
            index_100=145,
            rank_pct=88,
            trend_30d_pct=12.5,
            gsc_opportunity=True
        )
    )
    
    pub_dict = asset.to_public_dict()
    assert "metrics_absolute" not in pub_dict or pub_dict["metrics_absolute"] is None
    assert pub_dict["metrics_relative"]["index_100"] == 145
    assert pub_dict["metrics_relative"]["rank_pct"] == 88


def test_public_pulse_dataset_validation():
    """Valida la función guardiana de seguridad del dataset público completo."""
    safe_asset = ContentAsset(
        id="safe-post",
        slug="safe-post",
        asset_type="post",
        status="published",
        visibility="public",
        title_es="Safe"
    )
    
    dataset = PublicPulseDataset(
        version="1.0.0",
        generated_at=datetime.now(),
        total_assets=1,
        published_assets=1,
        scheduled_assets=0,
        ideas_count=0,
        parity_summary={"complete": 1},
        assets=[safe_asset]
    )
    # Debe pasar sin lanzar excepciones
    dataset.validate_security_invariants()
