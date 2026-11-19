import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { ALLOWED_PAGE_SIZES } from '../../lib/sportFormatters';
import './Paginator.css';

/**
 * Compute visible page tokens with ellipsis for desktop pagination.
 */
function buildPageItems(currentPage, totalPages) {
  if (totalPages <= 7) {
    return Array.from({ length: totalPages }, (_, idx) => idx + 1);
  }

  const pages = [1];
  const left = Math.max(2, currentPage - 1);
  const right = Math.min(totalPages - 1, currentPage + 1);

  if (left > 2) pages.push('ellipsis-left');
  for (let p = left; p <= right; p += 1) {
    pages.push(p);
  }
  if (right < totalPages - 1) pages.push('ellipsis-right');
  pages.push(totalPages);

  return pages;
}

/**
 * Segmented selector for page size (12 | 24 | 48).
 */
export function PageSizeSelector({ pageSize, onChange, disabled = false }) {
  const { t } = useLanguage();

  return (
    <div
      className="page-size-selector glass-panel"
      role="group"
      aria-label={t('sport.pagination.perPageLabel')}
    >
      <span className="page-size-label">{t('sport.pagination.perPageShort')}</span>
      <div className="page-size-pills">
        {ALLOWED_PAGE_SIZES.map((size) => (
          <button
            key={size}
            type="button"
            className={`page-size-btn ${pageSize === size ? 'active' : ''}`}
            aria-pressed={pageSize === size}
            disabled={disabled}
            onClick={() => onChange(size)}
          >
            {size}
          </button>
        ))}
      </div>
    </div>
  );
}

/**
 * Adaptive Paginator: full numbered pills on desktop (>768px),
 * compact touch-friendly "‹ 2 / 6 ›" (>= 44px targets) on mobile (<=768px).
 */
export function Paginator({
  page,
  pageSize,
  total,
  totalPages,
  onPageChange,
  onPageSizeChange,
  disabled = false,
}) {
  const { t } = useLanguage();

  if (typeof total !== 'number' || total === 0) {
    return null;
  }

  const startItem = Math.min((page - 1) * pageSize + 1, total);
  const endItem = Math.min(page * pageSize, total);
  const pageItems = buildPageItems(page, totalPages);

  const rangeText = t('sport.pagination.rangeText')
    .replace('{start}', String(startItem))
    .replace('{end}', String(endItem))
    .replace('{total}', String(total));

  const compactPageText = t('sport.pagination.compactPage')
    .replace('{page}', String(page))
    .replace('{totalPages}', String(totalPages));

  return (
    <div className="paginator-bar glass-panel">
      <div className="paginator-info">
        <span className="paginator-range-text">{rangeText}</span>
      </div>

      {totalPages > 1 && (
        <nav className="paginator-nav" aria-label={t('sport.pagination.navAriaLabel')}>
          <button
            type="button"
            className="paginator-step-btn"
            disabled={disabled || page <= 1}
            onClick={() => onPageChange(page - 1)}
            aria-label={t('sport.pagination.previous')}
          >
            <ChevronLeft size={16} />
            <span className="paginator-step-label">{t('sport.pagination.previous')}</span>
          </button>

          {/* Desktop numbered pages */}
          <div className="paginator-pages-desktop">
            {pageItems.map((item) => {
              if (typeof item === 'string') {
                return (
                  <span key={item} className="paginator-ellipsis" aria-hidden="true">
                    …
                  </span>
                );
              }
              const isCurrent = item === page;
              return (
                <button
                  key={item}
                  type="button"
                  className={`paginator-page-btn ${isCurrent ? 'active' : ''}`}
                  aria-current={isCurrent ? 'page' : undefined}
                  disabled={disabled}
                  onClick={() => onPageChange(item)}
                >
                  {item}
                </button>
              );
            })}
          </div>

          {/* Mobile compact indicator */}
          <div className="paginator-pages-mobile" aria-live="polite">
            <span>{compactPageText}</span>
          </div>

          <button
            type="button"
            className="paginator-step-btn"
            disabled={disabled || page >= totalPages}
            onClick={() => onPageChange(page + 1)}
            aria-label={t('sport.pagination.next')}
          >
            <span className="paginator-step-label">{t('sport.pagination.next')}</span>
            <ChevronRight size={16} />
          </button>
        </nav>
      )}

      {onPageSizeChange && (
        <div className="paginator-size-inline">
          <PageSizeSelector
            pageSize={pageSize}
            onChange={onPageSizeChange}
            disabled={disabled}
          />
        </div>
      )}
    </div>
  );
}
