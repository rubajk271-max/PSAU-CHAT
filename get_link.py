import subprocess
import re
import sys
import time

print("Starting secure tunnel... Please hold.")
try:
    # We use pinggy because it is extremely stable
    cmd = ["ssh", "-p", "443", "-o", "StrictHostKeyChecking=no", "-R0:localhost:8501", "a.pinggy.io"]
    
    process = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        text=True
    )
    
    # Pinggy output takes a few seconds to print the URL block
    url = None
    for line in iter(process.stdout.readline, ""):
        print(line, end="") # Print to terminal so user sees it live
        if "https://" in line and (".pinggy.link" in line or ".pinggy.io" in line):
            url = re.search(r'(https://[^\s]+)', line)
            if url:
                print("\n" + "="*50)
                print(f"✅ SUCCESS! Your mobile link is: \n👉 {url.group(1)} 👈")
                print("="*50)
                print("\n(Leave this terminal open to keep the link active!)")
                break
                
    # Wait for natural termination
    process.wait()

except KeyboardInterrupt:
    print("\nTunnel closed.")
except Exception as e:
    print(f"Error: {e}")
