import re
from typing import Dict, Any, List
from core.subagent import BaseSubAgent
from core.agent_manager import AgentManager

FRENCH_P1_TRIGGER_KEYWORDS = [
    "urgence", "evacuation sanitaire", "rapatriement", "ambulance", "hospitalisation",
    "infarctus", "accident", "perte de passeport", "vol annule", "assistance immediate"
]

ENGLISH_P1_TRIGGER_KEYWORDS = [
    "emergency", "medical evacuation", "repatriation", "ambulance", "hospitalization",
    "heart attack", "accident", "lost passport", "flight cancelled", "immediate assistance"
]

class BilingualKeyExtractorSubAgent(BaseSubAgent):
    """
    Subagent 1: Audits multilingual key parity across English and French locales.
    """
    def __init__(self):
        super().__init__(
            subagent_id="bilingual_key_extractor",
            name="Bilingual String & Parity Auditor SubAgent",
            parent_agent_id="bilingual_concierge",
            description="Audits copy dictionaries across EN/FR for key parity, missing translations, and placeholder mismatches."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        en_strings = payload.get("en_strings", {})
        fr_strings = payload.get("fr_strings", {})

        # Default sample dictionary if empty
        if not en_strings:
            en_strings = {
                "nav.home": "Home",
                "nav.services": "Medical Services",
                "nav.contact": "Contact Specialist",
                "cta.book": "Book Evacuation Consultation",
                "label.phone": "Emergency Hotline (+230)"
            }
        if not fr_strings:
            fr_strings = {
                "nav.home": "Accueil",
                "nav.services": "Services Médicaux",
                "nav.contact": "Contacter un Spécialiste",
                "cta.book": "Réserver une Consultation Évacuation"
                # "label.phone" is intentionally missing to demonstrate parity audit
            }

        en_keys = set(en_strings.keys())
        fr_keys = set(fr_strings.keys())

        missing_in_fr = list(en_keys - fr_keys)
        missing_in_en = list(fr_keys - en_keys)
        total_keys = len(en_keys.union(fr_keys))

        matched_keys = len(en_keys.intersection(fr_keys))
        parity_score = round((matched_keys / max(total_keys, 1)) * 100, 1)

        return {
            "total_keys_audited": total_keys,
            "matched_keys": matched_keys,
            "parity_score": parity_score,
            "missing_in_french": missing_in_fr,
            "missing_in_english": missing_in_en
        }


class MauritiusLocaleValidatorSubAgent(BaseSubAgent):
    """
    Subagent 2: Validates Mauritian localization standards (+230 phone numbers and MUR/EUR/USD currencies).
    """
    def __init__(self):
        super().__init__(
            subagent_id="mauritius_locale_validator",
            name="Mauritius Locale Validator SubAgent",
            parent_agent_id="bilingual_concierge",
            description="Validates local Mauritian phone formats (+230) and currency tokens (MUR, Rs, EUR, USD)."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        phone = payload.get("phone", "")
        currency = payload.get("currency", "MUR")

        cleaned_phone = re.sub(r"[\s\-\(\)]", "", str(phone))
        valid_phone = cleaned_phone.startswith("+230") and len(cleaned_phone) == 12
        
        valid_currencies = ["MUR", "RS", "EUR", "€", "USD", "$"]
        currency_clean = str(currency).upper().strip()
        valid_curr = any(c in currency_clean for c in valid_currencies)

        formatted_phone = f"+230 {cleaned_phone[4:8]} {cleaned_phone[8:]}" if valid_phone else phone

        return {
            "phone_valid": valid_phone,
            "currency_valid": valid_curr,
            "formatted_phone": formatted_phone,
            "canonical_currency": currency_clean if valid_curr else "INVALID"
        }


class EmergencyTriageSubAgent(BaseSubAgent):
    """
    Subagent 3: Classifies incoming inquiries for medical/travel P1 emergencies in EN and FR.
    """
    def __init__(self):
        super().__init__(
            subagent_id="bilingual_emergency_triage",
            name="Bilingual Emergency Triage SubAgent",
            parent_agent_id="bilingual_concierge",
            description="Performs heuristic language detection and scans for high-severity P1 emergency keywords in French and English."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        message = payload.get("message", "")
        alert_mobile = payload.get("alert_mobile", True)
        msg_lower = message.lower()
        
        # Heuristic language detection
        is_french = any(w in msg_lower for w in ["bonjour", "merci", "urgence", "patient", "rapatriement", "pourquoi", "nous", "vous", "est"])
        detected_lang = "French (FR)" if is_french else "English (EN)"

        # Urgency trigger evaluation
        p1_matched = []
        triggers = FRENCH_P1_TRIGGER_KEYWORDS if is_french else ENGLISH_P1_TRIGGER_KEYWORDS
        for trig in triggers:
            if trig in msg_lower:
                p1_matched.append(trig)

        is_p1 = len(p1_matched) > 0
        priority = "P1 Urgent" if is_p1 else "Normal Inquiry"

        # Dispatch mobile alert if P1 and requested
        escalated_to_mobile = False
        if is_p1 and alert_mobile:
            manager = AgentManager()
            dispatcher = manager.get_agent("mobile_dispatcher")
            if dispatcher and hasattr(dispatcher, "send_notification"):
                dispatcher.send_notification(
                    title="🚨 Urgence P1 / Medical Escalation",
                    message=f"Bilingual Concierge intercepted urgent request ({detected_lang}): '{message[:120]}...'",
                    urgency="P1"
                )
                escalated_to_mobile = True

        return {
            "detected_language": detected_lang,
            "is_p1_urgent": is_p1,
            "matched_triggers": p1_matched,
            "priority": priority,
            "escalated_to_mobile": escalated_to_mobile
        }
