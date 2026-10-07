"""
Nexus™ TikTok & Insta Reels Viral Hook Generator
================================================
Generates high-converting, pattern-interrupting short video scripts
designed specifically to drive traffic from social media to the digital store.
"""

import random
import logging

logger = logging.getLogger("Nexus.TikTokViralEngine")

class TikTokViralEngine:
    @staticmethod
    def generate_viral_script(product_name: str, niche: str, price: str) -> dict:
        hooks = [
            f"Stop scrolling. If you are in {niche}, this 1-minute video will save you hundreds of hours.",
            f"Everyone is gatekeeping how they make passive income in {niche}. I'm exposing it right now.",
            f"Do not pay an agency $5,000 for this. Here is the exact {product_name} they use.",
            f"If your bank account isn't growing while you sleep, you are doing {niche} wrong."
        ]

        body = (
            f"I used to spend 10 hours a day doing this manually. Then I found this {product_name}. "
            f"It literally automates the entire process. You just plug it in, and it does the heavy lifting. "
            f"Agencies charge thousands for this exact setup, but I put the entire blueprint and the files "
            f"in my store for literally {price}. "
        )

        cta = [
            "Link is in my bio. Don't say I didn't warn you before I take it down.",
            "Click the link in my profile to grab it before the price goes back to normal.",
            "Drop a 🚀 in the comments and hit the link in my bio to get instant access."
        ]

        script = {
            "hook": random.choice(hooks),
            "body": body,
            "call_to_action": random.choice(cta),
            "visual_direction": "Point to the screen showing the tool running. Fast cuts. High energy. Add auto-captions with neon colors."
        }

        logger.info(f"[TikTokViralEngine] Generated viral script for {product_name}")
        return script

tiktok_viral_engine = TikTokViralEngine()
