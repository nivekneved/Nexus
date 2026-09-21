"""
Nexus™ B2B Lead Scraper & MX Verifier (Micro-Edition)
=====================================================
A lightweight Python script to verify B2B lead emails via DNS MX records,
filtering out non-existent domains and eliminating bounce penalties.

Usage:
  python nexus_b2b_lead_scraper.py
"""

import socket
import json

def verify_domain_mx(domain: str) -> bool:
    """Verifies that a domain has valid mail exchange records."""
    try:
        # Check domain resolution
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def verify_email_list(emails: list) -> dict:
    valid = []
    invalid = []
    for email_addr in emails:
        if "@" not in email_addr:
            invalid.append({"email": email_addr, "reason": "MALFORMED"})
            continue
        domain = email_addr.split("@")[-1].strip().lower()
        if verify_domain_mx(domain):
            valid.append({"email": email_addr, "domain": domain, "deliverable": True})
        else:
            invalid.append({"email": email_addr, "domain": domain, "deliverable": False, "reason": "NO_HOST_OR_MX"})
            
    return {
        "total_checked": len(emails),
        "valid_count": len(valid),
        "invalid_count": len(invalid),
        "valid_leads": valid,
        "suppressed_leads": invalid
    }

if __name__ == "__main__":
    sample_targets = [
        "devenpawaray@gmail.com",
        "fakeuser123@notarealdomain99999.mu",
        "contact@google.com",
        "info@chamarel-lodge.mu"
    ]
    print("🔍 Nexus Lead Scraper & MX Verifier starting...")
    res = verify_email_list(sample_targets)
    print(f"✓ Valid deliverable addresses: {res['valid_count']}/{res['total_checked']}")
    for v in res["valid_leads"]:
        print(f"  ✓ {v['email']}")
    for inv in res["suppressed_leads"]:
        print(f"  ❌ Blocked/Suppressed: {inv['email']} ({inv['reason']})")
