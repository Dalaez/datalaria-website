/**
 * apps/snake/sw.js
 * Service Worker PWA Offline — Neon Snake v2.3.1
 * Datalaria Helix — Strict Offline Resilience (Invariante INV-SNAKE-8, INV-SNAKE-13, INV-SNAKE-14 & INV-SNAKE-15)
 */

const CACHE_NAME = 'datalaria-snake-v2.3.1';

const PRECACHE_ASSETS = [
  '/games/snake/',
  '/games/snake/index.html',
  '/games/snake/manifest.json',
  '/games/snake/icon.svg',
  '/games/snake/icon-192.png',
  '/games/snake/icon-512.png',
  '/games/snake/icon-maskable-192.png',
  '/games/snake/icon-maskable-512.png',
  '/games/snake/apple-touch-icon.png'
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
          if (key !== CACHE_NAME && key.startsWith('datalaria-snake-')) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  // Ignorar llamadas a Supabase API
  if (event.request.url.includes('supabase.co')) {
    return;
  }

  // Solo gestionar peticiones GET
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Estrategia: Cache First con Network Fallback y Stale-While-Revalidate
  if (url.pathname.startsWith('/games/snake/')) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          // Revalidación en segundo plano
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
            return caches.match('/games/snake/index.html');
          }
        });
      })
    );
  }
});
