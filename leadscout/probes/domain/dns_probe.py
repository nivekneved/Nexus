"""
LeadScout-Core: DNS Probe
=========================
Inspects MX records, SPF records, and classifies email providers (Google Workspace, Office 365, etc.).
"""

from typing import Dict, Any
from leadscout.probes.base import BaseProbe
from leadscout.core.card import LeadCard
from leadscout.core.network import NetworkClient

class InspectDNSAndMXTask(BaseProbe):
    name = "InspectDNSAndMXTask"

    async def execute(self, card: LeadCard) -> Dict[str, Any]:
        if not card.domain:
            return {}

        mx_records = await NetworkClient.resolve_dns_mx(card.domain)
        txt_records = await NetworkClient.resolve_dns_txt(card.domain)

        spf_record = next((t for t in txt_records if "v=spf1" in t), None)

        provider = "Unknown"
        mx_str = " ".join(mx_records).lower()
        if "google" in mx_str or "googlemail" in mx_str:
            provider = "Google Workspace"
        elif "outlook" in mx_str or "protection.outlook" in mx_str:
            provider = "Microsoft Office 365"
        elif "zoho" in mx_str:
            provider = "Zoho Mail"

        return {
            "mx_records": mx_records,
            "spf_record": spf_record,
            "email_provider": provider
        }
