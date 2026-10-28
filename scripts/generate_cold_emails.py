import csv
import os

LEADS_FILE = 'C:/Users/deven/OneDrive/Desktop/Agents/real_leads_output.csv'
OUTPUT_DIR = 'C:/Users/deven/OneDrive/Desktop/Agents/campaigns'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Email Templates based on Niche
templates = {
    "Plumbing": {
        "Product": "ReceiptChase",
        "Price": "Rs 85,000 MUR (~$1,888 USD)",
        "Subject": "Home Depot receipts going missing? (Quick question)",
        "Body": """Hi {Name},

I was looking at {Company} online and noticed you have a decent sized field team.

Quick question: How much billable material are you writing off every month because your guys lose the Home Depot/Lowe's receipts in their trucks?

I just finished building 'ReceiptChase'â€”itâ€™s a dead-simple app for your field guys. They literally just snap a photo of the receipt and tag the job before they even leave the parking lot. It syncs straight to your office dashboard so your bookkeeper doesn't have to chase them on Fridays.

I'm not selling a SaaS subscription. I'm selling the complete software and intellectual property (IP) outright for {Price}. You own it forever, host it yourself, and never pay a monthly fee.

If you want to see a live demo of how it stops material leakage, check it out here: https://nexus.mu/turnkey_fleet

Best,
Kingsley Vance Maurya
Nexus Principal Engineering"""
    },
    "Mechanics": {
        "Product": "BayText",
        "Price": "Rs 95,000 MUR (~$2,100 USD)",
        "Subject": "Stop customers calling for car updates",
        "Body": """Hi {Name},

I was looking up {Company} and I have a quick operational question.

How many hours a day does your team lose just answering the phone to tell a customer, "We're still waiting on parts" or "It's next in the bay"?

I built 'BayText'â€”a digital status board for mechanics. You just drag a customer's car into the 'Ready' column on an iPad, and it automatically shoots them an SMS text message. It kills the "is it ready yet?" phone calls instantly.

I'm not looking to charge you $300/month like Shopmonkey. I am selling the complete, white-labeled software outright for {Price}. You buy it once, you own the IP forever.

You can view the storefront and secure the source code here: https://nexus.mu/turnkey_fleet

Cheers,
Kingsley Vance Maurya
Nexus Principal Engineering"""
    },
    "Properties": {
        "Product": "KeySnap",
        "Price": "Rs 105,000 MUR (~$2,330 USD)",
        "Subject": "Contractors losing master keys?",
        "Body": """Hi {Name},

I noticed you manage {Company} and likely deal with contractors checking out units constantly.

I'm reaching out because I just built a visual lockbox log that kills the paper sign-out sheet. It's an iPad app where a contractor scans the key barcode and takes a quick selfie to check it out. If it's not back by 5 PM, it auto-texts them. No more $1,000 re-keying jobs because a plumber "lost" the master key.

We sell the complete software and IP outright for {Price}. No recurring SaaS fees. You own the code.

Take a look at the live demo here: https://nexus.mu/turnkey_fleet

Best,
Kingsley Vance Maurya
Nexus Principal Engineering"""
    },
    "Catering": {
        "Product": "CaterMap",
        "Price": "Rs 95,000 MUR (~$2,100 USD)",
        "Subject": "Translating bride's allergy spreadsheets",
        "Body": """Hi {Name},

I saw the events {Company} puts onâ€”beautiful work.

I know that translating a 150-person guest spreadsheet with 12 different dietary restrictions into a kitchen prep list is a nightmare. One mistake with a nut allergy plate is a massive liability.

I built 'CaterMap'. You upload the bride's messy Excel sheet, and it generates a visual floor plan for your servers (highlighting exactly which seat gets the allergy plate) and exact prep counts for the kitchen.

I am selling the software outright (with full IP transfer) for {Price}. No monthly SaaS fees.

You can download the Turnkey asset right now here: https://nexus.mu/turnkey_fleet

Best,
Kingsley Vance Maurya
Nexus Principal Engineering"""
    },
    "Photography": {
        "Product": "GuestLens",
        "Price": "Rs 85,000 MUR (~$1,888 USD)",
        "Subject": "App-less guest photo collector for your weddings",
        "Body": """Hi {Name},

I love the portfolio for {Company}.

I noticed a lot of photographers struggle to collect all the candid photos guests take at the reception because guests refuse to download random photo-sharing apps.

I just built 'GuestLens'â€”an app-less, frictionless web app. You put a QR code on the tables, guests scan it, and upload straight from their browser to a gallery you control. No app store downloads.

I'm selling the complete software package and IP for {Price}. You can white-label it and offer it as a premium add-on to your wedding packages. It pays for itself in two weddings.

Secure the source code here: https://nexus.mu/turnkey_fleet

Cheers,
Kingsley Vance Maurya
Nexus Principal Engineering"""
    }
}

# Determine Niche based on company name (Simple heuristic for demo)
def get_niche(company_name):
    name = company_name.lower()
    if 'plumb' in name or 'rooter' in name:
        return 'Plumbing'
    elif 'auto' in name or 'mechanic' in name:
        return 'Mechanics'
    elif 'prop' in name or 'real estate' in name:
        return 'Properties'
    elif 'cater' in name or 'food' in name:
        return 'Catering'
    elif 'photo' in name or 'lens' in name:
        return 'Photography'
    else:
        return 'Plumbing' # Default fallback

print("Generating hyper-personalized cold outreach sequences...")

try:
    with open(LEADS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            company = row['Company']
            email = row['Email']

            # Skip rows with no email
            if email == 'N/A':
                continue

            niche = get_niche(company)
            template = templates[niche]

            # Simple name extraction (first word of company if no contact name exists)
            name = company.split()[0]
            if name.lower() in ['the', 'a', 'an', 'grand', 'city', 'london', 'texas', 'austin', 'sunset']:
                # If first word is generic, just say "Team" or use a better heuristic
                 name = "Team"

            # If the email itself has a name (e.g., m.hendricks), extract it
            if '@' in email:
                prefix = email.split('@')[0]
                if '.' in prefix:
                    name = prefix.split('.')[1].capitalize() if len(prefix.split('.')) > 1 else prefix.capitalize()
                elif len(prefix) > 3 and not prefix.lower() in ['info', 'contact', 'hello', 'sales', 'dispatch', 'management', 'service', 'booking']:
                    name = prefix.capitalize()

            subject = template['Subject']
            body = template['Body'].format(Name=name, Company=company, Price=template['Price'])

            # Save the sequence
            safe_company = "".join([c for c in company if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            filename = f"{safe_company.replace(' ', '_')}_Sequence.txt"
            filepath = os.path.join(OUTPUT_DIR, filename)

            with open(filepath, 'w', encoding='utf-8') as out_f:
                out_f.write(f"TO: {email}\n")
                out_f.write(f"SUBJECT: {subject}\n")
                out_f.write("-" * 50 + "\n")
                out_f.write(body)

            print(f"âœ… Generated pitch for {company} -> {filename}")
except FileNotFoundError:
    print(f"Error: Could not find {LEADS_FILE}. Make sure the lead scraper ran successfully.")

print(f"\nAll sequences saved to {OUTPUT_DIR}/")
