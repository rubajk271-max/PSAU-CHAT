import subprocess
import re
import sys

cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:8501", "serveo.net"]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

with open("out_link.txt", "w") as f:
    for line in iter(process.stdout.readline, ""):
        if "https://" in line:
            url = re.search(r'(https://[^\s]+)', line)
            if url:
                f.write(url.group(1))
                break
