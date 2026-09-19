import os
import re
import json
from typing import Optional

# Gemini is optional — falls back to rule-based-only if no API key
try:
    from google import genai
    from google.genai import types
    _GENAI_AVAILABLE = True
except ImportError:
    _GENAI_AVAILABLE = False

class SpamClassifier:
    """
    Advanced Spam Classifier Engine:
    - Feature 1: Immunity Shield (OTPs, Security codes, VIP Whitelist)
    - Feature 3: Brand Spoofing & Phishing Detection
    - Feature 6: Instant Blacklist Filter (banned TLDs & keywords)
    - AI Brain: Google Gemini 2.5 Flash for deep semantic reasoning
    """

    # Critical keywords that trigger the Immunity Shield (never delete)
    IMMUNITY_KEYWORDS = [
        "verification code", "one-time password", "otp", "password reset",
        "security code", "two-factor", "2fa", "login attempt", "account recovery",
        "wire confirmation", "tax document", "w-2", "flight confirmation",
        "boarding pass", "e-ticket"
    ]

    # Known major brands for spoof detection
    KNOWN_BRANDS = {
        "apple": ["apple.com", "icloud.com"],
        "google": ["google.com", "accounts.google.com", "youtube.com"],
        "microsoft": ["microsoft.com", "live.com", "outlook.com", "office.com"],
        "amazon": ["amazon.com", "amazon.co.uk", "amazon.ca", "amazon.in", "aws.amazon.com"],
        "paypal": ["paypal.com", "intl.paypal.com"],
        "netflix": ["netflix.com"],
        "meta": ["meta.com", "facebookmail.com", "instagram.com"],
        "github": ["github.com"],
        "coinbase": ["coinbase.com"],
        "chase": ["chase.com"],
        "bank of america": ["bankofamerica.com"],
        "fedex": ["fedex.com"],
        "dhl": ["dhl.com"],
        "ups": ["ups.com"]
    }

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        self.model_name = "gemini-2.5-flash"
        self._llm_available = False

        if self.api_key and _GENAI_AVAILABLE:
            try:
                self.client = genai.Client(api_key=self.api_key)
                self._llm_available = True
            except Exception:
                self._llm_available = False

        # Load configurable whitelist & blacklist from environment
        whitelist_raw = os.getenv("WHITELIST_DOMAINS", "@gmail.com,@github.com,@google.com,@apple.com")
        self.whitelist = [w.strip().lower() for w in whitelist_raw.split(",") if w.strip()]

        blacklist_dom_raw = os.getenv("BLACKLIST_DOMAINS", ".xyz,.top,.click,.buzz,.loan")
        self.blacklist_domains = [b.strip().lower() for b in blacklist_dom_raw.split(",") if b.strip()]

        blacklist_kw_raw = os.getenv("BLACKLIST_KEYWORDS", "casino,viagra,lottery winner,inheritance fund")
        self.blacklist_keywords = [k.strip().lower() for k in blacklist_kw_raw.split(",") if k.strip()]

    def check_immunity_shield(self, sender: str, subject: str, body: str) -> dict | None:
        """
        Feature 1: Immunity Shield.
        Instantly protects critical security, 2FA, OTP, and VIP senders.
        """
        sender_lower = sender.lower()
        subject_lower = subject.lower()
        body_snippet = body[:1000].lower()

        # 1. Check VIP Whitelist domains / emails
        for wl in self.whitelist:
            if wl in sender_lower:
                return {
                    "is_spam": False,
                    "confidence": 1.0,
                    "category": "Immunity Shield (VIP Whitelist)",
                    "reason": f"Sender matches whitelisted contact/domain: '{wl}'",
                    "immune": True
                }

        # 2. Check Security / 2FA / Password Reset keywords
        for kw in self.IMMUNITY_KEYWORDS:
            if kw in subject_lower or kw in body_snippet:
                return {
                    "is_spam": False,
                    "confidence": 1.0,
                    "category": "Immunity Shield (2FA / Security)",
                    "reason": f"Email contains protected security keyword: '{kw}'",
                    "immune": True
                }

        return None

    def check_blacklist(self, sender: str, subject: str, body: str) -> dict | None:
        """
        Feature 6: Fast-path instant blacklist filter.
        Trashes known bad TLDs or spam keywords without burning LLM tokens.
        """
        sender_lower = sender.lower()
        subject_lower = subject.lower()
        body_snippet = body[:1000].lower()

        for dom in self.blacklist_domains:
            if dom in sender_lower:
                return {
                    "is_spam": True,
                    "confidence": 1.0,
                    "category": "Blacklisted Domain/TLD",
                    "reason": f"Sender domain matches blacklist rule: '{dom}'",
                    "blacklisted": True
                }

        for kw in self.blacklist_keywords:
            if kw in subject_lower or kw in body_snippet:
                return {
                    "is_spam": True,
                    "confidence": 0.98,
                    "category": "Blacklisted Keyword",
                    "reason": f"Email matches banned blacklist keyword: '{kw}'",
                    "blacklisted": True
                }

        return None

    def check_brand_spoofing(self, sender: str) -> dict | None:
        """
        Feature 3: Brand Spoofing & Phishing Detector.
        Catches emails where the display name pretends to be Apple/Google/PayPal/Amazon
        but the actual sending address is from an unauthorized domain.
        """
        # Extract display name vs actual email in angle brackets
        # e.g., "Apple Security <support@alert-xyz-security.top>"
        match = re.search(r'^(.*?)\s*<([^>]+)>', sender)
        if not match:
            return None

        display_name = match.group(1).lower()
        actual_email = match.group(2).lower()
        actual_domain = actual_email.split("@")[-1] if "@" in actual_email else ""

        for brand, legitimate_domains in self.KNOWN_BRANDS.items():
            # If display name claims to be this brand
            if brand in display_name:
                # Check if the actual email domain is legitimate
                is_legit = any(actual_domain == legit or actual_domain.endswith("." + legit) for legit in legitimate_domains)
                if not is_legit:
                    return {
                        "is_spam": True,
                        "confidence": 0.99,
                        "category": "Brand Phishing / Spoofing",
                        "reason": f"Display name claims to be '{brand.title()}' but sending domain is '{actual_domain}'",
                        "spoofed": True
                    }

        return None

    def classify(self, sender: str, subject: str, body: str) -> dict:
        """
        Full 4-Stage Classification Pipeline:
        1. Immunity Shield Check (Fast Bypass)
        2. Blacklist Check (Fast Trash)
        3. Brand Spoofing Check (Phishing Trap)
        4. Gemini 2.5 Flash Deep Reasoning Engine
        """
        # 1. Immunity Shield
        immune_result = self.check_immunity_shield(sender, subject, body)
        if immune_result:
            return immune_result

        # 2. Blacklist Check
        blacklist_result = self.check_blacklist(sender, subject, body)
        if blacklist_result:
            return blacklist_result

        # 3. Brand Spoofing Check
        spoof_result = self.check_brand_spoofing(sender)
        if spoof_result:
            return spoof_result

        # 4. LLM Semantic Reasoning (Gemini 2.5 Flash)
        if not self._llm_available:
            # Safe fallback: keep email in inbox when AI is unavailable
            return {
                "is_spam": False,
                "confidence": 0.0,
                "category": "Unclassified (No API Key)",
                "reason": "Gemini API key not configured — rule-based filters passed. Email kept safely in inbox."
            }

        body_preview = body[:2500]

        prompt = f"""
You are an expert email triage security assistant.
Analyze the following email and determine if it is SPAM (or Phishing / Unsolicited Scam / Dangerous Junk) or HAM (Legitimate personal, business, transactional receipt, security alert, or subscribed newsletter).

Email Details:
- Sender: {sender}
- Subject: {subject}
- Body:
\"\"\"
{body_preview}
\"\"\"

Respond STRICTLY with valid JSON matching this schema:
{{
  "is_spam": boolean,
  "confidence": float (between 0.0 and 1.0),
  "category": string (e.g. "Phishing", "Scam", "Cold Pitch / Promo", "Legitimate", "Receipt", "Newsletter", "Personal"),
  "reason": string (short 1-2 sentence explanation of your decision)
}}
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )

            result = json.loads(response.text.strip())
            return result
        except Exception as e:
            # Fail-safe: keep email rather than risk deleting something important
            return {
                "is_spam": False,
                "confidence": 0.0,
                "category": "Error (Kept)",
                "reason": f"LLM classification error — email kept safely: {str(e)}"
            }
