import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
import json
import urllib.request
from datetime import datetime
import google.generativeai as genai

# Load config from your .env
from dotenv import load_dotenv
load_dotenv(r"C:\Users\deven\OneDrive\Desktop\Agents\.env")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

LEADS_FILE = r"C:\Users\deven\OneDrive\Desktop\Agents\real_leads_output.csv"
STATE_FILE = r"C:\Users\deven\OneDrive\Desktop\Agents\campaign_tracking.json"

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=4)

def scrape_website_context(website):
    """Scrapes the target website for live context to feed the AI."""
    if not website or website.lower() == "n/a" or len(website) < 5:
        return "No website available."

    if not website.startswith('http'):
        website = 'http://' + website

    print(f"  [*] Live Intelligence: Scraping {website}...")
    try:
        req = urllib.request.Request(website, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8', errors='ignore')
            # Very rudimentary tag stripping for context extraction
            import re
            text = re.sub(r'<[^>]+>', ' ', html)
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:1500] # Return first 1500 chars of visible-ish text
    except Exception as e:
        print(f"  [-] Scrape failed: {e}")
        return "Failed to scrape website."

def draft_ai_pitch(name, company, website_context):
    """Uses Gemini Tool-Calling logic to critique and perfect the pitch."""
    if not model:
        return get_fallback_initial_pitch(name, company)

    prompt = f"""
You are Kingsley Vance Maurya, Director of Operations at Nexus AI Solutions.
You are pitching your autonomous AI workforce (which replaces SaaS subscriptions with a one-time $1 lifetime license test).

Target Name: {name}
Target Company: {company}
Company Website Context: {website_context}

Task:
1. Write a 1-sentence hyper-personalized opening hook based on their website context.
2. State the problem: Manual operations, SaaS seat fees, and inbox triage waste 10+ hours a week.
3. State the solution: Nexus Autonomous AI Workforce. No SaaS fees, lifetime license.
4. Call to Action: Provide this exact link to test drive the founder license for $1.00 USD: https://www.paypal.com/ncp/payment/B4SASTZDVFXY4
5. Sign off as:
Best,
Kingsley Vance Maurya
Director of Operations | Nexus AI Solutions
WhatsApp: +230 58169420

CRITIQUE YOURSELF: Ensure it does not sound like generic spam. Make it read like an elite, sharp, peer-to-peer executive email.

Return ONLY a JSON object with:
{{
    "subject": "Strategic AI operations for [Company]",
    "body": "[The full email body]"
}}
"""
    try:
        response = model.generate_content(prompt)
        raw_json = response.text.strip()
        if raw_json.startswith('```json'): raw_json = raw_json[7:-3]
        elif raw_json.startswith('```'): raw_json = raw_json[3:-3]
        data = json.loads(raw_json)
        return data.get("subject"), data.get("body")
    except Exception as e:
        print(f"  [-] AI Generation Error, using fallback. {e}")
        return get_fallback_initial_pitch(name, company)

def get_fallback_initial_pitch(name, company):
    subject = f"Strategic AI operations for {company}"
    body = f"""Hi {name},

I noticed the operations you are running at {company} and wanted to reach out directly.

Many fast-growing teams in your space waste over 10+ hours weekly manually filtering inbox noise, chasing client invoices, and triaging alerts. We've solved this.

I am the architect behind Nexus — an autonomous 14-agent local AI workforce that handles email classification, finance audits, and smart drafting directly on your machines. It's not a SaaS subscription; you own the license.

We are doing a limited local rollout. You can test drive the founder license right now:
💳 Instant Checkout ($1.00 USD Live Test): https://www.paypal.com/ncp/payment/B4SASTZDVFXY4

Would love to show you a quick live teardown of the engine if you have 5 minutes this week.

Best,
Kingsley Vance Maurya
Director of Operations | Nexus AI Solutions
WhatsApp: +230 58169420"""
    return subject, body

def get_followup_pitch(name, company):
    subject = f"Re: Strategic AI operations for {company}"
    body = f"""Hi {name},

Just floating this to the top of your inbox.

We are closing out our initial deployment slots for the Nexus AI workforce this week. If {company} is still dealing with operational bottlenecks and you want to eliminate recurring SaaS seat fees, you can bypass the waitlist and grab the lifetime license test here:
💳 Instant Checkout ($1.00 USD Live Test): https://www.paypal.com/ncp/payment/B4SASTZDVFXY4

Let me know if you have any questions!

Best,
Kingsley Vance Maurya
Director of Operations | Nexus AI Solutions
WhatsApp: +230 58169420"""
    return subject, body

