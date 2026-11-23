export type AssetType = 'post' | 'app' | 'kit' | 'suite' | 'mega_bundle';
export type AssetStatus = 'idea' | 'draft' | 'review' | 'scheduled' | 'published';
export type LanguageParity = 'complete' | 'missing_en' | 'missing_es' | 'outdated_en' | 'outdated_es';
export type FreshnessStatus = 'fresh' | 'review_soon' | 'stale';

export interface SeoAudit {
  score_0_100: number;
  title_ok: boolean;
  description_ok: boolean;
  parity_ok: boolean;
  taxonomy_ok: boolean;
  internal_links_ok: boolean;
  issues: string[];
}

export interface RelativeMetrics {
  index_100: number;
  rank_pct: number;
  trend_30d_pct: number;
  gsc_opportunity: boolean;
}

export interface ContentAsset {
  id: string;
  slug: string;
  asset_type: AssetType;
  status: AssetStatus;
  visibility: 'public' | 'private';

  version?: string | null;
  release_type?: 'article' | 'initial_launch' | 'version_upgrade' | 'kit_launch' | 'kit_edition' | null;
  parent_asset_id?: string | null;
  editorial_post_slug?: string | null;

  title_es?: string | null;
  title_en?: string | null;
  url_es?: string | null;
  url_en?: string | null;
  brief_es?: string | null;
  brief_en?: string | null;

  publish_date?: string | null;
  last_modified_es?: string | null;
  last_modified_en?: string | null;

  language_parity: LanguageParity;
  category: string;
  categories: string[];
  tags: string[];
  series?: string | null;
  word_count_es: number;
  word_count_en: number;
  reading_time_min: number;

  related_app?: string | null;
  related_kit?: string | null;
  included_kits?: string[];

  price?: string | null;
  original_price?: string | null;
  checkout_url?: string | null;
  deliverables?: string[];

  seo_audit: SeoAudit;
  freshness_status: FreshnessStatus;
  owner: string;
  campaign?: string | null;
  social_channels: string[];

  metrics_relative?: RelativeMetrics | null;
  is_local_idea?: boolean;
  is_cloud_idea?: boolean;
  cloud_user_id?: string;
}

export interface MonthlyTrafficPoint {
  month: string;
  label: string;
  index_100: number;
}

export interface PublicPulseDataset {
  version: string;
  generated_at: string;
  total_assets: number;
  published_assets: number;
  scheduled_assets: number;
  ideas_count: number;
  parity_summary: Record<string, number>;
  monthly_traffic_index?: MonthlyTrafficPoint[];
  assets: ContentAsset[];
}

export interface OmnichannelFunnel4Layers {
  native_reach: number;
  avg_ptr_pct: number;
  ga4_social_sessions: number;
  ga4_social_key_events: number;
  avg_social_engagement_sec: number;
  gsc_clicks_30d: number;
  gsc_clicks_prev_30d: number;
  gsc_lift_pct: number;
}

export interface OmnichannelSummaryItem {
  channel: string;
  sessions_30d: number;
  sessions_es_30d: number;
  sessions_en_30d: number;
  en_share_pct: number;
  users_30d: number;
  engaged_sessions_30d: number;
  engagement_rate_pct: number;
  avg_engagement_sec: number;
  key_events_30d: number;
  conversion_rate_pct: number;
  sessions_prev_30d: number;
  trend_30d_pct: number;
}

export interface OmnichannelSocialPlatformSummary {
  platform: string;
  status: string;
  source?: string;
  scope?: string;
  last_synced_at?: string | null;
  articles_count?: number;
  posts_count?: number;
  matched_assets_count?: number;
  native_views?: number;
  total_impressions?: number;
  total_clicks?: number;
  native_ctr_pct?: number;
  native_reactions?: number;
  total_reactions?: number;
  native_comments?: number;
  total_comments?: number;
  followers_count?: number;
  ga4_sessions_30d: number;
  ptr_pct?: number;
  note?: string;
}

export interface OmnichannelMatrixRow {
  channel: string;
  category: string;
  sessions_30d: number;
  sessions_es_30d: number;
  sessions_en_30d: number;
  en_share_pct: number;
  key_events_30d: number;
  avg_engagement_sec: number;
}

export interface OmnichannelCategoryRoiItem {
  category: string;
  editorial_roi_score: number;
  social_traction_score: number;
  monetization_coverage_pct: number;
  total_views_30d: number;
  en_traffic_share_pct: number;
}

export interface OmnichannelRecommendationItem {
  id: string;
  agent: 'E02' | 'E06';
  type: 'ptr_leak' | 'hidden_winner' | 'dark_social' | 'canonical_shield';
  severity: 'high' | 'medium';
  channel: string;
  asset_or_ref: string;
  action: string;
}

export interface OmnichannelIntelligence {
  generated_at: string;
  is_synthetic: boolean;
  roi_formula_version: string;
  x_standby_zero_cost: boolean;
  funnel_4_layers: OmnichannelFunnel4Layers;
  channel_summary: OmnichannelSummaryItem[];
  social_funnel: Record<string, OmnichannelSocialPlatformSummary>;
  channel_category_matrix: OmnichannelMatrixRow[];
  category_roi_v2: OmnichannelCategoryRoiItem[];
  top_recommendations: OmnichannelRecommendationItem[];
}

