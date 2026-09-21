"""
Nexus™ 1-Click Public Tunnel Initiator
======================================
Exposes your local Nexus server (http://127.0.0.1:8000) to the public internet
using free Cloudflare Quick Tunnels (cloudflared) or Localtunnel.
Allows external clients, WhatsApp webhooks, and mobile testers to access /store
and live PayPal checkouts without port forwarding.
"""

import sys
import shutil
import subprocess
import time

def start_tunnel(port: int = 8000):
    print("=" * 60)
    print("🌐 Nexus™ Public Tunnel Starter")
    print(f"Target local server: http://127.0.0.1:{port}")
    print("=" * 60)

    # Check for cloudflared
    if shutil.which("cloudflared"):
        print("[*] Launching Cloudflare Quick Tunnel...")
        cmd = ["cloudflared", "tunnel", "--url", f"http://127.0.0.1:{port}"]
        try:
            subprocess.run(cmd)
            return
        except KeyboardInterrupt:
            print("\n[+] Tunnel stopped.")
            return

    # Check for npx localtunnel
    if shutil.which("npx"):
        print("[*] 'cloudflared' not found. Launching free tunnel via npx localtunnel...")
        cmd = ["npx", "-y", "localtunnel", "--port", str(port)]
        try:
            subprocess.run(cmd)
            return
        except KeyboardInterrupt:
            print("\n[+] Tunnel stopped.")
            return

    print("[-] Neither 'cloudflared' nor 'npx' was detected in PATH.")
    print("[*] To expose your server publicly in 1 step:")
    print("    Option 1: Deploy to Vercel via 'vercel --prod'")
    print("    Option 2: Install Cloudflare Tunnel: https://github.com/cloudflare/cloudflared/releases")
    print("    Option 3: Run 'npm install -g localtunnel' then 'lt --port 8000'")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    start_tunnel(port)
