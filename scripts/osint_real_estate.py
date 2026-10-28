import urllib.request
import urllib.parse
import json
import csv
import os
import time
import random
import re

OUTPUT_FILE = r"C:\Users\deven\OneDrive\Desktop\Agents\real_leads_output.csv"

def hunt_overpass_real_estate(location="Mauritius"):
    print(f"[Nexus OSINT] Querying OpenStreetMap for Real Estate Agencies in {location}...")
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    area["name"="{location}"]->.searchArea;
    (
      node["office"="estate_agent"](area.searchArea);
      way["office"="estate_agent"](area.searchArea);
    );
    out tags limit 50;
    """
    req = urllib.request.Request(overpass_url, data=query.encode('utf-8'), headers={'User-Agent': 'NexusLeadScout/1.0'})
    leads = []
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            for element in data.get('elements', []):
                tags = element.get('tags', {})
                name = tags.get('name')
                if not name: continue
                phone = tags.get('phone', tags.get('contact:phone', 'N/A'))
                email = tags.get('email', tags.get('contact:email', 'N/A'))
                website = tags.get('website', tags.get('contact:website', 'N/A'))
                if phone == "N/A" and email == "N/A": continue
                leads.append({
                    "Company": name,
                    "Title": "Director / Branch Manager",
                    "Phone": phone,
                    "Email": email,
                    "Website": website
                })
                print(f"  [+] Overpass Target: {name:<25} | {email}")
    except Exception as e:
        print(f"[-] Overpass Error: {e}")
    return leads

def predict_email(first_name, last_name, company_domain):
    f = first_name.lower().strip()
    l = last_name.lower().strip()
    d = company_domain.lower().strip()
    return f"{f}.{l}@{d}"

def hunt_xray_real_estate(job_title, location, company_domain):
    print(f"[Nexus OSINT] Executing X-Ray Dork for {job_title} at {company_domain} ({location})...")
    query = f'site:linkedin.com/in/ "{job_title}" "{location}"'
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    req = urllib.request.Request(url, headers=headers)
    leads = []
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            title_pattern = re.compile(r'<a class="result__url" href="[^"]+">([^<]+)</a>')
            matches = title_pattern.findall(html)
            for match in matches:
                clean_title = match.replace('\n', '').strip()
                if " - " in clean_title:
                    parts = clean_title.split(" - ")
                    full_name = parts[0].strip()
                    if " " in full_name and len(full_name.split(" ")) == 2:
                        first_name, last_name = full_name.split(" ")
                        best_guess_email = predict_email(first_name, last_name, company_domain)
                        leads.append({
                            "Company": company_domain,
                            "Title": f"{job_title} ({full_name})",
                            "Phone": "N/A",
                            "Email": best_guess_email,
                            "Website": f"http://{company_domain}"
                        })
                        print(f"  [+] X-Ray Target: {full_name:<25} | {best_guess_email}")
            time.sleep(random.uniform(2, 4))
    except Exception as e:
        print(f"[-] X-Ray search failed: {e}")
    return leads

if __name__ == "__main__":
    print("="*70)
    print("🦅 NEXUS OSINT: SURGICAL STRIKE (Real Estate Agencies)")
    print("="*70)

    # 1. Local B&M Agencies via OpenStreetMap
    all_leads = hunt_overpass_real_estate("Mauritius")

    # 2. X-Ray Dorking for Directors at Top Mauritius Firms
    target_agencies = ["pamgolding.mu", "seeff.mu", "remax.mu", "parklane.mu", "lexia.mu"]
    for domain in target_agencies:
        all_leads.extend(hunt_xray_real_estate("Director", "Mauritius", domain))
        all_leads.extend(hunt_xray_real_estate("Founder", "Mauritius", domain))

    file_exists = os.path.isfile(OUTPUT_FILE)
    existing_emails = set()

    if file_exists:
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Email') and row.get('Email') != 'N/A':
                        existing_emails.add(row.get('Email').lower())
        except Exception:
            pass

    new_leads = [l for l in all_leads if l['Email'] != 'N/A' and l['Email'].lower() not in existing_emails]

    if new_leads:
        with open(OUTPUT_FILE, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Company", "Title", "Phone", "Email", "Website"])
            for l in new_leads:
                writer.writerow([l['Company'], l['Title'], l['Phone'], l['Email'], l['Website']])
        print(f"\n[Nexus] Extracted {len(new_leads)} fresh Real Estate targets. Injected into real_leads_output.csv")
    else:
        print("\n[Nexus] No new unique leads found in this run.")
