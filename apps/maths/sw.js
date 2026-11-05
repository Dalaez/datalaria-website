/**
 * static/apps/maths/sw.js
 * Service Worker PWA Offline — Ábaco Arcade v2.1.0
 * Datalaria Helix — Strict Offline Resilience (Invariante INV-MATHS-8)
 */

const CACHE_NAME = 'datalaria-maths-v2.1.0';

const PRECACHE_ASSETS = [
  '/apps/maths/',
  '/apps/maths/index.html',
  '/apps/maths/manifest.json',
  '/apps/maths/icon.svg',
  '/apps/maths/datalaria_logo_transp.png'
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
          if (key !== CACHE_NAME && key.startsWith('datalaria-maths-')) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Solo gestionar peticiones GET del mismo origen
  if (event.request.method !== 'GET') return;

  // Estrategia: Cache First con Network Fallback para assets locales de la app
  if (url.pathname.startsWith('/apps/maths/')) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          // Revalidación en segundo plano (stale-while-revalidate)
          fetch(event.request).then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              caches.open(CACHE_NAME).then((cache) => cache.put(event.request, networkResponse));
            }
          }).catch(() => { /* Modo offline */ });
          return cachedResponse;
        }

        return fetch(event.request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, responseToCache));
          }
          return networkResponse;
        }).catch(() => {
          // Si estamos offline y se solicita la navegación, retornar index.html precacheado
          if (event.request.mode === 'navigate') {
            return caches.match('/apps/maths/index.html');
          }
        });
      })
    );
  }
});
