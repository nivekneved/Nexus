"""
Nexus Legal Compliance & Operational Guardrail System
=====================================================
Protects Deven and Nexus from legal, regulatory, reputational, and operational liability:
1. CAN-SPAM / GDPR / Mauritius Data Protection Act 2017 Compliance.
2. Mandatory Opt-Out & Unsubscribe mechanism with zero-friction compliance.
3. Permanent Suppression Registry (Hard bounces, Opt-outs, Invalid domains).
4. Anti-Harassment Cadence Guardrail (14-day contact cooldown).
5. Outbound SMTP Velocity Guardrail (Max 15/hour, 50/day) to safeguard personal Google account.
6. Pre-Flight DNS MX Verification before any network packet hits SMTP.
"""

import os
import re
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple

from core.storage import atomic_save_json, safe_load_json
from core.email_verifier import verify_email_deliverability

logger = logging.getLogger("Nexus.LegalGuardrails")

SUPPRESSION_FILE = os.path.join("data", "suppression_list.json")
DISPATCH_QUOTA_FILE = os.path.join("data", "dispatch_quota.json")

# Default seeds of known dead/unresolvable domains from past scans
INITIAL_SUPPRESSED_DOMAINS = [
    "chamarel-lodge.mu",
    "bellemare-azure.mu",
    "lemorne-villas.mu",
    "mru-discovery.mu",
    "coralcove.mu",
    "southernpalms.mu",
    "bluelagoon-cruises.mu",
    "apexrentals.mu"
]

