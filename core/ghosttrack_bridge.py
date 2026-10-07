"""
Nexus™ GhostTrack Pro OSINT & Reconnaissance Bridge
===================================================
Binds GhostTrack Pro intelligence capabilities into the central ToolRegistry
so all agents can leverage asynchronous username recon, email MX validation,
Mauritius Yellow Pages (yellow.mu & yellow-pages.mu), and domain intelligence.
"""

import os
import sys
import json
import time
import asyncio
import aiohttp
import requests
import random
import logging
from typing import Dict, Any, List

logger = logging.getLogger("Nexus.GhostTrackBridge")

# Ensure GhostTrack path
ghost_dir = os.path.abspath(".artifacts/scratch/GhostTrack")
if ghost_dir not in sys.path:
    sys.path.insert(0, ghost_dir)

class GhostTrackBridge:
    """
    Exposes GhostTrack Pro OSINT capabilities as executable agent tools.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GhostTrackBridge, cls).__new__(cls)
            cls._instance._register_tools()
        return cls._instance

    def _register_tools(self):
        try:
            from core.tool_registry import tool_registry, AgentTool

            tool_registry.register(AgentTool(
                name="ghosttrack_username_recon",
                description="Performs rapid asynchronous username reconnaissance across social platforms via GhostTrack Pro.",
                category="osint",
                func=self.run_username_recon,
                parameters_schema={"username": "string"}
            ))

            tool_registry.register(AgentTool(
                name="ghosttrack_domain_recon",
                description="Performs DNS resolution and HTTP server reconnaissance on a target domain via GhostTrack Pro.",
                category="osint",
                func=self.run_domain_recon,
                parameters_schema={"domain": "string"}
            ))

            tool_registry.register(AgentTool(
                name="ghosttrack_mauritius_directory_search",
                description="Searches Mauritius Yellow Pages (yellow.mu and yellow-pages.mu) for business and contact information.",
                category="osint",
                func=self.run_mauritius_directory_search,
                parameters_schema={"query": "string"}
            ))
            logger.info("[GhostTrackBridge] Successfully registered GhostTrack Pro OSINT tools including Mauritius Yellow Pages.")
        except Exception as e:
            logger.error(f"[GhostTrackBridge] Failed to register tools: {e}")

    def run_username_recon(self, username: str) -> Dict[str, Any]:
        """Runs async username reconnaissance."""
        async def _recon():
            social_media = [
                {"url": "https://www.facebook.com/{}", "name": "Facebook"},
                {"url": "https://www.twitter.com/{}", "name": "Twitter"},
                {"url": "https://www.instagram.com/{}", "name": "Instagram"},
                {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
                {"url": "https://www.github.com/{}", "name": "GitHub"},
                {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
                {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
                {"url": "https://www.telegram.me/{}", "name": "Telegram"}
            ]
            results = {}
            async with aiohttp.ClientSession() as session:
                for site in social_media:
                    url = site['url'].format(username)
                    try:
                        async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=4) as resp:
                            if resp.status == 200:
                                results[site['name']] = url
                    except Exception:
                        pass
            return results

        try:
            import nest_asyncio
            nest_asyncio.apply()
            res = asyncio.run(_recon())
            return {"success": True, "username": username, "found_profiles": res}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_domain_recon(self, domain: str) -> Dict[str, Any]:
        """Runs domain DNS & HTTP server reconnaissance."""
        try:
            import socket
            ip = socket.gethostbyname(domain)
            server = "N/A"
            try:
                resp = requests.get(f"https://{domain}", timeout=4)
                server = resp.headers.get("Server", "Hidden")
            except Exception:
                pass
            return {
                "success": True,
                "domain": domain,
                "resolved_ip": ip,
                "server_header": server
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_mauritius_directory_search(self, query: str) -> Dict[str, Any]:
        """Searches yellow.mu and yellow-pages.mu for Mauritius business/contact info."""
        try:
            from bs4 import BeautifulSoup
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            ddg_url = f"https://html.duckduckgo.com/html/?q=site:yellow.mu+OR+site:yellow-pages.mu+{query}"
            resp = requests.get(ddg_url, headers=headers, timeout=8)
            matches = []
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                for a in soup.select('.result__snippet, .result__title'):
                    text = a.get_text(strip=True)
                    if text:
                        matches.append(text)
            return {
                "success": True,
                "query": query,
                "sources": ["yellow.mu", "yellow-pages.mu"],
                "matches": matches[:10]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

ghosttrack_bridge = GhostTrackBridge()
