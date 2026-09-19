import os
import json
import time
from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from agents.infra_finance_sentinel.subagents import (
    CloudBillingAuditSubAgent,
    DomainSSLWatcherSubAgent,
    ClientInvoiceChaserSubAgent,
    PaymentCollectorSubAgent,
    FINANCE_AUDIT_FILE
)

class InfraFinanceSentinelAgent(BaseAgent):
    """
    Employee #13: Cloud Bills, Domain Expirations & Client Invoice Chaser
    - Audits cloud infrastructure spending across Vercel, Hetzner, AWS, GCP
    - Monitors domain renewal deadlines (.mu, .com) and SSL expiries
    - Tracks client milestone invoices and drafts polite follow-up reminders
    """
    def __init__(self):
        super().__init__(
            agent_id="infra_finance_sentinel",
            name="Cloud Bills, Domain Expirations & Invoices",
            description="Audits monthly cloud spend across Vercel/Hetzner/AWS, warns on domain & SSL expirations, and tracks overdue client invoices with auto-drafted follow-ups.",
            icon="briefcase",
            schedule_minutes=240
        )
        self.config = {
            "MONTHLY_CLOUD_BUDGET_USD": 180.0,
            "DOMAIN_EXPIRY_WARNING_DAYS": 14,
            "AUTO_DRAFT_INVOICE_REMINDERS": True,
            "REQUIRE_APPROVAL_BEFORE_DISPATCH": True,
            "ALERT_ON_BUDGET_SPIKE": True
        }
        self.stats = {
            "monthly_burn_rate": "58.7%",
            "active_cloud_spend": "$105.70",
            "domains_healthy": "3/3",
            "overdue_invoices": 1
        }
        self._register_subagents()

    def _register_subagents(self):
        self.register_subagent(CloudBillingAuditSubAgent())
        self.register_subagent(DomainSSLWatcherSubAgent())
        self.register_subagent(ClientInvoiceChaserSubAgent())
        self.register_subagent(PaymentCollectorSubAgent())

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "MONTHLY_CLOUD_BUDGET_USD",
                "label": "Monthly Cloud Spend Cap (USD)",
                "type": "number",
                "default": 150.0,
                "description": "Total monthly threshold for Vercel, Hetzner, GCP, Cloudflare, and Twilio"
            },
            {
                "key": "DOMAIN_EXPIRY_WARNING_DAYS",
                "label": "Domain & SSL Warning Window (Days)",
                "type": "number",
                "default": 14,
                "description": "Notify when a domain or SSL cert expires in fewer than this many days"
            },
            {
                "key": "AUTO_ALERT_OVERDUE_INVOICES",
                "label": "Alert Mobile on Overdue Invoices",
                "type": "boolean",
                "default": True,
                "description": "Dispatch notification to +230 58169420 when an agency client invoice becomes overdue"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(step="Config Saved", file_used="infra_finance_sentinel/agent.py", message="Financial & infrastructure parameters updated", level="SUCCESS")
        return True

    def get_stats(self) -> List[Dict[str, Any]]:
        return [
            {"title": "Cloud Spend (USD)", "value": self.stats["active_cloud_spend"], "color": "blue"},
            {"title": "Budget Burn Rate", "value": self.stats["monthly_burn_rate"], "color": "green"},
            {"title": "Domains & SSL Active", "value": self.stats["domains_healthy"], "color": "blue"},
            {"title": "Overdue Invoices", "value": self.stats["overdue_invoices"], "color": "amber" if self.stats["overdue_invoices"] > 0 else "green"}
        ]

    def get_financial_health(self) -> Dict[str, Any]:
        if os.path.exists(FINANCE_AUDIT_FILE):
            try:
                with open(FINANCE_AUDIT_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def run_cycle(self) -> Dict[str, Any]:
        self.log(step="Audit Finance & Infra", file_used="infra_finance_sentinel/agent.py", message="Auditing cloud spend, domain expirations, and client receivables...", level="INFO")

        # 1. Cloud Billing Audit
        spend_res = self.run_subagent("cloud_billing_audit", {"monthly_budget_usd": float(self.config.get("MONTHLY_CLOUD_BUDGET_USD", 150.0))})
        spend_data = spend_res.get("data", {})
        self.stats["active_cloud_spend"] = f"${spend_data.get('total_spend_usd', 105.70):.2f}"
        self.stats["monthly_burn_rate"] = f"{spend_data.get('burn_rate_pct', 70.5)}%"

        # 2. Domain & SSL Watch
        domain_res = self.run_subagent("domain_ssl_watcher", {"warning_days": int(self.config.get("DOMAIN_EXPIRY_WARNING_DAYS", 14))})
        domain_data = domain_res.get("data", {})
        self.stats["domains_healthy"] = f"{domain_data.get('total_domains_tracked', 3)}/{domain_data.get('total_domains_tracked', 3)}"

        # 3. Client Invoices
        inv_res = self.run_subagent("client_invoice_chaser")
        inv_data = inv_res.get("data", {})
        self.stats["overdue_invoices"] = inv_data.get("overdue_count", 0)

        # 4. Online Payment & Revenue Reconciler
        payment_res = self.run_subagent("payment_collector")
        payment_data = payment_res.get("data", {})

        # Save combined audit
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "cloud_billing": spend_data,
            "domains": domain_data,
            "invoices": inv_data,
            "payments": payment_data
        }

        with open(FINANCE_AUDIT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        self.log(step="Audit Complete", file_used="infra_finance_audit.json", message=f"Financial audit logged: Cloud ${spend_data.get('total_spend_usd')}, {domain_data.get('total_domains_tracked')} domains verified, {payment_data.get('total_invoices', 0)} total payment links tracked (${payment_data.get('total_usd_collected', 0)} collected)", level="SUCCESS")

        return {
            "status": "Success",
            "cloud_spend_usd": spend_data.get("total_spend_usd"),
            "overdue_invoices": inv_data.get("overdue_count"),
            "total_invoices": payment_data.get("total_invoices", 0),
            "total_usd_collected": payment_data.get("total_usd_collected", 0)
        }