class LegalGuardrailsService:
    def __init__(self):
        self._ensure_suppression_initialized()

    def _ensure_suppression_initialized(self):
        """Bootstraps suppression list if missing."""
        data = safe_load_json(SUPPRESSION_FILE, default=None)
        if data is None:
            initial = {
                "emails": {},
                "domains": {dom: {"reason": "Non-existent domain (No MX record)", "added_at": "2026-09-19 18:00:00"} for dom in INITIAL_SUPPRESSED_DOMAINS},
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            atomic_save_json(SUPPRESSION_FILE, initial)

    def is_suppressed(self, email_address: str) -> Tuple[bool, Optional[str]]:
        """Checks if an email address or its root domain is permanently suppressed."""
        if not email_address:
            return True, "EMPTY_EMAIL"
        clean = email_address.strip().lower()
        domain = clean.split("@")[-1] if "@" in clean else clean

        data = safe_load_json(SUPPRESSION_FILE, default={"emails": {}, "domains": {}})
        emails = data.get("emails", {})
        domains = data.get("domains", {})

        if clean in emails:
            return True, f"Address suppressed: {emails[clean].get('reason', 'Opted out or bounced')}"

        if domain in domains:
            return True, f"Domain '@{domain}' suppressed: {domains[domain].get('reason', 'Invalid domain / No MX')}"

        return False, None

    def add_suppression(self, target: str, reason: str = "Bounced / Delivery Failure", source: str = "auto_guardrail") -> bool:
        """Adds an email or domain to the permanent suppression registry."""
        clean = target.strip().lower()
        data = safe_load_json(SUPPRESSION_FILE, default={"emails": {}, "domains": {}})
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"reason": reason, "added_at": now_str, "source": source}

        if "@" in clean:
            data.setdefault("emails", {})[clean] = entry
        else:
            data.setdefault("domains", {})[clean] = entry

        data["updated_at"] = now_str
        atomic_save_json(SUPPRESSION_FILE, data)
        logger.info(f"[LegalGuardrail] Suppressed '{clean}': {reason}")
        return True

    def remove_suppression(self, target: str) -> bool:
        """Removes an email or domain from suppression (for manual whitelist overrides)."""
        clean = target.strip().lower()
        data = safe_load_json(SUPPRESSION_FILE, default={"emails": {}, "domains": {}})
        updated = False
        if "@" in clean and clean in data.get("emails", {}):
            del data["emails"][clean]
            updated = True
        elif clean in data.get("domains", {}):
            del data["domains"][clean]
            updated = True
        if updated:
            data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            atomic_save_json(SUPPRESSION_FILE, data)
        return updated

    def get_suppression_data(self) -> Dict[str, Any]:
        return safe_load_json(SUPPRESSION_FILE, default={"emails": {}, "domains": {}})

    def check_rate_limits(self, max_per_hour: int = 15, max_per_day: int = 50) -> Tuple[bool, Optional[str]]:
        """
        Enforces outbound velocity caps to protect personal Google SMTP credentials
        from being flagged for automated spam abuse.
        """
        quota = safe_load_json(DISPATCH_QUOTA_FILE, default={"dispatches": []})
        now = time.time()
        one_hour_ago = now - 3600
        one_day_ago = now - 86400

        # Prune older than 24h
        valid_dispatches = [t for t in quota.get("dispatches", []) if t > one_day_ago]
        hourly_count = sum(1 for t in valid_dispatches if t > one_hour_ago)
        daily_count = len(valid_dispatches)

        if hourly_count >= max_per_hour:
            return False, f"Hourly dispatch limit reached ({hourly_count}/{max_per_hour}). Cooling down to protect sender reputation."

        if daily_count >= max_per_day:
            return False, f"Daily dispatch limit reached ({daily_count}/{max_per_day}). Scheduled resumption tomorrow."

        return True, None

    def record_dispatch_quota(self):
        """Records a successful outbound email in quota tracker."""
        quota = safe_load_json(DISPATCH_QUOTA_FILE, default={"dispatches": []})
        quota.setdefault("dispatches", []).append(time.time())
        # keep last 200
        quota["dispatches"] = quota["dispatches"][-200:]
        atomic_save_json(DISPATCH_QUOTA_FILE, quota)

    def check_contact_cooldown(self, email_address: str, cooldown_days: int = 14) -> Tuple[bool, Optional[str]]:
        """
        Anti-Harassment Guardrail: Guarantees a prospect is not contacted more
        than once every 14 days, fully adhering to anti-spam best practices.
        """
        from core.contact_history_service import contact_history_service
        contact = contact_history_service.get_contact_by_email(email_address)
        if not contact:
            return True, None

        last_str = contact.get("last_contacted")
        if not last_str:
            return True, None

        try:
            last_dt = datetime.strptime(last_str, "%Y-%m-%d %H:%M:%S")
            days_elapsed = (datetime.now() - last_dt).total_seconds() / 86400.0
            if days_elapsed < cooldown_days:
                remaining_days = round(cooldown_days - days_elapsed, 1)
                return False, f"Anti-harassment cooldown active: Contact was messaged {int(days_elapsed)}d ago. Wait {remaining_days}d."
        except Exception:
            pass

        return True, None

    def append_opt_out_footer(self, body_text: str, recipient_email: str) -> str:
        """
        Appends a fully compliant CAN-SPAM / Mauritius Data Protection Act 2017
        opt-out and identification footer to cold outreach emails.
        """
        if "Legal Notice & Opt-Out" in body_text or "Unsubscribe" in body_text:
            return body_text

        footer = (
            "\n\n---\n"
            "⚖️ Legal Notice & Opt-Out:\n"
            "You received this commercial proposal because your organization was identified as an established entity in Mauritius.\n"
            "If you do not wish to receive further communications regarding autonomous enterprise software, simply reply 'Unsubscribe' "
            "to be permanently excluded.\n\n"
            "Nexus AI Solutions • Grand Baie / Cybercity, Mauritius • Deven Pawaray (+230 58169420)\n"
            "Terms of Sale: https://nexus-workforce.vercel.app/terms"
        )
        return body_text + footer

    def pre_flight_check(
        self,
        recipient_email: str,
        ignore_cooldown: bool = False,
        skip_quota: bool = False
    ) -> Dict[str, Any]:
        """
        Comprehensive pre-send gatekeeper:
        1. Checks suppression registry.
        2. Validates email syntax & blocks throwaways.
        3. Validates DNS MX records (eliminates non-existent domains).
        4. Verifies anti-harassment 14-day cooldown.
        5. Verifies outbound rate limits.
        """
        clean_email = (recipient_email or "").strip().lower()
        if not clean_email or "@" not in clean_email:
            return {"allowed": False, "code": "INVALID_SYNTAX", "reason": "Invalid or empty email address"}

        # 1. Check Suppression Registry
        is_supp, supp_reason = self.is_suppressed(clean_email)
        if is_supp:
            return {"allowed": False, "code": "SUPPRESSED", "reason": supp_reason}

        # 2. Check Anti-Harassment Cooldown
        if not ignore_cooldown:
            can_contact, cooldown_reason = self.check_contact_cooldown(clean_email)
            if not can_contact:
                return {"allowed": False, "code": "COOLDOWN_ACTIVE", "reason": cooldown_reason}

        # 3. Check Outbound Quota Rate Limits
        if not skip_quota:
            quota_ok, quota_reason = self.check_rate_limits()
            if not quota_ok:
                return {"allowed": False, "code": "QUOTA_EXCEEDED", "reason": quota_reason}

        # 4. Perform DNS MX Deliverability Verification
        is_deliverable, mx_reason, primary_mx = verify_email_deliverability(clean_email)
        if not is_deliverable:
            # Automatically add dead domain to suppression list to protect future cycles
            domain = clean_email.split("@")[-1]
            self.add_suppression(domain, reason=f"Deliverability failure: {mx_reason}", source="mx_gatekeeper")
            return {
                "allowed": False,
                "code": "NO_MX_RECORDS",
                "reason": f"Domain '@{domain}' has no valid Mail Exchange (MX) records ({mx_reason}). Outbound dispatch blocked to protect sender reputation."
            }

        return {
            "allowed": True,
            "code": "VERIFIED",
            "primary_mx": primary_mx,
            "reason": "Passed all legal, deliverability, and rate-limit guardrails"
        }

legal_guardrails = LegalGuardrailsService()
