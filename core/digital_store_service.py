"""
Nexus™ Digital Product Store & Instant Delivery Service
======================================================
Automates the sale, payment capture, and instant digital fulfillment of self-hosted developer utilities.
Zero manual intervention: PayPal / MCB Juice / Crypto capture -> instant file download + automatic email delivery.
Integrated with Conversion Recovery Engine and Multi-Rail Telemetry.
"""

import os
import sys
import json
import time
import zipfile
import secrets
import urllib.parse
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

from core.payment_service import payment_service
from security.financial_shield import financial_shield

PRODUCTS_DIR = os.path.abspath("products")
CUSTOM_CATALOG_FILE = os.path.join(PRODUCTS_DIR, "custom_catalog.json")

CATALOG = {
    "ghosttrack-osint-dossier": {
        "id": "ghosttrack-osint-dossier",
        "name": "GhostTrack Deep OSINT Executive Dossier",
        "tagline": "Unredacted organizational mapping in < 30 mins",
        "description": "On-demand competitive intelligence and deep executive contact dossiers. Delivered automatically via email within 15 minutes. Perfect for M&A scouts, headhunters, and enterprise closers.",
        "price_usd": 99.00,
        "price_mur": 4500.0,
        "filename": "ghosttrack_dossier_target.pdf",
        "badge": "🕵️ OSINT Report",
        "features": [
            "Automated email/phone correlation",
            "Cross-platform verification without manual browsing",
            "Deep organizational mapping",
            "Delivered in under 30 minutes"
        ]
    },
    "ai-red-team-audit": {
        "id": "ai-red-team-audit",
        "name": "AI Agent Red-Teaming & RAG Audit",
        "tagline": "24-hour rapid security assessment for LLM startups",
        "description": "Turnkey security audit for startups deploying LLM chatbots and agentic workflows. We test for indirect prompt injections, execute tool allowlisting audits, and provide an OWASP Top 10 certification.",
        "price_usd": 399.00,
        "price_mur": 18000.0,
        "filename": "nexus_ai_redteam_report.pdf",
        "badge": "🛡️ Security Audit",
        "features": [
            "Indirect prompt-injection test harnesses",
            "OWASP Top 10 for Agentic AI checklists",
            "Automated tool allowlisting auditing",
            "24-hour rapid execution"
        ]
    },
    "m2m-api-compute-key": {
        "id": "m2m-api-compute-key",
        "name": "Autonomous M2M Micro-Settlements (x402)",
        "tagline": "API Key for Base L2 Programmatic Services",
        "description": "Purchase programmatic access for your bots (ElizaOS, LangChain) to query Nexus services (AST syntax validation, context sanitization, escrow checks) at sub-dollar micro-fees.",
        "price_usd": 1.00,
        "price_mur": 45.0,
        "filename": "nexus_x402_api_key.txt",
        "badge": "🤖 M2M Compute",
        "features": [
            "Sub-dollar micro-fees in USDC",
            "Coinbase x402 Payment Required protocol",
            "AST Python code syntax validation",
            "Zero human intervention required"
        ]
    },
    "digital-vending-bundle": {
        "id": "digital-vending-bundle",
        "name": "The Digital Vending Machine Bundle",
        "tagline": "Frictionless single-file Python power tools",
        "description": "Self-serve micro-utilities solving acute technical headaches. Includes WhatsApp batch messengers, zombie SaaS unsubscribers, automated invoice parsers, and local CSV dedupers.",
        "price_usd": 19.00,
        "price_mur": 850.0,
        "filename": "nexus_vending_bundle.zip",
        "badge": "⚡ Scripts",
        "features": [
            "Zero dependencies required",
            "100% commercial ownership rights",
            "Instant digital download",
            "Replaces multiple SaaS subscriptions"
        ]
    },
    "ar-recovery-concierge": {
        "id": "ar-recovery-concierge",
        "name": "Automated A/R Recovery Concierge (1 Month)",
        "tagline": "Converts aged, overdue B2B receivables into settled cash",
        "description": "A polite, persistent WhatsApp & Email automated recovery concierge. We automatically follow up on your stalled invoices using our dynamic dunning engine.",
        "price_usd": 110.00,
        "price_mur": 5000.0,
        "filename": "ar_onboarding_webhook.json",
        "badge": "💸 FinOps Service",
        "features": [
            "Polite escalating reminder intervals",
            "WhatsApp & Email multi-channel routing",
            "Funded by recovered cash",
            "Ideal for medical practices & creative agencies"
        ]
    },
    "turnkey-white-label-handover": {
        "id": "turnkey-white-label-handover",
        "name": "Turnkey Vertical White-Label Code Handover",
        "tagline": "Complete IP transfer of ready-to-run web software",
        "description": "Direct purchase of pre-built production suites (Medical 360™, i-Travellix™, Enn Rev Enn Sourir™). Eliminates months of custom agency development.",
        "price_usd": 999.00,
        "price_mur": 45000.0,
        "filename": "turnkey_deployment_spec.pdf",
        "badge": "📦 Full IP Transfer",
        "features": [
            "Frontend portal + enterprise backend engine",
            "Sandbox QA & zip packaging included",
            "Zero recurring SaaS fees",
            "Live in 48 hours"
        ]
    },
    "bilingual-outbound-engine": {
        "id": "bilingual-outbound-engine",
        "name": "Bilingual French/English Cold Outbound Engine",
        "tagline": "Signal-based acquisition pipeline setup",
        "description": "Plug-and-play outbound acquisition pipeline built for agencies targeting French-speaking and bilingual markets (Mauritius, France, Switzerland).",
        "price_usd": 550.00,
        "price_mur": 25000.0,
        "filename": "outbound_engine_config.json",
        "badge": "🌍 Outbound Pipeline",
        "features": [
            "Challenger messaging 3-touch sequence",
            "UCB1 Conversion Bandit optimization",
            "Deployed in under 72 hours",
            "Bypasses generic spam filters"
        ]
    }
}


