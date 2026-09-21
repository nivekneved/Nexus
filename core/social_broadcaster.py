"""
Nexus™ Autonomous Social & Webhook Broadcaster
==============================================
Enables agents to broadcast newly manufactured $1 digital tools,
promotional discounts, and updates to Discord webhooks, Slack, Telegram,
and social developer channels with zero external dependencies.
"""

import os
import sys
import json
import time
import urllib.request
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

QUEUE_FILE = "social_broadcast_queue.json"


class SocialBroadcaster:
    def __init__(self):
        self.queue_file = QUEUE_FILE

    def broadcast_new_product(
        self,
        product_name: str,
        price: str = "$1.00 USD",
        checkout_url: str = "http://127.0.0.1:8000/store",
        features: Optional[List[str]] = None,
        webhook_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Dispatches an automated rich announcement card to a Discord/Slack webhook.
        Falls back to local queued log if no webhook URL is configured.
        """
        load_dotenv(override=True)
        target_webhook = webhook_url or os.getenv("DISCORD_WEBHOOK_URL", "").strip() or os.getenv("SLACK_WEBHOOK_URL", "").strip()

        feature_str = "\n".join(f"• {f}" for f in (features or [
            "100% self-hosted Python script",
            "Zero monthly SaaS fees",
            "Commercial usage rights included"
        ]))

        discord_payload = {
            "username": "Nexus™ Digital Vending Machine",
            "avatar_url": "https://img.shields.io/badge/Nexus-Workforce-blue",
            "embeds": [{
                "title": f"🚀 New Micro-Tool Live: {product_name}",
                "description": (
                    f"A brand new self-hosted developer automation script has been manufactured and tested in the sandbox.\n\n"
                    f"**Price**: {price} (or Rs 45 MUR)\n\n"
                    f"**Features**:\n{feature_str}\n\n"
                    f"[⚡ 1-Click Instant PayPal Checkout]({checkout_url})"
                ),
                "color": 3723224,  # Cyan/Blue
                "footer": {"text": "Nexus AI Workforce • Grand Baie, Mauritius"}
            }]
        }

        # 1. Live Webhook Dispatch if configured
        if target_webhook and target_webhook.startswith("http"):
            try:
                req = urllib.request.Request(
                    target_webhook,
                    data=json.dumps(discord_payload).encode("utf-8"),
                    headers={"Content-Type": "application/json", "User-Agent": "NexusBroadcaster/3.0"}
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    record = {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "product_name": product_name,
                        "price": price,
                        "checkout_url": checkout_url,
                        "status": "DISPATCHED_WEBHOOK",
                        "status_code": resp.status
                    }
                    self._append_to_queue(record)
                    return {"success": True, "dispatched_to": "webhook", "status_code": resp.status, "record": record}
            except Exception as e:
                pass

        # 2. Local fallback queue
        record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "product_name": product_name,
            "price": price,
            "checkout_url": checkout_url,
            "status": "QUEUED_LOCAL",
            "note": "Queued locally. Add DISCORD_WEBHOOK_URL to .env to push live automatically."
        }
        self._append_to_queue(record)

        return {
            "success": True,
            "dispatched_to": "local_queue",
            "note": "Broadcast logged to queue. Set DISCORD_WEBHOOK_URL or SLACK_WEBHOOK_URL in .env to broadcast live.",
            "record": record
        }

    def generate_social_snippets(
        self,
        product_name: str,
        price: str = "$1.00 USD",
        checkout_url: str = "http://127.0.0.1:8000/store",
        description: str = ""
    ) -> Dict[str, str]:
        """Generates formatted social media announcements ready for Twitter/X, Reddit, and Telegram."""
        clean_desc = description or "Standalone, self-hosted Python automation script. No monthly fees, run locally forever."
        return {
            "twitter_x": (
                f"🚀 Just launched: {product_name}!\n\n"
                f"{clean_desc}\n\n"
                f"💵 Only {price} (Rs 45 MUR) — instant PayPal fulfillment.\n"
                f"🔗 Grab it here: {checkout_url}\n\n"
                f"#Python #BuildInPublic #DevTools #Automation #IndieHacker"
            ),
            "reddit_sideproject": (
                f"**[Tool] {product_name} - Self-hosted Python script to automate tasks with zero SaaS subscription**\n\n"
                f"Hey everyone! Built a lightweight, single-file Python utility: **{product_name}**.\n\n"
                f"- Runs 100% locally on your machine / VPS\n"
                f"- No monthly fees or telemetry\n"
                f"- Instant 1-click PayPal checkout ({price})\n\n"
                f"Check out the live vending machine: {checkout_url}\n"
                f"Feedback and pull requests welcome!"
            ),
            "telegram_discord": (
                f"⚡ **Nexus™ New Drop**: `{product_name}`\n"
                f"Price: {price} | Instant Download\n"
                f"{clean_desc}\n"
                f"👉 Instant Checkout: {checkout_url}"
            )
        }

    def get_queue(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns the recent broadcast events."""
        if not os.path.exists(self.queue_file):
            return []
        try:
            with open(self.queue_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data[:limit]
        except Exception:
            return []

    def _append_to_queue(self, record: Dict[str, Any]):
        queue = self.get_queue(limit=100)
        queue.insert(0, record)
        try:
            with open(self.queue_file, "w", encoding="utf-8") as f:
                json.dump(queue[:100], f, indent=2)
        except Exception:
            pass


social_broadcaster = SocialBroadcaster()
