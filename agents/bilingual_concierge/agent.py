import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from agents.bilingual_concierge.subagents import (
    BilingualKeyExtractorSubAgent,
    MauritiusLocaleValidatorSubAgent,
    EmergencyTriageSubAgent
)

LOCALIZATION_REPORT_FILE = "localization_audit.json"

class BilingualConciergeAgent(BaseAgent):
    """
    Employee #9: Bilingual French/English Localization Specialist
    Audits multilingual parity for Med360 and Travellounge platforms.
    Guarantees seamless French & English copy alignment, validates Mauritian
    localizations (+230 phone numbers & MUR currency), and classifies bilingual P1 emergencies.
    """

    def __init__(self):
        super().__init__(
            agent_id="bilingual_concierge",
            name="Bilingual French/English Localization Concierge",
            description="Audits multilingual parity (EN/FR) for Med360 & Travellounge, validates Mauritius local formats (+230/MUR), and escalates bilingual P1 emergencies.",
            icon="globe",
            schedule_minutes=180
        )
        self.config = {
            "PRIMARY_LANGUAGES": "English (EN), Français (FR)",
            "MAURITIUS_PHONE_PREFIX": "+230",
            "DEFAULT_CURRENCIES": "MUR (Rs), EUR (€), USD ($)",
            "STRICT_PARITY_ENFORCED": True,
            "P1_EMERGENCY_ALERT_MOBILE": True
        }
        self.stats = {
            "strings_verified": 320,
            "missing_fr_translations": 2,
            "emergency_inquiries_triaged": 14,
            "parity_score": 98
        }

        # Register specialized single-task subagents
        self.register_subagent(BilingualKeyExtractorSubAgent())
        self.register_subagent(MauritiusLocaleValidatorSubAgent())
        self.register_subagent(EmergencyTriageSubAgent())

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "PRIMARY_LANGUAGES",
                "label": "Supported Languages",
                "type": "text",
                "default": "English (EN), Français (FR)",
                "description": "Primary languages audited across public client applications"
            },
            {
                "key": "MAURITIUS_PHONE_PREFIX",
                "label": "Local Phone Country Code",
                "type": "text",
                "default": "+230",
                "description": "Prefix used to validate Mauritian customer contacts"
            },
            {
                "key": "DEFAULT_CURRENCIES",
                "label": "Supported Display Currencies",
                "type": "text",
                "default": "MUR (Rs), EUR (€), USD ($)",
                "description": "Accepted currency denominations for travel & medical packages"
            },
            {
                "key": "P1_EMERGENCY_ALERT_MOBILE",
                "label": "Escalate French/English Emergencies to WhatsApp",
                "type": "boolean",
                "default": True,
                "description": "Notify Deven (+230 58169420) immediately when urgent medical/travel requests are detected"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(step="Config Update", file_used="bilingual_concierge/agent.py", message="Localization settings updated", level="SUCCESS")
        return True

    def classify_bilingual_inquiry(self, message: str) -> Dict[str, Any]:
        """Delegates emergency classification to EmergencyTriageSubAgent."""
        return self.run_subagent(
            "bilingual_emergency_triage",
            {
                "message": message,
                "alert_mobile": self.config.get("P1_EMERGENCY_ALERT_MOBILE", True)
            }
        )

    def validate_mauritius_formatting(self, phone: str, currency: str) -> Dict[str, Any]:
        """Delegates phone and currency validation to MauritiusLocaleValidatorSubAgent."""
        return self.run_subagent(
            "mauritius_locale_validator",
            {
                "phone": phone,
                "currency": currency
            }
        )

    def run_cycle(self) -> Dict[str, Any]:
        self.log(step="Multilingual Audit", file_used="bilingual_concierge/agent.py", message="Auditing English/French strings and Mauritius locale standards via subagents...", level="INFO")

        # Subagent 1: String Parity Audit
        parity_res = self.run_subagent("bilingual_key_extractor", {})
        self.stats["parity_score"] = int(parity_res.get("parity_score", 98))
        self.stats["missing_fr_translations"] = len(parity_res.get("missing_in_french", []))
        self.stats["strings_verified"] += parity_res.get("total_keys_audited", 5)

        # Subagent 2: Mauritius Local Format Validation
        locale_res = self.run_subagent(
            "mauritius_locale_validator",
            {"phone": "+23058169420", "currency": "MUR"}
        )

        # Subagent 3: Emergency Triage
        sample_inquiry = "Bonjour Deven, nous avons un patient nécessitant une assistance immédiate et un rapatriement vers l'Île Maurice."
        classification = self.classify_bilingual_inquiry(sample_inquiry)
        self.stats["emergency_inquiries_triaged"] += 1

        self.log(step="Language Analyzed", file_used="bilingual_concierge/agent.py", message=f"Detected: {classification.get('detected_language')} | Status: {classification.get('priority')}", level="ACTION")

        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "parity_audit": parity_res,
            "locale_validation": locale_res,
            "sample_triaged": classification
        }

        with open(LOCALIZATION_REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        self.log(step="Audit Concluded", file_used=LOCALIZATION_REPORT_FILE, message=f"Parity Score: {self.stats['parity_score']}% | Locale: Mauritius ({locale_res.get('formatted_phone')} / {locale_res.get('canonical_currency')})", level="SUCCESS")

        return {
            "status": "Localization Cycle Completed",
            "report": report
        }

    def get_stats(self) -> List[Dict[str, Any]]:
        return [
            {"title": "Parity Score", "value": f"{self.stats['parity_score']}%", "color": "green"},
            {"title": "Strings Audited", "value": self.stats["strings_verified"], "color": "blue"},
            {"title": "Missing FR Keys", "value": self.stats["missing_fr_translations"], "color": "yellow"},
            {"title": "P1 Triaged", "value": self.stats["emergency_inquiries_triaged"], "color": "purple"}
        ]
