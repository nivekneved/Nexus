"""
Nexus™ Continuous Lead Deduplication & Cross-Referencing Engine
================================================================
Prevents autonomous agents from discovering and pitching the same leads repeatedly
by maintaining a persistent cryptographic suppression list and historical dispatch ledger.
"""

import hashlib
import time
import logging
from typing import Dict, Any, List, Set
from core.storage import safe_load_json, atomic_save_json

logger = logging.getLogger("Nexus.LeadDeduplication")

SUPPRESSION_LIST_FILE = "lead_suppression_list.json"
DISPATCH_HISTORY_FILE = "lead_dispatch_history.json"

class LeadDeduplicationEngine:
    def __init__(self):
        self._ensure_files()

    def _ensure_files(self):
        if not safe_load_json(SUPPRESSION_LIST_FILE):
            atomic_save_json(SUPPRESSION_LIST_FILE, [])
        if not safe_load_json(DISPATCH_HISTORY_FILE):
            atomic_save_json(DISPATCH_HISTORY_FILE, [])

    def _generate_fingerprint(self, company: str, email: str) -> str:
        """Generates a unique deterministic fingerprint for a lead."""
        company_clean = "".join(e for e in str(company).lower() if e.isalnum())
        email_clean = str(email).lower().strip()
        combined = f"{company_clean}:{email_clean}"
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()

    def get_suppressed_fingerprints(self) -> Set[str]:
        return set(safe_load_json(SUPPRESSION_LIST_FILE, default=[]))

    def filter_new_leads(self, raw_leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters out leads that have already been discovered, pitched, or suppressed."""
        suppressed = self.get_suppressed_fingerprints()
        unique_leads = []

        for lead in raw_leads:
            company = lead.get("company", "")
            email = lead.get("contact_email", "")
            if not company or not email:
                continue

            fingerprint = self._generate_fingerprint(company, email)
            if fingerprint not in suppressed:
                unique_leads.append(lead)

        logger.info(f"[LeadDeduplication] Filtered {len(raw_leads)} raw leads down to {len(unique_leads)} unique prospects.")
        return unique_leads

    def register_pitched_lead(self, company: str, email: str, campaign_name: str) -> bool:
        """Records a lead as 'pitched', adding it to the suppression list to prevent double-contact."""
        fingerprint = self._generate_fingerprint(company, email)
        suppression_list = safe_load_json(SUPPRESSION_LIST_FILE, default=[])

        if fingerprint in suppression_list:
            return False

        suppression_list.append(fingerprint)
        atomic_save_json(SUPPRESSION_LIST_FILE, suppression_list)

        history = safe_load_json(DISPATCH_HISTORY_FILE, default=[])
        history.insert(0, {
            "fingerprint": fingerprint,
            "company": company,
            "email": email,
            "campaign": campaign_name,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        atomic_save_json(DISPATCH_HISTORY_FILE, history)

        logger.info(f"[LeadDeduplication] Registered {company} ({email}) to suppression list. Will not be pitched again.")
        return True

lead_deduplication_engine = LeadDeduplicationEngine()