if __name__ == "__main__":
    print("="*70)
    print("🚀 NEXUS ARGON MAX DISPATCHER (Pooled + AI Live Context)")
    print("="*70)

    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("[-] ERROR: EMAIL credentials not found in .env")
        exit()

    state = load_state()
    now = datetime.now()
    initial_count = 0
    followup_count = 0

    # 1. Gather all leads that need emailing first to optimize the batch
    leads_to_process = []
    try:
        with open(LEADS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = row.get('Email', '').strip()
                company = row.get('Company', 'your company').strip()
                title = row.get('Title', '')
                website = row.get('Website', '')

                name = "there"
                if "(" in title and ")" in title:
                    full_name = title.split("(")[1].split(")")[0]
                    name = full_name.split(" ")[0]

                if not email or "@" not in email or email.lower() == "n/a":
                    continue

                lead_state = state.get(email)

                if not lead_state:
                    leads_to_process.append({"type": "INITIAL", "email": email, "name": name, "company": company, "website": website})
                else:
                    step = lead_state.get("step", 1)
                    last_date_str = lead_state.get("last_contact_date")
                    if step == 1 and last_date_str:
                        days_passed = (now - datetime.fromisoformat(last_date_str)).days
                        if days_passed >= 3:
                            leads_to_process.append({"type": "FOLLOWUP", "email": email, "name": name, "company": company, "website": website})

    except Exception as e:
        print(f"[-] Failed to read leads: {e}")
        exit()

    if not leads_to_process:
        print("[Nexus] Dispatch Complete. No new leads require pitches or follow-ups.")
        exit()

    print(f"[!] Target Acquired: {len(leads_to_process)} leads queued for dispatch.")

    # 2. Connection Pooling - Open SMTP ONCE for the entire batch
    print("[*] Establishing Persistent SMTP Connection Pool...")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
    except Exception as e:
        print(f"[-] Critical SMTP Connection Failure: {e}")
        exit()

    # 3. Process Batch
    for target in leads_to_process:
        email_addr = target['email']
        name = target['name']
        company = target['company']

        try:
            if target['type'] == "INITIAL":
                print(f"\n[Nexus Dispatcher] Firing INITIAL pitch to {name} at {company} ({email_addr})...")
                website_context = scrape_website_context(target['website'])
                subject, body = draft_ai_pitch(name, company, website_context)

                msg = MIMEMultipart()
                msg['From'] = f"Kingsley Vance Maurya <{EMAIL_USER}>"
                msg['To'] = email_addr
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                server.sendmail(EMAIL_USER, email_addr, msg.as_string())

                state[email_addr] = {
                    "step": 1,
                    "last_contact_date": now.isoformat(),
                    "company": company,
                    "name": name
                }
                initial_count += 1

            elif target['type'] == "FOLLOWUP":
                print(f"\n[Nexus Dispatcher] Firing FOLLOW-UP #1 to {name} at {company} ({email_addr})...")
                subject, body = get_followup_pitch(name, company)

                msg = MIMEMultipart()
                msg['From'] = f"Kingsley Vance Maurya <{EMAIL_USER}>"
                msg['To'] = email_addr
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                server.sendmail(EMAIL_USER, email_addr, msg.as_string())

                state[email_addr]["step"] = 2
                state[email_addr]["last_contact_date"] = now.isoformat()
                followup_count += 1

            # Save state iteratively so we don't lose progress if it crashes
            save_state(state)

            # Anti-spam pacing
            time.sleep(2.5)

        except Exception as e:
            print(f"  [-] Failed to process {email_addr}: {e}")
            # Reconnect if connection dropped
            try:
                server.quit()
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
            except:
                pass

    server.quit()
    print(f"\n[Nexus] ARGON MAX Batch Dispatch Complete.")
    print(f"  > Initial Pitches Sent: {initial_count}")
    print(f"  > Follow-Ups Sent:      {followup_count}")
