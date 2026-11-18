/**
 * apps/pulse/web/src/lib/supabase.ts
 * ----------------------------------
 * Cliente de integración Supabase para Datalaria Pulse Pro (Cloud).
 * Cluster: datalaria-core (Constitución Art. 4).
 * Esquema: pulse
 */

import { createClient, type User, type SupabaseClient } from '@supabase/supabase-js';
import type { ContentAsset } from '../types';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://wkbmxekmofrjtcsyytrv.supabase.co';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndrYm14ZWttb2ZyanRjc3l5dHJ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkyNjQyOTgsImV4cCI6MjA4NDg0MDI5OH0.h-oWBsGc493dSCYLw6CVbWTFvsX1aGh90yZuVINB14Y';

export const isSupabaseConfigured = Boolean(supabaseUrl && supabaseAnonKey);

export const supabase: SupabaseClient = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
  },
  db: {
    schema: 'pulse',
  },
});

export interface CloudIdea {
  id: string;
  user_id: string;
  title: string;
  notes: string;
  category: string;
  tags: string[];
  status: 'idea' | 'draft' | 'review' | 'scheduled' | 'published';
  target_date: string | null;
  created_at: string;
  updated_at: string;
}

export async function getCurrentUser(): Promise<User | null> {
  if (!isSupabaseConfigured) return null;
  try {
    const { data: { user }, error } = await supabase.auth.getUser();
    if (error) return null;
    return user;
  } catch {
    return null;
  }
}

export async function signOut(): Promise<void> {
  await supabase.auth.signOut();
}

/**
 * Consulta de ideas del usuario en Supabase (pulse.ideas con RLS)
 */
export async function fetchUserIdeas(): Promise<CloudIdea[]> {
  const { data, error } = await supabase
    .from('ideas')
    .select('*')
    .order('created_at', { ascending: false });

  if (error) {
    console.warn('[Pulse Supabase] Error consultando ideas:', error.message);
    return [];
  }
  return data || [];
}

/**
 * Insertar nueva idea en pulse.ideas
 */
export async function insertUserIdea(idea: {
  title: string;
  notes?: string;
  category?: string;
  tags?: string[];
  status?: string;
  target_date?: string | null;
}): Promise<CloudIdea | null> {
  const user = await getCurrentUser();
  if (!user) return null;

  const payload = {
    user_id: user.id,
    title: idea.title,
    notes: idea.notes || '',
    category: idea.category || 'General',
    tags: idea.tags || [],
    status: idea.status || 'idea',
    target_date: idea.target_date || null,
  };

  const { data, error } = await supabase
    .from('ideas')
    .insert([payload])
    .select()
    .single();

  if (error) {
    console.error('[Pulse Supabase] Error insertando idea:', error.message);
    return null;
  }
  return data;
}

/**
 * Actualizar idea existente en pulse.ideas
 */
export async function updateUserIdea(id: string, updates: Partial<CloudIdea>): Promise<CloudIdea | null> {
  const { data, error } = await supabase
    .from('ideas')
    .update({
      ...updates,
      updated_at: new Date().toISOString(),
    })
    .eq('id', id)
    .select()
    .single();

  if (error) {
    console.error('[Pulse Supabase] Error actualizando idea:', error.message);
    return null;
  }
  return data;
}

/**
 * Eliminar idea de pulse.ideas
 */
export async function deleteUserIdea(id: string): Promise<boolean> {
  const { error } = await supabase
    .from('ideas')
    .delete()
    .eq('id', id);

  if (error) {
    console.error('[Pulse Supabase] Error eliminando idea:', error.message);
    return false;
  }
  return true;
}

/**
 * Descarga el snapshot maestro privado de Datalaria (borradores y proyectos embargados)
 * protegido por RLS exclusivo por email en pulse.private_snapshot.
 */
export async function fetchAdminCatalogSnapshot(): Promise<{
  assets: ContentAsset[];
  updatedAt?: string;
} | null> {
  if (!isSupabaseConfigured) return null;
  try {
    const { data, error } = await supabase
      .from('private_snapshot')
      .select('payload, updated_at')
      .eq('id', 'master')
      .maybeSingle();

    if (error || !data) {
      return null;
    }

    const rawPayload = (data as { payload?: unknown; updated_at?: string }).payload;
    if (Array.isArray(rawPayload)) {
      return { assets: rawPayload as ContentAsset[], updatedAt: data.updated_at };
    }
    if (rawPayload && typeof rawPayload === 'object' && Array.isArray((rawPayload as { assets?: unknown }).assets)) {
      return {
        assets: (rawPayload as { assets: ContentAsset[] }).assets,
        updatedAt: data.updated_at,
      };
    }
    return null;
  } catch {
    return null;
  }
}
