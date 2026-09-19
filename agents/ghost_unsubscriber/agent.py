import os
import json
import time
from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from agents.ghost_unsubscriber.subagents import (
    UnsubscribeHarvesterSubAgent,
    UnsubscribeExecutorSubAgent,
    NewsletterDigestSubAgent,
    SUBSCRIPTIONS_FILE,
    DIGEST_FILE
)

class GhostUnsubscriberAgent(BaseAgent):
    """
    Employee #11: Zombie Subscription Purger & 2-Minute Newsletter Digest
    - Extracts RFC 2369 List-Unsubscribe headers from incoming emails
    - Maintains a live catalog of active subscriptions and sends frequency
    - Enables 1-click unsubscribe directly from Command Center
    - Synthesizes repetitive newsletters into a single 2-minute daily brief
    """
    def __init__(self):
        super().__init__(
            agent_id="ghost_unsubscriber",
            name="Zombie Subscription Purger & Digest",
            description="Extracts List-Unsubscribe headers, catalogs heavy marketing senders, provides 1-click batch unsubscribe, and generates a 2-minute daily newsletter digest.",
            icon="checklist",
            schedule_minutes=120
        )
        self.config = {
            "REQUIRE_CONFIRMATION_BEFORE_UNSUB": True,
            "AUTO_PURGE_UNSUBSCRIBED_TO_TRASH": True,
            "DISPATCH_MOBILE_WHATSAPP": True,
            "MOBILE_NUMBER": "+230 58169420",
            "DISPATCH_TIME": "08:00",
            "AUTO_AGGREGATE_DIGEST": True,
            "HEAVY_SENDER_THRESHOLD": 3
        }
        self.stats = {
            "subscriptions_detected": 3,
            "unsubscribed_total": 0,
            "active_subscriptions": 3,
            "digests_compiled": 4
        }
        self._register_subagents()
        self._init_catalog_if_needed()

    def _register_subagents(self):
        self.register_subagent(UnsubscribeHarvesterSubAgent())
        self.register_subagent(UnsubscribeExecutorSubAgent())
        self.register_subagent(NewsletterDigestSubAgent())

    def _init_catalog_if_needed(self):
        if not os.path.exists(SUBSCRIPTIONS_FILE):
            # Seed with common dev newsletter samples
            initial = [
                {
                    "id": "sub_1",
                    "sender_raw": "Substack Weekly <digest@substack.com>",
                    "sender_email": "digest@substack.com",
                    "sender_name": "Substack Weekly",
                    "frequency_count": 5,
                    "status": "ACTIVE",
                    "unsub_http": "https://substack.com/unsubscribe",
                    "unsub_mailto": "mailto:unsub@substack.com",
                    "first_detected": "2026-09-10 10:00:00",
                    "last_received": "2026-09-18 14:00:00",
                    "last_subject": "Top tech stories of the week"
                },
                {
                    "id": "sub_2",
                    "sender_raw": "Product Hunt Daily <daily@producthunt.com>",
                    "sender_email": "daily@producthunt.com",
                    "sender_name": "Product Hunt",
                    "frequency_count": 7,
                    "status": "ACTIVE",
                    "unsub_http": "https://producthunt.com/me/subscriptions",
                    "unsub_mailto": None,
                    "first_detected": "2026-09-08 09:15:00",
                    "last_received": "2026-09-18 09:30:00",
                    "last_subject": "Top 10 tools launched today"
                },
                {
                    "id": "sub_3",
                    "sender_raw": "Cloud SaaS Deals <promotions@saasgrowth.io>",
                    "sender_email": "promotions@saasgrowth.io",
                    "sender_name": "Cloud SaaS Deals",
                    "frequency_count": 4,
                    "status": "ACTIVE",
                    "unsub_http": "https://saasgrowth.io/optout",
                    "unsub_mailto": None,
                    "first_detected": "2026-09-12 11:45:00",
                    "last_received": "2026-09-17 16:20:00",
                    "last_subject": "Exclusive 50% discount on dev cloud hosting"
                }
            ]
            with open(SUBSCRIPTIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(initial, f, indent=2)

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "AUTO_AGGREGATE_DIGEST",
                "label": "Auto-Aggregate to Morning Digest",
                "type": "boolean",
                "default": True,
                "description": "Condense incoming newsletter blasts into a single daily brief"
            },
            {
                "key": "HEAVY_SENDER_THRESHOLD",
                "label": "Heavy Sender Alert Threshold",
                "type": "number",
                "default": 3,
                "description": "Flag senders emailing more than this count per week"
            },
            {
                "key": "AUTO_PURGE_CONFIRMED",
                "label": "Auto-Trash Unsubscribed Senders",
                "type": "boolean",
                "default": False,
                "description": "Automatically trash subsequent emails from senders previously marked Unsubscribed"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(step="Config Saved", file_used="ghost_unsubscriber/agent.py", message="Unsubscriber parameters updated", level="SUCCESS")
        return True

    def get_stats(self) -> List[Dict[str, Any]]:
        subs = self.get_subscriptions()
        active = sum(1 for s in subs if s.get("status") == "ACTIVE")
        unsubbed = sum(1 for s in subs if s.get("status") == "UNSUBSCRIBED")
        return [
            {"title": "Active Subscriptions", "value": active, "color": "blue"},
            {"title": "Unsubscribed & Cleaned", "value": unsubbed, "color": "green"},
            {"title": "Heavy Senders (>3/wk)", "value": sum(1 for s in subs if s.get("frequency_count", 0) >= 3), "color": "amber"},
            {"title": "Daily 2-Min Digests", "value": self.stats["digests_compiled"], "color": "blue"}
        ]

    def get_subscriptions(self) -> List[Dict[str, Any]]:
        if os.path.exists(SUBSCRIPTIONS_FILE):
            try:
                with open(SUBSCRIPTIONS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def get_digest(self) -> Dict[str, Any]:
        if os.path.exists(DIGEST_FILE):
            try:
                with open(DIGEST_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def trigger_unsubscribe(self, subscription_id: str) -> Dict[str, Any]:
        """Manually or autonomously triggers an unsubscribe action for a sender."""
        res = self.run_subagent("unsub_executor", {"subscription_id": subscription_id})
        if res.get("success"):
            self.stats["unsubscribed_total"] += 1
            self.log(step="Unsubscribe Dispatched", file_used="subscriptions_catalog.json", message=f"Successfully unsubscribed from {res.get('data', {}).get('sender_name')}", level="ACTION")
        return res

    def run_cycle(self) -> Dict[str, Any]:
        self.log(step="Scan Subscriptions", file_used="ghost_unsubscriber/agent.py", message="Auditing incoming newsletters and subscription headers...", level="INFO")
        
        # 1. Harvest headers and update frequency counts
        sample_emails = [
            {"sender": "Tech Radar Pro <news@techradarpro.com>", "subject": "Top dev tools for September", "body": "To stop receiving these emails click here: https://techradarpro.com/unsubscribe?id=8291"},
            {"sender": "Substack Weekly <digest@substack.com>", "subject": "Engineering management essays", "body": "Unsubscribe here: https://substack.com/unsubscribe"}
        ]
        harvest_res = self.run_subagent("unsub_harvester", {"emails": sample_emails})

        # 2. Compile daily 2-minute digest
        if self.config.get("AUTO_AGGREGATE_DIGEST"):
            digest_res = self.run_subagent("newsletter_digest", {"newsletters": sample_emails})
            self.stats["digests_compiled"] += 1
            self.log(step="Digest Published", file_used="daily_newsletter_digest.md", message=f"Compiled 2-minute morning brief from {len(sample_emails)} promotional items", level="SUCCESS")

        catalog = self.get_subscriptions()
        self.stats["subscriptions_detected"] = len(catalog)
        self.stats["active_subscriptions"] = sum(1 for s in catalog if s.get("status") == "ACTIVE")

        return {
            "status": "Success",
            "total_subscriptions_cataloged": len(catalog),
            "active_subscriptions": self.stats["active_subscriptions"]
        }
