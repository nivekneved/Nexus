"""
Nexus Architecture — Unified Domain Controllers
================================================
Consolidates 18 fragmented pseudo-agent modules into 4 deterministic,
high-cohesion domain controllers powered by SQLite WAL DAL:
1. CommsDomainController      (`core.domains.comms`)
2. OperationsDomainController (`core.domains.operations`)
3. CommerceDomainController   (`core.domains.commerce`)
4. ResearchDomainController   (`core.domains.research`)
"""

from core.domains.comms import CommsDomainController
from core.domains.operations import OperationsDomainController
from core.domains.commerce import CommerceDomainController
from core.domains.research import ResearchDomainController

__all__ = [
    "CommsDomainController",
    "OperationsDomainController",
    "CommerceDomainController",
    "ResearchDomainController"
]
