import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.subagent import BaseSubAgent
from core.agent_manager import AgentManager

class TicketSentimentClassifierSubAgent(BaseSubAgent):
    """
    Subagent 1: Audits incoming support ticket content for customer sentiment, SLA urgency, and priority level.
    """
    def __init__(self):
        super().__init__(
            subagent_id="support_sentiment_classifier",
            name="Ticket Sentiment Classifier SubAgent",
            parent_agent_id="customer_support",
            description="Evaluates inbound support tickets for customer sentiment, urgency keywords, and SLA tiering."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        subject = payload.get("subject", "")
        body = payload.get("body", "")
        client_tier = payload.get("client_tier", "Standard")

        text = f"{subject} {body}".lower()
        urgency_terms = ["urgent", "broken", "critical", "outage", "webhook", "down", "emergency", "fail"]
        frustrated_terms = ["frustrated", "disappointed", "unacceptable", "terrible", "cancel", "refund"]

        is_urgent = any(term in text for term in urgency_terms)
        is_frustrated = any(term in text for term in frustrated_terms)

        if client_tier.lower() == "enterprise" and is_urgent:
            priority = "P1"
            sentiment = "Urgent / Attentive"
        elif is_frustrated:
            priority = "P2"
            sentiment = "Frustrated / At Risk"
        elif is_urgent:
            priority = "P2"
            sentiment = "Urgent"
        else:
            priority = "P3"
            sentiment = "Neutral / Inquisitive"

        return {
            "priority": priority,
            "sentiment": sentiment,
            "is_critical": priority in ["P0", "P1"],
            "sla_hours": 1 if priority == "P1" else (4 if priority == "P2" else 24)
        }


class VIPEscalationSubAgent(BaseSubAgent):
    """
    Subagent 2: Handles immediate mobile escalation to Deven's WhatsApp for P0/P1 enterprise issues.
    """
    def __init__(self):
        super().__init__(
            subagent_id="support_vip_escalation",
            name="VIP Escalation Sentinel SubAgent",
            parent_agent_id="customer_support",
            description="Routes P0/P1 tickets and enterprise VIP inquiries directly to mobile notification channels."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        ticket = payload.get("ticket", {})
        enabled = payload.get("enabled", True)

        is_p1 = ticket.get("priority") in ["P0", "P1"]
        escalated = False

        if enabled and is_p1:
            client = ticket.get("client", "Client")
            subject = ticket.get("subject", "Urgent Inquiry")
            manager = AgentManager()
            dispatcher = manager.get_agent("mobile_dispatcher")
            if dispatcher and hasattr(dispatcher, "send_notification"):
                dispatcher.send_notification(
                    title=f"🚨 P1 Client Alert: {client}",
                    message=f"Enterprise client '{client}' flagged urgent: '{subject}'. Response draft ready on dashboard.",
                    urgency="P1"
                )
                escalated = True

        return {
            "escalated": escalated,
            "ticket_id": ticket.get("id", "unknown"),
            "target": "mobile_dispatcher (WhatsApp +230 58169420)" if escalated else "None"
        }


class SupportReplyDrafterSubAgent(BaseSubAgent):
    """
    Subagent 3: Pre-generates context-aware, empathetic support replies and commits to persistent ledger.
    """
    def __init__(self):
        super().__init__(
            subagent_id="support_reply_drafter",
            name="Support Reply Drafter SubAgent",
            parent_agent_id="customer_support",
            description="Drafts empathetic, context-rich replies matching brand voice and updates the ticket ledger."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        ticket = payload.get("ticket", {})
        brand_tone = payload.get("brand_tone", "Empathetic, clear, and reassuring")
        tickets_file = payload.get("tickets_file", "support_tickets.json")

        client = ticket.get("client", "Valued Client")
        subject = ticket.get("subject", "your inquiry")

        draft = (
            f"Hello {client},\n\n"
            f"Thank you for contacting us regarding '{subject}'. "
            f"Our engineering and support sentinels have received your request with high priority. "
            f"We are actively investigating the telemetry logs and will provide a full resolution update shortly.\n\n"
            f"Warm regards,\nNexus Support Operations (Brand Tone: {brand_tone})"
        )
        ticket["draft_preview"] = draft

        # Persist to disk
        all_tickets = []
        if os.path.exists(tickets_file):
            try:
                with open(tickets_file, "r", encoding="utf-8") as f:
                    all_tickets = json.load(f)
            except Exception:
                all_tickets = []

        all_tickets.insert(0, ticket)
        all_tickets = all_tickets[:100]

        try:
            with open(tickets_file, "w", encoding="utf-8") as f:
                json.dump(all_tickets, f, indent=2, ensure_ascii=False)
        except Exception as e:
            return {"success": False, "error": str(e), "draft": draft}

        return {
            "success": True,
            "ticket_id": ticket.get("id"),
            "draft": draft,
            "total_tickets": len(all_tickets)
        }
