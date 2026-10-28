import urllib.request
import json
import csv
import os
import time

OUTPUT_FILE = r"C:\Users\deven\OneDrive\Desktop\Agents\real_leads_output.csv"

def find_dentists_mauritius():
    print("[Nexus OSINT] Querying OpenStreetMap/Overpass for Dental Clinics in Mauritius...")
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Query for amenity=dentist or healthcare=dentist in Mauritius
    overpass_query = """
    [out:json];
    area["name"="Mauritius"]->.searchArea;
    (
      node["amenity"="dentist"](area.searchArea);
      node["healthcare"="dentist"](area.searchArea);
    );
    out tags limit 100;
    """

    req = urllib.request.Request(overpass_url, data=overpass_query.encode('utf-8'), headers={'User-Agent': 'NexusLeadScout/1.0'})
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

                # We need at least a phone or an email to pitch
                if phone == "N/A" and email == "N/A":
                    continue

                leads.append({
                    "Company": name,
                    "Title": "Principal Dentist / Owner",
                    "Phone": phone,
                    "Email": email,
                    "Website": website
                })
                print(f"  [+] Target Acquired: {name:<25} | {phone:<15} | {email}")
    except Exception as e:
        print(f"[-] OSINT API Error: {e}")

    return leads

if __name__ == "__main__":
    print("="*70)
    print("🦅 NEXUS OSINT: SURGICAL STRIKE (Dentists - Mauritius)")
    print("="*70)

    all_leads = find_dentists_mauritius()

    # Check for duplicates before injecting
    file_exists = os.path.isfile(OUTPUT_FILE)
    existing_emails = set()
    existing_phones = set()

    if file_exists:
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Email') and row.get('Email') != 'N/A':
                        existing_emails.add(row.get('Email').lower())
                    if row.get('Phone') and row.get('Phone') != 'N/A':
                        existing_phones.add(row.get('Phone').replace(' ', ''))
        except Exception:
            pass

    new_leads = []
    for l in all_leads:
        em = l['Email'].lower() if l['Email'] != 'N/A' else 'N/A'
        ph = l['Phone'].replace(' ', '') if l['Phone'] != 'N/A' else 'N/A'

        if em != 'N/A' and em in existing_emails: continue
        if ph != 'N/A' and ph in existing_phones: continue

        new_leads.append(l)
        if em != 'N/A': existing_emails.add(em)
        if ph != 'N/A': existing_phones.add(ph)

    if new_leads:
        with open(OUTPUT_FILE, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Company", "Title", "Phone", "Email", "Website"])
            for l in new_leads:
                writer.writerow([l['Company'], l['Title'], l['Phone'], l['Email'], l['Website']])
        print(f"\n[Nexus] Extracted {len(new_leads)} fresh Dental Clinics. Injected into real_leads_output.csv")
    else:
        print("\n[Nexus] No new unique leads found in this run.")
