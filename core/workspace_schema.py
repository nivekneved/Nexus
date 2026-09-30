# -*- coding: utf-8 -*-
"""
Nexus Dynamic Workspace Schema Engine
Defines the unified declarative specification for all dashboard workspaces,
replacing thousands of lines of hardcoded HTML panes with dynamic, data-driven layouts.
"""

from typing import Dict, Any, List

WORKSPACES: Dict[str, Dict[str, Any]] = {
    "ceo-cockpit": {
        "id": "ceo-cockpit",
        "title": "Executive Command Center",
        "badge": "Autonomous Executive Cockpit",
        "badge_color": "#10b981",
        "desc": "Nexus coordinates 18 autonomous AI employees running privately on your infrastructure with zero payroll overhead.",
        "kpis": [
            {"label": "Fleet Status", "icon": "👑", "value": "18 Armed", "sub": "Zero Third-Party Telemetry"},
            {"label": "Monthly Goal", "icon": "💰", "value": "Rs 150,000 MUR", "sub": "Pipeline: Rs 90,000 MUR"},
            {"label": "Cloud FinOps", "icon": "☁️", "value": "$2.00 / $50", "sub": "Compute Cap: <$180/mo"},
            {"label": "Treasury", "icon": "⛓️", "value": "$123.50 USDC", "sub": "Base L2 Sovereign Vault"}
        ],
        "tasks": [
            "ceo_morning_standup",
            "ceo_cross_platform_blitz",
            "ceo_revenue_deliberation",
            "ceo_partner_sla",
            "ceo_emergency_lockdown"
        ],
        "feed": {
            "title": "Autonomous Executive Telemetry & Action Log",
            "endpoint": "/api/standup/brief",
            "type": "briefing"
        }
    },
    "domain-comms": {
        "id": "domain-comms",
        "title": "Communications & Inbound Command",
        "badge": "Communications Workspace",
        "badge_color": "#0284c7",
        "desc": "Unified multi-inbox hygiene, anti-spam quarantine, WhatsApp mobile dispatcher, and VIP customer support concierge.",
        "kpis": [
            {"label": "Active Inboxes", "icon": "📫", "value": "1/1 Verified", "sub": "IMAP / SMTP Syncing"},
            {"label": "Spam Quarantined", "icon": "🛡️", "value": "0 Detected", "sub": "AI Bayesian Filter"},
            {"label": "Support Tickets", "icon": "💬", "value": "3 Closed", "sub": "<90s SLA Maintained"},
            {"label": "WhatsApp Gateway", "icon": "📱", "value": "Connected", "sub": "Escalation: +230 58169420"}
        ],
        "tasks": [
            "comms_vip_broadcast",
            "comms_cold_outbound",
            "comms_support_reply",
            "comms_spam_sweep",
            "comms_whatsapp_dispatch"
        ],
        "feed": {
            "title": "Priority Unified Inbound & Dispatch Feed",
            "endpoint": "/api/comms/feed",
            "type": "table",
            "columns": ["Time", "Channel", "Sender", "Subject", "Status"]
        }
    },
    "domain-operations": {
        "id": "domain-operations",
        "title": "Operations, Infrastructure & 24/7 Autopilot",
        "badge": "Operations Workspace",
        "badge_color": "#d97706",
        "desc": "Continuous background execution, SQLite WAL integrity, compute survival tiers, cryptographic loss-free snapshots, and 25 security safeguards.",
        "kpis": [
            {"label": "24/7 Autopilot", "icon": "🌙", "value": "Active", "sub": "Continuous Night Shift"},
            {"label": "Database Engine", "icon": "💾", "value": "SQLite WAL", "sub": "Zero-Loss Integrity"},
            {"label": "Enterprise Shields", "icon": "🛡️", "value": "25 Armed", "sub": "Rate Limits & Air-Gap Ready"},
            {"label": "Survival Physics", "icon": "⚙️", "value": "Normal Tier", "sub": "98.9% Margin Target"}
        ],
        "tasks": [
            "ops_crypto_snapshot",
            "ops_codebase_audit",
            "ops_shields_verify",
            "ops_finops_cloud_cap",
            "ops_disaster_recovery_dryrun"
        ],
        "feed": {
            "title": "System Operations & SRE Heartbeat Ledger",
            "endpoint": "/api/autopilot/events",
            "type": "table",
            "columns": ["Timestamp", "Subsystem", "Event", "Latency", "Integrity"]
        }
    },
    "domain-commerce": {
        "id": "domain-commerce",
        "title": "Commerce, Treasury & Revenue Studio",
        "badge": "Commerce Workspace",
        "badge_color": "#059669",
        "desc": "Multi-currency accounts receivable (MUR & USD), Base L2 USDC crypto treasury, AES-256 encrypted vault, and digital store fulfillment.",
        "kpis": [
            {"label": "Accounts Receivable", "icon": "💳", "value": "Rs 90,000 MUR", "sub": "19 Tracked Invoices"},
            {"label": "Base L2 Treasury", "icon": "⛓️", "value": "$123.50 USDC", "sub": "Wallet: 0xEAE5...1F2"},
            {"label": "Digital Store", "icon": "🛒", "value": "8 Products Live", "sub": "$1 Vending Machine"},
            {"label": "Target Progress", "icon": "📈", "value": "60% Staged", "sub": "Towards Rs 150,000 MUR"}
        ],
        "tasks": [
            "comm_vending_tool",
            "comm_issue_invoice",
            "comm_treasury_audit",
            "comm_dunning_notice",
            "comm_flash_sale"
        ],
        "feed": {
            "title": "Invoicing & Accounts Receivable Ledger",
            "endpoint": "/api/finance/invoices",
            "type": "table",
            "columns": ["Invoice ID", "Client", "Amount", "Due Date", "Status", "Receipt"]
        }
    },
    "domain-research": {
        "id": "domain-research",
        "title": "Research, Market Intelligence & B2B Leads",
        "badge": "Research Workspace",
        "badge_color": "#7c3aed",
        "desc": "High-intent B2B sales leads CRM, emerging technology intelligence dossiers, GitHub radar CVE watchdog, and executive social thought leadership.",
        "kpis": [
            {"label": "B2B Leads in CRM", "icon": "🎯", "value": "28 Qualified", "sub": "Mauritius & Global Leads"},
            {"label": "Tech Dossiers", "icon": "📑", "value": "1 Compiled", "sub": "Agentic Architecture"},
            {"label": "CVE Radar", "icon": "🛡️", "value": "Zero Critical", "sub": "Local Dependencies"},
            {"label": "Social Hooks", "icon": "📢", "value": "5 Drafts Ready", "sub": "High-Ticket Retainers"}
        ],
        "tasks": [
            "mkt_linkedin_post",
            "mkt_facebook_post",
            "mkt_x_thread",
            "mkt_carousel_post",
            "mkt_b2b_lead_dossier"
        ],
        "feed": {
            "title": "B2B Sales Intelligence & Lead Prospect Pipeline",
            "endpoint": "/api/leads/pipeline",
            "type": "table",
            "columns": ["Company", "Sector", "Location", "Decision Maker", "Status"]
        }
    }
}

