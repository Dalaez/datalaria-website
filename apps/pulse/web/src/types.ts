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
