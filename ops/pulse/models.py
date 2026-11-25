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
ReleaseType = Literal["article", "initial_launch", "version_upgrade", "kit_launch", "kit_edition"]


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


class GscQueryMetric(BaseModel):
    """Métrica de consulta individual en Google Search Console."""
    query: str
    lang: Literal["es", "en", "other"] = "other"
    clicks: int = Field(default=0, ge=0)
    impressions: int = Field(default=0, ge=0)
    ctr_pct: float = Field(default=0.0, ge=0.0)
    position: float = Field(default=0.0, ge=0.0)
    is_brand_query: bool = False


class AbsoluteMetrics(BaseModel):
    """
    Métricas cuantitativas reales obtenidas de GA4 y Search Console.
    USO EXCLUSIVO: index.json privado y tracker local. NUNCA exportar a public.json.
    """
    ga4_views_30d: int = 0
    ga4_users_30d: int = 0
    ga4_engagement_sec: float = 0.0
    ga4_views_es_30d: int = 0
    ga4_views_en_30d: int = 0
    ga4_views_prev_30d: int = 0
    gsc_clicks_30d: int = 0
    gsc_impressions_30d: int = 0
    gsc_ctr_pct: float = 0.0
    gsc_avg_position: float = 0.0
    gsc_clicks_prev_30d: int = 0
    gsc_impressions_prev_30d: int = 0
    gsc_ctr_prev_pct: float = 0.0
    gsc_avg_position_prev: float = 0.0
    gsc_clicks_es_30d: int = 0
    gsc_clicks_en_30d: int = 0
    gsc_impressions_es_30d: int = 0
    gsc_impressions_en_30d: int = 0
    gsc_ctr_es_pct: float = 0.0
    gsc_ctr_en_pct: float = 0.0
    gsc_avg_position_es: float = 0.0
    gsc_avg_position_en: float = 0.0
    gsc_top_queries: List[GscQueryMetric] = Field(default_factory=list)


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

    # Versionado y control de publicaciones (Hito P2.1)
    version: Optional[str] = None
    release_type: Optional[ReleaseType] = None
    parent_asset_id: Optional[str] = None
    editorial_post_slug: Optional[str] = None

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


# ==============================================================================
# CONTRATOS PYDANTIC V2 PARA EL ANALIZADOR DE IMPACTO SEO/GA4 (HITO 7.2 / ADR-020)
# ==============================================================================

OpportunityType = Literal[
    "gsc_position_4_20",
    "serp_snippet_truncation",
    "high_retention_low_ctr",
]
BridgeType = Literal["kit_b2b", "app_sandbox", "helix_waitlist"]


class QuickWinItem(BaseModel):
    """Oportunidad accionable de mejora de CTR y posicionamiento en buscadores."""
    id: str
    slug: str
    title_es: str
    title_en: str
    category: str
    ga4_views_30d: int = Field(ge=0)
    ga4_users_30d: int = Field(ge=0)
    avg_engagement_sec: float = Field(ge=0.0)
    gsc_impressions_30d: int = Field(ge=0)
    gsc_avg_position: float = Field(ge=0.0)
    gsc_ctr_pct: float = Field(ge=0.0)
    seo_score: int = Field(ge=0, le=100)
    seo_issues: List[str] = Field(default_factory=list)
    opportunity_type: OpportunityType
    priority_score: float = Field(ge=0.0, le=100.0)
    recommended_title_es: str = Field(min_length=35, max_length=95)
    recommended_title_en: str = Field(min_length=35, max_length=95)
    recommended_desc_es: str = Field(min_length=75, max_length=245)
    top_query: Optional[str] = None


class CannibalizationAlertItem(BaseModel):
    """Alerta de canibalización cuando >=2 URLs del mismo idioma compiten por la misma consulta."""
    query: str
    lang: Literal["es", "en", "other"] = "other"
    total_impressions: int = Field(ge=0)
    total_clicks: int = Field(ge=0)
    competing_urls: List[Dict[str, Any]] = Field(default_factory=list)
    recommended_action: str


