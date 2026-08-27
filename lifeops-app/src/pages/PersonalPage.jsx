import React from 'react';
import { useSearchParams } from 'react-router-dom';
import { SportModule } from '../components/Personal/SportModule';
import { BooksModule } from '../components/Personal/BooksModule';
import { FilmsModule } from '../components/Personal/FilmsModule';
import { Activity, BookOpen, Film } from 'lucide-react';
import './PersonalPage.css';

export function PersonalPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const currentTab = searchParams.get('tab') || 'sport';

  const setTab = (tab) => {
    setSearchParams({ tab });
  };

  return (
    <div className="personal-page">
      {/* Header */}
      <div className="page-header-title">
        <h1>📓 Área Personal</h1>
        <p>Diario de actividad diaria, entrenamientos deportivos, libros leídos y entretenimiento.</p>
      </div>

      {/* Tab Switcher */}
      <div className="tab-switcher glass-panel">
        <button 
          className={`tab-btn ${currentTab === 'sport' ? 'active' : ''}`}
          onClick={() => setTab('sport')}
        >
          <Activity size={17} />
          <span>Deporte & Fitness</span>
        </button>

        <button 
          className={`tab-btn ${currentTab === 'books' ? 'active' : ''}`}
          onClick={() => setTab('books')}
        >
          <BookOpen size={17} />
          <span>Biblioteca & Libros</span>
        </button>

        <button 
          className={`tab-btn ${currentTab === 'films' ? 'active' : ''}`}
          onClick={() => setTab('films')}
        >
          <Film size={17} />
          <span>Cine & Series</span>
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content animate-fade-in">
        {currentTab === 'sport' && <SportModule />}
        {currentTab === 'books' && <BooksModule />}
        {currentTab === 'films' && <FilmsModule />}
      </div>
    </div>
  );
}
