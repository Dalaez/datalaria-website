import React from 'react';
import { useLanguage } from '../../context/LanguageContext';
import { Globe } from 'lucide-react';
import './LanguageSwitcher.css';

export function LanguageSwitcher({ compact = false }) {
  const { language, toggleLanguage, setLanguage } = useLanguage();

  return (
    <div className={`language-switcher-pill ${compact ? 'compact' : ''}`} title="Cambiar Idioma / Change Language">
      <button 
        type="button"
        className={`lang-option-btn ${language === 'es' ? 'active' : ''}`}
        onClick={() => setLanguage('es')}
      >
        <span className="flag-emoji">🇪🇸</span>
        <span className="lang-code">ES</span>
      </button>
      <div className="lang-divider" />
      <button 
        type="button"
        className={`lang-option-btn ${language === 'en' ? 'active' : ''}`}
        onClick={() => setLanguage('en')}
      >
        <span className="flag-emoji">🇬🇧</span>
        <span className="lang-code">EN</span>
      </button>
    </div>
  );
}