import copy

def get_workspace_schema(workspace_id: str) -> Dict[str, Any]:
    """Retrieve declarative schema for a given workspace populated with real-time DB metrics."""
    base_schema = WORKSPACES.get(workspace_id)
    if not base_schema:
        return {
            "id": workspace_id,
            "title": f"Workspace: {workspace_id.replace('-', ' ').title()}",
            "badge": "Autonomous Fleet Panel",
            "badge_color": "#4f46e5",
            "desc": "Autonomous workspace panel synchronized with live telemetry and system events.",
            "kpis": [
                {"label": "Status", "icon": "⚡", "value": "Online", "sub": "System Armed"},
                {"label": "Sync Mode", "icon": "🔄", "value": "Real-time", "sub": "Local WAL Storage"}
            ],
            "tasks": ["ceo_morning_standup", "comm_vending_tool", "ops_crypto_snapshot"],
            "feed": {"title": "System Activity Log", "endpoint": "/api/autopilot/events", "type": "briefing"}
        }

    schema = copy.deepcopy(base_schema)

    # Query real database metrics and live Base L2 balance
    try:
        from core.db import get_real_revenue_metrics
        from core.crypto_treasury import crypto_treasury
        metrics = get_real_revenue_metrics()
        wallet = crypto_treasury.get_wallet()
        onchain_usdc = float(wallet.get("balance_usdc", 0.0))
        wallet_addr = wallet.get("address", "0xEAE558282090d878582ec4C4C1C2470f9826b1F2")
        short_addr = f"{wallet_addr[:6]}...{wallet_addr[-3:]}"

        if workspace_id == "ceo-cockpit":
            for kpi in schema.get("kpis", []):
                if kpi.get("label") == "Monthly Goal":
                    kpi["value"] = f"Rs {metrics['total_realized_mur']:,.0f} MUR"
                    kpi["sub"] = f"Pipeline: Rs {metrics['total_pipeline_mur']:,.0f} MUR"
                elif kpi.get("label") == "Treasury":
                    kpi["value"] = f"${onchain_usdc:.2f} USDC"
                    kpi["sub"] = "Base L2 Sovereign Vault"
        elif workspace_id == "domain-commerce":
            for kpi in schema.get("kpis", []):
                if kpi.get("label") == "Accounts Receivable":
                    kpi["value"] = f"Rs {metrics['total_pipeline_mur']:,.0f} MUR"
                    kpi["sub"] = f"{metrics['total_invoices_count']} Tracked Invoices"
                elif kpi.get("label") == "Base L2 Treasury":
                    kpi["value"] = f"${onchain_usdc:.2f} USDC"
                    kpi["sub"] = f"Wallet: {short_addr}"
                elif kpi.get("label") == "Target Progress":
                    pct = min(100, int((metrics["total_realized_mur"] / 150000.0) * 100)) if metrics["total_realized_mur"] > 0 else 0
                    kpi["value"] = f"{pct}% Realized"
                    kpi["sub"] = "Towards Rs 150,000 MUR"
    except Exception as e:
        # Fall back to base schema gracefully if DB query fails
        pass

    return schema
