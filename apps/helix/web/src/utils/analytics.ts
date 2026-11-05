/**
 * Telemetría GA4 tipada para Datalaria Helix (SPEC-APP-HELIX §5).
 */

declare global {
  interface Window {
    gtag?: (command: string, action: string, params?: Record<string, unknown>) => void;
    dataLayer?: Array<Record<string, unknown>>;
  }
}

export type HelixEventName =
  | 'join_waitlist_helix'
  | 'generate_helix_spec_zip'
  | 'copy_helix_megaprompt'
  | 'begin_checkout_helix_kit';

export function trackHelixEvent(
  eventName: HelixEventName,
  params: Record<string, unknown> = {}
): void {
  const payload = {
    app: 'helix',
    timestamp: new Date().toISOString(),
    ...params,
  };

  try {
    if (typeof window.gtag === 'function') {
      window.gtag('event', eventName, payload);
    }
    if (Array.isArray(window.dataLayer)) {
      window.dataLayer.push({ event: eventName, ...payload });
    }
  } catch {
    // Silencioso ante bloqueadores de anuncios o entornos sin GA4
  }
}