class MonetizationOrphanItem(BaseModel):
    """Post de alto tráfico/retención que carece de puente hacia Kits B2B o Apps Sandbox."""
    id: str
    slug: str
    title_es: str
    category: str
    ga4_views_30d: int = Field(ge=0)
    ga4_users_30d: int = Field(ge=0)
    avg_engagement_sec: float = Field(ge=0.0)
    rank_pct: int = Field(ge=0, le=100)
    recommended_bridge_type: BridgeType
    recommended_target_id: str
    recommended_shortcode_or_url: str
    rationale_es: str


class DecayAlertItem(BaseModel):
    """Activo evergreen con signos de fatiga orgánica o déficit de enlazado interno."""
    id: str
    slug: str
    title_es: str
    category: str
    publish_date: Optional[date] = None
    days_since_publish: int = Field(ge=0)
    ga4_views_30d: int = Field(ge=0)
    seo_score: int = Field(ge=0, le=100)
    recommended_action: str


class CategoryPerformanceItem(BaseModel):
    """Rendimiento agregado y cobertura de monetización por categoría oficial."""
    category: str
    published_posts: int = Field(ge=0)
    total_views_30d: int = Field(ge=0)
    avg_views_per_post: float = Field(ge=0.0)
    total_users_30d: int = Field(ge=0)
    avg_engagement_sec: float = Field(ge=0.0)
    monetized_posts: int = Field(ge=0)
    monetization_coverage_pct: float = Field(ge=0.0, le=100.0)
    editorial_roi_score: float = Field(ge=0.0, le=100.0)
    social_traction_score: float = Field(default=0.0, ge=0.0, le=100.0)
    total_gsc_impressions_30d: int = Field(default=0, ge=0)
    total_gsc_clicks_30d: int = Field(default=0, ge=0)
    avg_gsc_ctr_pct: float = Field(default=0.0, ge=0.0)
    en_traffic_share_pct: float = Field(default=0.0, ge=0.0, le=100.0)


class BacklogPrioritizedItem(BaseModel):
    """Idea editorial prospectiva priorizada mediante Editorial ROI Score v2."""
    id: str
    title_es: str
    title_en: str
    category: str
    target_kit_or_app: str
    seo_demand_score: float = Field(ge=0.0, le=100.0)
    monetization_fit_score: float = Field(ge=0.0, le=100.0)
    ecosystem_synergy_score: float = Field(ge=0.0, le=100.0)
    social_traction_score: float = Field(default=0.0, ge=0.0, le=100.0)
    editorial_roi_score: float = Field(ge=0.0, le=100.0)
    rationale_es: str


class ReleaseEditorialImpactItem(BaseModel):
    """Impacto y cobertura editorial de un lanzamiento de App, Versión o Kit B2B."""
    asset_id: str
    asset_type: AssetType
    version: str
    release_type: str
    title_es: str
    publish_date: Optional[date] = None
    status: str
    linked_posts_count: int = Field(ge=0)
    latest_post_date: Optional[date] = None
    editorial_views_30d: int = Field(ge=0)
    editorial_coverage_status: Literal["covered", "scheduled_coverage", "silent_release_alert", "pending_launch"]
    recommended_scriba_action: str


CanonicalChannel = Literal[
    "linkedin",
    "x",
    "devto",
    "coderlegion",
    "newsletter",
    "google_organic",
    "direct",
    "other",
]


class ChannelAttributionMetric(BaseModel):
    """Métrica de adquisición GA4 por ruta/activo y canal canónico (Hito 7.11 / ADR-033)."""
    channel: CanonicalChannel
    path: str
    asset_id: Optional[str] = None
    lang: Literal["es", "en", "other"] = "other"
    source: str = ""
    medium: str = ""
    campaign: str = ""
    sessions: int = Field(default=0, ge=0)
    users: int = Field(default=0, ge=0)
    engaged_sessions: int = Field(default=0, ge=0)
    engagement_sec: float = Field(default=0.0, ge=0.0)
    key_events: int = Field(default=0, ge=0)
    key_events_breakdown: Dict[str, int] = Field(default_factory=dict)


