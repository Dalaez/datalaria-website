import React, { useState, useEffect } from 'react';
import { api } from '../../lib/api';
import { Modal } from '../common/Modal';
import { useLanguage } from '../../context/LanguageContext';
import { 
  Plus, 
  Trash2, 
  Edit2,
  ChevronRight, 
  ChevronLeft, 
  Clock, 
  Calendar, 
  Folder,
  Layers
} from 'lucide-react';
import './KanbanBoard.css';

export function KanbanBoard() {
  const { t, language } = useLanguage();
  const [tasks, setTasks] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedProjectId, setSelectedProjectId] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const columns = [
    { id: 'todo', title: t('professional.columns.todo'), color: '#6b7280', icon: '📝' },
    { id: 'in_progress', title: t('professional.columns.in_progress'), color: '#06b6d4', icon: '⚡' },
    { id: 'review', title: t('professional.columns.review'), color: '#8b5cf6', icon: '🔍' },
    { id: 'done', title: t('professional.columns.done'), color: '#10b981', icon: '✅' },
  ];

  const defaultFormData = {
    title: '',
    description: '',
    project_id: '',
    priority: 'medium',
    status: 'todo',
    due_date: '',
    estimated_hours: '',
  };

  const [formData, setFormData] = useState(defaultFormData);

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

  const handleOpenCreate = () => {
    setEditingTask(null);
    setFormData(defaultFormData);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (task) => {
    setEditingTask(task);
    setFormData({
      title: task.title || '',
      description: task.description || '',
      project_id: task.project_id || '',
      priority: task.priority || 'medium',
      status: task.status || 'todo',
      due_date: task.due_date || '',
      estimated_hours: task.estimated_hours != null ? task.estimated_hours : '',
    });
    setIsModalOpen(true);
  };

  const handleSubmitTask = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = {
        title: formData.title,
        description: formData.description || null,
        project_id: formData.project_id || null,
        priority: formData.priority,
        status: editingTask ? formData.status : 'todo',
        due_date: formData.due_date || null,
        estimated_hours: formData.estimated_hours !== '' ? parseFloat(formData.estimated_hours) : null,
      };

      if (editingTask) {
        await api.updateTask(editingTask.id, payload);
      } else {
        await api.createTask(payload);
      }

      setIsModalOpen(false);
      setFormData(defaultFormData);
      setEditingTask(null);
      fetchData();
    } catch (err) {
      alert(`${t('common.error')}: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleMoveTask = async (taskId, currentStatus, direction) => {
    const statusOrder = ['todo', 'in_progress', 'review', 'done'];
    const currentIndex = statusOrder.indexOf(currentStatus);
    const targetIndex = direction === 'next' ? currentIndex + 1 : currentIndex - 1;

    if (targetIndex < 0 || targetIndex >= statusOrder.length) return;
    const targetStatus = statusOrder[targetIndex];

    try {
      // Optimistic update
      setTasks((prev) =>
        prev.map((t) => (t.id === taskId ? { ...t, status: targetStatus } : t))
      );
      await api.updateTask(taskId, { status: targetStatus });
    } catch (err) {
      console.error('Error updating task status:', err);
      fetchData();
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm(t('common.confirmDelete'))) return;
    try {
      await api.deleteTask(taskId);
      setTasks(tasks.filter((t) => t.id !== taskId));
    } catch (err) {
      alert(`${t('common.error')}: ${err.message}`);
    }
  };

  const getPriorityBadge = (priority) => {
    switch (priority) {
      case 'critical':
      case 'urgent':
        return <span className="kanban-priority-pill critical">{t('professional.priorities.urgent')}</span>;
      case 'high':
        return <span className="kanban-priority-pill high">{t('professional.priorities.high')}</span>;
      case 'medium':
        return <span className="kanban-priority-pill medium">{t('professional.priorities.medium')}</span>;
      case 'low':
        return <span className="kanban-priority-pill low">{t('professional.priorities.low')}</span>;
      default:
        return null;
    }
  };

  const isOverdue = (dueDate, status) => {
    if (!dueDate || status === 'done') return false;
    const today = new Date().toISOString().split('T')[0];
    return dueDate < today;
  };

  const getProjectName = (projectId) => {
    if (!projectId) return null;
    const p = projects.find((item) => item.id === projectId);
    return p ? p.name : null;
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
              <option value="">{language === 'es' ? 'Todos los Proyectos' : 'All Projects'}</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
        </div>

        <button className="btn-primary" onClick={handleOpenCreate}>
          <Plus size={16} />
          <span>{t('professional.addTask')}</span>
        </button>
      </div>

      {/* Kanban Board Columns */}
      <div className="kanban-board">
        {columns.map((col) => {
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

              {/* Tasks List */}
              <div className="kanban-cards-container">
                {colTasks.length === 0 ? (
                  <div className="empty-column-placeholder">
                    {language === 'es' ? 'Sin tareas en esta etapa' : 'No tasks in this stage'}
                  </div>
                ) : (
                  colTasks.map((task) => {
                    const overdue = isOverdue(task.due_date, task.status);
                    const projName = getProjectName(task.project_id);

                    return (
                      <div 
                        key={task.id} 
                        className={`kanban-task-card ${overdue ? 'overdue-card' : ''}`}
                      >
                        <div className="task-card-top-row">
                          <div className="task-badges-left">
                            {getPriorityBadge(task.priority)}
                            {projName && (
                              <span className="task-project-tag" title={projName}>
                                <Layers size={11} /> {projName}
                              </span>
                            )}
                          </div>
                          <div className="task-actions-right">
                            <button 
                              className="task-icon-btn edit"
                              onClick={() => handleOpenEdit(task)}
                              title={t('common.edit')}
                            >
                              <Edit2 size={13} />
                            </button>
                            <button 
                              className="task-icon-btn delete"
                              onClick={() => handleDeleteTask(task.id)}
                              title={t('common.delete')}
                            >
                              <Trash2 size={13} />
                            </button>
                          </div>
                        </div>

                        <h4 className="kanban-task-title">{task.title}</h4>

                        {task.description && (
                          <p className="kanban-task-desc">{task.description}</p>
                        )}

                        <div className="kanban-task-meta">
                          {task.due_date && (
                            <div className={`meta-chip ${overdue ? 'overdue' : ''}`}>
                              <Calendar size={12} />
                              <span>{task.due_date}</span>
                            </div>
                          )}
                          {task.estimated_hours && (
                            <div className="meta-chip">
                              <Clock size={12} />
                              <span>{task.estimated_hours}h</span>
                            </div>
                          )}
                        </div>

                        {/* Navigation Arrows between status columns */}
                        <div className="kanban-task-footer">
                          <button
                            className="nav-step-btn"
                            disabled={col.id === 'todo'}
                            onClick={() => handleMoveTask(task.id, task.status, 'prev')}
                            title={language === 'es' ? 'Mover a columna anterior' : 'Move to previous column'}
                          >
                            <ChevronLeft size={14} />
                          </button>
                          <span className="kanban-step-label">{col.title}</span>
                          <button
                            className="nav-step-btn"
                            disabled={col.id === 'done'}
                            onClick={() => handleMoveTask(task.id, task.status, 'next')}
                            title={language === 'es' ? 'Mover a columna siguiente' : 'Move to next column'}
                          >
                            <ChevronRight size={14} />
                          </button>
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

      {/* Modal Nueva / Editar Tarea */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingTask(null);
        }}
        title={editingTask ? t('professional.editTask') : t('professional.addTask')}
      >
        <form onSubmit={handleSubmitTask} className="modal-form">
          <div className="form-group">
            <label>{t('professional.fields.title')}</label>
            <input 
              type="text" 
              required
              placeholder={language === 'es' ? 'Ej: Diseñar arquitectura, Revisar métricas...' : 'e.g. Design DB schema, Review metrics...'}
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
          </div>

          <div className="form-group">
            <label>{t('professional.fields.project')}</label>
            <select
              value={formData.project_id}
              onChange={(e) => setFormData({ ...formData, project_id: e.target.value })}
            >
              <option value="">{language === 'es' ? 'Sin Proyecto (General)' : 'No Project (General)'}</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>

          <div className="form-row">
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

            <div className="form-group">
              <label>{t('professional.fields.dueDate')}</label>
              <input 
                type="date"
                value={formData.due_date}
                onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
              />
            </div>
          </div>

          <div className="form-group">
            <label>{t('professional.fields.estimatedHours')}</label>
            <input 
              type="number" 
              step="0.5" 
              min="0"
              placeholder="3.5"
              value={formData.estimated_hours}
              onChange={(e) => setFormData({ ...formData, estimated_hours: e.target.value })}
            />
          </div>

          <div className="form-group">
            <label>{t('professional.fields.description')}</label>
            <textarea 
              placeholder={language === 'es' ? 'Detalles sobre lo que se debe entregar...' : 'Details and acceptance criteria...'}
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </div>

          <div className="form-actions">
            <button 
              type="button" 
              className="btn-secondary" 
              onClick={() => {
                setIsModalOpen(false);
                setEditingTask(null);
              }}
            >
              {t('common.cancel')}
            </button>
            <button type="submit" className="btn-primary" disabled={submitting}>
              {submitting ? t('common.saving') : (editingTask ? t('common.saveChanges') : t('professional.addTask'))}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
