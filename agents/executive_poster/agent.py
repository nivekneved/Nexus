"""
Nexus Autonomous Workforce — Employee #19: Executive Social Ghostwriter & Auto-Poster
Official Role: Crafts, reviews, and publishes authoritative social media content
               on behalf of Deven Pawaray (Founder & CEO).
Channels: LinkedIn, X (Twitter), Instagram, and WhatsApp VIP Broadcasts.
"""

import os
import random
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from agents.executive_poster.subagents import (
    ExecutiveGhostwriterSubAgent,
    SocialPublishingSubAgent,
    SocialAnalyticsRadarSubAgent,
    EXECUTIVE_PRESET_PROMPTS,
    load_posts_ledger
)


class ExecutivePosterAgent(BaseAgent):
    """
    Employee #19: Executive Social Ghostwriter & Auto-Poster
    Autonomous content creation and multi-channel publishing agent.
    Mines company telemetry and strategic wins to author high-converting
    founder posts in Deven Pawaray's voice, providing 1-click visual approval
    and instant browser intent dispatch.
    """
    def __init__(self):
        super().__init__(
            agent_id="executive_poster",
            name="Executive Social Ghostwriter & Auto-Poster",
            description="Autonomous personal ghostwriter for Deven Pawaray. Drafts viral thought leadership, launches, and updates for LinkedIn, X, and WhatsApp with 1-click publishing.",
            icon="feather",
            schedule_minutes=240  # Runs every 4 hours
        )
        self.config = {
            "AUTO_PILOT_ENABLED": True,
            "CHANNELS": ["linkedin", "twitter_x", "whatsapp"],
            "VOICE_PERSONA": "Visionary Founder & CEO (Deven Pawaray)",
            "MIN_ENGAGEMENT_TARGET": "5.0%"
        }

        # Register 3 single-task subagents
        self.register_subagent(ExecutiveGhostwriterSubAgent())
        self.register_subagent(SocialPublishingSubAgent())
        self.register_subagent(SocialAnalyticsRadarSubAgent())

    def run_cycle(self) -> Dict[str, Any]:
        """
        Periodic autonomous cycle:
        1. Checks if a new draft is needed (e.g. at least 1 fresh draft in the queue).
        2. If empty or stale, crafts an authentic thought leadership post using a rotating prompt.
        3. Updates analytics radar.
        """
        posts = load_posts_ledger()
        recent_drafts = [p for p in posts if p.get("status") == "DRAFT"]

        crafted_post = None
        if not recent_drafts:
            # Pick a rotating high-impact prompt
            preset = random.choice(EXECUTIVE_PRESET_PROMPTS)
            res = self.run_subagent("sub_executive_ghostwriter", {
                "preset_id": preset["id"],
                "topic": preset["prompt"],
                "category": preset["category"]
            })
            if res.get("success"):
                crafted_post = res.get("post")

        analytics = self.run_subagent("sub_social_analytics")

        return {
            "cycle_completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "new_post_drafted": crafted_post is not None,
            "draft_title": crafted_post.get("title") if crafted_post else "Existing drafts ready for CEO review",
            "total_posts_managed": analytics.get("total_posts", len(posts)),
            "status": "AUTONOMOUS_CYCLE_COMPLETE"
        }

    def get_stats(self) -> List[Dict[str, Any]]:
        posts = load_posts_ledger()
        published = len([p for p in posts if p.get("status") == "PUBLISHED"])
        drafts = len([p for p in posts if p.get("status") == "DRAFT"])
        total_views = sum(p.get("metrics", {}).get("estimated_views", 0) for p in posts)
        return [
            {"title": "Published Dispatches", "value": published, "color": "green"},
            {"title": "Ready for CEO Review", "value": drafts, "color": "yellow"},
            {"title": "Estimated Audience Reach", "value": f"{total_views:,}", "color": "purple"}
        ]

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "AUTO_PILOT_ENABLED",
                "label": "Autonomous Daily Ghostwriting",
                "type": "boolean",
                "default": True,
                "description": "Automatically draft daily executive posts based on company milestones"
            },
            {
                "key": "VOICE_PERSONA",
                "label": "Executive Persona",
                "type": "string",
                "default": "Visionary Founder & CEO (Deven Pawaray)",
                "description": "Voice used when crafting social media thought leadership"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(step="Config Update", file_used="executive_poster/agent.py", message="Executive Ghostwriter settings updated", level="SUCCESS")
        return True
