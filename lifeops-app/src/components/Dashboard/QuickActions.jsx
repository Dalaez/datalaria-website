import React from 'react';
import { Activity, BookOpen, Film, PlusCircle, CheckSquare, FileText } from 'lucide-react';
import './QuickActions.css';

export function QuickActions({ onAction }) {
  const actions = [
    { id: 'sport', label: 'Registrar Deporte', icon: Activity, color: 'emerald' },
    { id: 'book', label: 'Añadir Libro', icon: BookOpen, color: 'cyan' },
    { id: 'film', label: 'Registrar Película/Serie', icon: Film, color: 'purple' },
    { id: 'task', label: 'Nueva Tarea', icon: CheckSquare, color: 'amber' },
    { id: 'report', label: 'Generar Informe', icon: FileText, color: 'emerald' },
  ];

  return (
    <div className="quick-actions-panel glass-panel">
      <div className="panel-header">
        <h3>Acciones Rápidas</h3>
        <span className="panel-badge">LifeOps Control</span>
      </div>

      <div className="quick-buttons-grid">
        {actions.map((action) => {
          const Icon = action.icon;
          return (
            <button
              key={action.id}
              onClick={() => onAction && onAction(action.id)}
              className={`action-btn color-${action.color}`}
            >
              <Icon size={18} />
              <span>{action.label}</span>
              <PlusCircle size={14} className="plus-icon" />
            </button>
          );
        })}
      </div>
    </div>
  );
}
