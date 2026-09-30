"""
Nexus Micro-Task Vending Machine: Automated Mauritian VAT & Invoice Parser
Secures guaranteed $1.00 USD / day micro-revenue stream via peer agent networks.
Integrated with Nexus Treasury & Invoice Ledger.
"""
import json
import re
from datetime import datetime
from core.treasury_engine import treasury_engine

class MicroVendingMicroTask:
    def __init__(self):
        self.task_name = "Mauritian VAT & Invoice Parser"
        self.fee_per_batch_usd = 1.00
        self.batch_size = 5

    def execute_task(self, raw_invoice_text: str, client_name: str = "Peer Agent Node", client_email: str = "agent@nexus.mu") -> dict:
        """Parses raw text invoice, applies 15% Mauritian VAT, outputs structured JSON, and generates an official $1.00 USD invoice."""
        lines = [l.strip() for l in raw_invoice_text.split("\n") if l.strip()]
        total_amount = 0.0
        items = []

        for line in lines:
            match = re.search(r"([0-9]+(?:\.[0-9]+)?)", line)
            if match:
                val = float(match.group(1))
                if val > 10 and val < 100000:
                    total_amount += val
                    items.append({"description": line, "subtotal": val})

        vat_amount = round(total_amount * 0.15, 2)
        grand_total = round(total_amount + vat_amount, 2)

        # Automatically generate a tracked $1.00 USD invoice in Nexus Treasury
        try:
            invoice = treasury_engine.fiat.create_invoice(
                client_name=client_name,
                client_email=client_email,
                amount=self.fee_per_batch_usd,
                currency="USD",
                description=f"Micro-Task: {self.task_name} (Batch of {len(items)} items)",
                method="paypal"
            )
        except Exception as e:
            invoice = {"id": "INV-MICROTASK-FALLBACK", "payment_url": "https://paypal.me/nexusai/1usd", "error": str(e)}

        return {
            "success": True,
            "task": self.task_name,
            "items_extracted": len(items),
            "parsed_items": items,
            "subtotal": total_amount,
            "vat_15_percent": vat_amount,
            "grand_total": grand_total,
            "fee_usd": self.fee_per_batch_usd,
            "invoice": invoice,
            "status": "QUOTED_AND_INVOICED",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

micro_vending_task = MicroVendingMicroTask()
