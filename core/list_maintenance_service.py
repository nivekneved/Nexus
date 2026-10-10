# -*- coding: utf-8 -*-
"""
Nexus™ Mass Email List Maintenance & Hygiene Service (v37.0)
============================================================
Sends the Email Hygiene Agent to audit the contact list:
1. Removes duplicate emails (case-insensitive)
2. Removes malformed / incomplete emails (missing @ or domain)
3. Verifies domain MX records & suppressions (legal guardrails)
4. Generates a comprehensive cleaning and audit report
"""

import time
import logging
from typing import Dict, Any, List
from core.storage import safe_load_json, atomic_save_json
from core.legal_guardrails import legal_guardrails
from core.tool_registry import tool_registry
from core.telemetry import telemetry

logger = logging.getLogger("Nexus.ListMaintenance")

CONTACTS_LEDGER = "mass_email_contacts.json"

class ListMaintenanceService:
    @staticmethod
    def audit_and_clean_list() -> Dict[str, Any]:
        """
        Audits the mass emailing contact list, removes duplicates, malformed addresses,
        and unverified domains, and returns a detailed cleaning report.
        """
        start_time = time.time()
        contacts = safe_load_json(CONTACTS_LEDGER, default=[])
        initial_count = len(contacts)

        telemetry.emit(
            agent_id="email_hygiene",
            agent_name="Email Hygiene & Anti-Spam",
            step="LIST_MAINTENANCE_STARTED",
            file_used="core/list_maintenance_service.py",
            message=f"Starting email list hygiene audit on {initial_count} contacts...",
            level="INFO"
        )

        seen_emails = set()
        cleaned_contacts = []
        removed_duplicates = 0
        removed_malformed = 0
        removed_suppressed = 0
        removed_unverified_domain = 0

        for c in contacts:
            email = (c.get("email") or "").strip().lower()

            # 1. Check completeness / malformed
            if not email or "@" not in email or "." not in email.split("@")[-1]:
                removed_malformed += 1
                continue

            # 2. Check duplicates
            if email in seen_emails:
                removed_duplicates += 1
                continue
            seen_emails.add(email)

            # 3. Check suppression list / legal guardrails
            suppressed, _ = legal_guardrails.is_suppressed(email)
            if suppressed:
                removed_suppressed += 1
                continue

            # 4. Check domain deliverability via tool registry
            domain_check = tool_registry.call_tool("verify_email_domain", email_address=email)
            if not domain_check.get("success") or not domain_check.get("deliverable"):
                removed_unverified_domain += 1
                continue

            cleaned_contacts.append(c)

        atomic_save_json(CONTACTS_LEDGER, cleaned_contacts)
        final_count = len(cleaned_contacts)
        total_removed = initial_count - final_count
        elapsed_ms = (time.time() - start_time) * 1000.0

        telemetry.emit(
            agent_id="email_hygiene",
            agent_name="Email Hygiene & Anti-Spam",
            step="LIST_MAINTENANCE_SUCCESS",
            file_used="core/list_maintenance_service.py",
            message=f"List hygiene audit completed in {elapsed_ms:.1f}ms. Cleaned {initial_count} down to {final_count} verified contacts.",
            level="SUCCESS"
        )

        return {
            "success": True,
            "version": "37.0 Mass Email List Maintenance",
            "execution_time_ms": elapsed_ms,
            "audit_metrics": {
                "initial_count": initial_count,
                "final_verified_count": final_count,
                "total_removed": total_removed,
                "breakdown": {
                    "duplicates_removed": removed_duplicates,
                    "malformed_removed": removed_malformed,
                    "suppressed_bounced_removed": removed_suppressed,
                    "unverified_domain_removed": removed_unverified_domain
                }
            },
            "message": f"List successfully audited and cleaned. {final_count} pristine contacts ready for campaign dispatch."
        }

list_maintenance_service = ListMaintenanceService()
