/**
 * LifeOps — 360° Analytics Engine (v1.1.0 — ADR-013)
 * ===================================================
 * Pure deterministic aggregation engine for multi-dimensional filtering:
 * - Time windows: week (7d), this_week, month (30d), calendar_month, quarter (90d), year
 * - Period-over-period delta calculation (INV-8)
 * - Category & Subcategory drill-down (sport -> running/cycling/gym, book, film, tasks)
 * - Multi-metric time-series buckets (sessions, km, kcal, hours, pages)
 * - Subcategory distribution (Donut/Bar) & Daily Consistency Heatmap (Strava/GitHub style)
 */

const DAY_MS = 24 * 60 * 60 * 1000;

export const CATEGORY_COLORS = {
  all: '#10b981',
  sport: '#10b981',
  book: '#06b6d4',
  film: '#8b5cf6',
  tasks: '#f59e0b',
};

export const SUBCATEGORY_PALETTE = [
  '#10b981', // emerald
  '#06b6d4', // cyan
  '#8b5cf6', // purple
  '#f59e0b', // amber
  '#ec4899', // pink
  '#3b82f6', // blue
  '#14b8a6', // teal
  '#f43f5e', // rose
];

/**
 * Parse YYYY-MM-DD safely in local calendar time (midnight)
 */
export function parseIsoDate(dateStr) {
  if (!dateStr) return null;
  const clean = String(dateStr).split('T')[0];
  const parts = clean.split('-').map(Number);
  if (parts.length !== 3 || parts.some(Number.isNaN)) return null;
  return new Date(parts[0], parts[1] - 1, parts[2], 0, 0, 0, 0);
}

