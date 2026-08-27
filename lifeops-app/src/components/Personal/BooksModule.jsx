import React, { useState, useEffect } from 'react';
import { api } from '../../lib/api';
import { Modal } from '../common/Modal';
import { 
  BookOpen, 
  Plus, 
  Trash2, 
  Star, 
  Bookmark, 
  CheckCircle2, 
  Clock, 
  BookMarked 
} from 'lucide-react';
import './BooksModule.css';

export function BooksModule() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    title: '',
    author: '',
    date: new Date().toISOString().split('T')[0],
    pages_total: 300,
    pages_read: 0,
    status: 'reading',
    genre: '',
    rating: 5,
    notes: '',
  });

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

      await api.createBookActivity(payload);
      setIsModalOpen(false);
      setFormData({
        title: '',
        author: '',
        date: new Date().toISOString().split('T')[0],
        pages_total: 300,
        pages_read: 0,
        status: 'reading',
        genre: '',
        rating: 5,
        notes: '',
      });
      fetchBooks();
    } catch (err) {
      alert(`Error al registrar el libro: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Seguro que deseas eliminar este libro?')) return;
    try {
      await api.deleteActivity(id);
      setBooks(books.filter((b) => b.id !== id));
    } catch (err) {
      alert(`Error al eliminar: ${err.message}`);
    }
  };

  const completedBooks = books.filter((b) => b.book?.status === 'completed').length;
  const currentlyReading = books.filter((b) => b.book?.status === 'reading').length;
  const totalPagesRead = books.reduce((acc, curr) => acc + (curr.book?.pages_read || 0), 0);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return <span className="status-chip completed"><CheckCircle2 size={12} /> Leído</span>;
      case 'reading':
        return <span className="status-chip reading"><Clock size={12} /> Leyendo</span>;
      case 'wishlist':
        return <span className="status-chip wishlist"><Bookmark size={12} /> Pendiente</span>;
      default:
        return <span className="status-chip">{status}</span>;
    }
  };

  return (
    <div className="books-module">
      {/* Header */}
      <div className="module-header">
        <div>
          <h2>Biblioteca & Lecturas</h2>
          <p>Seguimiento de libros leídos, páginas y progreso de lectura.</p>
        </div>
        <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
          <Plus size={16} />
          <span>Añadir Libro</span>
        </button>
      </div>

      {/* Metrics Banner */}
      <div className="metrics-banner">
        <div className="metric-box">
          <span className="metric-label">LIBROS LEÍDOS</span>
          <span className="metric-value">{completedBooks} <small>completados</small></span>
        </div>
        <div className="metric-box">
          <span className="metric-label">LEYENDO AHORA</span>
          <span className="metric-value" style={{ color: 'var(--accent-cyan)' }}>
            {currentlyReading} <small>en curso</small>
          </span>
        </div>
        <div className="metric-box">
          <span className="metric-label">PÁGINAS LEÍDAS</span>
          <span className="metric-value" style={{ color: 'var(--accent-purple)' }}>
            {totalPagesRead.toLocaleString()} <small>págs</small>
          </span>
        </div>
      </div>

      {/* Books Grid */}
      {loading ? (
        <div className="loading-state">Cargando biblioteca...</div>
      ) : books.length === 0 ? (
        <div className="empty-state glass-panel">
          <BookMarked size={40} className="empty-icon" />
          <h3>Tu biblioteca está vacía</h3>
          <p>Registra el libro que estés leyendo actualmente o añade tu lista de deseos.</p>
          <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
            <Plus size={16} />
            <span>Añadir primer libro</span>
          </button>
        </div>
      ) : (
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
                  <button 
                    className="delete-icon-btn" 
                    onClick={() => handleDelete(act.id)}
                    title="Eliminar libro"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>

                <div className="book-details">
                  <h4 className="book-title">{act.title}</h4>
                  <span className="book-author">por {b.author || 'Autor desconocido'}</span>
                  {b.genre && <span className="genre-chip">{b.genre}</span>}
                </div>

                {/* Progress bar */}
                <div className="reading-progress-section">
                  <div className="progress-labels">
                    <span>Progreso: {percent}%</span>
                    <span>{read} / {b.pages_total || '?'} págs</span>
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
      )}

      {/* Modal Form */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Añadir Libro a la Biblioteca"
      >
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label>Título del Libro *</label>
            <input 
              type="text" 
              required
              placeholder="Ej: Hábitos Atómicos, Sapiens, Clean Architecture..."
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Autor / Autora *</label>
              <input 
                type="text" 
                required
                placeholder="Ej: James Clear"
                value={formData.author}
                onChange={(e) => setFormData({ ...formData, author: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Género</label>
              <input 
                type="text" 
                placeholder="Ej: Desarrollo Personal, Ensayo, Ciencia Ficción"
                value={formData.genre}
                onChange={(e) => setFormData({ ...formData, genre: e.target.value })}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Estado de Lectura *</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              >
                <option value="reading">📖 Leyendo Actualmente</option>
                <option value="completed">✅ Leído / Completado</option>
                <option value="wishlist">🔖 Lista de Deseos / Pendiente</option>
                <option value="abandoned">⏹️ Abandonado</option>
              </select>
            </div>

            <div className="form-group">
              <label>Valoración (1 a 5 estrellas)</label>
              <select
                value={formData.rating}
                onChange={(e) => setFormData({ ...formData, rating: e.target.value })}
              >
                <option value="5">⭐⭐⭐⭐⭐ (5 - Excelente)</option>
                <option value="4">⭐⭐⭐⭐ (4 - Muy Bueno)</option>
                <option value="3">⭐⭐⭐ (3 - Bueno)</option>
                <option value="2">⭐⭐ (2 - Regular)</option>
                <option value="1">⭐ (1 - Malo)</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Páginas Totales</label>
              <input 
                type="number" 
                min="1"
                value={formData.pages_total}
                onChange={(e) => setFormData({ ...formData, pages_total: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Páginas Leídas</label>
              <input 
                type="number" 
                min="0"
                value={formData.pages_read}
                onChange={(e) => setFormData({ ...formData, pages_read: e.target.value })}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Notas / Citas destacadas</label>
            <textarea 
              placeholder="Ideas clave del libro o reflexiones..."
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            />
          </div>

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={() => setIsModalOpen(false)}>
              Cancelar
            </button>
            <button type="submit" className="btn-primary" disabled={submitting}>
              {submitting ? 'Guardando...' : 'Añadir a la Biblioteca'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
