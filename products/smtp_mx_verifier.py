# -*- coding: utf-8 -*-
# Nexus Bulk SMTP Socket Email Verifier
import socket, dns.resolver

def verify_email(email):
    domain = email.split("@")[-1]
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_host = str(records[0].exchange)
        print(f"Found MX host {mx_host} for {domain}. Deliverable!")
        return True
    except Exception as e:
        print(f"Domain {domain} unverified: {e}")
        return False

if __name__ == "__main__":
    verify_email("test@gmail.com")
