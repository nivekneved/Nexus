"""
LeadScout-Core: CLI Runner
===========================
Recursive event-driven lead intelligence runner with rich terminal output.
"""

import asyncio
import argparse
import sys
from leadscout.core.orchestrator import RecursiveOrchestrator

def main():
    parser = argparse.ArgumentParser(description="LeadScout-Core: Recursive Event-Driven Lead Intelligence Engine")
    parser.add_argument("company", help="Target company name")
    parser.add_argument("domain", help="Target company domain")
    args = parser.parse_args()

    print(f"\n[LeadScout-Core Engine] Initializing recursive pipeline for target: {args.company} ({args.domain})...\n")

    orchestrator = RecursiveOrchestrator()
    card = asyncio.run(orchestrator.run_pipeline(args.company, args.domain))

    print("=" * 60)
    print(f"LEAD DOSSIER: {card.company_name}")
    print("=" * 60)
    print(f"Domain             : {card.domain}")
    print(f"Email Provider     : {card.email_provider}")
    print(f"MX Records         : {', '.join(card.mx_records)}")
    print(f"Tech Stack         : {', '.join(card.tech_stack)}")
    print(f"Staff Members      : {', '.join([s['name'] + ' (' + s['title'] + ')' for s in card.staff_members])}")
    print(f"Confirmed Emails   : {', '.join([e['email'] for e in card.confirmed_emails])}")
    print(f"Qualification Score: {card.qualification_score}% (Tier 1)")
    print(f"Completed Probes   : {len(card.completed_probes)} probes executed")
    print("=" * 60)
    print("✔ Lead card successfully saturated and committed!\n")

if __name__ == "__main__":
    main()
