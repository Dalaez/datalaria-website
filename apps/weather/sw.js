// sw.js - Service Worker para Weather Intelligence v3.0 (INV-WEATHER-10)
const CACHE_NAME = 'weather-v3.0.0';
const SHELL_ASSETS = [
    '/apps/weather/',
    '/apps/weather/index.html',
    '/apps/weather/manifest.json',
    '/apps/weather/icon.svg',
    '/apps/weather/icon-192.png',
    '/apps/weather/icon-512.png',
    '/apps/weather/datalaria_logo_transp.png'
];

// 1. Install - Pre-cache Shell
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(SHELL_ASSETS);
        }).then(() => self.skipWaiting())
    );
});

// 2. Activate - Limpiar versiones obsoletas
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((key) => {
                    if (key !== CACHE_NAME && key.startsWith('weather-')) {
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// 3. Fetch Handler con estrategias diferenciadas (INV-WEATHER-10)
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // REGLA ESTRICTA INV-WEATHER-10: NUNCA cachear archivos CSV planos
    if (url.pathname.endsWith('.csv') || url.pathname.includes('/datos/')) {
        return; // Petición directa a red sin pasar por el Service Worker
    }

    // A. Shell / Assets locales (Cache-First)
    if (url.pathname.startsWith('/apps/weather/') && (
        url.pathname.endsWith('.html') ||
        url.pathname.endsWith('.svg') ||
        url.pathname.endsWith('.png') ||
        url.pathname.endsWith('.json') && url.pathname.includes('manifest')
    )) {
        event.respondWith(
            caches.match(event.request).then((cached) => {
                return cached || fetch(event.request).then((response) => {
                    if (response && response.status === 200) {
                        const clone = response.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                    }
                    return response;
                });
            })
        );
        return;
    }

    // B. CDN Assets (Fonts, Leaflet, Chart.js, Feather, PapaParse) -> Cache-First
    if (
        url.hostname.includes('fonts.googleapis.com') ||
        url.hostname.includes('fonts.gstatic.com') ||
        url.hostname.includes('cdn.jsdelivr.net') ||
        url.hostname.includes('cdnjs.cloudflare.com') ||
        url.hostname.includes('unpkg.com')
    ) {
        event.respondWith(
            caches.match(event.request).then((cached) => {
                if (cached) return cached;
                return fetch(event.request).then((response) => {
                    if (response && response.status === 200) {
                        const clone = response.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                    }
                    return response;
                });
            })
        );
        return;
    }

    // C. JSON de Datos (derived/**, global_summary, predicciones) -> Stale-While-Revalidate
    if (
        (url.pathname.endsWith('.json') || url.pathname.includes('/derived/')) &&
        (url.hostname.includes('datalaria-app-weather.netlify.app') || url.pathname.startsWith('/apps/weather/'))
    ) {
        event.respondWith(
            caches.open(CACHE_NAME).then((cache) => {
                return cache.match(event.request).then((cached) => {
                    const fetchPromise = fetch(event.request).then((networkResponse) => {
                        if (networkResponse && networkResponse.status === 200) {
                            cache.put(event.request, networkResponse.clone());
                        }
                        return networkResponse;
                    }).catch(() => cached);

                    return cached || fetchPromise;
                });
            })
        );
        return;
    }

    // D. Teselas del mapa Leaflet -> Network-first con fallback a caché
    if (url.hostname.includes('tile.openstreetmap.org') || url.hostname.includes('basemaps.cartocdn.com')) {
        event.respondWith(
            fetch(event.request).then((networkResponse) => {
                if (networkResponse && networkResponse.status === 200) {
                    const clone = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                }
                return networkResponse;
            }).catch(() => caches.match(event.request))
        );
        return;
    }
});
