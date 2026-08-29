import React, { useEffect, useState } from 'react';
import { api, API_BASE_URL } from '../../lib/api';
import { Server, Database, CheckCircle2, AlertCircle, RefreshCw, Cloud } from 'lucide-react';
import './SystemHealth.css';

export function SystemHealth() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  const checkHealth = async (isAutoRetry = false) => {
    setLoading(true);
    if (!isAutoRetry) setError(null);

    try {
      const data = await api.getHealth();
      setHealth(data);
      setError(null);
    } catch (err) {
      console.warn('Health check attempt failed:', err);
      setError(err.message || 'Error al conectar con la API');
      
      // Auto-retry up to 3 times with a 6-second delay to handle Render cold-start waking up
      if (retryCount < 3) {
        setTimeout(() => {
          setRetryCount((prev) => prev + 1);
        }, 6000);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkHealth(retryCount > 0);
  }, [retryCount]);

  const endpointLabel = API_BASE_URL.replace('https://', '').replace('http://', '');

  return (
    <div className="system-health-widget glass-panel">
      <div className="health-header">
        <div className="health-title">
          <Server size={18} className="icon-server" />
          <span>Backend Connection</span>
        </div>
        <button onClick={() => { setRetryCount(0); checkHealth(false); }} className="refresh-btn" title="Recomprobar">
          <RefreshCw size={14} className={loading ? 'spin' : ''} />
        </button>
      </div>

      <div className="health-body">
        {loading ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            <Cloud size={16} className="spin" color="var(--accent-cyan)" />
            <span>Conectando con Backend Cloud ({endpointLabel})...</span>
          </div>
        ) : error ? (
          <div className="health-alert error">
            <AlertCircle size={18} />
            <div>
              <span className="alert-title">API Offline ({endpointLabel})</span>
              <span className="alert-desc">
                {retryCount < 3 
                  ? 'La instancia gratuita de Render se está activando (Cold start)... reintentando automáticamente.'
                  : 'Pulsa el botón de refresco para volver a comprobar.'}
              </span>
            </div>
          </div>
        ) : (
          <div className="health-alert success">
            <CheckCircle2 size={18} />
            <div className="health-details">
              <span className="alert-title">
                {health?.engine} — {health?.status?.toUpperCase()}
              </span>
              <span className="alert-desc">
                <Database size={12} style={{ display: 'inline', marginRight: '4px' }} />
                {health?.database} (schema: <code>{health?.schema}</code>)
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
