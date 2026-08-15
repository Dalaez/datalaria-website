import React, { useEffect, useState } from 'react';
import { api } from '../../lib/api';
import { Server, Database, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-react';
import './SystemHealth.css';

export function SystemHealth() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const checkHealth = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getHealth();
      setHealth(data);
    } catch (err) {
      setError(err.message || 'Error al conectar con la API');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  return (
    <div className="system-health-widget glass-panel">
      <div className="health-header">
        <div className="health-title">
          <Server size={18} className="icon-server" />
          <span>Backend Connection</span>
        </div>
        <button onClick={checkHealth} className="refresh-btn" title="Recomprobar">
          <RefreshCw size={14} className={loading ? 'spin' : ''} />
        </button>
      </div>

      <div className="health-body">
        {loading ? (
          <p className="health-status-text muted">Verificando estado de FastAPI...</p>
        ) : error ? (
          <div className="health-alert error">
            <AlertCircle size={18} />
            <div>
              <span className="alert-title">API Offline (localhost:8000)</span>
              <span className="alert-desc">Verifica que uvicorn esté corriendo</span>
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
