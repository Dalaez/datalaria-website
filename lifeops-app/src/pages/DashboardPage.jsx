import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { api } from '../lib/api';
import { StatWidget } from '../components/Dashboard/StatWidget';
import { QuickActions } from '../components/Dashboard/QuickActions';
import { SystemHealth } from '../components/Dashboard/SystemHealth';
import { Activity, BookOpen, Film, Briefcase, CheckSquare, Flame, TrendingUp } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export function DashboardPage() {
  const { user } = useAuth();
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
    { name: 'Deporte', count: breakdown?.sport || 0, color: '#10b981' },
    { name: 'Libros', count: breakdown?.book || 0, color: '#06b6d4' },
    { name: 'Cine/Series', count: breakdown?.film || 0, color: '#8b5cf6' },
    { name: 'Aprendizaje', count: breakdown?.learning || 0, color: '#f59e0b' },
    { name: 'Journal', count: breakdown?.journal || 0, color: '#ec4899' },
  ];

  return (
    <div className="dashboard-page">
      {/* Page Title */}
      <div className="page-header-title">
        <h1>¡Hola, {user?.email?.split('@')[0] || 'Datalaria'}! 👋</h1>
        <p>Aquí tienes el resumen de tu actividad personal y profesional en LifeOps.</p>
      </div>

      {/* KPI Stats Grid */}
      <div className="stats-grid">
        <StatWidget
          title="Actividades (Semana)"
          value={summary?.activities_this_week || 0}
          subtitle={`Total histórico: ${summary?.total_activities || 0}`}
          icon={Activity}
          color="emerald"
        />
        <StatWidget
          title="Proyectos Activos"
          value={summary?.active_projects || 0}
          subtitle={`De ${summary?.total_projects || 0} proyectos`}
          icon={Briefcase}
          color="purple"
        />
        <StatWidget
          title="Tareas Pendientes"
          value={summary?.tasks_todo || 0}
          subtitle={`${summary?.tasks_overdue || 0} vencidas`}
          icon={CheckSquare}
          color="amber"
        />
        <StatWidget
          title="Hábitos Activos"
          value={summary?.active_habits || 0}
          subtitle="Rachas en progreso"
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
            else if (actionId === 'report') alert('El Módulo de Generación de Informes Word se desarrollará en la Fase 4 📄');
          }}
        />

        {/* Activity Distribution Chart */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.1rem', fontWeight: 600 }}>
              Desglose de Actividad (Últimos 30 días)
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