class ChannelSummaryItem(BaseModel):
    """Resumen agregado de adquisición, calidad y conversión por canal canónico (30d)."""
    channel: CanonicalChannel
    sessions_30d: int = Field(default=0, ge=0)
    sessions_es_30d: int = Field(default=0, ge=0)
    sessions_en_30d: int = Field(default=0, ge=0)
    en_share_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    users_30d: int = Field(default=0, ge=0)
    engaged_sessions_30d: int = Field(default=0, ge=0)
    engagement_rate_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    avg_engagement_sec: float = Field(default=0.0, ge=0.0)
    key_events_30d: int = Field(default=0, ge=0)
    conversion_rate_pct: float = Field(default=0.0, ge=0.0)
    sessions_prev_30d: int = Field(default=0, ge=0)
    trend_30d_pct: float = 0.0


class HiddenChannelWinnerItem(BaseModel):
    """Activo con alta retención o conversiones en canal social pero bajo volumen (<30 sesiones)."""
    asset_id: str
    slug: str
    title_es: str
    channel: CanonicalChannel
    sessions_30d: int = Field(ge=0)
    avg_engagement_sec: float = Field(ge=0.0)
    key_events_30d: int = Field(default=0, ge=0)
    recommended_action: str


class DarkSocialAlertItem(BaseModel):
    """Alerta de fuga UTM / pico de tráfico (direct)/(none) sin atribución correlativa (ADR-033)."""
    alert_type: Literal["dark_social_spike", "high_direct_share"]
    dispatch_id: Optional[str] = None
    channel_expected: Optional[str] = None
    direct_sessions_current: int = Field(ge=0)
    direct_sessions_baseline: float = Field(ge=0.0)
    spike_pct: float
    severity: Literal["high", "medium"] = "medium"
    recommended_action: str


LedgerChannel = Literal["linkedin", "devto", "coderlegion", "x", "newsletter"]


class DistributionLedgerEntry(BaseModel):
    """Registro canónico e idempotente de una publicación externa en vivo (Hito 7.12 / ADR-033)."""
    asset_id: str
    slug: str
    lang: Literal["es", "en"]
    channel: LedgerChannel
    external_id: str
    external_url: Optional[str] = None
    canonical_url: str
    published_at_utc: str


class DistributionLedger(BaseModel):
    """Contrato raíz de data/pulse/private/distribution_ledger.json (INV-PULSE-12)."""
    version: str = "1.0.0"
    visibility: Literal["private"] = "private"
    updated_at: datetime
    entries: List[DistributionLedgerEntry] = Field(default_factory=list)


class NativePlatformMetric(BaseModel):
    """Métricas nativas extraídas gratuitamente de Dev.to, CoderLegion o LinkedIn Empresa (Hito 7.12)."""
    platform: Literal["devto", "coderlegion", "linkedin_company", "x"]
    external_id: str
    asset_id: Optional[str] = None
    slug: str = ""
    lang: Literal["es", "en", "other"] = "other"
    title: str = ""
    url: str = ""
    canonical_url: str = ""
    views: int = Field(default=0, ge=0)
    reactions: int = Field(default=0, ge=0)
    comments: int = Field(default=0, ge=0)
    reading_time_min: int = Field(default=0, ge=0)
    published_at: Optional[str] = None


class PullThroughAlertItem(BaseModel):
    """Alerta de Fuga de Traspaso: alto alcance nativo (>=300 vistas) con bajo retorno a Datalaria (PTR < 2%)."""
    asset_id: str
    slug: str
    title_es: str
    platform: Literal["devto", "coderlegion", "linkedin_company"]
    native_views: int = Field(ge=0)
    native_reactions: int = Field(default=0, ge=0)
    native_comments: int = Field(default=0, ge=0)
    ga4_sessions_30d: int = Field(ge=0)
    ptr_pct: float = Field(ge=0.0)
    recommended_action: str


class CanonicalShieldAlertItem(BaseModel):
    """Alerta de Escudo Anti-Canibalización Canónica: >=500 vistas nativas y 0 imp. GSC tras >21 días."""
    asset_id: str
    slug: str
    title_es: str
    platform: Literal["devto", "coderlegion"]
    native_views: int = Field(ge=0)
    gsc_impressions_30d: int = Field(ge=0)
    days_since_publish: int = Field(ge=0)
    canonical_url: str
    recommended_action: str


