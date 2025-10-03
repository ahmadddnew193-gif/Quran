self.addEventListener('install', function(event) {
  console.log("Service Worker installed.");
  self.skipWaiting();
});

self.addEventListener('activate', function(event) {
  console.log("Service Worker activated.");
});

self.addEventListener('push', function(event) {
  console.log("Push event:", event.data.text());

  const data = event.data.json();

  const options = {
    body: data.body,
    icon: "icon.png",
    badge: "icon.png",
    vibrate: [200, 100, 200],
    data: { url: data.url || "/" }
  };

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

self.addEventListener("notificationclick", function(event) {
  event.notification.close();
  event.waitUntil(clients.openWindow(event.notification.data.url));
});