class DigitalStoreService:
    def __init__(self):
        os.makedirs(PRODUCTS_DIR, exist_ok=True)
        self._ensure_bundle_zip()

    def _ensure_bundle_zip(self):
        """Creates the master zip bundle including all 7 tools if not present or outdated."""
        zip_path = os.path.join(PRODUCTS_DIR, "nexus_dev_superpack.zip")
        sources = [
            "nexus_email_guardian.py",
            "nexus_whatsapp_bot_starter.py",
            "nexus_b2b_lead_scraper.py",
            "nexus_mcb_recon.py",
            "nexus_invoice_pdf_extractor.py",
            "nexus_crypto_price_alert.py",
            "nexus_seo_keyword_serp_tracker.py"
        ]
        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for src in sources:
                    src_path = os.path.join(PRODUCTS_DIR, src)
                    if os.path.exists(src_path):
                        zf.write(src_path, arcname=src)
                # Include a comprehensive README in the zip
                readme_content = (
                    "Nexus™ Anti-SaaS Developer Arsenal & Superpack\n"
                    "===============================================\n"
                    "Thank you for supporting independent, open-source and self-hosted software!\n\n"
                    "Tools included in this archive:\n"
                    "1. nexus_email_guardian.py           - IMAP spam cleaner & 2FA protector\n"
                    "2. nexus_whatsapp_bot_starter.py     - FastAPI conversational WhatsApp business bot\n"
                    "3. nexus_b2b_lead_scraper.py         - DNS MX record gatekeeper & verifier\n"
                    "4. nexus_mcb_recon.py                - MCB statement & Juice PDF reconciler (Mauritius B2B)\n"
                    "5. nexus_invoice_pdf_extractor.py    - PDF invoice line item & 15% VAT extractor\n"
                    "6. nexus_crypto_price_alert.py       - Self-hosted crypto feed & threshold daemon\n"
                    "7. nexus_seo_keyword_serp_tracker.py - Local Google search ranking tracker\n\n"
                    "Perpetual Commercial Rights:\n"
                    "You own these scripts permanently. Zero telemetry, zero recurring subscriptions.\n"
                    "Run them locally on your machine, server, or VPS.\n\n"
                    f"Created with pride by {os.getenv('FOUNDER_NAME', 'Deven Pawaray')} & Nexus AI.\n"
                    f"Support & Inquiries: {os.getenv('FOUNDER_EMAIL', 'devenpawaray@gmail.com')} | WhatsApp: {os.getenv('FOUNDER_WHATSAPP', '+23058169420')}\n"
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
        currency: str = "USD",
        payment_method: str = "paypal",
        add_setup_service: bool = False,
        coupon_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Creates an order with multi-rail support (PayPal REST API or MCB Juice domestic routing),
        order bump integration, and coupon verification.
        """
        product = self.get_product(product_id)
        if not product:
            raise ValueError(f"Product '{product_id}' not found in catalog.")

        is_usd = currency.upper() == "USD"
        base_amount = product["price_usd"] if is_usd else product["price_mur"]

        # Order bump: Add 1-on-1 Setup Assistance
        bump_amount = 0.0
        if add_setup_service:
            bump_amount = 5.00 if is_usd else 225.0

        total_amount = base_amount + bump_amount

        # Coupon application
        applied_discount = 0.0
        if coupon_code and coupon_code.strip().upper() == "SAVE15":
            applied_discount = round(total_amount * 0.15, 2)
            total_amount = round(total_amount - applied_discount, 2)

        download_token = secrets.token_urlsafe(16)
        description = f"Nexus: {product['name']}"
        if add_setup_service:
            description += " + 1-on-1 Setup"

        # Record lead in conversion recovery engine
        try:
            from core.revenue_engine import revenue_engine
            revenue_engine.capture_abandoned_lead(
                contact=buyer_email,
                source="store_checkout",
                cart_details={
                    "product_id": product_id,
                    "product_name": product["name"],
                    "amount": total_amount,
                    "currency": currency.upper(),
                    "buyer_name": buyer_name,
                    "add_setup_service": add_setup_service,
                    "coupon": coupon_code
                }
            )
            revenue_engine.track_event("initiate_checkout", {
                "product_id": product_id,
                "amount": total_amount,
                "currency": currency.upper(),
                "payment_method": payment_method
            })
        except Exception:
            pass

        # 1. Domestic MCB Juice Flow
        if payment_method.lower() in ("juice", "mcb_wire") or currency.upper() == "MUR":
            juice_ref = f"NEXUS-{product_id.replace('nexus-', '').upper()[:8]}-{secrets.token_hex(2).upper()}"
            inv = payment_service.create_invoice(
                client_name=buyer_name or "Mauritius Developer",
                client_email=buyer_email,
                amount=total_amount,
                currency="MUR",
                description=description,
                method="mcb_wire"
            )
            
            # Enrich invoice with digital metadata
            invoices = payment_service.load_invoices()
            for record in invoices:
                if record["id"] == inv["id"]:
                    record["product_id"] = product_id
                    record["product_name"] = product["name"]
                    record["download_token"] = download_token
                    record["delivery_status"] = "PENDING_JUICE"
                    record["buyer_email"] = buyer_email
                    record["juice_ref"] = juice_ref
                    break
            payment_service.save_invoices(invoices)

            whatsapp_phone = os.getenv("FOUNDER_WHATSAPP", "+23058169420")
            wa_text = (
                f"Bonjour Deven! 👋\n\n"
                f"Je viens de commander *{product['name']}* sur le Nexus Store.\n"
                f"💵 Montant: Rs {total_amount:,.2f} MUR\n"
                f"📝 Référence: *{juice_ref}*\n"
                f"📧 Email de réception: {buyer_email}\n\n"
                f"Voici la capture de mon paiement Juice. Merci de me débloquer le script!"
            )
            wa_link = f"https://wa.me/{whatsapp_phone.replace('+', '').replace(' ', '')}?text={urllib.parse.quote(wa_text)}"

            return {
                "success": True,
                "payment_method": "juice",
                "product_id": product_id,
                "product_name": product["name"],
                "amount": total_amount,
                "currency": "MUR",
                "juice_reference": juice_ref,
                "juice_mobile": "+230 58169420",
                "invoice_id": inv.get("id"),
                "whatsapp_confirmation_url": wa_link,
                "download_token": download_token,
                "instructions": f"Envoyez Rs {total_amount:,.2f} au 58169420 avec la référence {juice_ref}."
            }

        # 2. Global PayPal REST API Flow
        inv = payment_service.create_invoice(
            client_name=buyer_name or "Valued Developer",
            client_email=buyer_email or "developer@example.com",
            amount=total_amount,
            currency="USD",
            description=description,
            method="paypal"
        )

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
            "payment_method": "paypal",
            "product_id": product_id,
            "product_name": product["name"],
            "order_id": inv.get("paypal_order_id"),
            "checkout_url": inv.get("payment_url"),
            "invoice_id": inv.get("id"),
            "amount": total_amount,
            "currency": "USD",
            "download_token": download_token
        }

    def fulfill_order(self, order_id_or_invoice_id: str) -> Dict[str, Any]:
        """
        Validates payment capture, marks invoice as COMPLETED,
        triggers automatic conversion recording, and dispatches digital file.
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

        # If not yet confirmed completed and order_id exists, verify with PayPal
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

        # Mark lead as converted in RevenueEngine
        try:
            from core.revenue_engine import revenue_engine
            if buyer_email:
                revenue_engine.mark_lead_converted(buyer_email)
            revenue_engine.track_event("purchase", {
                "order_id": order_id or target_inv["id"],
                "product_id": product["id"],
                "amount": target_inv.get("amount"),
                "currency": target_inv.get("currency")
            })
        except Exception:
            pass

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
        """Dispatches automated delivery email with direct download link and preview."""
        from core.email_client import EmailClient
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

        base_url = "https://nexus-workforce.vercel.app"
        download_url = f"{base_url}/download/{product['id']}?token={download_token}"

        body_text = (
            f"Dear Developer,\n\n"
            f"Thank you so much for your purchase of {product['name']}!\n\n"
            f"Your instant download link is:\n"
            f"{download_url}\n\n"
            f"Quick Start:\n"
            f"1. Save the file locally on your machine.\n"
            f"2. Run it directly with Python 3.\n"
            f"3. No monthly subscription, no vendor lock-in. You own the script forever.\n\n"
            f"Warm regards,\n"
            f"{os.getenv('FOUNDER_NAME', 'Deven Pawaray')} & Nexus AI Team\n"
            f"WhatsApp Support: {os.getenv('FOUNDER_WHATSAPP', '+23058169420')}\n"
        )

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #070b14; color: #f8fafc; padding: 30px;">
          <div style="max-width: 600px; margin: 0 auto; background: #0d1527; border-radius: 16px; padding: 30px; border: 1px solid #1e2c4f;">
            <div style="font-size: 24px; font-weight: bold; color: #38bdf8; margin-bottom: 10px;">⚡ Nexus™ Workforce</div>
            <h2 style="color: #ffffff; margin-top: 0;">Thank you for your purchase!</h2>
            <p style="color: #94a3b8; font-size: 16px;">Here is your instant access to <strong>{product['name']}</strong>.</p>
            
            <div style="margin: 25px 0; text-align: center;">
              <a href="{download_url}" style="background: linear-gradient(135deg, #0284c7, #0369a1); color: #ffffff; padding: 14px 28px; border-radius: 10px; text-decoration: none; font-weight: bold; font-size: 16px; display: inline-block;">
                📥 Download {product['filename']} Now
              </a>
            </div>

            <div style="background: #070b14; border-radius: 8px; padding: 16px; font-family: monospace; font-size: 12px; color: #cbd5e1; overflow-x: auto; margin-bottom: 20px;">
              <div style="color: #38bdf8; font-weight: bold; margin-bottom: 8px;">// Preview snippet</div>
              <pre style="margin: 0;">{file_snippet}</pre>
            </div>

            <p style="color: #94a3b8; font-size: 14px; line-height: 1.5;">
              • 100% self-hosted on your machine.<br>
              • Zero monthly subscriptions.<br>
              • Commercial rights included.
            </p>

            <hr style="border: none; border-top: 1px solid #1e2c4f; margin: 25px 0;">
            <p style="font-size: 12px; color: #64748b;">
              Created with pride by {os.getenv('FOUNDER_NAME', 'Deven Pawaray')} | Grand Baie, Mauritius<br>
              WhatsApp Support: {os.getenv('FOUNDER_WHATSAPP', '+23058169420')} | Email: {os.getenv('FOUNDER_EMAIL', 'devenpawaray@gmail.com')}
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
                from_name=f"Nexus Micro-Store ({os.getenv('FOUNDER_NAME', 'Deven Pawaray')})",
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
                # If product matches or if user bought bundle or agency license
                if inv.get("product_id") in (product_id, "nexus-developer-bundle", "nexus-agency-license"):
                    return True
        return False


digital_store_service = DigitalStoreService()
