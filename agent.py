import os
import sys
import json
import logging
import argparse
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Force UTF-8 on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from email_client import EmailClient
from spam_classifier import SpamClassifier

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("email_agent.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("EmailAgent")
console = Console(force_terminal=True, legacy_windows=False)

LEDGER_FILE = "trash_ledger.json"
REPORT_FILE = "daily_report.md"

class EmailSpamAgent:
    """
    Enterprise Email Hygiene Agent:
    - Feature 1: Immunity Shield (OTPs, Security, VIP)
    - Feature 2: Two-Tier Action (Direct Trash vs. AI-Review Folder)
    - Feature 3: Brand Spoofing & Phishing Detection
    - Feature 4: Unsubscribe Header Extractor
    - Feature 5: Daily Audit Digest (daily_report.md)
    - Feature 6: Instant Blacklist Filter
    - Feature 7: Undo & Restore Safety Ledger (trash_ledger.json)
    """
    def __init__(self):
        load_dotenv()
        
        self.imap_server = os.getenv("IMAP_SERVER", "imap.gmail.com")
        self.imap_port = int(os.getenv("IMAP_PORT", 993))
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.trash_folder = os.getenv("TRASH_FOLDER", "[Gmail]/Trash")
        self.review_folder = os.getenv("REVIEW_FOLDER", "[Gmail]/Spam")
        self.dry_run = os.getenv("DRY_RUN", "True").lower() in ("true", "1", "yes")
        
        # Two-Tier Thresholds
        self.high_threshold = float(os.getenv("HIGH_SPAM_THRESHOLD", 0.90))
        self.medium_threshold = float(os.getenv("MEDIUM_SPAM_THRESHOLD", 0.70))

        if not self.email_user or not self.email_password:
            console.print("[bold red][!] Missing EMAIL_USER or EMAIL_PASSWORD in .env file![/bold red]")

        self.classifier = SpamClassifier()

    def run_cycle(self):
        """Executes a single check-and-clean cycle across all 7 features."""
        dry_run_color = "green" if self.dry_run else "red"
        console.print(Panel.fit(
            f"[bold cyan]AI Email Hygiene Agent Active[/bold cyan]\n"
            f"Account: [yellow]{self.email_user}[/yellow] | Dry Run: [{dry_run_color}]{self.dry_run}[/{dry_run_color}]\n"
            f"High Spam Threshold: [red]{self.high_threshold * 100:.0f}%[/red] (Trash) | Review Threshold: [yellow]{self.medium_threshold * 100:.0f}%[/yellow] (Quarantine)",
            title="7-Feature Email Triage System"
        ))

        client = EmailClient(
            host=self.imap_server,
            port=self.imap_port,
            username=self.email_user,
            password=self.email_password,
            trash_folder=self.trash_folder,
            review_folder=self.review_folder
        )

        try:
            client.connect()
            unread_emails = client.fetch_unread_emails("INBOX")

            if not unread_emails:
                console.print("[green][OK] Inbox clean! No unread emails to process.[/green]\n")
                return

            table = Table(title="Email Triage Summary", show_lines=True)
            table.add_column("From", style="cyan", no_wrap=False)
            table.add_column("Subject", style="white")
            table.add_column("Verdict", justify="center")
            table.add_column("Confidence", justify="right")
            table.add_column("Action Taken", style="bold")

            trashed_count = 0
            reviewed_count = 0
            kept_count = 0
            cycle_records = []

            for mail in unread_emails:
                sender = mail["sender"]
                subject = mail["subject"]
                body = mail["body"]
                uid = mail["uid"]
                unsub = mail.get("unsubscribe_link", "")

                # Run through 4-stage classifier
                verdict = self.classifier.classify(sender=sender, subject=subject, body=body)

                is_spam = verdict.get("is_spam", False)
                confidence = verdict.get("confidence", 0.0)
                category = verdict.get("category", "General")
                reason = verdict.get("reason", "")
                is_immune = verdict.get("immune", False)

                action_taken = "KEPT IN INBOX"
                target_folder = None

                # Decision Matrix
                if is_immune or not is_spam:
                    # Feature 1: Immunity Shield / Legitimate
                    kept_count += 1
                    status_text = "[green]PROTECTED[/green]" if is_immune else "[green]HAM[/green]"
                    table.add_row(
                        sender[:28],
                        subject[:35],
                        f"{status_text}\n({category})",
                        f"{confidence * 100:.0f}%",
                        "[green]KEPT IN INBOX[/green]"
                    )
                elif confidence >= self.high_threshold:
                    # High confidence -> Trash
                    trashed_count += 1
                    target_folder = self.trash_folder
                    action_desc = "[red]MOVED TO TRASH[/red]" if not self.dry_run else "[yellow]WOULD TRASH (DRY RUN)[/yellow]"
                    client.move_to_folder(uid, self.trash_folder, dry_run=self.dry_run)
                    action_taken = "TRASH"
                    table.add_row(
                        sender[:28],
                        subject[:35],
                        f"[red]HIGH SPAM[/red]\n({category})",
                        f"{confidence * 100:.0f}%",
                        action_desc
                    )
                    self._record_in_ledger(uid, sender, subject, category, reason, "TRASH", self.trash_folder)
                elif confidence >= self.medium_threshold:
                    # Medium confidence -> Review Folder (Two-Tier)
                    reviewed_count += 1
                    target_folder = self.review_folder
                    action_desc = "[yellow]MOVED TO REVIEW[/yellow]" if not self.dry_run else "[yellow]WOULD REVIEW (DRY RUN)[/yellow]"
                    client.move_to_folder(uid, self.review_folder, dry_run=self.dry_run)
                    action_taken = "REVIEW"
                    table.add_row(
                        sender[:28],
                        subject[:35],
                        f"[yellow]REVIEW JUNK[/yellow]\n({category})",
                        f"{confidence * 100:.0f}%",
                        action_desc
                    )
                    self._record_in_ledger(uid, sender, subject, category, reason, "REVIEW", self.review_folder)
                else:
                    # Low confidence -> Keep safely
                    kept_count += 1
                    table.add_row(
                        sender[:28],
                        subject[:35],
                        f"[green]HAM[/green]\n({category})",
                        f"{confidence * 100:.0f}%",
                        "[green]KEPT IN INBOX[/green]"
                    )

                cycle_records.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "sender": sender,
                    "subject": subject,
                    "category": category,
                    "confidence": f"{confidence * 100:.0f}%",
                    "action": action_taken,
                    "reason": reason,
                    "unsubscribe_link": unsub
                })

            console.print(table)
            console.print(f"\n[bold]Cycle Complete:[/bold] [red]{trashed_count} Trashed[/red], [yellow]{reviewed_count} Quarantined for Review[/yellow], [green]{kept_count} Kept[/green].\n")

            # Feature 5: Update Daily Report
            self._update_daily_report(cycle_records, trashed_count, reviewed_count, kept_count)

        except Exception as e:
            console.print(f"[bold red]Error during cycle:[/bold red] {e}")
        finally:
            client.disconnect()

    def _record_in_ledger(self, uid: str, sender: str, subject: str, category: str, reason: str, action: str, folder: str):
        """Feature 7: Appends trashed/reviewed email to persistent JSON ledger for Undo/Restore."""
        ledger = []
        if os.path.exists(LEDGER_FILE):
            try:
                with open(LEDGER_FILE, "r", encoding="utf-8") as f:
                    ledger = json.load(f)
            except Exception:
                ledger = []

        ledger.append({
            "uid": uid,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sender": sender,
            "subject": subject,
            "category": category,
            "reason": reason,
            "action": action,
            "original_folder": folder
        })

        with open(LEDGER_FILE, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2, ensure_ascii=False)

    def _update_daily_report(self, records: list, trashed: int, reviewed: int, kept: int):
        """Feature 5: Updates daily audit report markdown document."""
        today = datetime.now().strftime("%Y-%m-%d")
        header = f"# Email Triage Audit Digest ({today})\n\n"
        
        content = f"### Summary Stats for {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"- **Trashed (High Risk)**: {trashed}\n"
        content += f"- **Quarantined (Review)**: {reviewed}\n"
        content += f"- **Kept (Legitimate/Protected)**: {kept}\n\n"
        
        content += "| Time | From | Subject | Category | Action | Unsubscribe Link |\n"
        content += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        for r in records:
            unsub_display = f"[Unsubscribe]({r['unsubscribe_link']})" if r['unsubscribe_link'] else "None"
            content += f"| {r['timestamp']} | `{r['sender'][:25]}` | {r['subject'][:30]} | {r['category']} | **{r['action']}** | {unsub_display} |\n"
        content += "\n---\n\n"

        if not os.path.exists(REPORT_FILE):
            with open(REPORT_FILE, "w", encoding="utf-8") as f:
                f.write(header + content)
        else:
            with open(REPORT_FILE, "a", encoding="utf-8") as f:
                f.write(content)

    def list_trashed(self):
        """Feature 7: Lists all items in the recovery ledger."""
        if not os.path.exists(LEDGER_FILE):
            console.print("[yellow]No items in recovery ledger yet.[/yellow]")
            return

        with open(LEDGER_FILE, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        table = Table(title="Undo / Recovery Ledger", show_lines=True)
        table.add_column("UID", style="cyan")
        table.add_column("Date", style="dim")
        table.add_column("From", style="yellow")
        table.add_column("Subject", style="white")
        table.add_column("Action", style="bold red")

        for item in ledger[-20:]:  # Show last 20 items
            table.add_row(item["uid"], item["timestamp"], item["sender"][:25], item["subject"][:35], item["action"])

        console.print(table)
        console.print("[dim]To restore an email back to Inbox, run: [bold]python agent.py --restore <UID>[/bold][/dim]\n")

    def restore_email(self, uid: str):
        """Feature 7: Restores an email from Trash/Review back to Inbox."""
        if not os.path.exists(LEDGER_FILE):
            console.print("[red]No recovery ledger found.[/red]")
            return

        with open(LEDGER_FILE, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        target = next((item for item in ledger if item["uid"] == str(uid)), None)
        if not target:
            console.print(f"[red]UID {uid} not found in ledger.[/red]")
            return

        client = EmailClient(
            host=self.imap_server,
            port=self.imap_port,
            username=self.email_user,
            password=self.email_password
        )
        client.connect()
        try:
            success = client.restore_email(uid=uid, from_folder=target["original_folder"], to_folder="INBOX")
            if success:
                console.print(f"[bold green]Successfully restored '{target['subject']}' (UID: {uid}) back to INBOX![/bold green]")
            else:
                console.print(f"[bold red]Failed to restore UID {uid}. It may have been permanently purged.[/bold red]")
        finally:
            client.disconnect()

def main():
    parser = argparse.ArgumentParser(description="AI Email Spam & Hygiene Agent")
    parser.add_argument("--list-trashed", action="store_true", help="List all emails in the recovery ledger")
    parser.add_argument("--restore", type=str, help="Restore an email UID back to INBOX")
    args = parser.parse_args()

    agent = EmailSpamAgent()

    if args.list_trashed:
        agent.list_trashed()
    elif args.restore:
        agent.restore_email(args.restore)
    else:
        agent.run_cycle()

if __name__ == "__main__":
    main()
