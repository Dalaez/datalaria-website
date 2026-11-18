/**
 * apps/reading/sw.js
 * Service Worker PWA Offline — Lector Arcade v1.0.0
 * Datalaria Helix — Strict Offline Resilience (Invariante INV-READ-8)
 */

const CACHE_NAME = 'datalaria-reading-v1.0.0';

const PRECACHE_ASSETS = [
  '/apps/reading/',
  '/apps/reading/index.html',
  '/apps/reading/manifest.json',
  '/apps/reading/icon.svg',
  '/apps/reading/icon-192.png',
  '/apps/reading/icon-512.png',
  '/apps/reading/icon-maskable-192.png',
  '/apps/reading/icon-maskable-512.png',
  '/apps/reading/apple-touch-icon.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS);
    })
  );
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME && key.startsWith('datalaria-reading-')) {
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
  if (url.pathname.startsWith('/apps/reading/')) {
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
            return caches.match('/apps/reading/index.html');
          }
        });
      })
    );
  }
});
