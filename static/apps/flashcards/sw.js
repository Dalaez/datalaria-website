/**
 * apps/flashcards/sw.js
 * Service Worker PWA Offline — Flashcards AI v2.1.0
 * Datalaria Helix — Strict Offline Resilience (Invariante INV-FLASH-8)
 */

const CACHE_NAME = 'datalaria-flashcards-v2.1.0';

const PRECACHE_ASSETS = [
  '/apps/flashcards/',
  '/apps/flashcards/index.html',
  '/apps/flashcards/manifest.json',
  '/apps/flashcards/icon.svg',
  '/apps/flashcards/icon-192.png',
  '/apps/flashcards/icon-512.png',
  '/apps/flashcards/icon-maskable-192.png',
  '/apps/flashcards/icon-maskable-512.png',
  '/apps/flashcards/apple-touch-icon.png'
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
          if (key !== CACHE_NAME && key.startsWith('datalaria-flashcards-')) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  // Ignorar llamadas de inferencia externa a Gemini API (BYOK)
  if (event.request.url.includes('generativelanguage.googleapis.com')) {
    return;
  }

  // Solo gestionar peticiones GET
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Estrategia: Cache First con Network Fallback y Stale-While-Revalidate para la app
  if (url.pathname.startsWith('/apps/flashcards/')) {
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
            return caches.match('/apps/flashcards/index.html');
          }
        });
      })
    );
  }
});
