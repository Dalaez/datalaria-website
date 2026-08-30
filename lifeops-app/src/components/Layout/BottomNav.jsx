import React from 'react';
import { NavLink } from 'react-router-dom';
import { useLanguage } from '../../context/LanguageContext';
import { 
  LayoutDashboard, 
  User, 
  Briefcase, 
  FileText, 
  Settings 
} from 'lucide-react';
import './BottomNav.css';

export function BottomNav() {
  const { t } = useLanguage();

  const navItems = [
    { to: '/', label: t('nav.dashboard'), icon: LayoutDashboard, exact: true },
    { to: '/personal', label: t('nav.personal'), icon: User },
    { to: '/professional', label: t('nav.professional'), icon: Briefcase },
    { to: '/reports', label: t('nav.reports'), icon: FileText },
    { to: '/settings', label: t('nav.settings'), icon: Settings },
  ];

  return (
    <nav className="mobile-bottom-nav">
      {navItems.map((item) => {
        const Icon = item.icon;
        return (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.exact}
            className={({ isActive }) => `bottom-nav-item ${isActive ? 'active' : ''}`}
          >
            <div className="bottom-nav-icon-wrapper">
              <Icon size={20} />
            </div>
            <span className="bottom-nav-label">{item.label}</span>
          </NavLink>
        );
      })}
    </nav>
  );
}
