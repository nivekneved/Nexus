import os
import json
import time
from typing import Dict, Any, Optional
from core.subagent import BaseSubAgent
from core.polymorphic_engine import engine
from security.shield import shield
from spam_classifier import SpamClassifier

class EmailImmunitySubAgent(BaseSubAgent):
    """Subagent 1: Fast-pass bypass for 2FA, OTPs, password resets, and VIP whitelist domains."""
    def __init__(self):
        super().__init__(
            subagent_id="email_immunity_shield",
            name="Immunity & 2FA Shield SubAgent",
            parent_agent_id="email_hygiene",
            description="Guarantees 2FA tokens, password resets, and VIP domains bypass AI triage with zero false-positive risk."
        )
        self.classifier = SpamClassifier()

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        sender = payload.get("sender", "")
        subject = payload.get("subject", "")
        body = payload.get("body", "")

        is_immune, reason = self.classifier.check_immunity_shield(sender, subject, body)
        return {
            "is_immune": is_immune,
            "reason": reason
        }


class EmailSpoofHunterSubAgent(BaseSubAgent):
    """Subagent 2: Brand Spoofing Phishing Trap."""
    def __init__(self):
        super().__init__(
            subagent_id="email_spoof_hunter",
            name="Brand Spoofing Hunter SubAgent",
            parent_agent_id="email_hygiene",
            description="Catches phishing senders displaying corporate brand names (PayPal, Apple, Google) from fraudulent addresses."
        )
        self.classifier = SpamClassifier()

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        sender = payload.get("sender", "")
        is_spoof, reason = self.classifier.check_brand_spoofing(sender)
        return {
            "is_spoof": is_spoof,
            "reason": reason
        }


class EmailBlacklistSubAgent(BaseSubAgent):
    """Subagent 3: Fast Blacklist Engine for spam TLDs and banned keywords."""
    def __init__(self):
        super().__init__(
            subagent_id="email_blacklist_killer",
            name="Blacklist Keyword & TLD SubAgent",
            parent_agent_id="email_hygiene",
            description="Instantly matches malicious TLDs (.xyz, .top, .buzz) and prohibited spam keywords without invoking LLM."
        )
        self.classifier = SpamClassifier()

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        sender = payload.get("sender", "")
        subject = payload.get("subject", "")
        body = payload.get("body", "")

        is_blacklisted, reason = self.classifier.check_blacklist(sender, subject, body)
        return {
            "is_blacklisted": is_blacklisted,
            "reason": reason
        }


class EmailClassifierSubAgent(BaseSubAgent):
    """Subagent 4: Gemini LLM structured triage reasoning with Polymorphic Engine caching."""
    def __init__(self):
        super().__init__(
            subagent_id="email_gemini_evaluator",
            name="Gemini Structured Evaluator SubAgent",
            parent_agent_id="email_hygiene",
            description="Invokes Gemini 2.5 Flash with structured schema to judge email intent with polymorphic SHA-256 caching."
        )
        self.classifier = SpamClassifier()

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        sender = payload.get("sender", "")
        subject = payload.get("subject", "")
        body = payload.get("body", "")

        # Use polymorphic caching on email hash
        cache_key = {"sender": sender, "subject": subject, "body_preview": body[:200]}
        
        def _classify():
            # Cost guard check
            shield.consume_api_token(1)
            return self.classifier.classify(sender, subject, body)

        result = engine.cached_execute(
            namespace="email_gemini_classification",
            key_data=cache_key,
            executor_fn=_classify,
            ttl_seconds=600
        )
        return result


class EmailAuditLedgerSubAgent(BaseSubAgent):
    """Subagent 5: Tamper-Evident Ledger Hashing and Persistent Audit Logger."""
    def __init__(self):
        super().__init__(
            subagent_id="email_audit_ledger",
            name="Tamper-Evident Ledger SubAgent",
            parent_agent_id="email_hygiene",
            description="Generates SHA-256 tamper-evident integrity hashes for every trashed or quarantined email."
        )
        self.ledger_file = "trash_ledger.json"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        entry = payload.get("entry", {})
        # Generate SHA-256 tamper-evident hash
        audit_hash = shield.generate_audit_hash(entry)
        entry["audit_hash"] = audit_hash
        entry["timestamp"] = entry.get("timestamp") or time.strftime("%Y-%m-%d %H:%M:%S")

        ledger = []
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, "r", encoding="utf-8") as f:
                    ledger = json.load(f)
            except Exception:
                ledger = []

        ledger.append(entry)
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2, ensure_ascii=False)

        return {
            "success": True,
            "uid": entry.get("uid"),
            "audit_hash": audit_hash,
            "total_ledger_entries": len(ledger)
        }
