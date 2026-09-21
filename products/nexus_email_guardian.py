"""
Nexus™ Email Guardian (Micro-Edition)
=====================================
A lightweight, self-hosted Python script to clean marketing noise and protect 2FA verification codes.
Runs locally on your machine with zero monthly subscriptions.

Usage:
  1. Set your Gmail / Outlook email and App Password below.
  2. Run: python nexus_email_guardian.py
"""

import imaplib
import email
from email.header import decode_header
import sys

# === CONFIGURATION ===
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
EMAIL_ACCOUNT = "your_email@gmail.com"
APP_PASSWORD = "your_16_digit_app_password"

# Folders & Filters
TRASH_FOLDER = "[Gmail]/Bin"  # Or "[Gmail]/Trash"
PROTECTED_KEYWORDS = ["verification", "security code", "otp", "invoice", "receipt", "2fa"]
SPAM_TLDS = [".xyz", ".top", ".buzz", ".loan", ".click"]

def decode_mime(header_val):
    if not header_val:
        return ""
    decoded_parts = decode_header(header_val)
    text = ""
    for part, enc in decoded_parts:
        if isinstance(part, bytes):
            text += part.decode(enc or "utf-8", errors="replace")
        else:
            text += str(part)
    return text

def run_guardian():
    print("🛡️ Nexus Email Guardian starting...")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
        print("✓ Connected securely to IMAP server.")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    mail.select("INBOX")
    status, messages = mail.search(None, "UNSEEN")
    if status != "OK" or not messages[0]:
        print("✓ Inbox is clear. No unread emails.")
        mail.logout()
        return

    uids = messages[0].split()
    print(f"🔎 Found {len(uids)} unread email(s). Analyzing...")

    for uid in uids:
        res, data = mail.fetch(uid, "(RFC822)")
        if res != "OK":
            continue
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        subject = decode_mime(msg.get("Subject", ""))
        sender = decode_mime(msg.get("From", ""))

        # 1. Check for 2FA / OTP Immunity
        is_immune = any(k in subject.lower() or k in sender.lower() for k in PROTECTED_KEYWORDS)
        if is_immune:
            print(f"  🔒 PROTECTED (2FA/Invoice): {subject[:50]} (From: {sender[:30]})")
            continue

        # 2. Check for spam TLDs
        is_spam = any(tld in sender.lower() for tld in SPAM_TLDS)
        if is_spam:
            print(f"  🗑️ SPAM TRASHED: {subject[:50]} (From: {sender[:30]})")
            mail.copy(uid, TRASH_FOLDER)
            mail.store(uid, "+FLAGS", "\\Deleted")
        else:
            print(f"  ✉️ REGULAR MAIL: {subject[:50]}")

    mail.expunge()
    mail.logout()
    print("🛡️ Sweep complete. Your inbox is clean and protected.")

if __name__ == "__main__":
    run_guardian()
