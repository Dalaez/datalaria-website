// apps/obs-management/web/sw.js - Service Worker para Agentic Radar v2.0.0
// Arquitectura Zero-CDN, Offline 100% en Sandbox y Network-First para App Shell (INV-OBS-1, INV-OBS-6)

const CACHE_NAME = 'obs-radar-v2.0.0';

const SHELL_ASSETS = [
    './',
    'index.html',
    'manifest.json',
    'styles.css',
    'engine.js',
    'i18n.js',
    'app.js',
    'icon.svg',
    'apple-touch-icon.png',
    'icons/icon-192.png',
    'icons/icon-512.png',
    'icons/icon-maskable-192.png',
    'icons/icon-maskable-512.png'
];

// 1. Install - Pre-cache Shell determinista y tolerante a fallos
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return Promise.allSettled(
                SHELL_ASSETS.map((asset) => cache.add(new Request(asset, { cache: 'reload' })).catch(() => {}))
            );
        }).then(() => self.skipWaiting())
    );
});

// 2. Activate - Limpiar versiones obsoletas inmediatamente
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((key) => {
                    if (key !== CACHE_NAME && key.startsWith('obs-radar-')) {
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

// 3. Fetch Handler con estrategias diferenciadas
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // Solo gestionar peticiones GET
    if (event.request.method !== 'GET') return;

    // Regla de Exclusión: NUNCA interceptar ni cachear APIs backend, Lemon Squeezy o Google Analytics
    if (
        url.pathname.includes('/api/') ||
        url.hostname.includes('lemonsqueezy.com') ||
        url.hostname.includes('google-analytics.com') ||
        url.hostname.includes('googletagmanager.com')
    ) {
        return;
    }

    const scopePath = new URL(self.registration.scope).pathname;
    const isAppShellNav = url.origin === self.location.origin && (
        url.pathname === scopePath ||
        url.pathname === scopePath + 'index.html' ||
        url.pathname === '/apps/obs-management/' ||
        url.pathname === '/apps/obs-management/index.html'
    );

    // Estrategia A: Navegación HTML / App Shell -> Network-First con Fallback Offline a Caché
    if (isAppShellNav || event.request.mode === 'navigate' || url.pathname.endsWith('.html')) {
        event.respondWith(
            fetch(event.request).then((response) => {
                if (response && response.status === 200) {
                    const cacheCopy = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, cacheCopy.clone()).catch(() => {});
                        if (isAppShellNav || event.request.mode === 'navigate') {
                            cache.put('./', cacheCopy.clone()).catch(() => {});
                            cache.put('index.html', cacheCopy).catch(() => {});
                        }
                    });
                }
                return response;
            }).catch(() => {
                return caches.match(event.request, { ignoreSearch: true }).then((cached) => {
                    return cached || caches.match('./') || caches.match('index.html');
                });
            })
        );
        return;
    }

    // Estrategia B: Assets estáticos locales (CSS, JS, SVG, PNG, manifest.json) -> Stale-While-Revalidate
    if (url.origin === self.location.origin) {
        event.respondWith(
            caches.match(event.request).then((cached) => {
                const networkFetch = fetch(event.request).then((response) => {
                    if (response && response.status === 200) {
                        const clone = response.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone).catch(() => {}));
                    }
                    return response;
                }).catch(() => cached);

                return cached || networkFetch;
            }).catch(() => fetch(event.request))
        );
    }
});
