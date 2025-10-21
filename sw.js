// FREE Service Worker for Real-Time Push Notifications
// No external dependencies - completely FREE

const CACHE_NAME = 'scribble-tools-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/favicon.ico'
];

// Install event - cache essential files
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

// Push notification event
self.addEventListener('push', event => {
    console.log('Push notification received');
    
    const data = event.data ? event.data.json() : {};
    const title = data.title || '📝 New Blog Post Available!';
    const options = {
        body: data.body || 'Check out the latest updates on Scribble Tools',
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        image: data.image || null,
        data: {
            url: data.url || '#blogs',
            timestamp: Date.now()
        },
        actions: [
            {
                action: 'read-now',
                title: '📖 Read Now'
            },
            {
                action: 'read-later',
                title: '⏰ Read Later'
            },
            {
                action: 'dismiss',
                title: '❌ Dismiss'
            }
        ],
        requireInteraction: true, // Keep notification visible until user interacts
        vibrate: [200, 100, 200], // Vibration pattern for mobile
        tag: 'blog-notification', // Replace previous notifications with same tag
        renotify: false
    };
    
    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

// Notification click event
self.addEventListener('notificationclick', event => {
    console.log('Notification clicked:', event.action);
    
    event.notification.close();
    
    const notificationData = event.notification.data;
    
    if (event.action === 'read-now') {
        // Open the blog post immediately
        event.waitUntil(
            clients.matchAll({ type: 'window' }).then(clientList => {
                // Check if app is already open
                for (const client of clientList) {
                    if (client.url.includes(self.location.origin)) {
                        client.focus();
                        client.postMessage({
                            type: 'NAVIGATE_TO',
                            url: notificationData.url
                        });
                        return;
                    }
                }
                // Open new window if app not already open
                return clients.openWindow(notificationData.url);
            })
        );
    } else if (event.action === 'read-later') {
        // Save to reading list
        event.waitUntil(
            addToReadingList(notificationData)
        );
    } else if (event.action === 'dismiss') {
        // Just close - no action needed
        console.log('Notification dismissed');
    } else {
        // Default click (no action button) - open the link
        event.waitUntil(
            clients.openWindow(notificationData.url)
        );
    }
});

// Add to reading list (FREE localStorage-based system)
async function addToReadingList(notificationData) {
    try {
        // Use IndexedDB for more robust storage
        const request = indexedDB.open('ScribbleToolsDB', 1);
        
        request.onupgradeneeded = function(event) {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('readingList')) {
                db.createObjectStore('readingList', { keyPath: 'id', autoIncrement: true });
            }
        };
        
        request.onsuccess = function(event) {
            const db = event.target.result;
            const transaction = db.transaction(['readingList'], 'readwrite');
            const store = transaction.objectStore('readingList');
            
            const article = {
                url: notificationData.url,
                timestamp: notificationData.timestamp,
                dateAdded: new Date().toISOString(),
                status: 'unread'
            };
            
            store.add(article);
        };
        
        // Send message to app if open
        const clients = await self.clients.matchAll();
        clients.forEach(client => {
            client.postMessage({
                type: 'READING_LIST_UPDATED',
                action: 'added'
            });
        });
        
        // Show confirmation
        self.registration.showNotification('📚 Saved to Reading List', {
            body: 'Article saved for later reading',
            icon: '/favicon.ico',
            tag: 'reading-list-confirmation',
            requireInteraction: false
        });
        
        setTimeout(() => {
            self.registration.getNotifications({ tag: 'reading-list-confirmation' })
                .then(notifications => {
                    notifications.forEach(notification => notification.close());
                });
        }, 3000);
        
    } catch (error) {
        console.error('Error adding to reading list:', error);
    }
}

// Background sync for offline functionality (FREE)
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync-subscriptions') {
        event.waitUntil(syncPendingSubscriptions());
    }
});

// Sync pending subscriptions when back online
async function syncPendingSubscriptions() {
    try {
        const request = indexedDB.open('ScribbleToolsDB', 1);
        
        request.onsuccess = function(event) {
            const db = event.target.result;
            const transaction = db.transaction(['pendingSubscriptions'], 'readwrite');
            const store = transaction.objectStore('pendingSubscriptions');
            
            store.getAll().onsuccess = function(event) {
                const pendingSubscriptions = event.target.result;
                
                pendingSubscriptions.forEach(async (subscription) => {
                    try {
                        // Attempt to sync with server
                        const response = await fetch('/api/subscribe-brevo.php', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(subscription.data)
                        });
                        
                        if (response.ok) {
                            // Remove from pending list
                            store.delete(subscription.id);
                        }
                    } catch (error) {
                        console.log('Will retry subscription sync later');
                    }
                });
            };
        };
    } catch (error) {
        console.error('Sync error:', error);
    }
}

// Message handling from main app
self.addEventListener('message', event => {
    const { type, data } = event.data;
    
    switch (type) {
        case 'SKIP_WAITING':
            self.skipWaiting();
            break;
        case 'GET_VERSION':
            event.ports[0].postMessage({ version: CACHE_NAME });
            break;
        case 'SIMULATE_NOTIFICATION':
            // For testing purposes
            self.registration.showNotification('Test Notification', {
                body: 'This is a test of the notification system',
                icon: '/favicon.ico',
                data: { url: '#blogs' }
            });
            break;
    }
});

console.log('🔔 Service Worker registered - FREE real-time notifications enabled!');