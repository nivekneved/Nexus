"""
CompetitorPoacher: HTTP/2 Client with Header Rotation & Jitter
============================================================
"""

import asyncio
import random
import httpx
from typing import Dict, Any, Optional

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
]

class PoacherNetwork:
    @staticmethod
    async def get_client() -> httpx.AsyncClient:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }
        return httpx.AsyncClient(http2=True, headers=headers, timeout=12.0, follow_redirects=True)

    @staticmethod
    async def jitter_sleep(min_sec: float = 0.5, max_sec: float = 2.0):
        await asyncio.sleep(random.uniform(min_sec, max_sec))
