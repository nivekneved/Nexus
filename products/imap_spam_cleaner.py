# -*- coding: utf-8 -*-
# Nexus 1-File Python IMAP Spam Cleaner
import imaplib, os

def clean_spam(user, password, host="imap.gmail.com"):
    print(f"Connecting to {host} as {user}...")
    mail = imaplib.IMAP4_SSL(host, 993)
    mail.login(user, password)
    mail.select("INBOX")
    _, messages = mail.search(None, '(OR SUBJECT "spam" SUBJECT "unsubscribe")')
    uids = messages[0].split()
    print(f"Found {len(uids)} promotional/spam emails to purge.")
    for uid in uids:
        mail.store(uid, '+FLAGS', '\\Deleted')
    mail.expunge()
    mail.logout()
    print("✅ IMAP inbox successfully cleaned!")

if __name__ == "__main__":
    user = os.getenv("EMAIL_USER", "your_email@gmail.com")
    pwd = os.getenv("EMAIL_PASSWORD", "your_app_password")
    clean_spam(user, pwd)
