"""
Contratos Pydantic v2 para Datalaria Pulse (Content Ops as Code).
Especificación técnica formal: SPEC-APP-PULSE (specs/apps/pulse/spec.md).
"""

from datetime import date, datetime
from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, computed_field


AssetType = Literal["post", "app", "kit", "suite", "mega_bundle"]
AssetStatus = Literal["idea", "draft", "review", "scheduled", "published", "available", "coming"]
VisibilityType = Literal["public", "private"]
LanguageParity = Literal["complete", "missing_en", "missing_es", "outdated_en", "outdated_es"]
FreshnessStatus = Literal["fresh", "review_soon", "stale"]


class SeoAudit(BaseModel):
    score_0_100: int = Field(default=0, ge=0, le=100)
    title_ok: bool = True
    description_ok: bool = True
    parity_ok: bool = True
    taxonomy_ok: bool = True
    internal_links_ok: bool = True
    issues: List[str] = Field(default_factory=list)


class RelativeMetrics(BaseModel):
    """
    Métricas de rendimiento en escalas relativas.
    Garantiza INV-PULSE-2 (cero exposición de cifras absolutas en el dataset público).
    """
    index_100: int = Field(default=100, description="Índice base 100 relativo a la mediana de activos con visitas")
    rank_pct: int = Field(default=50, ge=0, le=100, description="Percentil relativo en tráfico")
    trend_30d_pct: float = Field(default=0.0, description="Variación porcentual respecto al periodo previo")
    gsc_opportunity: bool = Field(default=False, description="Oportunidad de optimización SEO en Search Console")


class AbsoluteMetrics(BaseModel):
    """
    Métricas cuantitativas reales obtenidas de GA4 y Search Console.
    USO EXCLUSIVO: index.json privado y tracker local. NUNCA exportar a public.json.
    """
    ga4_views_30d: int = 0
    ga4_users_30d: int = 0
    ga4_engagement_sec: float = 0.0
    gsc_clicks_30d: int = 0
    gsc_impressions_30d: int = 0
    gsc_ctr_pct: float = 0.0
    gsc_avg_position: float = 0.0


class ContentAsset(BaseModel):
    """
    Entidad canónica unificada para Posts, Apps, Kits y Suites.
    Agrupa versiones ES y EN en una sola tarjeta/fila.
    """
    id: str = Field(description="Identificador único (translationKey, slug de app o id de kit)")
    slug: str = Field(description="Slug base URL")
    asset_type: AssetType
    status: AssetStatus
    visibility: VisibilityType = "public"

    # Metadatos bilingües
    title_es: Optional[str] = None
    title_en: Optional[str] = None
    url_es: Optional[str] = None
    url_en: Optional[str] = None
    brief_es: Optional[str] = None
    brief_en: Optional[str] = None

    # Publicación y fechas
    publish_date: Optional[date] = None
    last_modified_es: Optional[datetime] = None
    last_modified_en: Optional[datetime] = None

    # Calidad y taxonomía
    language_parity: LanguageParity = "complete"
    category: str = "General"
    categories: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    series: Optional[str] = None
    word_count_es: int = 0
    word_count_en: int = 0
    reading_time_min: int = 0

    # Relaciones entre activos
    related_app: Optional[str] = None
    related_kit: Optional[str] = None
    included_kits: List[str] = Field(default_factory=list)

    # Monetización (para Kits / Suites)
    price: Optional[str] = None
    original_price: Optional[str] = None
    checkout_url: Optional[str] = None
    deliverables: List[str] = Field(default_factory=list)

    # Auditoría SEO y ciclo de vida
    seo_audit: SeoAudit = Field(default_factory=SeoAudit)
    freshness_status: FreshnessStatus = "fresh"
    owner: str = "Daniel Alaez"
    campaign: Optional[str] = None
    social_channels: List[str] = Field(default_factory=list)

    # Métricas
    metrics_relative: Optional[RelativeMetrics] = None
    metrics_absolute: Optional[AbsoluteMetrics] = None

    def to_public_dict(self) -> Dict[str, Any]:
        """
        Exporta el activo para consumo público (public.json).
        Cumple estrictamente INV-PULSE-1 (solo public) e INV-PULSE-2 (cero métricas absolutas).
        """
        if self.visibility == "private":
            raise ValueError(f"Violación de INV-PULSE-1: Se intentó exportar a público el activo privado {self.id}")

        data = self.model_dump(
            exclude={"metrics_absolute"},
            mode="json"
        )
        return data


class MonthlyTrafficPoint(BaseModel):
    """Punto en la serie temporal de tráfico mensual relativo."""
    month: str = Field(description="Año y mes YYYY-MM")
    label: str = Field(description="Etiqueta legible ej. Oct 25")
    index_100: int = Field(description="Índice relativo base 100 respecto a la mediana")


class PublicPulseDataset(BaseModel):
    """
    Esquema raíz de static/apps/pulse/data/public.json.
    """
    version: str = "1.0.0"
    generated_at: datetime
    total_assets: int
    published_assets: int
    scheduled_assets: int
    ideas_count: int
    parity_summary: Dict[str, int]
    monthly_traffic_index: List[MonthlyTrafficPoint] = Field(default_factory=list)
    assets: List[ContentAsset]

    def validate_security_invariants(self) -> None:
        """
        Verifica determinísticamente INV-PULSE-1 e INV-PULSE-2.
        """
        for asset in self.assets:
            if asset.visibility != "public":
                raise ValueError(f"INV-PULSE-1 FAILED: Activo privado {asset.id} detectado en dataset público.")
            if asset.metrics_absolute is not None:
                raise ValueError(f"INV-PULSE-2 FAILED: Métricas absolutas detectadas en activo {asset.id}.")
