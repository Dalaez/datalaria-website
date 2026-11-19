/**
 * Pure formatting and deterministic KPI helpers for Sport & Fitness workouts.
 * Extracted from SportModule.jsx to keep React component files Fast-Refresh clean.
 */

export const ALLOWED_PAGE_SIZES = [12, 24, 48];

/**
 * Extracts total workout duration in seconds.
 * Prefers metadata.duration_seconds (exact), falls back to duration_minutes * 60.
 */
export function getWorkoutTotalSeconds(act) {
  if (!act) return 0;
  if (act.metadata?.duration_seconds != null) {
    return parseInt(act.metadata.duration_seconds, 10) || 0;
  }
  if (act.duration_minutes != null) {
    return Math.round(Number(act.duration_minutes) * 60);
  }
  return 0;
}

/**
 * Formats seconds into human-readable duration (e.g. "48m 25s", "1h 15m 30s", "45 min").
 */
export function formatWorkoutDuration(act) {
  const totalSec = getWorkoutTotalSeconds(act);
  if (!totalSec) return '-';

  const h = Math.floor(totalSec / 3600);
  const m = Math.floor((totalSec % 3600) / 60);
  const s = totalSec % 60;

  if (h > 0) {
    return s > 0 ? `${h}h ${m}m ${s}s` : `${h}h ${m}m`;
  }
  return s > 0 ? `${m}m ${s}s` : `${m} min`;
}

/**
 * Calculates real-time running pace (MM:SS /km) or cycling speed (km/h).
 */
export function calculatePaceOrSpeed(totalSec, distanceKm, workoutType) {
  const dist = parseFloat(distanceKm);
  const sec = parseInt(totalSec, 10);
  if (!sec || !dist || dist <= 0) return null;

  if (workoutType === 'cycling') {
    const hours = sec / 3600;
    const speed = (dist / hours).toFixed(1);
    return { type: 'speed', value: `${speed} km/h` };
  }

  const secondsPerKm = sec / dist;
  const paceMin = Math.floor(secondsPerKm / 60);
  const paceSec = Math.round(secondsPerKm % 60);
  const formattedPace = `${paceMin}:${paceSec.toString().padStart(2, '0')} /km`;
  return { type: 'pace', value: formattedPace };
}

/**
 * Deterministic client-side summary aggregator used for mock mode and 404 fallback.
 */
export function computeSportSummaryClient(activities = []) {
  let count = 0;
  let totalKm = 0;
  let totalSeconds = 0;
  let totalKcal = 0;
  let pbCount = 0;

  for (const act of activities) {
    count += 1;
    totalSeconds += getWorkoutTotalSeconds(act);
    const w = act?.workout || {};
    if (w.distance_km != null) totalKm += Number(w.distance_km) || 0;
    if (w.calories != null) totalKcal += parseInt(w.calories, 10) || 0;
    if (w.personal_best) pbCount += 1;
  }

  return {
    count,
    total_km: Math.round(totalKm * 100) / 100,
    total_seconds: totalSeconds,
    total_kcal: totalKcal,
    pb_count: pbCount,
  };
}
