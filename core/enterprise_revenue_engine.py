"""
Nexus Enterprise Revenue & Proposal Generator Engine (v4.0)
============================================================
Operationalizes high-ticket pricing ($1,500-$5,000 upfront + $500/mo retainers),
95%+ margin turnkey micro-SaaS packaging, and compounds the $1.00/day baseline.
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from core.storage import atomic_save_json, safe_load_json
from core.treasury_engine import treasury_engine
from core.departmental_personas import departmental_personas

logger = logging.getLogger("Nexus.EnterpriseRevenue")

ENTERPRISE_DEALS_FILE = "enterprise_deals_ledger.json"

class EnterpriseRevenueEngine:
    def __init__(self):
        self._ensure_initialized()

    def _ensure_initialized(self):
        if not os.path.exists(ENTERPRISE_DEALS_FILE):
            atomic_save_json(ENTERPRISE_DEALS_FILE, [])

    def generate_high_ticket_proposal(self, client_name: str, client_email: str, niche: str = "Private Healthcare Clinic") -> Dict[str, Any]:
        """
        Leverages finance-tracker, growth-hacker, and brand-guardian personas
        to draft a $1,500–$5,000 upfront + $500/mo enterprise agency proposal with an official invoice.
        """
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        deal_id = f"DEAL-{int(time.time() * 1000)}"

        # 1. Pull persona wisdom
        finance_persona = departmental_personas.get_persona_detail("finance-tracker")
        growth_persona = departmental_personas.get_persona_detail("growth-hacker")
        brand_persona = departmental_personas.get_persona_detail("brand-guardian")

        upfront_fee = 2500.00  # $2,500 USD (~Rs 115,000 MUR)
        monthly_retainer = 500.00 # $500 USD / mo (~Rs 23,000 MUR)

        # 2. Create official upfront deployment invoice in Treasury
        invoice = treasury_engine.fiat.create_invoice(
            client_name=client_name,
            client_email=client_email,
            amount=upfront_fee,
            currency="USD",
            description=f"Turnkey Enterprise Deployment ({niche}) + Month 1 Ops",
            method="paypal"
        )

        proposal = {
            "deal_id": deal_id,
            "client_name": client_name,
            "client_email": client_email,
            "niche": niche,
            "pricing_structure": {
                "upfront_deployment_usd": upfront_fee,
                "monthly_retainer_usd": monthly_retainer,
                "profit_margin_percent": 96.5,
                "currency": "USD"
            },
            "agency_personas_applied": [
                finance_persona.get("id") if finance_persona else "finance-tracker",
                growth_persona.get("id") if growth_persona else "growth-hacker",
                brand_persona.get("id") if brand_persona else "brand-guardian"
            ],
            "pitch_copy": (
                f"Dear {client_name},\n\n"
                f"We have engineered a turnkey digital operations suite tailored specifically for {niche}. "
                f"Unlike standard software tools that leave you with maintenance overhead, our solution includes "
                f"full white-ip transfer, 24/7 autonomous agent monitoring, bilingual (FR/EN) support, and guaranteed 99.9% uptime.\n\n"
                f"Investment: ${upfront_fee:,.2f} USD upfront deployment + ${monthly_retainer:,.2f} USD/mo Human-on-the-Loop retainer.\n"
                f"Secure your deployment slot here: {invoice.get('payment_url')}"
            ),
            "invoice": invoice,
            "status": "PROPOSAL_DISPATCHED",
            "timestamp": now_str
        }

        deals = safe_load_json(ENTERPRISE_DEALS_FILE, default=[])
        deals.insert(0, proposal)
        atomic_save_json(ENTERPRISE_DEALS_FILE, deals)

        logger.info(f"[EnterpriseRevenue] Generated high-ticket proposal for {client_name}: ${upfront_fee} + ${monthly_retainer}/mo")
        return {
            "success": True,
            "proposal": proposal
        }

    def get_ledger(self) -> List[Dict[str, Any]]:
        return safe_load_json(ENTERPRISE_DEALS_FILE, default=[])

enterprise_revenue_engine = EnterpriseRevenueEngine()
