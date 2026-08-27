import React, { useState, useEffect } from 'react';
import { api } from '../../lib/api';
import { Modal } from '../common/Modal';
import { 
  Activity, 
  Plus, 
  Trash2, 
  Award, 
  Flame, 
  Heart, 
  Clock, 
  Navigation, 
  TrendingUp,
  Dumbbell,
  Bike
} from 'lucide-react';
import './SportModule.css';

export function SportModule() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
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
  });

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
          distance_km: formData.distance_km ? parseFloat(formData.distance_km) : null,
          calories: formData.calories ? parseInt(formData.calories) : null,
          avg_heart_rate: formData.avg_heart_rate ? parseInt(formData.avg_heart_rate) : null,
          elevation_m: formData.elevation_m ? parseInt(formData.elevation_m) : null,
          personal_best: formData.personal_best,
          notes: formData.notes,
        },
      };

      await api.createSportActivity(payload);
      setIsModalOpen(false);
      // Reset form
      setFormData({
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
      });
      fetchWorkouts();
    } catch (err) {
      alert(`Error al registrar el entrenamiento: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Seguro que deseas eliminar este entrenamiento?')) return;
    try {
      await api.deleteActivity(id);
      setWorkouts(workouts.filter((w) => w.id !== id));
    } catch (err) {
      alert(`Error al eliminar: ${err.message}`);
    }
  };

  // Aggregated KPIs
  const totalKm = workouts.reduce((acc, curr) => acc + (curr.workout?.distance_km || 0), 0);
  const totalCalories = workouts.reduce((acc, curr) => acc + (curr.workout?.calories || 0), 0);
  const totalMinutes = workouts.reduce((acc, curr) => acc + (curr.duration_minutes || 0), 0);
  const totalPBs = workouts.filter((w) => w.workout?.personal_best).length;

  const getSportIcon = (type) => {
    switch (type?.toLowerCase()) {
      case 'running': return <Activity size={18} color="var(--accent-emerald)" />;
      case 'cycling': return <Bike size={18} color="var(--accent-cyan)" />;
      case 'gym': return <Dumbbell size={18} color="var(--accent-purple)" />;
      default: return <Activity size={18} color="var(--accent-amber)" />;
    }
  };

  return (
    <div className="sport-module">
      {/* Top Action Bar */}
      <div className="module-header">
        <div>
          <h2>Entrenamientos & Rendimiento</h2>
          <p>Registra y analiza tus sesiones de running, ciclismo, fuerza y más.</p>
        </div>
        <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
          <Plus size={16} />
          <span>Registrar Entrenamiento</span>
        </button>
      </div>

      {/* Metrics Banner */}
      <div className="metrics-banner">
        <div className="metric-box">
          <span className="metric-label">DISTANCIA TOTAL</span>
          <span className="metric-value">{totalKm.toFixed(1)} <small>km</small></span>
        </div>
        <div className="metric-box">
          <span className="metric-label">TIEMPO TOTAL</span>
          <span className="metric-value">{(totalMinutes / 60).toFixed(1)} <small>hrs</small></span>
        </div>
        <div className="metric-box">
          <span className="metric-label">CALORÍAS</span>
          <span className="metric-value">{totalCalories.toLocaleString()} <small>kcal</small></span>
        </div>
        <div className="metric-box">
          <span className="metric-label">RÉCORDS (PB)</span>
          <span className="metric-value">{totalPBs} <small>medallas</small></span>
        </div>
      </div>

      {/* Workouts List */}
      {loading ? (
        <div className="loading-state">Cargando entrenamientos...</div>
      ) : workouts.length === 0 ? (
        <div className="empty-state glass-panel">
          <Activity size={40} className="empty-icon" />
          <h3>No hay entrenamientos registrados</h3>
          <p>Comienza registrando tu primera carrera, sesión de gimnasio o salida en bici.</p>
          <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
            <Plus size={16} />
            <span>Añadir primer entrenamiento</span>
          </button>
        </div>
      ) : (
        <div className="workouts-grid">
          {workouts.map((act) => {
            const w = act.workout || {};
            return (
              <div key={act.id} className="workout-card glass-card">
                <div className="workout-card-top">
                  <div className="workout-type-badge">
                    {getSportIcon(w.workout_type)}
                    <span className="type-name">{w.workout_type?.toUpperCase()}</span>
                  </div>
                  <div className="card-top-right">
                    {w.personal_best && (
                      <span className="pb-badge" title="Récord personal">
                        <Award size={14} /> PB
                      </span>
                    )}
                    <button 
                      className="delete-icon-btn" 
                      onClick={() => handleDelete(act.id)}
                      title="Eliminar sesión"
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
                      <span>{w.distance_km} km</span>
                    </div>
                  )}
                  {act.duration_minutes != null && (
                    <div className="stat-chip">
                      <Clock size={13} />
                      <span>{act.duration_minutes} min</span>
                    </div>
                  )}
                  {w.calories != null && (
                    <div className="stat-chip">
                      <Flame size={13} />
                      <span>{w.calories} kcal</span>
                    </div>
                  )}
                  {w.avg_heart_rate != null && (
                    <div className="stat-chip">
                      <Heart size={13} />
                      <span>{w.avg_heart_rate} ppm</span>
                    </div>
                  )}
                  {w.elevation_m != null && (
                    <div className="stat-chip">
                      <TrendingUp size={13} />
                      <span>+{w.elevation_m}m</span>
                    </div>
                  )}
                </div>

                {w.notes && <p className="workout-notes">{w.notes}</p>}
              </div>
            );
          })}
        </div>
      )}

      {/* Modal Form */}
      <Modal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)}
        title="Registrar Sesión de Entrenamiento"
      >
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label>Título del Entrenamiento *</label>
            <input 
              type="text" 
              required
              placeholder="Ej: Carrera 10k ritmo suave, Pierna en gimnasio..."
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Deporte *</label>
              <select
                value={formData.workout_type}
                onChange={(e) => setFormData({ ...formData, workout_type: e.target.value })}
              >
                <option value="running">🏃 Running / Carrera</option>
                <option value="cycling">🚴 Ciclismo</option>
                <option value="gym">🏋️ Gimnasio / Fuerza</option>
                <option value="swimming">🏊 Natación</option>
                <option value="hiking">🥾 Senderismo</option>
                <option value="crossfit">⚡ CrossFit</option>
                <option value="other">🎯 Otro</option>
              </select>
            </div>

            <div className="form-group">
              <label>Fecha *</label>
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
              <label>Duración (minutos) *</label>
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
              <label>Distancia (km)</label>
              <input 
                type="number" 
                step="0.01" 
                min="0"
                placeholder="Ej: 8.5"
                value={formData.distance_km}
                onChange={(e) => setFormData({ ...formData, distance_km: e.target.value })}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Calorías (kcal)</label>
              <input 
                type="number" 
                min="0"
                placeholder="Ej: 450"
                value={formData.calories}
                onChange={(e) => setFormData({ ...formData, calories: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>FC Media (ppm)</label>
              <input 
                type="number" 
                min="40" 
                max="240"
                placeholder="Ej: 145"
                value={formData.avg_heart_rate}
                onChange={(e) => setFormData({ ...formData, avg_heart_rate: e.target.value })}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Desnivel positivo (m)</label>
              <input 
                type="number" 
                min="0"
                placeholder="Ej: 120"
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
                <span>🏅 ¿Marca personal / Récord?</span>
              </label>
            </div>
          </div>

          <div className="form-group">
            <label>Notas / Sensaciones</label>
            <textarea 
              placeholder="Sensaciones, climatología, ruta..."
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            />
          </div>

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={() => setIsModalOpen(false)}>
              Cancelar
            </button>
            <button type="submit" className="btn-primary" disabled={submitting}>
              {submitting ? 'Guardando...' : 'Guardar Entrenamiento'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
