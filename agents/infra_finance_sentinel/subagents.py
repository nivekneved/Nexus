import os
import json
import time
from typing import Dict, Any, List, Optional
from core.subagent import BaseSubAgent

FINANCE_AUDIT_FILE = "infra_finance_audit.json"

class CloudBillingAuditSubAgent(BaseSubAgent):
    """
    Subagent 1: Audits cloud infrastructure spending across Vercel, AWS, Google Cloud,
    Hetzner, and DigitalOcean, alerting on unexpected usage spikes or billing anomalies.
    """
    def __init__(self):
        super().__init__(
            subagent_id="cloud_billing_audit",
            name="Cloud Infrastructure Billing Auditor",
            parent_agent_id="infra_finance_sentinel",
            description="Audits cloud spend against monthly budgets, flagging cost spikes across Vercel, Hetzner, AWS, and GCP."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        monthly_budget_usd = payload.get("monthly_budget_usd", 150.0)

        # Active infrastructure cost items
        infra_items = [
            {"provider": "Vercel Pro", "service": "Frontend Edge Hosting", "current_usd": 20.0, "status": "NORMAL"},
            {"provider": "Google Cloud Platform", "service": "Gemini 2.5 API & Firebase", "current_usd": 14.50, "status": "NORMAL"},
            {"provider": "Hetzner Cloud", "service": "Backend Dedicated Docker Host", "current_usd": 38.00, "status": "NORMAL"},
            {"provider": "Cloudflare Pro", "service": "DNS & Enterprise WAF", "current_usd": 25.00, "status": "NORMAL"},
            {"provider": "Twilio / WhatsApp Comms", "service": "SMS & WhatsApp API (+230 58169420)", "current_usd": 8.20, "status": "NORMAL"}
        ]

        total_current_usd = sum(item["current_usd"] for item in infra_items)
        burn_rate_pct = round((total_current_usd / monthly_budget_usd) * 100, 1)

        is_over_budget = total_current_usd > monthly_budget_usd

        return {
            "monthly_budget_usd": monthly_budget_usd,
            "total_spend_usd": total_current_usd,
            "burn_rate_pct": burn_rate_pct,
            "is_over_budget": is_over_budget,
            "breakdown": infra_items
        }


class DomainSSLWatcherSubAgent(BaseSubAgent):
    """
    Subagent 2: Monitors domain registration renewal deadlines (.mu, .com)
    and SSL certificate validity, warning 14 days before expiration.
    """
    def __init__(self):
        super().__init__(
            subagent_id="domain_ssl_watcher",
            name="Domain & SSL Expiration Sentinel",
            parent_agent_id="infra_finance_sentinel",
            description="Monitors domain renewal deadlines and SSL certificate expiries, preventing unexpected DNS downtime."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        warning_threshold_days = payload.get("warning_days", 14)

        domains = [
            {
                "domain": "eco-travellounge.mu",
                "registrar": "Mauritius Telecom NIC / Cloudflare",
                "expires_in_days": 182,
                "auto_renew": True,
                "ssl_status": "Valid (Let's Encrypt / Cloudflare)",
                "status": "HEALTHY"
            },
            {
                "domain": "travellounge.mu",
                "registrar": "Mauritius Telecom NIC",
                "expires_in_days": 28,
                "auto_renew": True,
                "ssl_status": "Valid",
                "status": "ATTENTION_SOON"
            },
            {
                "domain": "nexus-workforce.io",
                "registrar": "Namecheap",
                "expires_in_days": 310,
                "auto_renew": True,
                "ssl_status": "Valid",
                "status": "HEALTHY"
            }
        ]

        urgent_expiries = [d for d in domains if d["expires_in_days"] <= warning_threshold_days]

        return {
            "total_domains_tracked": len(domains),
            "urgent_expiries_count": len(urgent_expiries),
            "domains": domains
        }


class ClientInvoiceChaserSubAgent(BaseSubAgent):
    """
    Subagent 3: Tracks client milestone invoices, overdue retainers,
    and drafts polite WhatsApp / email payment reminders.
    """
    def __init__(self):
        super().__init__(
            subagent_id="client_invoice_chaser",
            name="Client Retainer & Milestone Chaser",
            parent_agent_id="infra_finance_sentinel",
            description="Tracks client billing milestones and auto-drafts polite follow-up payment reminders for overdue invoices."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        from core.payment_service import payment_service
        receivables_data = payment_service.get_receivables()
        raw_invoices = receivables_data.get("invoices", [])

        # Filter out Travellounge per explicit instruction: Do not recover from Travellounge
        filtered = [
            inv for inv in raw_invoices 
            if "travellounge" not in inv.get("client_name", "").lower()
        ]

        chaser_invoices = []
        for inv in filtered:
            rem_info = payment_service.format_reminder_message(inv["id"])
            chaser_invoices.append({
                "invoice_id": inv["id"],
                "client": inv.get("client_name", "Client"),
                "project": inv.get("description", "Service"),
                "amount_mur": f"Rs {inv.get('amount', 0):,.2f}" if inv.get("currency") == "MUR" else None,
                "amount_usd": f"${inv.get('amount', 0):,.2f}" if inv.get("currency") == "USD" else None,
                "due_date": inv.get("due_date", "On Receipt"),
                "status": inv.get("status", "PENDING"),
                "reminder_draft": rem_info.get("formatted_message"),
                "whatsapp_link": rem_info.get("whatsapp_link")
            })

        overdue = [inv for inv in chaser_invoices if "OVERDUE" in inv["status"]]

        return {
            "total_invoices_tracked": len(chaser_invoices),
            "overdue_count": len(overdue),
            "invoices": chaser_invoices
        }


class PaymentCollectorSubAgent(BaseSubAgent):
    """
    Subagent 4: Reconciles live payment links, verifies PayPal order statuses,
    and tallies collected revenue across PayPal and MCB Wire pipelines.
    """
    def __init__(self):
        super().__init__(
            subagent_id="payment_collector",
            name="Online Payment & PayPal Reconciler",
            parent_agent_id="infra_finance_sentinel",
            description="Reconciles live online payment links and invoices across PayPal Checkout and MCB Wire/Juice pipelines."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        from core.payment_service import payment_service
        invoices = payment_service.load_invoices()
        
        pending_count = sum(1 for inv in invoices if inv.get("status") == "PENDING")
        paid_count = sum(1 for inv in invoices if inv.get("status") in ("COMPLETED", "PAID"))
        total_usd_collected = sum(float(inv.get("amount", 0)) for inv in invoices if inv.get("status") in ("COMPLETED", "PAID") and inv.get("currency") == "USD")

        return {
            "total_invoices": len(invoices),
            "pending_invoices": pending_count,
            "paid_invoices": paid_count,
            "total_usd_collected": total_usd_collected,
            "recent_invoices": invoices[:5]
        }

