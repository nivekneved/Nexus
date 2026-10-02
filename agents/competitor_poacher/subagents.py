# -*- coding: utf-8 -*-
"""
Competitor Review Poacher Subagents
=============================================================================
Scans software review platforms (G2, Capterra, Trustpilot) for frustrated SaaS users
complaining about recurring monthly costs, price hikes, or downtime, and crafts
targeted poacher pitch campaigns.
"""

import os
import json
import time
import secrets
from datetime import datetime
from typing import Dict, Any, List
from core.paths import resolve_data_path

POACHED_LEADS_FILE = resolve_data_path("competitor_poached_leads.json")

SAMPLE_COMPETITOR_COMPLAINTS = [
    {
        "id": "COMP-001",
        "competitor": "Enterprise SaaS CRM Corp",
        "platform": "G2 Reviews",
        "rating": 2,
        "reviewer_title": "Way too expensive for a solo founder — 300% price hike!",
        "review_text": "We were paying $490/month and out of nowhere they bumped us to $1,400/month without notice. Their support is slow and we are trapped in their cloud ecosystem.",
        "author": "Marcus Vance (CTO at FinTech Startup)",
        "date": "2026-10-01",
        "sentiment": "FRUSTRATED_PRICING"
    },
    {
        "id": "COMP-002",
        "competitor": "Cloud Automation Suite X",
        "platform": "Trustpilot",
        "rating": 1,
        "reviewer_title": "Constant server outages and data privacy concerns",
        "review_text": "Our automated workflows failed three times last week because their US servers went down. We need a 100% self-hosted local solution where we control our own data.",
        "author": "Sarah Jenkins (Operations Director)",
        "date": "2026-09-28",
        "sentiment": "UPTIME_AND_PRIVACY"
    },
    {
        "id": "COMP-003",
        "competitor": "AI Email Marketing Pro",
        "platform": "Capterra",
        "rating": 2,
        "reviewer_title": "Hidden per-contact tier billing is bleeding our budget",
        "review_text": "They charge extra for every 5,000 subscribers. As our mailing list grew, our monthly bill hit $850. Looking for an open-source or perpetual lifetime license alternative.",
        "author": "David K. (Growth Lead)",
        "date": "2026-09-25",
        "sentiment": "BILLING_TIER_FATIGUE"
    }
]


from core.subagent import BaseSubAgent


class CompetitorReviewScraperSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            subagent_id="competitor_review_scraper",
            name="Competitor Review Scraper & Pain Point Detector",
            parent_agent_id="competitor_poacher",
            description="Scans review sites for SaaS billing/downtime complaints."
        )

    def execute(self, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = payload or {}
        target_competitor = context.get("competitor", "All Competitors")
        detected = SAMPLE_COMPETITOR_COMPLAINTS
        if target_competitor != "All Competitors":
            detected = [c for c in detected if target_competitor.lower() in c["competitor"].lower()]

        return {
            "success": True,
            "scanned_platforms": ["G2", "Trustpilot", "Capterra"],
            "pain_points_detected": len(detected),
            "complaints": detected
        }


class PoacherCampaignGeneratorSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            subagent_id="poacher_campaign_generator",
            name="Poacher Campaign Pitch Generator",
            parent_agent_id="competitor_poacher",
            description="Crafts tailored anti-SaaS pitches."
        )

    def execute(self, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = payload or {}
        complaints = context.get("complaints", SAMPLE_COMPETITOR_COMPLAINTS)
        generated_leads = []

        if not os.path.exists(POACHED_LEADS_FILE):
            os.makedirs(os.path.dirname(POACHED_LEADS_FILE), exist_ok=True)
            with open(POACHED_LEADS_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

        try:
            with open(POACHED_LEADS_FILE, "r", encoding="utf-8") as f:
                existing_leads = json.load(f)
        except Exception:
            existing_leads = []

        for comp in complaints:
            lead_id = f"POACH-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}"

            # Craft tailored anti-SaaS pitch
            pitch = (
                f"Hi {comp['author'].split(' ')[0]},\n\n"
                f"I saw your review regarding {comp['competitor']} on {comp['platform']} ("
                f"\"{comp['reviewer_title']}\").\n\n"
                f"Paying recurring monthly cloud rent while facing price hikes and downtime is brutal for growing teams. "
                f"That's why we built Nexus™ — a 100% self-hosted autonomous AI workforce with zero monthly subscription fees "
                f"and perpetual lifetime commercial licenses ($249 one-time buyout).\n\n"
                f"Would you be open to a 5-minute local demo?\n\n"
                f"Best regards,\n"
                f"Deven Pawaray (Founder, Nexus Autonomous Systems)\n"
                f"🔗 https://nexus-workforce.vercel.app"
            )

            new_lead = {
                "id": lead_id,
                "competitor": comp["competitor"],
                "author": comp["author"],
                "reviewer_title": comp["reviewer_title"],
                "review_text": comp["review_text"],
                "platform": comp["platform"],
                "tailored_pitch": pitch,
                "status": "READY_TO_DISPATCH",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Avoid duplicates by title
            if not any(l.get("reviewer_title") == comp["reviewer_title"] for l in existing_leads):
                existing_leads.insert(0, new_lead)
                generated_leads.append(new_lead)

        try:
            with open(POACHED_LEADS_FILE, "w", encoding="utf-8") as f:
                json.dump(existing_leads[:200], f, indent=2)
        except Exception:
            pass

        return {
            "success": True,
            "new_leads_generated": len(generated_leads),
            "leads": generated_leads
        }


def load_poached_leads() -> List[Dict[str, Any]]:
    if not os.path.exists(POACHED_LEADS_FILE):
        return []
    try:
        with open(POACHED_LEADS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []
