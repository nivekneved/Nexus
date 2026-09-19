import os
import json
import time
from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from agents.tech_trend_curator.subagents import (
    TechSignalScraperSubAgent,
    GeminiSynthesizerSubAgent,
    DossierPublisherSubAgent,
    TECH_DOSSIER_FILE
)

class TechTrendCuratorAgent(BaseAgent):
    """
    Employee #14: Executive AI & Dev Ecosystem Daily Dossier
    - Scrapes top engineering releases from Hacker News, Google AI, Apple Developer
    - Synthesizes noisy articles into a 3-minute actionable morning brief
    - Delivers structured recommendations directly to dashboard & mobile
    """
    def __init__(self):
        super().__init__(
            agent_id="tech_trend_curator",
            name="Executive AI & Dev Trend Curator",
            description="Aggregates Hacker News, Google AI, and Apple Developer announcements into a structured 3-minute morning dossier with actionable takeaways for engineering leaders.",
            icon="globe",
            schedule_minutes=360
        )
        self.config = {
            "DISPATCH_HOUR": 8,
            "NOTIFY_MOBILE": True,
            "MOBILE_NUMBER": "+230 58169420",
            "TOPICS": "AI Agents & LLM Frameworks, Modern Web Architecture & Frontend (Next.js, Vite, Tailwind)"
        }
        self.stats = {
            "signals_analyzed": 24,
            "dossiers_published": 5,
            "avg_read_time": "3 mins",
            "action_items_active": 3
        }
        self._register_subagents()

    def _register_subagents(self):
        self.register_subagent(TechSignalScraperSubAgent())
        self.register_subagent(GeminiSynthesizerSubAgent())
        self.register_subagent(DossierPublisherSubAgent())

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "TOPICS",
                "label": "Curated Topic Filters",
                "type": "text",
                "default": "AI Models, Mobile SDKs, Web Frameworks, Cloud Infra",
                "description": "Areas of focus to prioritize during developer news synthesis"
            },
            {
                "key": "NOTIFY_MOBILE",
                "label": "Dispatch Summary to WhatsApp",
                "type": "boolean",
                "default": True,
                "description": "Send morning 3-minute executive summary to +230 58169420"
            },
            {
                "key": "DISPATCH_HOUR",
                "label": "Morning Dispatch Target Hour (0-23)",
                "type": "number",
                "default": 8,
                "description": "Local Mauritius time (UTC+4) to generate the morning brief"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(step="Config Saved", file_used="tech_trend_curator/agent.py", message="Tech curator preferences updated", level="SUCCESS")
        return True

    def get_stats(self) -> List[Dict[str, Any]]:
        return [
            {"title": "Signals Audited", "value": self.stats["signals_analyzed"], "color": "blue"},
            {"title": "Dossiers Published", "value": self.stats["dossiers_published"], "color": "green"},
            {"title": "Avg Read Time", "value": self.stats["avg_read_time"], "color": "blue"},
            {"title": "Action Items Active", "value": self.stats["action_items_active"], "color": "amber"}
        ]

    def get_latest_dossier(self) -> Dict[str, Any]:
        if os.path.exists(TECH_DOSSIER_FILE):
            try:
                with open(TECH_DOSSIER_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def run_cycle(self) -> Dict[str, Any]:
        self.log(step="Scrape Signals", file_used="tech_trend_curator/agent.py", message="Harvesting top engineering signals from Hacker News & developer feeds...", level="INFO")

        # 1. Scrape Signals
        scrape_res = self.run_subagent("tech_signal_scraper")
        signals = scrape_res.get("data", {}).get("signals", [])
        self.stats["signals_analyzed"] += len(signals)

        # 2. Synthesize Brief
        syn_res = self.run_subagent("gemini_synthesizer", {"signals": signals})
        brief = syn_res.get("data", {})

        # 3. Publish Dossier
        pub_res = self.run_subagent("dossier_publisher", {"brief": brief})
        self.stats["dossiers_published"] += 1

        self.log(step="Dossier Published", file_used="latest_tech_dossier.md", message=f"Morning Tech Brief ready: '{brief.get('headline')}'", level="SUCCESS")

        # Dispatch Morning Brief to WhatsApp (+230 58169420)
        if self.config.get("NOTIFY_MOBILE"):
            try:
                from core.agent_manager import AgentManager
                dispatcher = AgentManager().get_agent("mobile_dispatcher")
                if dispatcher and hasattr(dispatcher, "send_notification"):
                    headline = brief.get("headline", "Daily Tech Briefing")
                    dispatcher.send_notification(
                        title=f"📰 3-Min Executive Tech Brief ({brief.get('date', 'Today')})",
                        message=f"{headline}. Top takeaway: Autonomous agent architectures and React 19 updates live. Full brief available in Command Center.",
                        urgency="P2"
                    )
            except Exception:
                pass

        return {
            "status": "Success",
            "headline": brief.get("headline"),
            "takeaways_count": len(brief.get("key_takeaways", [])),
            "reading_time": brief.get("reading_time", "3 minutes")
        }
