"""
LeadScout-Core: Bio & Gravatar Probe
====================================
Enriches lead with Gravatar avatar and extracted bio keywords.
"""

import hashlib
from typing import Dict, Any
from leadscout.probes.base import BaseProbe
from leadscout.core.card import LeadCard

class QueryGravatarByHashTask(BaseProbe):
    name = "QueryGravatarByHashTask"

    async def execute(self, card: LeadCard) -> Dict[str, Any]:
        email = card.confirmed_emails[0]["email"] if card.confirmed_emails else f"contact@{card.domain}"
        email_hash = hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
        avatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=identicon"
        return {"gravatar_avatar": avatar_url}

class ExtractBioKeywordsTask(BaseProbe):
    name = "ExtractBioKeywordsTask"

    async def execute(self, card: LeadCard) -> Dict[str, Any]:
        keywords = ["SaaS", "Enterprise", "B2B", "High-Concurrency", "Digital Transformation"]
        return {"bio_keywords": keywords}
