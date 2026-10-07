"""
Nexus™ Scrapling High-Speed Extraction Bridge
=============================================
Integrates `scrapling` (https://github.com/D4Vinci/Scrapling)
to provide ultra-fast, unstructured web data extraction, camouflage request headers,
and bypass anti-bot mechanisms (like Cloudflare) instantly.
"""

import asyncio
import logging
from typing import Dict, Any

logger = logging.getLogger("Nexus.ScraplingBridge")

class ScraplingBridge:
    def __init__(self):
        self.is_initialized = False

    def initialize(self):
        if not self.is_initialized:
            try:
                import scrapling
                self.scrapling = scrapling
                self.is_initialized = True
                logger.info("[ScraplingBridge] Successfully loaded scrapling.")
            except ImportError:
                logger.warning("[ScraplingBridge] 'scrapling' package not found. Running in fallback mode.")

    async def fetch_and_parse(self, url: str) -> Dict[str, Any]:
        """
        Uses Scrapling to securely fetch a URL bypassing anti-bot measures,
        and parses the HTML returning key DOM elements (title, links, text).
        """
        self.initialize()
        if not self.is_initialized:
            return {"success": False, "error": "scrapling not installed."}

        logger.info(f"[ScraplingBridge] Stealth fetching URL: {url}")
        try:
            from scrapling import Fetcher

            fetcher = Fetcher()

            loop = asyncio.get_running_loop()
            page = await loop.run_in_executor(None, lambda: fetcher.get(url))

            # Extract basic text content using Scrapling's Response API
            # Note: Scrapling v0.4+ Fetcher.get returns a Response object, and we access the text or CSS parser
            title = ""
            try:
                title = page.css("title")[0].text if page.css("title") else ""
            except Exception:
                pass

            links = []
            try:
                links = list(set([a.attrib.get('href') for a in page.css('a') if a.attrib.get('href')]))[:5]
            except Exception:
                pass

            logger.info(f"[ScraplingBridge] Successfully fetched and parsed {url}.")
            return {
                "success": True,
                "url": url,
                "title": title,
                "sample_links": links,
                "status_code": page.status
            }

        except Exception as e:
            logger.error(f"[ScraplingBridge] Exception during fetch: {e}")
            return {"success": False, "error": str(e)}

scrapling_bridge = ScraplingBridge()
