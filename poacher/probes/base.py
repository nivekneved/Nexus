"""
CompetitorPoacher: Abstract Base Probe Interface
===============================================
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from poacher.core.models import PoacherCard

class BaseProbe(ABC):
    name: str = "base_probe"

    @abstractmethod
    async def execute(self, card: PoacherCard) -> Dict[str, Any]:
        """Executes probe logic and returns discovered delta updates."""
        pass
