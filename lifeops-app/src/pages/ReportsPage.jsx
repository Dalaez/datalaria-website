import React, { useState, useEffect } from 'react';
import { api } from '../lib/api';
import { useLanguage } from '../context/LanguageContext';
import { 
  FileText, 
  Download, 
  Calendar, 
  Activity, 
  Briefcase, 
  Sparkles, 
  Clock, 
  CheckCircle2, 
  AlertCircle,
  FileCheck,
  FileSpreadsheet,
  Table,
  BookOpen,
  Film,
  CheckSquare,
  HardDriveDownload
} from 'lucide-react';
import './ReportsPage.css';

export function ReportsPage() {
  const { t, language } = useLanguage();
  const [selectedTemplate, setSelectedTemplate] = useState('monthly_summary');
  const [datePreset, setDatePreset] = useState('current_month');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [exportingEntity, setExportingEntity] = useState(null);
  const [isExportingExcel, setIsExportingExcel] = useState(false);
  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [successMessage, setSuccessMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // Set date ranges according to presets
  useEffect(() => {
    const now = new Date();
    const y = now.getFullYear();
    const m = now.getMonth();

    if (datePreset === 'current_month') {
      const first = new Date(y, m, 1).toISOString().split('T')[0];
      const last = now.toISOString().split('T')[0];
      setDateFrom(first);
      setDateTo(last);
    } else if (datePreset === 'previous_month') {
      const first = new Date(y, m - 1, 1).toISOString().split('T')[0];
      const last = new Date(y, m, 0).toISOString().split('T')[0];
      setDateFrom(first);
      setDateTo(last);
    } else if (datePreset === 'current_year') {
      const first = new Date(y, 0, 1).toISOString().split('T')[0];
      const last = now.toISOString().split('T')[0];
      setDateFrom(first);
      setDateTo(last);
    }
  }, [datePreset]);

  // Load history
  const fetchHistory = async () => {
    try {
      setHistoryLoading(true);
      const data = await api.getReportHistory();
      setHistory(data || []);
    } catch (err) {
      console.error('Error fetching report history:', err);
    } finally {
      setHistoryLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleGenerate = async (templateId) => {
    const tid = templateId || selectedTemplate;
    try {
      setIsGenerating(true);
      setErrorMessage(null);
      setSuccessMessage(null);

      await api.downloadReport(tid, dateFrom, dateTo);

      setSuccessMessage(t('reports.feedbackWordSuccess'));
      fetchHistory();

      setTimeout(() => setSuccessMessage(null), 5000);
    } catch (err) {
      console.error('Generation error:', err);
      setErrorMessage(err.message || t('common.error'));
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExportCSV = async (entity, label) => {
    try {
      setExportingEntity(entity);
      setErrorMessage(null);
      setSuccessMessage(null);

      await api.exportCSV(entity);
      setSuccessMessage(t('reports.feedbackCsvSuccess'));
      setTimeout(() => setSuccessMessage(null), 4000);
    } catch (err) {
      console.error('CSV export error:', err);
      setErrorMessage(t('common.error'));
    } finally {
      setExportingEntity(null);
    }
  };

  const handleExportExcel = async () => {
    try {
      setIsExportingExcel(true);
      setErrorMessage(null);
      setSuccessMessage(null);

      await api.exportExcel();
      setSuccessMessage(t('reports.feedbackExcelSuccess'));
      setTimeout(() => setSuccessMessage(null), 4000);
    } catch (err) {
      console.error('Excel export error:', err);
      setErrorMessage(t('common.error'));
    } finally {
      setIsExportingExcel(false);
    }
  };

  const templates = [
    {
      id: 'monthly_summary',
      title: language === 'es' ? 'Informe Mensual Integral' : 'Comprehensive Monthly Report',
      badge: language === 'es' ? 'Recomendado' : 'Recommended',
      icon: Sparkles,
      iconColor: 'var(--accent-emerald)',
      category: 'General & Personal',
      description: language === 'es' 
        ? 'Dossier ejecutivo completo 360°. Incluye métricas deportivas (km, calorías, PB), biblioteca de lecturas, valoraciones de cine/series y portafolio de proyectos con tareas completadas.'
        : 'Full 360° executive dossier. Includes fitness metrics (km, calories, PB), reading library, movie ratings and project portfolio with completed tasks.',
      sections: language === 'es'
        ? ['Resumen Ejecutivo KPIs', 'Deporte & Rendimiento', 'Lectura & Cultura', 'Portafolio Profesional']
        : ['Executive KPIs Summary', 'Fitness & Performance', 'Reading & Culture', 'Professional Portfolio'],
    },
    {
      id: 'sport_performance',
      title: language === 'es' ? 'Dossier de Rendimiento Deportivo' : 'Fitness Performance Dossier',
      badge: language === 'es' ? 'Deporte' : 'Sport',
      icon: Activity,
      iconColor: 'var(--accent-cyan)',
      category: 'Salud & Fitness',
      description: language === 'es'
        ? 'Análisis detallado de tu actividad física. Desglose de entrenamientos por disciplina (Running, Ciclismo, Gym), volumen de kilómetros, ritmo promedio, marcas personales y gasto calórico.'
        : 'In-depth analysis of your workouts. Breakdown by discipline (Running, Cycling, Gym), distance volume, average pace, personal bests and calories burned.',
      sections: language === 'es'
        ? ['Volumen Total de Horas/Km', 'Tabla Desglosada de Sesiones', 'Marcas Personales (PB)', 'Calorías Quemadas']
        : ['Total Hours & Distance Volume', 'Itemized Workouts Table', 'Personal Bests (PB)', 'Calories Burned'],
    },
    {
      id: 'project_status',
      title: language === 'es' ? 'Estado de Portafolio de Proyectos' : 'Project Portfolio Status',
      badge: language === 'es' ? 'Profesional' : 'Professional',
      icon: Briefcase,
      iconColor: 'var(--accent-purple)',
      category: 'Gestión & Empresa',
      description: language === 'es'
        ? 'Informe ejecutivo de avance corporativo. Estado de proyectos, control presupuestario, cálculo de horas estimadas vs. reales y tabla de entregables del tablero Kanban.'
        : 'Executive corporate progress report. Project statuses, budget tracking, estimated vs. actual hours and Kanban deliverables table.',
      sections: language === 'es'
        ? ['Control Presupuestario', 'Fechas Límite & Hitos', 'Tareas Completadas', 'Prioridades Abiertas']
        : ['Budget Tracking', 'Deadlines & Milestones', 'Completed Tasks', 'Open Priorities'],
    },
  ];

  const exportEntities = [
    { id: 'sport', label: t('reports.modules.sport'), icon: Activity, color: 'var(--accent-emerald)', desc: t('reports.modules.sportDesc') },
    { id: 'books', label: t('reports.modules.books'), icon: BookOpen, color: 'var(--accent-cyan)', desc: t('reports.modules.booksDesc') },
    { id: 'films', label: t('reports.modules.films'), icon: Film, color: 'var(--accent-purple)', desc: t('reports.modules.filmsDesc') },
    { id: 'tasks', label: t('reports.modules.tasks'), icon: CheckSquare, color: 'var(--accent-amber)', desc: t('reports.modules.tasksDesc') },
    { id: 'projects', label: t('reports.modules.projects'), icon: Briefcase, color: '#38bdf8', desc: t('reports.modules.projectsDesc') },
  ];

  return (
    <div className="reports-page-container">
      {/* Page Header */}
      <div className="reports-header-section">
        <div>
          <h1 className="reports-page-title">
            <FileText className="title-icon" color="var(--accent-emerald)" size={28} />
            {t('reports.title')}
          </h1>
          <p className="reports-page-subtitle">
            {t('reports.subtitle')}
          </p>
        </div>
      </div>

      {/* Alerts / Feedback */}
      {successMessage && (
        <div className="feedback-banner success">
          <CheckCircle2 size={18} />
          <span>{successMessage}</span>
        </div>
      )}
      {errorMessage && (
        <div className="feedback-banner error">
          <AlertCircle size={18} />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* Period Selector Toolbar */}
      <div className="report-controls-panel glass-panel">
        <div className="controls-group">
          <span className="control-label">
            <Calendar size={15} /> {t('reports.periodTitle')}
          </span>
          <div className="preset-buttons-group">
            <button 
              className={`preset-btn ${datePreset === 'current_month' ? 'active' : ''}`}
              onClick={() => setDatePreset('current_month')}
            >
              {t('reports.presets.current_month')}
            </button>
            <button 
              className={`preset-btn ${datePreset === 'previous_month' ? 'active' : ''}`}
              onClick={() => setDatePreset('previous_month')}
            >
              {t('reports.presets.previous_month')}
            </button>
            <button 
              className={`preset-btn ${datePreset === 'current_year' ? 'active' : ''}`}
              onClick={() => setDatePreset('current_year')}
            >
              {t('reports.presets.current_year')}
            </button>
            <button 
              className={`preset-btn ${datePreset === 'custom' ? 'active' : ''}`}
              onClick={() => setDatePreset('custom')}
            >
              {t('reports.presets.custom')}
            </button>
          </div>
        </div>

        <div className="date-inputs-group">
          <div className="date-input-field">
            <label>{t('reports.fromLabel')}</label>
            <input 
              type="date" 
              value={dateFrom} 
              onChange={(e) => {
                setDateFrom(e.target.value);
                setDatePreset('custom');
              }}
            />
          </div>
          <div className="date-input-field">
            <label>{t('reports.toLabel')}</label>
            <input 
              type="date" 
              value={dateTo} 
              onChange={(e) => {
                setDateTo(e.target.value);
                setDatePreset('custom');
              }}
            />
          </div>
        </div>
      </div>

      {/* Section 1: Template Cards Grid */}
      <div className="section-title-wrapper">
        <h2 className="section-block-title">
          <FileText size={20} color="var(--accent-emerald)" />
          {t('reports.wordTemplatesTitle')}
        </h2>
        <span className="section-block-tag">{t('reports.wordTag')}</span>
      </div>

      <div className="templates-grid">
        {templates.map((tpl) => {
          const Icon = tpl.icon;
          const isSelected = selectedTemplate === tpl.id;
          return (
            <div 
              key={tpl.id} 
              className={`template-card glass-panel ${isSelected ? 'selected' : ''}`}
              onClick={() => setSelectedTemplate(tpl.id)}
            >
              <div className="template-card-top">
                <div className="template-icon-wrapper" style={{ background: `rgba(255,255,255,0.05)` }}>
                  <Icon size={22} color={tpl.iconColor} />
                </div>
                <span className="template-badge">{tpl.badge}</span>
              </div>

              <h3 className="template-title">{tpl.title}</h3>
              <p className="template-desc">{tpl.description}</p>

              <div className="template-sections-list">
                <span className="sections-title">{t('reports.sectionsIncluded')}</span>
                <ul>
                  {tpl.sections.map((sec, i) => (
                    <li key={i}>
                      <span className="bullet-dot" style={{ backgroundColor: tpl.iconColor }}></span>
                      <span>{sec}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="template-footer">
                <button 
                  className="generate-action-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleGenerate(tpl.id);
                  }}
                  disabled={isGenerating}
                >
                  <Download size={16} />
                  <span>{isGenerating && selectedTemplate === tpl.id ? t('reports.generatingWord') : t('reports.downloadWord')}</span>
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Section 2: Data Portability & Raw Export (.csv / .xlsx) */}
      <div className="section-title-wrapper" style={{ marginTop: '1.5rem' }}>
        <h2 className="section-block-title">
          <FileSpreadsheet size={20} color="var(--accent-cyan)" />
          {t('reports.rawExportTitle')}
        </h2>
        <span className="section-block-tag" style={{ background: 'rgba(6, 182, 212, 0.15)', color: 'var(--accent-cyan)', borderColor: 'rgba(6, 182, 212, 0.3)' }}>
          {t('reports.rawExportTag')}
        </span>
      </div>

      <div className="export-master-panel glass-panel">
        {/* Full Excel Master Card */}
        <div className="excel-master-card">
          <div className="excel-info-side">
            <div className="excel-badge-icon">
              <Table size={24} color="#10b981" />
            </div>
            <div>
              <h3 className="excel-title">{t('reports.excelMasterTitle')}</h3>
              <p className="excel-desc">{t('reports.excelMasterDesc')}</p>
            </div>
          </div>
          <button 
            className="excel-download-btn"
            onClick={handleExportExcel}
            disabled={isExportingExcel}
          >
            <HardDriveDownload size={18} />
            <span>{isExportingExcel ? t('reports.exportingExcel') : t('reports.downloadExcelBtn')}</span>
          </button>
        </div>

        {/* CSV Individual Modules Grid */}
        <div className="csv-modules-grid">
          {exportEntities.map((ent) => {
            const Icon = ent.icon;
            const isThisExporting = exportingEntity === ent.id;
            return (
              <div key={ent.id} className="csv-module-card">
                <div className="csv-card-left">
                  <div className="csv-icon-pill" style={{ background: `rgba(255,255,255,0.05)` }}>
                    <Icon size={18} color={ent.color} />
                  </div>
                  <div>
                    <span className="csv-module-title">{ent.label}</span>
                    <span className="csv-module-desc">{ent.desc}</span>
                  </div>
                </div>
                <button 
                  className="csv-download-btn"
                  onClick={() => handleExportCSV(ent.id, ent.label)}
                  disabled={isThisExporting}
                  title={`Descargar ${ent.label} en CSV`}
                >
                  <Download size={14} />
                  <span>{isThisExporting ? t('reports.exportingCsv') : t('reports.downloadCsvBtn')}</span>
                </button>
              </div>
            );
          })}
        </div>
      </div>

      {/* Section 3: Generation History Table */}
      <div className="history-section glass-panel">
        <div className="history-header">
          <div className="history-title-group">
            <Clock size={18} color="var(--accent-emerald)" />
            <h3>{t('reports.historyTitle')}</h3>
          </div>
          <span className="history-count">{history.length} {t('reports.historyCount')}</span>
        </div>

        {historyLoading ? (
          <div className="history-loading">{t('common.loading')}</div>
        ) : history.length === 0 ? (
          <div className="history-empty">
            <FileCheck size={28} color="var(--text-muted)" />
            <p>{t('reports.historyEmpty')}</p>
          </div>
        ) : (
          <div className="history-table-wrapper">
            <table className="history-table">
              <thead>
                <tr>
                  <th>{t('reports.tableHeaders.file')}</th>
                  <th>{t('reports.tableHeaders.period')}</th>
                  <th>{t('reports.tableHeaders.date')}</th>
                  <th>{t('reports.tableHeaders.records')}</th>
                  <th>{t('reports.tableHeaders.format')}</th>
                </tr>
              </thead>
              <tbody>
                {history.map((h) => (
                  <tr key={h.id}>
                    <td className="file-name-cell">
                      <FileText size={15} color="var(--accent-emerald)" />
                      <span>{h.report_name}</span>
                    </td>
                    <td>
                      {h.period_start} - {h.period_end}
                    </td>
                    <td>
                      {new Date(h.generated_at).toLocaleString(language === 'es' ? 'es-ES' : 'en-US', {
                        day: '2-digit',
                        month: '2-digit',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </td>
                    <td>
                      <span className="records-pill">
                        {(h.metadata?.activities_count || 0) + (h.metadata?.tasks_count || 0)} {t('common.items')}
                      </span>
                    </td>
                    <td>
                      <span className="docx-badge">.DOCX</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