class PulseImpactReport(BaseModel):
    """Contrato raíz de data/pulse/private/impact_report.json (INV-PULSE-6 / INV-PULSE-12)."""
    version: str = "1.3.0"
    generated_at: datetime
    visibility: Literal["private"] = "private"
    total_published_posts: int = Field(ge=0)
    total_scheduled_posts: int = Field(ge=0)
    total_30d_post_views: int = Field(ge=0)
    median_post_views: float = Field(ge=0.0)
    p75_post_views: float = Field(ge=0.0)
    monthly_growth_yoy_pct: float
    total_30d_gsc_clicks: int = Field(default=0, ge=0)
    total_30d_gsc_impressions: int = Field(default=0, ge=0)
    gsc_clicks_prev_30d: int = Field(default=0, ge=0)
    gsc_impressions_prev_30d: int = Field(default=0, ge=0)
    gsc_brand_clicks_30d: int = Field(default=0, ge=0)
    gsc_brand_impressions_30d: int = Field(default=0, ge=0)
    avg_gsc_ctr_pct: float = Field(default=0.0, ge=0.0)
    avg_gsc_position: float = Field(default=0.0, ge=0.0)
    en_views_share_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    en_gsc_impressions_share_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    category_performance: List[CategoryPerformanceItem]
    quick_wins_ctr: List[QuickWinItem]
    monetization_orphans: List[MonetizationOrphanItem]
    decay_alerts: List[DecayAlertItem]
    prioritized_backlog: List[BacklogPrioritizedItem]
    release_editorial_impact: List[ReleaseEditorialImpactItem] = Field(default_factory=list)
    cannibalization_alerts: List[CannibalizationAlertItem] = Field(default_factory=list)
    channel_summary: List[ChannelSummaryItem] = Field(default_factory=list)
    hidden_channel_winners: List[HiddenChannelWinnerItem] = Field(default_factory=list)
    dark_social_alerts: List[DarkSocialAlertItem] = Field(default_factory=list)
    social_platform_summary: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    ptr_leak_alerts: List[PullThroughAlertItem] = Field(default_factory=list)
    canonical_shield_alerts: List[CanonicalShieldAlertItem] = Field(default_factory=list)
    silent_releases_count: int = 0


# ==============================================================================
# CONTRATOS PYDANTIC V2 PARA TELEMETRÍA FINANCIERA Y EJECUTIVA (HITO 9.2 / INV-PULSE-13)
# ==============================================================================

RevenueSourceStatus = Literal["ok", "unavailable", "error"]


class RevenueProductBreakdown(BaseModel):
    """Agregado anónimo de ventas por producto/kit de Lemon Squeezy (sin PII)."""
    product_id: str
    product_name: str
    orders_30d: int = Field(default=0, ge=0)
    orders_total: int = Field(default=0, ge=0)
    net_revenue_eur_30d: float = Field(default=0.0, ge=0.0)
    net_revenue_eur_total: float = Field(default=0.0, ge=0.0)
    avg_order_value_eur: float = Field(default=0.0, ge=0.0)


class RevenueCountryBreakdown(BaseModel):
    """Agregado anónimo de ventas por código ISO de país (sin ciudad, IP ni dirección)."""
    country: str
    orders_30d: int = Field(default=0, ge=0)
    net_revenue_eur_30d: float = Field(default=0.0, ge=0.0)


class RevenueMonthlyPoint(BaseModel):
    """Punto mensual agregado de ingresos netos en EUR."""
    month: str
    orders: int = Field(default=0, ge=0)
    net_revenue_eur: float = Field(default=0.0, ge=0.0)


class RevenueLanguageSlice(BaseModel):
    """Desglose agregado de pedidos e ingresos por idioma inferido (ES/EN/Other)."""
    orders_30d: int = Field(default=0, ge=0)
    net_revenue_eur_30d: float = Field(default=0.0, ge=0.0)


