import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { LanguageSwitcher } from '../components/common/LanguageSwitcher';
import { Settings, Shield, Server, Database, User, Globe, Lock, CheckCircle2, AlertCircle, KeyRound } from 'lucide-react';

export function SettingsPage() {
  const { user, updatePassword } = useAuth();
  const { t, language } = useLanguage();

  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [savingPassword, setSavingPassword] = useState(false);
  const [passwordSuccess, setPasswordSuccess] = useState(null);
  const [passwordError, setPasswordError] = useState(null);

  const handleUpdatePassword = async (e) => {
    e.preventDefault();
    setPasswordError(null);
    setPasswordSuccess(null);

    if (newPassword.length < 6) {
      setPasswordError('La contraseña debe tener al menos 6 caracteres.');
      return;
    }

    if (newPassword !== confirmPassword) {
      setPasswordError(t('settings.passwordMismatch'));
      return;
    }

    try {
      setSavingPassword(true);
      await updatePassword(newPassword);
      setPasswordSuccess(t('settings.passwordUpdatedSuccess'));
      setNewPassword('');
      setConfirmPassword('');
      setTimeout(() => setPasswordSuccess(null), 4000);
    } catch (err) {
      setPasswordError(err.message || t('common.error'));
    } finally {
      setSavingPassword(false);
    }
  };

  return (
    <div className="settings-page">
      <div className="page-header-title">
        <h1>⚙️ {t('settings.title')}</h1>
        <p>{t('settings.subtitle')}</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '1.5rem' }}>
        {/* Language & Regional */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
            <Globe size={20} color="var(--accent-cyan)" />
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.1rem', fontWeight: 600 }}>
              {t('settings.languageSection')}
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', fontSize: '0.9rem' }}>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
              {t('settings.languageDesc')}
            </p>

            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <LanguageSwitcher />
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                {language === 'es' ? '🇪🇸 Español (Activo)' : '🇬🇧 English (Active)'}
              </span>
            </div>
          </div>
        </div>

        {/* Change Password / Security */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
            <KeyRound size={20} color="var(--accent-amber)" />
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.1rem', fontWeight: 600 }}>
              {t('settings.securitySection')}
            </h3>
          </div>

          {passwordSuccess && (
            <div className="feedback-banner success" style={{ marginBottom: '1rem', padding: '0.6rem 0.8rem', fontSize: '0.82rem' }}>
              <CheckCircle2 size={16} />
              <span>{passwordSuccess}</span>
            </div>
          )}

          {passwordError && (
            <div className="feedback-banner error" style={{ marginBottom: '1rem', padding: '0.6rem 0.8rem', fontSize: '0.82rem' }}>
              <AlertCircle size={16} />
              <span>{passwordError}</span>
            </div>
          )}

          <form onSubmit={handleUpdatePassword} style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                {t('settings.changePasswordTitle')}
              </label>
              <input
                type="password"
                required
                placeholder={t('settings.newPasswordPlaceholder')}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                style={{
                  width: '100%',
                  background: 'var(--bg-input)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px',
                  padding: '0.55rem 0.85rem',
                  color: 'var(--text-primary)',
                  fontSize: '0.88rem'
                }}
              />
            </div>

            <div>
              <input
                type="password"
                required
                placeholder={t('settings.confirmPasswordPlaceholder')}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                style={{
                  width: '100%',
                  background: 'var(--bg-input)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px',
                  padding: '0.55rem 0.85rem',
                  color: 'var(--text-primary)',
                  fontSize: '0.88rem'
                }}
              />
            </div>

            <button
              type="submit"
              className="btn-primary"
              disabled={savingPassword}
              style={{ width: 'fit-content', marginTop: '0.25rem' }}
            >
              <Lock size={15} />
              <span>{savingPassword ? t('common.saving') : t('settings.updatePasswordBtn')}</span>
            </button>
          </form>
        </div>

        {/* Account Info */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
            <User size={20} color="var(--accent-emerald)" />
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.1rem', fontWeight: 600 }}>
              {t('settings.accountSection')}
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', fontSize: '0.9rem' }}>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>{t('settings.userIdLabel')}</span>
              <code style={{ background: 'rgba(0,0,0,0.3)', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.85rem', color: 'var(--accent-emerald)' }}>
                {user?.id || 'Desconectado'}
              </code>
            </div>

            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>{t('settings.emailLabel')}</span>
              <span style={{ fontWeight: 500 }}>{user?.email}</span>
            </div>

            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>AUTH PROVIDER</span>
              <span style={{ fontWeight: 500 }}>Supabase Auth (datalaria-core)</span>
            </div>
          </div>
        </div>

        {/* System & Endpoints */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
            <Server size={20} color="var(--accent-purple)" />
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.1rem', fontWeight: 600 }}>
              Infraestructura & Endpoints
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', fontSize: '0.9rem' }}>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>BACKEND FASTAPI</span>
              <code>https://lifeops-api.onrender.com</code>
            </div>

            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>DATABASE SCHEMA</span>
              <code>lifeops (datalaria-core)</code>
            </div>

            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>CORS DOMAINS</span>
              <code>http://localhost:1313, http://localhost:5173, https://datalaria.com</code>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
