/**
 * static/apps/conversor/sw.js
 * Service Worker PWA Offline — Conversor Universal Pro
 * Datalaria Helix — Strict Offline Resilience (Invariante INV-CONV-10)
 */

const CACHE_NAME = 'datalaria-conversor-v2.1.0';

const PRECACHE_ASSETS = [
  '/apps/conversor/',
  '/apps/conversor/index.html',
  '/apps/conversor/manifest.json',
  '/apps/conversor/icon.svg',
  '/apps/conversor/datalaria_logo_transp.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME && key.startsWith('datalaria-conversor-')) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Solo gestionar peticiones GET del mismo origen o fuentes de Google
  if (event.request.method !== 'GET') return;

  // Estrategia: Cache First con Network Fallback para assets locales de la app
  if (url.pathname.startsWith('/apps/conversor/')) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          // Revalidación en segundo plano (stale-while-revalidate)
          fetch(event.request).then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              caches.open(CACHE_NAME).then((cache) => cache.put(event.request, networkResponse));
            }
          }).catch(() => {/* Offline */});
          return cachedResponse;
        }

        return fetch(event.request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, responseToCache));
          }
          return networkResponse;
        }).catch(() => {
          // Si estamos offline y se solicita la app, retornar el index cacheado
          if (event.request.mode === 'navigate') {
            return caches.match('/apps/conversor/index.html');
          }
        });
      })
    );
  }
});
