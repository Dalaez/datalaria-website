import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Mail, Lock, ArrowRight, ShieldCheck, AlertCircle } from 'lucide-react';
import './LoginPage.css';

export function LoginPage() {
  const { signIn, signUp } = useAuth();
  const navigate = useNavigate();

  const [isRegister, setIsRegister] = useState(false);
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
      if (isRegister) {
        await signUp(email, password);
        setMessage('¡Cuenta creada correctamente! Comprueba tu email o inicia sesión.');
      } else {
        await signIn(email, password);
        navigate('/');
      }
    } catch (err) {
      setError(err.message || 'Error en la autenticación');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-glass-card animate-fade-in">
        {/* Logo Branding */}
        <div className="login-brand">
          <div className="brand-logo-large">
            <Sparkles size={28} />
          </div>
          <h2>LifeOps</h2>
          <p>Tu cuaderno de bitácora personal & profesional</p>
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
            <label>Correo Electrónico</label>
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

          <div className="form-group">
            <label>Contraseña</label>
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

          <button type="submit" className="login-submit-btn" disabled={loading}>
            <span>{loading ? 'Procesando...' : isRegister ? 'Crear Cuenta' : 'Iniciar Sesión'}</span>
            <ArrowRight size={18} />
          </button>
        </form>

        {/* Footer Toggle */}
        <div className="login-footer">
          <span>
            {isRegister ? '¿Ya tienes cuenta?' : '¿No tienes cuenta aún?'}
          </span>
          <button
            type="button"
            className="toggle-mode-btn"
            onClick={() => {
              setIsRegister(!isRegister);
              setError(null);
              setMessage(null);
            }}
          >
            {isRegister ? 'Inicia Sesión' : 'Regístrate'}
          </button>
        </div>

        <div className="login-security-tag">
          <ShieldCheck size={14} color="var(--accent-emerald)" />
          <span>Protegido con Supabase Auth (datalaria-core)</span>
        </div>
      </div>
    </div>
  );
}
