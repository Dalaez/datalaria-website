import React from 'react';
import { NavLink } from 'react-router-dom';
import { useLanguage } from '../../context/LanguageContext';
import { 
  LayoutDashboard, 
  User, 
  Briefcase, 
  Settings, 
  Activity, 
  BookOpen, 
  Film, 
  CheckSquare, 
  Sparkles,
  FileText,
  ChevronLeft,
  ChevronRight,
  X
} from 'lucide-react';
import './Sidebar.css';

export function Sidebar({ collapsed, toggleSidebar, mobileOpen, closeMobile }) {
  const { t, language } = useLanguage();

  const navItems = [
    { to: '/', label: t('nav.dashboard'), icon: LayoutDashboard, exact: true },
    { to: '/personal', label: t('nav.personal'), icon: User },
    { to: '/professional', label: t('nav.professional'), icon: Briefcase },
    { to: '/reports', label: t('nav.reports'), icon: FileText, badge: '.docx/.xlsx' },
    { to: '/settings', label: t('nav.settings'), icon: Settings },
  ];

  const shortcuts = [
    { to: '/personal?tab=sport', label: t('nav.sport'), icon: Activity, color: 'var(--accent-emerald)' },
    { to: '/personal?tab=books', label: t('nav.books'), icon: BookOpen, color: 'var(--accent-cyan)' },
    { to: '/personal?tab=films', label: t('nav.films'), icon: Film, color: 'var(--accent-purple)' },
    { to: '/professional?tab=tasks', label: t('nav.kanban'), icon: CheckSquare, color: 'var(--accent-amber)' },
  ];

  const handleNavClick = () => {
    if (closeMobile && window.innerWidth <= 768) {
      closeMobile();
    }
  };

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''} ${mobileOpen ? 'mobile-open' : ''}`}>
      {/* Brand Header & Toggle */}
      <div className="sidebar-brand">
        <div className="brand-logo-icon" title="LifeOps">
          <Sparkles className="icon-sparkle" size={20} />
        </div>
        {!collapsed && (
          <div className="brand-text">
            <span className="brand-title">LifeOps</span>
            <span className="brand-subtitle">Datalaria Studio</span>
          </div>
        )}

        {/* Desktop Toggle Button */}
        <button 
          type="button" 
          className="sidebar-toggle-btn desktop-only"
          onClick={toggleSidebar}
          title={collapsed 
            ? (language === 'es' ? 'Expandir menú lateral' : 'Expand sidebar') 
            : (language === 'es' ? 'Contraer menú lateral' : 'Collapse sidebar')}
        >
          {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>

        {/* Mobile Close Button */}
        <button
          type="button"
          className="sidebar-close-btn mobile-only"
          onClick={closeMobile}
          title="Cerrar menú"
        >
          <X size={18} />
        </button>
      </div>

      {/* Navigation Menu */}
      <nav className="sidebar-nav">
        {!collapsed ? (
          <div className="nav-section-label">MAIN</div>
        ) : (
          <div className="nav-section-divider" />
        )}

        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.exact}
              onClick={handleNavClick}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
              title={collapsed ? item.label : undefined}
            >
              <Icon size={18} className="nav-icon" />
              {!collapsed && <span className="nav-label">{item.label}</span>}
              {!collapsed && item.badge && <span className="nav-badge">{item.badge}</span>}
            </NavLink>
          );
        })}

        {!collapsed ? (
          <div className="nav-section-label" style={{ marginTop: '1.75rem' }}>SHORTCUTS</div>
        ) : (
          <div className="nav-section-divider" style={{ margin: '1rem 0' }} />
        )}

        <div className="quick-access-list">
          {shortcuts.map((sc) => {
            const Icon = sc.icon;
            return (
              <NavLink 
                key={sc.to} 
                to={sc.to} 
                onClick={handleNavClick}
                className="quick-item"
                title={collapsed ? sc.label : undefined}
              >
                <Icon size={15} color={sc.color} />
                {!collapsed && <span>{sc.label}</span>}
              </NavLink>
            );
          })}
        </div>
      </nav>

      {/* Footer Version Badge */}
      <div className="sidebar-footer">
        <div className="version-pill" title="LifeOps v0.1.0">
          <span className="dot-active"></span>
          {!collapsed && <span>v0.1.0 (FastAPI + React)</span>}
        </div>
      </div>
    </aside>
  );
}
