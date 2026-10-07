import sys
import os
import asyncio

# Ensure root directory is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.storage import safe_load_json
from core.enterprise_revenue_engine import enterprise_revenue_engine

def main():
    print("Loading leads pipeline...")
    leads = safe_load_json("leads_pipeline.json", default=[])

    medical_leads = [
        l for l in leads
        if "clinic" in str(l.get("industry", "")).lower() or
           "health" in str(l.get("industry", "")).lower() or
           "medical" in str(l.get("industry", "")).lower()
    ]

    if not medical_leads:
        print("No medical/healthcare leads found in the pipeline.")
        return

    print(f"Found {len(medical_leads)} medical/healthcare leads. Generating proposals...")

    for lead in medical_leads:
        print(f"\n--- Generating Proposal for {lead.get('company', 'Unknown')} ---")
        contact_name = lead.get('contact_name', 'Executive Director')
        contact_email = lead.get('contact_email', 'contact@clinic.mu')

        try:
            res = enterprise_revenue_engine.generate_high_ticket_proposal(
                client_name=contact_name,
                client_email=contact_email,
                niche="Private Healthcare Clinic & Telemedicine"
            )
            prop = res.get('proposal', {})
            print(f"✅ Success! Proposal ID: {prop.get('deal_id')}")
            print(f"Value: ${prop.get('pricing_structure', {}).get('upfront_deployment_usd')} Upfront + ${prop.get('pricing_structure', {}).get('monthly_retainer_usd')}/mo")
            print(f"Payment Link: {prop.get('invoice', {}).get('payment_url')}")
            print("-" * 50)
        except Exception as e:
            print(f"❌ Error generating proposal for {contact_name}: {e}")

if __name__ == "__main__":
    main()
