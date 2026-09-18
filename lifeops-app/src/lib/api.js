import { supabase } from './supabase';

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://lifeops-api.onrender.com';

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
          due_date: '2026-09-20',
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
          due_date: '2026-09-25',
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
          due_date: '2026-09-15',
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
          due_date: '2026-09-14',
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
          due_date: '2026-09-10',
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
          due_date: '2026-09-08',
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
          due_date: '2026-09-05',
          estimated_hours: 10,
          comments: [],
          project: { name: 'Modelos MBA & Estrategia', color: '#8b5cf6' }
        }
      ];
    }
    if (endpoint.includes('activity_type=sport')) {
      return [
        {
          id: 'sport-1',
          title: 'Tirada Larga Dominical — Medio Maratón',
          date: '2026-09-10',
          duration_minutes: 108,
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
          title: 'Ruta de Montaña — Puertos de Ciclismo',
          date: '2026-09-08',
          duration_minutes: 165,
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
          title: 'Series 10x400m en Pista de Atletismo',
          date: '2026-09-06',
          duration_minutes: 52,
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
          title: 'Fuerza — Tren Superior & Core',
          date: '2026-09-04',
          duration_minutes: 60,
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
        }
      ];
    }
    if (endpoint.includes('activity_type=book')) {
      return [
        {
          id: 'book-1',
          title: 'Designing Data-Intensive Applications',
          date: '2026-09-01',
          book: {
            author: 'Martin Kleppmann',
            pages_total: 560,
            pages_read: 385,
            status: 'reading',
            genre: 'Ingeniería de Software',
            rating: 5,
            notes: 'Obra maestra sobre replicación, particionado y consenso en bases de datos.'
          }
        },
        {
          id: 'book-2',
          title: 'Clean Code: A Handbook of Agile Software',
          date: '2026-08-20',
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
          title: 'Building Microservices: Designing Fine-Grained Systems',
          date: '2026-09-05',
          book: {
            author: 'Sam Newman',
            pages_total: 610,
            pages_read: 0,
            status: 'wishlist',
            genre: 'Cloud Architecture',
            rating: 5,
            notes: 'Segunda edición recomendada para profundizar en integración y observabilidad.'
          }
        }
      ];
    }
    if (endpoint.includes('activity_type=film')) {
      return [
        {
          id: 'film-1',
          title: 'Oppenheimer',
          date: '2026-09-02',
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
          title: 'Severance — Temporada 2',
          date: '2026-09-07',
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
          title: 'Silicon Valley',
          date: '2026-08-28',
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
    return null;
  }

  return response.json();
}

/**
 * Convenience API methods
 */
export const api = {
  // System Health
  getHealth: () => fetch(`${API_BASE_URL}/health`).then((res) => res.json()),

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
  getActivitiesWithDetails: (type) => apiFetch(`/api/v1/activities/details${type ? `?activity_type=${type}` : ''}`),
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