class LemonSqueezySummary(BaseModel):
    """Resumen financiero agregado de Lemon Squeezy sin ningún dato personal (INV-PULSE-13)."""
    status: RevenueSourceStatus = "unavailable"
    last_synced_at: Optional[str] = None
    currency: Literal["EUR"] = "EUR"
    net_revenue_eur_30d: float = Field(default=0.0, ge=0.0)
    net_revenue_eur_total: float = Field(default=0.0, ge=0.0)
    orders_30d: int = Field(default=0, ge=0)
    orders_total: int = Field(default=0, ge=0)
    refunded_orders_30d: int = Field(default=0, ge=0)
    avg_order_value_eur: float = Field(default=0.0, ge=0.0)
    active_products_count: int = Field(default=0, ge=0)
    checkouts_created_30d: int = Field(default=0, ge=0)
    checkouts_completed_30d: int = Field(default=0, ge=0)
    checkout_abandonment_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    language_breakdown: Dict[str, RevenueLanguageSlice] = Field(default_factory=dict)
    by_product: List[RevenueProductBreakdown] = Field(default_factory=list)
    by_country: List[RevenueCountryBreakdown] = Field(default_factory=list)
    monthly_trend: List[RevenueMonthlyPoint] = Field(default_factory=list)
    note: str = ""


class BrevoListSummary(BaseModel):
    """Resumen agregado de una lista de contactos de Brevo (cero emails)."""
    list_id: int
    name: str
    lang_hint: Literal["es", "en", "all"] = "all"
    total_subscribers: int = Field(default=0, ge=0)
    unique_subscribers: int = Field(default=0, ge=0)


class BrevoCampaignSummary(BaseModel):
    """Métricas agregadas de una campaña enviada en Brevo."""
    campaign_id: int
    name: str
    sent_date: Optional[str] = None
    delivered: int = Field(default=0, ge=0)
    unique_opens: int = Field(default=0, ge=0)
    open_rate_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    unique_clicks: int = Field(default=0, ge=0)
    ctr_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    unsubscribes: int = Field(default=0, ge=0)


class BrevoAudienceSummary(BaseModel):
    """Resumen agregado de listas y campañas de Brevo (cero PII)."""
    status: RevenueSourceStatus = "unavailable"
    last_synced_at: Optional[str] = None
    total_lists: int = Field(default=0, ge=0)
    total_subscribers: int = Field(default=0, ge=0)
    es_subscribers: int = Field(default=0, ge=0)
    en_subscribers: int = Field(default=0, ge=0)
    waitlist_helix_subscribers: int = Field(default=0, ge=0)
    campaigns_analyzed: int = Field(default=0, ge=0)
    avg_open_rate_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    avg_ctr_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    total_unsubscribes: int = Field(default=0, ge=0)
    lists: List[BrevoListSummary] = Field(default_factory=list)
    recent_campaigns: List[BrevoCampaignSummary] = Field(default_factory=list)
    note: str = ""


class RevenueMetricsReport(BaseModel):
    """Contrato raíz privado de data/pulse/private/revenue_metrics.json (gitignored, INV-PULSE-13)."""
    version: str = "1.0.0"
    visibility: Literal["private"] = "private"
    pii_stripped: Literal[True] = True
    generated_at: datetime
    lemon_squeezy: LemonSqueezySummary
    brevo: BrevoAudienceSummary


class ExecutiveStateSnapshot(BaseModel):
    """Bus ejecutivo unificado para 00-chief-orchestrator y Datalaria Mercator (INV-PULSE-13)."""
    version: str = "1.0.0"
    visibility: Literal["private"] = "private"
    pii_stripped: Literal[True] = True
    generated_at: datetime
    north_star_target_eur_month: float = Field(default=500.0, gt=0.0)
    stage_label: str = "Estadio 1 (0 -> 500 €/mes)"
    stage_progress_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    revenue: Dict[str, Any] = Field(default_factory=dict)
    audience: Dict[str, Any] = Field(default_factory=dict)
    traffic_seo: Dict[str, Any] = Field(default_factory=dict)
    social: Dict[str, Any] = Field(default_factory=dict)
    catalog_health: Dict[str, Any] = Field(default_factory=dict)
    top_priorities: List[str] = Field(default_factory=list)

