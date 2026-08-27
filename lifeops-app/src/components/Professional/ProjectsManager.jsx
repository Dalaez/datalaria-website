import React, { useState, useEffect } from 'react';
import { api } from '../../lib/api';
import { Modal } from '../common/Modal';
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
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    name: '',
    description: '',
    status: 'active',
    priority: 'medium',
    budget: '',
    start_date: new Date().toISOString().split('T')[0],
    target_end_date: '',
    color: '#8b5cf6',
  });

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
      setFormData({
        name: '',
        description: '',
        status: 'active',
        priority: 'medium',
        budget: '',
        start_date: new Date().toISOString().split('T')[0],
        target_end_date: '',
        color: '#8b5cf6',
      });
      fetchProjects();
    } catch (err) {
      alert(`Error al crear el proyecto: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Seguro que deseas eliminar este proyecto? Sus tareas quedarán sin proyecto asignado.')) return;
    try {
      await api.deleteProject(id);
      setProjects(projects.filter((p) => p.id !== id));
    } catch (err) {
      alert(`Error al eliminar proyecto: ${err.message}`);
    }
  };

  const activeProjects = projects.filter((p) => p.status === 'active').length;
  const totalBudget = projects.reduce((acc, curr) => acc + (curr.budget || 0), 0);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'active': return <span className="proj-status active">En Curso</span>;
      case 'planning': return <span className="proj-status planning">Planificación</span>;
      case 'completed': return <span className="proj-status completed">Completado</span>;
      case 'on_hold': return <span className="proj-status on-hold">En Pausa</span>;
      default: return <span className="proj-status">{status}</span>;
    }
  };

  return (
    <div className="projects-module">
      {/* Header */}
      <div className="module-header">
        <div>
          <h2>Gestión de Proyectos</h2>
          <p>Control de portafolio de proyectos, presupuestos y fechas clave.</p>
        </div>
        <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
          <Plus size={16} />
          <span>Nuevo Proyecto</span>
        </button>
      </div>

      {/* Metrics Banner */}
      <div className="metrics-banner">
        <div className="metric-box">
          <span className="metric-label">PROYECTOS ACTIVOS</span>
          <span className="metric-value">{activeProjects} <small>activos</small></span>
        </div>
        <div className="metric-box">
          <span className="metric-label">TOTAL PROYECTOS</span>
          <span className="metric-value" style={{ color: 'var(--accent-purple)' }}>
            {projects.length} <small>registrados</small>
          </span>
        </div>
        <div className="metric-box">
          <span className="metric-label">PRESUPUESTO TOTAL</span>
          <span className="metric-value" style={{ color: 'var(--accent-cyan)' }}>
            {totalBudget > 0 ? `${totalBudget.toLocaleString()} €` : '0 €'}
          </span>
        </div>
      </div>

      {/* Projects Grid */}
      {loading ? (
        <div className="loading-state">Cargando proyectos...</div>
      ) : projects.length === 0 ? (
        <div className="empty-state glass-panel">
          <FolderKanban size={40} className="empty-icon" />
          <h3>No hay proyectos registrados</h3>
          <p>Crea tu primer proyecto para organizar tareas, hitos y controlar presupuestos.</p>
          <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
            <Plus size={16} />
            <span>Crear primer proyecto</span>
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
                  title="Eliminar proyecto"
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
                    <span className="info-label">Presupuesto</span>
                    <span className="info-value">{project.budget.toLocaleString()} €</span>
                  </div>
                )}
                {project.target_end_date && (
                  <div className="info-item">
                    <span className="info-label">Fecha Objetivo</span>
                    <span className="info-value">{project.target_end_date}</span>
                  </div>
                )}
                <div className="info-item">
                  <span className="info-label">Prioridad</span>
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
        title="Crear Nuevo Proyecto"
      >
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label>Nombre del Proyecto *</label>
            <input 
              type="text" 
              required
              placeholder="Ej: Lanzamiento Web Datalaria, Migración Cloud..."
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Estado *</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              >
                <option value="active">⚡ Activo / En Curso</option>
                <option value="planning">📝 En Planificación</option>
                <option value="on_hold">⏸️ En Pausa</option>
                <option value="completed">✅ Completado</option>
              </select>
            </div>

            <div className="form-group">
              <label>Prioridad *</label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
              >
                <option value="low">🟢 Baja</option>
                <option value="medium">🟡 Media</option>
                <option value="high">🟠 Alta</option>
                <option value="critical">🔴 Crítica</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Presupuesto Asignado (€)</label>
              <input 
                type="number" 
                min="0"
                placeholder="Ej: 5000"
                value={formData.budget}
                onChange={(e) => setFormData({ ...formData, budget: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Color Identificador</label>
              <div className="color-picker-row">
                {PRESET_COLORS.map((c) => (
                  <button
                    key={c}
                    type="button"
                    className={`color-dot-btn ${formData.color === c ? 'selected' : ''}`}
                    style={{ backgroundColor: c }}
                    onClick={() => setFormData({ ...formData, color: c })}
                  />
                ))}
              </div>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Fecha de Inicio</label>
              <input 
                type="date"
                value={formData.start_date}
                onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Fecha Objetivo de Finalización</label>
              <input 
                type="date"
                value={formData.target_end_date}
                onChange={(e) => setFormData({ ...formData, target_end_date: e.target.value })}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Descripción / Objetivos</label>
            <textarea 
              placeholder="Alcance del proyecto, entregables..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </div>

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={() => setIsModalOpen(false)}>
              Cancelar
            </button>
            <button type="submit" className="btn-primary" disabled={submitting}>
              {submitting ? 'Creando...' : 'Crear Proyecto'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
