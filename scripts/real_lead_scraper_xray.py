import urllib.request
import urllib.parse
import re
import csv
import time
import os
import random

OUTPUT_FILE = r"C:\Users\deven\OneDrive\Desktop\Agents\real_leads_output.csv"

def predict_email(first_name, last_name, company_domain):
    """Predicts common corporate email formats."""
    f = first_name.lower().strip()
    l = last_name.lower().strip()
    d = company_domain.lower().strip()
    return [
        f"{f}.{l}@{d}",
        f"{f[0]}{l}@{d}",
        f"{f}@{d}",
        f"{f}{l[0]}@{d}"
    ]

def hunt_xray_leads(job_title, location, company_domain):
    print(f"[Nexus OSINT] Executing X-Ray Dork for {job_title} in {location} ({company_domain})...")

    # The Dork: site:linkedin.com/in/ "General Manager" "Mauritius"
    query = f'site:linkedin.com/in/ "{job_title}" "{location}"'
    encoded_query = urllib.parse.quote_plus(query)

    # We use DuckDuckGo HTML search to bypass Google's aggressive CAPTCHAs
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    req = urllib.request.Request(url, headers=headers)
    leads = []

    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')

            # Simple regex to extract names from the SERP titles (e.g., "John Doe - General Manager - Hotel X | LinkedIn")
            # This is fragile but works for a raw OSINT script without BeautifulSoup
            title_pattern = re.compile(r'<a class="result__url" href="[^"]+">([^<]+)</a>')
            matches = title_pattern.findall(html)

            for match in matches:
                # Clean up the DuckDuckGo formatting
                clean_title = match.replace('\n', '').strip()
                if " - " in clean_title:
                    parts = clean_title.split(" - ")
                    full_name = parts[0].strip()

                    # Ensure it's a person, not a company page
                    if " " in full_name and len(full_name.split(" ")) == 2:
                        first_name, last_name = full_name.split(" ")

                        # Generate the most likely email address
                        predicted_emails = predict_email(first_name, last_name, company_domain)
                        best_guess_email = predicted_emails[0] # Usually first.last@company.com

                        leads.append({
                            "Company": company_domain,
                            "Title": f"{job_title} ({full_name})",
                            "Phone": "N/A",
                            "Email": best_guess_email,
                            "Website": f"http://{company_domain}"
                        })
                        print(f"  [+] Extracted via X-Ray: {full_name} | {best_guess_email} | {company_domain}")

            time.sleep(random.uniform(2, 4)) # Random delay to mimic human behavior

    except Exception as e:
        print(f"[-] X-Ray search failed: {e}")

    return leads

if __name__ == "__main__":
    print("="*70)
    print("🦅 NEXUS OSINT HARVESTER: X-RAY DORKING MODULE (LinkedIn Bypass)")
    print("="*70)

    all_leads = []
    # Target corporate executives in Mauritius without paying for LinkedIn Sales Navigator
    all_leads.extend(hunt_xray_leads("General Manager", "Mauritius", "luxresorts.com"))
    all_leads.extend(hunt_xray_leads("Managing Director", "Mauritius", "beachcomber.com"))

    file_exists = os.path.isfile(OUTPUT_FILE)
    existing_emails = set()

    if file_exists:
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_emails.add(row.get('Email', ''))
        except Exception:
            pass

    new_leads = [l for l in all_leads if l['Email'] not in existing_emails]

    if new_leads:
        with open(OUTPUT_FILE, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Company", "Title", "Phone", "Email", "Website"])
            for l in new_leads:
                writer.writerow([l['Company'], l['Title'], l['Phone'], l['Email'], l['Website']])

        print(f"\n[Nexus] Extracted {len(new_leads)} new corporate leads via X-Ray. Injected into real_leads_output.csv")
    else:
        print("\n[Nexus] No new unique leads found in this run.")
