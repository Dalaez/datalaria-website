import React, { useState, useEffect } from 'react';
import { api } from '../../lib/api';
import { Modal } from '../common/Modal';
import { useLanguage } from '../../context/LanguageContext';
import { 
  FolderKanban, 
  Plus, 
  Trash2, 
  Calendar, 
  DollarSign, 
  Layers, 
  Clock,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import './ProjectsManager.css';

const PRESET_COLORS = [
  '#10b981', // Emerald
  '#06b6d4', // Cyan
  '#8b5cf6', // Purple
  '#f59e0b', // Amber
  '#ec4899', // Pink
  '#3b82f6', // Blue
];

export function ProjectsManager() {
  const { t, language } = useLanguage();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const defaultFormData = {
    name: '',
    description: '',
    status: 'active',
    priority: 'medium',
    budget: '',
    start_date: new Date().toISOString().split('T')[0],
    target_end_date: '',
    color: '#8b5cf6',
  };

  const [formData, setFormData] = useState(defaultFormData);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const data = await api.getProjects();
      setProjects(data || []);
    } catch (err) {
      console.error('Error fetching projects:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = {
        name: formData.name,
        description: formData.description || null,
        status: formData.status,
        priority: formData.priority,
        budget: formData.budget ? parseFloat(formData.budget) : null,
        start_date: formData.start_date || null,
        target_end_date: formData.target_end_date || null,
        color: formData.color,
      };

      await api.createProject(payload);
      setIsModalOpen(false);
      setFormData(defaultFormData);
      fetchProjects();
    } catch (err) {
      alert(`${t('common.error')}: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm(t('common.confirmDelete'))) return;
    try {
      await api.deleteProject(id);
      setProjects(projects.filter((p) => p.id !== id));
    } catch (err) {
      alert(`${t('common.error')}: ${err.message}`);
    }
  };

  const activeProjects = projects.filter((p) => p.status === 'active').length;
  const totalBudget = projects.reduce((sum, p) => sum + (p.budget || 0), 0);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'active':
        return <span className="status-badge active">● {language === 'es' ? 'Activo' : 'Active'}</span>;
      case 'completed':
        return <span className="status-badge completed">✔ {language === 'es' ? 'Completado' : 'Completed'}</span>;
      case 'on_hold':
        return <span className="status-badge on-hold">⏸ {language === 'es' ? 'Pausado' : 'On Hold'}</span>;
      default:
        return <span className="status-badge">{status}</span>;
    }
  };

  return (
    <div className="projects-module">
      {/* Top Header */}
      <div className="module-header">
        <div>
          <h2>{t('professional.projectsTitle')}</h2>
          <p>{t('professional.projectsSubtitle')}</p>
        </div>
        <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
          <Plus size={16} />
          <span>{t('professional.addProject')}</span>
        </button>
      </div>

      {/* Metrics Banner */}
      <div className="metrics-banner">
        <div className="metric-box">
          <span className="metric-label">{language === 'es' ? 'PROYECTOS ACTIVOS' : 'ACTIVE PROJECTS'}</span>
          <span className="metric-value">{activeProjects} <small>{language === 'es' ? 'en marcha' : 'in progress'}</small></span>
        </div>
        <div className="metric-box">
          <span className="metric-label">{language === 'es' ? 'TOTAL PROYECTOS' : 'TOTAL PROJECTS'}</span>
          <span className="metric-value" style={{ color: 'var(--accent-purple)' }}>
            {projects.length} <small>{t('common.all')}</small>
          </span>
        </div>
        <div className="metric-box">
          <span className="metric-label">{language === 'es' ? 'PRESUPUESTO TOTAL' : 'TOTAL BUDGET'}</span>
          <span className="metric-value" style={{ color: 'var(--accent-cyan)' }}>
            {totalBudget > 0 ? `${totalBudget.toLocaleString()} €` : '0 €'}
          </span>
        </div>
      </div>

      {/* Projects Grid */}
      {loading ? (
        <div className="loading-state">{t('common.loading')}</div>
      ) : projects.length === 0 ? (
        <div className="empty-state glass-panel">
          <FolderKanban size={40} className="empty-icon" />
          <h3>{language === 'es' ? 'No hay proyectos registrados' : 'No projects registered'}</h3>
          <p>{language === 'es' ? 'Crea tu primer proyecto para organizar tareas, hitos y controlar presupuestos.' : 'Create your first project to organize tasks, milestones and track budgets.'}</p>
          <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
            <Plus size={16} />
            <span>{t('professional.addProject')}</span>
          </button>
        </div>
      ) : (
        <div className="projects-grid">
          {projects.map((project) => (
            <div key={project.id} className="project-card glass-card">
              {/* Color Header Stripe */}
              <div 
                className="project-accent-bar" 
                style={{ backgroundColor: project.color || 'var(--accent-purple)' }} 
              />

              <div className="project-card-header">
                <div className="project-title-group">
                  <h4 className="project-name">{project.name}</h4>
                  {getStatusBadge(project.status)}
                </div>

                <button 
                  className="delete-icon-btn" 
                  onClick={() => handleDelete(project.id)}
                  title={t('common.delete')}
                >
                  <Trash2 size={14} />
                </button>
              </div>

              {project.description && (
                <p className="project-desc">{project.description}</p>
              )}

              {/* Financials & Dates */}
              <div className="project-info-grid">
                {project.budget != null && (
                  <div className="info-item">
                    <span className="info-label">{t('professional.fields.budget')}</span>
                    <span className="info-value">{project.budget.toLocaleString()} €</span>
                  </div>
                )}
                {project.target_end_date && (
                  <div className="info-item">
                    <span className="info-label">{t('professional.fields.targetEndDate')}</span>
                    <span className="info-value">{project.target_end_date}</span>
                  </div>
                )}
                <div className="info-item">
                  <span className="info-label">{t('professional.fields.priority')}</span>
                  <span className="info-value" style={{ textTransform: 'capitalize' }}>
                    {project.priority}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal Form */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={t('professional.addProject')}
      >
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label>{language === 'es' ? 'Nombre del Proyecto *' : 'Project Name *'}</label>
            <input 
              type="text" 
              required
              placeholder={language === 'es' ? 'Ej: Lanzamiento Web Datalaria, Migración Cloud...' : 'e.g. Datalaria Website Launch, Cloud Migration...'}
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('professional.fields.status')}</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              >
                <option value="active">{language === 'es' ? 'Activo' : 'Active'}</option>
                <option value="on_hold">{language === 'es' ? 'En Pausa' : 'On Hold'}</option>
                <option value="completed">{language === 'es' ? 'Completado' : 'Completed'}</option>
              </select>
            </div>

            <div className="form-group">
              <label>{t('professional.fields.priority')}</label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
              >
                <option value="low">🟢 {t('professional.priorities.low')}</option>
                <option value="medium">🟡 {t('professional.priorities.medium')}</option>
                <option value="high">🟠 {t('professional.priorities.high')}</option>
                <option value="critical">🔴 {t('professional.priorities.urgent')}</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('professional.fields.budget')}</label>
              <input 
                type="number" 
                min="0"
                placeholder="2500"
                value={formData.budget}
                onChange={(e) => setFormData({ ...formData, budget: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>{t('professional.fields.targetEndDate')}</label>
              <input 
                type="date"
                value={formData.target_end_date}
                onChange={(e) => setFormData({ ...formData, target_end_date: e.target.value })}
              />
            </div>
          </div>

          <div className="form-group">
            <label>{language === 'es' ? 'Color de Identificación' : 'Project Color Tag'}</label>
            <div className="color-presets-row">
              {PRESET_COLORS.map((c) => (
                <button
                  type="button"
                  key={c}
                  className={`color-preset-circle ${formData.color === c ? 'selected' : ''}`}
                  style={{ backgroundColor: c }}
                  onClick={() => setFormData({ ...formData, color: c })}
                />
              ))}
            </div>
          </div>

          <div className="form-group">
            <label>{t('professional.fields.description')}</label>
            <textarea 
              placeholder={language === 'es' ? 'Objetivos y alcance del proyecto...' : 'Project scope and objectives...'}
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </div>

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={() => setIsModalOpen(false)}>
              {t('common.cancel')}
            </button>
            <button type="submit" className="btn-primary" disabled={submitting}>
              {submitting ? t('common.loading') : t('professional.addProject')}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
