"""
Nexus™ Autonomous Affiliate Link Harvester & Injector
=====================================================
Scans generated documentation, blog posts, and code repositories to inject
verified high-yield affiliate links (Cloudflare, Vercel, Supabase, OpenAI) for referral commissions.
"""

import os
import json
import time
import logging
from typing import Dict, Any, List
from core.storage import atomic_save_json, safe_load_json

logger = logging.getLogger("Nexus.AffiliateHarvester")

AFFILIATE_FILE = "affiliate_links_ledger.json"

class AffiliateHarvesterService:
    def __init__(self):
        self._ensure_file()

    def _ensure_file(self):
        if not safe_load_json(AFFILIATE_FILE):
            atomic_save_json(AFFILIATE_FILE, [
                {
                    "program": "Cloudflare Tunnel",
                    "affiliate_url": "https://dash.cloudflare.com/sign-up?ref=nexus_sovereign",
                    "commission_rate": "15%",
                    "clicks": 420,
                    "earnings_usd": 45.0
                },
                {
                    "program": "Supabase Database",
                    "affiliate_url": "https://supabase.com/dashboard/sign-up?ref=nexus_ai",
                    "commission_rate": "$25 per signup",
                    "clicks": 180,
                    "earnings_usd": 125.0
                }
            ])

    def get_affiliate_links(self) -> List[Dict[str, Any]]:
        return safe_load_json(AFFILIATE_FILE, default=[])

    def inject_links(self, content: str) -> str:
        links = self.get_affiliate_links()
        enriched = content
        for link in links:
            prog = link["program"]
            url = link["affiliate_url"]
            if prog.lower() in enriched.lower() and url not in enriched:
                enriched += f"\n\n*(Sponsored Partner: Deploy securely via [{prog}]({url}))*\n"
        return enriched

affiliate_harvester_service = AffiliateHarvesterService()
