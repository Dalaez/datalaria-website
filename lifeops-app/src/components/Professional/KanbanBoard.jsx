import React, { useState, useEffect } from 'react';
import { api } from '../../lib/api';
import { Modal } from '../common/Modal';
import { 
  Plus, 
  Trash2, 
  ChevronRight, 
  ChevronLeft, 
  Clock, 
  Calendar, 
  AlertCircle, 
  CheckCircle2,
  Folder
} from 'lucide-react';
import './KanbanBoard.css';

const COLUMNS = [
  { id: 'todo', title: 'Por Hacer', color: '#6b7280', icon: '📝' },
  { id: 'in_progress', title: 'En Curso', color: '#06b6d4', icon: '⚡' },
  { id: 'review', title: 'En Revisión', color: '#8b5cf6', icon: '🔍' },
  { id: 'done', title: 'Completado', color: '#10b981', icon: '✅' },
];

export function KanbanBoard() {
  const [tasks, setTasks] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedProjectId, setSelectedProjectId] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  // New task form state
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    project_id: '',
    priority: 'medium',
    due_date: '',
    estimated_hours: '',
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      const [tasksData, projectsData] = await Promise.all([
        api.getTasks(null, selectedProjectId || null),
        api.getProjects(),
      ]);
      setTasks(tasksData || []);
      setProjects(projectsData || []);
    } catch (err) {
      console.error('Error fetching kanban data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [selectedProjectId]);

  const handleCreateTask = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = {
        title: formData.title,
        description: formData.description || null,
        project_id: formData.project_id || null,
        priority: formData.priority,
        due_date: formData.due_date || null,
        estimated_hours: formData.estimated_hours ? parseFloat(formData.estimated_hours) : null,
        status: 'todo',
      };
      await api.createTask(payload);
      setIsModalOpen(false);
      setFormData({
        title: '',
        description: '',
        project_id: '',
        priority: 'medium',
        due_date: '',
        estimated_hours: '',
      });
      fetchData();
    } catch (err) {
      alert(`Error al crear la tarea: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleMoveStatus = async (taskId, currentStatus, direction) => {
    const statusOrder = ['todo', 'in_progress', 'review', 'done'];
    const currentIndex = statusOrder.indexOf(currentStatus);
    const newIndex = direction === 'next' ? currentIndex + 1 : currentIndex - 1;

    if (newIndex < 0 || newIndex >= statusOrder.length) return;
    const newStatus = statusOrder[newIndex];

    // Optimistic UI update
    setTasks(tasks.map((t) => (t.id === taskId ? { ...t, status: newStatus } : t)));

    try {
      await api.updateTask(taskId, { status: newStatus });
    } catch (err) {
      alert(`Error al actualizar estado: ${err.message}`);
      fetchData();
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm('¿Deseas eliminar esta tarea?')) return;
    try {
      await api.deleteTask(taskId);
      setTasks(tasks.filter((t) => t.id !== taskId));
    } catch (err) {
      alert(`Error al eliminar tarea: ${err.message}`);
    }
  };

  const getPriorityBadge = (priority) => {
    switch (priority) {
      case 'critical':
        return <span className="priority-pill critical">Crítica</span>;
      case 'high':
        return <span className="priority-pill high">Alta</span>;
      case 'medium':
        return <span className="priority-pill medium">Media</span>;
      case 'low':
        return <span className="priority-pill low">Baja</span>;
      default:
        return null;
    }
  };

  const isOverdue = (dueDate, status) => {
    if (!dueDate || status === 'done') return false;
    const today = new Date().toISOString().split('T')[0];
    return dueDate < today;
  };

  return (
    <div className="kanban-module">
      {/* Top Filter & Actions Bar */}
      <div className="kanban-topbar">
        <div className="kanban-filters">
          <div className="project-filter-wrapper">
            <Folder size={16} className="filter-icon" />
            <select
              value={selectedProjectId}
              onChange={(e) => setSelectedProjectId(e.target.value)}
              className="project-select"
            >
              <option value="">Todos los Proyectos</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
        </div>

        <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
          <Plus size={16} />
          <span>Nueva Tarea</span>
        </button>
      </div>

      {/* Kanban Board Columns */}
      <div className="kanban-board">
        {COLUMNS.map((col) => {
          const colTasks = tasks.filter((t) => t.status === col.id);

          return (
            <div key={col.id} className="kanban-column glass-panel">
              {/* Column Header */}
              <div className="column-header">
                <div className="column-title-group">
                  <span className="col-icon">{col.icon}</span>
                  <h3>{col.title}</h3>
                </div>
                <span className="col-count-badge">{colTasks.length}</span>
              </div>

              {/* Column Cards Container */}
              <div className="column-cards-container">
                {colTasks.length === 0 ? (
                  <div className="empty-column-placeholder">
                    <span>Sin tareas</span>
                  </div>
                ) : (
                  colTasks.map((task) => {
                    const project = projects.find((p) => p.id === task.project_id);
                    const overdue = isOverdue(task.due_date, task.status);

                    return (
                      <div key={task.id} className="kanban-task-card glass-card">
                        {/* Project & Priority line */}
                        <div className="task-card-meta">
                          {project && (
                            <span 
                              className="task-project-tag"
                              style={{ borderColor: project.color || 'var(--accent-purple)' }}
                            >
                              {project.name}
                            </span>
                          )}
                          {getPriorityBadge(task.priority)}
                        </div>

                        {/* Title & Desc */}
                        <h4 className="task-title">{task.title}</h4>
                        {task.description && (
                          <p className="task-desc">{task.description}</p>
                        )}

                        {/* Footer Indicators */}
                        <div className="task-footer">
                          <div className="task-chips">
                            {task.due_date && (
                              <div className={`chip-date ${overdue ? 'overdue' : ''}`}>
                                <Calendar size={12} />
                                <span>{task.due_date}</span>
                              </div>
                            )}
                            {task.estimated_hours != null && (
                              <div className="chip-hours">
                                <Clock size={12} />
                                <span>{task.estimated_hours}h</span>
                              </div>
                            )}
                          </div>

                          {/* Navigation & Delete controls */}
                          <div className="task-actions">
                            {col.id !== 'todo' && (
                              <button 
                                className="action-step-btn"
                                onClick={() => handleMoveStatus(task.id, task.status, 'prev')}
                                title="Mover a columna anterior"
                              >
                                <ChevronLeft size={14} />
                              </button>
                            )}
                            {col.id !== 'done' && (
                              <button 
                                className="action-step-btn"
                                onClick={() => handleMoveStatus(task.id, task.status, 'next')}
                                title="Avanzar a siguiente columna"
                              >
                                <ChevronRight size={14} />
                              </button>
                            )}
                            <button 
                              className="delete-icon-btn"
                              onClick={() => handleDeleteTask(task.id)}
                              title="Eliminar tarea"
                            >
                              <Trash2 size={13} />
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Modal Nueva Tarea */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Crear Nueva Tarea"
      >
        <form onSubmit={handleCreateTask} className="modal-form">
          <div className="form-group">
            <label>Título de la Tarea *</label>
            <input 
              type="text" 
              required
              placeholder="Ej: Diseñar arquitectura de base de datos, Revisar KPIs..."
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
          </div>

          <div className="form-group">
            <label>Proyecto Asociado</label>
            <select
              value={formData.project_id}
              onChange={(e) => setFormData({ ...formData, project_id: e.target.value })}
            >
              <option value="">Sin Proyecto (General)</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>

          <div className="form-row">
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

            <div className="form-group">
              <label>Fecha Límite</label>
              <input 
                type="date"
                value={formData.due_date}
                onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Horas Estimadas</label>
            <input 
              type="number" 
              step="0.5" 
              min="0"
              placeholder="Ej: 3.5"
              value={formData.estimated_hours}
              onChange={(e) => setFormData({ ...formData, estimated_hours: e.target.value })}
            />
          </div>

          <div className="form-group">
            <label>Descripción / Criterios de Aceptación</label>
            <textarea 
              placeholder="Detalles sobre lo que se debe entregar..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </div>

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={() => setIsModalOpen(false)}>
              Cancelar
            </button>
            <button type="submit" className="btn-primary" disabled={submitting}>
              {submitting ? 'Creando...' : 'Crear Tarea'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
