# -*- coding: utf-8 -*-
"""
Nexus Unified Ecosystem Orchestrator (v44.0)
=============================================
Automatically spins up and manages all auxiliary systems when server.py starts:
  1. 24/7 Revenue & Settlement Daemon (Base L2 polling, 14-board outreach, bandit evolution)
  2. Public Cloudflare Tunnel (exposing /api/mesh/inbound and /api/v1/x402/service)
  3. Perpetual Lead Scouring & Cross-Agent Sales Pipeline
  4. Active Agent Standby Elimination & Task Dispatcher (Zero idle agents)
  5. Full Fleet Unrestricted Release & Continuous Background Loops
"""

import os
import sys
import time
import re
import shutil
import threading
import subprocess
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("Nexus.Orchestrator")


def find_cloudflared_bin() -> Optional[str]:
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


class EcosystemOrchestrator:
    def __init__(self):
        self._daemon_thread: Optional[threading.Thread] = None
        self._tunnel_process: Optional[subprocess.Popen] = None
        self._tunnel_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self.public_tunnel_url: Optional[str] = None
        self.started_at: Optional[str] = None
        self.is_running = False

    def start_all(self, port: int = 8000):
        if self.is_running:
            return
        self.is_running = True
        self.started_at = time.strftime("%Y-%m-%d %H:%M:%S")
        self._stop_event.clear()

        # In serverless environments (e.g. Vercel), persistent daemons and subprocess tunnels are bypassed
        if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
            logger.info("[Ecosystem] Running in serverless mode: Background daemon threads bypassed.")
            return

        print("\n\033[1;35m" + "=" * 70)
        print("⚡ NEXUS ECOSYSTEM: ALL SYSTEMS & AGENTS STARTING TOGETHER")
        print("   [1] AI Core Web Server:            http://127.0.0.1:8000")
        print("   [2] Revenue & Settlement Daemon:   Active (Base L2 Poll & 14-Board Outreach)")
        print("   [3] Perpetual Lead Pipeline:       Active (24/7 Global B2B Scouring)")
        print("   [4] Active Agent Standby Killer:   Active (Zero Idle Agents)")
        print("   [5] Fleet Background Loops:        Active (41 Agents Airborne)")
        print("   [6] Cloudflare Tunnel:             Initializing Public Gateway...")
        print("=" * 70 + "\033[0m\n")

        # 1. Start Revenue & Settlement Daemon Thread
        self._start_revenue_daemon()

        # 2. Launch Perpetual Lead Pipeline & Eliminate Standby Agents
        self._launch_agents_and_pipelines()

        # 3. Start Cloudflare Tunnel Subprocess
        if not os.getenv("TESTING") and not os.getenv("VERCEL"):
            self._start_cloudflare_tunnel(port=port)

    def _start_revenue_daemon(self):
        def _daemon_worker():
            from scripts.revenue_daemon import run_daemon_cycle
            logger.info("[Ecosystem] Revenue & Settlement Daemon thread started.")
            time.sleep(3)
            try:
                run_daemon_cycle()
            except Exception as e:
                logger.error(f"[Ecosystem] Initial revenue cycle error: {e}")

            while not self._stop_event.is_set():
                if self._stop_event.wait(900):
                    break
                try:
                    run_daemon_cycle()
                except Exception as e:
                    logger.error(f"[Ecosystem] Recurring revenue cycle error: {e}")

        self._daemon_thread = threading.Thread(target=_daemon_worker, daemon=True, name="NexusRevenueDaemonThread")
        self._daemon_thread.start()

    def _launch_agents_and_pipelines(self):
        def _launch_worker():
            time.sleep(2)
            try:
                # 1. Release locks and launch continuous background loops for all 41 agents
                from core.fleet_ultimate_release import fleet_ultimate_release
                fleet_ultimate_release.release_and_activate_all_agents()
                logger.info("[Ecosystem] All 41 agents launched into continuous background execution loops.")

                # 2. Eliminate standby and assign active work queues
                from core.active_agent_task_dispatcher import active_agent_dispatcher
                active_agent_dispatcher.assign_work_to_all_agents()
                logger.info("[Ecosystem] Active agent task dispatcher executed. Zero standby enforced.")

                # 3. Execute perpetual lead scouring and cross-agent sales dispatch
                from core.perpetual_lead_sales_pipeline import perpetual_lead_sales
                perpetual_lead_sales.execute_perpetual_scour_and_dispatch()
                logger.info("[Ecosystem] Perpetual lead pipeline scouring initiated.")

                # 4. Start 24/7 perpetual lead scouring daemon to continuously fill database
                from core.perpetual_lead_scour_daemon import perpetual_lead_daemon
                perpetual_lead_daemon.start_daemon()
                logger.info("[Ecosystem] Perpetual lead scouring daemon started (filling database 24/7).")
            except Exception as e:
                logger.error(f"[Ecosystem] Error launching agents and pipelines: {e}")

        launch_thread = threading.Thread(target=_launch_worker, daemon=True, name="NexusAgentLaunchThread")
        launch_thread.start()

    def _start_cloudflare_tunnel(self, port: int = 8000):
        cf_bin = find_cloudflared_bin()
        if not cf_bin:
            logger.warning("[Ecosystem] cloudflared binary not found. Public gateway skipped.")
            return

        try:
            cmd = [cf_bin, "tunnel", "--url", f"http://127.0.0.1:{port}"]
            self._tunnel_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )

            def _tunnel_reader():
                url_pattern = re.compile(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com")
                for line in iter(self._tunnel_process.stdout.readline, b""):
                    if self._stop_event.is_set():
                        break
                    text = line.decode("utf-8", errors="replace").rstrip()
                    if not text:
                        continue
                    match = url_pattern.search(text)
                    if match and not self.public_tunnel_url:
                        self.public_tunnel_url = match.group(0)
                        print(f"\n\033[1;32m{'=' * 70}\033[0m")
                        print(f"\033[1;32m🌐 PUBLIC CLOUDFLARE TUNNEL LIVE: {self.public_tunnel_url}\033[0m")
                        print(f"\033[1;36m   • Inbound AI Mesh Webhook: {self.public_tunnel_url}/api/mesh/inbound\033[0m")
                        print(f"\033[1;36m   • HTTP 402 Pay-per-Call:   {self.public_tunnel_url}/api/v1/x402/service\033[0m")
                        print(f"\033[1;32m{'=' * 70}\033[0m\n")

            self._tunnel_thread = threading.Thread(target=_tunnel_reader, daemon=True, name="CloudflareTunnelReader")
            self._tunnel_thread.start()
        except Exception as e:
            logger.error(f"[Ecosystem] Could not start Cloudflare tunnel: {e}")

    def stop_all(self):
        logger.info("[Ecosystem] Shutting down auxiliary systems...")
        self._stop_event.set()
        if self._tunnel_process:
            try:
                self._tunnel_process.terminate()
                self._tunnel_process.wait(timeout=2)
            except Exception:
                try:
                    self._tunnel_process.kill()
                except Exception:
                    pass
            self._tunnel_process = None
        self.is_running = False

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_running": self.is_running,
            "started_at": self.started_at,
            "daemon_active": self._daemon_thread is not None and self._daemon_thread.is_alive(),
            "tunnel_active": self._tunnel_process is not None and self._tunnel_process.poll() is None,
            "public_url": self.public_tunnel_url,
            "inbound_webhook": f"{self.public_tunnel_url}/api/mesh/inbound" if self.public_tunnel_url else None,
            "x402_service": f"{self.public_tunnel_url}/api/v1/x402/service" if self.public_tunnel_url else None
        }


# Global singleton instance
ecosystem_orchestrator = EcosystemOrchestrator()
