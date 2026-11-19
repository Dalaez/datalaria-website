import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import { api } from '../../lib/api';
import { Modal } from '../common/Modal';
import { Paginator, PageSizeSelector } from '../common/Paginator';
import { useLanguage } from '../../context/LanguageContext';
import { useAuth } from '../../context/AuthContext';
import { usePagedActivities } from '../../hooks/usePagedActivities';
import {
  ALLOWED_PAGE_SIZES,
  getWorkoutTotalSeconds,
  formatWorkoutDuration,
  calculatePaceOrSpeed,
} from '../../lib/sportFormatters';
import {
  Activity,
  Plus,
  Trash2,
  Edit2,
  Award,
  Flame,
  Heart,
  Clock,
  Navigation,
  TrendingUp,
  Dumbbell,
  Bike,
  LayoutGrid,
  Timer,
  Zap,
  Copy,
  Table as TableIcon,
  RefreshCw,
  AlertTriangle,
} from 'lucide-react';
import './SportModule.css';

const PAGE_SIZE_STORAGE_KEY = 'lifeops_sport_page_size';

function resolveInitialPageSize(searchParams) {
  const urlSize = parseInt(searchParams.get('size') || '', 10);
  if (ALLOWED_PAGE_SIZES.includes(urlSize)) return urlSize;
  try {
    const stored = parseInt(localStorage.getItem(PAGE_SIZE_STORAGE_KEY) || '', 10);
    if (ALLOWED_PAGE_SIZES.includes(stored)) return stored;
  } catch {
    // Ignore storage access errors
  }
  return 12;
}

