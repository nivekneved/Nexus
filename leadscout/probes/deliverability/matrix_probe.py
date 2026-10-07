"""
LeadScout-Core: Email Permutation Synthesizer
============================================
Synthesizes email address permutations for discovered staff members.
"""

from typing import Dict, Any
from leadscout.probes.base import BaseProbe
from leadscout.core.card import LeadCard

class SynthesizeEmailPermutationsTask(BaseProbe):
    name = "SynthesizeEmailPermutationsTask"

    async def execute(self, card: LeadCard) -> Dict[str, Any]:
        if not card.domain or not card.staff_members:
            return {}

        permutations = []
        domain = card.domain
        for staff in card.staff_members:
            name_parts = staff["name"].lower().split()
            if len(name_parts) >= 2:
                first, last = name_parts[0], name_parts[1]
                permutations.extend([
                    f"{first}.{last}@{domain}",
                    f"{first[0]}{last}@{domain}",
                    f"{first}@{domain}",
                    f"{first}_{last}@{domain}"
                ])
        return {"email_permutations": permutations}
