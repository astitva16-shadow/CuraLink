/**
 * CuraLink Service Worker
 * Provides offline capabilities and caching for PWA functionality
 */

const CACHE_NAME = 'curalink-v1';
const RUNTIME_CACHE = 'curalink-runtime-v1';

// Core assets to cache on install
const CORE_ASSETS = [
  '/',
  '/static/manifest.json',
  // Add your CSS files here when you know their paths
  // '/static/css/main.css',
  // Add your JS files here
  // '/static/js/main.js',
];

// Install event - cache core assets
self.addEventListener('install', (event) => {
  console.log('Service Worker: Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Service Worker: Caching core assets');
        return cache.addAll(CORE_ASSETS);
      })
      .then(() => self.skipWaiting())
      .catch((error) => {
        console.error('Service Worker: Cache installation failed:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME && cache !== RUNTIME_CACHE) {
            console.log('Service Worker: Clearing old cache:', cache);
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip Django admin and API endpoints from caching
  if (url.pathname.startsWith('/admin/') || 
      url.pathname.startsWith('/api/') ||
      url.pathname.includes('/accounts/logout/')) {
    return;
  }

  event.respondWith(
    caches.match(request)
      .then((cachedResponse) => {
        // Return cached response if found
        if (cachedResponse) {
          // For HTML pages, fetch in background and update cache (stale-while-revalidate)
          if (request.headers.get('Accept').includes('text/html')) {
            fetch(request)
              .then((response) => {
                if (response && response.status === 200) {
                  const responseClone = response.clone();
                  caches.open(RUNTIME_CACHE).then((cache) => {
                    cache.put(request, responseClone);
                  });
                }
              })
              .catch(() => {
                // Network failed, but we have cache
              });
          }
          return cachedResponse;
        }

        // Not in cache, fetch from network
        return fetch(request)
          .then((response) => {
            // Check if valid response
            if (!response || response.status !== 200 || response.type === 'error') {
              return response;
            }

            // Clone the response
            const responseToCache = response.clone();

            // Cache static assets and pages
            if (url.pathname.startsWith('/static/') || 
                request.headers.get('Accept').includes('text/html') ||
                request.headers.get('Accept').includes('text/css') ||
                request.headers.get('Accept').includes('application/javascript')) {
              caches.open(RUNTIME_CACHE)
                .then((cache) => {
                  cache.put(request, responseToCache);
                });
            }

            return response;
          })
          .catch(() => {
            // Network failed and no cache - return offline page for HTML requests
            if (request.headers.get('Accept').includes('text/html')) {
              return caches.match('/').then((response) => {
                return response || new Response('Offline - Please check your connection', {
                  status: 503,
                  statusText: 'Service Unavailable',
                  headers: new Headers({
                    'Content-Type': 'text/html'
                  })
                });
              });
            }
          });
      })
  );
});

// Background sync for offline form submissions (optional, advanced feature)
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-appointments') {
    event.waitUntil(syncAppointments());
  }
});

// Push notifications (optional, for future use)
self.addEventListener('push', (event) => {
  const data = event.data ? event.data.json() : {};
  const title = data.title || 'CuraLink Notification';
  const options = {
    body: data.body || 'You have a new notification',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-96x96.png',
    vibrate: [200, 100, 200],
    data: data.url || '/',
    actions: [
      {
        action: 'open',
        title: 'Open'
      },
      {
        action: 'close',
        title: 'Close'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'open') {
    event.waitUntil(
      clients.openWindow(event.notification.data)
    );
  }
});

// Helper function for background sync (example)
async function syncAppointments() {
  // This would sync any offline appointment bookings
  // Implementation depends on your specific needs
  console.log('Background sync: Syncing appointments...');
}
