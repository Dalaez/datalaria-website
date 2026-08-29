import React from 'react';
import { NavLink } from 'react-router-dom';
import { useLanguage } from '../../context/LanguageContext';
import { 
  LayoutDashboard, 
  User, 
  Briefcase, 
  BarChart3, 
  Settings, 
  Activity, 
  BookOpen, 
  Film, 
  CheckSquare, 
  Sparkles,
  FileText 
} from 'lucide-react';
import './Sidebar.css';

export function Sidebar() {
  const { t } = useLanguage();

  const navItems = [
    { to: '/', label: t('nav.dashboard'), icon: LayoutDashboard, exact: true },
    { to: '/personal', label: t('nav.personal'), icon: User },
    { to: '/professional', label: t('nav.professional'), icon: Briefcase },
    { to: '/reports', label: t('nav.reports'), icon: FileText, badge: '.docx/.xlsx' },
    { to: '/settings', label: t('nav.settings'), icon: Settings },
  ];

  return (
    <aside className="sidebar">
      {/* Brand Header */}
      <div className="sidebar-brand">
        <div className="brand-logo-icon">
          <Sparkles className="icon-sparkle" size={20} />
        </div>
        <div className="brand-text">
          <span className="brand-title">LifeOps</span>
          <span className="brand-subtitle">Datalaria Studio</span>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="sidebar-nav">
        <div className="nav-section-label">MAIN</div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.exact}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon size={18} className="nav-icon" />
              <span className="nav-label">{item.label}</span>
              {item.badge && <span className="nav-badge">{item.badge}</span>}
            </NavLink>
          );
        })}

        <div className="nav-section-label" style={{ marginTop: '1.75rem' }}>SHORTCUTS</div>
        <div className="quick-access-list">
          <NavLink to="/personal?tab=sport" className="quick-item">
            <Activity size={15} color="var(--accent-emerald)" />
            <span>{t('nav.sport')}</span>
          </NavLink>
          <NavLink to="/personal?tab=books" className="quick-item">
            <BookOpen size={15} color="var(--accent-cyan)" />
            <span>{t('nav.books')}</span>
          </NavLink>
          <NavLink to="/personal?tab=films" className="quick-item">
            <Film size={15} color="var(--accent-purple)" />
            <span>{t('nav.films')}</span>
          </NavLink>
          <NavLink to="/professional?tab=tasks" className="quick-item">
            <CheckSquare size={15} color="var(--accent-amber)" />
            <span>{t('nav.kanban')}</span>
          </NavLink>
        </div>
      </nav>

      {/* Footer Version Badge */}
      <div className="sidebar-footer">
        <div className="version-pill">
          <span className="dot-active"></span>
          <span>v0.1.0 (FastAPI + React)</span>
        </div>
      </div>
    </aside>
  );
}
