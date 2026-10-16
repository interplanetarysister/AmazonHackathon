/* Local demonstration notifications only.
 * This worker does not subscribe to push, scan cameras, or poll carrier accounts.
 * Only explicit browser commands trigger showNotification().
 */
self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil((async () => {
    const windows = await self.clients.matchAll({type: 'window', includeUncontrolled: true});
    for (const windowClient of windows) {
      if (windowClient.url.startsWith(self.location.origin + '/')) {
        return windowClient.focus();
      }
    }
    return self.clients.openWindow('/');
  })());
});
