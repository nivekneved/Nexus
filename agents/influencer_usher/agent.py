"""
Employee #18: Marketing & Social Media Influencer Usher

An autonomous AI agent that:
  1. Discovers best-fit influencers for each Nexus product (Influencer Matcher)
  2. Generates viral, platform-specific marketing copy (Viral Campaign Generator)
  3. Monitors social trends across Chirper, X, and LinkedIn (Social Signal Radar)
  4. Auto-crafts multi-touch follow-up sequences for warm leads (Lead Nurture Sequencer)

Designed to be always-on, turning Nexus products into consistent cashflow
through influencer partnerships, viral content, and disciplined sales follow-up.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List

from core.base_agent import BaseAgent
from agents.influencer_usher.subagents import (
    InfluencerMatcherSubAgent,
    ViralCampaignSubAgent,
    SocialSignalRadarSubAgent,
    LeadNurtureSubAgent,
    NEXUS_PRODUCTS,
    INFLUENCER_CAMPAIGN_FILE,
    SOCIAL_SIGNALS_FILE,
)


class InfluencerUsherAgent(BaseAgent):
    """
    Employee #18: Marketing & Social Media Influencer Usher

    Core mandate:
    - Scout the influencer landscape and rank profiles by ROI
    - Generate viral campaign content for every Nexus product
    - Radar-scan social platforms to inject campaigns at peak trend moments
    - Nurture every warm lead with personalised, timed follow-up sequences
    """

    def __init__(self):
        super().__init__(
            agent_id="influencer_usher",
            name="Marketing & Social Media Influencer Usher",
            description=(
                "Autonomous marketing agent: discovers best-fit influencers, "
                "generates viral campaign copy, monitors social signals across "
                "Chirper, X, and LinkedIn, and delivers influencer-led content at peak trend moments."
            ),
            icon="megaphone",
            schedule_minutes=120,  # Runs every 2 hours
        )

        self.config = {
            "AUTO_GENERATE_CAMPAIGNS": True,
            "MONITOR_SOCIAL_SIGNALS": True,
            "NURTURE_WARM_LEADS": True,
            "TOP_INFLUENCERS_PER_PRODUCT": 3,
            "DEFAULT_CAMPAIGN_PLATFORM": "all",
            "MIN_ENGAGEMENT_RATE": 2.0,
        }

        # Register all 4 subagents
        self.register_subagent(InfluencerMatcherSubAgent())
        self.register_subagent(ViralCampaignSubAgent())
        self.register_subagent(SocialSignalRadarSubAgent())
        self.register_subagent(LeadNurtureSubAgent())

        # Runtime stats
        self._stats = {
            "campaigns_generated": self._count_campaigns(),
            "influencers_ranked": 8,
            "signals_monitored": 8,
            "leads_nurtured": 0,
        }

    # ─────────────────────────────────────────
    # Core Execution Cycle
    # ─────────────────────────────────────────
    def run_cycle(self) -> Dict[str, Any]:
        """Full autonomous marketing & sales cycle."""
        self.log(
            step="Cycle Start",
            file_used="influencer_usher/agent.py",
            message="🎯 Influencer Usher starting full sales & marketing cycle...",
            level="INFO",
        )

        results: Dict[str, Any] = {}

        # Step 1 — Rank influencers for all products
        self.log(
            step="Influencer Match",
            file_used="influencer_usher/subagents.py",
            message="Scoring influencer profiles by engagement-to-cost ratio...",
            level="INFO",
        )
        match_res = self.run_subagent("influencer_matcher", {})
        results["influencer_matches"] = match_res

        # Step 2 — Generate viral campaign content for each product
        campaigns = []
        if self.config.get("AUTO_GENERATE_CAMPAIGNS"):
            for product in NEXUS_PRODUCTS:
                self.log(
                    step="Campaign Generate",
                    file_used="influencer_usher/subagents.py",
                    message=f"Generating viral campaign copy for {product['name']}...",
                    level="INFO",
                )
                cmp_res = self.run_subagent(
                    "viral_campaign_generator",
                    {
                        "product_id": product["id"],
                        "platform": self.config.get("DEFAULT_CAMPAIGN_PLATFORM", "all"),
                    },
                )
                campaigns.append(cmp_res)
        results["campaigns"] = campaigns
        self._stats["campaigns_generated"] = self._count_campaigns()

        # Step 3 — Social Signal Radar scan
        if self.config.get("MONITOR_SOCIAL_SIGNALS"):
            self.log(
                step="Signal Radar",
                file_used="influencer_usher/subagents.py",
                message="Scanning Chirper, X/Twitter, and LinkedIn for trending signals...",
                level="INFO",
            )
            radar_res = self.run_subagent("social_signal_radar", {})
            results["social_signals"] = radar_res
            self._stats["signals_monitored"] = radar_res.get("data", {}).get(
                "total_signals_monitored", self._stats["signals_monitored"]
            )

        self.log(
            step="Cycle Complete",
            file_used="influencer_usher/agent.py",
            message=(
                f"✅ Influencer Usher cycle complete. "
                f"Campaigns: {len(campaigns)} | "
                f"Signals monitored: {self._stats['signals_monitored']}"
            ),
            level="SUCCESS",
        )

        self.run_count += 1
        self.last_run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_run_status = "Success"

        return {
            "status": "Influencer Usher Cycle Complete",
            "campaigns_generated": len(campaigns),
            "results": results,
        }

    # ─────────────────────────────────────────
    # Public API Methods (called by server.py)
    # ─────────────────────────────────────────
    def get_influencer_matches(self, product_id: str = None) -> Dict[str, Any]:
        """Returns ranked influencer matches, optionally filtered by product."""
        res = self.run_subagent("influencer_matcher", {"product_id": product_id} if product_id else {})
        return res.get("data", res)

    def generate_campaign(self, product_id: str, platform: str = "all", lead_name: str = "there") -> Dict[str, Any]:
        """Generates campaign content for a specific product and platform."""
        res = self.run_subagent(
            "viral_campaign_generator",
            {"product_id": product_id, "platform": platform, "lead_name": lead_name},
        )
        return res.get("data", res)

    def get_social_signals(self) -> Dict[str, Any]:
        """Returns the latest social signal radar results."""
        res = self.run_subagent("social_signal_radar", {})
        return res.get("data", res)

    def nurture_lead(self, lead_name: str, product_id: str, company: str = "your organisation", channel: str = "email") -> Dict[str, Any]:
        """Generates a 3-touch nurture sequence for a warm lead."""
        res = self.run_subagent(
            "lead_nurture_sequencer",
            {"lead_name": lead_name, "product_id": product_id, "company": company, "channel": channel},
        )
        self._stats["leads_nurtured"] += 1
        return res.get("data", res)

    def get_campaigns(self) -> List[Dict[str, Any]]:
        """Returns all persisted campaigns."""
        try:
            with open(INFLUENCER_CAMPAIGN_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def get_signals_file(self) -> Dict[str, Any]:
        """Returns the latest social signals from file."""
        try:
            with open(SOCIAL_SIGNALS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"signals": [], "last_updated": None}

    # ─────────────────────────────────────────
    # BaseAgent Overrides
    # ─────────────────────────────────────────
    def get_stats(self) -> List[Dict[str, Any]]:
        return [
            {"title": "Campaigns Generated", "value": self._stats["campaigns_generated"], "color": "purple"},
            {"title": "Influencer Profiles Ranked", "value": self._stats["influencers_ranked"], "color": "blue"},
            {"title": "Social Signals Monitored", "value": self._stats["signals_monitored"], "color": "green"},
            {"title": "Leads Nurtured", "value": self._stats["leads_nurtured"], "color": "orange"},
        ]

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "AUTO_GENERATE_CAMPAIGNS",
                "label": "Auto-Generate Campaign Content",
                "type": "boolean",
                "default": True,
                "description": "Automatically produce viral copy for all Nexus products on each cycle",
            },
            {
                "key": "MONITOR_SOCIAL_SIGNALS",
                "label": "Monitor Social Signals (Chirper / X / LinkedIn)",
                "type": "boolean",
                "default": True,
                "description": "Continuously scan trending topics and map them to product opportunities",
            },
            {
                "key": "NURTURE_WARM_LEADS",
                "label": "Enable Lead Nurture Sequences",
                "type": "boolean",
                "default": True,
                "description": "Auto-generate Day-1/3/7 follow-up sequences for warm leads",
            },
            {
                "key": "DEFAULT_CAMPAIGN_PLATFORM",
                "label": "Default Campaign Platform",
                "type": "select",
                "options": ["all", "x_thread", "instagram_caption", "linkedin_post", "whatsapp_pitch"],
                "default": "all",
                "description": "Which platform to generate content for by default",
            },
            {
                "key": "MIN_ENGAGEMENT_RATE",
                "label": "Minimum Influencer Engagement Rate (%)",
                "type": "number",
                "default": 2.0,
                "description": "Only recommend influencers above this engagement threshold",
            },
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(
            step="Config Update",
            file_used="influencer_usher/agent.py",
            message="Influencer Usher configuration updated",
            level="SUCCESS",
        )
        return True

    # ─────────────────────────────────────────
    # Internals
    # ─────────────────────────────────────────
    def _count_campaigns(self) -> int:
        try:
            with open(INFLUENCER_CAMPAIGN_FILE, "r", encoding="utf-8") as f:
                return len(json.load(f))
        except Exception:
            return 0
