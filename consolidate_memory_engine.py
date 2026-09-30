import os
import re

# 4. Create the Cognitive Memory Engine (Unified Memory Hub)
memory_engine_code = """
import os
import json
from typing import Dict, Any, List, Optional
from core.paths import resolve_data_path
from core.jarvis_memory import jarvis_memory
from core.tiered_memory import tiered_memory
from core.contact_history_service import contact_history_service

class CognitiveMemoryEngine:
    \"\"\"
    Unified Memory Hub uniting Short-Term Working Memory,
    Tiered/Semantic Memory, and Contact/CRM History.
    \"\"\"
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
"""

with open("core/cognitive_memory_engine.py", "w", encoding="utf-8") as f:
    f.write(memory_engine_code)


# 5. Refactor server.py to use the Treasury and Memory Engines
try:
    with open("server.py", "r", encoding="utf-8") as f:
        server_code = f.read()

    # --- Treasury Engine Refactor ---
    # Replace old imports
    server_code = server_code.replace(
        "from core.crypto_treasury import crypto_treasury",
        "from core.treasury_engine import treasury_engine"
    )
    server_code = server_code.replace(
        "from core.payment_service import payment_service",
        "from core.treasury_engine import treasury_engine"
    )
    server_code = server_code.replace(
        "from core.crypto_verifier import crypto_verifier",
        "from core.treasury_engine import treasury_engine"
    )
    server_code = server_code.replace(
        "from core.receipt_generator import generate_invoice_receipt_html",
        "from core.treasury_engine import treasury_engine"
    )

    # Replace usages
    server_code = server_code.replace("crypto_treasury.", "treasury_engine.crypto.")
    server_code = server_code.replace("payment_service.", "treasury_engine.fiat.")
    server_code = server_code.replace("crypto_verifier.", "treasury_engine.verifier.")

    # We had some custom receipt generator routing in server.py, let's fix it safely
    server_code = server_code.replace("generate_invoice_receipt_html(", "treasury_engine.receipts.generate_receipt_html(")

    # --- Memory Engine Refactor ---
    server_code = server_code.replace(
        "from core.contact_history_service import contact_history_service",
        "from core.cognitive_memory_engine import cognitive_memory"
    )
    server_code = server_code.replace(
        "from core.jarvis_memory import jarvis_memory",
        "from core.cognitive_memory_engine import cognitive_memory"
    )
    server_code = server_code.replace(
        "from core.tiered_memory import tiered_memory",
        "from core.cognitive_memory_engine import cognitive_memory"
    )

    server_code = server_code.replace("contact_history_service.", "cognitive_memory.crm.")
    server_code = server_code.replace("jarvis_memory.", "cognitive_memory.working.")
    server_code = server_code.replace("tiered_memory.", "cognitive_memory.tiered.")

    with open("server.py", "w", encoding="utf-8") as f:
        f.write(server_code)

    print("Successfully refactored server.py to use the unified Treasury and Memory Engines!")
except Exception as e:
    print(f"Error patching server.py: {e}")