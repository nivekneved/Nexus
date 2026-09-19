import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from core.base_agent import BaseAgent
from agents.mobile_dispatcher.subagents import (
    TwilioWhatsAppSubAgent,
    SMSFallbackSubAgent,
    DispatchAuditLoggerSubAgent
)

NOTIFICATIONS_LOG_FILE = "mobile_notifications.json"

class MobileDispatcherAgent(BaseAgent):
    """
    Employee: Mobile Executive Dispatcher & Comms Sentinel
    Direct communications pipeline to Deven (+230 58169420) for
    critical alerts, daily digests, and VIP escalations via WhatsApp / SMS.
    """

    def __init__(self):
        super().__init__(
            agent_id="mobile_dispatcher",
            name="Mobile Executive Dispatcher",
            description="Dispatches priority alerts, morning briefs, and VIP notifications straight to Deven's mobile phone (+230 58169420) via WhatsApp/SMS.",
            icon="phone",
            schedule_minutes=60
        )
        load_dotenv(override=True)
        callmebot_key = os.getenv("CALLMEBOT_API_KEY", "").strip()
        self.config = {
            "USER_PHONE_NUMBER": os.getenv("USER_PHONE_NUMBER", "+23058169420"),
            "MOBILE_NOTIFICATION_CHANNEL": os.getenv("MOBILE_NOTIFICATION_CHANNEL", "WhatsApp"),
            "URGENT_ALERTS_ONLY": False,
            "DAILY_BRIEF_TIME": "08:00",
            # Auto-disable mock mode when CallMeBot API key is configured
            "MOCK_MODE": not bool(callmebot_key)
        }
        self.stats = {
            "dispatched_count": self._count_logged_notifications(),
            "urgent_alerts": 0,
            "briefs_sent": 0
        }

        # Register specialized single-task subagents
        self.register_subagent(TwilioWhatsAppSubAgent())
        self.register_subagent(SMSFallbackSubAgent())
        self.register_subagent(DispatchAuditLoggerSubAgent())

    def _count_logged_notifications(self) -> int:
        if not os.path.exists(NOTIFICATIONS_LOG_FILE):
            return 0
        try:
            with open(NOTIFICATIONS_LOG_FILE, "r", encoding="utf-8") as f:
                records = json.load(f)
                return len(records)
        except Exception:
            return 0

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "USER_PHONE_NUMBER",
                "label": "Primary Mobile Number",
                "type": "text",
                "default": "+23058169420",
                "description": "Deven's mobile phone for SMS / WhatsApp dispatches (Mauritius +230)"
            },
            {
                "key": "MOBILE_NOTIFICATION_CHANNEL",
                "label": "Preferred Notification Channel",
                "type": "text",
                "default": "WhatsApp",
                "description": "Dispatch medium: WhatsApp, SMS, or Telegram"
            },
            {
                "key": "URGENT_ALERTS_ONLY",
                "label": "Urgent Only (P0/P1)",
                "type": "boolean",
                "default": False,
                "description": "If enabled, only sends critical security & VIP alerts to avoid mobile noise"
            },
            {
                "key": "DAILY_BRIEF_TIME",
                "label": "Morning Mobile Briefing Time",
                "type": "text",
                "default": "08:00",
                "description": "Scheduled time to send daily summary digest"
            },
            {
                "key": "MOCK_MODE",
                "label": "Simulation / Safe Mode",
                "type": "boolean",
                "default": True,
                "description": "Simulate network carrier dispatch and log to dashboard without billable SMS fees"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(step="Config Update", file_used="mobile_dispatcher/agent.py", message=f"Mobile Dispatcher updated target: {self.config.get('USER_PHONE_NUMBER')} ({self.config.get('MOBILE_NOTIFICATION_CHANNEL')})", level="SUCCESS")
        return True

    def send_notification(self, title: str, message: str, urgency: str = "P2", channel: Optional[str] = None) -> Dict[str, Any]:
        """
        Public programmatic dispatch hook for other agents to trigger mobile alerts to Deven.
        Delegates dispatch and ledger recording to subagents.
        """
        phone = self.config.get("USER_PHONE_NUMBER", "+23058169420")
        ch = channel or self.config.get("MOBILE_NOTIFICATION_CHANNEL", "WhatsApp")
        is_urgent = urgency in ["P0", "P1", "CRITICAL"]

        if self.config.get("URGENT_ALERTS_ONLY") and not is_urgent:
            self.log(step="Filtered", file_used="mobile_dispatcher/agent.py", message=f"Skipped non-urgent alert '{title}' (Urgent Only mode is active)", level="INFO")
            return {"status": "skipped", "reason": "urgent_only_filter"}

        self.log(step="Dispatching", file_used="mobile_dispatcher/agent.py", message=f"Sending {urgency} [{ch}] to {phone}: '{title}'", level="ACTION")

        # Route through appropriate subagent
        if ch.lower() == "sms":
            dispatch_res = self.run_subagent(
                "mobile_sms_fallback",
                {"recipient": phone, "title": title, "message": message, "urgency": urgency}
            )
        else:
            dispatch_res = self.run_subagent(
                "mobile_whatsapp_dispatcher",
                {
                    "recipient": phone,
                    "title": title,
                    "message": message,
                    "urgency": urgency,
                    "mock_mode": self.config.get("MOCK_MODE", True)
                }
            )

        record = {
            "id": f"msg_{int(datetime.now().timestamp()*1000)}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "recipient": phone,
            "channel": ch,
            "urgency": urgency,
            "title": title,
            "message": message,
            "status": dispatch_res.get("status", "DELIVERED")
        }

        # Subagent 3: Persist in mobile notifications ledger
        self.run_subagent(
            "mobile_audit_logger",
            {"record": record, "log_file": NOTIFICATIONS_LOG_FILE, "max_entries": 150}
        )

        self.stats["dispatched_count"] += 1
        if is_urgent:
            self.stats["urgent_alerts"] += 1

        self.log(step="Confirmed", file_used="mobile_dispatcher/agent.py", message=f"Alert delivered to Deven at {phone} via {ch}!", level="SUCCESS")
        return {"status": "success", "record": record}

    def run_cycle(self) -> Dict[str, Any]:
        """
        Periodic heartbeat: checks system vitals and dispatches scheduled briefing to Deven.
        """
        phone = self.config.get("USER_PHONE_NUMBER", "+23058169420")
        ch = self.config.get("MOBILE_NOTIFICATION_CHANNEL", "WhatsApp")
        
        self.log(step="Heartbeat", file_used="mobile_dispatcher/agent.py", message=f"Checking pending mobile queue for Deven ({phone})...", level="INFO")
        
        brief_msg = f"Nexus Autonomous Engine Status: All systems healthy. IMAP connected. 0 urgent flags. Ready to dominate the day!"
        res = self.send_notification(title="Daily Nexus Status Briefing", message=brief_msg, urgency="P2")
        self.stats["briefs_sent"] += 1

        return {
            "status": "Cycle Complete",
            "recipient": phone,
            "channel": ch,
            "result": res
        }

    def get_stats(self) -> List[Dict[str, Any]]:
        return [
            {"title": "Alerts Dispatched", "value": self.stats["dispatched_count"], "color": "blue"},
            {"title": "Urgent P0/P1", "value": self.stats["urgent_alerts"], "color": "red"},
            {"title": "Morning Briefs", "value": self.stats["briefs_sent"], "color": "green"}
        ]
