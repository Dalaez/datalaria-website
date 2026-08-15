import React from 'react';
import { NavLink } from 'react-router-dom';
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
  Sparkles 
} from 'lucide-react';
import './Sidebar.css';

export function Sidebar() {
  const navItems = [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard, exact: true },
    { to: '/personal', label: 'Área Personal', icon: User, badge: 'Diario' },
    { to: '/professional', label: 'Área Profesional', icon: Briefcase, badge: 'Proyectos' },
    { to: '/stats', label: 'Estadísticas', icon: BarChart3 },
    { to: '/settings', label: 'Ajustes', icon: Settings },
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
        <div className="nav-section-label">PRINCIPAL</div>
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

        <div className="nav-section-label" style={{ marginTop: '1.75rem' }}>ACCESOS RÁPIDOS</div>
        <div className="quick-access-list">
          <NavLink to="/personal?tab=sport" className="quick-item">
            <Activity size={15} color="var(--accent-emerald)" />
            <span>Deporte & Fitness</span>
          </NavLink>
          <NavLink to="/personal?tab=books" className="quick-item">
            <BookOpen size={15} color="var(--accent-cyan)" />
            <span>Lecturas</span>
          </NavLink>
          <NavLink to="/personal?tab=films" className="quick-item">
            <Film size={15} color="var(--accent-purple)" />
            <span>Cine & Series</span>
          </NavLink>
          <NavLink to="/professional?tab=tasks" className="quick-item">
            <CheckSquare size={15} color="var(--accent-amber)" />
            <span>Tareas Pendientes</span>
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
