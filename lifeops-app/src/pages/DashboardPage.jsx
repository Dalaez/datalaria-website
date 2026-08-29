import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../lib/api';
import { StatWidget } from '../components/Dashboard/StatWidget';
import { QuickActions } from '../components/Dashboard/QuickActions';
import { SystemHealth } from '../components/Dashboard/SystemHealth';
import { Activity, BookOpen, Film, Briefcase, CheckSquare, Flame, TrendingUp } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export function DashboardPage() {
  const { user } = useAuth();
  const { t, language } = useLanguage();
  const navigate = useNavigate();
  const [summary, setSummary] = useState(null);
  const [breakdown, setBreakdown] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboardData() {
      try {
        const [summaryData, breakdownData] = await Promise.all([
          api.getDashboardSummary().catch(() => null),
          api.getActivityBreakdown().catch(() => null),
        ]);
        setSummary(summaryData);
        setBreakdown(breakdownData);
      } catch (err) {
        console.error('Error loading dashboard:', err);
      } finally {
        setLoading(false);
      }
    }
    loadDashboardData();
  }, []);

  const chartData = [
    { name: language === 'es' ? 'Deporte' : 'Sport', count: breakdown?.sport || 0, color: '#10b981' },
    { name: language === 'es' ? 'Libros' : 'Books', count: breakdown?.book || 0, color: '#06b6d4' },
    { name: language === 'es' ? 'Cine/Series' : 'Cinema/TV', count: breakdown?.film || 0, color: '#8b5cf6' },
    { name: language === 'es' ? 'Aprendizaje' : 'Learning', count: breakdown?.learning || 0, color: '#f59e0b' },
    { name: 'Journal', count: breakdown?.journal || 0, color: '#ec4899' },
  ];

  return (
    <div className="dashboard-page">
      {/* Page Title */}
      <div className="page-header-title">
        <h1>{t('dashboard.welcome')}, {user?.email?.split('@')[0] || 'Datalaria'}! 👋</h1>
        <p>{t('dashboard.subtitle')}</p>
      </div>

      {/* KPI Stats Grid */}
      <div className="stats-grid">
        <StatWidget
          title={language === 'es' ? 'Actividades (Semana)' : 'Activities (Week)'}
          value={summary?.activities_this_week || 0}
          subtitle={`${language === 'es' ? 'Total histórico' : 'All-time total'}: ${summary?.total_activities || 0}`}
          icon={Activity}
          color="emerald"
        />
        <StatWidget
          title={language === 'es' ? 'Proyectos Activos' : 'Active Projects'}
          value={summary?.active_projects || 0}
          subtitle={`${language === 'es' ? 'De' : 'Of'} ${summary?.total_projects || 0} ${language === 'es' ? 'proyectos' : 'projects'}`}
          icon={Briefcase}
          color="purple"
        />
        <StatWidget
          title={language === 'es' ? 'Tareas Pendientes' : 'Pending Tasks'}
          value={summary?.tasks_todo || 0}
          subtitle={`${summary?.tasks_overdue || 0} ${language === 'es' ? 'vencidas' : 'overdue'}`}
          icon={CheckSquare}
          color="amber"
        />
        <StatWidget
          title={language === 'es' ? 'Hábitos Activos' : 'Active Habits'}
          value={summary?.active_habits || 0}
          subtitle={language === 'es' ? 'Rachas en progreso' : 'Streaks in progress'}
          icon={Flame}
          color="cyan"
        />
      </div>

      {/* Main Content Sections */}
      <div className="dashboard-sections-grid">
        {/* Quick Actions Panel */}
        <QuickActions
          onAction={(actionId) => {
            if (actionId === 'sport') navigate('/personal?tab=sport');
            else if (actionId === 'book') navigate('/personal?tab=books');
            else if (actionId === 'film') navigate('/personal?tab=films');
            else if (actionId === 'task') navigate('/professional?tab=kanban');
            else if (actionId === 'report') navigate('/reports');
          }}
        />

        {/* Activity Distribution Chart */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.1rem', fontWeight: 600 }}>
              {language === 'es' ? 'Desglose de Actividad (Últimos 30 días)' : 'Activity Breakdown (Last 30 Days)'}
            </h3>
            <TrendingUp size={18} color="var(--accent-emerald)" />
          </div>

          <div style={{ width: '100%', height: 220 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <XAxis dataKey="name" stroke="#6b7280" fontSize={12} tickLine={false} />
                <YAxis stroke="#6b7280" fontSize={12} tickLine={false} allowDecimals={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(17, 24, 39, 0.95)',
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderRadius: '8px',
                    color: '#fff',
                  }}
                />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Backend Connection Health */}
        <SystemHealth />
      </div>
    </div>
  );
}
