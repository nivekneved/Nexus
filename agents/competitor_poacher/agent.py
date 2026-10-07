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
        """Runs the complete competitor review scanning and poacher pitch generation cycle using PoacherOrchestrator."""
        self.log(
            step="Poacher Recon Swarm",
            file_used="poacher/core/orchestrator.py",
            message="Executing high-speed competitive reconnaissance swarm via PoacherOrchestrator...",
            level="INFO"
        )
        try:
            import asyncio
            from poacher.core.orchestrator import PoacherOrchestrator
            orchestrator = PoacherOrchestrator()
            card = asyncio.run(orchestrator.execute_poaching_campaign("HubSpot Enterprise", "hubspot.com"))

            leads = load_poached_leads()
            new_poached = {
                "id": card.card_id,
                "competitor": card.competitor_name,
                "platform": "G2 / Trustpilot Recon",
                "user": card.talent_roster[0].name if card.talent_roster else "Operations Lead",
                "pain_category": card.churn_signals[0].pain_category if card.churn_signals else "Price Hike",
                "complaint": card.churn_signals[0].review_snippet if card.churn_signals else "SaaS price increase with zero support.",
                "offer_angle": f"Local deployment of Nexus Workforce with lifetime ownership. Stack: {', '.join(card.tech_stack[:3])}",
                "pitch_draft": f"Hi there,\n\nWe noticed your team at {card.competitor_name} is navigating pricing and support friction. Nexus offers autonomous AI workstations with lifetime ownership and zero recurring seat fees.\n\nLet's connect!",
                "status": "TARGET_SATURATED"
            }
            leads.insert(0, new_poached)
            from core.storage import atomic_save_json
            atomic_save_json(POACHED_LEADS_FILE, leads)
            self.stats["poached_leads_ready"] = len(leads)
            return {
                "success": True,
                "status": "Competitor Poacher Swarm Completed",
                "card": card.model_dump(),
                "poached_leads": leads
            }
        except Exception as e:
            self.log(step="Poacher Error", file_used="poacher", message=str(e), level="ERROR")
            scraper = self.run_subagent("competitor_review_scraper", {})
            complaints_data = scraper.get("data", {}).get("complaints", scraper.get("complaints", []))
            generator = self.run_subagent("poacher_campaign_generator", {"complaints": complaints_data})
            self.stats["poached_leads_ready"] = len(load_poached_leads())
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
