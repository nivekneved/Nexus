# -*- coding: utf-8 -*-
"""
Nexus™ Universal Agent Internet & Unsandboxed Execution Bridge (v70.0)
======================================================================
Provides each and every agent across the entire Nexus fleet with:
1. Free, unrestricted outbound HTTP/HTTPS access to the public internet (APIs, webhooks, portals).
2. Live public web search capabilities (DuckDuckGo, Wikipedia, Google Scrape).
3. Stealth web scraping and DOM extraction without anti-bot blockage.
4. Unsandboxed code execution allowing direct OS, socket, file, and sub-process execution.
5. Bidirectional external agent network broadcasting (GitHub, Supabase, webhooks).
"""

import os
import sys
import time
import json
import logging
import urllib.request
import urllib.parse
import re
import subprocess
import tempfile
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("Nexus.AgentInternetBridge")

# Common realistic desktop browser headers for bypass
DEFAULT_BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
    "DNT": "1",
    "Sec-Ch-Ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
}

class AgentInternetBridge:
    """
    Universal gateway unlocking live internet access and unsandboxed execution
    for every digital employee and subagent in the workforce.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentInternetBridge, cls).__new__(cls)
            cls._instance.total_requests = 0
            cls._instance.total_searches = 0
            cls._instance.total_scrapes = 0
            cls._instance.total_unsandboxed_runs = 0
        return cls._instance

    # =========================================================================
    # 1. LIVE PUBLIC HTTP/HTTPS DISPATCH
    # =========================================================================
    def fetch_public_url(
        self,
        url: str,
        method: str = "GET",
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 15.0
    ) -> Dict[str, Any]:
        """
        Executes a real outbound HTTP/HTTPS request across the public internet.
        Supports GET, POST, PUT, DELETE, PATCH with JSON or text bodies.
        """
        self.total_requests += 1
        t0 = time.time()
        logger.info(f"[InternetBridge] 🌐 Dispatching live {method.upper()} to: {url}")

        merged_headers = dict(DEFAULT_BROWSER_HEADERS)
        if headers:
            merged_headers.update(headers)

        # Try with pooled httpx client from core.http_pool first
        try:
            from core.http_pool import cached_sync_request
            pooled = cached_sync_request(
                method=method,
                url=url,
                ttl_seconds=300 if method.upper() == "GET" else 0,
                headers=merged_headers,
                json_payload=payload,
                timeout=timeout
            )
            pooled["mode"] = "LIVE_PUBLIC_INTERNET_POOLED"
            return pooled
        except Exception as e_httpx:
            err_str = str(e_httpx)
            if "11001" in err_str or "getaddrinfo failed" in err_str or "Name or service not known" in err_str:
                elapsed_ms = (time.time() - t0) * 1000.0
                return {
                    "success": False,
                    "mode": "DNS_UNRESOLVABLE_FAST_FAIL",
                    "error": err_str,
                    "url": url,
                    "execution_time_ms": round(elapsed_ms, 1)
                }
            logger.warning(f"[InternetBridge] Pooled httpx failed ({e_httpx}), attempting urllib fallback...")

        # Urllib fallback
        try:
            req_data = None
            if payload is not None and method.upper() in ("POST", "PUT", "PATCH"):
                req_data = json.dumps(payload).encode("utf-8")
                merged_headers["Content-Type"] = "application/json"

            req = urllib.request.Request(url, data=req_data, headers=merged_headers, method=method.upper())
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                elapsed_ms = (time.time() - t0) * 1000.0
                return {
                    "success": 200 <= resp.status < 400,
                    "mode": "LIVE_PUBLIC_INTERNET_FALLBACK",
                    "status_code": resp.status,
                    "url": url,
                    "execution_time_ms": round(elapsed_ms, 1),
                    "content": body[:10000],
                    "headers": dict(resp.headers)
                }
        except Exception as e:
            elapsed_ms = (time.time() - t0) * 1000.0
            logger.error(f"[InternetBridge] Outbound HTTP failed to {url}: {e}")
            return {
                "success": False,
                "mode": "LIVE_PUBLIC_INTERNET",
                "error": str(e),
                "url": url,
                "execution_time_ms": round(elapsed_ms, 1)
            }

    # =========================================================================
    # 2. LIVE PUBLIC WEB SEARCH
    # =========================================================================
    def search_public_web(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Searches the live public internet for current trends, leads, documentation,
        and market intelligence using multi-engine search aggregators.
        """
        self.total_searches += 1
        t0 = time.time()
        logger.info(f"[InternetBridge] 🔍 Querying public search for: '{query}'")

        results = []

        # Attempt 1: DuckDuckGo Instant Answer JSON API
        try:
            enc_q = urllib.parse.quote_plus(query)
            ddg_api = f"https://api.duckduckgo.com/?q={enc_q}&format=json&no_html=1&skip_disambig=1"
            req = urllib.request.Request(ddg_api, headers=DEFAULT_BROWSER_HEADERS)
            with urllib.request.urlopen(req, timeout=8) as r:
                data = json.loads(r.read().decode("utf-8", errors="replace"))
                if data.get("AbstractText"):
                    results.append({
                        "title": data.get("Heading", query),
                        "url": data.get("AbstractURL", ""),
                        "snippet": data.get("AbstractText", ""),
                        "source": "DuckDuckGo Instant Answer"
                    })
                for topic in data.get("RelatedTopics", [])[:max_results]:
                    if isinstance(topic, dict) and "Text" in topic:
                        results.append({
                            "title": topic.get("Text", "").split(" - ")[0],
                            "url": topic.get("FirstURL", ""),
                            "snippet": topic.get("Text", ""),
                            "source": "DuckDuckGo Topic"
                        })
        except Exception as e:
            logger.debug(f"[InternetBridge] DuckDuckGo API note: {e}")

        # Attempt 2: DuckDuckGo HTML Scraper Fallback if more results needed
        if len(results) < max_results:
            try:
                enc_q = urllib.parse.quote_plus(query)
                ddg_html_url = f"https://html.duckduckgo.com/html/?q={enc_q}"
                req = urllib.request.Request(ddg_html_url, headers=DEFAULT_BROWSER_HEADERS)
                with urllib.request.urlopen(req, timeout=8) as r:
                    html_content = r.read().decode("utf-8", errors="replace")
                    matches = re.findall(
                        r'<a class="result__url"[^>]*href="([^"]+)"[^>]*>.*?</a>.*?<a class="result__snippet"[^>]*>(.*?)</a>',
                        html_content,
                        re.DOTALL
                    )
                    for link, snip in matches[:max_results]:
                        clean_snip = re.sub(r"<[^>]+>", "", snip).strip()
                        if link and clean_snip:
                            results.append({
                                "title": query,
                                "url": link.strip(),
                                "snippet": clean_snip,
                                "source": "DuckDuckGo Web"
                            })
            except Exception as e:
                logger.debug(f"[InternetBridge] DuckDuckGo HTML scraper note: {e}")

        # Attempt 3: Wikipedia Summary API if still sparse
        if len(results) < 2:
            try:
                wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
                req = urllib.request.Request(wiki_url, headers=DEFAULT_BROWSER_HEADERS)
                with urllib.request.urlopen(req, timeout=8) as r:
                    wdata = json.loads(r.read().decode("utf-8", errors="replace"))
                    if wdata.get("extract"):
                        results.append({
                            "title": wdata.get("title", query),
                            "url": wdata.get("content_urls", {}).get("desktop", {}).get("page", ""),
                            "snippet": wdata.get("extract", ""),
                            "source": "Wikipedia Global Knowledge"
                        })
            except Exception:
                pass

        elapsed_ms = (time.time() - t0) * 1000.0
        return {
            "success": len(results) > 0,
            "query": query,
            "results_count": len(results[:max_results]),
            "results": results[:max_results],
            "execution_time_ms": round(elapsed_ms, 1)
        }

    # =========================================================================
    # 3. STEALTH WEBPAGE SCRAPING & TEXT EXTRACTION
    # =========================================================================
    def scrape_webpage(self, url: str, max_chars: int = 8000) -> Dict[str, Any]:
        """
        Extracts clean readable text, headings, and links from any public webpage
        bypassing anti-bot checks via stealth camouflage.
        """
        self.total_scrapes += 1
        t0 = time.time()
        logger.info(f"[InternetBridge] 🕷️ Scraping webpage: {url}")

        # Use StealthScraperBridge if available
        try:
            from core.stealth_scraper_bridge import stealth_scraper
            res = stealth_scraper.fetch_stealth(url)
            html = res.get("html", "")
            if html:
                # Strip scripts, styles, and extract text
                clean_text = re.sub(r"<(script|style|nav|footer)[^>]*>.*?</\1>", " ", html, flags=re.DOTALL | re.IGNORECASE)
                clean_text = re.sub(r"<[^>]+>", " ", clean_text)
                clean_text = re.sub(r"\s+", " ", clean_text).strip()
                title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE)
                title = title_match.group(1).strip() if title_match else ""

                elapsed_ms = (time.time() - t0) * 1000.0
                return {
                    "success": True,
                    "url": url,
                    "title": title,
                    "text_preview": clean_text[:max_chars],
                    "total_length": len(clean_text),
                    "execution_time_ms": round(elapsed_ms, 1),
                    "engine": "StealthScraperBridge"
                }
        except Exception as e:
            logger.warning(f"[InternetBridge] Stealth scraper exception: {e}")

        # Fallback to direct fetch
        fetch_res = self.fetch_public_url(url)
        if fetch_res.get("success"):
            html = fetch_res.get("content", "")
            clean_text = re.sub(r"<(script|style|nav|footer)[^>]*>.*?</\1>", " ", html, flags=re.DOTALL | re.IGNORECASE)
            clean_text = re.sub(r"<[^>]+>", " ", clean_text)
            clean_text = re.sub(r"\s+", " ", clean_text).strip()
            return {
                "success": True,
                "url": url,
                "text_preview": clean_text[:max_chars],
                "total_length": len(clean_text),
                "engine": "Standard HTTP Fetcher"
            }

        return {"success": False, "url": url, "error": fetch_res.get("error", "Failed to retrieve page content.")}

    # =========================================================================
    # 4. UNSANDBOXED REAL CODE EXECUTION
    # =========================================================================
    def execute_unsandboxed_code(
        self,
        code_str: str,
        timeout: float = 30.0,
        working_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes Python code freely and completely outside any sandbox.
        Allows real file I/O, outbound socket connections, multiprocessing, and OS operations.
        """
        self.total_unsandboxed_runs += 1
        t0 = time.time()
        logger.info("[InternetBridge] ⚡ Executing unsandboxed Python code...")

        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cwd = working_dir or root_dir

        tmp_file = None
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
                f.write("# -*- coding: utf-8 -*-\n")
                f.write("import sys, os\n")
                f.write(f"sys.path.insert(0, r'{root_dir}')\n")
                f.write(code_str)
                tmp_file = f.name

            res = subprocess.run(
                [sys.executable, tmp_file],
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            elapsed_ms = (time.time() - t0) * 1000.0
            return {
                "success": res.returncode == 0,
                "mode": "UNSANDBOXED_SOVEREIGN_EXECUTION",
                "exit_code": res.returncode,
                "stdout": res.stdout[:15000],
                "stderr": res.stderr[:5000],
                "execution_time_ms": round(elapsed_ms, 1)
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "mode": "UNSANDBOXED_SOVEREIGN_EXECUTION",
                "error": f"Execution timed out after {timeout} seconds.",
                "timeout": timeout
            }
        except Exception as e:
            return {
                "success": False,
                "mode": "UNSANDBOXED_SOVEREIGN_EXECUTION",
                "error": str(e)
            }
        finally:
            if tmp_file and os.path.exists(tmp_file):
                try:
                    os.remove(tmp_file)
                except Exception:
                    pass

    # =========================================================================
    # 5. EXTERNAL AGENT NETWORK & BROADCAST BRIDGE
    # =========================================================================
    def broadcast_to_agent_network(
        self,
        platform: str = "webhook",
        title: str = "",
        content: str = "",
        target_url: Optional[str] = None,
        message: Optional[str] = None,
        channel: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Broadcasts intelligence, requests, or products directly to external platforms
        (GitHub issues, Supabase realtime mesh, Discord/Slack webhooks).
        """
        if message and not content:
            content = message
        if channel and not platform:
            platform = channel
        if not title:
            title = f"Agent Fleet Broadcast [{time.strftime('%Y-%m-%d %H:%M:%S')}]"

        try:
            from core.live_agent_network_bridge import live_agent_network_bridge
            p = (platform or "webhook").lower()
            if p == "github":
                return live_agent_network_bridge.broadcast_to_github(title=title, body=content)
            elif p == "supabase":
                payload = {"title": title, "content": content, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
                if metadata:
                    payload.update(metadata)
                return live_agent_network_bridge.broadcast_to_supabase(payload)
            elif p in ("webhook", "discord", "slack") and target_url:
                payload = {"title": title, "content": content}
                if metadata:
                    payload.update(metadata)
                return live_agent_network_bridge.dispatch_external_webhook(target_url, payload)
            else:
                # Mesh internal routing fallback
                return {
                    "success": True,
                    "mode": "INTERNAL_MESH_BROADCAST",
                    "channel": platform,
                    "title": title,
                    "content": content
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # =========================================================================
    # 5.5 ARGON MAX PROTOCOL-LEVEL OSINT (CERTIFICATE TRANSPARENCY & TECH FINGERPRINTING)
    # =========================================================================
    def discover_live_ct_domains(self, pattern: str = "%.mu", limit: int = 15) -> Dict[str, Any]:
        """
        Queries Certificate Transparency (CT) logs via crt.sh JSON protocol to discover
        newly issued SSL certificates and live commercial domains in real time.
        """
        t0 = time.time()
        enc_q = urllib.parse.quote(pattern)
        ct_url = f"https://crt.sh/?q={enc_q}&output=json"
        domains = []
        seen = set()
        try:
            res = self.fetch_public_url(ct_url, timeout=10.0)
            if res.get("success") and res.get("content"):
                entries = json.loads(res["content"])
                for item in entries:
                    name_val = (item.get("common_name") or item.get("name_value") or "").strip().lower()
                    for line in name_val.splitlines():
                        clean_d = line.lstrip("*.").strip()
                        if clean_d and "." in clean_d and clean_d not in seen:
                            seen.add(clean_d)
                            domains.append({
                                "domain": clean_d,
                                "issuer": item.get("issuer_name", "")[:80],
                                "logged_at": item.get("entry_timestamp", "")
                            })
                            if len(domains) >= limit:
                                break
                    if len(domains) >= limit:
                        break
        except Exception as e:
            logger.debug(f"[InternetBridge] CT log query note: {e}")

        return {
            "success": len(domains) > 0,
            "pattern": pattern,
            "domains_discovered": len(domains),
            "domains": domains,
            "execution_time_ms": round((time.time() - t0) * 1000.0, 1)
        }

    def fingerprint_domain_buying_signals(self, url_or_domain: str) -> Dict[str, Any]:
        """
        Inspects a live prospect website's DOM and HTTP headers for B2B buying signals:
        - Missing WhatsApp Concierge widget (wa.me / api.whatsapp.com)
        - Missing instant booking / appointment widget
        - Expensive legacy SaaS bloat (Intercom, HubSpot, Zendesk, Drift, Calendly)
        - Exposed contact emails and phone numbers
        """
        target_url = url_or_domain.strip()
        if not target_url.startswith("http"):
            target_url = f"https://{target_url}"

        res = self.fetch_public_url(target_url, timeout=10.0)
        html = (res.get("content") or "").lower()
        headers = res.get("headers") or {}

        has_whatsapp = ("wa.me/" in html) or ("api.whatsapp.com" in html) or ("whatsapp" in html)
        has_booking = any(k in html for k in ["calendly", "book-now", "reservation", "appointment", "booking"])
        expensive_saas = [
            saas for saas in ["intercom", "hubspot", "zendesk", "drift", "salesforce", "freshdesk", "mailchimp"]
            if saas in html
        ]
        emails_found = list(set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", res.get("content") or "")))[:5]

        recommended_pitch_angle = (
            "Missing 24/7 WhatsApp AI Booking Concierge — high nocturnal lead leakage"
            if not has_whatsapp else
            (f"Replace expensive {', '.join(expensive_saas)} subscription with Sovereign Nexus AI"
             if expensive_saas else "Upgrade static contact form to autonomous bilingual AI closing funnel")
        )

        return {
            "success": res.get("success", False),
            "url": target_url,
            "server": headers.get("server", "Unknown"),
            "has_whatsapp_widget": has_whatsapp,
            "has_booking_engine": has_booking,
            "legacy_saas_detected": expensive_saas,
            "emails_extracted": emails_found,
            "recommended_pitch_angle": recommended_pitch_angle
        }

    # =========================================================================
    # 6. UNIVERSAL AGENT INJECTION
    # =========================================================================
    def inject_into_agent(self, agent) -> bool:
        """Dynamically binds sovereign capabilities onto a single agent instance."""
        if not agent:
            return False
        agent.fetch_public_url = self.fetch_public_url
        agent.search_public_web = self.search_public_web
        agent.scrape_webpage = self.scrape_webpage
        agent.execute_unsandboxed_code = self.execute_unsandboxed_code
        agent.broadcast_to_agent_network = self.broadcast_to_agent_network
        agent.discover_live_ct_domains = self.discover_live_ct_domains
        agent.fingerprint_domain_buying_signals = self.fingerprint_domain_buying_signals
        agent.is_sandbox_free = True
        agent.internet_access_enabled = True
        return True

    def inject_into_all_agents(self, manager=None) -> Dict[str, Any]:
        """
        Dynamically attaches direct internet and unsandboxed execution capabilities
        onto each and every agent registered in the Nexus workforce.
        """
        if manager is None:
            from core.agent_manager import AgentManager
            manager = AgentManager()

        upgraded = []
        all_agents = dict(manager.agents)
        all_agents.update(manager.domain_controllers)

        for aid, agent in all_agents.items():
            # 1. Bind live internet methods directly
            agent.fetch_public_url = self.fetch_public_url
            agent.search_public_web = self.search_public_web
            agent.scrape_webpage = self.scrape_webpage
            agent.execute_unsandboxed_code = self.execute_unsandboxed_code
            agent.broadcast_to_agent_network = self.broadcast_to_agent_network

            # 2. Set sovereign flags
            agent.is_sandbox_free = True
            agent.internet_access_enabled = True

            upgraded.append(aid)

        logger.info(f"[InternetBridge] 🚀 Successfully injected live internet & unsandboxed bridge into all {len(upgraded)} agents.")
        return {
            "success": True,
            "version": "v70.0 Universal Agent Internet & Unsandboxed Bridge",
            "agents_upgraded_count": len(upgraded),
            "upgraded_agent_ids": upgraded,
            "capabilities_injected": [
                "fetch_public_url",
                "search_public_web",
                "scrape_webpage",
                "execute_unsandboxed_code",
                "broadcast_to_agent_network"
            ]
        }


# Singleton Instance
agent_internet_bridge = AgentInternetBridge()
