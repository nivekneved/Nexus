# -*- coding: utf-8 -*-
"""
Competitor Review Poacher Agent
=============================================================================
Employee #19: Autonomous Competitor Review Poacher & Anti-SaaS Converter
Scans review platforms for frustrated users complaining about SaaS price hikes
and downtime, converting them into Nexus lifetime license buyers.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from agents.competitor_poacher.subagents import (
    CompetitorReviewScraperSubAgent,
    PoacherCampaignGeneratorSubAgent,
    load_poached_leads,
    POACHED_LEADS_FILE,
    SAMPLE_COMPETITOR_COMPLAINTS
)


class CompetitorPoacherAgent(BaseAgent):
    """
    Employee #19: Autonomous Competitor Review Poacher & Anti-SaaS Converter
    Scans public review platforms (G2, Trustpilot, Capterra) for frustrated
    SaaS users experiencing price gouging or downtime, auto-crafting bespoke
    anti-SaaS conversion pitches to win them over to Nexus.
    """
    def __init__(self):
        super().__init__(
            agent_id="competitor_poacher",
            name="Competitor Review Poacher & Anti-SaaS Converter",
            description="Scans review sites for frustrated SaaS users complaining about high bills or downtime, and converts them into perpetual Nexus license buyers.",
            icon="shield",
            schedule_minutes=240
        )
        self.config = {
            "AUTO_SCAN_REVIEWS": True,
            "TARGET_PLATFORMS": ["G2", "Trustpilot", "Capterra"],
            "AUTO_DISPATCH_PITCH": False,
            "MAX_LEADS_PER_DAY": 10
        }
        self.stats = {
            "competitors_monitored": 12,
            "complaints_analyzed": len(SAMPLE_COMPETITOR_COMPLAINTS),
            "poached_leads_ready": len(load_poached_leads()),
            "estimated_conversion_value_usd": 1245
        }

        # Register specialized subagents
        self.register_subagent(CompetitorReviewScraperSubAgent())
        self.register_subagent(PoacherCampaignGeneratorSubAgent())

        self._ensure_seed_leads()

    def _ensure_seed_leads(self):
        leads = load_poached_leads()
        if not leads:
            gen = PoacherCampaignGeneratorSubAgent()
            gen.run({"complaints": SAMPLE_COMPETITOR_COMPLAINTS})
            self.stats["poached_leads_ready"] = len(load_poached_leads())

    def get_poached_leads(self) -> List[Dict[str, Any]]:
        return load_poached_leads()

    def run_cycle(self) -> Dict[str, Any]:
        """Runs the complete competitor review scanning and poacher pitch generation cycle."""
        self.log(
            step="Review Scraping",
            file_used="competitor_poacher/agent.py",
            message="Scanning G2, Trustpilot & Capterra for SaaS price hike and downtime complaints...",
            level="INFO"
        )

        scraper = self.run_subagent("competitor_review_scraper_sub_agent", {})
        generator = self.run_subagent("poacher_campaign_generator_sub_agent", {"complaints": scraper.get("complaints", [])})

        self.stats["poached_leads_ready"] = len(load_poached_leads())
        self.log(
            step="Poacher Pitch Generated",
            file_used=POACHED_LEADS_FILE,
            message=f"Successfully synthesized {generator.get('new_leads_generated', 0)} bespoke anti-SaaS poacher pitches.",
            level="SUCCESS"
        )

        return {
            "status": "Competitor Poacher Cycle Completed",
            "scraper_results": scraper,
            "campaign_results": generator
        }

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "AUTO_SCAN_REVIEWS",
                "label": "Auto-Scan Software Reviews",
                "type": "boolean",
                "default": True,
                "description": "Continuously monitor review boards for disgruntled SaaS customers"
            },
            {
                "key": "MAX_LEADS_PER_DAY",
                "label": "Max Poacher Leads / Day",
                "type": "number",
                "default": 10,
                "description": "Maximum number of tailored outreach pitches to generate daily"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(step="Config Update", file_used="competitor_poacher/agent.py", message="Competitor poacher configuration updated", level="SUCCESS")
        return True

    def get_stats(self) -> List[Dict[str, Any]]:
        return [
            {"title": "Competitors Monitored", "value": self.stats["competitors_monitored"], "color": "blue"},
            {"title": "Complaints Analyzed", "value": self.stats["complaints_analyzed"], "color": "yellow"},
            {"title": "Ready Poacher Leads", "value": self.stats["poached_leads_ready"], "color": "green"},
            {"title": "Pipeline Value", "value": f"${self.stats['estimated_conversion_value_usd']} USD", "color": "purple"}
        ]
