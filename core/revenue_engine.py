# -*- coding: utf-8 -*-
"""
Nexus Workforce Engine — Conversion Recovery & Revenue Telemetry Engine
=============================================================================
Diagnoses revenue bottlenecks, captures abandoned checkout leads in real-time,
and automates recovery campaigns via email and WhatsApp to turn lost prospects
into paying customers.
"""

import os
import json
import time
import secrets
import urllib.parse
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.paths import resolve_data_path

REVENUE_EVENTS_FILE = resolve_data_path("revenue_events.json")
ABANDONED_LEADS_FILE = resolve_data_path("abandoned_leads.json")


class RevenueEngine:
    def __init__(self):
        self._ensure_storage()

    def _ensure_storage(self):
        for f_path in [REVENUE_EVENTS_FILE, ABANDONED_LEADS_FILE]:
            if not os.path.exists(f_path):
                try:
                    with open(f_path, "w", encoding="utf-8") as f:
                        json.dump([], f, indent=2)
                except Exception:
                    pass

    def track_event(self, event_name: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Tracks critical funnel telemetry events."""
        event_record = {
            "id": f"EVT-{int(time.time() * 1000)}-{secrets.token_hex(3)}",
            "event_name": event_name,
            "payload": payload or {},
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            events = []
            if os.path.exists(REVENUE_EVENTS_FILE):
                with open(REVENUE_EVENTS_FILE, "r", encoding="utf-8") as f:
                    try:
                        events = json.load(f)
                    except Exception:
                        events = []
            events.insert(0, event_record)
            with open(REVENUE_EVENTS_FILE, "w", encoding="utf-8") as f:
                json.dump(events[:1000], f, indent=2)
            return {"success": True, "event_id": event_record["id"], "tracked": event_name}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def capture_abandoned_lead(
        self,
        contact: str,
        source: str = "store_checkout_modal",
        cart_details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Captures an email or phone number entered during checkout before completion.
        Generates recovery tokens, discount codes, and automated rescue sequences.
        """
        if not contact or "@" not in contact and len(contact.strip()) < 7:
            return {"success": False, "error": "Invalid contact information."}

        contact = contact.strip().lower()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cart = cart_details or {}
        product_id = cart.get("product_id", "nexus-developer-bundle")
        product_name = cart.get("product_name", "Nexus™ Software Utility")
        amount = float(cart.get("amount", 9.00))
        currency = cart.get("currency", "USD").upper()

        leads = []
        if os.path.exists(ABANDONED_LEADS_FILE):
            try:
                with open(ABANDONED_LEADS_FILE, "r", encoding="utf-8") as f:
                    leads = json.load(f)
            except Exception:
                leads = []

        # Check if recent lead exists within last 24h
        existing = next((l for l in leads if l.get("contact") == contact and l.get("product_id") == product_id), None)
        discount_code = "SAVE15"
        discounted_amount = round(amount * 0.85, 2)
        recovery_token = secrets.token_urlsafe(12)
        recovery_url = f"/store?recover={recovery_token}&prod={product_id}&coupon={discount_code}"

        if existing:
            existing["cart_details"] = cart
            existing["last_active"] = now_str
            existing["attempts"] = existing.get("attempts", 1) + 1
            lead_id = existing["id"]
        else:
            lead_id = f"LEAD-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}"
            new_lead = {
                "id": lead_id,
                "contact": contact,
                "buyer_name": cart.get("buyer_name", "Developer"),
                "product_id": product_id,
                "product_name": product_name,
                "amount": amount,
                "currency": currency,
                "discount_code": discount_code,
                "discounted_amount": discounted_amount,
                "source": source,
                "cart_details": cart,
                "status": "PENDING_RECOVERY",
                "recovery_token": recovery_token,
                "recovery_url": recovery_url,
                "captured_at": now_str,
                "last_active": now_str,
                "recovery_dispatched": False,
                "dispatched_at": None,
                "attempts": 1
            }
            leads.insert(0, new_lead)

        try:
            with open(ABANDONED_LEADS_FILE, "w", encoding="utf-8") as f:
                json.dump(leads[:500], f, indent=2)
            
            # Log funnel dropoff event
            self.track_event("lead_captured", {
                "lead_id": lead_id,
                "contact": contact,
                "product_id": product_id,
                "amount": amount,
                "currency": currency
            })

            return {
                "success": True,
                "lead_id": lead_id,
                "status": "CAPTURED",
                "recovery_url": recovery_url,
                "discount_code": discount_code
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def trigger_lead_recovery(self, lead_id: str, channel: str = "auto") -> Dict[str, Any]:
        """
        Executes an automated recovery action for an abandoned checkout lead.
        Supports SMTP email dispatch and direct WhatsApp message link generation.
        """
        leads = []
        if os.path.exists(ABANDONED_LEADS_FILE):
            try:
                with open(ABANDONED_LEADS_FILE, "r", encoding="utf-8") as f:
                    leads = json.load(f)
            except Exception:
                leads = []

        lead = next((l for l in leads if l["id"] == lead_id), None)
        if not lead:
            return {"success": False, "error": f"Lead {lead_id} not found."}

        contact = lead.get("contact", "")
        buyer_name = lead.get("buyer_name", "Developer")
        prod_name = lead.get("product_name", "Nexus™ Software Utility")
        currency = lead.get("currency", "USD")
        orig_price = lead.get("amount", 9.0)
        disc_price = lead.get("discounted_amount", orig_price * 0.85)
        disc_code = lead.get("discount_code", "SAVE15")
        rec_url = lead.get("recovery_url", "/store")

        curr_symbol = "$" if currency == "USD" else "Rs "
        whatsapp_phone = os.getenv("FOUNDER_WHATSAPP", "+23058169420")
        founder_name = os.getenv("FOUNDER_NAME", "Deven Pawaray")

        # 1. Prepare copy for WhatsApp
        wa_message = (
            f"Hello {buyer_name}! 👋\n\n"
            f"I noticed you were checking out *{prod_name}* on the Nexus Store.\n\n"
            f"To help you get started without friction, here is a private 15% discount:\n"
            f"🎁 Coupon: *{disc_code}* (Only {curr_symbol}{disc_price:,.2f} {currency})\n"
            f"🔗 Complete 1-Click Access: https://nexus-workforce.vercel.app{rec_url}\n\n"
            f"Let me know if you have any questions or need custom integration help! — {founder_name}"
        )
        wa_link = f"https://wa.me/{whatsapp_phone.replace('+', '').replace(' ', '')}?text={urllib.parse.quote(wa_message)}"

        email_result = None
        # 2. If contact is email, attempt automated dispatch
        if "@" in contact and (channel in ("auto", "email")):
            try:
                from core.email_client import EmailClient
                email_user = os.getenv("EMAIL_ACCOUNT", "").strip()
                email_pass = os.getenv("EMAIL_PASSWORD", "").strip()
                if email_user and email_pass:
                    client = EmailClient(
                        host="imap.gmail.com",
                        port=993,
                        username=email_user,
                        password=email_pass,
                        smtp_host="smtp.gmail.com",
                        smtp_port=465
                    )
                    subject = f"Complete your setup: 15% off {prod_name} (Nexus™ Anti-SaaS)"
                    body_text = (
                        f"Hi {buyer_name},\n\n"
                        f"We noticed you were checking out {prod_name}.\n\n"
                        f"As an independent developer, you shouldn't have to pay recurring monthly SaaS rent. "
                        f"To welcome you to our community, here is a 15% discount coupon ({disc_code}) bringing your "
                        f"one-time buyout price down to {curr_symbol}{disc_price:,.2f} {currency}.\n\n"
                        f"Claim your perpetual license here:\n"
                        f"https://nexus-workforce.vercel.app{rec_url}\n\n"
                        f"Zero subscriptions. Run 100% locally on your machine forever.\n\n"
                        f"Best regards,\n"
                        f"{founder_name} & Nexus Engineering Team\n"
                        f"WhatsApp: {whatsapp_phone}\n"
                    )
                    html_body = f"""
                    <div style="background:#070b14;color:#f8fafc;padding:30px;font-family:sans-serif;">
                      <div style="max-width:560px;margin:0 auto;background:#0d1527;border:1px solid #1e2c4f;border-radius:16px;padding:28px;">
                        <h2 style="color:#38bdf8;margin-top:0;">⚡ Nexus™ Anti-SaaS Arsenal</h2>
                        <p style="font-size:16px;color:#cbd5e1;">Hi <strong>{buyer_name}</strong>,</p>
                        <p style="color:#94a3b8;line-height:1.6;">You were almost done securing your perpetual license for <strong>{prod_name}</strong>.</p>
                        <div style="background:rgba(56,189,248,0.08);border:1px dashed #38bdf8;border-radius:12px;padding:18px;margin:20px 0;text-align:center;">
                          <div style="font-size:13px;color:#94a3b8;text-transform:uppercase;letter-spacing:1px;">Special Recovery Coupon</div>
                          <div style="font-size:24px;font-weight:bold;color:#38bdf8;margin:6px 0;">{disc_code} (15% OFF)</div>
                          <div style="font-size:15px;color:#cbd5e1;">New Price: <strong>{curr_symbol}{disc_price:,.2f} {currency}</strong> (One-Time Buyout)</div>
                        </div>
                        <div style="text-align:center;margin:25px 0;">
                          <a href="https://nexus-workforce.vercel.app{rec_url}" style="background:linear-gradient(135deg,#0284c7,#0369a1);color:#fff;padding:14px 28px;border-radius:10px;text-decoration:none;font-weight:bold;font-size:16px;display:inline-block;">
                            ⚡ Complete Checkout &amp; Download Source
                          </a>
                        </div>
                        <p style="font-size:12px;color:#64748b;margin-top:20px;">Questions? Reply directly to this email or reach us on WhatsApp: {whatsapp_phone}</p>
                      </div>
                    </div>
                    """
                    email_result = client.send_email(
                        to_email=contact,
                        subject=subject,
                        body=body_text,
                        from_name=f"Nexus Store ({founder_name})",
                        html_body=html_body
                    )
            except Exception as ex:
                email_result = {"success": False, "error": str(ex)}

        lead["recovery_dispatched"] = True
        lead["dispatched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lead["status"] = "DISPATCHED"

        try:
            with open(ABANDONED_LEADS_FILE, "w", encoding="utf-8") as f:
                json.dump(leads, f, indent=2)
        except Exception:
            pass

        return {
            "success": True,
            "lead_id": lead_id,
            "contact": contact,
            "channel": channel,
            "email_dispatched": email_result.get("success") if email_result else False,
            "email_details": email_result,
            "whatsapp_link": wa_link,
            "whatsapp_message": wa_message
        }

    def mark_lead_converted(self, contact_or_token: str) -> bool:
        """Marks a lead as recovered upon successful purchase."""
        if not contact_or_token:
            return False
        leads = []
        if os.path.exists(ABANDONED_LEADS_FILE):
            try:
                with open(ABANDONED_LEADS_FILE, "r", encoding="utf-8") as f:
                    leads = json.load(f)
            except Exception:
                return False

        updated = False
        target = contact_or_token.strip().lower()
        for l in leads:
            if l.get("contact") == target or l.get("recovery_token") == contact_or_token:
                l["status"] = "CONVERTED"
                l["converted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updated = True
                break

        if updated:
            try:
                with open(ABANDONED_LEADS_FILE, "w", encoding="utf-8") as f:
                    json.dump(leads, f, indent=2)
                self.track_event("lead_recovered", {"target": contact_or_token})
            except Exception:
                pass
        return updated

    def get_funnel_analytics(self) -> Dict[str, Any]:
        """Calculates real-time conversion funnel metrics and identifying dropoffs."""
        events = []
        if os.path.exists(REVENUE_EVENTS_FILE):
            try:
                with open(REVENUE_EVENTS_FILE, "r", encoding="utf-8") as f:
                    events = json.load(f)
            except Exception:
                events = []

        leads = []
        if os.path.exists(ABANDONED_LEADS_FILE):
            try:
                with open(ABANDONED_LEADS_FILE, "r", encoding="utf-8") as f:
                    leads = json.load(f)
            except Exception:
                leads = []

        # Count events by type
        counts = {
            "page_view": 0,
            "view_item": 0,
            "preview_code": 0,
            "initiate_checkout": 0,
            "lead_captured": 0,
            "order_bump_toggled": 0,
            "payment_attempt": 0,
            "purchase": 0,
            "dropoff": 0,
            "social_share": 0
        }
        for ev in events:
            name = ev.get("event_name")
            if name in counts:
                counts[name] += 1

        # Check completed purchases from invoices ledger
        try:
            from core.payment_service import payment_service
            invoices = payment_service.load_invoices()
            completed_invoices = [i for i in invoices if i.get("status") in ("COMPLETED", "PAID", "SETTLED")]
            paid_revenue_usd = sum(
                float(i.get("amount", 0)) if i.get("currency") == "USD" else float(i.get("amount", 0)) / 46.5
                for i in completed_invoices
            )
        except Exception:
            completed_invoices = []
            paid_revenue_usd = 0.0

        initiated = max(counts["initiate_checkout"], len(leads))
        completed = max(counts["purchase"], len(completed_invoices))
        cvr = round((completed / initiated * 100), 1) if initiated > 0 else 0.0

        # Calculate lost revenue from abandoned leads
        potential_lost_usd = sum(
            l.get("amount", 9.0) if l.get("currency") == "USD" else l.get("amount", 415.0) / 46.5
            for l in leads if l.get("status") != "CONVERTED"
        )

        return {
            "success": True,
            "metrics": {
                "page_views": counts["page_view"],
                "product_views": counts["view_item"],
                "code_previews": counts["preview_code"],
                "checkout_initiated": initiated,
                "leads_captured": len(leads),
                "order_bumps_toggled": counts["order_bump_toggled"],
                "payment_attempts": counts["payment_attempt"],
                "completed_purchases": completed,
                "conversion_rate_pct": cvr,
                "social_shares": counts["social_share"],
                "total_settled_revenue_usd": round(paid_revenue_usd, 2),
                "potential_abandoned_loss_usd": round(potential_lost_usd, 2)
            },
            "leads": leads[:20],
            "recent_events": events[:20]
        }

    def get_diagnostics_report(self) -> Dict[str, Any]:
        """Provides an architectural diagnosis of conversion leaks and recommended fixes."""
        analytics = self.get_funnel_analytics()
        metrics = analytics["metrics"]
        
        leakages = []
        if metrics["code_previews"] > 0 and metrics["checkout_initiated"] == 0:
            leakages.append({
                "stage": "Preview -> Checkout",
                "severity": "HIGH",
                "issue": "Users inspect source previews but fail to click 'Buy This Script'.",
                "recommendation": "Add prominent 1-click CTA inside preview modal with money-back guarantee badge."
            })
        if metrics["checkout_initiated"] > metrics["leads_captured"]:
            leakages.append({
                "stage": "Checkout -> Lead Capture",
                "severity": "CRITICAL",
                "issue": "Users open checkout modal but leave before entering their email.",
                "recommendation": "Trigger low-friction 1-tap Google/GitHub login or reduce form to just email."
            })
        if metrics["leads_captured"] > metrics["completed_purchases"]:
            abandoned_unrecovered = metrics["leads_captured"] - metrics["completed_purchases"]
            leakages.append({
                "stage": "Lead Captured -> Completed Purchase",
                "severity": "CRITICAL",
                "issue": f"{abandoned_unrecovered} abandoned leads left in checkout modal without purchasing.",
                "recommendation": "Fire automatic 15% discount recovery email/WhatsApp sequence within 5 minutes."
            })

        return {
            "success": True,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "health_score": "OPTIMIZED" if not leakages else "NEEDS_ATTENTION",
            "leakages_identified": leakages,
            "metrics_summary": metrics
        }


revenue_engine = RevenueEngine()
