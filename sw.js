const CACHE_NAME = 'tubedz-cache-v2.0';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './logo.png',
  './manifest.json'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Let network handle YouTube streams, embeds & Google APIs
  if (event.request.url.includes('youtube') || 
      event.request.url.includes('googlevideo') || 
      event.request.url.includes('googleapis') ||
      event.request.url.includes('ytimg')) {
    return;
  }

  // Network-First for HTML navigation so updates are seen instantly without stale cache
  if (event.request.mode === 'navigate' || event.request.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(event.request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return networkResponse;
        })
        .catch(() => caches.match(event.request) || caches.match('./index.html'))
    );
    return;
  }

  // Cache-first for static icons and assets
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      return cachedResponse || fetch(event.request);
    })
  );
});
