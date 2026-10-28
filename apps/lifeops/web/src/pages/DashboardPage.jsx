import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../lib/api';
import {
  CATEGORY_COLORS,
  addDays,
  aggregateSlice,
  buildConsistencyHeatmap,
  buildSubcategoryBreakdown,
  buildTimeSeries,
  computeDelta,
  filterRecords,
  formatDurationCompact,
  formatPaceMinKm,
  normalizeRecords,
  parseIsoDate,
  resolveTimeWindows,
  toIsoDateString,
} from '../lib/analyticsEngine';
import { StatWidget } from '../components/Dashboard/StatWidget';
import { QuickActions } from '../components/Dashboard/QuickActions';
import { SystemHealth } from '../components/Dashboard/SystemHealth';
import {
  Activity,
  Award,
  BarChart3,
  BookOpen,
  Briefcase,
  Calendar,
  CheckCircle2,
  CheckSquare,
  Clock,
  Film,
  Flame,
  Layers,
  PieChart as PieChartIcon,
  RefreshCw,
  RotateCcw,
  Star,
  TrendingUp,
} from 'lucide-react';
import {
  Bar,
  CartesianGrid,
  Cell,
  ComposedChart,
  Line,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import './DashboardPage.css';

const SPORT_SUBCATEGORIES = ['all', 'running', 'cycling', 'gym', 'swimming', 'hiking', 'crossfit', 'other'];
const BOOK_SUBCATEGORIES = ['all', 'completed', 'reading', 'wishlist'];
const FILM_SUBCATEGORIES = ['all', 'movie', 'series', 'documentary', 'anime'];
const TASK_SUBCATEGORIES = ['all', 'done', 'in_progress', 'review', 'todo'];

function getInitialParam(name, fallback) {
  if (typeof window === 'undefined') return fallback;
  try {
    const url = new URL(window.location.href);
    const hashQuery = window.location.hash.includes('?') ? window.location.hash.split('?')[1] : '';
    const sp = new URLSearchParams(url.search ? `${url.search}&${hashQuery}` : hashQuery);
    return sp.get(name) || fallback;
  } catch {
    return fallback;
  }
}

export function DashboardPage() {
  const { user } = useAuth();
  const { t, language } = useLanguage();
  const navigate = useNavigate();

  // Raw datasets & Sync state
  const [summary, setSummary] = useState(null);
  const [activities, setActivities] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [isSyncing, setIsSyncing] = useState(true);
  const [hasHydratedData, setHasHydratedData] = useState(false);
  const [elapsedSec, setElapsedSec] = useState(() => Number(getInitialParam('sec', '0')));
  const autoPeriodAppliedRef = useRef(false);

  // Interactive Analytics Filter State (with query param support for deep linking / mockups)
  const now = new Date();
  const initialCat = getInitialParam('cat', 'all');
  const initialSubcat = getInitialParam('subcat', 'all');
  const initialPeriod = getInitialParam('period', 'month');
  const initialMetric = getInitialParam('metric', initialCat === 'sport' ? 'distance_km' : 'count');

  const [period, setPeriod] = useState(initialPeriod); // 'week' | 'month' | 'calendar_month' | 'quarter' | 'year'
  const [selectedYear, setSelectedYear] = useState(now.getFullYear());
  const [selectedMonth, setSelectedMonth] = useState(now.getMonth());
  const [comparePrev, setComparePrev] = useState(true);
  const [category, setCategory] = useState(initialCat); // 'all' | 'sport' | 'book' | 'film' | 'tasks'
  const [subcategory, setSubcategory] = useState(initialSubcat);
  const [metric, setMetric] = useState(initialMetric); // 'count' | 'distance_km' | 'calories' | 'duration_hours' | 'pages_read' | 'elevation_m'

  const applyAutoPeriodIfNeeded = (acts) => {
    if (autoPeriodAppliedRef.current || !Array.isArray(acts) || acts.length === 0) return;
    autoPeriodAppliedRef.current = true;

    const today = new Date();
    const cutoff30 = addDays(today, -29);
    const cutoff90 = addDays(today, -89);

    const hasInLast30 = acts.some((a) => {
      const d = parseIsoDate(a.date);
      return d && d >= cutoff30;
    });
    if (hasInLast30) return; // Keep 'month' (30 Days)

    const hasInLast90 = acts.some((a) => {
      const d = parseIsoDate(a.date);
      return d && d >= cutoff90;
    });
    if (hasInLast90) {
      setPeriod('quarter'); // Auto-select 90 Days so existing records are immediately visible
      return;
    }

    setPeriod('year');
  };

  // 1. Instant Stale-While-Revalidate Hydration from local cache
  useEffect(() => {
    if (!user?.id) return;
    const cached = api.getCachedDashboardBundle(user.id);
    if (cached) {
      if (cached.summary) setSummary(cached.summary);
      if (Array.isArray(cached.activities) && cached.activities.length > 0) {
        setActivities(cached.activities);
        setHasHydratedData(true);
        applyAutoPeriodIfNeeded(cached.activities);
      }
      if (Array.isArray(cached.tasks)) setTasks(cached.tasks);
    }
  }, [user?.id]);

  // 2. Live elapsed timer while syncing with cloud
  useEffect(() => {
    if (!isSyncing) {
      setElapsedSec(0);
      return undefined;
    }
    const interval = setInterval(() => {
      setElapsedSec((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, [isSyncing]);

  // 3. Fetch fresh data from API (limit: 200 matches Render's le=200 contract)
  useEffect(() => {
    let timeoutId;
    let isMounted = true;

    async function loadDashboardData() {
      if (isMounted) setIsSyncing(true);
      try {
        const [summaryData, activitiesData, tasksData] = await Promise.all([
          api.getDashboardSummary().catch(() => null),
          api.getActivitiesWithDetails(null, { limit: 200 }).catch(() => null),
          api.getTasks().catch(() => null),
        ]);

        if (!isMounted) return;

        if (summaryData) setSummary(summaryData);
        if (Array.isArray(activitiesData)) {
          setActivities(activitiesData);
          applyAutoPeriodIfNeeded(activitiesData);
        }
        if (Array.isArray(tasksData)) setTasks(tasksData);

        if (summaryData || Array.isArray(activitiesData)) {
          setHasHydratedData(true);
          setIsSyncing(false);
        } else {
          // Backend container on Render is still waking up -> retry in 5s
          timeoutId = setTimeout(loadDashboardData, 5000);
        }
      } catch (err) {
        console.error('Error loading 360 analytics:', err);
        if (isMounted) {
          timeoutId = setTimeout(loadDashboardData, 5000);
        }
      }
    }

    loadDashboardData();
    return () => {
      isMounted = false;
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, []);

  // Available metrics per category
  const availableMetrics = useMemo(() => {
    if (category === 'sport') {
      return [
        { id: 'count', label: t('dashboard.analytics.metricSessions'), unit: '' },
        { id: 'distance_km', label: t('dashboard.analytics.metricDistance'), unit: 'km' },
        { id: 'calories', label: t('dashboard.analytics.metricCalories'), unit: 'kcal' },
        { id: 'duration_hours', label: t('dashboard.analytics.metricDuration'), unit: 'h' },
        { id: 'elevation_m', label: t('dashboard.analytics.metricElevation'), unit: 'm' },
      ];
    }
    if (category === 'book') {
      return [
        { id: 'count', label: t('dashboard.analytics.metricCount'), unit: '' },
        { id: 'pages_read', label: t('dashboard.analytics.metricPages'), unit: 'pág' },
      ];
    }
    if (category === 'film') {
      return [
        { id: 'count', label: t('dashboard.analytics.metricCount'), unit: '' },
      ];
    }
    if (category === 'tasks') {
      return [
        { id: 'count', label: t('dashboard.analytics.metricCount'), unit: '' },
        { id: 'duration_hours', label: t('dashboard.analytics.metricDuration'), unit: 'h' },
      ];
    }
    return [
      { id: 'count', label: t('dashboard.analytics.metricCount'), unit: '' },
      { id: 'distance_km', label: t('dashboard.analytics.metricDistance'), unit: 'km' },
      { id: 'calories', label: t('dashboard.analytics.metricCalories'), unit: 'kcal' },
      { id: 'duration_hours', label: t('dashboard.analytics.metricDuration'), unit: 'h' },
    ];
  }, [category, t]);

  // Keep selected metric valid when switching categories
  const activeMetric = useMemo(() => {
    if (availableMetrics.some((m) => m.id === metric)) return metric;
    return availableMetrics[0].id;
  }, [availableMetrics, metric]);

  const activeMetricUnit = useMemo(() => {
    const found = availableMetrics.find((m) => m.id === activeMetric);
    return found ? found.unit : '';
  }, [availableMetrics, activeMetric]);

  const handleCategoryChange = (newCat) => {
    setCategory(newCat);
    setSubcategory('all');
    if (newCat === 'sport') setMetric('distance_km');
    else if (newCat === 'book') setMetric('pages_read');
    else setMetric('count');
  };

  // Normalize all records once
  const allRecords = useMemo(() => normalizeRecords(activities, tasks), [activities, tasks]);

  // Resolve current and previous period dates
  const windowInfo = useMemo(
    () =>
      resolveTimeWindows({
        period,
        selectedYear,
        selectedMonth,
      }),
    [period, selectedYear, selectedMonth]
  );

  // Filter records for current and previous periods
  const currRecords = useMemo(
    () =>
      filterRecords(allRecords, {
        category,
        subcategory,
        start: windowInfo.currStart,
        end: windowInfo.currEnd,
      }),
    [allRecords, category, subcategory, windowInfo]
  );

  const prevRecords = useMemo(
    () =>
      filterRecords(allRecords, {
        category,
        subcategory,
        start: windowInfo.prevStart,
        end: windowInfo.prevEnd,
      }),
    [allRecords, category, subcategory, windowInfo]
  );

  const currStats = useMemo(() => aggregateSlice(currRecords), [currRecords]);
  const prevStats = useMemo(() => aggregateSlice(prevRecords), [prevRecords]);

  // Time-series chart data
  const timeSeriesData = useMemo(
    () =>
      buildTimeSeries({
        currRecords,
        prevRecords,
        windowInfo,
        metric: activeMetric,
        language,
      }),
    [currRecords, prevRecords, windowInfo, activeMetric, language]
  );

  // Subcategory distribution data
  const subcategoryData = useMemo(
    () =>
      buildSubcategoryBreakdown({
        currRecords,
        category,
        subcategory,
        metric: activeMetric,
        language,
        t,
      }),
    [currRecords, category, subcategory, activeMetric, language, t]
  );

  // 16-week daily consistency heatmap
  const heatmapData = useMemo(
    () =>
      buildConsistencyHeatmap({
        allRecords,
        category,
        subcategory,
        metric: activeMetric,
        weeksCount: 16,
      }),
    [allRecords, category, subcategory, activeMetric]
  );

  const forceBanner = getInitialParam('banner', 'false') === 'true';
  const showInitialBlockingLoader = (isSyncing && !hasHydratedData) || forceBanner;

  // Context-Aware 4 KPI Cards with Period-over-Period Trend
  const kpiCards = useMemo(() => {
    const maskIfLoading = (val) => (showInitialBlockingLoader ? '···' : val);

    if (category === 'sport') {
      const subLabel =
        subcategory !== 'all'
          ? t(`sport.types.${subcategory}`).replace(/^[^\wÁÉÍÓÚáéíóúÑñ]+\s*/, '')
          : language === 'es'
            ? 'Deporte Total'
            : 'All Sports';
      const avgKm =
        currStats.sportCount > 0 ? (currStats.distanceKm / currStats.sportCount).toFixed(1) : '0.0';
      const paceOrSpeed =
        subcategory === 'cycling' && currStats.durationHours > 0
          ? `${(currStats.distanceKm / currStats.durationHours).toFixed(1)} km/h`
          : formatPaceMinKm(currStats.totalSeconds, currStats.distanceKm);

      return [
        {
          id: 'sport-sessions',
          title: `${language === 'es' ? 'Sesiones' : 'Sessions'} (${subLabel})`,
          value: maskIfLoading(currStats.sportCount),
          subtitle: `${currStats.pbCount} PB · ${language === 'es' ? 'Ant:' : 'Prev:'} ${prevStats.sportCount}`,
          icon: Activity,
          color: 'emerald',
          trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.sportCount, prevStats.sportCount, '', language) : null,
        },
        {
          id: 'sport-distance',
          title: language === 'es' ? 'Distancia Recorrida' : 'Total Distance',
          value: maskIfLoading(`${currStats.distanceKm.toFixed(1)} km`),
          subtitle: `${avgKm} km / ${language === 'es' ? 'sesión' : 'session'}`,
          icon: TrendingUp,
          color: 'cyan',
          trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.distanceKm, prevStats.distanceKm, 'km', language) : null,
        },
        {
          id: 'sport-time',
          title: language === 'es' ? 'Tiempo Activo & Ritmo' : 'Active Time & Pace',
          value: maskIfLoading(formatDurationCompact(currStats.totalSeconds)),
          subtitle: `${language === 'es' ? 'Ritmo/Vel:' : 'Pace/Spd:'} ${paceOrSpeed}`,
          icon: Clock,
          color: 'purple',
          trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.durationHours, prevStats.durationHours, 'h', language) : null,
        },
        {
          id: 'sport-calories',
          title: language === 'es' ? 'Calorías & Esfuerzo' : 'Calories & Effort',
          value: maskIfLoading(`${currStats.calories.toLocaleString()} kcal`),
          subtitle: `${currStats.avgHeartRate ? `${currStats.avgHeartRate} ppm` : '—'} · +${currStats.elevationM} m`,
          icon: Flame,
          color: 'amber',
          trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.calories, prevStats.calories, 'kcal', language) : null,
        },
      ];
    }

    if (category === 'book') {
      return [
        {
          id: 'book-count',
          title: language === 'es' ? 'Libros en Periodo' : 'Books in Period',
          value: maskIfLoading(currStats.bookCount),
          subtitle: `${currStats.booksCompleted} ${language === 'es' ? 'completados' : 'completed'}`,
          icon: BookOpen,
          color: 'cyan',
          trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.bookCount, prevStats.bookCount, '', language) : null,
        },
        {
          id: 'book-pages',
          title: language === 'es' ? 'Páginas Leídas' : 'Pages Read',
          value: maskIfLoading(currStats.pagesRead.toLocaleString()),
          subtitle: `${language === 'es' ? 'Periodo anterior:' : 'Previous period:'} ${prevStats.pagesRead}`,
          icon: Layers,
          color: 'emerald',
          trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.pagesRead, prevStats.pagesRead, 'pág', language) : null,
        },
        {
          id: 'book-completed',
          title: language === 'es' ? 'Libros Terminados' : 'Books Finished',
          value: maskIfLoading(currStats.booksCompleted),
          subtitle: `${language === 'es' ? 'Total histórico:' : 'All-time:'} ${summary?.books_count || activities.filter((a) => a.activity_type === 'book').length}`,
          icon: Award,
          color: 'purple',
          trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.booksCompleted, prevStats.booksCompleted, '', language) : null,
        },
        {
          id: 'book-rating',
          title: language === 'es' ? 'Valoración Media' : 'Average Rating',
          value: maskIfLoading(currStats.avgBookRating ? `${currStats.avgBookRating} ★` : '—'),
          subtitle: language === 'es' ? 'Escala de 1 a 5 estrellas' : '1 to 5 stars scale',
          icon: Star,
          color: 'amber',
          trend: null,
        },
      ];
    }

    if (category === 'film') {
      return [
        {
          id: 'film-count',
          title: language === 'es' ? 'Títulos Vistos' : 'Titles Watched',
          value: maskIfLoading(currStats.filmCount),
          subtitle: `${language === 'es' ? 'Periodo anterior:' : 'Previous period:'} ${prevStats.filmCount}`,
          icon: Film,
          color: 'purple',
          trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.filmCount, prevStats.filmCount, '', language) : null,
        },
        {
          id: 'film-movies',
          title: language === 'es' ? 'Películas' : 'Movies',
          value: maskIfLoading(currStats.moviesCount),
          subtitle: `${currStats.seriesCount} ${language === 'es' ? 'series en periodo' : 'series in period'}`,
          icon: Award,
          color: 'cyan',
          trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.moviesCount, prevStats.moviesCount, '', language) : null,
        },
        {
          id: 'film-series',
          title: language === 'es' ? 'Series & Docs' : 'Series & Docs',
          value: maskIfLoading(currStats.filmCount - currStats.moviesCount),
          subtitle: `${language === 'es' ? 'Total videoteca:' : 'All-time catalog:'} ${summary?.films_count || activities.filter((a) => a.activity_type === 'film').length}`,
          icon: Layers,
          color: 'emerald',
          trend: null,
        },
        {
          id: 'film-rating',
          title: language === 'es' ? 'Valoración Media' : 'Average Rating',
          value: maskIfLoading(currStats.avgFilmRating ? `${currStats.avgFilmRating} ★` : '—'),
          subtitle: language === 'es' ? 'Crítica personal media' : 'Average personal rating',
          icon: Star,
          color: 'amber',
          trend: null,
        },
      ];
    }

    if (category === 'tasks') {
      const totalTasksVal = currStats.tasksCount || summary?.total_tasks || tasks.length;
      const doneTasksVal = currStats.tasksCount > 0 ? currStats.tasksDone : (summary?.tasks_done ?? tasks.filter((tk) => tk.status === 'done').length);
      const completionRate = totalTasksVal > 0 ? Math.round((doneTasksVal / totalTasksVal) * 100) : 0;
      return [
        {
          id: 'tasks-total',
          title: language === 'es' ? 'Tareas Kanban' : 'Kanban Tasks',
          value: maskIfLoading(totalTasksVal),
          subtitle: `${summary?.active_projects || 0} ${language === 'es' ? 'proyectos activos' : 'active projects'}`,
          icon: Briefcase,
          color: 'amber',
          trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.tasksCount, prevStats.tasksCount, '', language) : null,
        },
        {
          id: 'tasks-done',
          title: language === 'es' ? 'Tareas Completadas' : 'Completed Tasks',
          value: maskIfLoading(doneTasksVal),
          subtitle: `${completionRate}% ${language === 'es' ? 'tasa de cierre' : 'completion rate'}`,
          icon: CheckSquare,
          color: 'emerald',
          trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.tasksDone, prevStats.tasksDone, '', language) : null,
        },
        {
          id: 'tasks-progress',
          title: language === 'es' ? 'En Curso / Pendientes' : 'In Progress / Pending',
          value: maskIfLoading((summary?.tasks_in_progress || 0) + (summary?.tasks_todo || 0) || currStats.tasksInProgress),
          subtitle: `${summary?.tasks_overdue || 0} ${language === 'es' ? 'vencidas' : 'overdue'}`,
          icon: Activity,
          color: 'purple',
          trend: null,
        },
        {
          id: 'tasks-hours',
          title: language === 'es' ? 'Carga Estimada' : 'Estimated Workload',
          value: maskIfLoading(`${currStats.durationHours} h`),
          subtitle: language === 'es' ? 'Horas planificadas en Kanban' : 'Planned Kanban hours',
          icon: Clock,
          color: 'cyan',
          trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.durationHours, prevStats.durationHours, 'h', language) : null,
        },
      ];
    }

    // Default: 'all' (360° Overview)
    const kanbanDone = currStats.tasksCount > 0 ? currStats.tasksDone : (summary?.tasks_done ?? tasks.filter((tk) => tk.status === 'done').length);
    const kanbanTotal = currStats.tasksCount > 0 ? currStats.tasksCount : (summary?.total_tasks ?? tasks.length);

    return [
      {
        id: 'all-activities',
        title: language === 'es' ? 'Registros en Periodo' : 'Records in Period',
        value: maskIfLoading(currStats.totalCount),
        subtitle: `${language === 'es' ? 'Histórico:' : 'All-time:'} ${(summary?.total_activities || activities.length) + (summary?.total_tasks || tasks.length)}`,
        icon: Activity,
        color: 'emerald',
        trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.totalCount, prevStats.totalCount, '', language) : null,
      },
      {
        id: 'all-sport',
        title: language === 'es' ? 'Deporte & Kilómetros' : 'Sport & Distance',
        value: maskIfLoading(`${currStats.distanceKm.toFixed(1)} km`),
        subtitle: `${currStats.sportCount} ${language === 'es' ? 'sesiones' : 'sessions'} · ${currStats.calories.toLocaleString()} kcal`,
        icon: Flame,
        color: 'cyan',
        trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.distanceKm, prevStats.distanceKm, 'km', language) : null,
      },
      {
        id: 'all-culture',
        title: language === 'es' ? 'Libros & Cine/Series' : 'Books & Cinema/TV',
        value: maskIfLoading(currStats.bookCount + currStats.filmCount),
        subtitle: `${currStats.pagesRead} ${language === 'es' ? 'págs' : 'pages'} · ${currStats.filmCount} ${language === 'es' ? 'títulos' : 'titles'}`,
        icon: BookOpen,
        color: 'purple',
        trend:
          !showInitialBlockingLoader && comparePrev
            ? computeDelta(currStats.bookCount + currStats.filmCount, prevStats.bookCount + prevStats.filmCount, '', language)
            : null,
      },
      {
        id: 'all-kanban',
        title: language === 'es' ? 'Tareas Kanban' : 'Kanban Tasks',
        value: maskIfLoading(`${kanbanDone}/${kanbanTotal}`),
        subtitle: `${summary?.active_projects || 0} ${language === 'es' ? 'proyectos' : 'projects'} · ${summary?.tasks_overdue || 0} ${language === 'es' ? 'vencidas' : 'overdue'}`,
        icon: CheckSquare,
        color: 'amber',
        trend: !showInitialBlockingLoader && comparePrev ? computeDelta(currStats.tasksDone, prevStats.tasksDone, '', language) : null,
      },
    ];
  }, [category, subcategory, currStats, prevStats, comparePrev, language, summary, activities, tasks, t, showInitialBlockingLoader]);

  // Subcategory pills list for current category
  const subcategoryOptions = useMemo(() => {
    if (category === 'sport') {
      return SPORT_SUBCATEGORIES.map((sc) => ({
        id: sc,
        label: sc === 'all' ? t('common.all') : t(`sport.types.${sc}`),
      }));
    }
    if (category === 'book') {
      return BOOK_SUBCATEGORIES.map((sc) => ({
        id: sc,
        label: sc === 'all' ? t('common.all') : t(`books.statuses.${sc}`),
      }));
    }
    if (category === 'film') {
      return FILM_SUBCATEGORIES.map((sc) => ({
        id: sc,
        label: sc === 'all' ? t('common.all') : t(`films.types.${sc}`),
      }));
    }
    if (category === 'tasks') {
      return TASK_SUBCATEGORIES.map((sc) => ({
        id: sc,
        label:
          sc === 'all'
            ? t('common.all')
            : t(`professional.columns.${sc}`),
      }));
    }
    return [];
  }, [category, t]);

  const monthOptions = useMemo(
    () =>
      language === 'es'
        ? ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        : ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    [language]
  );

  const primaryBarColor = CATEGORY_COLORS[category] || '#10b981';
  const progressPercent = Math.min(94, Math.max(15, elapsedSec * 3.2));

  return (
    <div className="dashboard-page">
      {/* Page Title & Live Sync Status Pill */}
      <div className="dashboard-header-row">
        <div className="page-header-title">
          <h1>
            {t('dashboard.welcome')}, {user?.email?.split('@')[0] || 'Datalaria'}! 👋
          </h1>
          <p>{t('dashboard.subtitle')}</p>
        </div>

        <div className={`sync-status-pill ${isSyncing ? 'syncing' : 'synced'}`}>
          {isSyncing ? (
            <>
              <RefreshCw size={14} className="spin-icon" />
              <span>
                {t('dashboard.analytics.syncingBadge')} ({elapsedSec}s)
              </span>
            </>
          ) : (
            <>
              <CheckCircle2 size={14} />
              <span>{t('dashboard.analytics.syncedBadge')}</span>
            </>
          )}
        </div>
      </div>

      {/* ── Foreground Cloud Sync / Cold-Start Banner (shown when waiting for initial data) ── */}
      {showInitialBlockingLoader && (
        <div className="cloud-sync-banner glass-panel" role="status" aria-live="polite">
          <div className="cloud-sync-banner-top">
            <div className="cloud-sync-title-row">
              <div className="cloud-sync-spinner-box">
                <RefreshCw size={20} className="spin-icon" />
              </div>
              <div className="cloud-sync-title-text">
                <h3>{t('dashboard.analytics.syncBannerTitle')}</h3>
                <p>
                  {elapsedSec >= 4
                    ? t('dashboard.analytics.syncBannerColdDesc')
                    : t('dashboard.analytics.syncBannerFastDesc')}
                </p>
              </div>
            </div>
            <span className="cloud-sync-timer-badge">{elapsedSec}s</span>
          </div>

          <div className="cloud-sync-progress-track">
            <div className="cloud-sync-progress-bar" style={{ width: `${progressPercent}%` }} />
          </div>

          <div className="cloud-sync-steps">
            <span className="cloud-sync-step done">
              ✓ {t('dashboard.analytics.syncStepAuth')}
            </span>
            <span className="cloud-sync-step active">
              ⟳ {t('dashboard.analytics.syncStepEngine')} ({elapsedSec}s)
            </span>
            <span className="cloud-sync-step">
              ⏳ {t('dashboard.analytics.syncStepData')}
            </span>
          </div>
        </div>
      )}

      {/* ── Control Bar: Time Window, Comparison & Category/Subcategory Drill-down ── */}
      <div className="analytics-control-bar glass-panel">
        <div className="control-bar-top">
          <div className="period-pills-group">
            {[
              { id: 'week', label: t('dashboard.analytics.periodWeek') },
              { id: 'month', label: t('dashboard.analytics.periodMonth') },
              { id: 'calendar_month', label: t('dashboard.analytics.periodCalendarMonth') },
              { id: 'quarter', label: t('dashboard.analytics.periodQuarter') },
              { id: 'year', label: t('dashboard.analytics.periodYear') },
            ].map((p) => (
              <button
                key={p.id}
                type="button"
                className={`period-pill ${period === p.id ? 'active' : ''}`}
                onClick={() => setPeriod(p.id)}
              >
                <Calendar size={13} />
                {p.label}
              </button>
            ))}
          </div>

          {/* Year / Month Selectors when Calendar Month or Year mode is active */}
          {(period === 'calendar_month' || period === 'year') && (
            <div className="period-selects-inline">
              {period === 'calendar_month' && (
                <select
                  className="analytics-select"
                  value={selectedMonth}
                  onChange={(e) => setSelectedMonth(Number(e.target.value))}
                  aria-label="Month selector"
                >
                  {monthOptions.map((mName, idx) => (
                    <option key={mName} value={idx}>
                      {mName}
                    </option>
                  ))}
                </select>
              )}
              <select
                className="analytics-select"
                value={selectedYear}
                onChange={(e) => setSelectedYear(Number(e.target.value))}
                aria-label="Year selector"
              >
                {[now.getFullYear(), now.getFullYear() - 1, now.getFullYear() - 2].map((yr) => (
                  <option key={yr} value={yr}>
                    {yr}
                  </option>
                ))}
              </select>
            </div>
          )}

          <button
            type="button"
            className={`compare-toggle-btn ${comparePrev ? 'active' : ''}`}
            onClick={() => setComparePrev((prev) => !prev)}
          >
            ⇄ {t('dashboard.analytics.compareToggle')}
          </button>
        </div>

        {/* Category Tabs */}
        <div className="control-bar-categories">
          <div className="category-tabs">
            {[
              { id: 'all', label: `🌐 ${t('dashboard.analytics.catAll')}` },
              { id: 'sport', label: `🏃 ${t('dashboard.analytics.catSport')}` },
              { id: 'book', label: `📚 ${t('dashboard.analytics.catBooks')}` },
              { id: 'film', label: `🎬 ${t('dashboard.analytics.catFilms')}` },
              { id: 'tasks', label: `📋 ${t('dashboard.analytics.catTasks')}` },
            ].map((cat) => (
              <button
                key={cat.id}
                type="button"
                className={`category-tab cat-${cat.id} ${category === cat.id ? 'active' : ''}`}
                onClick={() => handleCategoryChange(cat.id)}
              >
                {cat.label}
              </button>
            ))}
          </div>

          {(category !== 'all' || subcategory !== 'all') && (
            <button
              type="button"
              className="reset-filter-btn"
              onClick={() => {
                setCategory('all');
                setSubcategory('all');
                setMetric('count');
              }}
            >
              <RotateCcw size={13} />
              {t('dashboard.analytics.resetFilters')}
            </button>
          )}
        </div>

        {/* Subcategory Drill-down Pills */}
        {subcategoryOptions.length > 0 && (
          <div className="subcategory-pills-row">
            <span className="subcategory-label">
              {language === 'es' ? 'Subcategoría:' : 'Subcategory:'}
            </span>
            {subcategoryOptions.map((sub) => (
              <button
                key={sub.id}
                type="button"
                className={`subcategory-pill ${subcategory === sub.id ? 'active' : ''}`}
                onClick={() => setSubcategory(sub.id)}
              >
                {sub.label}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* ── Block 1: Dynamic KPI Cards with Period-over-Period Trend ── */}
      <div className="stats-grid">
        {kpiCards.map((card) => (
          <StatWidget
            key={card.id}
            title={card.title}
            value={card.value}
            subtitle={card.subtitle}
            icon={card.icon}
            color={card.color}
            trend={card.trend}
          />
        ))}
      </div>

      {/* ── Block 2 & 3: Time-Series Evolution + Subcategory Breakdown ── */}
      <div className="analytics-charts-grid">
        {/* Time-Series Multi-Metric Chart */}
        <div className="analytics-chart-card glass-panel">
          <div className="chart-card-header">
            <div className="chart-card-title-group">
              <h3>
                <BarChart3 size={18} color={primaryBarColor} />
                {t('dashboard.analytics.timeSeriesTitle')}
              </h3>
              <p className="chart-period-caption">
                {toIsoDateString(windowInfo.currStart)} → {toIsoDateString(windowInfo.currEnd)}
                {comparePrev &&
                  ` · vs. ${toIsoDateString(windowInfo.prevStart)} → ${toIsoDateString(windowInfo.prevEnd)}`}
              </p>
            </div>

            {availableMetrics.length > 1 && (
              <div className="metric-selector-pills">
                {availableMetrics.map((m) => (
                  <button
                    key={m.id}
                    type="button"
                    className={`metric-pill ${activeMetric === m.id ? 'active' : ''}`}
                    onClick={() => setMetric(m.id)}
                  >
                    {m.label}
                  </button>
                ))}
              </div>
            )}
          </div>

          <div style={{ width: '100%', height: 255 }}>
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={timeSeriesData} margin={{ top: 10, right: 12, left: -18, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="label" stroke="#6b7280" fontSize={11} tickLine={false} />
                <YAxis stroke="#6b7280" fontSize={11} tickLine={false} allowDecimals={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(15, 23, 42, 0.96)',
                    borderColor: 'rgba(255, 255, 255, 0.12)',
                    borderRadius: '10px',
                    color: '#fff',
                    fontSize: '0.82rem',
                  }}
                  formatter={(value, name) => [
                    `${value}${activeMetricUnit ? ` ${activeMetricUnit}` : ''}`,
                    name === 'current'
                      ? t('dashboard.analytics.currentPeriod')
                      : t('dashboard.analytics.previousPeriod'),
                  ]}
                />
                <Bar
                  dataKey="current"
                  fill={primaryBarColor}
                  radius={[6, 6, 0, 0]}
                  maxBarSize={38}
                />
                {comparePrev && (
                  <Line
                    type="monotone"
                    dataKey="previous"
                    stroke="#94a3b8"
                    strokeWidth={2}
                    strokeDasharray="4 4"
                    dot={{ r: 3, fill: '#94a3b8' }}
                  />
                )}
              </ComposedChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-legend-inline">
            <span>
              <span className="legend-dot" style={{ backgroundColor: primaryBarColor }} />
              {t('dashboard.analytics.currentPeriod')}
            </span>
            {comparePrev && (
              <span>
                <span className="legend-line" />
                {t('dashboard.analytics.previousPeriod')}
              </span>
            )}
          </div>
        </div>

        {/* Subcategory Breakdown Donut + Progress List */}
        <div className="analytics-chart-card glass-panel">
          <div className="chart-card-header">
            <div className="chart-card-title-group">
              <h3>
                <PieChartIcon size={18} color="var(--accent-cyan)" />
                {t('dashboard.analytics.breakdownTitle')}
              </h3>
              <p className="chart-period-caption">{t('dashboard.analytics.breakdownHint')}</p>
            </div>
          </div>

          {subcategoryData.length === 0 ? (
            <div style={{ padding: '2.5rem 1rem', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
              {showInitialBlockingLoader
                ? t('dashboard.analytics.syncingBadge')
                : t('dashboard.analytics.noDataPeriod')}
            </div>
          ) : (
            <div className="subcategory-breakdown-body">
              <div style={{ width: '100%', height: 145 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={subcategoryData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      innerRadius={40}
                      outerRadius={64}
                      paddingAngle={3}
                    >
                      {subcategoryData.map((entry) => (
                        <Cell key={entry.key} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(15, 23, 42, 0.96)',
                        borderColor: 'rgba(255, 255, 255, 0.12)',
                        borderRadius: '10px',
                        color: '#fff',
                        fontSize: '0.8rem',
                      }}
                      formatter={(val, name, props) => [
                        `${val}${activeMetricUnit ? ` ${activeMetricUnit}` : ''} (${props.payload.sharePct}%)`,
                        name,
                      ]}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="subcategory-list">
                {subcategoryData.map((item) => (
                  <div
                    key={item.key}
                    className="subcategory-row"
                    onClick={() => {
                      if (category === 'all' && ['sport', 'book', 'film', 'tasks'].includes(item.key)) {
                        handleCategoryChange(item.key);
                      } else if (category !== 'all' && subcategory === 'all') {
                        setSubcategory(item.key);
                      }
                    }}
                    role="button"
                    tabIndex={0}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        if (category === 'all' && ['sport', 'book', 'film', 'tasks'].includes(item.key)) {
                          handleCategoryChange(item.key);
                        } else if (category !== 'all' && subcategory === 'all') {
                          setSubcategory(item.key);
                        }
                      }
                    }}
                  >
                    <div className="subcategory-row-top">
                      <span className="subcategory-name">
                        <span className="legend-dot" style={{ backgroundColor: item.color }} />
                        {item.name}
                      </span>
                      <span className="subcategory-stats">
                        {item.value}
                        {activeMetricUnit ? ` ${activeMetricUnit}` : ''} ({item.sharePct}%)
                      </span>
                    </div>
                    <div className="subcategory-bar-track">
                      <div
                        className="subcategory-bar-fill"
                        style={{ width: `${Math.max(4, item.sharePct)}%`, backgroundColor: item.color }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ── Block 4: Daily Consistency Heatmap (Strava / GitHub Style) ── */}
      <div className="consistency-heatmap-panel glass-panel">
        <div className="heatmap-header">
          <div className="chart-card-title-group">
            <h3>
              <Flame size={18} color="var(--accent-emerald)" />
              {t('dashboard.analytics.heatmapTitle')}
            </h3>
          </div>

          <div className="heatmap-badges">
            <span className="heatmap-stat-badge">
              📅 {t('dashboard.analytics.activeDays')}: <strong>{heatmapData.activeDays}</strong>
            </span>
            <span className="heatmap-stat-badge">
              🔥 {t('dashboard.analytics.currentStreak')}: <strong>{heatmapData.currentStreak}d</strong>
            </span>
            <span className="heatmap-stat-badge">
              🏆 {t('dashboard.analytics.bestStreak')}: <strong>{heatmapData.bestStreak}d</strong>
            </span>
          </div>
        </div>

        <div className="heatmap-scroll-wrapper">
          <div className="heatmap-grid">
            <div className="heatmap-day-labels">
              <span>{language === 'es' ? 'Lun' : 'Mon'}</span>
              <span></span>
              <span>{language === 'es' ? 'Mié' : 'Wed'}</span>
              <span></span>
              <span>{language === 'es' ? 'Vie' : 'Fri'}</span>
              <span></span>
              <span>{language === 'es' ? 'Dom' : 'Sun'}</span>
            </div>

            {heatmapData.weeks.map((week) => (
              <div key={week.weekStartStr} className="heatmap-week-col">
                {week.days.map((cell) => {
                  const titleText =
                    cell.count > 0
                      ? `${cell.dateStr}: ${cell.value}${activeMetricUnit ? ` ${activeMetricUnit}` : ''} (${cell.titles.join(', ')})`
                      : `${cell.dateStr}: 0`;
                  return (
                    <div
                      key={cell.dateStr}
                      className={`heatmap-cell level-${cell.level} ${cell.isFuture ? 'future' : ''}`}
                      title={titleText}
                    />
                  );
                })}
              </div>
            ))}
          </div>
        </div>

        <div className="heatmap-footer">
          <span>
            {category === 'all'
              ? t('dashboard.analytics.catAll')
              : `${category.toUpperCase()} ${subcategory !== 'all' ? `→ ${subcategory}` : ''}`}
          </span>
          <div className="heatmap-scale">
            <span>{t('dashboard.analytics.less')}</span>
            <span className="heatmap-scale-box heatmap-cell level-0" />
            <span className="heatmap-scale-box heatmap-cell level-1" />
            <span className="heatmap-scale-box heatmap-cell level-2" />
            <span className="heatmap-scale-box heatmap-cell level-3" />
            <span className="heatmap-scale-box heatmap-cell level-4" />
            <span>{t('dashboard.analytics.more')}</span>
          </div>
        </div>
      </div>

      {/* ── Operational Controls: Quick Actions & Backend Health ── */}
      <div className="dashboard-sections-grid">
        <QuickActions
          onAction={(actionId) => {
            if (actionId === 'sport') navigate('/personal?tab=sport');
            else if (actionId === 'book') navigate('/personal?tab=books');
            else if (actionId === 'film') navigate('/personal?tab=films');
            else if (actionId === 'task') navigate('/professional?tab=kanban');
            else if (actionId === 'report') navigate('/reports');
          }}
        />
        <SystemHealth />
      </div>
    </div>
  );
}
