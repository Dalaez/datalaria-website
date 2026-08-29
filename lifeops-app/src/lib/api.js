import { supabase } from './supabase';

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://lifeops-api.onrender.com';

/**
 * Fetch wrapper that automatically injects the Supabase JWT access token
 * into the Authorization header for FastAPI endpoints.
 */
export async function apiFetch(endpoint, options = {}) {
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
