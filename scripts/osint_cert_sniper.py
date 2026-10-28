import urllib.request
import json
import csv
import os
import time
import re

OUTPUT_FILE = r"C:\Users\deven\OneDrive\Desktop\Agents\real_leads_output.csv"

def hunt_new_domains(tld="%.mu"):
    print(f"[Nexus OSINT] Sniping Certificate Transparency Logs (crt.sh) for newly registered {tld} domains...")
    # Query crt.sh for recent SSL certificates issued to this TLD
    url = f"https://crt.sh/?q={tld}&output=json"

    leads = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())

            # crt.sh can return thousands. We grab the most recent 25.
            domains = set()
            for entry in data[:100]:
                name = entry.get('name_value', '').lower()
                # Clean up wildcards
                name = name.replace('*.', '')
                if re.match(r'^[a-z0-9-]+\.[a-z]+$', name):
                    domains.add(name)
                if len(domains) >= 25:
                    break

            for domain in domains:
                company_name = domain.split('.')[0].capitalize()

                # A new domain means a new business. Pitch web dev / AI infrastructure.
                leads.append({
                    "Company": company_name,
                    "Title": "Founder / IT Director",
                    "Phone": "N/A",
                    "Email": f"hello@{domain}",
                    "Website": f"https://{domain}"
                })
                leads.append({
                    "Company": company_name,
                    "Title": "Founder / IT Director",
                    "Phone": "N/A",
                    "Email": f"admin@{domain}",
                    "Website": f"https://{domain}"
                })
                print(f"  [+] New Infrastructure Detected: {domain}")

    except Exception as e:
        print(f"[-] Failed to query crt.sh: {e}")

    return leads

if __name__ == "__main__":
    print("="*70)
    print("🦅 NEXUS OSINT: CERTIFICATE TRANSPARENCY SNIPER")
    print("="*70)

    all_leads = hunt_new_domains("%.mu") # Target Mauritius explicitly
    all_leads.extend(hunt_new_domains("%.ai")) # Target AI startups globally

    file_exists = os.path.isfile(OUTPUT_FILE)
    existing_emails = set()

    if file_exists:
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_emails.add(row.get('Email', '').lower())
        except Exception:
            pass

    new_leads = [l for l in all_leads if l['Email'].lower() not in existing_emails]

    if new_leads:
        with open(OUTPUT_FILE, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Company", "Title", "Phone", "Email", "Website"])
            for l in new_leads:
                writer.writerow([l['Company'], l['Title'], l['Phone'], l['Email'], l['Website']])

        print(f"\n[Nexus] Extracted {len(new_leads)} newly established companies. Injected into real_leads_output.csv")
    else:
        print("\n[Nexus] No new unique leads found in this run.")