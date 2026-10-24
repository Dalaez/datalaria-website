import React from 'react';
import { useLanguage } from '../../context/LanguageContext';
import { Activity, BookOpen, Film, PlusCircle, CheckSquare, FileText } from 'lucide-react';
import './QuickActions.css';

export function QuickActions({ onAction }) {
  const { t } = useLanguage();

  const actions = [
    { id: 'sport', label: t('dashboard.recordWorkout'), icon: Activity, color: 'emerald' },
    { id: 'book', label: t('dashboard.addBook'), icon: BookOpen, color: 'cyan' },
    { id: 'film', label: t('dashboard.recordFilm'), icon: Film, color: 'purple' },
    { id: 'task', label: t('dashboard.createTask'), icon: CheckSquare, color: 'amber' },
    { id: 'report', label: t('dashboard.generateReport'), icon: FileText, color: 'emerald' },
  ];

  return (
    <div className="quick-actions-panel glass-panel">
      <div className="panel-header">
        <h3>{t('dashboard.quickActionsTitle')}</h3>
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
