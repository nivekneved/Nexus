"""
Nexus™ $1.00 Digital Product Launch & Distribution Playbook
==========================================================
Generates tailored, high-converting promo copy and direct checkout links
for Reddit, X/Twitter, GitHub READMEs, and developer communities.
"""

import os
from core.digital_store_service import digital_store_service

def generate_promotions():
    print("=" * 75)
    print(" 🚀 NEXUS™ $1.00 DIGITAL PRODUCT DISTRIBUTION PLAYBOOK")
    print("=" * 75)
    print("Target: Instant $1.00 USD cashflow via 1-click self-hosted Python tools\n")

    catalog = digital_store_service.get_catalog()
    
    # 1. REDDIT COPY (r/SideProject, r/Python, r/selfhosted)
    print("--- [1] REDDIT (r/SideProject or r/selfhosted) ---")
    print("Title: I was tired of $30/mo SaaS tools just to clean my inbox and verify emails, so I built 3 standalone $1 Python scripts.")
    print("\nBody:")
    print(
        "Hey everyone,\n\n"
        "Like many developers and small founders, I was frustrated with paying monthly recurring subscriptions "
        "for tiny utility features that should just be simple, self-hosted Python scripts.\n\n"
        "So I packaged my personal production tools into zero-dependency, single-file scripts you can run locally forever:\n\n"
        "1. 🛡️ Nexus Email Guardian: Connects to your IMAP (Gmail/Outlook), nukes disposable spam TLDs (.xyz, .buzz), "
        "and locks down 2FA/OTP/invoice emails so you never lose them.\n"
        "2. 💬 Nexus WhatsApp Bot Starter: A clean FastAPI bot template that generates 1-click wa.me chat links and auto-quotes clients.\n"
        "3. 🔍 Nexus B2B Lead Scraper & MX Verifier: Checks DNS mail exchange records directly so you never hit bounce penalties.\n\n"
        "No telemetry, no accounts required, no vendor lock-in. You pay $1.00 once via PayPal, the source code is delivered instantly "
        "to your browser and emailed to you, and it's yours to run or modify forever.\n\n"
        "Check it out here: http://localhost:8000/store (or get the 3-in-1 pack for $1)\n"
        "Would love to hear what other micro-tools you'd like to see packaged like this!\n"
    )

    # 2. X / TWITTER COPY (Build in public thread)
    print("--- [2] X / TWITTER THREAD ---")
    print(
        "1/3 I just launched 3 self-hosted Python micro-tools for $1.00 each.\n"
        "No subscriptions. No API vendor lock-in. Run them on your machine forever.\n\n"
        "• Email Guardian (IMAP spam killer & 2FA shield)\n"
        "• WhatsApp Bot Starter (FastAPI + wa.me router)\n"
        "• B2B DNS MX Verifier (zero-bounce lead checker)\n\n"
        "2/3 Why $1? Because micro-tools shouldn't cost $30/month SaaS retainers. Pay once, download the source code, run locally.\n\n"
        "3/3 Grab any script (or all 3 in a bundle) for $1:\n"
        "👉 http://localhost:8000/store\n"
        "#buildinpublic #python #indiehackers #selfhosted\n"
    )

    # 3. GITHUB README BADGE
    print("--- [3] GITHUB README EMBED BADGE ---")
    print(
        "[![Get Nexus Dev Superpack ($1.00)](https://img.shields.io/badge/Get%20Dev%20Superpack-$1.00%20USD-blue?style=for-the-badge&logo=paypal)](http://localhost:8000/store)\n"
    )

    # 4. DIRECT 1-CLICK PAYPAL LINKS
    print("--- [4] DIRECT 1-CLICK PAYPAL CHECKOUT LINKS ---")
    for item in catalog:
        print(f"• {item['name']} ({item['id']}): ${item['price_usd']:.2f} USD")
        print(f"  File: {item['filename']}")
        print(f"  Store Link: http://localhost:8000/store")
        print()

if __name__ == "__main__":
    generate_promotions()
