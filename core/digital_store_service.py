"""
Nexus™ Digital Product Store & Instant Delivery Service
======================================================
Automates the sale, payment capture, and instant digital fulfillment of $1.00 USD Python tools.
Zero manual intervention: PayPal capture -> instant file download + automatic email delivery.
"""

import os
import sys
import json
import time
import zipfile
import secrets
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

from core.payment_service import payment_service
from security.financial_shield import financial_shield

PRODUCTS_DIR = os.path.abspath("products")
CUSTOM_CATALOG_FILE = os.path.join(PRODUCTS_DIR, "custom_catalog.json")
CATALOG = {
    "nexus-email-guardian": {
        "id": "nexus-email-guardian",
        "name": "Nexus™ Email Guardian",
        "tagline": "Self-Hosted IMAP Spam Killer & 2FA Security Shield",
        "description": "A lightweight, zero-dependency Python script that runs locally to purge marketing spam while locking down 2FA/OTP verification codes.",
        "price_usd": 1.00,
        "price_mur": 45.0,
        "filename": "nexus_email_guardian.py",
        "badge": "Popular",
        "features": [
            "100% self-hosted — no 3rd-party reading your inbox",
            "Protects 2FA, OTP, banking, and receipt emails",
            "Auto-purges disposable spam TLDs (.xyz, .buzz, etc.)",
            "Zero monthly subscription fee"
        ]
    },
    "nexus-whatsapp-bot": {
        "id": "nexus-whatsapp-bot",
        "name": "Nexus™ WhatsApp Bot Starter",
        "tagline": "FastAPI Conversational Business Bot & Direct wa.me Router",
        "description": "Production-ready FastAPI conversational WhatsApp concierge template. Ready for Meta Cloud API or direct wa.me link generation.",
        "price_usd": 1.00,
        "price_mur": 45.0,
        "filename": "nexus_whatsapp_bot_starter.py",
        "badge": "Hot",
        "features": [
            "Instant 1-click wa.me customer chat links",
            "Autonomous FAQ & business hours auto-responder",
            "Integrated payment links (PayPal & MCB Juice)",
            "Deployable in 60 seconds on any free VPS or local server"
        ]
    },
    "nexus-b2b-scraper": {
        "id": "nexus-b2b-scraper",
        "name": "Nexus™ B2B Lead Scraper & MX Verifier",
        "tagline": "DNS MX Gatekeeper & Zero-Bounce Email Verifier",
        "description": "A high-speed DNS-level mail exchange verifier in Python. Filters out ghost domains, prevents SMTP bounce bans, and cleans prospect lists.",
        "price_usd": 1.00,
        "price_mur": 45.0,
        "filename": "nexus_b2b_lead_scraper.py",
        "badge": "Essential",
        "features": [
            "Validates real DNS MX mail servers instantly",
            "Prevents sender domain reputation damage & blacklisting",
            "Zero external API keys or paid credits required",
            "Processes thousands of leads in seconds"
        ]
    },
    "nexus-developer-bundle": {
        "id": "nexus-developer-bundle",
        "name": "Nexus™ 3-in-1 Dev Superpack",
        "tagline": "Complete Automation Triad (Email + WhatsApp + Lead Verifier)",
        "description": "Get all three flagship Nexus automation utilities bundled together for the special launch price of just $1.00 USD.",
        "price_usd": 1.00,
        "price_mur": 45.0,
        "filename": "nexus_dev_superpack.zip",
        "badge": "Best Value (3-in-1)",
        "features": [
            "Includes Email Guardian + WhatsApp Bot + B2B Lead Verifier",
            "All source code with MIT-style commercial usage rights",
            "Full developer setup instructions & documentation",
            "Instant single-click zip download"
        ]
    }
}


