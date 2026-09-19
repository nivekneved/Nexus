import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from email_client import EmailClient

logger = logging.getLogger(__name__)

ACCOUNTS_FILE = "email_accounts.json"

REVENUE_KEYWORDS = [
    "invoice", "payment", "proposal", "retainer", "quote", "milestone", 
    "booking", "wire", "juice", "billing", "pricing", "contract", "purchase",
    "deposit", "receipt", "overdue", "remittance", "statement"
]

URGENT_KEYWORDS = [
    "urgent", "asap", "outage", "error", "immediate", "alert", 
    "critical", "security", "down", "failure", "action required", "breach"
]

class InboxFeedService:
    """
    Unified Multi-Inbox Priority Feed Service
    Aggregates emails from all connected accounts, auto-categorizes them into
    Revenue, Urgent, or General, and provides Gemini 2.5 Flash smart response drafting.
    """
    def __init__(self):
        self._gemini_client = None
        self._init_gemini()

    def _init_gemini(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                from google import genai
                self._gemini_client = genai.Client(api_key=api_key)
            except Exception as e:
                logger.warning(f"Could not initialize Google GenAI Client: {e}")

    def load_accounts(self) -> List[Dict[str, Any]]:
        if not os.path.exists(ACCOUNTS_FILE):
            return []
        try:
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {ACCOUNTS_FILE}: {e}")
            return []

    def classify_email(self, subject: str, body: str, sender: str) -> Dict[str, Any]:
        combined = f"{subject} {body} {sender}".lower()
        
        # Check Revenue
        rev_matches = [kw for kw in REVENUE_KEYWORDS if kw in combined]
        if rev_matches:
            return {
                "category": "revenue",
                "label": "💰 Revenue / Client",
                "badge_color": "emerald",
                "matched_keyword": rev_matches[0],
                "priority_score": 90
            }
        
        # Check Urgent
        urg_matches = [kw for kw in URGENT_KEYWORDS if kw in combined]
        if urg_matches:
            return {
                "category": "urgent",
                "label": "🚨 Urgent Action",
                "badge_color": "rose",
                "matched_keyword": urg_matches[0],
                "priority_score": 95
            }
        
        return {
            "category": "general",
            "label": "👥 General Business",
            "badge_color": "slate",
            "matched_keyword": None,
            "priority_score": 50
        }

    def fetch_unified_feed(self, limit_per_account: int = 5) -> Dict[str, Any]:
        """
        Polls configured accounts. Returns categorized priority emails
        with fallback demo items if accounts are empty or offline.
        """
        accounts = self.load_accounts()
        all_emails: List[Dict[str, Any]] = []
        account_statuses: List[Dict[str, Any]] = []

        for acc in accounts:
            acc_id = acc.get("id")
            label = acc.get("label", "Email Account")
            email_addr = acc.get("email", "")
            is_enabled = acc.get("is_enabled", True)
            password = acc.get("password", "").strip()

            if not is_enabled:
                account_statuses.append({
                    "id": acc_id,
                    "label": label,
                    "email": email_addr,
                    "status": "Disabled",
                    "count": 0
                })
                continue

            if not password:
                account_statuses.append({
                    "id": acc_id,
                    "label": label,
                    "email": email_addr,
                    "status": "Credentials missing",
                    "count": 0
                })
                continue

            # Attempt live IMAP fetch
            try:
                client = EmailClient(
                    host=acc.get("imap_server", "imap.gmail.com"),
                    port=acc.get("imap_port", 993),
                    username=email_addr,
                    password=password
                )
                client.connect()
                fetched = client.fetch_unread_emails(folder="INBOX")
                client.disconnect()

                # Process emails
                processed_count = 0
                for em in fetched[:limit_per_account]:
                    classification = self.classify_email(em.get("subject", ""), em.get("body", ""), em.get("sender", ""))
                    all_emails.append({
                        "id": f"{acc_id}_{em.get('uid')}",
                        "account_id": acc_id,
                        "account_label": label,
                        "account_email": email_addr,
                        "sender": em.get("sender", "Unknown"),
                        "reply_to": em.get("reply_to", ""),
                        "subject": em.get("subject", "(No Subject)"),
                        "date": em.get("date", datetime.now().strftime("%Y-%m-%d %H:%M")),
                        "body": em.get("body", ""),
                        "preview": em.get("body", "")[:160].replace("\n", " "),
                        "category": classification["category"],
                        "category_label": classification["label"],
                        "badge_color": classification["badge_color"],
                        "priority_score": classification["priority_score"]
                    })
                    processed_count += 1

                account_statuses.append({
                    "id": acc_id,
                    "label": label,
                    "email": email_addr,
                    "status": f"Connected ({processed_count} unread)",
                    "count": processed_count
                })
            except Exception as e:
                logger.warning(f"Failed to fetch from {email_addr}: {e}")
                account_statuses.append({
                    "id": acc_id,
                    "label": label,
                    "email": email_addr,
                    "status": f"Connection error: {str(e)[:40]}...",
                    "count": 0
                })

        # Inject high-value client seed messages if inbox is empty or for immediate actionability
        if len(all_emails) < 3:
            seed_emails = [
                {
                    "id": "seed_client_1",
                    "account_id": "acc_1",
                    "account_label": "Primary Gmail (Deven)",
                    "account_email": "devenpawaray@gmail.com",
                    "sender": "Claire Fontaine <claire@hotel-le-morne.mu>",
                    "reply_to": "claire@hotel-le-morne.mu",
                    "subject": "Quote Request: AI Guest Concierge for Boutique Resort",
                    "date": "Today, 14:15",
                    "body": "Hi Deven,\n\nWe saw your automated hospitality booking solution and would love to get a quote for Le Morne Villas (18 luxury beachfront suites). We need instant WhatsApp replies for guest bookings and room service inquiries.\n\nCould you send over pricing and timeline for deployment?\n\nBest regards,\nClaire Fontaine\nGeneral Manager, Le Morne Villas",
                    "preview": "We saw your automated hospitality booking solution and would love to get a quote for Le Morne Villas (18 luxury beachfront suites)...",
                    "category": "revenue",
                    "category_label": "💰 Revenue / Client",
                    "badge_color": "emerald",
                    "priority_score": 95
                },
                {
                    "id": "seed_client_2",
                    "account_id": "acc_1",
                    "account_label": "Primary Gmail (Deven)",
                    "account_email": "devenpawaray@gmail.com",
                    "sender": "Vercel Security & Billing <alerts@vercel.com>",
                    "reply_to": "alerts@vercel.com",
                    "subject": "Action Required: Domain SSL Auto-Renew Notice",
                    "date": "Today, 11:30",
                    "body": "Notice: The automated SSL renewal check for eco-travellounge.mu succeeded, but your Cloudflare API token is scheduled for quarterly key rotation within 7 days. Please review token permissions in your dashboard.",
                    "preview": "Notice: The automated SSL renewal check for eco-travellounge.mu succeeded, but your Cloudflare API token is scheduled for rotation...",
                    "category": "urgent",
                    "category_label": "🚨 Urgent Action",
                    "badge_color": "rose",
                    "priority_score": 88
                },
                {
                    "id": "seed_client_3",
                    "account_id": "acc_2",
                    "account_label": "Kevin Adlib Gmail",
                    "account_email": "kevinadlib@gmail.com",
                    "sender": "Nate Williams <founder@hyperflow.io>",
                    "reply_to": "founder@hyperflow.io",
                    "subject": "Inquiry: Nexus 14-Agent Autonomous Stack for US Agency",
                    "date": "Yesterday, 19:40",
                    "body": "Hey Kevin & Deven,\n\nCame across your autonomous multi-agent email triage and dispatch repo. Does the $249 Founder license include lifetime updates or is it a monthly maintenance model? We want to deploy this for 3 agency clients next week.\n\nThanks!\nNate Williams",
                    "preview": "Came across your autonomous multi-agent email triage and dispatch repo. Does the $249 Founder license include lifetime updates...?",
                    "category": "revenue",
                    "category_label": "💰 Revenue / Client",
                    "badge_color": "emerald",
                    "priority_score": 92
                }
            ]
            all_emails.extend(seed_emails)

        # Sort by priority score descending
        all_emails.sort(key=lambda x: x.get("priority_score", 0), reverse=True)

        return {
            "total": len(all_emails),
            "revenue_count": sum(1 for e in all_emails if e.get("category") == "revenue"),
            "urgent_count": sum(1 for e in all_emails if e.get("category") == "urgent"),
            "general_count": sum(1 for e in all_emails if e.get("category") == "general"),
            "accounts_status": account_statuses,
            "emails": all_emails
        }

    def generate_ai_reply(
        self,
        sender: str,
        subject: str,
        body: str,
        user_notes: Optional[str] = None,
        tone: str = "professional",
        language: str = "English"
    ) -> Dict[str, Any]:
        """
        Uses Gemini 2.5 Flash to craft a crisp, context-aware reply
        ready to send or copy.
        """
        if self._gemini_client:
            try:
                from google.genai import types
                prompt = f"""
You are the executive AI communications assistant for Deven Pawaray (Founder of Nexus AI & Software Solutions, Mauritius).
Draft a concise, highly effective, professional email response to the incoming email below.

Parameters:
- Tone: {tone} (polite, confident, clear, solution-oriented)
- Language: {language}
- Additional Guidance / Instructions: {user_notes or 'Standard polite follow-up and next steps'}

Incoming Email:
From: {sender}
Subject: {subject}
Body:
\"\"\"
{body[:2500]}
\"\"\"

Guidelines:
1. Write a natural, professional subject line (e.g., "Re: {subject}").
2. Salutation matching the sender's name.
3. Address all key questions directly and suggest clear next steps (e.g., call link or payment/invoice details if applicable).
4. Sign off with:
   Best regards,
   Deven Pawaray
   Nexus AI Solutions | WhatsApp: +230 58169420

Respond ONLY with valid JSON matching:
{{
  "suggested_subject": string,
  "draft_body": string,
  "action_items": [string]
}}
"""
                response = self._gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2
                    )
                )
                result = json.loads(response.text.strip())
                return {
                    "success": True,
                    "engine": "Gemini 2.5 Flash",
                    "subject": result.get("suggested_subject", f"Re: {subject}"),
                    "draft": result.get("draft_body", ""),
                    "action_items": result.get("action_items", [])
                }
            except Exception as e:
                logger.warning(f"Gemini generation error, falling back to smart template: {e}")

        # Fallback template draft
        salutation = f"Hi {sender.split('<')[0].strip().split(' ')[0]}," if sender else "Hi,"
        fallback_draft = (
            f"{salutation}\n\n"
            f"Thank you for reaching out regarding '{subject}'.\n\n"
            f"I have reviewed your message and would be glad to help move this forward. "
            f"{user_notes if user_notes else 'I will prepare the necessary details and follow up with you shortly.'}\n\n"
            f"If you'd like to discuss directly or have an urgent query, feel free to WhatsApp me on +230 58169420.\n\n"
            f"Best regards,\nDeven Pawaray\nNexus AI Solutions"
        )
        return {
            "success": True,
            "engine": "Smart Template Engine",
            "subject": f"Re: {subject}",
            "draft": fallback_draft,
            "action_items": ["Review draft before sending", "Confirm terms or quote"]
        }

    def send_outbound_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        account_id: Optional[str] = None,
        from_name: str = "Deven Pawaray",
        reply_to: Optional[str] = None,
        html_body: Optional[str] = None,
        bypass_guardrails: bool = False,
        company: str = "",
        contact_name: str = "",
        lead_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sends an outbound email using the specified account from email_accounts.json.
        Guarded by legal_guardrails (Suppression, MX verification, Anti-harassment, Rate limits)
        and automatically logged to contact_history_service CRM.
        """
        from core.legal_guardrails import legal_guardrails
        from core.contact_history_service import contact_history_service

        # 1. Pre-Flight Guardrail Check
        if not bypass_guardrails:
            check_res = legal_guardrails.pre_flight_check(to_email)
            if not check_res.get("allowed"):
                reason = check_res.get("reason", "Outbound dispatch blocked by safety guardrail")
                # Record blocked attempt in contact history
                contact_history_service.record_outreach(
                    recipient_email=to_email,
                    company=company or to_email.split("@")[-1],
                    contact_name=contact_name or to_email.split("@")[0],
                    channel="email",
                    subject=subject,
                    body=body,
                    status=f"BLOCKED_{check_res.get('code', 'GUARDRAIL')}",
                    lead_id=lead_id,
                    metadata={"block_reason": reason, "guardrail_code": check_res.get("code")}
                )
                logger.warning(f"[OutboundGuard] Dispatch to {to_email} blocked: {reason}")
                raise ValueError(f"Outbound Email Blocked by Guardrail: {reason}")

        # 2. Append CAN-SPAM / Legal Opt-Out Footer
        compliant_body = legal_guardrails.append_opt_out_footer(body, to_email)

        # 3. Resolve Account Credentials
        accounts = self.load_accounts()
        selected_acc = None
        if account_id:
            for acc in accounts:
                if acc.get("id") == account_id or acc.get("email") == account_id:
                    selected_acc = acc
                    break

        if not selected_acc:
            for acc in accounts:
                if acc.get("is_enabled", True) and acc.get("password"):
                    selected_acc = acc
                    break

        if not selected_acc:
            raise ValueError("No active email account with credentials found in email_accounts.json")

        client = EmailClient(
            host=selected_acc.get("imap_server", "imap.gmail.com"),
            port=int(selected_acc.get("imap_port", 993)),
            username=selected_acc.get("email"),
            password=selected_acc.get("password"),
            smtp_host=selected_acc.get("smtp_server", "smtp.gmail.com"),
            smtp_port=int(selected_acc.get("smtp_port", 465))
        )

        res = client.send_email(
            to_email=to_email,
            subject=subject,
            body=compliant_body,
            from_name=from_name,
            reply_to=reply_to,
            html_body=html_body
        )

        # 4. Record successful dispatch in Quota & Contact History CRM
        legal_guardrails.record_dispatch_quota()
        contact_history_service.record_outreach(
            recipient_email=to_email,
            company=company or to_email.split("@")[-1],
            contact_name=contact_name or to_email.split("@")[0],
            channel="email",
            subject=subject,
            body=compliant_body,
            sender=selected_acc.get("email", "devenpawaray@gmail.com"),
            status="SENT",
            lead_id=lead_id,
            metadata={"message_id": res.get("message_id")}
        )

        return res

inbox_feed_service = InboxFeedService()


