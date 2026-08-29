import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';
import { api } from '../../lib/api';
import { NotificationDrawer } from '../Notifications/NotificationDrawer';
import { LanguageSwitcher } from '../common/LanguageSwitcher';
import { LogOut, User, Bell, Search, ShieldCheck } from 'lucide-react';
import './Header.css';

export function Header() {
  const { user, signOut } = useAuth();
  const { t } = useLanguage();
  const [alerts, setAlerts] = useState([]);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  const fetchAlerts = async () => {
    try {
      const data = await api.getAlerts();
      setAlerts(data || []);
    } catch (err) {
      console.error('Error fetching alerts:', err);
    }
  };

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 60000); // Poll every minute
    return () => clearInterval(interval);
  }, []);

  const handleDismiss = async (alertId) => {
    try {
      await api.dismissAlert(alertId);
      setAlerts((prev) => prev.filter((a) => a.id !== alertId));
    } catch (err) {
      console.error('Error dismissing alert:', err);
    }
  };

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
          <input type="text" placeholder={t('header.search')} />
        </div>
      </div>

      {/* User & Actions */}
      <div className="header-right" style={{ position: 'relative' }}>
        {/* Multilingual Switcher */}
        <LanguageSwitcher />

        {/* Connection Status Pill */}
        <div className="status-pill">
          <ShieldCheck size={14} color="var(--accent-emerald)" />
          <span>Supabase Auth</span>
        </div>

        {/* Notifications Icon & Drawer */}
        <div style={{ position: 'relative' }}>
          <button 
            className="header-icon-btn" 
            title={t('header.notifications')}
            onClick={() => setIsDrawerOpen(!isDrawerOpen)}
          >
            <Bell size={18} />
            {alerts.length > 0 && (
              <span className="notif-dot" title={`${alerts.length} alertas pendientes`}>
                {alerts.length}
              </span>
            )}
          </button>

          <NotificationDrawer 
            isOpen={isDrawerOpen}
            onClose={() => setIsDrawerOpen(false)}
            alerts={alerts}
            onDismiss={handleDismiss}
          />
        </div>

        <div className="header-divider"></div>

        {/* User Profile Menu */}
        <div className="user-profile-widget">
          <div className="user-avatar">{userInitial}</div>
          <div className="user-info">
            <span className="user-email">{userEmail}</span>
            <span className="user-role">LifeOps</span>
          </div>

          <button onClick={handleLogout} className="logout-btn" title={t('nav.logout')}>
            <LogOut size={16} />
          </button>
        </div>
      </div>
    </header>
  );
}
