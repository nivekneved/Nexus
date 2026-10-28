import os
import time
import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import re

# Load config from your .env
from dotenv import load_dotenv
load_dotenv(r"C:\Users\deven\OneDrive\Desktop\Agents\.env")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", 993))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None

def get_text_from_email(msg):
    text = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    text = part.get_payload(decode=True).decode()
                except:
                    pass
    else:
        try:
            text = msg.get_payload(decode=True).decode()
        except:
            pass
    return text

def analyze_and_draft_reply(sender_email, subject, body):
    if not model:
        print("  [-] No Gemini API Key. Cannot generate AI reply.")
        return None

    prompt = f"""
You are Kingsley Vance Maurya, Director of Operations at Nexus AI Solutions in Mauritius.
You recently sent a cold email to this prospect offering a lifetime license for an autonomous AI workforce (14 agents) instead of a SaaS subscription, including a $1.00 USD PayPal test link.

The prospect replied.
Sender: {sender_email}
Subject: {subject}
Message Body:
{body}

Analyze their reply.
1. If it's a hard NO, unsubscribe, or bounce -> do not reply.
2. If it's a question, positive, or asking for a meeting -> draft a sharp, authoritative, and polite response answering them. Push for a 5-minute WhatsApp call or direct them back to the $1 link to test it out instantly.
3. Keep the tone elite, direct, and slightly British-corporate.
4. Sign off as:
Best,
Kingsley Vance Maurya
Director of Operations | Nexus AI Solutions
WhatsApp: +230 58169420

Respond ONLY with a valid JSON object in this exact format, nothing else:
{{
    "should_reply": true/false,
    "reply_subject": "Re: ...",
    "reply_body": "..."
}}
"""
    try:
        response = model.generate_content(prompt)
        raw_json = response.text.strip()
        # Clean markdown code blocks if Gemini added them
        if raw_json.startswith('```json'):
            raw_json = raw_json[7:-3]
        elif raw_json.startswith('```'):
            raw_json = raw_json[3:-3]

        data = json.loads(raw_json)
        return data
    except Exception as e:
        print(f"  [-] AI Generation Error: {e}")
        return None

def send_reply(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = f"Kingsley Vance Maurya <{EMAIL_USER}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"  [-] SMTP ERROR for {to_email}: {e}")
        return False

def check_inbox():
    print(f"\n[Nexus Inbound Handler] Connecting to {EMAIL_USER}...")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_USER, EMAIL_PASSWORD)
        mail.select("inbox")

        # Search for UNSEEN emails
        status, messages = mail.search(None, 'UNSEEN')
        if status != "OK":
            print("  [-] Failed to search inbox.")
            return

        email_ids = messages[0].split()
        if not email_ids:
            print("  [✓] Inbox is clear. No new replies.")
            return

        print(f"  [!] Found {len(email_ids)} unread email(s). Processing...")

        for e_id in email_ids:
            res, msg_data = mail.fetch(e_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        try:
                            subject = subject.decode(encoding if encoding else 'utf-8')
                        except:
                            subject = str(subject)

                    sender = msg.get("From")
                    # Extract email address between < >
                    sender_email = re.findall(r'<([^>]+)>', sender)
                    sender_email = sender_email[0] if sender_email else sender

                    body = get_text_from_email(msg)

                    # Ignore automated daemon/bounce emails
                    if "mailer-daemon" in sender_email.lower() or "noreply" in sender_email.lower() or "postmaster" in sender_email.lower():
                        print(f"  [~] Ignoring bounce/automated email from {sender_email}")
                        continue

                    print(f"\n  ► Inbound Reply from: {sender_email}")
                    print(f"  ► Subject: {subject}")

                    # Pass to AI
                    ai_decision = analyze_and_draft_reply(sender_email, subject, body)

                    if ai_decision and ai_decision.get("should_reply"):
                        print(f"  [+] AI Decision: REPLY (Drafting negotiation...)")
                        reply_subj = ai_decision.get("reply_subject")
                        reply_body = ai_decision.get("reply_body")

                        success = send_reply(sender_email, reply_subj, reply_body)
                        if success:
                            print(f"  [+] SUCCESS: AI Negotiation sent to {sender_email}")
                    else:
                        print(f"  [-] AI Decision: DO NOT REPLY (Negative/Not interested).")

            # Mark as read/seen is done automatically by fetching, but we ensure it's processed

        mail.close()
        mail.logout()

    except Exception as e:
        print(f"[-] IMAP Connection Error: {e}")

if __name__ == "__main__":
    print("="*70)
    print("🛡️ NEXUS AUTONOMOUS INBOUND REPLY HANDLER (Kingsley Persona)")
    print("="*70)

    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("[-] ERROR: EMAIL credentials not found in .env")
        exit()

    while True:
        check_inbox()
        print("[Nexus] Sleeping for 60 seconds before next inbox poll...")
        time.sleep(60)
