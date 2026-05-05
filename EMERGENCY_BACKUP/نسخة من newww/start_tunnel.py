from pyngrok import ngrok
import time
url = ngrok.connect(8501, bind_tls=True)
print(f"URL={url.public_url}")
while True:
    time.sleep(10)
