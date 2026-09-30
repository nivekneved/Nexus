"""
Nexus Public Gateway & Inbound Mesh Proxy Manager
=================================================
Exposes Nexus's machine endpoints (/api/mesh/inbound, /api/v1/x402/service)
to the public internet via free Cloudflare Tunnel or Ngrok.
Enables external autonomous bots across Moltbook, Virtuals, and AgentVerse
to trigger live requests and pay directly.
"""

import os
import sys
import shutil
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Nexus.PublicTunnel")


def find_cloudflared_bin():
    cli = shutil.which("cloudflared")
    if cli:
        return cli
    candidate_paths = [
        r"C:\Program Files (x86)\cloudflared\cloudflared.exe",
        r"C:\Program Files\cloudflared\cloudflared.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\cloudflared\cloudflared.exe"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Microsoft\WinGet\Packages\Cloudflare.cloudflared_Microsoft.Winget.Source_8wekyb3d8bbwe\cloudflared.exe")
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            return p
    return None

def detect_tunnels():
    cf_bin = find_cloudflared_bin()
    has_ngrok = shutil.which("ngrok") is not None
    return cf_bin, has_ngrok


def main():
    cf_bin, has_ng = detect_tunnels()
    port = 8000

    print("=" * 65)
    print("🌐 Nexus Inbound Mesh & Public Gateway Manager")
    print("=" * 65)
    print(f"Target Service: http://localhost:{port}")
    print(f"Target Endpoints: /api/mesh/inbound, /api/v1/x402/service, /api/boards/feed\n")

    if cf_bin:
        print(f"✅ Found Cloudflare Tunnel at '{cf_bin}'. Launching free quick tunnel...")
        print("Press Ctrl+C to terminate the tunnel.\n")
        cmd = [cf_bin, "tunnel", "--url", f"http://localhost:{port}"]
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\nCloudflare tunnel terminated.")
        except KeyboardInterrupt:
            print("\nCloudflare tunnel terminated.")
    elif has_ng:
        print("✅ Found Ngrok ('ngrok'). Launching HTTP tunnel...")
        print("Press Ctrl+C to terminate the tunnel.\n")
        cmd = ["ngrok", "http", str(port)]
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\nNgrok tunnel terminated.")
    else:
        print("ℹ️ No tunnel CLI found on system PATH.")
        print("\nTo expose your agent endpoints to the public web for free:")
        print("Option A (Recommended - 100% Free, No Account Needed):")
        print("  1. Download cloudflared: winget install Cloudflare.cloudflared")
        print("  2. Run: python scripts/start_public_tunnel.py")
        print("\nOption B (Ngrok):")
        print("  1. Download ngrok: winget install ngrok")
        print("  2. Run: python scripts/start_public_tunnel.py")
        print("=" * 65)


if __name__ == "__main__":
    main()
