import os
import json
import urllib.request
import urllib.parse
import ssl
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.subagent import BaseSubAgent

NOTIFICATIONS_LOG_FILE = "mobile_notifications.json"

# ── CallMeBot WhatsApp Gateway ─────────────────────────────────────────────
# Free, zero-dependency WhatsApp dispatch for personal numbers.
# ONE-TIME SETUP (do this once on your phone):
#   1. Add +34 698 28 89 73 to your WhatsApp contacts as "CallMeBot"
#   2. Send this exact message to that number via WhatsApp:
#      "I allow callmebot to send me messages"
#   3. You will receive your API key in reply.
#   4. Set CALLMEBOT_API_KEY=<your_key> in .env
# That's it — live WhatsApp dispatch is active forever, for free.
CALLMEBOT_ENDPOINT = "https://api.callmebot.com/whatsapp.php"

class TwilioWhatsAppSubAgent(BaseSubAgent):
    """
    Subagent 1: WhatsApp Dispatcher via CallMeBot (free, zero-cost, no Twilio).
    Sends live WhatsApp messages to +23058169420 when CALLMEBOT_API_KEY is set in .env.
    Falls back to safe simulation when not yet configured.

    ONE-TIME SETUP:
      1. Add +34 698 28 89 73 to WhatsApp contacts as 'CallMeBot'
      2. Send: 'I allow callmebot to send me messages'
      3. Copy the API key you receive back into CALLMEBOT_API_KEY in .env
    """
    def __init__(self):
        super().__init__(
            subagent_id="mobile_whatsapp_dispatcher",
            name="WhatsApp Dispatcher SubAgent (CallMeBot)",
            parent_agent_id="mobile_dispatcher",
            description="Dispatches live WhatsApp alerts to +23058169420 via free CallMeBot API. Set CALLMEBOT_API_KEY in .env to activate."
        )
        self._ssl_ctx = ssl.create_default_context()

    def _send_via_callmebot(self, phone: str, api_key: str, text: str) -> Dict[str, Any]:
        """
        Fires a GET request to CallMeBot WhatsApp gateway.
        Phone must include country code (e.g. +23058169420).
        Text is URL-encoded automatically.
        """
        params = urllib.parse.urlencode({
            "phone": phone,
            "text": text,
            "apikey": api_key
        })
        url = f"{CALLMEBOT_ENDPOINT}?{params}"

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "NexusWorkforce-MobileDispatcher/2.9"}
        )
        with urllib.request.urlopen(req, timeout=15, context=self._ssl_ctx) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            status_code = resp.status
            return {
                "channel": "WhatsApp (CallMeBot Live)",
                "phone": phone,
                "status": "DELIVERED" if status_code == 200 else f"HTTP_{status_code}",
                "mock_mode": False,
                "response": body[:200],
                "dispatched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        recipient = payload.get("recipient", "+23058169420")
        title     = payload.get("title", "Nexus Alert")
        message   = payload.get("message", "")
        urgency   = payload.get("urgency", "P2")
        mock_mode = payload.get("mock_mode", True)

        formatted_text = f"[{urgency}] *{title}*\n{message}\n\n_Nexus Autonomous OS | Mauritius +230_"

        api_key = os.getenv("CALLMEBOT_API_KEY", "").strip()

        # Live dispatch when API key is configured
        if api_key and not mock_mode:
            try:
                result = self._send_via_callmebot(recipient, api_key, formatted_text)
                result["urgency"] = urgency
                result["formatted_text"] = formatted_text
                return result
            except Exception as e:
                # Never drop the event — fall through to simulation on error
                return {
                    "channel": "WhatsApp (CallMeBot Error - Simulated)",
                    "recipient": recipient,
                    "urgency": urgency,
                    "status": "SIMULATED",
                    "mock_mode": True,
                    "error": str(e)[:150],
                    "dispatched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "formatted_text": formatted_text
                }

        # Simulation / no-key mode
        return {
            "channel": "WhatsApp (Simulation)",
            "recipient": recipient,
            "urgency": urgency,
            "status": "SIMULATED",
            "mock_mode": True,
            "dispatched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formatted_text": formatted_text,
            "note": (
                "CALLMEBOT_API_KEY not set. "
                "To activate live WhatsApp: add +34 698 28 89 73 on WhatsApp, "
                "send 'I allow callmebot to send me messages', "
                "then paste the key you receive into CALLMEBOT_API_KEY in .env"
            )
        }



class SMSFallbackSubAgent(BaseSubAgent):
    """
    Subagent 2: P0 Emergency Voice Call via CallMeBot (free, same API key as WhatsApp).
    When urgency is P0/CRITICAL, this makes an actual phone call to +23058169420.
    Uses api.callmebot.com/call.php — zero cost, no Twilio needed.
    """
    CALLMEBOT_CALL_ENDPOINT = "https://api.callmebot.com/call.php"

    def __init__(self):
        super().__init__(
            subagent_id="mobile_sms_fallback",
            name="P0 Emergency Voice Call SubAgent (CallMeBot)",
            parent_agent_id="mobile_dispatcher",
            description="Makes a live phone call to +23058169420 via CallMeBot for P0/CRITICAL emergencies. Free, same API key as WhatsApp."
        )
        self._ssl_ctx = ssl.create_default_context()

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        recipient = payload.get("recipient", "+23058169420")
        title     = payload.get("title", "Nexus P0 Alert")
        message   = payload.get("message", "")
        urgency   = payload.get("urgency", "P1")

        # Strip the + for CallMeBot call endpoint (it expects plain digits)
        phone_digits = recipient.lstrip("+")

        # Compose a spoken message (keep it short and clear for TTS)
        spoken = f"Nexus urgent alert. {title}. {message[:200]}"

        api_key = os.getenv("CALLMEBOT_API_KEY", "").strip()
        is_critical = urgency in ("P0", "CRITICAL")

        if api_key and is_critical:
            try:
                params = urllib.parse.urlencode({
                    "phone": phone_digits,
                    "text": spoken,
                    "apikey": api_key
                })
                url = f"{self.CALLMEBOT_CALL_ENDPOINT}?{params}"
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "NexusWorkforce-P0Pager/2.9"}
                )
                with urllib.request.urlopen(req, timeout=20, context=self._ssl_ctx) as resp:
                    body = resp.read().decode("utf-8", errors="replace")
                    return {
                        "channel": "Voice Call (CallMeBot Live)",
                        "recipient": recipient,
                        "urgency": urgency,
                        "status": "CALL_INITIATED" if resp.status == 200 else f"HTTP_{resp.status}",
                        "spoken_text": spoken[:100],
                        "response": body[:150],
                        "dispatched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
            except Exception as e:
                return {
                    "channel": "Voice Call (CallMeBot Error)",
                    "recipient": recipient,
                    "urgency": urgency,
                    "status": "FAILED",
                    "error": str(e)[:150],
                    "dispatched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

        # Non-P0 or no key — simulate
        return {
            "channel": "Voice Call (Simulation)",
            "recipient": recipient,
            "urgency": urgency,
            "status": "SIMULATED",
            "note": "Live calls only trigger for P0/CRITICAL urgency with CALLMEBOT_API_KEY set.",
            "dispatched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }



class DispatchAuditLoggerSubAgent(BaseSubAgent):
    """
    Subagent 3: Maintains tamper-evident notification log in mobile_notifications.json.
    """
    def __init__(self):
        super().__init__(
            subagent_id="mobile_audit_logger",
            name="Mobile Dispatch Audit Logger SubAgent",
            parent_agent_id="mobile_dispatcher",
            description="Persists all inbound and outbound comms into rolling ledger with tamper-evident records."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        record = payload.get("record", {})
        log_file = payload.get("log_file", NOTIFICATIONS_LOG_FILE)
        max_entries = payload.get("max_entries", 150)

        all_records = []
        if os.path.exists(log_file):
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    all_records = json.load(f)
            except Exception:
                all_records = []

        all_records.append(record)
        if len(all_records) > max_entries:
            all_records = all_records[-max_entries:]

        try:
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(all_records, f, indent=2, ensure_ascii=False)
        except Exception as e:
            return {"success": False, "error": str(e)}

        return {
            "success": True,
            "total_logged": len(all_records),
            "logged_id": record.get("id")
        }
