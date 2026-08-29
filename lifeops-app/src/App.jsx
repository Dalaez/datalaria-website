import React, { Suspense, lazy } from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { LanguageProvider } from './context/LanguageContext';
import { ProtectedRoute } from './components/Auth/ProtectedRoute';
import { MainLayout } from './components/Layout/MainLayout';
import './App.css';

// Route-level Code Splitting for ultra-fast initial load
const LoginPage = lazy(() => import('./pages/LoginPage').then((m) => ({ default: m.LoginPage })));
const DashboardPage = lazy(() => import('./pages/DashboardPage').then((m) => ({ default: m.DashboardPage })));
const PersonalPage = lazy(() => import('./pages/PersonalPage').then((m) => ({ default: m.PersonalPage })));
const ProfessionalPage = lazy(() => import('./pages/ProfessionalPage').then((m) => ({ default: m.ProfessionalPage })));
const ReportsPage = lazy(() => import('./pages/ReportsPage').then((m) => ({ default: m.ReportsPage })));
const SettingsPage = lazy(() => import('./pages/SettingsPage').then((m) => ({ default: m.SettingsPage })));

function RouteFallback() {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '60vh',
      color: 'var(--text-muted)',
      fontSize: '0.9rem',
      fontFamily: 'var(--font-heading)'
    }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.75rem' }}>
        <div style={{
          width: '28px',
          height: '28px',
          border: '2px solid rgba(255, 255, 255, 0.1)',
          borderTopColor: 'var(--accent-emerald)',
          borderRadius: '50%',
          animation: 'spin 0.8s linear infinite'
        }} />
        <span>Cargando LifeOps...</span>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <HashRouter>
          <Suspense fallback={<RouteFallback />}>
            <Routes>
              {/* Public Route */}
              <Route path="/login" element={<LoginPage />} />

              {/* Protected Main Layout */}
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <MainLayout />
                  </ProtectedRoute>
                }
              >
                <Route index element={<DashboardPage />} />
                <Route path="personal" element={<PersonalPage />} />
                <Route path="professional" element={<ProfessionalPage />} />
                <Route path="reports" element={<ReportsPage />} />
                <Route path="stats" element={<DashboardPage />} />
                <Route path="settings" element={<SettingsPage />} />
              </Route>

              {/* Fallback */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Suspense>
        </HashRouter>
      </AuthProvider>
    </LanguageProvider>
  );
}
