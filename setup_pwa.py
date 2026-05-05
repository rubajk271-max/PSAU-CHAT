import streamlit as st
import os
import shutil

pwa_dir = os.path.dirname(st.__file__)
static_dir = os.path.join(pwa_dir, "static")

manifest = """{
  "name": "PSAU Chat",
  "short_name": "PSAU Chat",
  "theme_color": "#0ABAB5",
  "background_color": "#FFFFFF",
  "display": "standalone",
  "scope": "/",
  "start_url": "/",
  "icons": [
    {
      "src": "logo1.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "logo1.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}"""

sw = """
self.addEventListener('install', function(e) {
  self.skipWaiting();
});

self.addEventListener('activate', function(e) {
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', function(event) {
  // Pass-through fetch for PWA validation
  event.respondWith(
    fetch(event.request).catch(function() {
      return new Response('Offline mode');
    })
  );
});
"""

with open(os.path.join(static_dir, "manifest.json"), "w") as f:
    f.write(manifest)

with open(os.path.join(static_dir, "service-worker.js"), "w") as f:
    f.write(sw)

try:
    shutil.copy("logo1.png", os.path.join(static_dir, "logo1.png"))
except Exception:
    pass

print(f"PWA files deployed to {static_dir}")
