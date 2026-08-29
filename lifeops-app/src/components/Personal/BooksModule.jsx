import React, { useState, useEffect } from 'react';
import { api } from '../../lib/api';
import { Modal } from '../common/Modal';
import { useLanguage } from '../../context/LanguageContext';
import { 
  BookOpen, 
  Plus, 
  Trash2, 
  Edit2, 
  Star, 
  Bookmark, 
  CheckCircle2, 
  Clock, 
  BookMarked,
  LayoutGrid,
  Table as TableIcon
} from 'lucide-react';
import './BooksModule.css';

export function BooksModule() {
  const { t, language } = useLanguage();
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingBook, setEditingBook] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [viewMode, setViewMode] = useState(() => {
    return localStorage.getItem('lifeops_view_books') || 'grid';
  });

  const handleViewChange = (mode) => {
    setViewMode(mode);
    localStorage.setItem('lifeops_view_books', mode);
  };

  const defaultFormData = {
    title: '',
    author: '',
    date: new Date().toISOString().split('T')[0],
    pages_total: 300,
    pages_read: 0,
    status: 'reading',
    genre: '',
    rating: 5,
    notes: '',
  };

  const [formData, setFormData] = useState(defaultFormData);

  const fetchBooks = async () => {
    try {
      setLoading(true);
      const data = await api.getActivitiesWithDetails('book');
      setBooks(data || []);
    } catch (err) {
      console.error('Error fetching books:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  const handleOpenCreate = () => {
    setEditingBook(null);
    setFormData(defaultFormData);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (act) => {
    setEditingBook(act);
    const b = act.book || {};
    setFormData({
      title: act.title || '',
      author: b.author || '',
      date: act.date || new Date().toISOString().split('T')[0],
      pages_total: b.pages_total || 300,
      pages_read: b.pages_read || 0,
      status: b.status || 'reading',
      genre: b.genre || '',
      rating: act.rating || 5,
      notes: act.description || act.notes || '',
    });
    setIsModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = {
        activity: {
          activity_type: 'book',
          title: formData.title,
          date: formData.date,
          rating: formData.rating ? parseInt(formData.rating) : null,
          description: formData.notes,
        },
        book: {
          author: formData.author,
          pages_total: formData.pages_total ? parseInt(formData.pages_total) : null,
          pages_read: formData.pages_read ? parseInt(formData.pages_read) : 0,
          status: formData.status,
          genre: formData.genre || null,
        },
      };

      if (editingBook) {
        await api.updateBookActivity(editingBook.id, payload);
      } else {
        await api.createBookActivity(payload);
      }

      setIsModalOpen(false);
      setFormData(defaultFormData);
      setEditingBook(null);
      fetchBooks();
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
      setBooks(books.filter((b) => b.id !== id));
    } catch (err) {
      alert(`${t('common.error')}: ${err.message}`);
    }
  };

  const completedBooks = books.filter((b) => b.book?.status === 'completed').length;
  const currentlyReading = books.filter((b) => b.book?.status === 'reading').length;
  const totalPagesRead = books.reduce((acc, curr) => acc + (curr.book?.pages_read || 0), 0);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return <span className="status-chip completed"><CheckCircle2 size={12} /> {t('books.statuses.completed')}</span>;
      case 'reading':
        return <span className="status-chip reading"><Clock size={12} /> {t('books.statuses.reading')}</span>;
      case 'wishlist':
        return <span className="status-chip wishlist"><Bookmark size={12} /> {t('books.statuses.wishlist')}</span>;
      default:
        return <span className="status-chip">{status}</span>;
    }
  };

  return (
    <div className="books-module">
      {/* Header */}
      <div className="module-header">
        <div>
          <h2>{t('books.title')}</h2>
          <p>{t('books.subtitle')}</p>
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
            <span>{t('books.addBook')}</span>
          </button>
        </div>
      </div>

      {/* Metrics Banner */}
      <div className="metrics-banner">
        <div className="metric-box">
          <span className="metric-label">{t('books.booksRead')}</span>
          <span className="metric-value">{completedBooks} <small>{t('common.all')}</small></span>
        </div>
        <div className="metric-box">
          <span className="metric-label">{t('books.readingNow')}</span>
          <span className="metric-value" style={{ color: 'var(--accent-cyan)' }}>
            {currentlyReading} <small>{t('books.statuses.reading')}</small>
          </span>
        </div>
        <div className="metric-box">
          <span className="metric-label">{t('books.pagesRead')}</span>
          <span className="metric-value" style={{ color: 'var(--accent-purple)' }}>
            {totalPagesRead.toLocaleString()} <small>p.</small>
          </span>
        </div>
      </div>

      {/* Books Content */}
      {loading ? (
        <div className="loading-state">{t('books.loading')}</div>
      ) : books.length === 0 ? (
        <div className="empty-state glass-panel">
          <BookMarked size={40} className="empty-icon" />
          <h3>{t('books.emptyTitle')}</h3>
          <p>{t('books.emptyDesc')}</p>
          <button className="btn-primary" onClick={handleOpenCreate}>
            <Plus size={16} />
            <span>{t('books.emptyAction')}</span>
          </button>
        </div>
      ) : viewMode === 'grid' ? (
        /* Cards / Grid View */
        <div className="books-grid">
          {books.map((act) => {
            const b = act.book || {};
            const total = b.pages_total || 1;
            const read = b.pages_read || 0;
            const percent = Math.min(100, Math.round((read / total) * 100));

            return (
              <div key={act.id} className="book-card glass-card">
                <div className="book-card-header">
                  {getStatusBadge(b.status)}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
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

                <div className="book-details">
                  <h4 className="book-title">{act.title}</h4>
                  <span className="book-author">by {b.author || 'Unknown'}</span>
                  {b.genre && <span className="genre-chip">{b.genre}</span>}
                </div>

                {/* Progress bar */}
                <div className="reading-progress-section">
                  <div className="progress-labels">
                    <span>{t('books.progress')}: {percent}%</span>
                    <span>{read} / {b.pages_total || '?'} {t('common.pills')}</span>
                  </div>
                  <div className="progress-track">
                    <div 
                      className="progress-fill" 
                      style={{ width: `${percent}%` }} 
                    />
                  </div>
                </div>

                {/* Rating stars */}
                {act.rating && (
                  <div className="rating-stars">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <Star 
                        key={star} 
                        size={14} 
                        fill={star <= act.rating ? '#fbbf24' : 'transparent'} 
                        color={star <= act.rating ? '#fbbf24' : 'var(--text-muted)'} 
                      />
                    ))}
                  </div>
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
                <th>{language === 'es' ? 'Autor' : 'Author'}</th>
                <th>{language === 'es' ? 'Género' : 'Genre'}</th>
                <th>{language === 'es' ? 'Páginas' : 'Pages'}</th>
                <th>{language === 'es' ? 'Progreso' : 'Progress'}</th>
                <th>{language === 'es' ? 'Estado' : 'Status'}</th>
                <th>{language === 'es' ? 'Valoración' : 'Rating'}</th>
                <th style={{ textAlign: 'right' }}>{t('common.actions')}</th>
              </tr>
            </thead>
            <tbody>
              {books.map((act) => {
                const b = act.book || {};
                const total = b.pages_total || 1;
                const read = b.pages_read || 0;
                const percent = Math.min(100, Math.round((read / total) * 100));

                return (
                  <tr key={act.id}>
                    <td className="table-date-cell">{act.date}</td>
                    <td className="table-title-cell">{act.title}</td>
                    <td>{b.author || '-'}</td>
                    <td>{b.genre || '-'}</td>
                    <td>{read} / {b.pages_total || '?'}</td>
                    <td>
                      <div className="table-progress-box">
                        <div className="table-mini-track">
                          <div className="table-mini-fill" style={{ width: `${percent}%` }} />
                        </div>
                        <span className="table-progress-pct">{percent}%</span>
                      </div>
                    </td>
                    <td>{getStatusBadge(b.status)}</td>
                    <td>
                      {act.rating ? (
                        <div style={{ display: 'flex', gap: '2px', color: '#fbbf24' }}>
                          {'★'.repeat(act.rating)}{'☆'.repeat(5 - act.rating)}
                        </div>
                      ) : '-'}
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
          setEditingBook(null);
        }}
        title={editingBook ? t('books.editBookTitle') : t('books.createBookTitle')}
      >
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label>{t('books.fields.title')}</label>
            <input 
              type="text" 
              required
              placeholder={t('books.titlePlaceholder')}
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('books.fields.author')}</label>
              <input 
                type="text" 
                required
                placeholder={t('books.authorPlaceholder')}
                value={formData.author}
                onChange={(e) => setFormData({ ...formData, author: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>{t('books.fields.genre')}</label>
              <input 
                type="text" 
                placeholder={t('books.genrePlaceholder')}
                value={formData.genre}
                onChange={(e) => setFormData({ ...formData, genre: e.target.value })}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('books.fields.status')}</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              >
                <option value="reading">{t('books.statuses.reading')}</option>
                <option value="completed">{t('books.statuses.completed')}</option>
                <option value="wishlist">{t('books.statuses.wishlist')}</option>
                <option value="abandoned">{t('books.statuses.abandoned')}</option>
              </select>
            </div>

            <div className="form-group">
              <label>{t('books.fields.date')}</label>
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
              <label>{t('books.fields.pagesRead')}</label>
              <input 
                type="number" 
                min="0"
                placeholder="0"
                value={formData.pages_read}
                onChange={(e) => setFormData({ ...formData, pages_read: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>{t('books.fields.pagesTotal')}</label>
              <input 
                type="number" 
                min="1"
                placeholder="320"
                value={formData.pages_total}
                onChange={(e) => setFormData({ ...formData, pages_total: e.target.value })}
              />
            </div>
          </div>

          <div className="form-group">
            <label>{t('books.fields.rating')}</label>
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
            <label>{t('books.fields.notes')}</label>
            <textarea 
              placeholder={t('books.notesPlaceholder')}
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
                setEditingBook(null);
              }}
            >
              {t('common.cancel')}
            </button>
            <button type="submit" className="btn-primary" disabled={submitting}>
              {submitting ? t('common.saving') : (editingBook ? t('common.saveChanges') : t('books.addBook'))}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
