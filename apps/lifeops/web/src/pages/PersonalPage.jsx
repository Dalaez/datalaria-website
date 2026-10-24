import React from 'react';
import { useSearchParams } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { SportModule } from '../components/Personal/SportModule';
import { BooksModule } from '../components/Personal/BooksModule';
import { FilmsModule } from '../components/Personal/FilmsModule';
import { Activity, BookOpen, Film } from 'lucide-react';
import './PersonalPage.css';

export function PersonalPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const currentTab = searchParams.get('tab') || 'sport';
  const { t } = useLanguage();

  const setTab = (tab) => {
    setSearchParams({ tab });
  };

  return (
    <div className="personal-page">
      {/* Header */}
      <div className="page-header-title">
        <h1>📓 {t('nav.personal')}</h1>
        <p>{t('sport.subtitle')}</p>
      </div>

      {/* Tab Switcher */}
      <div className="tab-switcher glass-panel">
        <button 
          className={`tab-btn ${currentTab === 'sport' ? 'active' : ''}`}
          onClick={() => setTab('sport')}
        >
          <Activity size={17} />
          <span>{t('nav.sport')}</span>
        </button>

        <button 
          className={`tab-btn ${currentTab === 'books' ? 'active' : ''}`}
          onClick={() => setTab('books')}
        >
          <BookOpen size={17} />
          <span>{t('nav.books')}</span>
        </button>

        <button 
          className={`tab-btn ${currentTab === 'films' ? 'active' : ''}`}
          onClick={() => setTab('films')}
        >
          <Film size={17} />
          <span>{t('nav.films')}</span>
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
