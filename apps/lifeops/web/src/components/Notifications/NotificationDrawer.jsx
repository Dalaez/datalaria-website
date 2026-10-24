import React, { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../../context/LanguageContext';
import { 
  Bell, 
  AlertTriangle, 
  AlertCircle, 
  Info, 
  CheckCircle2, 
  X, 
  ExternalLink,
  Sparkles
} from 'lucide-react';
import './NotificationDrawer.css';

export function NotificationDrawer({ isOpen, onClose, alerts = [], onDismiss }) {
  const drawerRef = useRef(null);
  const navigate = useNavigate();
  const { t } = useLanguage();

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (drawerRef.current && !drawerRef.current.contains(e.target)) {
        onClose();
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleAction = (url) => {
    onClose();
    if (url) navigate(url);
  };

  const getSeverityIcon = (sev) => {
    switch (sev) {
      case 'critical':
        return <AlertCircle size={16} color="var(--accent-rose)" />;
      case 'warning':
        return <AlertTriangle size={16} color="var(--accent-amber)" />;
      default:
        return <Info size={16} color="var(--accent-cyan)" />;
    }
  };

  return (
    <div className="notification-drawer glass-panel" ref={drawerRef}>
      <div className="notif-header">
        <div className="notif-title-group">
          <Bell size={16} color="var(--accent-emerald)" />
          <h4>{t('notifications.title')}</h4>
          <span className="notif-count-pill">{alerts.length}</span>
        </div>
        <button className="notif-close-btn" onClick={onClose}>
          <X size={16} />
        </button>
      </div>

      <div className="notif-body">
        {alerts.length === 0 ? (
          <div className="notif-empty">
            <CheckCircle2 size={32} color="var(--accent-emerald)" className="empty-check-icon" />
            <h5>{t('notifications.noAlerts')}</h5>
            <p>{t('notifications.allCaughtUp')}</p>
          </div>
        ) : (
          <div className="notif-list">
            {alerts.map((a) => (
              <div key={a.id} className={`notif-card ${a.severity}`}>
                <div className="notif-card-top">
                  <div className="notif-card-title-row">
                    {getSeverityIcon(a.severity)}
                    <span className="notif-item-title">{a.title}</span>
                  </div>
                  <button 
                    className="notif-dismiss-btn" 
                    onClick={() => onDismiss(a.id)}
                    title={t('notifications.dismiss')}
                  >
                    <X size={13} />
                  </button>
                </div>

                <p className="notif-item-desc">{a.message}</p>

                {a.action_url && (
                  <button 
                    className="notif-action-btn"
                    onClick={() => handleAction(a.action_url)}
                  >
                    <span>{a.action_label || 'Ver detalles'}</span>
                    <ExternalLink size={12} />
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
