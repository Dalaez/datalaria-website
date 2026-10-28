import { supabase } from './supabase';

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://lifeops-api.onrender.com';
const SWR_CACHE_PREFIX = 'lifeops_swr_v2:';

if (typeof window !== 'undefined') {
  try {
    for (let i = localStorage.length - 1; i >= 0; i--) {
      const k = localStorage.key(i);
      if (k && k.startsWith('lifeops_swr_v1:')) {
        localStorage.removeItem(k);
      }
    }
  } catch {
    // Ignore storage access errors
  }
}

/**
 * INV-10: Stale-While-Revalidate local cache helpers strictly namespaced by user.id
 */
export function getCachedEndpoint(userId, endpoint) {
  if (!userId || typeof window === 'undefined') return null;
  try {
    const raw = localStorage.getItem(`${SWR_CACHE_PREFIX}${userId}:${endpoint}`);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    return parsed?.data ?? null;
  } catch {
    return null;
  }
}

export function setCachedEndpoint(userId, endpoint, data) {
  if (!userId || typeof window === 'undefined') return;
  try {
    const now = Date.now();
    localStorage.setItem(
      `${SWR_CACHE_PREFIX}${userId}:${endpoint}`,
      JSON.stringify({ ts: now, data })
    );
    // Cross-populate module-specific activity caches when full details are fetched
    if (endpoint.startsWith('/api/v1/activities/details') && !endpoint.includes('activity_type=') && Array.isArray(data)) {
      for (const t of ['sport', 'book', 'film']) {
        localStorage.setItem(
          `${SWR_CACHE_PREFIX}${userId}:/api/v1/activities/details?activity_type=${t}`,
          JSON.stringify({ ts: now, data: data.filter((a) => a.activity_type === t) })
        );
      }
    }
  } catch {
    // Ignore storage quota errors safely
  }
}

export function clearUserCache(userId) {
  if (typeof window === 'undefined') return;
  try {
    const prefix = userId ? `${SWR_CACHE_PREFIX}${userId}:` : SWR_CACHE_PREFIX;
    const keysToDelete = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k && k.startsWith(prefix)) keysToDelete.push(k);
    }
    keysToDelete.forEach((k) => localStorage.removeItem(k));
  } catch {
    // Ignore storage errors
  }
}

export function wakeUpServer() {
  if (typeof window === 'undefined') return;
  const isMock =
    window.location.hash.includes('mock=true') ||
    window.location.search.includes('mock=true') ||
    localStorage.getItem('lifeops_mock') === 'true';
  if (isMock) return;
  fetch(`${API_BASE_URL}/health`, { method: 'GET', mode: 'cors' }).catch(() => null);
}

