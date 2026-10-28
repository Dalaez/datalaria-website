import subprocess
import time
import os
import socketserver
import threading
from http.server import SimpleHTTPRequestHandler
from PIL import Image

PORT = 5176
STATIC_DIR = os.path.abspath("static/apps/lifeops")
DIR_ES = os.path.abspath("content/es/posts/app-lifeops_part6_analytics_dashboard_360")
DIR_EN = os.path.abspath("content/en/posts/app-lifeops_part6_analytics_dashboard_360")

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)
    def log_message(self, format, *args):
        pass

socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", PORT), Handler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()
print(f"HTTP Server started on port {PORT}")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
user_dir = os.path.abspath("temp_edge_full")

def capture_url(url, out_path, window_size="1440,1350"):
    cmd = [
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--window-size={window_size}",
        "--virtual-time-budget=6000",
        f"--user-data-dir={user_dir}",
        f"--screenshot={out_path}",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Edge error on {url}:", res.stderr)
    else:
        print(f"Captured {out_path} ({os.path.getsize(out_path)} bytes)")

try:
    # 1. Capture Spanish 360 Dashboard
    es_raw = os.path.abspath("scratch/raw_es_360.png")
    capture_url(f"http://localhost:{PORT}/#/?mock=true&lang=es", es_raw)

    # 2. Capture Spanish Sport Drill-down (running)
    es_sport_raw = os.path.abspath("scratch/raw_es_sport.png")
    capture_url(f"http://localhost:{PORT}/#/?mock=true&lang=es&cat=sport&subcat=running", es_sport_raw)

    # 3. Capture English 360 Dashboard
    en_raw = os.path.abspath("scratch/raw_en_360.png")
    capture_url(f"http://localhost:{PORT}/#/?mock=true&lang=en", en_raw)

    # 4. Capture English Sport Drill-down
    en_sport_raw = os.path.abspath("scratch/raw_en_sport.png")
    capture_url(f"http://localhost:{PORT}/#/?mock=true&lang=en&cat=sport&subcat=running", en_sport_raw)

finally:
    httpd.shutdown()
    httpd.server_close()
    print("Captures complete!")
