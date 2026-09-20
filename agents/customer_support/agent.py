import os
import json
from datetime import datetime
from typing import Dict, Any, List
from core.base_agent import BaseAgent
from agents.customer_support.subagents import (
    TicketSentimentClassifierSubAgent,
    VIPEscalationSubAgent,
    SupportReplyDrafterSubAgent
)

TICKETS_FILE = "support_tickets.json"

class CustomerSupportAgent(BaseAgent):
    """
    Employee #4: Customer Support & VIP Concierge
    Monitors incoming inquiries, evaluates sentiment, drafts context-aware replies,
    and escalates P1 urgent requests straight to Deven's mobile phone (+230 58169420).
    """
    def __init__(self):
        super().__init__(
            agent_id="customer_support",
            name="Customer Support & VIP Concierge",
            description="24/7 client triage: analyzes sentiment, drafts empathetic replies, and triggers mobile alerts to Deven (+230 58169420) for P1 emergencies.",
            icon="support",
            schedule_minutes=30
        )
        self.config = {
            "AUTO_DRAFT_RESPONSES": True,
            "P1_MOBILE_ALERT": True,
            "ESCALATION_EMAIL": "devenpawaray@gmail.com",
            "BRAND_TONE": "Empathetic, clear, and reassuring"
        }
        self.stats = {
            "tickets_reviewed": 28,
            "p1_escalations": 2,
            "drafts_ready": 7
        }

        # Register specialized single-task subagents
        self.register_subagent(TicketSentimentClassifierSubAgent())
        self.register_subagent(VIPEscalationSubAgent())
        self.register_subagent(SupportReplyDrafterSubAgent())

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "AUTO_DRAFT_RESPONSES",
                "label": "Auto-Draft Responses",
                "type": "boolean",
                "default": True,
                "description": "Pre-generate contextual AI responses ready for 1-click send"
            },
            {
                "key": "P1_MOBILE_ALERT",
                "label": "Mobile Alert on P1 Urgent",
                "type": "boolean",
                "default": True,
                "description": "Immediately alert Deven (+230 58169420) on mobile for critical tickets"
            },
            {
                "key": "ESCALATION_EMAIL",
                "label": "Escalation Notification Email",
                "type": "text",
                "default": "devenpawaray@gmail.com",
                "description": "Backup email for emergency escalations"
            },
            {
                "key": "BRAND_TONE",
                "label": "Response Tone & Voice",
                "type": "text",
                "default": "Empathetic, clear, and reassuring",
                "description": "AI persona guidelines when drafting responses"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(step="Config Update", file_used="customer_support/agent.py", message="Support concierge preferences updated", level="SUCCESS")
        return True

    def run_cycle(self) -> Dict[str, Any]:
        self.log(step="Ticket Ingestion", file_used="customer_support/agent.py", message="Checking support queues and client threads...", level="INFO")

        # Load real tickets from TICKETS_FILE
        from core.storage import safe_load_json
        existing_tickets = safe_load_json(TICKETS_FILE, default=[])
        pending_tickets = [t for t in existing_tickets if t.get("status") == "PENDING" and not t.get("draft_preview")]

        if not pending_tickets:
            self.log(step="Queue Clear", file_used=TICKETS_FILE, message="Support queue audit: 0 pending tickets. All queues clear.", level="INFO")
            return {
                "status": "Support Cycle Completed",
                "tickets_pending": 0,
                "message": "All customer queues clear, 0 pending tickets."
            }

        ticket_raw = pending_tickets[0]

        # Subagent 1: Classify sentiment and urgency
        classification = self.run_subagent(
            "support_sentiment_classifier",
            {
                "subject": ticket_raw["subject"],
                "body": ticket_raw["body"],
                "client_tier": ticket_raw.get("client_tier", "Standard")
            }
        )

        ticket_raw["priority"] = classification.get("priority", "P1")
        ticket_raw["sentiment"] = classification.get("sentiment", "Normal")
        self.stats["tickets_reviewed"] += 1

        # Subagent 2: VIP / P1 Mobile Escalation
        escalation_res = self.run_subagent(
            "support_vip_escalation",
            {
                "ticket": ticket_raw,
                "enabled": self.config.get("P1_MOBILE_ALERT", True)
            }
        )
        if escalation_res.get("escalated"):
            self.stats["p1_escalations"] += 1
            self.log(step="VIP Escalation", file_used="mobile_dispatcher", message=f"P1 ticket escalated to {escalation_res.get('target')}", level="WARN")

        # Subagent 3: Draft response and persist ticket
        draft_res = self.run_subagent(
            "support_reply_drafter",
            {
                "ticket": ticket_raw,
                "brand_tone": self.config.get("BRAND_TONE", "Empathetic, clear, and reassuring"),
                "tickets_file": TICKETS_FILE
            }
        )
        if draft_res.get("success"):
            self.stats["drafts_ready"] += 1

        self.log(step="Triage Complete", file_used=TICKETS_FILE, message=f"Processed ticket: {ticket_raw['subject']} (Priority: {ticket_raw['priority']})", level="SUCCESS")

        return {
            "status": "Support Cycle Completed",
            "ticket_processed": ticket_raw,
            "classification": classification,
            "escalation": escalation_res
        }

    def get_stats(self) -> List[Dict[str, Any]]:
        return [
            {"title": "Tickets Triaged", "value": self.stats["tickets_reviewed"], "color": "blue"},
            {"title": "P1 Urgent Alerts", "value": self.stats["p1_escalations"], "color": "red"},
            {"title": "Drafts Generated", "value": self.stats["drafts_ready"], "color": "green"}
        ]
