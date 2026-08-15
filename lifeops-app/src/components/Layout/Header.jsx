import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { LogOut, User, Bell, Search, ShieldCheck } from 'lucide-react';
import './Header.css';

export function Header() {
  const { user, signOut } = useAuth();

  const handleLogout = async () => {
    try {
      await signOut();
    } catch (err) {
      console.error('Logout error:', err);
    }
  };

  const userEmail = user?.email || 'Usuario';
  const userInitial = userEmail.charAt(0).toUpperCase();

  return (
    <header className="app-header">
      {/* Search Bar / Status */}
      <div className="header-left">
        <div className="header-search">
          <Search size={16} className="search-icon" />
          <input type="text" placeholder="Buscar actividades, tareas, proyectos..." />
        </div>
      </div>

      {/* User & Actions */}
      <div className="header-right">
        {/* Connection Status Pill */}
        <div className="status-pill">
          <ShieldCheck size={14} color="var(--accent-emerald)" />
          <span>Supabase Auth</span>
        </div>

        {/* Notifications Icon */}
        <button className="header-icon-btn" title="Notificaciones">
          <Bell size={18} />
          <span className="notif-dot"></span>
        </button>

        <div className="header-divider"></div>

        {/* User Profile Menu */}
        <div className="user-profile-widget">
          <div className="user-avatar">{userInitial}</div>
          <div className="user-info">
            <span className="user-email">{userEmail}</span>
            <span className="user-role">Administrador</span>
          </div>

          <button onClick={handleLogout} className="logout-btn" title="Cerrar Sesión">
            <LogOut size={16} />
          </button>
        </div>
      </div>
    </header>
  );
}
