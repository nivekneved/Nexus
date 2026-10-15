"""
CompetitorPoacher: Swarm Scheduler & Orchestrator
===============================================
"""

import asyncio
import logging
from typing import List, Dict, Any
from poacher.core.models import PoacherCard
from poacher.storage.repositories import PoacherRepository
from poacher.probes.talent.roster_probe import RosterProbe
from poacher.probes.talent.flight_risk import FlightRiskProbe
from poacher.probes.talent.contact_matrix import ContactMatrixProbe
from poacher.probes.churn.review_probe import ReviewProbe
from poacher.probes.churn.tender_probe import TenderProbe
from poacher.probes.tech.fingerprint import TechFingerprintProbe

logger = logging.getLogger("CompetitorPoacher.Orchestrator")

class PoacherOrchestrator:
    def __init__(self):
        self.probes = [
            TechFingerprintProbe(),
            RosterProbe(),
            FlightRiskProbe(),
            ContactMatrixProbe(),
            ReviewProbe(),
            TenderProbe()
        ]

    async def execute_poaching_campaign(self, competitor_name: str, target_domain: str) -> PoacherCard:
        card = PoacherCard(
            card_id=f"poach_{int(asyncio.get_event_loop().time())}",
            competitor_name=competitor_name,
            target_domain=target_domain
        )

        for probe in self.probes:
            logger.info(f"Executing poacher probe: {probe.name} against {competitor_name}")
            try:
                delta = await probe.execute(card)
                for k, v in delta.items():
                    if hasattr(card, k):
                        setattr(card, k, v)
            except Exception as e:
                logger.error(f"Error in probe {probe.name}: {e}")

        # Calculate poaching score
        score = 40.0
        if card.talent_roster: score += 20.0
        if card.churn_signals: score += 25.0
        if card.contract_tenders: score += 15.0
        card.poaching_score = min(score, 100.0)
        card.status = "TARGET_SATURATED"

        await PoacherRepository.persist(card)
        return card
