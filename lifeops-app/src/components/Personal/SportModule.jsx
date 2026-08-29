import React, { useState, useEffect } from 'react';
import { api } from '../../lib/api';
import { Modal } from '../common/Modal';
import { useLanguage } from '../../context/LanguageContext';
import { 
  Activity, 
  Plus, 
  Trash2, 
  Edit2, 
  Award, 
  Flame, 
  Heart, 
  Clock, 
  Navigation, 
  TrendingUp,
  Dumbbell,
  Bike,
  LayoutGrid,
  Table as TableIcon
} from 'lucide-react';
import './SportModule.css';

export function SportModule() {
  const { t, language } = useLanguage();
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingWorkout, setEditingWorkout] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [viewMode, setViewMode] = useState(() => {
    return localStorage.getItem('lifeops_view_sport') || 'grid';
  });

  const handleViewChange = (mode) => {
    setViewMode(mode);
    localStorage.setItem('lifeops_view_sport', mode);
  };

  // Form state
  const defaultFormData = {
    title: '',
    date: new Date().toISOString().split('T')[0],
    duration_minutes: 45,
    workout_type: 'running',
    distance_km: '',
    calories: '',
    avg_heart_rate: '',
    elevation_m: '',
    personal_best: false,
    notes: '',
  };

  const [formData, setFormData] = useState(defaultFormData);

  const fetchWorkouts = async () => {
    try {
      setLoading(true);
      const data = await api.getActivitiesWithDetails('sport');
      setWorkouts(data || []);
    } catch (err) {
      console.error('Error fetching workouts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkouts();
  }, []);

  const handleOpenCreate = () => {
    setEditingWorkout(null);
    setFormData(defaultFormData);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (act) => {
    setEditingWorkout(act);
    const w = act.workout || {};
    setFormData({
      title: act.title || '',
      date: act.date || new Date().toISOString().split('T')[0],
      duration_minutes: act.duration_minutes || 45,
      workout_type: w.workout_type || 'running',
      distance_km: w.distance_km != null ? w.distance_km : '',
      calories: w.calories != null ? w.calories : '',
      avg_heart_rate: w.avg_heart_rate || w.heart_rate_avg || '',
      elevation_m: w.elevation_m != null ? w.elevation_m : '',
      personal_best: Boolean(w.personal_best),
      notes: act.description || w.notes || act.notes || '',
    });
    setIsModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = {
        activity: {
          activity_type: 'sport',
          title: formData.title,
          date: formData.date,
          duration_minutes: formData.duration_minutes ? parseInt(formData.duration_minutes) : null,
          description: formData.notes,
        },
        workout: {
          workout_type: formData.workout_type,
          distance_km: formData.distance_km !== '' ? parseFloat(formData.distance_km) : null,
          calories: formData.calories !== '' ? parseInt(formData.calories) : null,
          avg_heart_rate: formData.avg_heart_rate !== '' ? parseInt(formData.avg_heart_rate) : null,
          elevation_m: formData.elevation_m !== '' ? parseInt(formData.elevation_m) : null,
          personal_best: formData.personal_best,
          notes: formData.notes,
        },
      };

      if (editingWorkout) {
        await api.updateSportActivity(editingWorkout.id, payload);
      } else {
        await api.createSportActivity(payload);
      }

      setIsModalOpen(false);
      setFormData(defaultFormData);
      setEditingWorkout(null);
      fetchWorkouts();
    } catch (err) {
      alert(`${t('common.error')}: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm(t('common.confirmDelete'))) return;
    try {
      await api.deleteActivity(id);
      setWorkouts((prev) => prev.filter((w) => w.id !== id));
    } catch (err) {
      alert(`${t('common.error')}: ${err.message}`);
    }
  };

  // KPIs
  const totalKm = workouts.reduce((sum, act) => sum + (act.workout?.distance_km || 0), 0);
  const totalMinutes = workouts.reduce((sum, act) => sum + (act.duration_minutes || 0), 0);
  const totalCalories = workouts.reduce((sum, act) => sum + (act.workout?.calories || 0), 0);
  const pbCount = workouts.filter((act) => act.workout?.personal_best).length;

  const getSportIcon = (type) => {
    switch (type) {
      case 'running': return <Activity size={16} color="var(--accent-emerald)" />;
      case 'cycling': return <Bike size={16} color="var(--accent-cyan)" />;
      case 'gym': return <Dumbbell size={16} color="var(--accent-purple)" />;
      default: return <Activity size={16} color="var(--accent-amber)" />;
    }
  };

  return (
    <div className="sport-module">
      {/* Top Action Bar */}
      <div className="module-header">
        <div>
          <h2>{t('sport.title')}</h2>
          <p>{t('sport.subtitle')}</p>
        </div>

        <div className="module-header-actions">
          {/* View Mode Toggle */}
          <div className="view-mode-toggle glass-panel">
            <button
              type="button"
              className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`}
              onClick={() => handleViewChange('grid')}
              title={t('common.cardsView')}
            >
              <LayoutGrid size={15} />
              <span>{t('common.cardsView')}</span>
            </button>
            <button
              type="button"
              className={`view-btn ${viewMode === 'table' ? 'active' : ''}`}
              onClick={() => handleViewChange('table')}
              title={t('common.tableView')}
            >
              <TableIcon size={15} />
              <span>{t('common.tableView')}</span>
            </button>
          </div>

          <button className="btn-primary" onClick={handleOpenCreate}>
            <Plus size={16} />
            <span>{t('sport.addWorkout')}</span>
          </button>
        </div>
      </div>

      {/* Metrics Banner */}
      <div className="metrics-banner">
        <div className="metric-box">
          <span className="metric-label">{t('sport.totalDistance')}</span>
          <span className="metric-value">{totalKm.toFixed(1)} <small>{t('common.km')}</small></span>
        </div>
        <div className="metric-box">
          <span className="metric-label">{t('sport.activeTime')}</span>
          <span className="metric-value" style={{ color: 'var(--accent-cyan)' }}>
            {(totalMinutes / 60).toFixed(1)} <small>{t('common.hours')}</small>
          </span>
        </div>
        <div className="metric-box">
          <span className="metric-label">{t('sport.caloriesBurned')}</span>
          <span className="metric-value" style={{ color: 'var(--accent-amber)' }}>
            {totalCalories.toLocaleString()} <small>{t('common.kcal')}</small>
          </span>
        </div>
        <div className="metric-box">
          <span className="metric-label">{t('sport.personalBests')}</span>
          <span className="metric-value" style={{ color: 'var(--accent-purple)' }}>
            {pbCount} <small>PBs 🏅</small>
          </span>
        </div>
      </div>

      {/* Workouts Content */}
      {loading ? (
        <div className="loading-state">{t('sport.loading')}</div>
      ) : workouts.length === 0 ? (
        <div className="empty-state glass-panel">
          <Activity size={40} className="empty-icon" />
          <h3>{t('sport.emptyTitle')}</h3>
          <p>{t('sport.emptyDesc')}</p>
          <button className="btn-primary" onClick={handleOpenCreate}>
            <Plus size={16} />
            <span>{t('sport.emptyAction')}</span>
          </button>
        </div>
      ) : viewMode === 'grid' ? (
        /* Grid / Cards View */
        <div className="workouts-grid">
          {workouts.map((act) => {
            const w = act.workout || {};
            return (
              <div key={act.id} className="workout-card glass-card">
                <div className="workout-card-header">
                  <div className="workout-type-badge">
                    {getSportIcon(w.workout_type)}
                    <span className="type-name">{w.workout_type?.toUpperCase()}</span>
                  </div>
                  <div className="card-top-right">
                    {w.personal_best && (
                      <span className="pb-badge" title={t('sport.isPBLabel')}>
                        <Award size={14} /> PB
                      </span>
                    )}
                    <button 
                      className="edit-icon-btn" 
                      onClick={() => handleOpenEdit(act)}
                      title={t('common.edit')}
                    >
                      <Edit2 size={14} />
                    </button>
                    <button 
                      className="delete-icon-btn" 
                      onClick={() => handleDelete(act.id)}
                      title={t('common.delete')}
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>

                <h4 className="workout-title">{act.title}</h4>
                <span className="workout-date">{act.date}</span>

                <div className="workout-stats-chips">
                  {w.distance_km != null && (
                    <div className="stat-chip">
                      <Navigation size={13} />
                      <span>{w.distance_km} {t('common.km')}</span>
                    </div>
                  )}
                  {act.duration_minutes != null && (
                    <div className="stat-chip">
                      <Clock size={13} />
                      <span>{act.duration_minutes} {t('common.min')}</span>
                    </div>
                  )}
                  {w.calories != null && (
                    <div className="stat-chip">
                      <Flame size={13} />
                      <span>{w.calories} {t('common.kcal')}</span>
                    </div>
                  )}
                  {(w.avg_heart_rate != null || w.heart_rate_avg != null) && (
                    <div className="stat-chip">
                      <Heart size={13} />
                      <span>{w.avg_heart_rate || w.heart_rate_avg} {t('common.ppm')}</span>
                    </div>
                  )}
                  {w.elevation_m != null && (
                    <div className="stat-chip">
                      <TrendingUp size={13} />
                      <span>+{w.elevation_m}m</span>
                    </div>
                  )}
                </div>

                {(act.description || w.notes || act.notes) && (
                  <p className="workout-notes">{act.description || w.notes || act.notes}</p>
                )}
              </div>
            );
          })}
        </div>
      ) : (
        /* Table / Synthesized View */
        <div className="module-table-wrapper glass-panel">
          <table className="module-data-table">
            <thead>
              <tr>
                <th>{language === 'es' ? 'Fecha' : 'Date'}</th>
                <th>{language === 'es' ? 'Deporte' : 'Sport'}</th>
                <th>{language === 'es' ? 'Título / Sesión' : 'Title / Session'}</th>
                <th>{language === 'es' ? 'Distancia' : 'Distance'}</th>
                <th>{language === 'es' ? 'Duración' : 'Duration'}</th>
                <th>{language === 'es' ? 'Calorías' : 'Calories'}</th>
                <th>{language === 'es' ? 'FC Media' : 'Avg HR'}</th>
                <th>{language === 'es' ? 'Récord' : 'Record'}</th>
                <th>{language === 'es' ? 'Notas' : 'Notes'}</th>
                <th style={{ textAlign: 'right' }}>{t('common.actions')}</th>
              </tr>
            </thead>
            <tbody>
              {workouts.map((act) => {
                const w = act.workout || {};
                return (
                  <tr key={act.id}>
                    <td className="table-date-cell">{act.date}</td>
                    <td>
                      <div className="table-sport-type">
                        {getSportIcon(w.workout_type)}
                        <span>{w.workout_type?.toUpperCase()}</span>
                      </div>
                    </td>
                    <td className="table-title-cell">{act.title}</td>
                    <td>{w.distance_km != null ? `${w.distance_km} km` : '-'}</td>
                    <td>{act.duration_minutes != null ? `${act.duration_minutes} min` : '-'}</td>
                    <td>{w.calories != null ? `${w.calories} kcal` : '-'}</td>
                    <td>{(w.avg_heart_rate || w.heart_rate_avg) ? `${w.avg_heart_rate || w.heart_rate_avg} ppm` : '-'}</td>
                    <td>
                      {w.personal_best ? (
                        <span className="table-pb-badge">🏅 PB</span>
                      ) : (
                        <span style={{ color: 'var(--text-muted)' }}>-</span>
                      )}
                    </td>
                    <td className="table-notes-cell" title={act.description || w.notes || act.notes || ''}>
                      {act.description || w.notes || act.notes || '-'}
                    </td>
                    <td>
                      <div className="table-actions-cell">
                        <button 
                          className="table-action-btn edit" 
                          onClick={() => handleOpenEdit(act)}
                          title={t('common.edit')}
                        >
                          <Edit2 size={14} />
                        </button>
                        <button 
                          className="table-action-btn delete" 
                          onClick={() => handleDelete(act.id)}
                          title={t('common.delete')}
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Modal Form (Create / Edit) */}
      <Modal 
        isOpen={isModalOpen} 
        onClose={() => {
          setIsModalOpen(false);
          setEditingWorkout(null);
        }}
        title={editingWorkout ? t('sport.editWorkoutTitle') : t('sport.createWorkoutTitle')}
      >
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label>{t('sport.fields.title')}</label>
            <input 
              type="text" 
              required
              placeholder={t('sport.titlePlaceholder')}
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('sport.fields.type')}</label>
              <select
                value={formData.workout_type}
                onChange={(e) => setFormData({ ...formData, workout_type: e.target.value })}
              >
                <option value="running">{t('sport.types.running')}</option>
                <option value="cycling">{t('sport.types.cycling')}</option>
                <option value="gym">{t('sport.types.gym')}</option>
                <option value="swimming">{t('sport.types.swimming')}</option>
                <option value="hiking">{t('sport.types.hiking')}</option>
                <option value="crossfit">{t('sport.types.crossfit')}</option>
                <option value="other">{t('sport.types.other')}</option>
              </select>
            </div>

            <div className="form-group">
              <label>{t('sport.fields.date')}</label>
              <input 
                type="date" 
                required
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('sport.fields.duration')}</label>
              <input 
                type="number" 
                min="1"
                required
                placeholder="45"
                value={formData.duration_minutes}
                onChange={(e) => setFormData({ ...formData, duration_minutes: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>{t('sport.fields.distance')}</label>
              <input 
                type="number" 
                step="0.01" 
                min="0"
                placeholder="8.5"
                value={formData.distance_km}
                onChange={(e) => setFormData({ ...formData, distance_km: e.target.value })}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('sport.fields.calories')}</label>
              <input 
                type="number" 
                min="0"
                placeholder="450"
                value={formData.calories}
                onChange={(e) => setFormData({ ...formData, calories: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>{t('sport.fields.heartRate')}</label>
              <input 
                type="number" 
                min="40" 
                max="240"
                placeholder="145"
                value={formData.avg_heart_rate}
                onChange={(e) => setFormData({ ...formData, avg_heart_rate: e.target.value })}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('sport.fields.elevation')}</label>
              <input 
                type="number" 
                min="0"
                placeholder="120"
                value={formData.elevation_m}
                onChange={(e) => setFormData({ ...formData, elevation_m: e.target.value })}
              />
            </div>

            <div className="form-group" style={{ justifyContent: 'center' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', marginTop: '1.25rem' }}>
                <input 
                  type="checkbox"
                  style={{ width: '18px', height: '18px', accentColor: 'var(--accent-emerald)' }}
                  checked={formData.personal_best}
                  onChange={(e) => setFormData({ ...formData, personal_best: e.target.checked })}
                />
                <span>{t('sport.isPBLabel')}</span>
              </label>
            </div>
          </div>

          <div className="form-group">
            <label>{t('sport.fields.notes')}</label>
            <textarea 
              placeholder={t('sport.workoutNotesPlaceholder')}
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            />
          </div>

          <div className="form-actions">
            <button 
              type="button" 
              className="btn-secondary" 
              onClick={() => {
                setIsModalOpen(false);
                setEditingWorkout(null);
              }}
            >
              {t('common.cancel')}
            </button>
            <button type="submit" className="btn-primary" disabled={submitting}>
              {submitting ? t('common.saving') : (editingWorkout ? t('common.saveChanges') : t('common.save'))}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
