"""
Nexus Dedicated Product Fleets & Partner Economics Engine
=========================================================
Architected for enterprise product scaling:
- Dedicated 11-Agent Fleet for Medical 360™ (Healthcare & Clinics)
- Dedicated 11-Agent Fleet for Enn Rev Enn Sourir™ (NGO / CSR Foundations)
- Financial modeling with 1/5 (20%) Annual Maintenance SLA Contracts
"""

from typing import Dict, Any, List
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# Financial Model & Product Portfolio Economics
# ─────────────────────────────────────────────────────────────────────────────

PRODUCT_ECONOMICS = [
    {
        "product_id": "medical360",
        "name": "Medical 360™ Clinic Portal",
        "icon": "🩺",
        "sector": "Private Healthcare, Clinics & Diagnostic Centers",
        "demo_url": "https://www.med360.mu/preview",
        "leads_count": 4,
        "contacted_count": 4,
        "base_price_mur": 45000,
        "maintenance_fee_ratio": "1/5 (20%)",
        "yearly_maintenance_mur": 9000,
        "year1_contract_per_win": 54000,
        "three_year_ltv_per_win": 72000,
        "pipeline_setup_potential": 180000,
        "pipeline_yearly_maintenance_arr": 36000,
        "total_year1_pipeline_potential": 216000,
        "target_companies": [
            {"company": "Ébène Diagnostic & Medical Center", "contact": "Dr. Salim Joomun", "status": "PITCHED"},
            {"company": "City Clinic Group", "contact": "Dr. Patrick Chui Wan Cheong", "status": "PITCHED"},
            {"company": "Clinique Bon Pasteur", "contact": "Christine Koenig", "status": "PITCHED"},
            {"company": "Clinique du Nord", "contact": "Dr. Alain Wong", "status": "PITCHED"}
        ]
    },
    {
        "product_id": "enn_rev_enn_sourir",
        "name": "Enn Rev Enn Sourir™ NGO & CSR",
        "icon": "❤️",
        "sector": "Corporate CSR Funds, Philanthropy & NGOs",
        "demo_url": "https://ennrevennsourir.vercel.app",
        "leads_count": 4,
        "contacted_count": 4,
        "base_price_mur": 45000,
        "maintenance_fee_ratio": "1/5 (20%)",
        "yearly_maintenance_mur": 9000,
        "year1_contract_per_win": 54000,
        "three_year_ltv_per_win": 72000,
        "pipeline_setup_potential": 180000,
        "pipeline_yearly_maintenance_arr": 36000,
        "total_year1_pipeline_potential": 216000,
        "target_companies": [
            {"company": "Fondation CIEL Nouveau Regard", "contact": "Delphine Bouic", "status": "DISPATCHED_SENT"},
            {"company": "Rogers Capital Corporate CSR", "contact": "Corinne Chung", "status": "DISPATCHED_SENT"},
            {"company": "MCB Forward Foundation", "contact": "Jean-François Desvaux", "status": "DISPATCHED_SENT"},
            {"company": "IBL Foundation", "contact": "Marie-Laurence Dupont", "status": "PITCHED"}
        ]
    },
    {
        "product_id": "itravellix_saas",
        "name": "i-Travellix™ Luxury Travel & Hospitality",
        "icon": "🌟",
        "sector": "Luxury Tour Operators, Inbound DMCs & Resorts",
        "demo_url": "https://i-travellix.vercel.app",
        "leads_count": 6,
        "contacted_count": 6,
        "base_price_mur": 50000,
        "maintenance_fee_ratio": "1/5 (20%)",
        "yearly_maintenance_mur": 10000,
        "year1_contract_per_win": 60000,
        "three_year_ltv_per_win": 80000,
        "pipeline_setup_potential": 300000,
        "pipeline_yearly_maintenance_arr": 60000,
        "total_year1_pipeline_potential": 360000,
        "target_companies": [
            {"company": "Southern Palms Inbound Voyages", "contact": "Kailash Ramgoolam", "status": "DISPATCHED_SENT"},
            {"company": "Coral Cove Travel & Expeditions", "contact": "Nathalie Ah-Kee", "status": "DISPATCHED_SENT"},
            {"company": "Mauritius Discovery Tours DMC", "contact": "Patrick Laroche", "status": "DISPATCHED_SENT"},
            {"company": "Belle Mare Azure Beach Resort", "contact": "Sophie Ramdin", "status": "PITCHED"},
            {"company": "Le Morne Sunset Luxury Villas", "contact": "Jean-Pierre Duval", "status": "PITCHED"},
            {"company": "Chamarel Eco-Lodge & Suites", "contact": "Arnaud Laurent", "status": "QUALIFIED"}
        ]
    },
    {
        "product_id": "nexus_license",
        "name": "Nexus Autonomous Workforce License",
        "icon": "⚡",
        "sector": "Global Tech Agencies, Consultancies & SaaS",
        "demo_url": "http://localhost:8000",
        "leads_count": 11,
        "contacted_count": 3,
        "base_price_mur": 12500,  # $249 USD
        "maintenance_fee_ratio": "1/5 (20%)",
        "yearly_maintenance_mur": 2500,   # $49.80 USD
        "year1_contract_per_win": 15000,
        "three_year_ltv_per_win": 20000,
        "pipeline_setup_potential": 137500,
        "pipeline_yearly_maintenance_arr": 27500,
        "total_year1_pipeline_potential": 165000,
        "target_companies": [
            {"company": "AuraFlow Growth Agency", "contact": "Marcus Vance", "status": "QUEUED"},
            {"company": "Nexus Partner Network", "contact": "Kevin Adlib", "status": "ACTIVE_PARTNER"},
            {"company": "Verve Scale Labs", "contact": "Chloe Chen", "status": "QUEUED"}
        ]
    },
    {
        "product_id": "whatsapp_flight_addon",
        "name": "WhatsApp Flight Addon™",
        "icon": "✈️",
        "sector": "Airlines, DMCs, Travel Agencies & Flight Portals",
        "demo_url": "https://whatsapp-flight-addon.vercel.app",
        "leads_count": 4,
        "contacted_count": 0,
        "base_price_mur": 25000,
        "maintenance_fee_ratio": "1/5 (20%)",
        "yearly_maintenance_mur": 5000,
        "year1_contract_per_win": 30000,
        "three_year_ltv_per_win": 40000,
        "pipeline_setup_potential": 100000,
        "pipeline_yearly_maintenance_arr": 20000,
        "total_year1_pipeline_potential": 120000,
        "target_companies": [
            {"company": "Air Mauritius Digital Sales", "contact": "Laurent L'Entêté", "status": "DISCOVERED"},
            {"company": "Rogers Aviation Mauritius", "contact": "Alexandre de Chazal", "status": "DISCOVERED"},
            {"company": "BlueSky Travel Agency", "contact": "Karine Hardy", "status": "DISCOVERED"},
            {"company": "Silver Wings Travels", "contact": "Sameer Kazi", "status": "DISCOVERED"}
        ]
    },
    {
        "product_id": "whatsapp_restaurant_sme",
        "name": "WhatsApp Restaurant & SME Booking",
        "icon": "🍽️",
        "sector": "Restaurants, Cafes, Spas, Salons & SME Retailers",
        "demo_url": "https://whatsapp-flight-addon.vercel.app",
        "leads_count": 4,
        "contacted_count": 0,
        "base_price_mur": 15000,
        "maintenance_fee_ratio": "1/5 (20%)",
        "yearly_maintenance_mur": 3000,
        "year1_contract_per_win": 18000,
        "three_year_ltv_per_win": 24000,
        "pipeline_setup_potential": 60000,
        "pipeline_yearly_maintenance_arr": 12000,
        "total_year1_pipeline_potential": 72000,
        "target_companies": [
            {"company": "Le Capitaine Restaurant Grand Baie", "contact": "Didier Rousset", "status": "DISCOVERED"},
            {"company": "L'Atelier Gourmand Mauritius", "contact": "Mathieu Bernard", "status": "DISCOVERED"},
            {"company": "La Table du Château", "contact": "Fabien Morel", "status": "DISCOVERED"},
            {"company": "Luigi's Italian Pizzeria & Pasta Bar", "contact": "Luigi Rossi", "status": "DISCOVERED"}
        ]
    }
]

