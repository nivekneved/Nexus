import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv, set_key

from core.base_agent import BaseAgent
from core.telemetry import telemetry
from email_client import EmailClient
from spam_classifier import SpamClassifier

LEDGER_FILE = "trash_ledger.json"
REPORT_FILE = "daily_report.md"
ACCOUNTS_FILE = "email_accounts.json"

PROVIDER_PRESETS = {
    "gmail": {
        "imap_server": "imap.gmail.com",
        "imap_port": 993,
        "trash_folder": "[Gmail]/Trash",
        "review_folder": "[Gmail]/Spam"
    },
    "outlook": {
        "imap_server": "outlook.office365.com",
        "imap_port": 993,
        "trash_folder": "Deleted Items",
        "review_folder": "Junk"
    },
    "yahoo": {
        "imap_server": "imap.mail.yahoo.com",
        "imap_port": 993,
        "trash_folder": "Trash",
        "review_folder": "Bulk"
    },
    "icloud": {
        "imap_server": "imap.mail.me.com",
        "imap_port": 993,
        "trash_folder": "Deleted Messages",
        "review_folder": "Junk"
    }
}

class EmailHygieneAgent(BaseAgent):
    """
    Employee #1: Email Hygiene & Anti-Spam Specialist
    - Multi-Account Support: Monitors up to 5 inboxes (Gmail, Outlook, Yahoo, iCloud)
    - 7-Feature Security Pipeline
    - Dynamic Configuration Schema & Inboxes Manager
    - Real-Time Mission Control Telemetry
    """
    def __init__(self):
        load_dotenv(override=True)
        super().__init__(
            agent_id="email_hygiene",
            name="Email Hygiene & Anti-Spam",
            description="Autonomous multi-inbox cleaner (up to 5 Gmail/Outlook/Yahoo accounts). Protects 2FA/VIPs, quarantines clutter, and trashes phishing.",
            icon="mail",
            schedule_minutes=60
        )
        self.classifier = SpamClassifier()
        self.stats = {
            "total_scanned": 0,
            "trashed": 0,
            "quarantined": 0,
            "protected": 0,
            "accounts_configured": 1
        }
        self._register_subagents()
        self._ensure_accounts_initialized()

    def _register_subagents(self):
        """Registers the 5 single-task subagents under Email Hygiene Specialist."""
        from agents.email_hygiene.subagents import (
            EmailImmunitySubAgent,
            EmailSpoofHunterSubAgent,
            EmailBlacklistSubAgent,
            EmailClassifierSubAgent,
            EmailAuditLedgerSubAgent
        )
        self.register_subagent(EmailImmunitySubAgent())
        self.register_subagent(EmailSpoofHunterSubAgent())
        self.register_subagent(EmailBlacklistSubAgent())
        self.register_subagent(EmailClassifierSubAgent())
        self.register_subagent(EmailAuditLedgerSubAgent())

    def _ensure_accounts_initialized(self):
        """Bootstraps email_accounts.json if missing from current .env settings."""
        if not os.path.exists(ACCOUNTS_FILE):
            load_dotenv(override=True)
            email_user = os.getenv("EMAIL_USER", "")
            if email_user:
                initial = [{
                    "id": "acc_1",
                    "label": "Primary Account",
                    "provider": "gmail" if "gmail" in email_user else "custom",
                    "email": email_user,
                    "password": os.getenv("EMAIL_PASSWORD", ""),
                    "imap_server": os.getenv("IMAP_SERVER", "imap.gmail.com"),
                    "imap_port": int(os.getenv("IMAP_PORT", 993)),
                    "trash_folder": os.getenv("TRASH_FOLDER", "[Gmail]/Trash"),
                    "review_folder": os.getenv("REVIEW_FOLDER", "[Gmail]/Spam"),
                    "is_enabled": True,
                    "last_scanned": None,
                    "last_status": "Ready"
                }]
                with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
                    json.dump(initial, f, indent=2)

    def load_accounts(self) -> List[Dict[str, Any]]:
        """Returns the list of configured email accounts (max 5)."""
        if not os.path.exists(ACCOUNTS_FILE):
            self._ensure_accounts_initialized()
        try:
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                accounts = json.load(f)
                return accounts[:5]
        except Exception:
            return []

    def save_accounts(self, accounts: List[Dict[str, Any]]) -> bool:
        """Saves up to 5 email accounts."""
        if len(accounts) > 5:
            raise ValueError("Maximum of 5 email accounts can be monitored simultaneously.")
        with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
            json.dump(accounts[:5], f, indent=2, ensure_ascii=False)
        self.stats["accounts_configured"] = len(accounts)
        return True

    def add_or_update_account(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adds or updates an account, auto-applying provider defaults."""
        accounts = self.load_accounts()
        acc_id = account_data.get("id")

        provider = account_data.get("provider", "gmail").lower()
        defaults = PROVIDER_PRESETS.get(provider, {})

        account_entry = {
            "id": acc_id or f"acc_{int(datetime.now().timestamp()*1000)}",
            "label": account_data.get("label", f"{provider.capitalize()} Inbox"),
            "provider": provider,
            "email": account_data.get("email", "").strip(),
            "password": account_data.get("password", "").strip(),
            "imap_server": account_data.get("imap_server") or defaults.get("imap_server", "imap.gmail.com"),
            "imap_port": int(account_data.get("imap_port") or defaults.get("imap_port", 993)),
            "trash_folder": account_data.get("trash_folder") or defaults.get("trash_folder", "Trash"),
            "review_folder": account_data.get("review_folder") or defaults.get("review_folder", "Junk"),
            "is_enabled": account_data.get("is_enabled", True),
            "last_scanned": None,
            "last_status": "Saved"
        }

        # Check existing
        existing_idx = next((i for i, a in enumerate(accounts) if a["id"] == account_entry["id"]), None)
        if existing_idx is not None:
            # Preserve existing password if not provided in update
            if not account_entry["password"]:
                account_entry["password"] = accounts[existing_idx].get("password", "")
            accounts[existing_idx] = account_entry
        else:
            if len(accounts) >= 5:
                raise ValueError("Maximum limit reached: You can configure up to 5 email accounts.")
            accounts.append(account_entry)

        self.save_accounts(accounts)
        self.log(step="Account Config", file_used=ACCOUNTS_FILE, message=f"Configured account: {account_entry['email']} ({account_entry['label']})", level="SUCCESS")
        return account_entry

    def delete_account(self, account_id: str) -> bool:
        accounts = self.load_accounts()
        filtered = [a for a in accounts if a["id"] != account_id]
        self.save_accounts(filtered)
        self.log(step="Account Removed", file_used=ACCOUNTS_FILE, message=f"Removed account ID {account_id}", level="WARN")
        return True

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "HIGH_SPAM_THRESHOLD",
                "label": "High Spam Threshold (Direct Trash)",
                "type": "number",
                "step": 0.05,
                "default": 0.90,
                "description": "Confidence score >= this value will be moved straight to Trash"
            },
            {
                "key": "MEDIUM_SPAM_THRESHOLD",
                "label": "Quarantine Threshold (Review Folder)",
                "type": "number",
                "step": 0.05,
                "default": 0.70,
                "description": "Confidence score >= this value will be moved to Review"
            },
            {
                "key": "WHITELIST_DOMAINS",
                "label": "Immunity Shield — VIP Whitelist",
                "type": "textarea",
                "description": "Comma-separated domains or emails that bypass AI and are never deleted"
            },
            {
                "key": "BLACKLIST_DOMAINS",
                "label": "Blacklisted TLDs & Domains",
                "type": "textarea",
                "description": "Comma-separated suspicious domains (e.g. .xyz, .top, .buzz)"
            },
            {
                "key": "BLACKLIST_KEYWORDS",
                "label": "Blacklisted Instant Spam Keywords",
                "type": "textarea",
                "description": "Comma-separated trigger words for instant trashing"
            },
            {
                "key": "DRY_RUN",
                "label": "Safe Dry-Run Mode",
                "type": "boolean",
                "default": True,
                "description": "Simulates all operations without actually moving emails"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        load_dotenv(override=True)
        return {
            "HIGH_SPAM_THRESHOLD": float(os.getenv("HIGH_SPAM_THRESHOLD", 0.90)),
            "MEDIUM_SPAM_THRESHOLD": float(os.getenv("MEDIUM_SPAM_THRESHOLD", 0.70)),
            "WHITELIST_DOMAINS": os.getenv("WHITELIST_DOMAINS", "@gmail.com,@github.com,@google.com,@apple.com"),
            "BLACKLIST_DOMAINS": os.getenv("BLACKLIST_DOMAINS", ".xyz,.top,.click,.buzz,.loan"),
            "BLACKLIST_KEYWORDS": os.getenv("BLACKLIST_KEYWORDS", "casino,viagra,lottery winner,inheritance fund"),
            "DRY_RUN": os.getenv("DRY_RUN", "True").lower() in ("true", "1", "yes"),
            "ACCOUNTS_COUNT": len(self.load_accounts())
        }

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        for key, val in new_config.items():
            if key != "ACCOUNTS_COUNT":
                set_key(".env", str(key), str(val))
        load_dotenv(override=True)
        self.classifier = SpamClassifier()
        self.log(step="Config Update", file_used=".env", message="Updated agent global rules in .env", level="SUCCESS")
        return True

    def run_cycle(self) -> Dict[str, Any]:
        """
        Executes a complete triage cycle across all configured active email accounts (up to 5).
        """
        load_dotenv(override=True)
        dry_run = os.getenv("DRY_RUN", "True").lower() in ("true", "1", "yes")
        high_threshold = float(os.getenv("HIGH_SPAM_THRESHOLD", 0.90))
        medium_threshold = float(os.getenv("MEDIUM_SPAM_THRESHOLD", 0.70))

        accounts = self.load_accounts()
        active_accounts = [a for a in accounts if a.get("is_enabled", True)]

        if not active_accounts:
            self.log(step="Halted", file_used=ACCOUNTS_FILE, message="No active email accounts configured. Please add an account in the Accounts panel.", level="WARN")
            return {"total_scanned": 0, "trashed": 0, "quarantined": 0, "kept": 0, "emails": []}

        self.log(
            step="Multi-Inbox Start",
            file_used="agent.py",
            message=f"Starting scan across {len(active_accounts)} active account(s) (Dry-Run: {dry_run})",
            level="INFO"
        )

        overall_emails = []
        cycle_total_scanned = 0
        cycle_trashed = 0
        cycle_quarantined = 0
        cycle_kept = 0

        for idx, acc in enumerate(active_accounts):
            acc_email = acc.get("email")
            acc_label = acc.get("label", f"Account #{idx+1}")
            acc_server = acc.get("imap_server", "imap.gmail.com")
            acc_port = int(acc.get("imap_port", 993))
            acc_pwd = acc.get("password", "")
            trash_f = acc.get("trash_folder", "[Gmail]/Trash")
            review_f = acc.get("review_folder", "[Gmail]/Spam")

            self.log(
                step="Inbox Selection",
                file_used="email_accounts.json",
                message=f"[{idx+1}/{len(active_accounts)}] Connecting to {acc_label} ({acc_email})...",
                level="INFO"
            )

            client = EmailClient(
                host=acc_server,
                port=acc_port,
                username=acc_email,
                password=acc_pwd,
                trash_folder=trash_f,
                review_folder=review_f
            )

            try:
                client.connect()
                acc["last_status"] = "Connected"
                self.log(step="IMAP Auth", file_used="email_client.py", message=f"Authenticated to {acc_email} on {acc_server}", level="SUCCESS")
                
                unread_emails = client.fetch_unread_emails("INBOX")
                self.log(step="Fetch Unread", file_used="email_client.py", message=f"Found {len(unread_emails)} unread in {acc_email}", level="INFO")
                cycle_total_scanned += len(unread_emails)

                for mail in unread_emails:
                    sender = mail["sender"]
                    subject = mail["subject"]
                    body = mail["body"]
                    uid = mail["uid"]
                    unsub = mail.get("unsubscribe_link", "")

                    payload = {"sender": sender, "subject": subject, "body": body}
                    
                    # 1. Immunity Shield SubAgent check
                    immunity_res = self.run_subagent("email_immunity_shield", payload)
                    if immunity_res.get("success") and immunity_res.get("data", {}).get("is_immune"):
                        verdict = {
                            "is_spam": False,
                            "confidence": 0.0,
                            "category": "Immunity Shield",
                            "reason": immunity_res["data"].get("reason", "Immunity Protected"),
                            "immune": True
                        }
                    else:
                        # 2. Spoof Hunter SubAgent check
                        spoof_res = self.run_subagent("email_spoof_hunter", payload)
                        if spoof_res.get("success") and spoof_res.get("data", {}).get("is_spoof"):
                            verdict = {
                                "is_spam": True,
                                "confidence": 0.99,
                                "category": "Brand Spoofing",
                                "reason": spoof_res["data"].get("reason", "Brand Impersonation Phishing"),
                                "immune": False
                            }
                        else:
                            # 3. Blacklist SubAgent check
                            bl_res = self.run_subagent("email_blacklist_killer", payload)
                            if bl_res.get("success") and bl_res.get("data", {}).get("is_blacklisted"):
                                verdict = {
                                    "is_spam": True,
                                    "confidence": 1.0,
                                    "category": "Blacklist Rule",
                                    "reason": bl_res["data"].get("reason", "Spam Rule Matched"),
                                    "immune": False
                                }
                            else:
                                # 4. Gemini Structured Evaluator SubAgent
                                gem_res = self.run_subagent("email_gemini_evaluator", payload)
                                if gem_res.get("success") and "data" in gem_res:
                                    verdict = gem_res["data"]
                                else:
                                    verdict = self.classifier.classify(sender=sender, subject=subject, body=body)

                    is_spam = verdict.get("is_spam", False)
                    confidence = verdict.get("confidence", 0.0)
                    category = verdict.get("category", "General")
                    reason = verdict.get("reason", "")
                    is_immune = verdict.get("immune", False)

                    if is_immune or not is_spam:
                        cycle_kept += 1
                        action = "PROTECTED" if is_immune else "KEPT"
                    elif confidence >= high_threshold:
                        cycle_trashed += 1
                        action = "TRASHED"
                        client.move_to_folder(uid, trash_f, dry_run=dry_run)
                        self._record_in_ledger(uid, sender, subject, category, reason, "TRASH", trash_f, account_email=acc_email)
                    elif confidence >= medium_threshold:
                        cycle_quarantined += 1
                        action = "QUARANTINED"
                        client.move_to_folder(uid, review_f, dry_run=dry_run)
                        self._record_in_ledger(uid, sender, subject, category, reason, "REVIEW", review_f, account_email=acc_email)
                    else:
                        cycle_kept += 1
                        action = "KEPT"

                    overall_emails.append({
                        "account": acc_email,
                        "uid": uid,
                        "sender": sender,
                        "subject": subject,
                        "date": mail.get("date", ""),
                        "verdict": "SPAM" if is_spam else "HAM",
                        "confidence": round(confidence * 100, 1),
                        "category": category,
                        "reason": reason,
                        "action": action,
                        "unsubscribe_link": unsub
                    })

                acc["last_scanned"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            except Exception as e:
                acc["last_status"] = f"Error: {str(e)[:40]}"
                self.log(step="Inbox Error", file_used="email_client.py", message=f"Failed scanning {acc_email}: {str(e)}", level="ERROR")
            finally:
                client.disconnect()

        # Update saved status in accounts file
        self.save_accounts(accounts)

        self.stats["total_scanned"] += cycle_total_scanned
        self.stats["trashed"] += cycle_trashed
        self.stats["quarantined"] += cycle_quarantined
        self.stats["protected"] += cycle_kept
        self.stats["accounts_configured"] = len(accounts)

        self.log(
            step="Multi-Inbox Done",
            file_used="daily_report.md",
            message=f"Completed multi-inbox scan: {cycle_total_scanned} scanned across {len(active_accounts)} accounts. ({cycle_trashed} trashed, {cycle_quarantined} quarantined, {cycle_kept} kept)",
            level="SUCCESS"
        )

        return {
            "total_scanned": cycle_total_scanned,
            "trashed": cycle_trashed,
            "quarantined": cycle_quarantined,
            "kept": cycle_kept,
            "dry_run": dry_run,
            "accounts_scanned": len(active_accounts),
            "emails": overall_emails
        }

    def get_stats(self) -> List[Dict[str, Any]]:
        accounts = self.load_accounts()
        active = sum(1 for a in accounts if a.get("is_enabled", True))
        return [
            {"title": "Inboxes Active", "value": f"{active}/{len(accounts)}", "color": "blue"},
            {"title": "Total Scanned", "value": self.stats["total_scanned"], "color": "blue"},
            {"title": "High Spam (Trash)", "value": self.stats["trashed"], "color": "red"},
            {"title": "Protected & Kept", "value": self.stats["protected"], "color": "green"}
        ]

    def _record_in_ledger(self, uid: str, sender: str, subject: str, category: str, reason: str, action: str, folder: str, account_email: str = ""):
        entry = {
            "uid": uid,
            "account": account_email,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sender": sender,
            "subject": subject,
            "category": category,
            "reason": reason,
            "action": action,
            "original_folder": folder
        }
        res = self.run_subagent("email_audit_ledger", {"entry": entry})
        if not res.get("success"):
            # Fallback direct append if subagent disabled
            ledger = []
            if os.path.exists(LEDGER_FILE):
                try:
                    with open(LEDGER_FILE, "r", encoding="utf-8") as f:
                        ledger = json.load(f)
                except Exception:
                    ledger = []
            ledger.append(entry)
            with open(LEDGER_FILE, "w", encoding="utf-8") as f:
                json.dump(ledger, f, indent=2, ensure_ascii=False)