export function toIsoDateString(dateObj) {
  const y = dateObj.getFullYear();
  const m = String(dateObj.getMonth() + 1).padStart(2, '0');
  const d = String(dateObj.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

export function addDays(dateObj, days) {
  const d = new Date(dateObj.getTime());
  d.setDate(d.getDate() + days);
  return d;
}

/**
 * INV-8: Safe deterministic percentage delta calculation.
 */
export function computeDelta(currentVal, prevVal, unit = '', language = 'es') {
  const curr = Number(currentVal) || 0;
  const prev = Number(prevVal) || 0;
  const vsLabel = language === 'es' ? 'vs. ant.' : 'vs. prev.';

  if (prev === 0 && curr === 0) {
    return {
      positive: true,
      deltaPct: 0,
      diff: 0,
      text: language === 'es' ? 'Estable (0% vs. ant.)' : 'Stable (0% vs. prev.)',
    };
  }

  const formatVal = (v) => {
    const abs = Math.abs(v);
    if (Number.isInteger(abs)) return abs.toString();
    return abs.toFixed(1);
  };

  if (prev === 0 && curr > 0) {
    const u = unit ? ` ${unit}` : '';
    return {
      positive: true,
      deltaPct: 100,
      diff: curr,
      text: `+100% (+${formatVal(curr)}${u} ${vsLabel})`,
    };
  }

  const diff = curr - prev;
  const pct = Math.round((diff / prev) * 100);
  const sign = diff >= 0 ? '+' : '-';
  const pctSign = pct >= 0 ? '+' : '';
  const u = unit ? ` ${unit}` : '';

  return {
    positive: diff >= 0,
    deltaPct: pct,
    diff,
    text: `${pctSign}${pct}% (${sign}${formatVal(diff)}${u} ${vsLabel})`,
  };
}

/**
 * Extract total workout duration in seconds with backwards compatibility
 */
export function getActivitySeconds(act) {
  if (!act) return 0;
  if (act.metadata && typeof act.metadata.duration_seconds === 'number') {
    return act.metadata.duration_seconds;
  }
  if (typeof act.duration_minutes === 'number') {
    return act.duration_minutes * 60;
  }
  return 0;
}

export function formatDurationCompact(totalSeconds) {
  const secs = Math.max(0, Math.round(Number(totalSeconds) || 0));
  if (secs === 0) return '0m';
  const h = Math.floor(secs / 3600);
  const m = Math.floor((secs % 3600) / 60);
  const s = secs % 60;
  if (h > 0) {
    return m > 0 ? `${h}h ${m}m` : `${h}h`;
  }
  if (m > 0) {
    return s > 0 ? `${m}m ${s}s` : `${m}m`;
  }
  return `${s}s`;
}

export function formatPaceMinKm(totalSeconds, distanceKm) {
  const km = Number(distanceKm) || 0;
  const secs = Number(totalSeconds) || 0;
  if (km <= 0 || secs <= 0) return '—';
  const paceSeconds = Math.round(secs / km);
  const mins = Math.floor(paceSeconds / 60);
  const remSecs = String(paceSeconds % 60).padStart(2, '0');
  return `${mins}:${remSecs} /km`;
}

/**
 * Resolve current and previous period date boundaries.
 * Supports:
 * - 'week': rolling last 7 days vs prior 7 days
 * - 'month': rolling last 30 days vs prior 30 days
 * - 'calendar_month': specific year + month (0..11) vs previous calendar month
 * - 'quarter': rolling last 90 days vs prior 90 days
 * - 'year': specific calendar year vs previous calendar year
 */
export function resolveTimeWindows({
  period = 'month',
  selectedYear = new Date().getFullYear(),
  selectedMonth = new Date().getMonth(),
  refDate = new Date(),
}) {
  const today = new Date(refDate.getFullYear(), refDate.getMonth(), refDate.getDate(), 0, 0, 0, 0);

  if (period === 'week') {
    const currEnd = today;
    const currStart = addDays(currEnd, -6);
    const prevEnd = addDays(currStart, -1);
    const prevStart = addDays(prevEnd, -6);
    return {
      currStart,
      currEnd,
      prevStart,
      prevEnd,
      granularity: 'day',
      daysCount: 7,
    };
  }

  if (period === 'month') {
    const currEnd = today;
    const currStart = addDays(currEnd, -29);
    const prevEnd = addDays(currStart, -1);
    const prevStart = addDays(prevEnd, -29);
    return {
      currStart,
      currEnd,
      prevStart,
      prevEnd,
      granularity: 'day',
      daysCount: 30,
    };
  }

  if (period === 'calendar_month') {
    const year = Number(selectedYear);
    const month = Number(selectedMonth);
    const currStart = new Date(year, month, 1, 0, 0, 0, 0);
    const currEnd = new Date(year, month + 1, 0, 0, 0, 0, 0);
    const prevStart = new Date(year, month - 1, 1, 0, 0, 0, 0);
    const prevEnd = new Date(year, month, 0, 0, 0, 0, 0);
    const daysCount = currEnd.getDate();
    return {
      currStart,
      currEnd,
      prevStart,
      prevEnd,
      granularity: 'day',
      daysCount,
    };
  }

  if (period === 'quarter') {
    const currEnd = today;
    const currStart = addDays(currEnd, -89);
    const prevEnd = addDays(currStart, -1);
    const prevStart = addDays(prevEnd, -89);
    return {
      currStart,
      currEnd,
      prevStart,
      prevEnd,
      granularity: 'week',
      daysCount: 90,
    };
  }

  // Default: 'year'
  const year = Number(selectedYear) || today.getFullYear();
  const currStart = new Date(year, 0, 1, 0, 0, 0, 0);
  const currEnd = new Date(year, 11, 31, 0, 0, 0, 0);
  const prevStart = new Date(year - 1, 0, 1, 0, 0, 0, 0);
  const prevEnd = new Date(year - 1, 11, 31, 0, 0, 0, 0);
  return {
    currStart,
    currEnd,
    prevStart,
    prevEnd,
    granularity: 'month',
    daysCount: 365,
  };
}

/**
 * Normalize an activity or task into a unified analytical record.
 */
export function normalizeRecords(activities = [], tasks = []) {
  const normalizedActivities = (activities || []).map((act) => {
    const dateObj = parseIsoDate(act.date || act.created_at);
    const type = act.activity_type || 'sport';
    const workout = act.workout || {};
    const book = act.book || {};
    const film = act.film || {};

    let subcategory = 'other';
    if (type === 'sport') subcategory = workout.workout_type || 'other';
    else if (type === 'book') subcategory = book.status || 'reading';
    else if (type === 'film') subcategory = film.media_type || 'movie';
    else subcategory = type;

    const seconds = getActivitySeconds(act);
    const distanceKm = type === 'sport' ? Number(workout.distance_km) || 0 : 0;
    const calories = type === 'sport' ? Number(workout.calories) || 0 : 0;
    const heartRate = type === 'sport' ? Number(workout.avg_heart_rate) || 0 : 0;
    const elevationM = type === 'sport' ? Number(workout.elevation_m) || 0 : 0;
    const personalBest = type === 'sport' ? Boolean(workout.personal_best) : false;

    const pagesRead = type === 'book' ? Number(book.pages_read) || 0 : 0;
    const pagesTotal = type === 'book' ? Number(book.pages_total) || 0 : 0;
    const bookGenre = type === 'book' ? book.genre || 'General' : null;
    const bookRating = type === 'book' ? Number(book.rating) || 0 : 0;

    const filmPlatform = type === 'film' ? film.platform || 'Otro' : null;
    const filmRating = type === 'film' ? Number(film.rating) || 0 : 0;
    const filmGenre = type === 'film' ? film.genre || 'General' : null;

    return {
      id: act.id,
      title: act.title,
      dateStr: dateObj ? toIsoDateString(dateObj) : '',
      dateObj,
      domain: 'personal',
      category: type, // 'sport' | 'book' | 'film' | 'learning' | 'journal'
      subcategory,
      seconds,
      durationHours: Number((seconds / 3600).toFixed(2)),
      distanceKm,
      calories,
      heartRate,
      elevationM,
      personalBest,
      pagesRead,
      pagesTotal,
      bookGenre,
      bookRating,
      filmPlatform,
      filmRating,
      filmGenre,
      raw: act,
    };
  });

  const normalizedTasks = (tasks || []).map((task) => {
    const rawDate = task.due_date || task.updated_at || task.created_at;
    const dateObj = parseIsoDate(rawDate) || new Date();
    return {
      id: task.id,
      title: task.title,
      dateStr: toIsoDateString(dateObj),
      dateObj,
      domain: 'professional',
      category: 'tasks',
      subcategory: task.status || 'todo',
      projectId: task.project_id || 'unassigned',
      projectName: task.project?.name || 'General',
      priority: task.priority || 'medium',
      seconds: (Number(task.estimated_hours) || 0) * 3600,
      durationHours: Number(task.estimated_hours) || 0,
      distanceKm: 0,
      calories: 0,
      heartRate: 0,
      elevationM: 0,
      personalBest: false,
      pagesRead: 0,
      pagesTotal: 0,
      raw: task,
    };
  });

  return [...normalizedActivities, ...normalizedTasks].filter((r) => r.dateObj !== null);
}

/**
 * Filter records by category, subcategory, and date window
 */
export function filterRecords(records, { category = 'all', subcategory = 'all', start, end }) {
  return records.filter((r) => {
    if (start && r.dateObj < start) return false;
    if (end && r.dateObj > end) return false;

    if (category !== 'all') {
      if (r.category !== category) return false;
    }

    if (subcategory !== 'all') {
      if (r.subcategory !== subcategory) return false;
    }

    return true;
  });
}

/**
 * Get the numeric value of a record for a given metric key
 */
export function getMetricValue(record, metric = 'count') {
  switch (metric) {
    case 'distance_km':
      return record.distanceKm || 0;
    case 'calories':
      return record.calories || 0;
    case 'duration_hours':
      return record.durationHours || 0;
    case 'pages_read':
      return record.pagesRead || 0;
    case 'elevation_m':
      return record.elevationM || 0;
    case 'count':
    default:
      return 1;
  }
}

/**
 * Compute aggregated totals for a slice of records
 */
export function aggregateSlice(records) {
  const totalCount = records.length;
  let sportCount = 0;
  let bookCount = 0;
  let filmCount = 0;
  let tasksCount = 0;
  let tasksDone = 0;
  let tasksInProgress = 0;

  let distanceKm = 0;
  let calories = 0;
  let totalSeconds = 0;
  let elevationM = 0;
  let pbCount = 0;
  let hrSum = 0;
  let hrCount = 0;

  let pagesRead = 0;
  let booksCompleted = 0;
  let bookRatingSum = 0;
  let bookRatingCount = 0;

  let moviesCount = 0;
  let seriesCount = 0;
  let filmRatingSum = 0;
  let filmRatingCount = 0;

  for (const r of records) {
    totalSeconds += r.seconds || 0;
    if (r.category === 'sport') {
      sportCount += 1;
      distanceKm += r.distanceKm || 0;
      calories += r.calories || 0;
      elevationM += r.elevationM || 0;
      if (r.personalBest) pbCount += 1;
      if (r.heartRate > 0) {
        hrSum += r.heartRate;
        hrCount += 1;
      }
    } else if (r.category === 'book') {
      bookCount += 1;
      pagesRead += r.pagesRead || 0;
      if (r.subcategory === 'completed') booksCompleted += 1;
      if (r.bookRating > 0) {
        bookRatingSum += r.bookRating;
        bookRatingCount += 1;
      }
    } else if (r.category === 'film') {
      filmCount += 1;
      if (r.subcategory === 'movie') moviesCount += 1;
      if (r.subcategory === 'series') seriesCount += 1;
      if (r.filmRating > 0) {
        filmRatingSum += r.filmRating;
        filmRatingCount += 1;
      }
    } else if (r.category === 'tasks') {
      tasksCount += 1;
      if (r.subcategory === 'done') tasksDone += 1;
      if (r.subcategory === 'in_progress' || r.subcategory === 'review') tasksInProgress += 1;
    }
  }

  return {
    totalCount,
    sportCount,
    bookCount,
    filmCount,
    tasksCount,
    tasksDone,
    tasksInProgress,
    distanceKm: Number(distanceKm.toFixed(2)),
    calories: Math.round(calories),
    totalSeconds,
    durationHours: Number((totalSeconds / 3600).toFixed(1)),
    elevationM: Math.round(elevationM),
    pbCount,
    avgHeartRate: hrCount > 0 ? Math.round(hrSum / hrCount) : 0,
    pagesRead,
    booksCompleted,
    avgBookRating: bookRatingCount > 0 ? Number((bookRatingSum / bookRatingCount).toFixed(1)) : 0,
    moviesCount,
    seriesCount,
    avgFilmRating: filmRatingCount > 0 ? Number((filmRatingSum / filmRatingCount).toFixed(1)) : 0,
  };
}

/**
 * Build aligned time-series buckets for Current Period vs Previous Period
 */
export function buildTimeSeries({
  currRecords,
  prevRecords,
  windowInfo,
  metric = 'count',
  language = 'es',
}) {
  const { currStart, currEnd, prevStart, granularity } = windowInfo;
  const monthNames = language === 'es'
    ? ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const dayNames = language === 'es'
    ? ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
    : ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  if (granularity === 'month') {
    const buckets = Array.from({ length: 12 }, (_, idx) => ({
      index: idx,
      label: monthNames[idx],
      current: 0,
      previous: 0,
      currCount: 0,
      prevCount: 0,
    }));

    for (const r of currRecords) {
      const m = r.dateObj.getMonth();
      buckets[m].current += getMetricValue(r, metric);
      buckets[m].currCount += 1;
    }
    for (const r of prevRecords) {
      const m = r.dateObj.getMonth();
      buckets[m].previous += getMetricValue(r, metric);
      buckets[m].prevCount += 1;
    }
    return buckets.map((b) => ({
      ...b,
      current: Number(b.current.toFixed(1)),
      previous: Number(b.previous.toFixed(1)),
    }));
  }

  if (granularity === 'week') {
    const totalWeeks = 13;
    const buckets = Array.from({ length: totalWeeks }, (_, idx) => {
      const wStart = addDays(currStart, idx * 7);
      const label = `${wStart.getDate()} ${monthNames[wStart.getMonth()]}`;
      return {
        index: idx,
        label,
        current: 0,
        previous: 0,
        currCount: 0,
        prevCount: 0,
      };
    });

    for (const r of currRecords) {
      const diffDays = Math.floor((r.dateObj - currStart) / DAY_MS);
      const idx = Math.min(totalWeeks - 1, Math.max(0, Math.floor(diffDays / 7)));
      buckets[idx].current += getMetricValue(r, metric);
      buckets[idx].currCount += 1;
    }
    for (const r of prevRecords) {
      const diffDays = Math.floor((r.dateObj - prevStart) / DAY_MS);
      const idx = Math.min(totalWeeks - 1, Math.max(0, Math.floor(diffDays / 7)));
      buckets[idx].previous += getMetricValue(r, metric);
      buckets[idx].prevCount += 1;
    }

    return buckets.map((b) => ({
      ...b,
      current: Number(b.current.toFixed(1)),
      previous: Number(b.previous.toFixed(1)),
    }));
  }

  // Daily granularity (7 days or 28-31 days)
  const totalDays = Math.max(1, Math.round((currEnd - currStart) / DAY_MS) + 1);
  const buckets = Array.from({ length: totalDays }, (_, idx) => {
    const d = addDays(currStart, idx);
    const label = totalDays <= 7
      ? `${dayNames[d.getDay()]} ${d.getDate()}`
      : `${d.getDate()} ${monthNames[d.getMonth()]}`;
    return {
      index: idx,
      dateStr: toIsoDateString(d),
      label,
      current: 0,
      previous: 0,
      currCount: 0,
      prevCount: 0,
    };
  });

  for (const r of currRecords) {
    const idx = Math.round((r.dateObj - currStart) / DAY_MS);
    if (idx >= 0 && idx < totalDays) {
      buckets[idx].current += getMetricValue(r, metric);
      buckets[idx].currCount += 1;
    }
  }

  for (const r of prevRecords) {
    const idx = Math.round((r.dateObj - prevStart) / DAY_MS);
    if (idx >= 0 && idx < totalDays) {
      buckets[idx].previous += getMetricValue(r, metric);
      buckets[idx].prevCount += 1;
    }
  }

  return buckets.map((b) => ({
    ...b,
    current: Number(b.current.toFixed(1)),
    previous: Number(b.previous.toFixed(1)),
  }));
}

/**
 * Build Subcategory Distribution (Donut / Horizontal Bar chart)
 */
export function buildSubcategoryBreakdown({
  currRecords,
  category = 'all',
  subcategory = 'all',
  metric = 'count',
  language = 'es',
  t,
}) {
  const groups = new Map();

  const labelForKey = (key) => {
    if (category === 'all') {
      const mapEs = { sport: 'Deporte', book: 'Libros', film: 'Cine / Series', tasks: 'Tareas Kanban', learning: 'Aprendizaje', journal: 'Journal' };
      const mapEn = { sport: 'Sport', book: 'Books', film: 'Cinema / TV', tasks: 'Kanban Tasks', learning: 'Learning', journal: 'Journal' };
      return (language === 'es' ? mapEs[key] : mapEn[key]) || key;
    }
    if (category === 'sport') {
      if (subcategory !== 'all') {
        return key; // Distance/duration tier label
      }
      const tr = t ? t(`sport.types.${key}`) : key;
      return tr && !tr.includes('sport.types.') ? tr.replace(/^[^\wÁÉÍÓÚáéíóúÑñ]+\s*/, '') : key;
    }
    if (category === 'book') {
      if (subcategory !== 'all') return key;
      const tr = t ? t(`books.statuses.${key}`) : key;
      return tr && !tr.includes('books.statuses.') ? tr.replace(/^[^\wÁÉÍÓÚáéíóúÑñ]+\s*/, '') : key;
    }
    if (category === 'film') {
      if (subcategory !== 'all') return key;
      const tr = t ? t(`films.types.${key}`) : key;
      return tr && !tr.includes('films.types.') ? tr.replace(/^[^\wÁÉÍÓÚáéíóúÑñ]+\s*/, '') : key;
    }
    if (category === 'tasks') {
      const mapEs = { todo: 'Por Hacer', in_progress: 'En Progreso', review: 'En Revisión', done: 'Completadas' };
      const mapEn = { todo: 'To Do', in_progress: 'In Progress', review: 'In Review', done: 'Completed' };
      return (language === 'es' ? mapEs[key] : mapEn[key]) || key;
    }
    return key;
  };

  for (const r of currRecords) {
    let key = r.subcategory;
    if (category === 'all') {
      key = r.category;
    } else if (category === 'sport' && subcategory !== 'all') {
      // Drill-down inside a specific sport (e.g. running): group by distance or duration tier
      const km = r.distanceKm || 0;
      if (km > 0) {
        if (km < 5) key = '< 5 km (Sprint)';
        else if (km <= 10) key = '5 - 10 km';
        else if (km <= 21.2) key = '10 - 21 km (Media)';
        else key = '> 21 km (Fondo)';
      } else {
        const mins = Math.round((r.seconds || 0) / 60);
        if (mins < 30) key = '< 30 min';
        else if (mins <= 60) key = '30 - 60 min';
        else key = '> 60 min';
      }
    } else if (category === 'book' && subcategory !== 'all') {
      key = r.bookGenre || 'General';
    } else if (category === 'film' && subcategory !== 'all') {
      key = r.filmPlatform || 'Otro';
    } else if (category === 'tasks' && subcategory !== 'all') {
      key = r.projectName || 'General';
    }

    const val = getMetricValue(r, metric);
    const prev = groups.get(key) || { key, value: 0, count: 0 };
    prev.value += val;
    prev.count += 1;
    groups.set(key, prev);
  }

  const entries = Array.from(groups.values()).sort((a, b) => b.value - a.value);
  const totalVal = entries.reduce((acc, item) => acc + item.value, 0);

  return entries.map((item, idx) => ({
    key: item.key,
    name: labelForKey(item.key),
    value: Number(item.value.toFixed(1)),
    count: item.count,
    sharePct: totalVal > 0 ? Math.round((item.value / totalVal) * 100) : 0,
    color: category === 'all' && CATEGORY_COLORS[item.key]
      ? CATEGORY_COLORS[item.key]
      : SUBCATEGORY_PALETTE[idx % SUBCATEGORY_PALETTE.length],
  }));
}

/**
 * Build a 16-week (112 days) Strava/GitHub style Consistency Heatmap
 * filtered by the active category and subcategory.
 */
export function buildConsistencyHeatmap({
  allRecords,
  category = 'all',
  subcategory = 'all',
  metric = 'count',
  refDate = new Date(),
  weeksCount = 16,
}) {
  const today = new Date(refDate.getFullYear(), refDate.getMonth(), refDate.getDate(), 0, 0, 0, 0);
  // Align end of heatmap to the end of the current week (Sunday)
  const dayOfWeekMon0 = (today.getDay() + 6) % 7; // Mon=0 .. Sun=6
  const endOfGrid = addDays(today, 6 - dayOfWeekMon0);
  const totalDays = weeksCount * 7;
  const startOfGrid = addDays(endOfGrid, -(totalDays - 1));

  // Filter records matching category/subcategory
  const matching = filterRecords(allRecords, { category, subcategory });
  const dayMap = new Map();

  for (const r of matching) {
    const k = r.dateStr;
    const prev = dayMap.get(k) || { count: 0, value: 0, titles: [] };
    prev.count += 1;
    prev.value += getMetricValue(r, metric);
    if (prev.titles.length < 3) prev.titles.push(r.title);
    dayMap.set(k, prev);
  }

  // Compute max value for intensity scaling (levels 0..4)
  let maxVal = 0;
  for (const v of dayMap.values()) {
    if (v.value > maxVal) maxVal = v.value;
  }

  const weeks = [];
  let activeDays = 0;
  let currentStreak = 0;
  let bestStreak = 0;
  let tempStreak = 0;

  for (let w = 0; w < weeksCount; w++) {
    const days = [];
    for (let d = 0; d < 7; d++) {
      const cellDate = addDays(startOfGrid, w * 7 + d);
      const iso = toIsoDateString(cellDate);
      const isFuture = cellDate > today;
      const entry = dayMap.get(iso);
      const val = entry ? Number(entry.value.toFixed(1)) : 0;
      const count = entry ? entry.count : 0;

      let level = 0;
      if (count > 0 && maxVal > 0) {
        const ratio = val / maxVal;
        if (ratio <= 0.25) level = 1;
        else if (ratio <= 0.5) level = 2;
        else if (ratio <= 0.75) level = 3;
        else level = 4;
      }

      if (!isFuture) {
        if (count > 0) {
          activeDays += 1;
          tempStreak += 1;
          if (tempStreak > bestStreak) bestStreak = tempStreak;
        } else {
          tempStreak = 0;
        }
      }

      days.push({
        dateStr: iso,
        dateObj: cellDate,
        dayOfWeek: d,
        count,
        value: val,
        level,
        isFuture,
        titles: entry ? entry.titles : [],
      });
    }
    weeks.push({
      weekIndex: w,
      weekStartStr: days[0].dateStr,
      days,
    });
  }

  // Calculate current active streak (counting backwards from today or yesterday)
  let cursor = today;
  const todayIso = toIsoDateString(today);
  const yesterdayIso = toIsoDateString(addDays(today, -1));
  if (!dayMap.has(todayIso) && dayMap.has(yesterdayIso)) {
    cursor = addDays(today, -1);
  }
  while (dayMap.has(toIsoDateString(cursor))) {
    currentStreak += 1;
    cursor = addDays(cursor, -1);
  }

  return {
    weeks,
    activeDays,
    totalDaysTracked: totalDays - (6 - dayOfWeekMon0),
    currentStreak,
    bestStreak,
  };
}
