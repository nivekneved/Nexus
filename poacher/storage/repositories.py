"""
CompetitorPoacher: Async Persistence Repositories
===============================================
"""

import json
import asyncio
from typing import List, Dict, Any, Optional
from poacher.storage.db import PoacherDB
from poacher.core.models import PoacherCard

class PoacherRepository:
    @staticmethod
    async def persist(card: PoacherCard):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            PoacherDB.save_card,
            card.card_id,
            card.competitor_name,
            card.target_domain,
            card.poaching_score,
            card.status,
            card.model_dump_json()
        )
