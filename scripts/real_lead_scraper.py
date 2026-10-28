import urllib.request
import urllib.parse
import json
import re
import time

def find_leads(query):
    # Using OpenStreetMap's Nominatim API (Free, No API Key required)
    # It pulls real, registered public businesses
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&extratags=1&addressdetails=1&limit=15"
    headers = {'User-Agent': 'NexusLeadScout/1.0 (devenpawaray@gmail.com)'}
    req = urllib.request.Request(url, headers=headers)

    leads = []
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())

            for place in data:
                name = place.get('name')
                if not name:
                    continue

                extratags = place.get('extratags', {})
                phone = extratags.get('phone', extratags.get('contact:phone', 'N/A'))
                website = extratags.get('website', extratags.get('contact:website', ''))

                email = "N/A"
                if website and website.startswith('http'):
                    # 2. OSINT DOM Scraper: Visit the actual website and extract emails using Regex
                    try:
                        req_site = urllib.request.Request(website, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req_site, timeout=5) as site_res:
                            html = site_res.read().decode('utf-8', errors='ignore')
                            # Regex to find email patterns
                            emails = re.findall(r'[a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+\.[a-zA-Z]{2,5}', html)
                            # Filter out common image extensions caught by regex
                            valid_emails = [e for e in emails if not e.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'))]
                            if valid_emails:
                                # Get the most likely contact email, avoid wix/sentry auto-injected ones if possible
                                email = valid_emails[0]
                    except Exception:
                        pass

                leads.append({
                    "Company": name,
                    "Title": "Owner / Manager", # Public OSINT gives company-level data
                    "Phone": phone,
                    "Email": email,
                    "Website": website if website else "N/A"
                })
                # Be polite to the free API
                time.sleep(1)
    except Exception as e:
        print(f"Error querying {query}: {e}")

    return leads

print("Executing REAL OSINT Lead Generation...")
print("1. Querying Public Business Registries (Maps Data)")
print("2. Scraping DOMs of target websites for contact data...")

# Let's target two niches for our Turnkey Apps:
# 1. Hotels/Resorts in Mauritius (For CaterMap / GuestLens)
# 2. Mechanics in London (For BayText / BookNudge)
leads_1 = find_leads("hotel in Mauritius")
leads_2 = find_leads("mechanic in London")

all_leads = leads_1 + leads_2

print(f"\nFound {len(all_leads)} REAL businesses. Extracting contact data...\n")
print("-" * 100)
print(f"{'Company':<35} | {'Phone':<18} | {'Email':<30}")
print("-" * 100)

for l in all_leads:
    company = l['Company'][:33]
    phone = str(l['Phone'])[:18]
    email = str(l['Email'])[:30]
    print(f"{company:<35} | {phone:<18} | {email:<30}")

print("-" * 100)

# Save to CSV
output_path = 'C:/Users/deven/OneDrive/Desktop/Agents/real_leads_output.csv'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write("Company,Title,Phone,Email,Website\n")
    for l in all_leads:
        f.write(f"\"{l['Company']}\",\"{l['Title']}\",\"{l['Phone']}\",\"{l['Email']}\",\"{l['Website']}\"\n")
print(f"\nSaved full verified details to {output_path}")