# ─────────────────────────────────────────────────────────────────────────────
# Dedicated 11-Agent Fleets
# ─────────────────────────────────────────────────────────────────────────────

MEDICAL_360_FLEET = [
    {
        "slot": 1,
        "agent_id": "med_lead_scout",
        "name": "Clinic & Hospital Prospector",
        "icon": "🏥",
        "role": "Scouting & Lead Intake",
        "mandate": "Harvests private clinics, dental practices, diagnostic labs, and pediatric clinics in Mauritius.",
        "status": "ONLINE",
        "cadence": "Every 4h"
    },
    {
        "slot": 2,
        "agent_id": "med_pain_auditor",
        "name": "Clinical Workflow Friction Auditor",
        "icon": "🩺",
        "role": "Qualification",
        "mandate": "Audits intake phone queues, manual patient records, and double-booking bottlenecks.",
        "status": "ONLINE",
        "cadence": "On Lead Ingest"
    },
    {
        "slot": 3,
        "agent_id": "med_pitch_crafter",
        "name": "Medical Value Proposition Crafter",
        "icon": "✍️",
        "role": "Commercial Proposal",
        "mandate": "Generates bilingual French/Creole pitches emphasizing appointment sync and compliance.",
        "status": "ONLINE",
        "cadence": "Automated"
    },
    {
        "slot": 4,
        "agent_id": "med_whatsapp_dispatcher",
        "name": "WhatsApp Clinic Dispatcher",
        "icon": "📱",
        "role": "Outreach",
        "mandate": "Transmits interactive demo invites and live booking previews to clinic managers (+230).",
        "status": "ONLINE",
        "cadence": "Real-time"
    },
    {
        "slot": 5,
        "agent_id": "med_demo_concierge",
        "name": "Interactive Demo Walkthrough Host",
        "icon": "🖥️",
        "role": "Demonstration",
        "mandate": "Guides clinic administrators through live interactive walkthroughs at med360.mu/preview.",
        "status": "ONLINE",
        "cadence": "On-Demand"
    },
    {
        "slot": 6,
        "agent_id": "med_objection_resolver",
        "name": "Healthcare Compliance Sentinel",
        "icon": "🛡️",
        "role": "Legal & Security",
        "mandate": "Resolves medical director concerns regarding patient confidentiality (DPA 2017) & encrypted backups.",
        "status": "ONLINE",
        "cadence": "Continuous"
    },
    {
        "slot": 7,
        "agent_id": "med_closer_contracts",
        "name": "Turnkey Medical Commercial Closer",
        "icon": "📑",
        "role": "Closing",
        "mandate": "Issues formal quotes (Rs 45,000 setup) and standardizes 1/5 yearly SLA maintenance agreements.",
        "status": "ONLINE",
        "cadence": "On Deal Qualification"
    },
    {
        "slot": 8,
        "agent_id": "med_juice_reconciler",
        "name": "MCB Juice & Wire Reconciler",
        "icon": "💳",
        "role": "Finance",
        "mandate": "Issues instant MCB Juice QR codes (+230 58169420) and IBAN transfer invoices with auto-receipts.",
        "status": "ONLINE",
        "cadence": "Instant"
    },
    {
        "slot": 9,
        "agent_id": "med_onboarding_provisioner",
        "name": "Clinic Portal Provisioner",
        "icon": "⚙️",
        "role": "Fulfillment",
        "mandate": "Provisions clinic subdomain, loads doctor timetables, configures SMS gateway, and tests booking flow.",
        "status": "ONLINE",
        "cadence": "Post-Payment"
    },
    {
        "slot": 10,
        "agent_id": "med_maintenance_sentinel",
        "name": "Yearly SLA & Maintenance Overseer",
        "icon": "🔧",
        "role": "Maintenance & ARR",
        "mandate": "Guarantees 99.9% portal uptime, quarterly security patches, and bills the 1/5 yearly fee (Rs 9,000/yr).",
        "status": "ONLINE",
        "cadence": "24/7 SLA Watch"
    },
    {
        "slot": 11,
        "agent_id": "med_expansion_scout",
        "name": "Multi-Branch Expansion Scout",
        "icon": "🚀",
        "role": "Upsell & Expansion",
        "mandate": "Upsells satellite clinic licenses, pharmacy inventory add-ons, and mobile doctor dispatchers.",
        "status": "ONLINE",
        "cadence": "Quarterly"
    }
]

