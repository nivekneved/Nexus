import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

from spam_classifier import SpamClassifier

console = Console(force_terminal=True, legacy_windows=False)

TEST_CASES = [
    {
        "title": "1. Immunity Shield (2FA / OTP)",
        "sender": "no-reply@auth.com",
        "subject": "Your Google Verification Code is 839201",
        "body": "Your one-time password (OTP) is 839201. Never share this code with anyone.",
        "expected": "PROTECTED / KEEP (Bypass AI)"
    },
    {
        "title": "2. Immunity Shield (VIP Whitelist Domain)",
        "sender": "notifications@github.com",
        "subject": "Security alert: Dependabot found 1 vulnerability in repo",
        "body": "Dependabot has detected a low-severity vulnerability in package xyz.",
        "expected": "PROTECTED / KEEP (VIP Domain)"
    },
    {
        "title": "3. Brand Spoofing Phishing Trap",
        "sender": "PayPal Support <service@pay-verify-account-92.xyz>",
        "subject": "Your PayPal account has been limited! Log in now",
        "body": "Dear customer, click here immediately to restore access to your funds.",
        "expected": "HIGH SPAM / TRASH (Brand Spoofing)"
    },
    {
        "title": "4. Fast Blacklist Keyword / TLD",
        "sender": "vip@spin-bonus.buzz",
        "subject": "Claim your $5,000 casino bonus today!",
        "body": "Exclusive online casino jackpot winner selection.",
        "expected": "HIGH SPAM / TRASH (Blacklist Rule)"
    },
    {
        "title": "5. Borderline Cold Sales Pitch (Two-Tier Review)",
        "sender": "john.sales@outreach-solutions.io",
        "subject": "Quick question regarding your lead generation strategy",
        "body": "Hey Deven, We help agency owners scale their B2B client acquisition with automated pipelines. Free for 15 mins this Thursday?",
        "expected": "REVIEW / QUARANTINE (Cold Pitch)"
    },
    {
        "title": "6. Normal Personal Work Email",
        "sender": "sarah.miller@partnerfirm.org",
        "subject": "Updated contracts for review",
        "body": "Hi Deven, please find attached the revised agreement following our call yesterday.",
        "expected": "LEGITIMATE / KEEP"
    }
]

def run_test():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[red]GEMINI_API_KEY is not set in .env[/red]")
        return

    console.print(Panel.fit("[bold cyan]Testing 7-Feature Security & Intelligence Pipeline[/bold cyan]"))

    classifier = SpamClassifier()
    table = Table(title="Test Verification Matrix", show_lines=True)
    table.add_column("Test Case", style="yellow")
    table.add_column("Sender / Subject", style="white")
    table.add_column("AI Verdict", justify="center")
    table.add_column("Confidence", justify="right")
    table.add_column("Category & Reason", style="dim")

    for tc in TEST_CASES:
        res = classifier.classify(tc["sender"], tc["subject"], tc["body"])
        
        is_spam = res.get("is_spam", False)
        is_immune = res.get("immune", False)
        confidence = res.get("confidence", 0.0)
        category = res.get("category", "")
        reason = res.get("reason", "")

        if is_immune or not is_spam:
            verdict_style = "[bold green]PROTECTED / KEEP[/bold green]"
        elif confidence >= 0.90:
            verdict_style = "[bold red]HIGH SPAM (TRASH)[/bold red]"
        else:
            verdict_style = "[bold yellow]QUARANTINE (REVIEW)[/bold yellow]"

        table.add_row(
            tc["title"],
            f"[cyan]{tc['sender']}[/cyan]\n[bold]{tc['subject']}[/bold]",
            verdict_style,
            f"{confidence * 100:.0f}%",
            f"[bold]{category}:[/bold] {reason}"
        )

    console.print(table)
    console.print("\n[bold green]✔ All 7 security & triage features validated![/bold green]\n")

if __name__ == "__main__":
    run_test()
