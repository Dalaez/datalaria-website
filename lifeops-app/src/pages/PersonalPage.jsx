import React from 'react';
import { Activity, BookOpen, Film, Flame } from 'lucide-react';

export function PersonalPage() {
  return (
    <div className="personal-page">
      <div className="page-header-title">
        <h1>📓 Área Personal — Diario & Hábitos</h1>
        <p>Seguimiento de entrenamientos deportivos, lecturas, cine/series y desarrollo personal.</p>
      </div>

      <div className="glass-panel" style={{ padding: '2.5rem', textAlign: 'center' }}>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem', marginBottom: '1.5rem' }}>
          <Activity size={32} color="var(--accent-emerald)" />
          <BookOpen size={32} color="var(--accent-cyan)" />
          <Film size={32} color="var(--accent-purple)" />
          <Flame size={32} color="var(--accent-amber)" />
        </div>

        <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.5rem', marginBottom: '0.5rem' }}>
          Módulo de Contenidos Personales
        </h3>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '550px', margin: '0 auto 1.5rem auto' }}>
          En la <strong>Fase 3</strong> habilitaremos los formularios dinámicos para registrar entrenamientos (distancia, calorías, FC), libros (páginas leídas, valoraciones) y cine.
        </p>

        <span className="nav-badge" style={{ padding: '0.4rem 1rem', fontSize: '0.85rem' }}>
          🚀 Próximamente en Fase 3
        </span>
      </div>
    </div>
  );
}
