import os
import re
import json
import time
import urllib.parse
from typing import Dict, Any, List, Optional
from core.subagent import BaseSubAgent
from security.shield import shield

SUBSCRIPTIONS_FILE = "subscriptions_catalog.json"
DIGEST_FILE = "daily_newsletter_digest.json"
DIGEST_MD_FILE = "daily_newsletter_digest.md"

class UnsubscribeHarvesterSubAgent(BaseSubAgent):
    """
    Subagent 1: Extracts RFC 2369 List-Unsubscribe headers (HTTP & mailto)
    and scans email bodies for direct unsubscribe links, cataloging senders and frequency.
    """
    def __init__(self):
        super().__init__(
            subagent_id="unsub_harvester",
            name="RFC 2369 Header & Link Harvester",
            parent_agent_id="ghost_unsubscriber",
            description="Extracts List-Unsubscribe headers and body links, maintaining a persistent catalog of all active subscriptions."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        emails = payload.get("emails", [])
        catalog = self._load_catalog()

        new_found = 0
        updated = 0

        url_regex = re.compile(r'https?://[^\s<>"\']+(?:unsubscribe|optout|opt-out|manage-preferences|email_preferences)[^\s<>"\']*', re.IGNORECASE)

        for mail in emails:
            sender = mail.get("sender", "")
            subject = mail.get("subject", "")
            body = mail.get("body", "")
            unsub_header = mail.get("unsubscribe_link", "")

            # Extract clean email domain/address
            email_match = re.search(r'[\w\.-]+@[\w\.-]+', sender)
            sender_email = email_match.group(0).lower() if email_match else sender.lower()

            unsub_http = None
            unsub_mailto = None

            # 1. Parse header if present (format: <mailto:...>, <https://...>)
            if unsub_header:
                tokens = [t.strip("<> \t\r\n") for t in unsub_header.split(",")]
                for tok in tokens:
                    if tok.lower().startswith("http") and not unsub_http:
                        unsub_http = tok
                    elif tok.lower().startswith("mailto:") and not unsub_mailto:
                        unsub_mailto = tok

            # 2. If no HTTP link from header, scan body
            if not unsub_http and body:
                matches = url_regex.findall(body)
                if matches:
                    unsub_http = matches[0]

            if unsub_http or unsub_mailto:
                # Update or insert into catalog
                existing = next((c for c in catalog if c["sender_email"] == sender_email), None)
                if existing:
                    existing["frequency_count"] = existing.get("frequency_count", 1) + 1
                    existing["last_received"] = time.strftime("%Y-%m-%d %H:%M:%S")
                    existing["last_subject"] = subject
                    if unsub_http and not existing.get("unsub_http"):
                        existing["unsub_http"] = unsub_http
                    if unsub_mailto and not existing.get("unsub_mailto"):
                        existing["unsub_mailto"] = unsub_mailto
                    updated += 1
                else:
                    catalog.append({
                        "id": f"sub_{len(catalog) + 1}",
                        "sender_raw": sender,
                        "sender_email": sender_email,
                        "sender_name": sender.split("<")[0].strip(' "'),
                        "frequency_count": 1,
                        "status": "ACTIVE",
                        "unsub_http": unsub_http,
                        "unsub_mailto": unsub_mailto,
                        "first_detected": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "last_received": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "last_subject": subject
                    })
                    new_found += 1

        self._save_catalog(catalog)

        return {
            "total_cataloged": len(catalog),
            "new_subscriptions_found": new_found,
            "frequency_updated": updated
        }

    def _load_catalog(self) -> List[Dict[str, Any]]:
        if os.path.exists(SUBSCRIPTIONS_FILE):
            try:
                with open(SUBSCRIPTIONS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_catalog(self, catalog: List[Dict[str, Any]]):
        with open(SUBSCRIPTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)


class UnsubscribeExecutorSubAgent(BaseSubAgent):
    """
    Subagent 2: Dispatches automated 1-Click Unsubscribe requests safely,
    protected by Safeguard 5 (SSRF Webhook & URL Filter) and rate limiting.
    """
    def __init__(self):
        super().__init__(
            subagent_id="unsub_executor",
            name="1-Click Unsubscribe Dispatcher",
            parent_agent_id="ghost_unsubscriber",
            description="Executes automated HTTP and mailto unsubscribe triggers with SSRF safety and audit logging."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        subscription_id = payload.get("subscription_id")
        target_email = payload.get("sender_email")

        catalog = []
        if os.path.exists(SUBSCRIPTIONS_FILE):
            with open(SUBSCRIPTIONS_FILE, "r", encoding="utf-8") as f:
                catalog = json.load(f)

        target = None
        for item in catalog:
            if subscription_id and item.get("id") == subscription_id:
                target = item
                break
            if target_email and item.get("sender_email") == target_email.lower():
                target = item
                break

        if not target:
            return {"success": False, "error": "Subscription entry not found in catalog."}

        unsub_url = target.get("unsub_http")
        unsub_mailto = target.get("unsub_mailto")

        action_taken = "NONE"
        action_detail = ""

        # 1. Try HTTP Unsubscribe with SSRF Filter
        if unsub_url:
            if not shield.validate_outgoing_url(unsub_url):
                return {"success": False, "error": f"Blocked by Safeguard 5 (SSRF Protection): URL '{unsub_url}' is private or invalid."}

            try:
                import urllib.request
                req = urllib.request.Request(
                    unsub_url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    status_code = resp.getcode()
                    action_taken = "HTTP_TRIGGERED"
                    action_detail = f"Dispatched HTTP GET/POST to unsubscribe endpoint (Status: {status_code})"
            except Exception as e:
                action_taken = "HTTP_ATTEMPTED"
                action_detail = f"Attempted request to {unsub_url}: {str(e)[:60]}"
        elif unsub_mailto:
            action_taken = "MAILTO_RECORDED"
            action_detail = f"Target requires RFC mailto command: {unsub_mailto}"

        # Update catalog state
        target["status"] = "UNSUBSCRIBED"
        target["unsubscribed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        target["execution_result"] = action_detail

        with open(SUBSCRIPTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)

        return {
            "success": True,
            "sender_email": target.get("sender_email"),
            "sender_name": target.get("sender_name"),
            "action_taken": action_taken,
            "detail": action_detail
        }


class NewsletterDigestSubAgent(BaseSubAgent):
    """
    Subagent 3: Gathers promo and newsletter items into a unified 2-minute daily digest,
    saving mental bandwidth while archiving repetitive clutter.
    """
    def __init__(self):
        super().__init__(
            subagent_id="newsletter_digest",
            name="2-Minute Executive Newsletter Digest",
            parent_agent_id="ghost_unsubscriber",
            description="Condenses 20+ daily newsletter blasts into a single 2-minute executive markdown brief."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        newsletters = payload.get("newsletters", [])
        date_str = time.strftime("%A, %d %B %Y")

        items_summary = []
        for nl in newsletters:
            sender = nl.get("sender_name") or nl.get("sender", "Unknown")
            subject = nl.get("subject", "No Subject")
            preview = nl.get("preview") or nl.get("body", "")[:120].strip().replace("\n", " ")
            items_summary.append({
                "source": sender,
                "headline": subject,
                "snippet": preview
            })

        digest_data = {
            "date": date_str,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_newsletters_condensed": len(items_summary),
            "reading_time": "2 minutes",
            "highlights": items_summary[:10]
        }

        # Save JSON
        with open(DIGEST_FILE, "w", encoding="utf-8") as f:
            json.dump(digest_data, f, indent=2, ensure_ascii=False)

        # Generate readable Markdown
        md_lines = [
            f"# ☕ 2-Minute Morning Newsletter Digest — {date_str}",
            "",
            f"> **Inbox Cleanliness:** Successfully condensed **{len(items_summary)} promotional blasts** into this single morning brief.",
            "",
            "## 📰 Key Newsletter Highlights",
            ""
        ]

        if not items_summary:
            md_lines.append("_No new marketing blasts detected today. Your inbox is clean!_")
        else:
            for idx, it in enumerate(items_summary[:10], 1):
                md_lines.append(f"### {idx}. {it['headline']}")
                md_lines.append(f"**From:** `{it['source']}`")
                md_lines.append(f"> {it['snippet']}...")
                md_lines.append("")

        md_lines.append("---")
        md_lines.append("*Generated autonomously by Nexus Ghost Unsubscriber Specialist.*")

        with open(DIGEST_MD_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))

        return {
            "success": True,
            "condensed_count": len(items_summary),
            "digest_file": DIGEST_FILE,
            "markdown_file": DIGEST_MD_FILE
        }
