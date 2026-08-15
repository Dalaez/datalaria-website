import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Settings, Shield, Server, Database, User } from 'lucide-react';

export function SettingsPage() {
  const { user } = useAuth();

  return (
    <div className="settings-page">
      <div className="page-header-title">
        <h1>⚙️ Ajustes & Configuración</h1>
        <p>Parámetros de conexión del sistema, datos de cuenta e información del servidor.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '1.5rem' }}>
        {/* Account Info */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
            <User size={20} color="var(--accent-emerald)" />
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.1rem', fontWeight: 600 }}>
              Cuenta de Usuario
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', fontSize: '0.9rem' }}>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>ID DE USUARIO (UUID)</span>
              <code style={{ background: 'rgba(0,0,0,0.3)', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.85rem', color: 'var(--accent-emerald)' }}>
                {user?.id || 'Desconectado'}
              </code>
            </div>

            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>CORREO ELECTRÓNICO</span>
              <span style={{ fontWeight: 500 }}>{user?.email}</span>
            </div>

            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>PROVEEDOR DE AUTH</span>
              <span style={{ fontWeight: 500 }}>Supabase Auth (datalaria-core)</span>
            </div>
          </div>
        </div>

        {/* System & Endpoints */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
            <Server size={20} color="var(--accent-cyan)" />
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.1rem', fontWeight: 600 }}>
              Endpoints de Infraestructura
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', fontSize: '0.9rem' }}>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>BACKEND FASTAPI</span>
              <code>http://localhost:8000</code>
            </div>

            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>DATABASE SCHEMA</span>
              <code>lifeops (datalaria-core)</code>
            </div>

            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>CORS PERMITIDOS</span>
              <code>http://localhost:5173</code>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
