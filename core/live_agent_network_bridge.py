"""
Nexus™ Live External Agent Network & API Bridge
===============================================
Establishes real external network connectivity using active API keys in .env:
1. GitHub Issues API (using GITHUB_TOKEN)
2. Supabase Realtime / Postgres Table (using SUPABASE_URL & SUPABASE_SERVICE_KEY)
3. Outbound HTTP Webhook Dispatcher
"""

import os
import logging
import httpx
from typing import Dict, Any, Optional

logger = logging.getLogger("Nexus.LiveAgentBridge")

class LiveAgentNetworkBridge:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN", "").strip()
        self.supabase_url = os.getenv("SUPABASE_URL", "").strip()
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY", os.getenv("SUPABASE_KEY", "")).strip()

    def broadcast_to_github(self, title: str, body: str, repo: str = "devenweb/Air-sass-mauritius") -> Dict[str, Any]:
        """Creates a real GitHub issue on a public repository as an agent broadcast."""
        if not self.github_token:
            return {"success": False, "error": "GITHUB_TOKEN not configured."}

        url = f"https://api.github.com/repos/{repo}/issues"
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        payload = {
            "title": title,
            "body": body,
            "labels": ["agent-broadcast", "micro-ask", "nexus-mesh"]
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                res = client.post(url, json=payload, headers=headers)
                if res.status_code in (200, 201):
                    data = res.json()
                    logger.info(f"[LiveAgentBridge] Successfully posted GitHub issue: {data.get('html_url')}")
                    return {"success": True, "platform": "github", "url": data.get("html_url"), "issue_number": data.get("number")}
                else:
                    return {"success": False, "platform": "github", "status_code": res.status_code, "error": res.text}
        except Exception as e:
            logger.error(f"[LiveAgentBridge] GitHub broadcast error: {e}")
            return {"success": False, "platform": "github", "error": str(e)}

    def broadcast_to_supabase(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Publishes live broadcast event to Supabase database table 'agent_board_broadcasts'."""
        if not self.supabase_url or not self.supabase_key:
            return {"success": False, "error": "Supabase credentials not configured."}

        url = f"{self.supabase_url}/rest/v1/agent_board_broadcasts"
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                res = client.post(url, json=payload, headers=headers)
                if res.status_code in (200, 201):
                    logger.info("[LiveAgentBridge] Successfully synced broadcast to Supabase.")
                    return {"success": True, "platform": "supabase", "data": res.json()}
                else:
                    return {"success": False, "platform": "supabase", "status_code": res.status_code, "error": res.text}
        except Exception as e:
            logger.error(f"[LiveAgentBridge] Supabase broadcast error: {e}")
            return {"success": False, "platform": "supabase", "error": str(e)}

    def dispatch_external_webhook(self, webhook_url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches real HTTP POST payload to any external webhook URL."""
        try:
            with httpx.Client(timeout=10.0) as client:
                res = client.post(webhook_url, json=payload)
                return {"success": res.status_code in (200, 201, 204), "status_code": res.status_code, "response": res.text[:200]}
        except Exception as e:
            return {"success": False, "error": str(e)}

live_agent_network_bridge = LiveAgentNetworkBridge()