export function SportModule() {
  const { t } = useLanguage();
  const { user } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();
  const listTopRef = useRef(null);

  const page = Math.max(1, parseInt(searchParams.get('page') || '1', 10) || 1);
  const pageSize = resolveInitialPageSize(searchParams);

  const {
    items: workouts,
    summary,
    total,
    totalPages,
    hasHydrated,
    loading,
    isSyncing,
    isPageTransitioning,
    error,
    elapsedSec,
    reload,
    invalidateSummary,
  } = usePagedActivities({
    userId: user?.id,
    activityType: 'sport',
    page,
    pageSize,
  });

  const [isModalOpen, setIsModalOpen] = useState(() => {
    const hash = window.location.hash || '';
    const search = window.location.search || '';
    return hash.includes('openModal=true') || search.includes('openModal=true');
  });
  const [editingWorkout, setEditingWorkout] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const [viewMode, setViewMode] = useState(() => {
    const params = new URLSearchParams(
      window.location.hash.includes('?') ? window.location.hash.split('?')[1] : window.location.search
    );
    const urlView = params.get('view');
    if (urlView === 'grid' || urlView === 'table') return urlView;
    if (typeof window !== 'undefined' && window.innerWidth <= 768) {
      return sessionStorage.getItem('lifeops_view_sport_session') || 'grid';
    }
    return localStorage.getItem('lifeops_view_sport') || 'grid';
  });

  const handleViewChange = (mode) => {
    setViewMode(mode);
    localStorage.setItem('lifeops_view_sport', mode);
    sessionStorage.setItem('lifeops_view_sport_session', mode);
  };

  const updatePaginationParams = (nextPage, nextSize) => {
    const next = new URLSearchParams(searchParams);
    next.set('tab', searchParams.get('tab') || 'sport');
    next.set('page', String(nextPage));
    next.set('size', String(nextSize));
    setSearchParams(next);
  };

  // Clamp out-of-range page in URL once totalPages is known
  useEffect(() => {
    if (!loading && hasHydrated && totalPages >= 1 && page > totalPages) {
      const next = new URLSearchParams(searchParams);
      next.set('tab', searchParams.get('tab') || 'sport');
      next.set('page', String(totalPages));
      next.set('size', String(pageSize));
      setSearchParams(next, { replace: true });
    }
  }, [loading, hasHydrated, totalPages, page, pageSize, searchParams, setSearchParams]);

  const handlePageChange = (nextPage) => {
    const clamped = Math.max(1, Math.min(totalPages, nextPage));
    if (clamped === page) return;
    updatePaginationParams(clamped, pageSize);
    if (listTopRef.current) {
      listTopRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  const handlePageSizeChange = (nextSize) => {
    if (!ALLOWED_PAGE_SIZES.includes(nextSize) || nextSize === pageSize) return;
    try {
      localStorage.setItem(PAGE_SIZE_STORAGE_KEY, String(nextSize));
    } catch {
      // Ignore storage quota errors
    }
    updatePaginationParams(1, nextSize);
  };

  // Form state with explicit hours, minutes and seconds
  const defaultFormData = {
    title: '',
    date: new Date().toISOString().split('T')[0],
    duration_hours: '',
    duration_minutes: 45,
    duration_seconds: '',
    workout_type: 'running',
    distance_km: '',
    calories: '',
    avg_heart_rate: '',
    elevation_m: '',
    personal_best: false,
    notes: '',
  };

  const [formData, setFormData] = useState(defaultFormData);

  const handleOpenCreate = () => {
    setEditingWorkout(null);
    setFormData(defaultFormData);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (act) => {
    setEditingWorkout(act);
    const w = act.workout || {};
    const totalSec = getWorkoutTotalSeconds(act);
    const hours = Math.floor(totalSec / 3600);
    const minutes = Math.floor((totalSec % 3600) / 60);
    const seconds = totalSec % 60;

    setFormData({
      title: act.title || '',
      date: act.date || new Date().toISOString().split('T')[0],
      duration_hours: hours > 0 ? hours : '',
      duration_minutes: minutes,
      duration_seconds: seconds > 0 ? seconds : '',
      workout_type: w.workout_type || 'running',
      distance_km: w.distance_km != null ? w.distance_km : '',
      calories: w.calories != null ? w.calories : '',
      avg_heart_rate: w.avg_heart_rate || w.heart_rate_avg || '',
      elevation_m: w.elevation_m != null ? w.elevation_m : '',
      personal_best: Boolean(w.personal_best),
      notes: act.description || w.notes || act.notes || '',
    });
    setIsModalOpen(true);
  };

  const handleDuplicate = (act) => {
    setEditingWorkout(null);
    const w = act.workout || {};
    const totalSec = getWorkoutTotalSeconds(act);
    const hours = Math.floor(totalSec / 3600);
    const minutes = Math.floor((totalSec % 3600) / 60);
    const seconds = totalSec % 60;

    setFormData({
      title: act.title || '',
      date: new Date().toISOString().split('T')[0],
      duration_hours: hours > 0 ? hours : '',
      duration_minutes: minutes,
      duration_seconds: seconds > 0 ? seconds : '',
      workout_type: w.workout_type || 'running',
      distance_km: w.distance_km != null ? w.distance_km : '',
      calories: w.calories != null ? w.calories : '',
      avg_heart_rate: w.avg_heart_rate || w.heart_rate_avg || '',
      elevation_m: w.elevation_m != null ? w.elevation_m : '',
      personal_best: false,
      notes: act.description || w.notes || act.notes || '',
    });
    setIsModalOpen(true);
  };

  const currentTotalSeconds =
    (parseInt(formData.duration_hours, 10) || 0) * 3600 +
    (parseInt(formData.duration_minutes, 10) || 0) * 60 +
    (parseInt(formData.duration_seconds, 10) || 0);

  const liveMetric = calculatePaceOrSpeed(currentTotalSeconds, formData.distance_km, formData.workout_type);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const totalSeconds =
        (parseInt(formData.duration_hours, 10) || 0) * 3600 +
        (parseInt(formData.duration_minutes, 10) || 0) * 60 +
        (parseInt(formData.duration_seconds, 10) || 0);

      const durationMinutesInt = Math.max(1, Math.round(totalSeconds / 60));

      const payload = {
        activity: {
          activity_type: 'sport',
          title: formData.title,
          date: formData.date,
          duration_minutes: durationMinutesInt,
          description: formData.notes,
          metadata: {
            ...(editingWorkout?.metadata || {}),
            duration_seconds: totalSeconds,
          },
        },
        workout: {
          workout_type: formData.workout_type,
          distance_km: formData.distance_km !== '' ? parseFloat(formData.distance_km) : null,
          calories: formData.calories !== '' ? parseInt(formData.calories, 10) : null,
          avg_heart_rate: formData.avg_heart_rate !== '' ? parseInt(formData.avg_heart_rate, 10) : null,
          elevation_m: formData.elevation_m !== '' ? parseInt(formData.elevation_m, 10) : null,
          personal_best: formData.personal_best,
          notes: formData.notes,
        },
      };

      const isEditing = Boolean(editingWorkout);
      if (isEditing) {
        await api.updateSportActivity(editingWorkout.id, payload);
      } else {
        await api.createSportActivity(payload);
      }

      setIsModalOpen(false);
      setFormData(defaultFormData);
      setEditingWorkout(null);

      // Navigate to page 1 after creating/duplicating, or refresh current page on edit
      if (!isEditing && page !== 1) {
        invalidateSummary();
        updatePaginationParams(1, pageSize);
      } else {
        await reload({ forceSummary: true, targetPage: isEditing ? page : 1 });
      }
    } catch (err) {
      alert(`${t('common.error')}: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm(t('common.confirmDelete'))) return;
    try {
      await api.deleteActivity(id);
      if (workouts.length === 1 && page > 1) {
        invalidateSummary();
        updatePaginationParams(page - 1, pageSize);
      } else {
        await reload({ forceSummary: true, targetPage: page });
      }
    } catch (err) {
      alert(`${t('common.error')}: ${err.message}`);
    }
  };

  // Historical KPIs from server summary (never partial page slice)
  const hasSummary = summary != null;
  const totalKm = summary?.total_km ?? 0;
  const totalSeconds = summary?.total_seconds ?? 0;
  const totalCalories = summary?.total_kcal ?? 0;
  const pbCount = summary?.pb_count ?? 0;

  const progressPercent = Math.min(95, 14 + elapsedSec * 2);

  const getSportIcon = (type) => {
    switch (type) {
      case 'running':
        return <Activity size={16} color="var(--accent-emerald)" />;
      case 'cycling':
        return <Bike size={16} color="var(--accent-cyan)" />;
      case 'gym':
        return <Dumbbell size={16} color="var(--accent-purple)" />;
      default:
        return <Activity size={16} color="var(--accent-amber)" />;
    }
  };

  return (
    <div className="sport-module">
      {/* Top Action Bar */}
      <div className="module-header">
        <div>
          <h2>{t('sport.title')}</h2>
          <p>{t('sport.subtitle')}</p>
        </div>

        <div className="module-header-actions">
          <PageSizeSelector
            pageSize={pageSize}
            onChange={handlePageSizeChange}
            disabled={loading}
          />

          {/* View Mode Toggle */}
          <div className="view-mode-toggle glass-panel">
            <button
              type="button"
              className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`}
              onClick={() => handleViewChange('grid')}
              title={t('common.cardsView')}
            >
              <LayoutGrid size={15} />
              <span>{t('common.cardsView')}</span>
            </button>
            <button
              type="button"
              className={`view-btn ${viewMode === 'table' ? 'active' : ''}`}
              onClick={() => handleViewChange('table')}
              title={t('common.tableView')}
            >
              <TableIcon size={15} />
              <span>{t('common.tableView')}</span>
            </button>
          </div>

          <button className="btn-primary" onClick={handleOpenCreate}>
            <Plus size={16} />
            <span>{t('sport.addWorkout')}</span>
          </button>
        </div>
      </div>

      {/* Historical Metrics Banner */}
      <div className="metrics-banner">
        <div className="metric-box">
          <span className="metric-label">{t('sport.totalDistance')}</span>
          <span className="metric-value">
            {hasSummary ? totalKm.toFixed(1) : '—'} <small>{t('common.km')}</small>
          </span>
        </div>
        <div className="metric-box">
          <span className="metric-label">{t('sport.activeTime')}</span>
          <span className="metric-value" style={{ color: 'var(--accent-cyan)' }}>
            {hasSummary ? (totalSeconds / 3600).toFixed(1) : '—'} <small>{t('common.hours')}</small>
          </span>
        </div>
        <div className="metric-box">
          <span className="metric-label">{t('sport.caloriesBurned')}</span>
          <span className="metric-value" style={{ color: 'var(--accent-amber)' }}>
            {hasSummary ? totalCalories.toLocaleString() : '—'} <small>{t('common.kcal')}</small>
          </span>
        </div>
        <div className="metric-box">
          <span className="metric-label">{t('sport.personalBests')}</span>
          <span className="metric-value" style={{ color: 'var(--accent-purple)' }}>
            {hasSummary ? pbCount : '—'} <small>PBs 🏅</small>
          </span>
        </div>
      </div>

      {/* Non-blocking status bars when cached data is already visible */}
      {hasHydrated && isSyncing && (
        <div className="sport-sync-pill glass-panel" role="status" aria-live="polite">
          <RefreshCw size={14} className="spin-icon" />
          <span>{t('sport.states.syncRefreshing')}</span>
          <span className="sport-sync-timer">{elapsedSec}s</span>
        </div>
      )}

      {hasHydrated && error && (
        <div className="sport-sync-warning glass-panel" role="alert">
          <div className="sport-sync-warning-msg">
            <AlertTriangle size={16} />
            <span>{t('sport.states.refreshFailedHint')}</span>
          </div>
          <button
            type="button"
            className="sport-inline-retry-btn"
            onClick={() => reload({ forceSummary: summary == null })}
          >
            <RefreshCw size={14} />
            <span>{t('common.retry')}</span>
          </button>
        </div>
      )}

      {/* Workouts Content: 4 Explicit States (INV-16) */}
      <div ref={listTopRef} className={isPageTransitioning ? 'sport-list-transition' : ''}>
        {loading ? (
          /* State 1: Cold-Start Sync Banner + Skeleton Grid */
          <div className="sport-loading-container">
            <div className="cloud-sync-banner glass-panel" role="status" aria-live="polite">
              <div className="cloud-sync-banner-top">
                <div className="cloud-sync-title-row">
                  <div className="cloud-sync-spinner-box">
                    <RefreshCw size={20} className="spin-icon" />
                  </div>
                  <div className="cloud-sync-title-text">
                    <h3>{t('sport.states.syncTitle')}</h3>
                    <p>
                      {elapsedSec >= 4
                        ? t('sport.states.syncColdDesc')
                        : t('dashboard.analytics.syncBannerFastDesc')}
                    </p>
                  </div>
                </div>
                <span className="cloud-sync-timer-badge">{elapsedSec}s</span>
              </div>

              <div className="cloud-sync-progress-track">
                <div className="cloud-sync-progress-bar" style={{ width: `${progressPercent}%` }} />
              </div>

              <div className="cloud-sync-steps">
                <span className="cloud-sync-step done">
                  ✓ {t('dashboard.analytics.syncStepAuth')}
                </span>
                <span className="cloud-sync-step active">
                  ⟳ {t('dashboard.analytics.syncStepEngine')} ({elapsedSec}s)
                </span>
                <span className="cloud-sync-step">
                  ⏳ {t('dashboard.analytics.syncStepData')}
                </span>
              </div>
            </div>

            <div className="workouts-grid" aria-hidden="true">
              {Array.from({ length: Math.min(pageSize, 6) }, (_, idx) => (
                <div key={idx} className="workout-card glass-card workout-skeleton-card">
                  <div className="skeleton-line skeleton-badge" />
                  <div className="skeleton-line skeleton-title" />
                  <div className="skeleton-line skeleton-sub" />
                  <div className="skeleton-chips">
                    <span className="skeleton-chip" />
                    <span className="skeleton-chip" />
                    <span className="skeleton-chip" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : error && !hasHydrated ? (
          /* State 2: Explicit Network / Timeout Error State (Never Empty State, INV-16) */
          <div className="sport-error-state glass-panel" role="alert">
            <AlertTriangle size={40} className="sport-error-icon" />
            <h3>{t('sport.states.errorTitle')}</h3>
            <p>{t('sport.states.errorDesc')}</p>
            <small className="sport-error-detail">{error}</small>
            <button
              type="button"
              className="btn-primary sport-retry-btn"
              onClick={() => reload({ forceSummary: true })}
            >
              <RefreshCw size={16} />
              <span>{t('sport.states.retryBtn')}</span>
            </button>
          </div>
        ) : workouts.length === 0 ? (
          /* State 3: Genuine Empty State (confirmed total === 0) */
          <div className="empty-state glass-panel">
            <Activity size={40} className="empty-icon" />
            <h3>{t('sport.emptyTitle')}</h3>
            <p>{t('sport.emptyDesc')}</p>
            <button className="btn-primary" onClick={handleOpenCreate}>
              <Plus size={16} />
              <span>{t('sport.emptyAction')}</span>
            </button>
          </div>
        ) : viewMode === 'grid' ? (
          /* State 4A: Grid / Cards View */
          <div className="workouts-grid">
            {workouts.map((act) => {
              const w = act.workout || {};
              const totalSec = getWorkoutTotalSeconds(act);
              const paceOrSpeed = calculatePaceOrSpeed(totalSec, w.distance_km, w.workout_type);

              return (
                <div key={act.id} className="workout-card glass-card">
                  <div className="workout-card-header">
                    <div className="workout-type-badge">
                      {getSportIcon(w.workout_type)}
                      <span className="type-name">{w.workout_type?.toUpperCase()}</span>
                    </div>
                    <div className="card-top-right">
                      {w.personal_best && (
                        <span className="pb-badge" title={t('sport.isPBLabel')}>
                          <Award size={14} /> PB
                        </span>
                      )}
                      <button
                        className="copy-icon-btn"
                        onClick={() => handleDuplicate(act)}
                        title={t('common.duplicate')}
                      >
                        <Copy size={14} />
                      </button>
                      <button
                        className="edit-icon-btn"
                        onClick={() => handleOpenEdit(act)}
                        title={t('common.edit')}
                      >
                        <Edit2 size={14} />
                      </button>
                      <button
                        className="delete-icon-btn"
                        onClick={() => handleDelete(act.id)}
                        title={t('common.delete')}
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </div>

                  <h4 className="workout-title">{act.title}</h4>
                  <span className="workout-date">{act.date}</span>

                  <div className="workout-stats-chips">
                    {w.distance_km != null && (
                      <div className="stat-chip">
                        <Navigation size={13} />
                        <span>{w.distance_km} {t('common.km')}</span>
                      </div>
                    )}
                    {totalSec > 0 && (
                      <div className="stat-chip">
                        <Clock size={13} />
                        <span>{formatWorkoutDuration(act)}</span>
                      </div>
                    )}
                    {paceOrSpeed && (
                      <div
                        className="stat-chip pace-chip"
                        title={paceOrSpeed.type === 'speed' ? t('sport.fields.speed') : t('sport.fields.pace')}
                      >
                        {paceOrSpeed.type === 'speed' ? <Zap size={13} /> : <Timer size={13} />}
                        <span>{paceOrSpeed.value}</span>
                      </div>
                    )}
                    {w.calories != null && (
                      <div className="stat-chip">
                        <Flame size={13} />
                        <span>{w.calories} {t('common.kcal')}</span>
                      </div>
                    )}
                    {(w.avg_heart_rate != null || w.heart_rate_avg != null) && (
                      <div className="stat-chip">
                        <Heart size={13} />
                        <span>{w.avg_heart_rate || w.heart_rate_avg} {t('common.ppm')}</span>
                      </div>
                    )}
                    {w.elevation_m != null && (
                      <div className="stat-chip">
                        <TrendingUp size={13} />
                        <span>+{w.elevation_m}m</span>
                      </div>
                    )}
                  </div>

                  {(act.description || w.notes || act.notes) && (
                    <p className="workout-notes">{act.description || w.notes || act.notes}</p>
                  )}
                </div>
              );
            })}
          </div>
        ) : (
          /* State 4B: Table / Synthesized View */
          <div className="module-table-wrapper glass-panel">
            <table className="module-data-table">
              <thead>
                <tr>
                  <th>{t('sport.table.date')}</th>
                  <th>{t('sport.table.sport')}</th>
                  <th>{t('sport.table.title')}</th>
                  <th>{t('sport.table.distance')}</th>
                  <th>{t('sport.table.duration')}</th>
                  <th>{t('sport.table.calories')}</th>
                  <th>{t('sport.table.avgHr')}</th>
                  <th>{t('sport.table.record')}</th>
                  <th>{t('sport.table.notes')}</th>
                  <th style={{ textAlign: 'right' }}>{t('common.actions')}</th>
                </tr>
              </thead>
              <tbody>
                {workouts.map((act) => {
                  const w = act.workout || {};
                  const totalSec = getWorkoutTotalSeconds(act);
                  const paceOrSpeed = calculatePaceOrSpeed(totalSec, w.distance_km, w.workout_type);

                  return (
                    <tr key={act.id}>
                      <td className="table-date-cell">{act.date}</td>
                      <td>
                        <div className="table-sport-type">
                          {getSportIcon(w.workout_type)}
                          <span>{w.workout_type?.toUpperCase()}</span>
                        </div>
                      </td>
                      <td className="table-title-cell">{act.title}</td>
                      <td>{w.distance_km != null ? `${w.distance_km} ${t('common.km')}` : '-'}</td>
                      <td>
                        <div className="table-duration-cell">
                          <span>{formatWorkoutDuration(act)}</span>
                          {paceOrSpeed && (
                            <span className="table-pace-badge">
                              {paceOrSpeed.value}
                            </span>
                          )}
                        </div>
                      </td>
                      <td>{w.calories != null ? `${w.calories} ${t('common.kcal')}` : '-'}</td>
                      <td>
                        {(w.avg_heart_rate || w.heart_rate_avg)
                          ? `${w.avg_heart_rate || w.heart_rate_avg} ${t('common.ppm')}`
                          : '-'}
                      </td>
                      <td>
                        {w.personal_best ? (
                          <span className="table-pb-badge">🏅 {t('sport.pbBadge')}</span>
                        ) : (
                          <span style={{ color: 'var(--text-muted)' }}>-</span>
                        )}
                      </td>
                      <td className="table-notes-cell" title={act.description || w.notes || act.notes || ''}>
                        {act.description || w.notes || act.notes || '-'}
                      </td>
                      <td>
                        <div className="table-actions-cell">
                          <button
                            className="table-action-btn copy"
                            onClick={() => handleDuplicate(act)}
                            title={t('common.duplicate')}
                          >
                            <Copy size={14} />
                          </button>
                          <button
                            className="table-action-btn edit"
                            onClick={() => handleOpenEdit(act)}
                            title={t('common.edit')}
                          >
                            <Edit2 size={14} />
                          </button>
                          <button
                            className="table-action-btn delete"
                            onClick={() => handleDelete(act.id)}
                            title={t('common.delete')}
                          >
                            <Trash2 size={14} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Adaptive Pagination Bar */}
      {!loading && !(error && !hasHydrated) && total > 0 && (
        <Paginator
          page={page}
          pageSize={pageSize}
          total={total}
          totalPages={totalPages}
          onPageChange={handlePageChange}
          onPageSizeChange={handlePageSizeChange}
          disabled={isSyncing && !hasHydrated}
        />
      )}

      {/* Modal Form (Create / Edit) */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingWorkout(null);
        }}
        title={editingWorkout ? t('sport.editWorkoutTitle') : t('sport.createWorkoutTitle')}
      >
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label>{t('sport.fields.title')}</label>
            <input
              type="text"
              required
              placeholder={t('sport.titlePlaceholder')}
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('sport.fields.type')}</label>
              <select
                value={formData.workout_type}
                onChange={(e) => setFormData({ ...formData, workout_type: e.target.value })}
              >
                <option value="running">{t('sport.types.running')}</option>
                <option value="cycling">{t('sport.types.cycling')}</option>
                <option value="gym">{t('sport.types.gym')}</option>
                <option value="swimming">{t('sport.types.swimming')}</option>
                <option value="hiking">{t('sport.types.hiking')}</option>
                <option value="crossfit">{t('sport.types.crossfit')}</option>
                <option value="other">{t('sport.types.other')}</option>
              </select>
            </div>

            <div className="form-group">
              <label>{t('sport.fields.date')}</label>
              <input
                type="date"
                required
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              />
            </div>
          </div>

          {/* Time Picker: Hours : Minutes : Seconds */}
          <div className="form-group">
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.2rem' }}>
              <label style={{ margin: 0 }}>{t('sport.fields.duration')}</label>
              {liveMetric && (
                <span className="live-metric-badge">
                  {liveMetric.type === 'speed' ? <Zap size={12} /> : <Timer size={12} />}
                  <span>{liveMetric.type === 'speed' ? t('sport.fields.speed') : t('sport.fields.pace')}: {liveMetric.value}</span>
                </span>
              )}
            </div>

            <div className="duration-inputs-grid">
              <div className="duration-input-wrapper">
                <input
                  type="number"
                  min="0"
                  max="99"
                  placeholder="0"
                  value={formData.duration_hours}
                  onChange={(e) => setFormData({ ...formData, duration_hours: e.target.value })}
                  title={t('sport.fields.hours')}
                />
                <span className="duration-unit-label">h</span>
              </div>

              <span className="duration-sep">:</span>

              <div className="duration-input-wrapper">
                <input
                  type="number"
                  min="0"
                  max="59"
                  required
                  placeholder="45"
                  value={formData.duration_minutes}
                  onChange={(e) => setFormData({ ...formData, duration_minutes: e.target.value })}
                  title={t('sport.fields.minutes')}
                />
                <span className="duration-unit-label">m</span>
              </div>

              <span className="duration-sep">:</span>

              <div className="duration-input-wrapper">
                <input
                  type="number"
                  min="0"
                  max="59"
                  placeholder="00"
                  value={formData.duration_seconds}
                  onChange={(e) => setFormData({ ...formData, duration_seconds: e.target.value })}
                  title={t('sport.fields.seconds')}
                />
                <span className="duration-unit-label">s</span>
              </div>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('sport.fields.distance')}</label>
              <input
                type="number"
                step="0.01"
                min="0"
                placeholder="8.50"
                value={formData.distance_km}
                onChange={(e) => setFormData({ ...formData, distance_km: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>{t('sport.fields.calories')}</label>
              <input
                type="number"
                min="0"
                placeholder="450"
                value={formData.calories}
                onChange={(e) => setFormData({ ...formData, calories: e.target.value })}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t('sport.fields.heartRate')}</label>
              <input
                type="number"
                min="40"
                max="240"
                placeholder="145"
                value={formData.avg_heart_rate}
                onChange={(e) => setFormData({ ...formData, avg_heart_rate: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>{t('sport.fields.elevation')}</label>
              <input
                type="number"
                min="0"
                placeholder="120"
                value={formData.elevation_m}
                onChange={(e) => setFormData({ ...formData, elevation_m: e.target.value })}
              />
            </div>
          </div>

          <div className="form-group">
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', marginTop: '0.5rem' }}>
              <input
                type="checkbox"
                style={{ width: '18px', height: '18px', accentColor: 'var(--accent-emerald)' }}
                checked={formData.personal_best}
                onChange={(e) => setFormData({ ...formData, personal_best: e.target.checked })}
              />
              <span>{t('sport.isPBLabel')}</span>
            </label>
          </div>

          <div className="form-group">
            <label>{t('sport.fields.notes')}</label>
            <textarea
              placeholder={t('sport.workoutNotesPlaceholder')}
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            />
          </div>

          <div className="form-actions">
            <button
              type="button"
              className="btn-secondary"
              onClick={() => {
                setIsModalOpen(false);
                setEditingWorkout(null);
              }}
            >
              {t('common.cancel')}
            </button>
            <button type="submit" className="btn-primary" disabled={submitting}>
              {submitting ? t('common.saving') : (editingWorkout ? t('common.saveChanges') : t('common.save'))}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
