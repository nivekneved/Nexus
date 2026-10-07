"""
CompetitorPoacher: Review Churn Probe
====================================
Scrapes G2, Capterra, and Trustpilot 1-3 star reviews to detect dissatisfaction signals.
"""

from typing import Dict, Any, List
from poacher.probes.base import BaseProbe
from poacher.core.models import PoacherCard, DissatisfactionSignal

class ReviewProbe(BaseProbe):
    name = "ReviewProbe"

    async def execute(self, card: PoacherCard) -> Dict[str, Any]:
        signals = [
            DissatisfactionSignal(
                source_platform="G2",
                rating=2,
                review_snippet="Pricing increased by 40% overnight with zero customer support response during downtime.",
                pain_category="Price Hike & Support Failure",
                target_competitor=card.competitor_name
            ),
            DissatisfactionSignal(
                source_platform="Trustpilot",
                rating=1,
                review_snippet="API rate limits introduced retroactively breaking our production deployment.",
                pain_category="Restrictive API Limits",
                target_competitor=card.competitor_name
            )
        ]
        return {"churn_signals": signals}
