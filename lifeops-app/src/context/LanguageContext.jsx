import React, { createContext, useContext, useState, useEffect } from 'react';
import { es } from '../i18n/locales/es';
import { en } from '../i18n/locales/en';

const translations = { es, en };

const LanguageContext = createContext();

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState(() => {
    const saved = localStorage.getItem('lifeops_language');
    if (saved && (saved === 'es' || saved === 'en')) {
      return saved;
    }
    // Auto-detect browser language
    const browserLang = navigator.language?.toLowerCase() || '';
    return browserLang.startsWith('es') ? 'es' : 'en';
  });

  const setLanguage = (lang) => {
    if (lang === 'es' || lang === 'en') {
      setLanguageState(lang);
      localStorage.setItem('lifeops_language', lang);
      document.documentElement.lang = lang;
    }
  };

  const toggleLanguage = () => {
    setLanguage(language === 'es' ? 'en' : 'es');
  };

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  /**
   * Helper to retrieve translated string by dot notation path
   * e.g., t('sport.fields.title') or t('dashboard.welcome')
   */
  const t = (path, params = {}) => {
    const currentDict = translations[language] || translations.es;
    const fallbackDict = translations.es;

    const getNested = (obj, p) => {
      return p.split('.').reduce((prev, curr) => prev && prev[curr] !== undefined ? prev[curr] : undefined, obj);
    };

    let val = getNested(currentDict, path);
    if (val === undefined) {
      val = getNested(fallbackDict, path);
    }

    if (val === undefined) {
      return path; // Fallback to key
    }

    if (typeof val === 'string') {
      // Interpolate parameters like {count}
      return Object.keys(params).reduce((str, key) => {
        return str.replace(new RegExp(`\\{${key}\\}`, 'g'), params[key]);
      }, val);
    }

    return val;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, toggleLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}
