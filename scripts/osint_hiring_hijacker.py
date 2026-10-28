import urllib.request
import xml.etree.ElementTree as ET
import re
import csv
import os
import time

OUTPUT_FILE = r"C:\Users\deven\OneDrive\Desktop\Agents\real_leads_output.csv"

def hunt_hiring_companies():
    print("[Nexus OSINT] Hijacking remote job boards (WeWorkRemotely, etc.) to intercept hiring budgets...")

    # We target Management, Finance, and Operations roles.
    # If they are willing to pay $80k/yr for a human, we can pitch a $250 lifetime AI license.
    rss_urls = [
        "https://weworkremotely.com/categories/remote-management-and-finance-jobs.rss",
        "https://weworkremotely.com/categories/remote-customer-support-jobs.rss"
    ]

    leads = []

    for url in rss_urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)

                for item in root.findall('./channel/item')[:15]: # Get top 15 recent jobs per feed
                    title = item.find('title').text
                    # Title format is usually "Company Name: Job Title"
                    if ":" in title:
                        company_name = title.split(":")[0].strip()
                        job_title = title.split(":")[1].strip()

                        # Generate a predictable corporate structure
                        # Since we don't have the exact CEO name from the RSS, we address the Hiring Manager
                        domain_guess = company_name.lower().replace(" ", "").replace(",", "").replace(".", "") + ".com"

                        leads.append({
                            "Company": company_name,
                            "Title": f"Hiring Manager ({job_title})",
                            "Phone": "N/A",
                            "Email": f"founders@{domain_guess}", # Often routes to leadership in startups
                            "Website": f"http://{domain_guess}"
                        })

                        # Also target the HR/Careers inbox
                        leads.append({
                            "Company": company_name,
                            "Title": f"Talent Acquisition ({job_title})",
                            "Phone": "N/A",
                            "Email": f"careers@{domain_guess}",
                            "Website": f"http://{domain_guess}"
                        })

                        print(f"  [+] Budget Intercepted: {company_name} is hiring for '{job_title}'")
        except Exception as e:
            print(f"[-] Failed to hijack RSS feed {url}: {e}")

    return leads

if __name__ == "__main__":
    print("="*70)
    print("🦅 NEXUS OSINT: HIRING BUDGET HIJACKER")
    print("="*70)

    all_leads = hunt_hiring_companies()

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

        print(f"\n[Nexus] Extracted {len(new_leads)} high-intent corporate targets. Injected into real_leads_output.csv")
    else:
        print("\n[Nexus] No new unique leads found in this run.")