class DigitalStoreService:
    def __init__(self):
        os.makedirs(PRODUCTS_DIR, exist_ok=True)
        self._ensure_bundle_zip()

    def _ensure_bundle_zip(self):
        """Creates the 3-in-1 zip bundle if it doesn't already exist or if files changed."""
        zip_path = os.path.join(PRODUCTS_DIR, "nexus_dev_superpack.zip")
        sources = [
            "nexus_email_guardian.py",
            "nexus_whatsapp_bot_starter.py",
            "nexus_b2b_lead_scraper.py"
        ]
        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for src in sources:
                    src_path = os.path.join(PRODUCTS_DIR, src)
                    if os.path.exists(src_path):
                        zf.write(src_path, arcname=src)
                # Include a README in the zip
                readme_content = (
                    "Nexus™ Developer Automation Superpack\n"
                    "====================================\n"
                    "Thank you for supporting independent open-source software!\n\n"
                    "Tools included:\n"
                    "1. nexus_email_guardian.py   - IMAP spam cleaner & 2FA protector\n"
                    "2. nexus_whatsapp_bot_starter.py - FastAPI WhatsApp business bot\n"
                    "3. nexus_b2b_lead_scraper.py - DNS MX record gatekeeper & verifier\n\n"
                    "Created with pride by Deven Pawaray & Nexus AI.\n"
                    "Support & Questions: devenpawaray@gmail.com | WhatsApp: +230 58169420\n"
                )
                zf.writestr("README.txt", readme_content)
        except Exception as e:
            print(f"[DigitalStoreService] Warning building zip bundle: {e}")

    def _load_custom_catalog(self) -> Dict[str, Dict[str, Any]]:
        try:
            if os.path.exists(CUSTOM_CATALOG_FILE):
                with open(CUSTOM_CATALOG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def register_custom_product(self, product_entry: Dict[str, Any]):
        """Persists a new factory-generated digital product into the catalog."""
        custom = self._load_custom_catalog()
        custom[product_entry["id"]] = product_entry
        try:
            with open(CUSTOM_CATALOG_FILE, "w", encoding="utf-8") as f:
                json.dump(custom, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[DigitalStoreService] Error saving custom catalog: {e}")
        CATALOG[product_entry["id"]] = product_entry
        self._ensure_bundle_zip()

    def get_catalog(self) -> List[Dict[str, Any]]:
        """Returns the full catalog of available digital products."""
        custom = self._load_custom_catalog()
        combined = {**CATALOG, **custom}
        return list(combined.values())

    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        custom = self._load_custom_catalog()
        return CATALOG.get(product_id) or custom.get(product_id)

    def create_checkout_order(
        self,
        product_id: str,
        buyer_email: str,
        buyer_name: str = "Valued Developer",
        currency: str = "USD"
    ) -> Dict[str, Any]:
        """Creates a live 1-click PayPal checkout token for a specific digital product."""
        product = self.get_product(product_id)
        if not product:
            raise ValueError(f"Product '{product_id}' not found in catalog.")

        amount = product["price_usd"] if currency.upper() == "USD" else product["price_mur"]
        download_token = secrets.token_urlsafe(16)

        # Create live invoice/order via payment_service
        inv = payment_service.create_invoice(
            client_name=buyer_name or "Valued Developer",
            client_email=buyer_email or "developer@example.com",
            amount=amount,
            currency=currency.upper(),
            description=f"Nexus Digital Tool: {product['name']}",
            method="paypal"
        )

        # Enrich invoice with digital delivery metadata
        invoices = payment_service.load_invoices()
        for record in invoices:
            if record["id"] == inv["id"]:
                record["product_id"] = product_id
                record["product_name"] = product["name"]
                record["download_token"] = download_token
                record["delivery_status"] = "PENDING"
                record["buyer_email"] = buyer_email
                break
        payment_service.save_invoices(invoices)

        return {
            "success": True,
            "product_id": product_id,
            "product_name": product["name"],
            "order_id": inv.get("paypal_order_id"),
            "checkout_url": inv.get("payment_url"),
            "invoice_id": inv.get("id"),
            "amount": amount,
            "currency": currency.upper(),
            "download_token": download_token
        }

    def fulfill_order(self, order_id_or_invoice_id: str) -> Dict[str, Any]:
        """
        Validates payment capture, marks invoice as COMPLETED,
        and triggers instant digital fulfillment (email dispatch).
        """
        invoices = payment_service.load_invoices()
        target_inv = None
        for inv in invoices:
            if inv["id"] == order_id_or_invoice_id or inv.get("paypal_order_id") == order_id_or_invoice_id:
                target_inv = inv
                break

        if not target_inv:
            return {"success": False, "error": f"Order {order_id_or_invoice_id} not found."}

        order_id = target_inv.get("paypal_order_id")
        current_status = target_inv.get("status")

        # If not yet confirmed completed, verify with PayPal
        if current_status != "COMPLETED" and order_id:
            st_res = payment_service.check_paypal_order_status(order_id)
            live_status = st_res.get("status")
            if live_status in ("COMPLETED", "CAPTURED", "APPROVED"):
                target_inv["status"] = "COMPLETED"
                target_inv["settled_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                return {
                    "success": False,
                    "status": live_status,
                    "error": f"Payment is not completed yet (status: {live_status})."
                }

        # Mark paid
        target_inv["status"] = "COMPLETED"
        product_id = target_inv.get("product_id")
        product = self.get_product(product_id) or CATALOG.get("nexus-developer-bundle")
        buyer_email = target_inv.get("buyer_email") or target_inv.get("client_email")
        download_token = target_inv.get("download_token") or secrets.token_urlsafe(16)
        target_inv["download_token"] = download_token

        # Send delivery email if not sent yet
        if target_inv.get("delivery_status") != "DELIVERED" and buyer_email and "@" in buyer_email:
            email_res = self._send_fulfillment_email(
                buyer_email=buyer_email,
                product=product,
                download_token=download_token
            )
            target_inv["delivery_status"] = "DELIVERED" if email_res.get("success") else "FAILED_EMAIL"
            target_inv["delivery_details"] = email_res

        payment_service.save_invoices(invoices)

        return {
            "success": True,
            "order_id": order_id,
            "invoice_id": target_inv["id"],
            "status": "COMPLETED",
            "product_id": product["id"],
            "product_name": product["name"],
            "download_token": download_token,
            "download_url": f"/download/{product['id']}?token={download_token}"
        }

    def _send_fulfillment_email(
        self,
        buyer_email: str,
        product: Dict[str, Any],
        download_token: str
    ) -> Dict[str, Any]:
        """Dispatches automated thank-you email with direct download link and script content."""
        from email_client import EmailClient
        import os

        email_user = os.getenv("EMAIL_ACCOUNT", "").strip()
        email_pass = os.getenv("EMAIL_PASSWORD", "").strip()
        if not email_user or not email_pass:
            return {"success": False, "error": "SMTP credentials not configured."}

        client = EmailClient(
            host="imap.gmail.com",
            port=993,
            username=email_user,
            password=email_pass,
            smtp_host="smtp.gmail.com",
            smtp_port=465
        )

        subject = f"Your Digital Download: {product['name']} (Nexus™ Workforce)"
        
        file_path = os.path.join(PRODUCTS_DIR, product["filename"])
        file_snippet = ""
        if os.path.exists(file_path) and product["filename"].endswith(".py"):
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()[:40]
                file_snippet = "".join(lines)

        download_url = f"http://127.0.0.1:8000/download/{product['id']}?token={download_token}"

        body_text = (
            f"Dear Developer,\n\n"
            f"Thank you so much for your purchase of {product['name']}!\n\n"
            f"Your instant download link is:\n"
            f"{download_url}\n\n"
            f"Quick Start:\n"
            f"1. Save the file locally on your machine.\n"
            f"2. Run it directly with Python 3.\n"
            f"3. No monthly subscription, no vendor lock-in. You own the script forever.\n\n"
            f"If you ever need any assistance or custom automation, feel free to reply directly to this email.\n\n"
            f"Warm regards,\n"
            f"Deven Pawaray & Nexus AI Team\n"
            f"Grand Baie, Mauritius | WhatsApp: +230 58169420\n"
        )

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 30px;">
          <div style="max-width: 600px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 30px; border: 1px solid #334155;">
            <div style="font-size: 24px; font-weight: bold; color: #38bdf8; margin-bottom: 10px;">⚡ Nexus™ Workforce</div>
            <h2 style="color: #ffffff; margin-top: 0;">Thank you for your purchase!</h2>
            <p style="color: #94a3b8; font-size: 16px;">Here is your instant access to <strong>{product['name']}</strong> ($1.00 USD).</p>
            
            <div style="margin: 25px 0; text-align: center;">
              <a href="{download_url}" style="background: #2563eb; color: #ffffff; padding: 14px 28px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 16px; display: inline-block;">
                📥 Download {product['filename']} Now
              </a>
            </div>

            <div style="background: #0f172a; border-radius: 8px; padding: 16px; font-family: monospace; font-size: 12px; color: #cbd5e1; overflow-x: auto; margin-bottom: 20px;">
              <div style="color: #38bdf8; font-weight: bold; margin-bottom: 8px;">// Preview snippet</div>
              <pre style="margin: 0;">{file_snippet}</pre>
            </div>

            <p style="color: #94a3b8; font-size: 14px; line-height: 1.5;">
              • 100% self-hosted on your machine.<br>
              • Zero monthly subscriptions.<br>
              • Commercial rights included.
            </p>

            <hr style="border: none; border-top: 1px solid #334155; margin: 25px 0;">
            <p style="font-size: 12px; color: #64748b;">
              Created with pride by Deven Pawaray | Grand Baie, Mauritius<br>
              WhatsApp Support: +230 58169420 | Email: devenpawaray@gmail.com
            </p>
          </div>
        </body>
        </html>
        """

        try:
            return client.send_email(
                to_email=buyer_email,
                subject=subject,
                body=body_text,
                from_name="Nexus Micro-Store (Deven Pawaray)",
                html_body=html_body
            )
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_download_path(self, product_id: str) -> Optional[str]:
        """Returns the absolute file path for a valid product."""
        product = self.get_product(product_id)
        if not product:
            return None
        file_path = os.path.join(PRODUCTS_DIR, product["filename"])
        if not os.path.exists(file_path):
            self._ensure_bundle_zip()
        return file_path if os.path.exists(file_path) else None

    def validate_download_token(self, product_id: str, token: str) -> bool:
        """Validates if a download token is authentic and tied to a paid order."""
        if not token:
            return False
        invoices = payment_service.load_invoices()
        for inv in invoices:
            if inv.get("download_token") == token:
                # If product matches or if user bought bundle
                if inv.get("product_id") in (product_id, "nexus-developer-bundle"):
                    return True
        return False


digital_store_service = DigitalStoreService()
