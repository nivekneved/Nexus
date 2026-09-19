import os
import time
import json
import base64
import urllib.request
import urllib.parse
import urllib.error
import ssl
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from security.financial_shield import financial_shield

load_dotenv()

INVOICES_FILE = "invoices.json"

class PaymentService:
    """
    Commercial Payment Gateway & Invoice Service
    Integrates Live PayPal REST API and Mauritius Commercial Bank (MCB) Wire & Juice pipelines.
    Protected by FinancialSecurityShield with cryptographic HMAC-SHA256 signatures and replay defense.
    """
    def __init__(self):
        self._cached_token: Optional[str] = None
        self._token_expires_at: float = 0
        self._ssl_ctx = ssl.create_default_context()
        self._ensure_ledger_signatures()

    def _ensure_ledger_signatures(self):
        """Ensures any existing invoices without cryptographic signatures are signed."""
        invoices = self.load_invoices()
        if not invoices:
            return
        needs_save = False
        prev_hash = "GENESIS_BLOCK_NEXUS_2026"
        # chronological order (oldest to newest)
        for inv in reversed(invoices):
            if "security_signature" not in inv or "block_hash" not in inv:
                inv["prev_hash"] = prev_hash
                sig, bhash = financial_shield.sign_invoice(inv, prev_hash)
                inv["security_signature"] = sig
                inv["block_hash"] = bhash
                needs_save = True
            prev_hash = inv["block_hash"]
        if needs_save:
            self.save_invoices(invoices)

    def _get_paypal_creds(self) -> tuple[str, str]:
        load_dotenv(override=True)
        client_id = os.getenv("PAYPAL_CLIENT_ID", "").strip()
        secret = os.getenv("PAYPAL_SECRET", "").strip()
        return client_id, secret

    def get_paypal_token(self) -> str:
        """Fetches and caches live OAuth2 Bearer token from PayPal."""
        now = time.time()
        if self._cached_token and now < self._token_expires_at - 60:
            return self._cached_token

        client_id, secret = self._get_paypal_creds()
        if not client_id or not secret:
            raise ValueError("PayPal Client ID or Secret is not configured in .env")

        auth_header = base64.b64encode(f"{client_id}:{secret}".encode()).decode("utf-8")
        req = urllib.request.Request(
            "https://api-m.paypal.com/v1/oauth2/token",
            data=b"grant_type=client_credentials",
            headers={
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "NexusWorkforce-PaymentEngine/2.5"
            }
        )

        with urllib.request.urlopen(req, timeout=12, context=self._ssl_ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            self._cached_token = data.get("access_token")
            expires_in = data.get("expires_in", 3600)
            self._token_expires_at = now + expires_in
            return self._cached_token

    def create_paypal_order(
        self,
        amount: float,
        currency: str = "USD",
        description: str = "Nexus AI Workforce Service",
        client_name: str = "",
        client_email: str = ""
    ) -> Dict[str, Any]:
        """Creates a live PayPal order and generates a 1-click checkout URL."""
        token = self.get_paypal_token()
        formatted_amount = f"{float(amount):.2f}"
        ref_id = f"NEXUS-{int(time.time())}"

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "reference_id": ref_id,
                "description": description[:120],
                "amount": {
                    "currency_code": currency.upper(),
                    "value": formatted_amount
                }
            }],
            "application_context": {
                "brand_name": "Nexus Workforce",
                "landing_page": "BILLING",
                "user_action": "PAY_NOW",
                "shipping_preference": "NO_SHIPPING"
            }
        }

        req = urllib.request.Request(
            "https://api-m.paypal.com/v2/checkout/orders",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "NexusWorkforce-PaymentEngine/2.5"
            }
        )

        with urllib.request.urlopen(req, timeout=15, context=self._ssl_ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            order_id = data.get("id")
            links = {link["rel"]: link["href"] for link in data.get("links", [])}
            approve_url = links.get("approve", f"https://www.paypal.com/checkoutnow?token={order_id}")

            return {
                "order_id": order_id,
                "reference_id": ref_id,
                "status": data.get("status", "CREATED"),
                "approve_url": approve_url,
                "amount": formatted_amount,
                "currency": currency.upper(),
                "description": description,
                "client_name": client_name,
                "client_email": client_email
            }

    def check_paypal_order_status(self, order_id: str) -> Dict[str, Any]:
        """Checks status of an order on PayPal, capturing it if approved."""
        token = self.get_paypal_token()
        req = urllib.request.Request(
            f"https://api-m.paypal.com/v2/checkout/orders/{order_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "NexusWorkforce-PaymentEngine/2.5"
            }
        )

        with urllib.request.urlopen(req, timeout=12, context=self._ssl_ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            status = data.get("status")

            # If buyer approved but not yet captured, execute capture
            if status == "APPROVED":
                capture_res = self.capture_paypal_order(order_id)
                return capture_res

            return {
                "order_id": order_id,
                "status": status,
                "details": data
            }

    def capture_paypal_order(self, order_id: str) -> Dict[str, Any]:
        """Captures payment for an approved PayPal order."""
        token = self.get_paypal_token()
        req = urllib.request.Request(
            f"https://api-m.paypal.com/v2/checkout/orders/{order_id}/capture",
            data=b"{}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "NexusWorkforce-PaymentEngine/2.5"
            }
        )
        with urllib.request.urlopen(req, timeout=15, context=self._ssl_ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "order_id": order_id,
                "status": data.get("status", "COMPLETED"),
                "captured": True,
                "details": data
            }

    def get_mcb_wire_details(self, amount: float, currency: str, ref_id: str) -> Dict[str, Any]:
        """Generates bank transfer instructions for MCB wire or Juice."""
        load_dotenv(override=True)
        acc_name = os.getenv("MCB_ACCOUNT_NAME", "Deven Pawaray")
        acc_num = os.getenv("MCB_ACCOUNT_NUMBER", "000443260370")
        iban = os.getenv("MCB_IBAN", "MU57MCBL0944000443260370000MUR")
        swift = os.getenv("MCB_SWIFT", "MCBLMUMU")

        instructions = (
            f"--- BANK WIRE / JUICE PAYMENT INSTRUCTIONS ---\n"
            f"Beneficiary: {acc_name}\n"
            f"Bank: Mauritius Commercial Bank (MCB)\n"
            f"Account Number: {acc_num}\n"
            f"IBAN: {iban}\n"
            f"SWIFT / BIC: {swift}\n"
            f"Amount Due: {currency.upper()} {amount:,.2f}\n"
            f"Payment Reference: {ref_id}\n"
            f"Local Juice Pay: +230 58169420 / Ref: {ref_id}\n"
            f"----------------------------------------------"
        )

        return {
            "beneficiary_name": acc_name,
            "account_number": acc_num,
            "iban": iban,
            "swift": swift,
            "juice_mobile": "+230 58169420",
            "instructions_text": instructions
        }

    # Persistence & Invoices Ledger
    def load_invoices(self) -> List[Dict[str, Any]]:
        from core.storage import safe_load_json
        return safe_load_json(INVOICES_FILE, default=[])

    def save_invoices(self, invoices: List[Dict[str, Any]]) -> bool:
        from core.storage import atomic_save_json
        try:
            return atomic_save_json(INVOICES_FILE, invoices)
        except Exception:
            return False


    def create_invoice(
        self,
        client_name: str,
        client_email: str,
        amount: float,
        currency: str = "USD",
        description: str = "Nexus AI Workforce License",
        method: str = "paypal"  # 'paypal' or 'mcb_wire'
    ) -> Dict[str, Any]:
        """Creates a recorded invoice and generates the payment mechanism."""
        ref_id = f"INV-{datetime.now().strftime('%Y%m%d')}-{int(time.time()) % 10000:04d}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        invoice_record = {
            "id": ref_id,
            "client_name": client_name or "Valued Client",
            "client_email": client_email or "client@example.com",
            "amount": float(amount),
            "currency": currency.upper(),
            "description": description,
            "method": method,
            "created_at": created_at,
            "status": "PENDING",
            "payment_url": None,
            "bank_details": None,
            "paypal_order_id": None
        }

        if method == "paypal":
            paypal_data = self.create_paypal_order(
                amount=amount,
                currency=currency,
                description=description,
                client_name=client_name,
                client_email=client_email
            )
            invoice_record["paypal_order_id"] = paypal_data["order_id"]
            invoice_record["payment_url"] = paypal_data["approve_url"]
        else:
            wire_info = self.get_mcb_wire_details(amount, currency, ref_id)
            invoice_record["bank_details"] = wire_info

        # Load invoices to determine previous hash
        invoices = self.load_invoices()
        prev_hash = invoices[0].get("block_hash", "GENESIS_BLOCK_NEXUS_2026") if invoices else "GENESIS_BLOCK_NEXUS_2026"
        
        # Cryptographically sign invoice
        sig, bhash = financial_shield.sign_invoice(invoice_record, prev_hash)
        invoice_record["prev_hash"] = prev_hash
        invoice_record["security_signature"] = sig
        invoice_record["block_hash"] = bhash

        # Save to database
        invoices.insert(0, invoice_record)
        self.save_invoices(invoices)
        
        # Audit log
        financial_shield.log_financial_audit(
            event="INVOICE_CREATED",
            details={"id": ref_id, "amount": amount, "currency": currency, "method": method, "sig": sig}
        )

        return invoice_record

    def mark_invoice_status(self, invoice_id: str, status: str) -> bool:
        invoices = self.load_invoices()
        updated = False
        for inv in invoices:
            if inv["id"] == invoice_id or inv.get("paypal_order_id") == invoice_id:
                inv["status"] = status.upper()
                inv["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Re-sign with new status
                prev_h = inv.get("prev_hash", "GENESIS_BLOCK_NEXUS_2026")
                sig, bhash = financial_shield.sign_invoice(inv, prev_h)
                inv["security_signature"] = sig
                inv["block_hash"] = bhash
                updated = True
                financial_shield.log_financial_audit(
                    event="INVOICE_STATUS_UPDATED",
                    details={"id": inv["id"], "new_status": inv["status"], "sig": sig}
                )
                break
        if updated:
            self.save_invoices(invoices)
        return updated

    def reconcile_juice_payment(
        self,
        invoice_id: str,
        juice_ref: str,
        payer_phone: str = "",
        amount_paid: Optional[float] = None
    ) -> Dict[str, Any]:
        """Reconciles an MCB Juice payment transfer with anti-replay defense."""
        invoices = self.load_invoices()
        target = next((inv for inv in invoices if inv["id"] == invoice_id), None)
        if not target:
            return {"success": False, "error": f"Invoice {invoice_id} not found"}

        verification = financial_shield.verify_and_reconcile_juice_payment(
            invoice=target,
            juice_ref=juice_ref,
            payer_phone=payer_phone,
            amount_paid=amount_paid
        )
        if not verification.get("success"):
            return verification

        target["status"] = "PAID"
        target["reconciliation_token"] = verification["reconciliation_token"]
        target["juice_ref"] = verification["juice_ref"]
        target["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Re-sign with updated status
        prev_h = target.get("prev_hash", "GENESIS_BLOCK_NEXUS_2026")
        sig, bhash = financial_shield.sign_invoice(target, prev_h)
        target["security_signature"] = sig
        target["block_hash"] = bhash

        self.save_invoices(invoices)
        return verification

    def verify_ledger(self) -> Dict[str, Any]:
        """Verifies the cryptographic integrity of all invoices."""
        invoices = self.load_invoices()
        return financial_shield.verify_ledger_integrity(invoices)

    def get_receivables(self) -> Dict[str, Any]:
        """Returns categorized receivables including client milestones and online links."""
        invoices = self.load_invoices()

        # Explicitly exclude Travellounge if ever present
        invoices = [inv for inv in invoices if "travellounge" not in inv.get("client_name", "").lower()]

        overdue_mur = sum(inv["amount"] for inv in invoices if inv["currency"] == "MUR" and "OVERDUE" in inv["status"])
        pending_mur = sum(inv["amount"] for inv in invoices if inv["currency"] == "MUR" and inv["status"] == "PENDING")
        total_mur_receivables = overdue_mur + pending_mur

        pending_usd = sum(inv["amount"] for inv in invoices if inv["currency"] == "USD" and inv["status"] == "PENDING")
        collected_usd = sum(inv["amount"] for inv in invoices if inv["currency"] == "USD" and inv["status"] in ("COMPLETED", "PAID"))
        collected_mur = sum(inv["amount"] for inv in invoices if inv["currency"] == "MUR" and inv["status"] in ("COMPLETED", "PAID"))

        return {
            "overdue_mur": overdue_mur,
            "pending_mur": pending_mur,
            "total_mur_receivables": total_mur_receivables,
            "pending_usd": pending_usd,
            "collected_usd": collected_usd,
            "collected_mur": collected_mur,
            "invoices": invoices
        }

    def format_reminder_message(self, invoice_id: str) -> Dict[str, Any]:
        """Generates polite, professional WhatsApp & Email reminder message."""
        invoices = self.load_invoices()
        target = next((inv for inv in invoices if inv["id"] == invoice_id), None)
        if not target:
            raise ValueError(f"Invoice {invoice_id} not found")

        client = target.get("client_name", "Client")
        amt = target.get("amount", 0)
        curr = target.get("currency", "MUR")
        desc = target.get("description", "Service")
        ref = target.get("id")

        if target.get("method") == "mcb_wire":
            msg = (
                f"Bonjour Team {client}! 👋\n\n"
                f"Hope you are having a productive week. Just a quick friendly follow-up regarding invoice *{ref}* "
                f"for *{desc}*.\n\n"
                f"💵 *Amount Due*: {curr} {amt:,.2f}\n"
                f"📱 *MCB Juice Transfer*: +230 58169420 (Deven Pawaray)\n"
                f"🏦 *MCB Account*: 000443260370\n"
                f"📝 *Payment Ref*: {ref}\n\n"
                f"Kindly let me know once transferred so I can reconcile the receipt. Thank you! - Deven"
            )
        else:
            pay_url = target.get("payment_url", "https://www.paypal.com")
            msg = (
                f"Hello {client}! 👋\n\n"
                f"Following up on invoice *{ref}* for *{desc}*.\n\n"
                f"💵 *Amount Due*: {curr} {amt:,.2f}\n"
                f"💳 *1-Click Card / PayPal Checkout*: {pay_url}\n\n"
                f"Thank you for your business! - Deven Pawaray"
            )

        return {
            "invoice_id": ref,
            "client_name": client,
            "amount": amt,
            "currency": curr,
            "formatted_message": msg,
            "whatsapp_link": f"https://wa.me/?text={urllib.parse.quote(msg)}"
        }

payment_service = PaymentService()

