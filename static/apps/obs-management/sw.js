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
self.addEventListener('install', (event) => {
event.waitUntil(
caches.open(CACHE_NAME).then((cache) => {
return Promise.allSettled(
SHELL_ASSETS.map((asset) => cache.add(new Request(asset, { cache: 'reload' })).catch(() => {}))
);
}).then(() => self.skipWaiting())
);
});
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
self.addEventListener('fetch', (event) => {
const url = new URL(event.request.url);
if (event.request.method !== 'GET') return;
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
