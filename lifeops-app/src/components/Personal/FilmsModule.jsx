import React, { useState, useEffect } from 'react';
import { api } from '../../lib/api';
import { Modal } from '../common/Modal';
import { 
  Film, 
  Plus, 
  Trash2, 
  Star, 
  Tv, 
  Clapperboard, 
  Tv2, 
  Calendar,
  Sparkles
} from 'lucide-react';
import './FilmsModule.css';

export function FilmsModule() {
  const [films, setFilms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    title: '',
    media_type: 'movie',
    director: '',
    platform: 'Cine',
    genre: '',
    year: new Date().getFullYear(),
    date: new Date().toISOString().split('T')[0],
    rating: 5,
    notes: '',
  });

  const fetchFilms = async () => {
    try {
      setLoading(true);
      const data = await api.getActivitiesWithDetails('film');
      setFilms(data || []);
    } catch (err) {
      console.error('Error fetching films:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFilms();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = {
        activity: {
          activity_type: 'film',
          title: formData.title,
          date: formData.date,
          rating: formData.rating ? parseInt(formData.rating) : null,
          description: formData.notes,
        },
        film: {
          media_type: formData.media_type,
          director: formData.director || null,
          platform: formData.platform || null,
          genre: formData.genre || null,
          year: formData.year ? parseInt(formData.year) : null,
        },
      };

      await api.createFilmActivity(payload);
      setIsModalOpen(false);
      setFormData({
        title: '',
        media_type: 'movie',
        director: '',
        platform: 'Cine',
        genre: '',
        year: new Date().getFullYear(),
        date: new Date().toISOString().split('T')[0],
        rating: 5,
        notes: '',
      });
      fetchFilms();
    } catch (err) {
      alert(`Error al registrar el título: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Seguro que deseas eliminar esta película o serie?')) return;
    try {
      await api.deleteActivity(id);
      setFilms(films.filter((f) => f.id !== id));
    } catch (err) {
      alert(`Error al eliminar: ${err.message}`);
    }
  };

  const totalMovies = films.filter((f) => f.film?.media_type === 'movie').length;
  const totalSeries = films.filter((f) => f.film?.media_type === 'series').length;
  const avgRating = films.length > 0 
    ? (films.reduce((acc, curr) => acc + (curr.rating || 0), 0) / films.length).toFixed(1)
    : '0.0';

  const getMediaIcon = (type) => {
    switch (type) {
      case 'series': return <Tv size={14} />;
      case 'documentary': return <Clapperboard size={14} />;
      case 'anime': return <Sparkles size={14} />;
      default: return <Film size={14} />;
    }
  };

  return (
    <div className="films-module">
      {/* Header */}
      <div className="module-header">
        <div>
          <h2>Cine, Series & Cultura</h2>
          <p>Catálogo y valoraciones de películas, series y documentales vistos.</p>
        </div>
        <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
          <Plus size={16} />
          <span>Registrar Película / Serie</span>
        </button>
      </div>

      {/* Metrics Banner */}
      <div className="metrics-banner">
        <div className="metric-box">
          <span className="metric-label">PELÍCULAS VISTAS</span>
          <span className="metric-value">{totalMovies} <small>films</small></span>
        </div>
        <div className="metric-box">
          <span className="metric-label">SERIES / ANIME</span>
          <span className="metric-value" style={{ color: 'var(--accent-purple)' }}>
            {totalSeries} <small>temporadas</small>
          </span>
        </div>
        <div className="metric-box">
          <span className="metric-label">VALORACIÓN MEDIA</span>
          <span className="metric-value" style={{ color: '#fbbf24' }}>
            ★ {avgRating} <small>/ 5</small>
          </span>
        </div>
      </div>

      {/* Films Grid */}
      {loading ? (
        <div className="loading-state">Cargando catálogo...</div>
      ) : films.length === 0 ? (
        <div className="empty-state glass-panel">
          <Film size={40} className="empty-icon" />
          <h3>No has registrado películas o series</h3>
          <p>Lleva un registro de tus películas favoritas, estrenos de cine o series maratoneadas.</p>
          <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
            <Plus size={16} />
            <span>Añadir primer título</span>
          </button>
        </div>
      ) : (
        <div className="films-grid">
          {films.map((act) => {
            const f = act.film || {};
            return (
              <div key={act.id} className="film-card glass-card">
                <div className="film-card-header">
                  <div className="media-type-badge">
                    {getMediaIcon(f.media_type)}
                    <span>{f.media_type?.toUpperCase()}</span>
                  </div>

                  <div className="film-card-actions">
                    {f.platform && <span className="platform-chip">{f.platform}</span>}
                    <button 
                      className="delete-icon-btn" 
                      onClick={() => handleDelete(act.id)}
                      title="Eliminar registro"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>

                <div className="film-body">
                  <h4 className="film-title">{act.title}</h4>
                  <div className="film-meta">
                    {f.year && <span>{f.year}</span>}
                    {f.director && <span>• Dir: {f.director}</span>}
                    {f.genre && <span>• {f.genre}</span>}
                  </div>
                </div>

                <div className="film-card-footer">
                  <div className="rating-stars">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <Star 
                        key={star} 
                        size={13} 
                        fill={star <= (act.rating || 0) ? '#fbbf24' : 'transparent'} 
                        color={star <= (act.rating || 0) ? '#fbbf24' : 'var(--text-muted)'} 
                      />
                    ))}
                  </div>
                  <span className="film-date">{act.date}</span>
                </div>

                {act.description && (
                  <p className="film-review">"{act.description}"</p>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Modal Form */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Registrar Película o Serie"
      >
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label>Título *</label>
            <input 
              type="text" 
              required
              placeholder="Ej: Oppenheimer, Dune 2, Succession, Shingeki no Kyojin..."
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Tipo de Contenido *</label>
              <select
                value={formData.media_type}
                onChange={(e) => setFormData({ ...formData, media_type: e.target.value })}
              >
                <option value="movie">🎬 Película</option>
                <option value="series">📺 Serie de TV</option>
                <option value="documentary">📽️ Documental</option>
                <option value="anime">✨ Anime</option>
              </select>
            </div>

            <div className="form-group">
              <label>Plataforma / Medio</label>
              <select
                value={formData.platform}
                onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
              >
                <option value="Cine">🍿 Cine / Sala</option>
                <option value="Netflix">🔴 Netflix</option>
                <option value="HBO Max">🟣 HBO Max</option>
                <option value="Prime Video">🔵 Prime Video</option>
                <option value="Disney+">🟦 Disney+</option>
                <option value="Apple TV+">⚪ Apple TV+</option>
                <option value="Filmin">🟠 Filmin</option>
                <option value="Otro">Otro</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Director / Creador</label>
              <input 
                type="text" 
                placeholder="Ej: Christopher Nolan"
                value={formData.director}
                onChange={(e) => setFormData({ ...formData, director: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Género</label>
              <input 
                type="text" 
                placeholder="Ej: Thriller, Ciencia Ficción, Drama..."
                value={formData.genre}
                onChange={(e) => setFormData({ ...formData, genre: e.target.value })}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Año de estreno</label>
              <input 
                type="number" 
                min="1900" 
                max="2030"
                value={formData.year}
                onChange={(e) => setFormData({ ...formData, year: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Valoración</label>
              <select
                value={formData.rating}
                onChange={(e) => setFormData({ ...formData, rating: e.target.value })}
              >
                <option value="5">⭐⭐⭐⭐⭐ (5 - Obra Maestra)</option>
                <option value="4">⭐⭐⭐⭐ (4 - Muy Buena)</option>
                <option value="3">⭐⭐⭐ (3 - Entretenida)</option>
                <option value="2">⭐⭐ (2 - Prescindible)</option>
                <option value="1">⭐ (1 - Mala)</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>Fecha de visionado</label>
            <input 
              type="date" 
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
            />
          </div>

          <div className="form-group">
            <label>Reseña o comentario</label>
            <textarea 
              placeholder="¿Qué te pareció el final? Actuaciones destacadas, fotografía..."
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            />
          </div>

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={() => setIsModalOpen(false)}>
              Cancelar
            </button>
            <button type="submit" className="btn-primary" disabled={submitting}>
              {submitting ? 'Guardando...' : 'Registrar'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
