"""
Nexus Public Gateway & Inbound Mesh Proxy Manager
=================================================
Exposes Nexus's machine endpoints (/api/mesh/inbound, /api/v1/x402/service)
to the public internet via free Cloudflare Tunnel or Ngrok.
Enables external autonomous bots across Moltbook, Virtuals, and AgentVerse
to trigger live requests and pay directly.
"""

import sys
import shutil
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Nexus.PublicTunnel")


def detect_tunnels():
    has_cloudflared = shutil.which("cloudflared") is not None
    has_ngrok = shutil.which("ngrok") is not None
    return has_cloudflared, has_ngrok


def main():
    has_cf, has_ng = detect_tunnels()
    port = 8000

    print("=" * 65)
    print("🌐 Nexus Inbound Mesh & Public Gateway Manager")
    print("=" * 65)
    print(f"Target Service: http://localhost:{port}")
    print(f"Target Endpoints: /api/mesh/inbound, /api/v1/x402/service, /api/boards/feed\n")

    if has_cf:
        print("✅ Found Cloudflare Tunnel ('cloudflared'). Launching free quick tunnel...")
        print("Press Ctrl+C to terminate the tunnel.\n")
        cmd = ["cloudflared", "tunnel", "--url", f"http://localhost:{port}"]
        try:
            subprocess.run(cmd)
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
