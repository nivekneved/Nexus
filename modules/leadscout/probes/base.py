"""
LeadScout-Core: Abstract Base Probe
===================================
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from leadscout.core.card import LeadCard

class BaseProbe(ABC):
    name: str = "base_probe"

    @abstractmethod
    async def execute(self, card: LeadCard) -> Dict[str, Any]:
        """Executes probe logic against the LeadCard and returns discovered delta updates."""
        pass
