"""
Nexus Ecosystem Unified Supervisor (start_all.py)
==================================================
Starts all core systems in a single terminal with graceful orchestration:
  1. 🧠 Nexus AI Core & Web Dashboard (server.py on http://127.0.0.1:8000)
  2. ⚡ 24/7 Autonomous Revenue & Settlement Daemon (scripts/revenue_daemon.py --loop)
  3. 🌐 Cloudflare Public Tunnel (exposes /api/mesh/inbound & /api/v1/x402/service to the wild web)

Press Ctrl+C at any time to cleanly terminate all processes.
"""

import os
import sys
import time
import re
import signal
import threading
import subprocess
import webbrowser
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent

# Locate Cloudflare binary
def find_cloudflared_bin():
    import shutil
    cli = shutil.which("cloudflared")
    if cli:
        return cli
    candidates = [
        r"C:\Program Files (x86)\cloudflared\cloudflared.exe",
        r"C:\Program Files\cloudflared\cloudflared.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\cloudflared\cloudflared.exe"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Microsoft\WinGet\Packages\Cloudflare.cloudflared_Microsoft.Winget.Source_8wekyb3d8bbwe\cloudflared.exe")
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


processes = []
shutting_down = False
tunnel_url = None


def stream_logs(proc, tag, color_code):
    global tunnel_url
    url_pattern = re.compile(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com")
    reset_code = "\033[0m"

    for line in iter(proc.stdout.readline, b""):
        if shutting_down:
            break
        text = line.decode("utf-8", errors="replace").rstrip()
        if not text:
            continue

        # Detect Cloudflare Tunnel public URL
        if "cloudflared" in tag.lower():
            match = url_pattern.search(text)
            if match and not tunnel_url:
                tunnel_url = match.group(0)
                print(f"\n\033[1;32m{'=' * 70}\033[0m")
                print(f"\033[1;32m🌐 PUBLIC TUNNEL ACTIVE: {tunnel_url}\033[0m")
                print(f"\033[1;36m   • Inbound Bot Webhook: {tunnel_url}/api/mesh/inbound\033[0m")
                print(f"\033[1;36m   • HTTP 402 Paywall:   {tunnel_url}/api/v1/x402/service\033[0m")
                print(f"\033[1;32m{'=' * 70}\033[0m\n")

        print(f"{color_code}[{tag}]{reset_code} {text}")


def shutdown_all(signum=None, frame=None):
    global shutting_down
    if shutting_down:
        return
    shutting_down = True
    print("\n\n\033[1;33m🛑 Shutting down Nexus Ecosystem... Please wait.\033[0m")
    for name, p in reversed(processes):
        try:
            print(f"   Terminating {name} (PID: {p.pid})...")
            p.terminate()
            p.wait(timeout=3)
        except Exception:
            try:
                p.kill()
            except Exception:
                pass
    print("\033[1;32m✅ All Nexus processes stopped cleanly. Good day, Sir.\033[0m")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, shutdown_all)
    signal.signal(signal.SIGTERM, shutdown_all)

    print("\033[1;35m" + "=" * 70)
    print("🚀 NEXUS ALL-IN-ONE SYSTEM SUPERVISOR (v4.0)")
    print("   Starting AI Engine, Revenue Daemon, and Cloudflare Tunnel...")
    print("=" * 70 + "\033[0m\n")

    py_exe = sys.executable

    # 1. Start Nexus Core Server (FastAPI / J.A.R.V.I.S. / Dashboards)
    print("\033[1;34m[1/3] Starting Nexus Core AI Server (server.py on http://127.0.0.1:8000)...\033[0m")
    p_server = subprocess.Popen(
        [py_exe, "server.py"],
        cwd=str(ROOT_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    processes.append(("AI-Core-Server", p_server))
    t1 = threading.Thread(target=stream_logs, args=(p_server, "AI-SERVER", "\033[34m"), daemon=True)
    t1.start()

    time.sleep(2)

    # 2. Start 24/7 Revenue & Settlement Daemon
    print("\033[1;33m[2/3] Starting 24/7 Revenue & Settlement Daemon (revenue_daemon.py --loop)...\033[0m")
    p_daemon = subprocess.Popen(
        [py_exe, "scripts/revenue_daemon.py", "--loop"],
        cwd=str(ROOT_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    processes.append(("Revenue-Daemon", p_daemon))
    t2 = threading.Thread(target=stream_logs, args=(p_daemon, "REVENUE-DAEMON", "\033[33m"), daemon=True)
    t2.start()

    time.sleep(1)

    # 3. Start Cloudflare Tunnel
    cf_bin = find_cloudflared_bin()
    if cf_bin:
        print(f"\033[1;32m[3/3] Starting Cloudflare Public Tunnel ({cf_bin})...\033[0m")
        p_tunnel = subprocess.Popen(
            [cf_bin, "tunnel", "--url", "http://127.0.0.1:8000"],
            cwd=str(ROOT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        processes.append(("Cloudflare-Tunnel", p_tunnel))
        t3 = threading.Thread(target=stream_logs, args=(p_tunnel, "TUNNEL", "\033[32m"), daemon=True)
        t3.start()
    else:
        print("\033[1;31m[3/3] Cloudflare Tunnel binary not found. Skipping public gateway.\033[0m")

    # Open local dashboard
    try:
        webbrowser.open("http://localhost:8000")
    except Exception:
        pass

    print("\n\033[1;32m✨ All services are LIVE! Local Dashboard: http://localhost:8000\033[0m")
    print("\033[1;37mPress Ctrl+C to terminate all services.\033[0m\n")

    # Monitor loop
    try:
        while True:
            time.sleep(1)
            for name, p in processes:
                code = p.poll()
                if code is not None and not shutting_down:
                    print(f"\n\033[1;31m⚠️ Process '{name}' exited with code {code}!\033[0m")
    except KeyboardInterrupt:
        shutdown_all()


if __name__ == "__main__":
    main()