function relDate(daysAgo) {
  const d = new Date();
  d.setDate(d.getDate() - daysAgo);
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

function getMockSportActivities() {
  return [
    {
      id: 'sport-1',
      activity_type: 'sport',
      title: 'Tirada Larga Dominical — Medio Maratón',
      date: relDate(1),
      duration_minutes: 108,
      metadata: { duration_seconds: 6495 },
      description: 'Ritmo constante preparando el maratón de otoño. Buenas sensaciones en el último tramo.',
      workout: {
        workout_type: 'running',
        distance_km: 21.1,
        calories: 1420,
        avg_heart_rate: 152,
        elevation_m: 145,
        personal_best: true,
        notes: 'PB de media maratón rebajado en 3 minutos.'
      }
    },
    {
      id: 'sport-2',
      activity_type: 'sport',
      title: 'Ruta de Montaña — Puertos de Ciclismo',
      date: relDate(3),
      duration_minutes: 165,
      metadata: { duration_seconds: 9920 },
      description: 'Entrenamiento de fondo en carretera con dos puertos de montaña.',
      workout: {
        workout_type: 'cycling',
        distance_km: 65.0,
        calories: 1890,
        avg_heart_rate: 142,
        elevation_m: 950,
        personal_best: false,
        notes: 'Excelente cadencia y gestión de hidratación.'
      }
    },
    {
      id: 'sport-3',
      activity_type: 'sport',
      title: 'Series 10x400m en Pista de Atletismo',
      date: relDate(5),
      duration_minutes: 52,
      metadata: { duration_seconds: 3145 },
      description: 'Velocidad y potencia aeróbica con descansos activos de 60 segundos.',
      workout: {
        workout_type: 'running',
        distance_km: 10.0,
        calories: 720,
        avg_heart_rate: 168,
        elevation_m: 15,
        personal_best: true,
        notes: 'Series consistentes entre 1:20 y 1:22.'
      }
    },
    {
      id: 'sport-4',
      activity_type: 'sport',
      title: 'Fuerza — Tren Superior & Core',
      date: relDate(6),
      duration_minutes: 60,
      metadata: { duration_seconds: 3600 },
      description: 'Press banca, dominadas con lastre y trabajo de estabilización central.',
      workout: {
        workout_type: 'gym',
        distance_km: null,
        calories: 450,
        avg_heart_rate: 125,
        elevation_m: null,
        personal_best: false,
        notes: 'Sobrecarga progresiva en dominadas.'
      }
    },
    {
      id: 'sport-5',
      activity_type: 'sport',
      title: 'Rodaje Regenerativo 8K Zona 2',
      date: relDate(9),
      duration_minutes: 42,
      metadata: { duration_seconds: 2520 },
      description: 'Carrera aeróbica suave manteniendo pulsaciones bajas.',
      workout: {
        workout_type: 'running',
        distance_km: 8.2,
        calories: 540,
        avg_heart_rate: 138,
        elevation_m: 45,
        personal_best: false,
        notes: 'Zancada fluida.'
      }
    },
    {
      id: 'sport-6',
      activity_type: 'sport',
      title: 'Salida Grupal Ciclismo de Carretera',
      date: relDate(12),
      duration_minutes: 130,
      metadata: { duration_seconds: 7800 },
      description: 'Relevos en llano y subida tendida.',
      workout: {
        workout_type: 'cycling',
        distance_km: 52.4,
        calories: 1410,
        avg_heart_rate: 139,
        elevation_m: 580,
        personal_best: false,
        notes: 'Viento lateral en el regreso.'
      }
    },
    {
      id: 'sport-7',
      activity_type: 'sport',
      title: 'Tempo Run 12K — Ritmo Umbral',
      date: relDate(18),
      duration_minutes: 56,
      metadata: { duration_seconds: 3360 },
      description: 'Bloque central de 8 km a ritmo de competición.',
      workout: {
        workout_type: 'running',
        distance_km: 12.0,
        calories: 830,
        avg_heart_rate: 161,
        elevation_m: 60,
        personal_best: false,
        notes: 'Control de lactato óptimo.'
      }
    },
    {
      id: 'sport-8',
      activity_type: 'sport',
      title: 'Sesión HIIT & Fuerza Funcional',
      date: relDate(24),
      duration_minutes: 50,
      metadata: { duration_seconds: 3000 },
      description: 'Trabajo metabólico y tren inferior.',
      workout: {
        workout_type: 'gym',
        distance_km: null,
        calories: 510,
        avg_heart_rate: 144,
        elevation_m: null,
        personal_best: false,
        notes: 'Sentadilla búlgara y kettlebells.'
      }
    },
    {
      id: 'sport-9',
      activity_type: 'sport',
      title: 'Carrera 15K Progresiva',
      date: relDate(36),
      duration_minutes: 74,
      metadata: { duration_seconds: 4440 },
      description: 'De menos a más por ribera del río.',
      workout: {
        workout_type: 'running',
        distance_km: 15.0,
        calories: 990,
        avg_heart_rate: 154,
        elevation_m: 85,
        personal_best: false,
        notes: 'Últimos 3 km a 4:35/km.'
      }
    },
    {
      id: 'sport-10',
      activity_type: 'sport',
      title: 'Fondo Ciclismo 45K',
      date: relDate(44),
      duration_minutes: 110,
      metadata: { duration_seconds: 6600 },
      description: 'Rodaje aeróbico de fin de semana.',
      workout: {
        workout_type: 'cycling',
        distance_km: 45.0,
        calories: 1180,
        avg_heart_rate: 136,
        elevation_m: 410,
        personal_best: false,
        notes: 'Cadencia media 90 rpm.'
      }
    }
  ];
}

function getMockBookActivities() {
  return [
    {
      id: 'book-1',
      activity_type: 'book',
      title: 'Designing Data-Intensive Applications',
      date: relDate(2),
      book: {
        author: 'Martin Kleppmann',
        pages_total: 560,
        pages_read: 420,
        status: 'reading',
        genre: 'Ingeniería de Software',
        rating: 5,
        notes: 'Obra maestra sobre replicación, particionado y consenso en bases de datos.'
      }
    },
    {
      id: 'book-2',
      activity_type: 'book',
      title: 'Clean Code: A Handbook of Agile Software',
      date: relDate(14),
      book: {
        author: 'Robert C. Martin',
        pages_total: 464,
        pages_read: 464,
        status: 'completed',
        genre: 'Arquitectura & Buenas Prácticas',
        rating: 5,
        notes: 'Lectura fundamental sobre nombres significativos y funciones pequeñas.'
      }
    },
    {
      id: 'book-3',
      activity_type: 'book',
      title: 'The Goal: A Process of Ongoing Improvement',
      date: relDate(27),
      book: {
        author: 'Eliyahu M. Goldratt',
        pages_total: 384,
        pages_read: 384,
        status: 'completed',
        genre: 'Operaciones & Management',
        rating: 5,
        notes: 'Teoría de las restricciones (TOC) aplicada a cuellos de botella.'
      }
    },
    {
      id: 'book-4',
      activity_type: 'book',
      title: 'Building Microservices: Designing Fine-Grained Systems',
      date: relDate(40),
      book: {
        author: 'Sam Newman',
        pages_total: 610,
        pages_read: 210,
        status: 'wishlist',
        genre: 'Cloud Architecture',
        rating: 4,
        notes: 'Segunda edición recomendada para profundizar en integración y observabilidad.'
      }
    }
  ];
}

function getMockFilmActivities() {
  return [
    {
      id: 'film-1',
      activity_type: 'film',
      title: 'Oppenheimer',
      date: relDate(4),
      film: {
        director: 'Christopher Nolan',
        platform: 'Cine',
        year: 2023,
        rating: 5,
        media_type: 'movie',
        genre: 'Biopic / Drama',
        notes: 'Ritmo trepidante, diseño de sonido demoledor e interpretaciones memorables.'
      }
    },
    {
      id: 'film-2',
      activity_type: 'film',
      title: 'Severance — Temporada 2',
      date: relDate(11),
      film: {
        director: 'Ben Stiller',
        platform: 'Apple TV+',
        year: 2025,
        rating: 5,
        media_type: 'series',
        genre: 'Sci-Fi / Thriller',
        notes: 'Continuación magistral del dilema de separación entre vida laboral y personal.'
      }
    },
    {
      id: 'film-3',
      activity_type: 'film',
      title: 'Dune: Part Two',
      date: relDate(21),
      film: {
        director: 'Denis Villeneuve',
        platform: 'HBO Max',
        year: 2024,
        rating: 5,
        media_type: 'movie',
        genre: 'Sci-Fi',
        notes: 'Fotografía colosal y banda sonora inolvidable.'
      }
    },
    {
      id: 'film-4',
      activity_type: 'film',
      title: 'Silicon Valley',
      date: relDate(38),
      film: {
        director: 'Mike Judge',
        platform: 'HBO Max',
        year: 2019,
        rating: 4,
        media_type: 'series',
        genre: 'Comedia Tech',
        notes: 'Sátira brillante sobre el ecosistema startup y capital riesgo.'
      }
    }
  ];
}

/**
 * Fetch wrapper that automatically injects the Supabase JWT access token
 * into the Authorization header for FastAPI endpoints.
 */
export async function apiFetch(endpoint, options = {}) {
  const isMock = typeof window !== 'undefined' && (
    window.location.hash.includes('mock=true') ||
    window.location.search.includes('mock=true') ||
    localStorage.getItem('lifeops_mock') === 'true'
  );

  if (isMock) {
    if (endpoint.includes('/api/v1/stats/dashboard')) {
      const allActs = [...getMockSportActivities(), ...getMockBookActivities(), ...getMockFilmActivities()];
      return {
        total_activities: allActs.length,
        activities_this_week: 5,
        activities_this_month: 14,
        sport_count: getMockSportActivities().length,
        books_count: getMockBookActivities().length,
        films_count: getMockFilmActivities().length,
        learning_count: 0,
        total_projects: 3,
        active_projects: 3,
        total_tasks: 7,
        tasks_todo: 2,
        tasks_in_progress: 2,
        tasks_done: 3,
        tasks_overdue: 0,
        active_habits: 3,
      };
    }
    if (endpoint.includes('/api/v1/stats/breakdown')) {
      return {
        period_start: relDate(30),
        period_end: relDate(0),
        sport: 8,
        book: 3,
        film: 3,
        learning: 0,
        journal: 0,
        total: 14,
      };
    }
    if (endpoint.includes('/api/v1/projects')) {
      return [
        { id: 'proj-1', name: 'LifeOps Cloud & API', color: '#10b981', status: 'active' },
        { id: 'proj-2', name: 'Datalaria Website', color: '#06b6d4', status: 'active' },
        { id: 'proj-3', name: 'Modelos MBA & Estrategia', color: '#8b5cf6', status: 'active' },
      ];
    }
    if (endpoint.includes('/api/v1/tasks')) {
      return [
        {
          id: 'task-1',
          title: 'Refactor endpoints con Pydantic v2',
          description: 'Actualizar schemas de FastAPI y validar contratos OpenAPI.',
          project_id: 'proj-1',
          priority: 'high',
          status: 'todo',
          due_date: relDate(-5),
          estimated_hours: 4,
          comments: [],
          project: { name: 'LifeOps Cloud & API', color: '#10b981' }
        },
        {
          id: 'task-2',
          title: 'Matriz RACI y Balance de Carga',
          description: 'Definir responsabilidades del sprint de lanzamiento.',
          project_id: 'proj-3',
          priority: 'medium',
          status: 'todo',
          due_date: relDate(-9),
          estimated_hours: 2.5,
          comments: [],
          project: { name: 'Modelos MBA & Estrategia', color: '#8b5cf6' }
        },
        {
          id: 'task-3',
          title: 'Implementación Tablero Kanban y Bitácora JSONB',
          description: 'Gestión ágil de tareas con bitácora cronológica persistida en columna JSONB.',
          project_id: 'proj-1',
          priority: 'critical',
          status: 'in_progress',
          due_date: relDate(1),
          estimated_hours: 8,
          comments: [
            { id: 'c1', text: 'Esquema PostgreSQL completado con columna comments JSONB default []', created_at: '2026-09-12T14:30:00Z' },
            { id: 'c2', text: 'Actualizaciones optimistas en React funcionando sin latencia visual', created_at: '2026-09-13T09:15:00Z' },
            { id: 'c3', text: 'Pruebas de persistencia atómica y validación de contrato OpenAPI superadas', created_at: '2026-09-13T11:45:00Z' }
          ],
          project: { name: 'LifeOps Cloud & API', color: '#10b981' }
        },
        {
          id: 'task-4',
          title: 'Tests E2E & Validación Render Cold-Starts',
          description: 'Simular contenedor dormido y comprobar reintentos con backoff.',
          project_id: 'proj-1',
          priority: 'medium',
          status: 'review',
          due_date: relDate(2),
          estimated_hours: 3,
          comments: [
            { id: 'c4', text: 'Prueba de 35s de timeout con spinner de activación superada con éxito.', created_at: '2026-09-12T18:00:00Z' }
          ],
          project: { name: 'LifeOps Cloud & API', color: '#10b981' }
        },
        {
          id: 'task-5',
          title: 'Diseño Glassmorphism y Tokens CSS',
          description: 'Variables CSS en :root con efectos de desenfoque por hardware.',
          project_id: 'proj-1',
          priority: 'high',
          status: 'done',
          due_date: relDate(4),
          estimated_hours: 6,
          comments: [],
          project: { name: 'LifeOps Cloud & API', color: '#10b981' }
        },
        {
          id: 'task-6',
          title: 'Setup Supabase Auth & Row Level Security',
          description: 'Aislamiento multi-tenant por user_id en esquema lifeops.',
          project_id: 'proj-1',
          priority: 'critical',
          status: 'done',
          due_date: relDate(8),
          estimated_hours: 5,
          comments: [],
          project: { name: 'LifeOps Cloud & API', color: '#10b981' }
        },
        {
          id: 'task-7',
          title: 'Suite Estratégica: DAFO Cuantitativo',
          description: 'Modelo matricial con ponderaciones de factores y análisis CAME.',
          project_id: 'proj-3',
          priority: 'medium',
          status: 'done',
          due_date: relDate(16),
          estimated_hours: 10,
          comments: [],
          project: { name: 'Modelos MBA & Estrategia', color: '#8b5cf6' }
        }
      ];
    }
    if (endpoint.includes('activity_type=sport')) {
      return getMockSportActivities();
    }
    if (endpoint.includes('activity_type=book')) {
      return getMockBookActivities();
    }
    if (endpoint.includes('activity_type=film')) {
      return getMockFilmActivities();
    }
    if (endpoint.includes('/api/v1/activities/details') || endpoint.includes('/api/v1/activities/')) {
      return [
        ...getMockSportActivities(),
        ...getMockBookActivities(),
        ...getMockFilmActivities(),
      ];
    }
    if (endpoint.includes('/api/v1/reports/history')) {
      const isEn = typeof window !== 'undefined' && (
        window.location.hash.includes('lang=en') || 
        window.location.search.includes('lang=en') || 
        localStorage.getItem('lifeops_language') === 'en'
      );
      return [
        {
          id: 'rep-1',
          report_name: isEn ? 'LifeOps_Comprehensive_Monthly_Report_2026-09.docx' : 'LifeOps_Informe_Mensual_Integral_2026-09.docx',
          period_start: '2026-09-01',
          period_end: '2026-09-15',
          generated_at: '2026-09-15T10:30:00Z',
          metadata: { activities_count: 24, tasks_count: 14 }
        },
        {
          id: 'rep-2',
          report_name: isEn ? 'LifeOps_Fitness_Performance_Dossier_2026-08.docx' : 'LifeOps_Dossier_Deportivo_2026-08.docx',
          period_start: '2026-08-01',
          period_end: '2026-08-31',
          generated_at: '2026-09-01T08:15:00Z',
          metadata: { activities_count: 18, tasks_count: 0 }
        },
        {
          id: 'rep-3',
          report_name: isEn ? 'LifeOps_Project_Portfolio_Status_Q3.docx' : 'LifeOps_Estado_Proyectos_Q3.docx',
          period_start: '2026-07-01',
          period_end: '2026-09-10',
          generated_at: '2026-09-10T16:45:00Z',
          metadata: { activities_count: 0, tasks_count: 32 }
        }
      ];
    }
  }

  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;
  const userId = session?.user?.id;
  const method = (options.method || 'GET').toUpperCase();

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {}),
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(errorData.detail || `HTTP Error ${response.status}`);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    if (userId && method !== 'GET') clearUserCache(userId);
    return null;
  }

  const jsonData = await response.json();

  if (userId) {
    if (method === 'GET') {
      setCachedEndpoint(userId, endpoint, jsonData);
    } else {
      clearUserCache(userId);
    }
  }

  return jsonData;
}

