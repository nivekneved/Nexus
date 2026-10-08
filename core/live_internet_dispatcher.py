# -*- coding: utf-8 -*-
"""
Nexus™ True Live Public Internet Request Dispatcher (v15.0)
============================================================
Enables real, live outbound HTTP/HTTPS requests over the public internet to public
APIs, webhooks, and enterprise registries, removing all local simulation fallbacks.
"""

import logging
import httpx
from typing import Dict, Any, Optional
from core.telemetry import telemetry

logger = logging.getLogger("Nexus.LiveInternetDispatcher")

class LiveInternetDispatcher:
    @staticmethod
    def dispatch_live_public_request(url: str, method: str = "GET", payload: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Executes a real outbound HTTP/HTTPS request across the public internet.
        """
        start_time = httpx.time.time() if hasattr(httpx, "time") else 0
        import time
        t0 = time.time()

        default_headers = {
            "User-Agent": "Nexus-Sovereign-Agent/13.0 (Autonomous M2M Node)",
            "Accept": "application/json"
        }
        if headers:
            default_headers.update(headers)

        try:
            logger.info(f"[LiveInternetDispatcher] Dispatching live {method} request to public URL: {url}")
            with httpx.Client(timeout=15.0, follow_redirects=True) as client:
                if method.upper() == "POST":
                    resp = client.post(url, json=payload or {}, headers=default_headers)
                else:
                    resp = client.get(url, headers=default_headers)

            elapsed_ms = (time.time() - t0) * 1000.0

            telemetry.emit(
                agent_id="executive_partner",
                agent_name="Executive Revenue Partner",
                step="LIVE_PUBLIC_INTERNET_REQUEST_SUCCESS",
                file_used="core/live_internet_dispatcher.py",
                message=f"Live public internet request to {url} returned status {resp.status_code} in {elapsed_ms:.1f}ms.",
                level="SUCCESS"
            )

            return {
                "success": True,
                "mode": "LIVE_PUBLIC_INTERNET",
                "url": url,
                "status_code": resp.status_code,
                "execution_time_ms": elapsed_ms,
                "response_body": resp.text[:2000] if resp.text else ""
            }
        except Exception as e:
            elapsed_ms = (time.time() - t0) * 1000.0
            logger.error(f"[LiveInternetDispatcher] Failed live public request to {url}: {e}")

            telemetry.emit(
                agent_id="executive_partner",
                agent_name="Executive Revenue Partner",
                step="LIVE_PUBLIC_INTERNET_REQUEST_ERROR",
                file_used="core/live_internet_dispatcher.py",
                message=f"Live public internet request to {url} failed: {e}",
                level="ERROR"
            )

            return {
                "success": False,
                "mode": "LIVE_PUBLIC_INTERNET",
                "url": url,
                "error": str(e),
                "execution_time_ms": elapsed_ms
            }

live_internet_dispatcher = LiveInternetDispatcher()