ENN_REV_ENN_SOURIR_FLEET = [
    {
        "slot": 1,
        "agent_id": "ngo_csr_scout",
        "name": "CSR Trust & Foundation Scout",
        "icon": "🏛️",
        "role": "Scouting & Lead Intake",
        "mandate": "Scouts major institutional CSR foundations (MCB, Rogers, CIEL, IBL) and philanthropic trusts.",
        "status": "ONLINE",
        "cadence": "Every 4h"
    },
    {
        "slot": 2,
        "agent_id": "ngo_tax_auditor",
        "name": "MRA 15% Tax Deduction Auditor",
        "icon": "📊",
        "role": "Tax & Financial Qualification",
        "mandate": "Calculates corporate tax offsets and CSR compliance certificates for prospective donors.",
        "status": "ONLINE",
        "cadence": "On Lead Ingest"
    },
    {
        "slot": 3,
        "agent_id": "ngo_story_crafter",
        "name": "Cause & Medical Impact Crafter",
        "icon": "❤️",
        "role": "Appeal & Storytelling",
        "mandate": "Drafts verified patient case stories, surgical fundraising campaigns, and impact reports.",
        "status": "ONLINE",
        "cadence": "Automated"
    },
    {
        "slot": 4,
        "agent_id": "ngo_whatsapp_dispatcher",
        "name": "Donor & Patron WhatsApp Concierge",
        "icon": "📱",
        "role": "Outreach",
        "mandate": "Delivers direct WhatsApp partnership pitches to foundation coordinators and board trustees.",
        "status": "ONLINE",
        "cadence": "Real-time"
    },
    {
        "slot": 5,
        "agent_id": "ngo_demo_concierge",
        "name": "NGO Platform Walkthrough Host",
        "icon": "🖥️",
        "role": "Demonstration",
        "mandate": "Demonstrates transparent medical crowdfunding, donor wall, and live fund reconciliation.",
        "status": "ONLINE",
        "cadence": "On-Demand"
    },
    {
        "slot": 6,
        "agent_id": "ngo_governance_sentinel",
        "name": "Integrity & Transparency Watchdog",
        "icon": "⚖️",
        "role": "Governance",
        "mandate": "Ensures every rupee collected has tamper-proof receipts, hospital bill matching, and audit logs.",
        "status": "ONLINE",
        "cadence": "Continuous"
    },
    {
        "slot": 7,
        "agent_id": "ngo_csr_closer",
        "name": "Corporate CSR Retainer Closer",
        "icon": "🤝",
        "role": "Closing",
        "mandate": "Finalizes institutional NGO deployments (Rs 45,000 setup) and annual maintenance contracts.",
        "status": "ONLINE",
        "cadence": "On Foundation Commit"
    },
    {
        "slot": 8,
        "agent_id": "ngo_juice_reconciler",
        "name": "Juice Crowdfund Reconciler",
        "icon": "💳",
        "role": "Finance",
        "mandate": "Reconciles 1-click MCB Juice donations, wire sponsorships, and generates automated tax receipts.",
        "status": "ONLINE",
        "cadence": "Instant"
    },
    {
        "slot": 9,
        "agent_id": "ngo_campaign_provisioner",
        "name": "Urgent Medical Campaign Provisioner",
        "icon": "🚑",
        "role": "Fulfillment",
        "mandate": "Launches urgent pediatric surgery campaigns, goal trackers, and photo verifications in <15m.",
        "status": "ONLINE",
        "cadence": "Emergency Dispatch"
    },
    {
        "slot": 10,
        "agent_id": "ngo_maintenance_sentinel",
        "name": "Yearly SLA & Platform Overseer",
        "icon": "🔧",
        "role": "Maintenance & ARR",
        "mandate": "Provides zero-downtime donation uptime, security guardrails, and bills the 1/5 yearly SLA (Rs 9,000/yr).",
        "status": "ONLINE",
        "cadence": "24/7 SLA Watch"
    },
    {
        "slot": 11,
        "agent_id": "ngo_patron_expander",
        "name": "High-Net-Worth Patron Expander",
        "icon": "👑",
        "role": "Endowment & Expansion",
        "mandate": "Converts one-time corporate donors into permanent annual foundation endowment sponsors.",
        "status": "ONLINE",
        "cadence": "Bi-Annual"
    }
]

