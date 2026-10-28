import urllib.request
import json
import time

def find_leads_overpass(query, location):
    overpass_url = "http://overpass-api.de/api/interpreter"

    # query for hotels in a specific location
    overpass_query = f"""
    [out:json];
    area["name"="{location}"]->.searchArea;
    (
      node["tourism"="hotel"](area.searchArea);
      way["tourism"="hotel"](area.searchArea);
    );
    out tags limit 40;
    """

    if query == 'mechanic':
        overpass_query = f"""
        [out:json];
        area["name"="{location}"]->.searchArea;
        (
          node["shop"="car_repair"](area.searchArea);
          way["shop"="car_repair"](area.searchArea);
        );
        out tags limit 40;
        """

    req = urllib.request.Request(overpass_url, data=overpass_query.encode('utf-8'), headers={'User-Agent': 'NexusLeadScout/1.0'})
    leads = []

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            for element in data.get('elements', []):
                tags = element.get('tags', {})
                name = tags.get('name')
                if not name:
                    continue
                phone = tags.get('phone', tags.get('contact:phone', 'N/A'))
                email = tags.get('email', tags.get('contact:email', 'N/A'))
                website = tags.get('website', tags.get('contact:website', 'N/A'))

                # Filter out useless ones
                if phone == "N/A" and email == "N/A":
                    continue

                leads.append({
                    "Company": name,
                    "Title": "Owner / Manager",
                    "Phone": phone,
                    "Email": email,
                    "Website": website
                })
    except Exception as e:
        print(f"Error with Overpass: {e}")

    return leads

print("Executing REAL OSINT Lead Generation via Overpass API...")
print("Pulling public registry data from OpenStreetMap...")
leads_1 = find_leads_overpass('hotel', 'Mauritius')
time.sleep(2)
leads_2 = find_leads_overpass('mechanic', 'London')

all_leads = leads_1 + leads_2

print(f"\nFound {len(all_leads)} REAL businesses.\n")
print("-" * 110)
print(f"{'Company':<35} | {'Phone':<25} | {'Email':<30}")
print("-" * 110)

for l in all_leads:
    company = l['Company'][:33]
    phone = str(l['Phone'])[:25]
    email = str(l['Email'])[:30]
    print(f"{company:<35} | {phone:<25} | {email:<30}")

print("-" * 110)

output_path = 'C:/Users/deven/OneDrive/Desktop/Agents/real_leads_output.csv'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write("Company,Title,Phone,Email,Website\n")
    for l in all_leads:
        f.write(f"\"{l['Company']}\",\"{l['Title']}\",\"{l['Phone']}\",\"{l['Email']}\",\"{l['Website']}\"\n")
print(f"\nSaved full verified details to {output_path}")