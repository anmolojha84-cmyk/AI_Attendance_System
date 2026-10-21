import os
import sys
import time
import re
import subprocess

os.environ["PYTHONIOENCODING"] = "utf-8"
app_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(app_dir)

cloudflared_path = os.path.join(app_dir, "cloudflared.exe")
log_path = os.path.join(app_dir, "tunnel.log")

print("=" * 65)
print("          AI SMART ATTENDANCE MONITORING SYSTEM")
print("          Designed for Laptop and Phone (Cross-Platform)")
print("=" * 65)
print("\n[1/3] Initializing Cloudflare Secure Live Tunnel...")

if os.path.exists(log_path):
    try:
        os.remove(log_path)
    except Exception:
        pass

tunnel_proc = subprocess.Popen(
    [cloudflared_path, "tunnel", "--edge-ip-version", "4", "--url", "http://localhost:8501"],
    stdout=open(log_path, "w", encoding="utf-8", errors="ignore"),
    stderr=subprocess.STDOUT
)

live_url = None
print("[2/3] Generating live public URL for Mobile access...")
for _ in range(20):
    time.sleep(1)
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                match = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", content)
                if match:
                    live_url = match.group(0)
                    break
        except Exception:
            pass

print("\n" + "=" * 65)
print("               >>> APPLICATION IS READY <<<")
print("=" * 65)
print("  💻 LAPTOP / LOCALHOST :  http://localhost:8501")
if live_url:
    print(f"  📱 PHONE / PUBLIC URL :  {live_url}")
else:
    print("  📱 PHONE / PUBLIC URL :  (Tunnel starting in background)")
print("=" * 65)
print("\n[3/3] Starting Web Application Engine...\n")

try:
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
        "--server.address", "0.0.0.0",
        "--server.port", "8501",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ])
except KeyboardInterrupt:
    print("\nShutting down server...")
finally:
    try:
        tunnel_proc.terminate()
    except Exception:
        pass
