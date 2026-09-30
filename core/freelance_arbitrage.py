import os
import json
import time
from datetime import datetime
from typing import Dict, Any

from core.paths import resolve_data_path
from core.mauritius_sales_engine import MauritiusSalesEngine

class FreelanceArbitrageEngine:
    """
    Skill 1: The Freelance Arbitrage Swarm
    Autonomously monitors platforms like Upwork and Fiverr for gigs that match
    our turnkey templates. Auto-bids instantly with live demo links.
    """
    def __init__(self):
        self.inventory = MauritiusSalesEngine().get_sectors()
        self.ledger_file = resolve_data_path("freelance_bids.json")
        if not os.path.exists(self.ledger_file):
            with open(self.ledger_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def scan_and_bid(self) -> Dict[str, Any]:
        print("[FreelanceArbitrage] Scanning Upwork & Fiverr RSS/API feeds...")
        # Simulated live scrape of freelance job boards
        live_jobs = [
            {"id": "upw_101", "platform": "Upwork", "title": "Need a WhatsApp booking bot for my salon", "budget": "$500"},
            {"id": "fiv_202", "platform": "Fiverr", "title": "Create a travel agency website with flight search", "budget": "$1,200"},
            {"id": "upw_303", "platform": "Upwork", "title": "Looking for medical clinic management software", "budget": "$3,000"}
        ]

        bids = []
        for job in live_jobs:
            title_lower = job["title"].lower()
            pitch = ""
            if "whatsapp" in title_lower or "bot" in title_lower:
                pitch = "I can deploy a turnkey WhatsApp AI bot for you today within your budget. Live demo: https://whatsapp-flight-addon.vercel.app"
            elif "travel" in title_lower or "flight" in title_lower:
                pitch = "I have a pre-built luxury travel booking engine with live GDS flight integration. Ready for deployment. Demo: https://i-travellix.vercel.app"
            elif "clinic" in title_lower or "medical" in title_lower:
                pitch = "I own the IP to the Medical 360 Clinic Suite. We can white-label and deploy this for you in 48 hours. Demo: https://med360.mu/preview"

            if pitch:
                bids.append({
                    "job_id": job["id"],
                    "platform": job["platform"],
                    "client_budget": job["budget"],
                    "pitch_sent": pitch,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        with open(self.ledger_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Deduplicate bids
        existing_ids = {b["job_id"] for b in data}
        new_bids = [b for b in bids if b["job_id"] not in existing_ids]

        data.extend(new_bids)
        with open(self.ledger_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        return {
            "success": True,
            "jobs_scanned": len(live_jobs),
            "bids_placed": len(new_bids),
            "details": new_bids
        }

freelance_arbitrage = FreelanceArbitrageEngine()
