import ssl
import urllib.request
import time

# Bypass SSL verification for internal Python requests
ssl._create_default_https_context = ssl._create_unverified_context

import pyngrok
from pyngrok import ngrok

print("Starting ngrok...")
url = ngrok.connect(8501, bind_tls=True)
print(f"URL: {url.public_url}")

with open("ngrok_url.txt", "w") as f:
    f.write(url.public_url)

while True:
    time.sleep(10)
