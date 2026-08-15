import { supabase } from './supabase';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
  createActivity: (data) => apiFetch('/api/v1/activities/', { method: 'POST', body: JSON.stringify(data) }),
  createSportActivity: (data) => apiFetch('/api/v1/activities/sport', { method: 'POST', body: JSON.stringify(data) }),
  createBookActivity: (data) => apiFetch('/api/v1/activities/book', { method: 'POST', body: JSON.stringify(data) }),
  createFilmActivity: (data) => apiFetch('/api/v1/activities/film', { method: 'POST', body: JSON.stringify(data) }),

  // Projects & Tasks (Professional Area)
  getProjects: () => apiFetch('/api/v1/projects/'),
  createProject: (data) => apiFetch('/api/v1/projects/', { method: 'POST', body: JSON.stringify(data) }),
  getTasks: (status) => apiFetch(`/api/v1/tasks/${status ? `?status=${status}` : ''}`),
  createTask: (data) => apiFetch('/api/v1/tasks/', { method: 'POST', body: JSON.stringify(data) }),
  updateTask: (id, data) => apiFetch(`/api/v1/tasks/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
};
