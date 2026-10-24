import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { useNavigate } from 'react-router-dom';
import { LanguageSwitcher } from '../components/common/LanguageSwitcher';
import { Sparkles, Mail, Lock, ArrowRight, ShieldCheck, AlertCircle, KeyRound, ArrowLeft } from 'lucide-react';
import './LoginPage.css';

export function LoginPage() {
  const { signIn, signUp, resetPassword } = useAuth();
  const { t } = useLanguage();
  const navigate = useNavigate();

  // 'login' | 'register' | 'forgot'
  const [authMode, setAuthMode] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    setLoading(true);

    try {
      if (authMode === 'register') {
        await signUp(email, password);
        setMessage('¡Cuenta creada correctamente! Comprueba tu email o inicia sesión.');
      } else if (authMode === 'forgot') {
        await resetPassword(email);
        setMessage(t('auth.resetEmailSent'));
      } else {
        await signIn(email, password);
        navigate('/');
      }
    } catch (err) {
      setError(err.message || t('common.error'));
    } finally {
      setLoading(false);
    }
  };

  const getSubtitle = () => {
    if (authMode === 'register') return t('auth.registerSubtitle');
    if (authMode === 'forgot') return t('auth.forgotSubtitle');
    return t('auth.loginSubtitle');
  };

  return (
    <div className="login-container">
      {/* Top language selector */}
      <div style={{ position: 'absolute', top: '1.5rem', right: '1.5rem', zIndex: 10 }}>
        <LanguageSwitcher />
      </div>

      <div className="login-glass-card animate-fade-in">
        {/* Logo Branding */}
        <div className="login-brand">
          <div className="brand-logo-large">
            {authMode === 'forgot' ? <KeyRound size={28} /> : <Sparkles size={28} />}
          </div>
          <h2>LifeOps</h2>
          <p>{getSubtitle()}</p>
        </div>

        {/* Status messages */}
        {error && (
          <div className="login-alert error">
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        {message && (
          <div className="login-alert success">
            <ShieldCheck size={16} />
            <span>{message}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label>{t('auth.emailLabel')}</label>
            <div className="input-with-icon">
              <Mail size={18} className="input-icon" />
              <input
                type="email"
                required
                placeholder="tu.email@ejemplo.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          {authMode !== 'forgot' && (
            <div className="form-group">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <label>{t('auth.passwordLabel')}</label>
                {authMode === 'login' && (
                  <button
                    type="button"
                    style={{
                      background: 'none',
                      border: 'none',
                      color: 'var(--accent-cyan)',
                      fontSize: '0.78rem',
                      cursor: 'pointer',
                      padding: 0,
                      marginBottom: '0.3rem'
                    }}
                    onClick={() => {
                      setAuthMode('forgot');
                      setError(null);
                      setMessage(null);
                    }}
                  >
                    {t('auth.forgotPassword')}
                  </button>
                )}
              </div>
              <div className="input-with-icon">
                <Lock size={18} className="input-icon" />
                <input
                  type="password"
                  required
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>
          )}

          <button type="submit" className="login-submit-btn" disabled={loading}>
            <span>
              {loading
                ? t('common.loading')
                : authMode === 'register'
                ? t('auth.registerButton')
                : authMode === 'forgot'
                ? t('auth.resetButton')
                : t('auth.loginButton')}
            </span>
            <ArrowRight size={18} />
          </button>
        </form>

        {/* Footer Toggle */}
        <div className="login-footer">
          {authMode === 'forgot' ? (
            <button
              type="button"
              className="toggle-mode-btn"
              style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', margin: '0 auto' }}
              onClick={() => {
                setAuthMode('login');
                setError(null);
                setMessage(null);
              }}
            >
              <ArrowLeft size={14} />
              <span>{t('auth.backToLogin')}</span>
            </button>
          ) : (
            <>
              <span>
                {authMode === 'register' ? t('auth.haveAccount') : t('auth.noAccount')}
              </span>
              <button
                type="button"
                className="toggle-mode-btn"
                onClick={() => {
                  setAuthMode(authMode === 'register' ? 'login' : 'register');
                  setError(null);
                  setMessage(null);
                }}
              >
                {authMode === 'register' ? t('auth.loginLink') : t('auth.registerLink')}
              </button>
            </>
          )}
        </div>

        <div className="login-security-tag">
          <ShieldCheck size={14} color="var(--accent-emerald)" />
          <span>Protegido con Supabase Auth (datalaria-core)</span>
        </div>
      </div>
    </div>
  );
}
