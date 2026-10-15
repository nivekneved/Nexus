"""
CompetitorPoacher: Flight Risk Probe
===================================
Calculates tenure and turnover heuristics to identify flight risks.
"""

from typing import Dict, Any
from poacher.probes.base import BaseProbe
from poacher.core.models import PoacherCard

class FlightRiskProbe(BaseProbe):
    name = "FlightRiskProbe"

    async def execute(self, card: PoacherCard) -> Dict[str, Any]:
        updated_roster = []
        for talent in card.talent_roster:
            # Heuristic adjustment for flight risk based on tenure
            if talent.tenure_months in (12, 13, 36, 37): # Common burnout / vesting cliffs
                talent.flight_risk_score = min(talent.flight_risk_score + 0.15, 0.99)
            updated_roster.append(talent)
        return {"talent_roster": updated_roster}
