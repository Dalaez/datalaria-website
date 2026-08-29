import React, { useState, useEffect } from 'react';
import { api } from '../../lib/api';
import { Modal } from '../common/Modal';
import { useLanguage } from '../../context/LanguageContext';
import { 
  Film, 
  Plus, 
  Trash2, 
  Edit2, 
  Star, 
  Tv, 
  Clapperboard, 
  Tv2, 
  Calendar,
  Sparkles,
  LayoutGrid,
  Table as TableIcon
} from 'lucide-react';
import './FilmsModule.css';

export function FilmsModule() {
  const { t, language } = useLanguage();
  const [films, setFilms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingFilm, setEditingFilm] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [viewMode, setViewMode] = useState(() => {
    return localStorage.getItem('lifeops_view_films') || 'grid';
  });

  const handleViewChange = (mode) => {
    setViewMode(mode);
    localStorage.setItem('lifeops_view_films', mode);
  };

  const defaultFormData = {
    title: '',
    media_type: 'movie',
    director: '',
    platform: 'Cine',
    genre: '',
    year: new Date().getFullYear(),
    date: new Date().toISOString().split('T')[0],
    rating: 5,
    notes: '',
  };

  const [formData, setFormData] = useState(defaultFormData);

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

  const handleOpenCreate = () => {
    setEditingFilm(null);
    setFormData(defaultFormData);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (act) => {
    setEditingFilm(act);
    const f = act.film || {};
    setFormData({
      title: act.title || '',
      media_type: f.media_type || 'movie',
      director: f.director || '',
      platform: f.platform || 'Cine',
      genre: f.genre || '',
      year: f.year || new Date().getFullYear(),
      date: act.date || new Date().toISOString().split('T')[0],
      rating: act.rating || 5,
      notes: act.description || f.review || act.notes || '',
    });
    setIsModalOpen(true);
  };

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

      if (editingFilm) {
        await api.updateFilmActivity(editingFilm.id, payload);
      } else {
        await api.createFilmActivity(payload);
      }

      setIsModalOpen(false);
      setFormData(defaultFormData);
      setEditingFilm(null);
      fetchFilms();
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
      setFilms(films.filter((f) => f.id !== id));
    } catch (err) {
      alert(`${t('common.error')}: ${err.message}`);
    }
  };

  const movieCount = films.filter((f) => f.film?.media_type === 'movie').length;
  const seriesCount = films.filter((f) => f.film?.media_type === 'series').length;
  const avgRating = films.length > 0 
    ? (films.reduce((acc, curr) => acc + (curr.rating || 0), 0) / films.length).toFixed(1)
    : '0.0';

  const getMediaIcon = (type) => {
    switch (type) {
      case 'series': return <Tv size={14} color="var(--accent-purple)" />;
      case 'anime': return <Sparkles size={14} color="var(--accent-rose)" />;
      case 'documentary': return <Tv2 size={14} color="var(--accent-cyan)" />;
      default: return <Clapperboard size={14} color="var(--accent-amber)" />;
    }
  };

  return (
    <div className="films-module">
      {/* Header */}
      <div className="module-header">
        <div>
          <h2>{t('films.title')}</h2>
          <p>{t('films.subtitle')}</p>
        </div>

        <div className="module-header-actions">
          {/* View Mode Switcher */}
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
            <span>{t('films.addFilm')}</span>
          </button>
        </div>
      </div>

      {/* Metrics Banner */}
      <div className="metrics-banner">
        <div className="metric-box">
          <span className="metric-label">{t('films.moviesWatched')}</span>
          <span className="metric-value">{movieCount} <small>films</small></span>
        </div>
        <div className="metric-box">
          <span className="metric-label">{t('films.seriesWatched')}</span>
          <span className="metric-value" style={{ color: 'var(--accent-purple)' }}>
            {seriesCount} <small>series</small>
          </span>
        </div>
        <div className="metric-box">
          <span className="metric-label">{t('films.avgRating')}</span>
          <span className="metric-value" style={{ color: '#fbbf24' }}>
            ★ {avgRating} <small>/ 5</small>
          </span>
        </div>
      </div>

      {/* Films Content */}
      {loading ? (
        <div className="loading-state">{t('films.loading')}</div>
      ) : films.length === 0 ? (
        <div className="empty-state glass-panel">
          <Film size={40} className="empty-icon" />
          <h3>{t('films.emptyTitle')}</h3>
          <p>{t('films.emptyDesc')}</p>
          <button className="btn-primary" onClick={handleOpenCreate}>
            <Plus size={16} />
            <span>{t('films.emptyAction')}</span>
          </button>
        </div>
      ) : viewMode === 'grid' ? (
        /* Cards / Grid View */
        <div className="films-grid">
          {films.map((act) => {
            const f = act.film || {};

            return (
              <div key={act.id} className="film-card glass-card">
                <div className="film-card-header">
                  <div className="media-type-chip">
                    {getMediaIcon(f.media_type)}
                    <span>{f.media_type?.toUpperCase()}</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    {f.platform && <span className="platform-chip">{f.platform}</span>}
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
      ) : (
        /* Table View */
        <div className="module-table-wrapper glass-panel">
          <table className="module-data-table">
            <thead>
              <tr>
                <th>{language === 'es' ? 'Fecha' : 'Date'}</th>
                <th>{language === 'es' ? 'Título' : 'Title'}</th>
                <th>{language === 'es' ? 'Tipo' : 'Type'}</th>
                <th>{language === 'es' ? 'Plataforma' : 'Platform'}</th>
                <th>{language === 'es' ? 'Año / Director' : 'Year / Director'}</th>
                <th>{language === 'es' ? 'Género' : 'Genre'}</th>
                <th>{language === 'es' ? 'Valoración' : 'Rating'}</th>
                <th>{language === 'es' ? 'Crítica / Notas' : 'Review / Notes'}</th>
                <th style={{ textAlign: 'right' }}>{t('common.actions')}</th>
              </tr>
            </thead>
            <tbody>
              {films.map((act) => {
                const f = act.film || {};

                return (
                  <tr key={act.id}>
                    <td className="table-date-cell">{act.date}</td>
                    <td className="table-title-cell">{act.title}</td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.8rem' }}>
                        {getMediaIcon(f.media_type)}
                        <span>{f.media_type?.toUpperCase()}</span>
                      </div>
                    </td>
                    <td>
                      {f.platform ? <span className="platform-chip">{f.platform}</span> : '-'}
                    </td>
                    <td>
                      {f.year || ''} {f.director ? `• ${f.director}` : ''}
                    </td>
                    <td>{f.genre || '-'}</td>
                    <td>
                      {act.rating ? (
                        <div style={{ display: 'flex', gap: '2px', color: '#fbbf24' }}>
                          {'★'.repeat(act.rating)}{'☆'.repeat(5 - act.rating)}
                        </div>
                      ) : '-'}
                    </td>
                    <td className="table-notes-cell" title={act.description || f.review || ''}>
                      {act.description || f.review || '-'}
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

      {/* Modal Form */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingFilm(null);
        }}
        title={editingFilm ? t('films.editFilmTitle') : t('films.createFilmTitle')}
      >
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label>{t('films.fields.title')}</label>
            <input 
              type="text" 
              required
              placeholder={t('films.titlePlaceholder')}
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('films.fields.mediaType')}</label>
              <select
                value={formData.media_type}
                onChange={(e) => setFormData({ ...formData, media_type: e.target.value })}
              >
                <option value="movie">{t('films.types.movie')}</option>
                <option value="series">{t('films.types.series')}</option>
                <option value="documentary">{t('films.types.documentary')}</option>
                <option value="anime">{t('films.types.anime')}</option>
              </select>
            </div>

            <div className="form-group">
              <label>{t('films.fields.platform')}</label>
              <select
                value={formData.platform}
                onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
              >
                <option value="Cine">🍿 Cine / Theater</option>
                <option value="Netflix">🔴 Netflix</option>
                <option value="HBO Max">🟣 HBO Max</option>
                <option value="Prime Video">🔵 Prime Video</option>
                <option value="Disney+">⭐ Disney+</option>
                <option value="Apple TV+">🍏 Apple TV+</option>
                <option value="Filmin">🟠 Filmin</option>
                <option value="Otro">🎯 Other</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('films.fields.director')}</label>
              <input 
                type="text" 
                placeholder={t('films.directorPlaceholder')}
                value={formData.director}
                onChange={(e) => setFormData({ ...formData, director: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>{t('films.fields.genre')}</label>
              <input 
                type="text" 
                placeholder={t('films.genrePlaceholder')}
                value={formData.genre}
                onChange={(e) => setFormData({ ...formData, genre: e.target.value })}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('films.fields.year')}</label>
              <input 
                type="number" 
                min="1900" 
                max="2100"
                value={formData.year}
                onChange={(e) => setFormData({ ...formData, year: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>{t('films.fields.date')}</label>
              <input 
                type="date" 
                required
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              />
            </div>
          </div>

          <div className="form-group">
            <label>{t('films.fields.rating')}</label>
            <div className="star-rating-selector">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  type="button"
                  key={star}
                  className="star-btn"
                  onClick={() => setFormData({ ...formData, rating: star })}
                >
                  <Star 
                    size={22} 
                    fill={star <= formData.rating ? '#fbbf24' : 'transparent'} 
                    color={star <= formData.rating ? '#fbbf24' : 'var(--text-muted)'} 
                  />
                </button>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label>{t('films.fields.review')}</label>
            <textarea 
              placeholder={t('films.reviewPlaceholder')}
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
                setEditingFilm(null);
              }}
            >
              {t('common.cancel')}
            </button>
            <button type="submit" className="btn-primary" disabled={submitting}>
              {submitting ? t('common.saving') : (editingFilm ? t('common.saveChanges') : t('films.addFilm'))}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
