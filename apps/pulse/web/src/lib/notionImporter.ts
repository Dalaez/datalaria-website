import { ContentAsset } from '../types';

export function parseNotionCsv(csvText: string): ContentAsset[] {
  const lines = csvText.split(/\r?\n/).filter((l) => l.trim().length > 0);
  if (lines.length < 2) return [];

  // Parse header
  const parseRow = (rowStr: string): string[] => {
    const result: string[] = [];
    let current = '';
    let inQuotes = false;
    for (let i = 0; i < rowStr.length; i++) {
      const char = rowStr[i];
      if (char === '"') {
        if (inQuotes && rowStr[i + 1] === '"') {
          current += '"';
          i++;
        } else {
          inQuotes = !inQuotes;
        }
      } else if (char === ',' && !inQuotes) {
        result.push(current.trim());
        current = '';
      } else {
        current += char;
      }
    }
    result.push(current.trim());
    return result;
  };

  const headers = parseRow(lines[0]).map((h) => h.toLowerCase().trim());
  const assets: ContentAsset[] = [];

  for (let idx = 1; idx < lines.length; idx++) {
    const row = parseRow(lines[idx]);
    if (row.length === 0 || !row[0]) continue;

    const getCol = (name: string): string => {
      const colIdx = headers.findIndex((h) => h.includes(name));
      return colIdx >= 0 && colIdx < row.length ? row[colIdx] : '';
    };

    const title = getCol('title') || `Item ${idx}`;
    const brief = getCol('content brief') || getCol('brief') || '';
    const statusRaw = getCol('status').toLowerCase();
    const cat = getCol('category') || 'General';
    const dateRaw = getCol('publish date') || getCol('date') || '';
    const link = getCol('link') || '';
    const tagsRaw = getCol('tags') || '';
    const wordCount = parseInt(getCol('word count') || '0', 10) || 0;

    let status: ContentAsset['status'] = 'idea';
    if (statusRaw.includes('publish')) status = 'published';
    else if (statusRaw.includes('sched')) status = 'scheduled';
    else if (statusRaw.includes('review')) status = 'review';
    else if (statusRaw.includes('draft')) status = 'draft';

    const tags = tagsRaw
      ? tagsRaw.split(',').map((t) => t.trim()).filter(Boolean)
      : [];

    const isEn = link.includes('/en/') || title.match(/\b(the|and|how|why|with|in|to)\b/i);

    assets.push({
      id: `notion-import-${idx}`,
      slug: title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, ''),
      asset_type: 'post',
      status,
      visibility: 'public',
      title_es: !isEn ? title : null,
      title_en: isEn ? title : null,
      url_es: !isEn && link ? link : null,
      url_en: isEn && link ? link : null,
      brief_es: !isEn ? brief : null,
      brief_en: isEn ? brief : null,
      publish_date: dateRaw || null,
      language_parity: 'complete',
      category: cat,
      categories: [cat],
      tags,
      word_count_es: !isEn ? wordCount : 0,
      word_count_en: isEn ? wordCount : 0,
      reading_time_min: Math.max(1, Math.ceil(wordCount / 200)),
      freshness_status: 'fresh',
      owner: getCol('author') || 'Usuario',
      social_channels: [],
      seo_audit: {
        score_0_100: 75,
        title_ok: title.length >= 35 && title.length <= 95,
        description_ok: brief.length >= 75,
        parity_ok: true,
        taxonomy_ok: tags.length >= 3,
        internal_links_ok: true,
        issues: []
      },
      metrics_relative: {
        index_100: 100,
        rank_pct: 50,
        trend_30d_pct: 0,
        gsc_opportunity: false
      }
    });
  }

  return assets;
}
