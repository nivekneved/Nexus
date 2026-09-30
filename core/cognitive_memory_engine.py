
import os
import json
from typing import Dict, Any, List, Optional
from core.paths import resolve_data_path
from core.jarvis_memory import jarvis_memory
from core.tiered_memory import tiered_memory
from core.contact_history_service import contact_history_service

class CognitiveMemoryEngine:
    """
    Unified Memory Hub uniting Short-Term Working Memory,
    Tiered/Semantic Memory, and Contact/CRM History.
    """
    def __init__(self):
        self.working = jarvis_memory
        self.tiered = tiered_memory
        self.crm = contact_history_service

    # --- CRM / Contact Routing ---
    def get_all_contacts(self) -> List[Dict[str, Any]]:
        return self.crm.get_all_contacts()

    def get_contact_stats(self) -> Dict[str, Any]:
        return self.crm.get_stats()

    def get_contact_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return self.crm.get_contact_by_email(email)

    def mark_contact_bounced(self, email: str, reason: str = "Unknown"):
        self.crm.mark_bounced(email, reason)

    # --- Tiered / Recall Routing ---
    def record_recall_event(self, event_type: str, data: Dict[str, Any]):
        return self.tiered.record_recall_event(event_type, data)

    def query_semantic_memory(self, query: str) -> List[Dict[str, Any]]:
        # Map to whatever search/query method exists in tiered_memory
        if hasattr(self.tiered, 'query'):
            return self.tiered.query(query)
        return []

    # --- Working Memory Routing ---
    def update_earnings(self, amount: float):
        # Implementation depends on jarvis_memory methods
        if hasattr(self.working, 'update_earnings'):
            self.working.update_earnings(amount)

    def get_earnings_status(self) -> Dict[str, Any]:
        if hasattr(self.working, 'get_earnings_status'):
            return self.working.get_earnings_status()
        return {}

cognitive_memory = CognitiveMemoryEngine()
