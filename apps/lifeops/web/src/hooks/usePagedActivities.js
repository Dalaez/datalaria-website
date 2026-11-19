import { useCallback, useEffect, useRef, useState } from 'react';
import { api, isMockModeEnabled } from '../lib/api';

function buildPagedEndpointKey(activityType, page, pageSize) {
  const params = new URLSearchParams();
  if (activityType) params.append('activity_type', activityType);
  params.append('page', String(page));
  params.append('page_size', String(pageSize));
  return `/api/v1/activities/paged?${params.toString()}`;
}

function buildSummaryCacheKey(activityType) {
  return `/api/v1/activities/paged-summary?activity_type=${activityType || 'all'}`;
}

/**
 * Reusable SWR pagination hook for Personal Area modules (ADR-030).
 * Implements 0 ms local hydration (page cache or Dashboard seed), explicit
 * 4-state lifecycle (never masks errors as empty state, INV-16), decoupled
 * summary KPI loading (include_summary), and idle prefetching of page + 1.
 */
export function usePagedActivities({ userId, activityType = 'sport', page = 1, pageSize = 12 }) {
  const isMock = isMockModeEnabled();

  const [items, setItems] = useState([]);
  const [summary, setSummary] = useState(null);
  const [total, setTotal] = useState(null);
  const [totalPages, setTotalPages] = useState(1);
  const [hasMore, setHasMore] = useState(false);

  const [hasHydrated, setHasHydrated] = useState(false);
  const [isSyncing, setIsSyncing] = useState(true);
  const [error, setError] = useState(null);
  const [elapsedSec, setElapsedSec] = useState(0);
  const [retryAttempt, setRetryAttempt] = useState(0);

  const summaryRef = useRef(null);
  const hasHydratedRef = useRef(false);
  const abortControllerRef = useRef(null);
  const idlePrefetchRef = useRef(null);

  useEffect(() => {
    summaryRef.current = summary;
  }, [summary]);

  useEffect(() => {
    hasHydratedRef.current = hasHydrated;
  }, [hasHydrated]);

  // Live seconds timer while syncing with cloud
  useEffect(() => {
    if (!isSyncing) {
      setElapsedSec(0);
      return undefined;
    }
    const timer = setInterval(() => {
      setElapsedSec((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [isSyncing]);

  // Instant 0 ms SWR hydration when userId/page/pageSize changes
  const hydrateFromCache = useCallback(
    (targetPage, targetSize) => {
      if (isMock || !userId) return false;

      const pageKey = buildPagedEndpointKey(activityType, targetPage, targetSize);
      const cachedPage = api.getCachedEndpoint(userId, pageKey);
      const cachedSummary = api.getCachedEndpoint(userId, buildSummaryCacheKey(activityType));

      if (cachedSummary) {
        setSummary(cachedSummary);
        summaryRef.current = cachedSummary;
      }

      if (cachedPage && Array.isArray(cachedPage.items)) {
        setItems(cachedPage.items);
        setTotal(typeof cachedPage.total === 'number' ? cachedPage.total : cachedPage.items.length);
        setTotalPages(cachedPage.total_pages || 1);
        setHasMore(Boolean(cachedPage.has_more));
        if (cachedPage.summary) {
          setSummary(cachedPage.summary);
          summaryRef.current = cachedPage.summary;
        }
        setHasHydrated(true);
        hasHydratedRef.current = true;
        return true;
      }

      // AUD-6: Seed page 1 instantaneously from Dashboard's cached sport list if available
      if (targetPage === 1 && activityType === 'sport') {
        const seed = api.getCachedSportSeed(userId, targetSize);
        if (seed) {
          setItems(seed.items);
          setTotal(seed.total);
          setTotalPages(seed.total_pages);
          setHasMore(seed.has_more);
          if (!summaryRef.current && seed.summary) {
            setSummary(seed.summary);
            summaryRef.current = seed.summary;
          }
          setHasHydrated(true);
          hasHydratedRef.current = true;
          return true;
        }
      }

      return false;
    },
    [activityType, isMock, userId]
  );

  const scheduleNextPagePrefetch = useCallback(
    (nextPage, targetSize) => {
      if (isMock || !userId) return;
      if (idlePrefetchRef.current) {
        clearTimeout(idlePrefetchRef.current);
      }
      idlePrefetchRef.current = setTimeout(() => {
        api
          .getActivitiesPaged(activityType, {
            page: nextPage,
            pageSize: targetSize,
            includeSummary: false,
            retry: false,
          })
          .catch(() => null);
      }, 350);
    },
    [activityType, isMock, userId]
  );

  const fetchPage = useCallback(
    async ({ targetPage = page, targetSize = pageSize, forceSummary = false } = {}) => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      const controller = new AbortController();
      abortControllerRef.current = controller;

      setError(null);
      setRetryAttempt(0);
      setIsSyncing(true);

      const needSummary = forceSummary || summaryRef.current == null;

      try {
        const res = await api.getActivitiesPaged(activityType, {
          page: targetPage,
          pageSize: targetSize,
          includeSummary: needSummary,
          retry: true,
          signal: controller.signal,
          onRetryAttempt: (attempt) => {
            if (!controller.signal.aborted) {
              setRetryAttempt(attempt);
            }
          },
        });

        if (controller.signal.aborted) return;

        const nextItems = Array.isArray(res?.items) ? res.items : [];
        const nextTotal = typeof res?.total === 'number' ? res.total : nextItems.length;
        const nextTotalPages = res?.total_pages || Math.max(1, Math.ceil(nextTotal / targetSize));
        const nextHasMore = Boolean(res?.has_more);

        setItems(nextItems);
        setTotal(nextTotal);
        setTotalPages(nextTotalPages);
        setHasMore(nextHasMore);

        if (res?.summary) {
          setSummary(res.summary);
          summaryRef.current = res.summary;
        }

        setHasHydrated(true);
        hasHydratedRef.current = true;
        setError(null);
        setIsSyncing(false);

        if (nextHasMore) {
          scheduleNextPagePrefetch(targetPage + 1, targetSize);
        }
      } catch (err) {
        if (controller.signal.aborted || err?.name === 'AbortError') {
          return;
        }
        setError(err?.message || 'Error al cargar actividades');
        setIsSyncing(false);
      }
    },
    [activityType, page, pageSize, scheduleNextPagePrefetch]
  );

  useEffect(() => {
    hydrateFromCache(page, pageSize);
    fetchPage({ targetPage: page, targetSize: pageSize, forceSummary: summaryRef.current == null });

    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      if (idlePrefetchRef.current) {
        clearTimeout(idlePrefetchRef.current);
      }
    };
  }, [page, pageSize, userId, hydrateFromCache, fetchPage]);

  const reload = useCallback(
    ({ forceSummary = true, targetPage = page, targetSize = pageSize } = {}) => {
      return fetchPage({ targetPage, targetSize, forceSummary });
    },
    [fetchPage, page, pageSize]
  );

  const invalidateSummary = useCallback(() => {
    summaryRef.current = null;
  }, []);

  return {
    items,
    summary,
    total,
    totalPages,
    hasMore,
    hasHydrated,
    loading: !hasHydrated && isSyncing && !error,
    isSyncing,
    isPageTransitioning: hasHydrated && isSyncing,
    error,
    elapsedSec,
    retryAttempt,
    reload,
    invalidateSummary,
  };
}