/**
 * Convenience API methods
 */
export const api = {
  // System Health & SWR Cache
  getHealth: () => fetch(`${API_BASE_URL}/health`).then((res) => res.json()),
  wakeUpServer,
  clearUserCache,
  getCachedDashboardBundle: (userId) => {
    if (!userId) return null;
    const summary = getCachedEndpoint(userId, '/api/v1/stats/dashboard');
    const activities = getCachedEndpoint(userId, '/api/v1/activities/details?limit=200');
    const tasks = getCachedEndpoint(userId, '/api/v1/tasks/');
    if (!summary && !activities && !tasks) return null;
    return { summary, activities, tasks };
  },

  // Dashboard Stats
  getDashboardSummary: () => apiFetch('/api/v1/stats/dashboard'),
  getActivityBreakdown: (from, to) => {
    const params = new URLSearchParams();
    if (from) params.append('date_from', from);
    if (to) params.append('date_to', to);
    const queryString = params.toString() ? `?${params.toString()}` : '';
    return apiFetch(`/api/v1/stats/breakdown${queryString}`);
  },

  // Activities (Personal Area)
  getActivities: (type) => apiFetch(`/api/v1/activities/${type ? `?activity_type=${type}` : ''}`),
  getActivitiesWithDetails: (type, options = {}) => {
    const params = new URLSearchParams();
    if (type) params.append('activity_type', type);
    if (options.dateFrom) params.append('date_from', options.dateFrom);
    if (options.dateTo) params.append('date_to', options.dateTo);
    if (options.limit) params.append('limit', String(options.limit));
    const qs = params.toString() ? `?${params.toString()}` : '';
    return apiFetch(`/api/v1/activities/details${qs}`);
  },
  createActivity: (data) => apiFetch('/api/v1/activities/', { method: 'POST', body: JSON.stringify(data) }),
  createSportActivity: (data) => apiFetch('/api/v1/activities/sport', { method: 'POST', body: JSON.stringify(data) }),
  createBookActivity: (data) => apiFetch('/api/v1/activities/book', { method: 'POST', body: JSON.stringify(data) }),
  createFilmActivity: (data) => apiFetch('/api/v1/activities/film', { method: 'POST', body: JSON.stringify(data) }),
  updateActivity: (id, data) => apiFetch(`/api/v1/activities/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  updateSportActivity: (id, data) => apiFetch(`/api/v1/activities/${id}/sport`, { method: 'PATCH', body: JSON.stringify(data) }),
  updateBookActivity: (id, data) => apiFetch(`/api/v1/activities/${id}/book`, { method: 'PATCH', body: JSON.stringify(data) }),
  updateFilmActivity: (id, data) => apiFetch(`/api/v1/activities/${id}/film`, { method: 'PATCH', body: JSON.stringify(data) }),
  deleteActivity: (id) => apiFetch(`/api/v1/activities/${id}`, { method: 'DELETE' }),

  // Projects & Tasks (Professional Area)
  getProjects: (status) => apiFetch(`/api/v1/projects/${status ? `?status=${status}` : ''}`),
  createProject: (data) => apiFetch('/api/v1/projects/', { method: 'POST', body: JSON.stringify(data) }),
  updateProject: (id, data) => apiFetch(`/api/v1/projects/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  deleteProject: (id) => apiFetch(`/api/v1/projects/${id}`, { method: 'DELETE' }),
  
  getTasks: (status, projectId) => {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (projectId) params.append('project_id', projectId);
    const qs = params.toString() ? `?${params.toString()}` : '';
    return apiFetch(`/api/v1/tasks/${qs}`);
  },
  getProjectTasks: (projectId) => apiFetch(`/api/v1/projects/${projectId}/tasks`),
  createTask: (data) => apiFetch('/api/v1/tasks/', { method: 'POST', body: JSON.stringify(data) }),
  updateTask: (id, data) => apiFetch(`/api/v1/tasks/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  deleteTask: (id) => apiFetch(`/api/v1/tasks/${id}`, { method: 'DELETE' }),
  addTaskComment: (taskId, text) => apiFetch(`/api/v1/tasks/${taskId}/comments`, { method: 'POST', body: JSON.stringify({ text }) }),
  deleteTaskComment: (taskId, commentId) => apiFetch(`/api/v1/tasks/${taskId}/comments/${commentId}`, { method: 'DELETE' }),


  // Reports (Word .docx)
  getReportTemplates: () => apiFetch('/api/v1/reports/templates'),
  getReportHistory: () => apiFetch('/api/v1/reports/history'),
  downloadReport: async (templateType, dateFrom, dateTo) => {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;

    const response = await fetch(`${API_BASE_URL}/api/v1/reports/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({
        template_type: templateType,
        date_from: dateFrom || null,
        date_to: dateTo || null,
      }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: 'Error al generar informe' }));
      throw new Error(err.detail || 'Error al generar informe');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `LifeOps_${templateType}_${new Date().toISOString().split('T')[0]}.docx`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },

  // Smart Alerts & Notifications
  getAlerts: () => apiFetch('/api/v1/alerts/'),
  dismissAlert: (alertId) => apiFetch(`/api/v1/alerts/${alertId}/dismiss`, { method: 'POST' }),

  // Data Exports (CSV & Excel)
  exportCSV: async (entity) => {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;

    const response = await fetch(`${API_BASE_URL}/api/v1/reports/export/csv?entity=${entity}`, {
      headers: {
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });

    if (!response.ok) {
      throw new Error('Error al exportar archivo CSV');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `lifeops_${entity}_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },

  exportExcel: async () => {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;

    const response = await fetch(`${API_BASE_URL}/api/v1/reports/export/excel`, {
      headers: {
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });

    if (!response.ok) {
      throw new Error('Error al exportar libro Excel');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `LifeOps_Backup_Completo_${new Date().toISOString().split('T')[0]}.xlsx`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },
};