import copy
from core.storage import safe_load_json

def get_partner_economics_summary() -> Dict[str, Any]:
    """Computes aggregate partner metrics and breakdown, dynamically synchronized with leads pipeline and contact history."""
    products = copy.deepcopy(PRODUCT_ECONOMICS)
    
    # Safely load live pipeline data
    leads = safe_load_json("leads_pipeline.json", default=[])
    contacts = safe_load_json("contact_history.json", default=[])
    
    if leads or contacts:
        contact_map = {str(c.get("company", "")).strip().lower(): c for c in contacts}
        
        # Categorize leads & contacts per product
        niche_to_prod = {
            "whatsapp_flight_addon": "whatsapp_flight_addon",
            "whatsapp_restaurant_sme": "whatsapp_restaurant_sme",
            "medical360_portal": "medical360",
            "ennrevennsourir_ngo": "enn_rev_enn_sourir",
            "itravellix_saas": "itravellix_saas",
            "mauritius_hospitality": "itravellix_saas",
            "general": "nexus_license",
            None: "nexus_license"
        }
        
        prod_leads: Dict[str, List[Dict[str, Any]]] = {p["product_id"]: [] for p in products}
        prod_contacts: Dict[str, int] = {p["product_id"]: 0 for p in products}
        
        for l in leads:
            pid = niche_to_prod.get(l.get("niche"), "nexus_license")
            if pid in prod_leads:
                prod_leads[pid].append(l)
                
        for c in contacts:
            pid = niche_to_prod.get(c.get("niche"), "nexus_license")
            if pid in prod_contacts:
                prod_contacts[pid] += 1
                
        for p in products:
            pid = p["product_id"]
            live_leads = prod_leads.get(pid, [])
            live_contact_count = prod_contacts.get(pid, 0)
            
            if live_leads:
                p["leads_count"] = len(live_leads)
                p["contacted_count"] = max(p["contacted_count"], live_contact_count)
                
                # Dynamically build target accounts with live CRM status
                dyn_targets = []
                seen_companies = set()
                for l in live_leads:
                    comp_name = l.get("company") or "Unnamed Prospect"
                    if comp_name.lower() in seen_companies:
                        continue
                    seen_companies.add(comp_name.lower())
                    
                    hist = contact_map.get(comp_name.lower())
                    status = (hist.get("status") if hist else None) or l.get("status") or "DISCOVERED"
                    contact_person = (hist.get("contact_name") if hist else None) or l.get("contact_role") or "Lead Contact"
                    
                    dyn_targets.append({
                        "company": comp_name,
                        "contact": contact_person,
                        "status": status
                    })
                    
                if dyn_targets:
                    p["target_companies"] = dyn_targets
                    
                # Recompute financial projections
                p["pipeline_setup_potential"] = p["leads_count"] * p["base_price_mur"]
                p["pipeline_yearly_maintenance_arr"] = p["leads_count"] * p["yearly_maintenance_mur"]
                p["total_year1_pipeline_potential"] = p["pipeline_setup_potential"] + p["pipeline_yearly_maintenance_arr"]

    total_leads = sum(p["leads_count"] for p in products)
    total_contacted = sum(p["contacted_count"] for p in products)
    total_setup_pipeline = sum(p["pipeline_setup_potential"] for p in products)
    total_arr_pipeline = sum(p["pipeline_yearly_maintenance_arr"] for p in products)
    total_year1_potential = sum(p["total_year1_pipeline_potential"] for p in products)
    
    return {
        "summary": {
            "total_leads": total_leads,
            "total_contacted": total_contacted,
            "total_setup_pipeline_mur": total_setup_pipeline,
            "total_annual_maintenance_arr_mur": total_arr_pipeline,
            "total_year1_potential_mur": total_year1_potential,
            "maintenance_fee_formula": "Yearly Maintenance = 1/5 (20%) of Total Solution Price",
            "three_year_aggregate_potential_mur": total_setup_pipeline + (total_arr_pipeline * 3)
        },
        "products": products
    }

def get_dedicated_fleets() -> Dict[str, Any]:
    """Returns the two 11-agent dedicated fleets."""
    return {
        "medical360_division": {
            "product_name": "Medical 360™ Turnkey Clinic Suite",
            "fleet_size": len(MEDICAL_360_FLEET),
            "base_price": 45000,
            "maintenance_contract_yearly": 9000,
            "agents": MEDICAL_360_FLEET
        },
        "enn_rev_enn_sourir_division": {
            "product_name": "Enn Rev Enn Sourir™ NGO & CSR Portal",
            "fleet_size": len(ENN_REV_ENN_SOURIR_FLEET),
            "base_price": 45000,
            "maintenance_contract_yearly": 9000,
            "agents": ENN_REV_ENN_SOURIR_FLEET
        }
    }
