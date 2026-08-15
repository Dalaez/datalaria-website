import React from 'react';
import { Briefcase, CheckSquare, Layers, Clock } from 'lucide-react';

export function ProfessionalPage() {
  return (
    <div className="professional-page">
      <div className="page-header-title">
        <h1>📋 Área Profesional — Proyectos & Tareas</h1>
        <p>Gestión de proyectos, prioridades, presupuestos y control de tareas (Kanban/Listas).</p>
      </div>

      <div className="glass-panel" style={{ padding: '2.5rem', textAlign: 'center' }}>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem', marginBottom: '1.5rem' }}>
          <Briefcase size={32} color="var(--accent-purple)" />
          <CheckSquare size={32} color="var(--accent-amber)" />
          <Layers size={32} color="var(--accent-cyan)" />
          <Clock size={32} color="var(--accent-emerald)" />
        </div>

        <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.5rem', marginBottom: '0.5rem' }}>
          Gestor de Proyectos & Tareas
        </h3>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '550px', margin: '0 auto 1.5rem auto' }}>
          En la <strong>Fase 3</strong> implementaremos el tablero Kanban interactivo, control de horas estimadas vs. reales y seguimiento de presupuestos.
        </p>

        <span className="nav-badge" style={{ padding: '0.4rem 1rem', fontSize: '0.85rem' }}>
          🚀 Próximamente en Fase 3
        </span>
      </div>
    </div>
  );
}
